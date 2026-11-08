# Where to get training data for Veya (and what is NOT possible)

## Can I take the dataset that Qwen3-8B was trained on? No.
Qwen3 was pretrained on about **36 trillion tokens** in 119 languages (web pages, text pulled out of PDFs, and synthetic math and
code data made by earlier Qwen models), as described in Qwen's own announcement. Qwen publishes the **model weights** under
Apache-2.0. As far as I found, that 36-trillion-token dataset is not available to download. A trained model cannot be turned back
into its dataset. What you CAN legally do with Qwen3 (Apache-2.0):
1. **Fine-tune its weights** on your own data (this is what `train_lora.py` does). The result is your model, built on Qwen.
2. **Use it as a teacher**: let it write training examples, check them, and train another model on them (this is what
   `make_dataset.py` does). Read the licence of any *other* provider before doing this with their outputs; some forbid it.

## What you actually need for Veya
Not web-scale text. You need (1) **500 to 5,000 excellent tutor answers** (Hinglish and English), (2) a **question bank** with
answers you trust, (3) later, **learner logs** (with consent). Public text only matters if you pretrain a base model from scratch.

## Public datasets (checked from their own dataset pages or papers)
| Dataset | What it is | Licence as I found it | Use for |
|---|---|---|---|
| SmolLM-Corpus (`HuggingFaceTB/smollm-corpus`) | FineWeb-Edu-Dedup (about 220B tokens of educational web pages), Cosmopedia v2 (about 39M synthetic textbooks and stories written by Mixtral-8x7B-Instruct), Python-Edu (Python files taken from The Stack v2) | ODC-By; for Python-Edu follow The Stack v2's licence terms | Small-model pretraining or continued pretraining on education text |
| Aya Dataset (Cohere Labs / Aya initiative) | about 204K human-written prompt and answer pairs in 101 languages | Apache 2.0 per the listings I saw (confirm on the dataset card) | Multilingual instruction tuning |
| Aya_Hindi (`Cognitive-Lab/Aya_Hindi`) | Hindi slice of the Aya Collection | Apache 2.0 per its card; you must accept access conditions | Hindi instruction tuning |
| AI4Bharat IndicLLMSuite (Sangraha, IndicAlign) | 251B tokens of Indian-language text; 74.7M instruction pairs in 20 languages. Some parts are machine-translated or LLM-written | The paper says permissive; one summary says the repo has no clear licence. **Read each dataset card** | Hindi and Indian-language text |

## From memory, NOT re-checked today (verify the licence card before use)
Wikipedia dumps (CC BY-SA), Project Gutenberg books (public domain in the US), OpenAssistant OASST (Apache 2.0), The Stack v2 (BigCode,
permissively licensed code, access terms apply), TinyStories (small synthetic stories).

## Not found
I did not find a large, clean, verified **Roman-script Hinglish** dataset. Build your own (gold examples plus checked teacher drafts,
as in this kit). That also makes the data truly yours.

## Rules that save you later
- Write down the licence of every dataset you use, and keep that list.
- Non-commercial (NC) licences are for research only. Do not train the model you sell on them.
- Do not copy tutorials or answers from other websites.
- Never train on real students' conversations without clear consent.
- Hold out a test set that the model never trains on.
