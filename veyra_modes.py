"""VEYRA: the central model-mode configuration.

VEYRA is ONE model family with three selectable intelligence modes (TARKA Core, Deep, Flash). They are NOT three
independently trained models: today only Core exists, and it runs Qwen3-8B (customized for Veya with prompts and, later,
fine-tuning). Deep and Flash are waitlist-only until a real checkpoint and configuration exist.

Everything that decides what a mode may do lives here: availability, model adapter, generation parameters, context
budget, tool permissions and usage restrictions. main.py enforces it on the server, so hiding a button in the
browser is never the only protection. To release a mode later: set its model (VEYA_DEEP_MODEL / VEYA_FLASH_MODEL) and
VEYA_MODE_DEEP=available (or FLASH) in .env. No frontend change is needed."""
import os
from dataclasses import dataclass

BRAND = "VEYRA"
FOUNDATION = "Qwen3-8B"
DEFAULT_MODE = "core"


class UnknownMode(Exception):
    pass


class ModeUnavailable(Exception):
    def __init__(self, mode: "Mode"):
        super().__init__(f"{mode.name} is not available yet. Join the waitlist to be told when it opens.")
        self.mode = mode


@dataclass(frozen=True)
class Mode:
    id: str
    name: str
    description: str
    status: str              # "available" or "waitlist"
    capabilities: tuple      # shown to users (planned capabilities for waitlist modes)
    adapter: dict            # which backend and checkpoint runs this mode
    generation: dict         # sampling and length options passed to the model server
    context_budget: dict     # how much history and input this mode may use
    tools: dict              # what this mode may use
    restrictions: dict       # usage limits

    @property
    def available(self) -> bool:
        return self.status == "available"

    def public(self) -> dict:
        """What the browser may see. Never includes adapter, parameters or limits."""
        return {"id": self.id, "name": self.name, "description": self.description, "status": self.status,
                "capabilities": list(self.capabilities), "selectable": self.available}


def _env_status(mode_id: str, default: str, model: str) -> str:
    """A mode only becomes available when it is switched on in .env AND has a model configured."""
    want = (os.getenv(f"VEYA_MODE_{mode_id.upper()}") or default).strip().lower()
    return "available" if want == "available" and model else "waitlist"


def build_modes() -> dict:
    ctx = int(os.getenv("VEYA_CTX") or 8192)
    max_msg = int(os.getenv("VEYA_MAX_MESSAGE") or 12000)
    core_model = os.getenv("VEYA_MODEL") or "qwen3:8b"
    deep_model = (os.getenv("VEYA_DEEP_MODEL") or "").strip()
    flash_model = (os.getenv("VEYA_FLASH_MODEL") or "").strip()
    all_tools = {"web_search": True, "weather": True, "documents": True, "memory": True, "code_run": True, "vision": True}
    modes = [
        Mode("core", "TARKA Core", "Balanced intelligence", "available",
             ("General AI assistance", "Programming education", "Code explanations and debugging", "Visual learning",
              "Mathematics and AI/ML education", "Normal reasoning"),
             {"provider": "ollama", "model": core_model},
             {"temperature": 0.7, "top_p": 0.8},
             {"history_messages": 10, "max_input_chars": max_msg, "num_ctx": ctx},
             all_tools, {"credits_per_message": 1}),
        Mode("deep", "TARKA Deep", "Advanced reasoning", _env_status("deep", "waitlist", deep_model),
             ("Complex problem-solving", "Advanced programming and algorithm analysis", "Multi-step reasoning workflows",
              "Mathematical and scientific problem-solving", "Additional verification and tool-assisted analysis"),
             {"provider": "ollama", "model": deep_model},
             {"temperature": 0.6, "top_p": 0.95, "think": True},
             {"history_messages": 16, "max_input_chars": max_msg, "num_ctx": max(ctx, 16384)},
             all_tools, {"credits_per_message": 3}),
        Mode("flash", "TARKA Flash", "Fast responses", _env_status("flash", "waitlist", flash_model),
             ("Short and quick answers", "Simple coding questions", "Fast concept explanations",
              "Quick revision and summaries", "Lower-latency response configuration"),
             {"provider": "ollama", "model": flash_model},
             {"temperature": 0.5, "top_p": 0.9, "num_predict": 400},
             {"history_messages": 4, "max_input_chars": 4000, "num_ctx": 4096},
             {**all_tools, "web_search": False, "vision": False, "code_run": False}, {"credits_per_message": 1}),
    ]
    return {m.id: m for m in modes}


def all_modes() -> dict:
    return build_modes()  # read from the environment each time, so a .env change plus restart is all a release needs


def resolve(mode_id: str | None) -> Mode:
    """Return the mode if it exists AND is available. Raises UnknownMode / ModeUnavailable otherwise."""
    modes = all_modes()
    m = modes.get((mode_id or DEFAULT_MODE).strip().lower())
    if m is None:
        raise UnknownMode(mode_id)
    if not m.available:
        raise ModeUnavailable(m)
    return m


def get(mode_id: str) -> Mode:
    """Return a mode (available or not). Raises UnknownMode."""
    m = all_modes().get((mode_id or "").strip().lower())
    if m is None:
        raise UnknownMode(mode_id)
    return m
