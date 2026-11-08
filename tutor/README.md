# Veya Code Tutor: your own coding-teacher model

**Goal:** a small model that explains coding in easy language, always in the same six parts (Idea, Visual, Code,
Step by step, Common mistake, Try it), and draws pictures (flow, chart, array, vars) that the Veya app shows.

## Be clear about what "your own model" means here

| Idea | Is it realistic? |
|---|---|
| Train a language model **from scratch** on your laptop | No. A from-scratch model needs billions of words and a GPU cluster. It would not be able to teach. |
| **Fine-tune** a small open model (LoRA) on good teaching examples | **Yes.** This is what this kit does. Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct` (Apache-2.0). |
| Use the big model + the tutor prompt (no training) | **Works today.** Pick the "Code tutor" mode in Veya. Do this first. |

So the real order is: (1) launch the tutor with the prompt, (2) collect good examples, (3) fine-tune only when the tuned
model is clearly better, or cheaper and faster, than the prompt version. An honest name is "Veya Tutor, fine-tuned from
Qwen2.5-Coder-1.5B". Do not describe it as trained from scratch.

## Steps

```
cd tutor
python seeds.py                      # writes data/seed.jsonl (10 gold examples, already checked)
python make_dataset.py generate --count 300 --model qwen3:8b    # your local model drafts examples; only valid ones are kept
python make_dataset.py review --n 10                            # READ them. Delete bad lines from data/raw.jsonl by hand.
python make_dataset.py build                                    # -> data/train.jsonl, data/val.jsonl
```
Generation is slow on a laptop (roughly a minute per example is normal). Let it run overnight; it can be stopped and
restarted, it skips what is done. The checker rejects answers with missing parts, broken Python, bad picture blocks or
Devanagari in Roman Hinglish, and answers that are off-topic. It cannot judge whether the teaching is *good*: that is why
you must read a sample yourself. Add your own best answers to `seeds.py`: ten great examples beat a hundred average ones.

**Training (GPU needed).** Use a free Google Colab or Kaggle GPU notebook:
```
pip install -r requirements-train.txt
python train_lora.py --smoke        # 3 steps, checks the setup (works on a Mac too, slowly)
python train_lora.py --epochs 3
python merge_export.py
```
Then copy `out/merged` to your Mac and run `bash export_gguf.sh` (needs git, python and Ollama). It creates the Ollama model
`veya-tutor`. In Veya's `.env` add `VEYA_TUTOR_MODEL=veya-tutor`, restart. The "Code tutor" mode now uses it.

**Judge it.**
```
python eval_tutor.py --model qwen3:8b      # baseline: big model + tutor prompt
python eval_tutor.py --model veya-tutor    # your tuned model
```
The score only checks format and code syntax. Also read the saved `eval_*.md` files. Ship the tuned model only if the
answers are clearly better, or nearly as good but much smaller and faster.

## Datasets
See `DATA_SOURCES.md` for where data can come from, what is verified, and what is not possible (for example, you cannot download Qwen3's training data).

## What was tested, and what was not
- Tested here: the validator (good and bad answers), all 10 gold examples (their Python runs and the traces are correct),
  the dataset pipeline against a fake teacher, the label masking and learning-rate schedule, and the picture rendering in the app.
- **Not tested here:** the actual training run, the merge, the GGUF conversion and `ollama create`. The sandbox had no GPU and no
  internet. Expect to fix small version issues on the first run (library versions change). If the chat template in `Modelfile`
  gives odd answers, copy the TEMPLATE from `ollama show qwen2.5-coder:1.5b --modelfile`.

## Data rules
- Use only examples you wrote, examples written by a model whose licence allows it (Qwen3 and Qwen2.5-Coder are Apache-2.0),
  or datasets whose licence allows your use. Do not copy tutorials from other websites.
- Never train on real students' chats without their clear consent.
