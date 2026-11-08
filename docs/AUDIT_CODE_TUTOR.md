# Veya Code Tutor: audit, fixes and what is still open

Scope: the code in this repository, read and tested in a sandbox with no GPU, no Ollama and no real FastAPI (stand-in libraries for
the backend tests, a real Chromium browser for the interface). **No real qwen3:8b answers were produced or checked here.** Anything
about what the model will say is therefore a design and a test harness, not a measured result.

## 1. Findings and fixes

| # | Finding | Where | Status |
|---|---|---|---|
| 1 | Algorithm "traces" were written by the AI (array pointer blocks, numbers in Step by step) and could be wrong | `tutor_prompt.py`, `tutor/seeds.py`, `static/index.html` | **Fixed.** New `sim` block: the app runs the real algorithm (`SimEngine`) and draws every step. The prompt forbids hand-written traces; the validator rejects them next to a sim |
| 2 | No Play, Pause, Step back, Reset or Speed; diagrams were still pictures | `static/index.html` | **Fixed** for bubble, selection and insertion sort, linear and binary search, and factorial (call stack). Other algorithms are not covered yet |
| 3 | Big-O chart numbers were typed by the AI | `tutor/seeds.py` | **Fixed.** New `complexity` block: the app calculates the values |
| 4 | Gold example taught "a variable is a box that holds a value" (misleading for Python) | `tutor/seeds.py` | **Fixed.** Names point to objects; `vars` diagrams draw name to object arrows, `same_as` shows two names on one object |
| 5 | Gold factorial used `if n == 1`: `factorial(0)` recurses forever | `tutor/seeds.py` | **Fixed** (`n <= 1`), with a regression case and engine tests for n = 0 to 12 and invalid n |
| 6 | Gold bubble sort ran one pass but was described as sorting | `tutor/seeds.py` | **Fixed** (full sort, code prints the sorted list, verified by running it) |
| 7 | XOR, Transformer and memory-model claims depend on the model | `tutor_prompt.py` | **Mitigated, not solved.** Fact guardrails in the prompt and regression cases nn01, tf02, py01. A prompt lowers errors; it cannot guarantee correctness |
| 8 | Code in answers was never checked | `main.py` (`check_code_blocks`), UI badges | **Fixed in part.** When `VEYA_ALLOW_RUN` is on and a sandbox exists, every Python block is run and the result is shown. "Ran without errors" does not mean the explanation is right. Not run: code that needs `input()`, or servers without a sandbox. Today's sandbox is macOS-only |
| 9 | Personal memories were injected into every prompt, including tutoring | `main.py` | **Fixed.** No memories in tutor mode |
| 10 | The text of used memories was returned, stored next to each message and shown under answers | `main.py`, UI | **Fixed.** Only a count is returned and stored. Text only with `show_context`. Old stored texts are stripped from the history API |
| 11 | Tutoring chats were mined for "facts about the user" after every message | `main.py` (`learn`) | **Fixed.** Skipped in tutor mode, so learning history and personal memory stay separate |
| 12 | Document isolation | `main.py` | **Checked, correct.** `doc_search`, `doc_text` and deletes are filtered by `user_id`; covered by a test |
| 13 | No consent record for using student data in training | `migrations.py`, `main.py` | **Added** `consents` table, `/v1/privacy/consents`, a Settings switch (off by default) and `training_export_allowed(uid)`. No export code exists; any future export must call that guard |
| 14 | Short replies could flip the chat language and lose the topic | `main.py` | **Fixed** for tutor mode: the language is taken from the last user messages and a "current learning objective" line is added |
| 15 | Adaptive tutoring is only prompt rules | `tutor_prompt.py` | **Open.** Quiz rules (one question, no answer leak, judge what was written, change strategy after two misses) are in the prompt and in 3 regression cases. There is no server-side quiz state or deterministic grading yet |
| 16 | Read-aloud buttons could overlap and could not be stopped | `static/index.html` | **Fixed.** One speaker for the whole app; tap again to stop |
| 17 | Found while testing: the step slider snapped back; insertion sort showed a duplicate value | `static/index.html` | **Fixed** (the insertion key is lifted out and its gap shown) |
| 18 | Default model in code was llama3.1:8b while the brand says Qwen3-8B | `main.py`, `veyra_modes.py` | **Fixed** (default qwen3:8b) |

## 2. Architecture now
- `SimEngine` (inside `static/index.html`, between `SIM-ENGINE-START/END` markers): pure functions that return a list of steps with array, comparisons, swaps, pointers, variables and counters. The player only draws steps.
- Reference tests (`tests/test_sim_engine.py`): the engine is loaded in Node and compared with independent Python implementations: final result, operation counts, a binary-search invariant at **every** iteration, factorial for n = 0 to 12, rejection of invalid input.
- Visual specs are validated twice: in the app before drawing (a bad spec shows an error, not a picture) and in `tutor/validate.py` for training data and evaluation.
- `veyra_modes.py` holds model modes; `migrations.py` holds versioned schema steps.

## 3. Regression suite (`eval/tutor_regression`)
55 fixed cases in 13 categories; checks are grouped into six dimensions (technical accuracy, execution correctness, visual correctness, teaching quality, adaptive behaviour, privacy and context). `run_regression.py --model NAME --release R` records one line per release in `releases.jsonl` and saves every answer for human reading. The checkers were tested offline with good and bad canned answers (13 scenarios). **The suite has not been run against a real model.** Automatic checks are a floor; teaching quality still needs a human reader.

## 4. Still open, in priority order
1. Run `run_regression.py` on your Mac for `qwen3:8b` and record the first baseline.
2. Server-side practice sessions: concept map, question bank with deterministic grading, an attempts log and misconception evidence (blueprint phase 2).
3. SQL join visual (source tables and joined result) and a neural-network forward-propagation widget; neither exists yet.
4. A multi-user code sandbox (containers) or in-browser Python (Pyodide). Today's runner is for one trusted user.
5. More simulators: stack and queue, BFS and DFS, CPU scheduling, paging.
6. Human rating of teaching quality for each release (fill `human_review` in `releases.jsonl`).
