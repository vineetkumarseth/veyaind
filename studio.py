"""Veya Studio: slides (PPTX), image, music, video generation.
Slides apne aap (local) banti hain. Image/music/video ke liye ek provider chahiye (key .env mein):
  OpenAI-compatible (sirf image) ya Replicate (image, music, video).
Yahan sirf pure functions hain (database/login main.py mein)."""
import io
import json
import os
import re
import socket
import time
from ipaddress import ip_address
from urllib.parse import urlparse

import httpx

KINDS = ("image", "music", "video")
LIMITS = {"slides": 20, "image": 10, "music": 5, "video": 2}  # ek user ke liye roz (VEYA_LIMIT_<KIND> se badlo)
MAX_BYTES = 120_000_000


def daily_limit(kind: str) -> int:
    try:
        return int(os.getenv(f"VEYA_LIMIT_{kind.upper()}", LIMITS[kind]))
    except ValueError:
        return LIMITS[kind]


def provider(kind: str) -> tuple[str, str]:
    """(provider, model) agar ready hai, warna ('', '')."""
    p = os.getenv(f"VEYA_{kind.upper()}_PROVIDER", "").strip().lower()
    model = os.getenv(f"VEYA_{kind.upper()}_MODEL", "").strip()
    if p == "openai" and kind == "image" and os.getenv("OPENAI_API_KEY") and model:
        return p, model
    if p == "replicate" and os.getenv("REPLICATE_API_TOKEN") and model:
        return p, model
    if p == "cloudflare" and kind == "image" and os.getenv("CLOUDFLARE_API_TOKEN") and os.getenv("CLOUDFLARE_ACCOUNT_ID"):
        return p, model or "@cf/black-forest-labs/flux-1-schnell"
    return "", ""


def status() -> dict:
    out = {"slides": {"ok": True, "limit": daily_limit("slides")}}
    for k in KINDS:
        p, m = provider(k)
        out[k] = {"ok": bool(p), "provider": p, "model": m, "limit": daily_limit(k)}
    return out


def _extra_input(kind: str) -> dict:
    try:
        v = json.loads(os.getenv(f"VEYA_{kind.upper()}_INPUT", "") or "{}")
        return v if isinstance(v, dict) else {}
    except json.JSONDecodeError:
        return {}


def safe_url(url: str) -> bool:
    """Provider ke URL se file khinchte waqt local/private network par jaane se roko."""
    u = urlparse(url)
    if u.scheme != "https" or not u.hostname:
        return False
    try:
        ip_address(u.hostname)
        return False  # seedha IP address nahi
    except ValueError:
        pass
    if u.hostname == "localhost" or u.hostname.endswith((".local", ".internal")):
        return False
    try:
        for _, _, _, _, sa in socket.getaddrinfo(u.hostname, 443):
            ip = ip_address(sa[0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return False
    except OSError:
        return False
    return True


def download(url: str) -> tuple[bytes, str]:
    if not safe_url(url):
        raise RuntimeError("Provider ka file link surakshit nahi laga, isliye download nahi kiya.")
    with httpx.stream("GET", url, timeout=120, follow_redirects=False) as r:
        r.raise_for_status()
        data = b""
        for chunk in r.iter_bytes():
            data += chunk
            if len(data) > MAX_BYTES:
                raise RuntimeError("Generated file bahut badi hai.")
        return data, r.headers.get("content-type", "").split(";")[0].strip()


EXT = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "audio/mpeg": "mp3", "audio/wav": "wav", "audio/x-wav": "wav", "audio/flac": "flac",
       "audio/ogg": "ogg", "video/mp4": "mp4", "video/webm": "webm"}
DEFAULT_MIME = {"image": ("image/png", "png"), "music": ("audio/mpeg", "mp3"), "video": ("video/mp4", "mp4")}


def _finish(kind: str, data: bytes, mime: str, url: str = "") -> tuple[bytes, str, str]:
    if mime not in EXT:
        m = re.search(r"\.(png|jpe?g|webp|mp3|wav|flac|ogg|mp4|webm)(?:\?|$)", url, re.I)
        ext = (m.group(1).lower().replace("jpeg", "jpg") if m else DEFAULT_MIME[kind][1])
        mime = next((k for k, v in EXT.items() if v == ext), DEFAULT_MIME[kind][0])
    return data, mime, EXT[mime]


def _openai_image(prompt: str, model: str) -> tuple[bytes, str, str]:
    base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    r = httpx.post(f"{base}/images/generations", json={"model": model, "prompt": prompt, "size": os.getenv("VEYA_IMAGE_SIZE", "1024x1024"), "n": 1, **_extra_input("image")},
                   headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}, timeout=180)
    r.raise_for_status()
    item = r.json()["data"][0]
    if item.get("b64_json"):
        import base64
        return _finish("image", base64.b64decode(item["b64_json"]), "image/png")
    data, mime = download(item["url"])
    return _finish("image", data, mime, item["url"])


def _sniff(data: bytes) -> str:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return "image/png"


def _cloudflare_image(prompt: str, model: str) -> tuple[bytes, str, str]:
    """Cloudflare Workers AI REST API. FLUX models answer JSON with base64, SDXL answers raw image bytes."""
    import base64
    acct = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    r = httpx.post(f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{model}", json={"prompt": prompt, **_extra_input("image")},
                   headers={"Authorization": "Bearer " + os.environ["CLOUDFLARE_API_TOKEN"]}, timeout=120)
    r.raise_for_status()
    ctype = r.headers.get("content-type", "").split(";")[0].strip()
    if ctype.startswith("image/"):
        return _finish("image", r.content, ctype)
    d = r.json()
    b64 = (d.get("result") or {}).get("image")
    if not b64:
        raise RuntimeError("Cloudflare did not return an image. " + str(d.get("errors") or "")[:200])
    raw = base64.b64decode(b64)
    return _finish("image", raw, _sniff(raw))


HTTP_HINTS = {
    401: "The provider rejected your key. Check the token in .env (no spaces, no quotes) and restart.",
    402: "The provider account needs billing or credit. Add a payment method there, or switch to a free provider (see SETUP_STUDIO.md).",
    403: "The provider refused this request. The token may lack permission, or the model needs terms accepted on its page.",
    404: "Model not found. Check the model name in .env (owner/name, exactly as on the provider's model page).",
    422: "The model rejected the input. It may need extra settings: see VEYA_<KIND>_INPUT in .env.example.",
    429: "Provider rate limit hit. Wait a minute and try again.",
}


def _replicate(kind: str, prompt: str, model: str) -> tuple[bytes, str, str]:
    hdr = {"Authorization": "Bearer " + os.environ["REPLICATE_API_TOKEN"]}
    inp = {"prompt": prompt, **_extra_input(kind)}
    if ":" in model:  # owner/name:version
        r = httpx.post("https://api.replicate.com/v1/predictions", json={"version": model.split(":", 1)[1], "input": inp}, headers=hdr, timeout=120)
    else:
        r = httpx.post(f"https://api.replicate.com/v1/models/{model}/predictions", json={"input": inp}, headers={**hdr, "Prefer": "wait"}, timeout=120)
    r.raise_for_status()
    d = r.json()
    get_url = (d.get("urls") or {}).get("get", "")
    t0 = time.time()
    while get_url and d.get("status") in ("starting", "processing") and time.time() - t0 < int(os.getenv("VEYA_JOB_TIMEOUT", "900")):
        time.sleep(3)
        g = httpx.get(get_url, headers=hdr, timeout=30)
        g.raise_for_status()
        d = g.json()
    if d.get("status") != "succeeded":
        raise RuntimeError(f"Provider ne kaam poora nahi kiya (status: {d.get('status')}). {str(d.get('error') or '')[:200]}")
    out = d.get("output")
    url = out[0] if isinstance(out, list) and out else out
    if isinstance(url, dict):
        url = next((v for v in url.values() if isinstance(v, str) and v.startswith("http")), "")
    if not isinstance(url, str) or not url:
        raise RuntimeError("Provider ne koi file nahi di.")
    data, mime = download(url)
    return _finish(kind, data, mime, url)


def generate(kind: str, prompt: str) -> tuple[bytes, str, str]:
    """(bytes, mime, ext). Error par RuntimeError (key kabhi message mein nahi)."""
    p, model = provider(kind)
    if not p:
        raise RuntimeError(f"No provider is set for {kind}. See SETUP_STUDIO.md.")
    try:
        if p == "openai":
            return _openai_image(prompt, model)
        if p == "cloudflare":
            return _cloudflare_image(prompt, model)
        return _replicate(kind, prompt, model)
    except RuntimeError:
        raise
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        hint = HTTP_HINTS.get(code, "").replace("<KIND>", kind.upper())
        raise RuntimeError(f"Provider error HTTP {code}. {hint} ({(e.response.text or '')[:140].replace(chr(10), ' ')})")
    except Exception as e:
        raise RuntimeError(f"Provider se baat nahi ho paayi ({type(e).__name__}).")


# ---------- slides ----------
def clean_outline(o: dict, n: int) -> dict:
    title = str(o.get("title", "")).strip()[:100]
    slides = []
    for s in (o.get("slides") or [])[:20]:
        if not isinstance(s, dict) or not str(s.get("title", "")).strip():
            continue
        bullets = [str(b).strip()[:180] for b in (s.get("bullets") or []) if str(b).strip()][:7]
        slides.append({"title": str(s["title"]).strip()[:90], "bullets": bullets, "notes": str(s.get("notes", "")).strip()[:1000]})
    if not title or not slides:
        raise ValueError("outline khali hai")
    return {"title": title, "slides": slides[: max(1, min(n, 20))]}


def build_pptx(outline: dict) -> bytes:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt
    teal, ink, mute = RGBColor(0x0A, 0x3A, 0x44), RGBColor(0x14, 0x23, 0x2B), RGBColor(0x5D, 0x6F, 0x78)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]

    def box(slide, x, y, w, h):
        tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
        tf.word_wrap = True
        return tf

    s = prs.slides.add_slide(blank)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = teal
    tf = box(s, 0.9, 2.3, 11.5, 2.2)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = outline["title"]
    p.font.size, p.font.bold, p.font.color.rgb = Pt(44), True, RGBColor(255, 255, 255)
    p2 = box(s, 0.9, 4.7, 11.5, 0.6).paragraphs[0]
    p2.text = "Made with Veya"
    p2.font.size, p2.font.color.rgb = Pt(18), RGBColor(0xB8, 0xD8, 0xDE)

    for i, sl in enumerate(outline["slides"], 1):
        s = prs.slides.add_slide(blank)
        bar = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.25), Inches(7.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = teal
        bar.line.fill.background()
        p = box(s, 0.8, 0.5, 11.8, 1.1).paragraphs[0]
        p.text = sl["title"]
        p.font.size, p.font.bold, p.font.color.rgb = Pt(34), True, teal
        tf = box(s, 0.9, 1.9, 11.5, 4.9)
        for j, b in enumerate(sl["bullets"] or [""]):
            para = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            para.text = ("•  " + b) if b else ""
            para.font.size, para.font.color.rgb = Pt(24), ink
            para.space_after = Pt(12)
        n = box(s, 12.2, 6.9, 0.8, 0.4).paragraphs[0]
        n.text, n.alignment = str(i), PP_ALIGN.RIGHT
        n.font.size, n.font.color.rgb = Pt(12), mute
        if sl["notes"]:
            s.notes_slide.notes_text_frame.text = sl["notes"]
    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()
