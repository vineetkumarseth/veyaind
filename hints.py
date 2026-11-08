"""Bhasha/script ka hint (main.py aur eval/run_eval.py dono yahi use karte hain, taaki test asli behaviour naape)."""
import re

HINGLISH_WORDS = set("""kal aaj subah raat shaam hai hain hoon tha nahi nahin kya kaise kyun kyon kaun kab kahan mujhe mera meri
mere tum tumhe tumhara aap aapko aapka yaar bhai batao bata dena karna karo jisse taaki aur mein chahiye sakta sakte
sakti raha rahi rahe bahut thoda accha achha theek paas liye isme uska unka jaldi neend uthna baje samajh nahi
padhna likho dikhao chalo abhi phir lekin kyunki toh bhi wala wali pasand kaam
ka ki ke ko kaisa kaisi rahega rahegi hoga hogi mausam barish kuch sab log nahin nahi kar karo kare rakho dijiye kijiye bataiye samjhao samjha banao banaiye parso chhatri lu leni jao kya hota hoti kisne kaunsa""".split())


def style_hint(text: str) -> tuple[str, str]:
    """Chhote model ko script/bhasha ka hint do: (system ke liye, user message ke peeche ke liye)."""
    if re.search(r"[\u0900-\u097F]", text):
        return "\nThe user wrote in Hindi (Devanagari). Reply in Hindi (Devanagari).", ""
    words = re.findall(r"[a-z']+", text.lower())
    if sum(w in HINGLISH_WORDS for w in words) >= 2 or "hinglish" in text.lower():
        return ("\nThe user wrote Roman Hinglish (Hindi in Latin letters). Reply ONLY in Roman Hinglish: simple everyday "
                "Hindi words, English for technical terms. First think about what the user really needs, then give a "
                "correct, practical, complete answer. For tips or steps use a numbered list with each point on its own "
                "line and one short sentence of reason. Never reply in English and never use Devanagari.",
                "\n\n(Roman Hinglish mein jawab do. Har point alag line mein, ek chhote reason ke saath.)")
    return "", ""
