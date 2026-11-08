# Veya (getveya.in)
Private AI assistant: apni API keys, local model (Ollama), per-user memory, dashboard.

## Chalana
1. Ollama install karo (ollama.com) aur chalu rakho.
2. `./run.sh` (pehli baar user banega aur API key ek hi baar dikhegi, save kar lo)
3. Browser: http://127.0.0.1:8000 -> key paste karo.

API: `POST /v1/chat` with `Authorization: Bearer sk-...` and `{"message": "..."}`

## Kya hai
- Hashed API keys, per-key rate limit (30/min)
- Chat history aur memories Fernet se encrypted (key: `.veya_key`, isse backup karo, kabhi share mat karo)
- Har query `user_id` se filter hoti hai, memory dekh/delete kar sakte ho
- Model: `VEYA_MODEL` env var se badlo (default qwen2.5:7b)

## Login
Dashboard par email+password se signup/login. Purana API-key wala account: "Use an API key" se login karo, phir API keys tab mein email+password jodo, taaki purani memory usi account mein rahe.
Google login: `.env.example` ko `.env` banao aur GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET bharo (redirect URI: http://127.0.0.1:8000/auth/google/callback). Jis email se password account bana hai, usse Google se nahi jud sakte (security ke liye).

## Chats, modes, settings
Sidebar mein New chat aur purani chats. Message ke neeche Copy, Read aloud, Try again; apne message par Copy aur Edit. Composer mein Mode: Default, Deep think (sirf qwen3), Coding, Study buddy, Short answers. Account menu (neeche naam par click): Settings, Memory, My files, API keys, Log out.

## Coding mode: code chalake check karna (optional)
`.env` mein `VEYA_ALLOW_RUN=1`, phir Settings mein checkbox. Veya ek Python script likhta hai (tests ke saath), use Mac par sandbox mein chalata hai (internet band, Desktop/Documents/Downloads aur is project folder padh nahi sakta), error aaye to khud theek karta hai (max 3 baar). Sirf macOS, sirf apne sawalon ke liye. Server par (multi-user) ise kabhi on mat karo, uske liye alag container chahiye.
Sandbox check: `python3 -c "from main import run_python; print(run_python('import urllib.request as u; print(u.urlopen(\"https://example.com\").status)'))"` ka jawab False hona chahiye (network band).

## Dosto ko try karwana (invite-only)
`.env` mein `VEYA_INVITE_CODE=koi-code` rakho, to signup (aur Google se naya account) bina code ke nahi banega. Link doge to Mac chalu, Ollama on, aur `VEYA_ALLOW_RUN=0` rakhna.

## Live data
Weather: message mein "mausam"/"weather" aur shehar ka naam ho to Veya Open-Meteo se abhi ka mausam laata hai (sirf shehar ka naam bahar jata hai). Shehar na likha ho to `.env` mein `VEYA_CITY` default. Band karne ke liye `VEYA_WEB_TOOLS=0`. Open-Meteo ki free API non-commercial use ke liye hai; startup ke commercial use se pehle unki terms/plan dekho.
Jawab ab token-by-token likhta hua dikhta hai (streaming). `VEYA_CTX=8192` context window hai.

## Web search (optional)
Chat mein **Web** button (globe). Key chahiye: Tavily (tavily.com) ya Serper (serper.dev), `.env` mein `TAVILY_API_KEY=` ya `SERPER_API_KEY=`, phir server restart. Button on ho to Veya tumhare sawal se ek chhoti English search query banata hai, sirf wahi provider ko jaati hai (chat, memory, documents nahi). Jawab ke neeche sources ke links aate hain. Roz ki limit `VEYA_WEB_LIMIT` (default 30 per user). Web ke natije untrusted text maane jaate hain. Button band ho to Sensex/score/khabar jaise sawal par Veya "live data nahi hai" bolta hai.

## Studio (slides, image, music, video)
Sidebar mein **Studio**. **Slides** apne aap chalti hain: topic likho, local model outline banata hai, `.pptx` download hota hai (internet nahi chahiye).
**Image, music, video** ke liye ek provider chahiye (khud ka GPU nahi): `.env.example` mein Studio section dekho. Replicate ek token se teeno chala sakta hai (model ka naam unke catalog se chuno), OpenAI sirf image ke liye. Har user ki roz ki limit hai. Files encrypted save hoti hain, sirf banane wale ko dikhti hain.
Cloud par daalne ke liye `DEPLOY.md`.

## Photos
Chat mein + dabao: photo upload ya camera. Photo samajhne ke liye vision model chahiye (ollama pull llama3.2-vision:11b); Veya apne aap use chunta hai. Photo se pehle baaki bade models memory se hata diye jaate hain. Agar photo par error aaye to .env mein `VEYA_VISION_MODEL=llava:latest` (halka model) daalo.

## Documents
Chat mein Attach ya Documents tab: PDF, DOCX, TXT, MD, CSV upload karo, phir sawal poochho. Files encrypted store hoti hain, aur sirf tumhare account mein dikhti hain. Cutoff: `VEYA_DOC_SIM` (default 0.5).

## Models
Chat ke upar model dropdown: Ollama ke installed models. Default `VEYA_MODEL` (main.py mein llama3.1:8b).

## Voice
'Talk' button: mic se bolo. Sunna: faster-whisper (offline, pehli baar ~500 MB model download). Bolna: Mac ki built-in awaaz (Lekha Hindi, Rishi English-India). Sirf Mac par.
`VEYA_STT=base` (tez, kam accurate), `VEYA_STT_LANG=hi` (language fix karo).

## New interface, credits and long messages
- The interface now has a sidebar (New chat, Library, Search with Ctrl/Cmd+K, Studio), a greeting home screen, a mode/model menu in the composer, tables with copy/CSV/full-screen, a Billing page and dark/light themes.
- Long messages: the chat limit is now 12000 characters (`VEYA_MAX_MESSAGE`) and the Studio prompt limit is 8000. Very long messages automatically keep less old chat so the context window does not overflow.
- Credits: set `VEYA_DAILY_CREDITS=20` in `.env` to give each user 20 chat messages a day. The sidebar shows the credits left. Blank = unlimited. A failed reply gives the credit back.
- Billing page: plans are placeholders (edit `PLANS` near the top of `static/index.html`). "Upgrade" does not take payment; it saves a "notify me" request (table `waitlist`), so you can see which plan people want.
- Studio: free images via Cloudflare Workers AI, clearer provider errors, and an in-app setup guide. See `SETUP_STUDIO.md`.
- Slides: your instructions in the prompt (for example "guide only, no questions and answers") are now followed, with a Short bullets / More detail choice.

## Code tutor mode and your own tutor model
- Pick **Code tutor** in the mode menu (or the "Learn coding" chip). Veya teaches in six parts and draws pictures: flow charts, arrays, variables and bar charts, drawn by the app itself (no internet or libraries). Each picture can be saved as SVG or PNG.
- `VEYA_TUTOR_MODEL=veya-tutor` makes that mode use your own fine-tuned model once you have trained one. See `tutor/README.md` (fine-tuning kit, not tested end to end in the sandbox).
- `VEYA_MODELS=qwen3:8b` shows only the models you want in the model menu. It does not delete anything. Remove extra models yourself with `ollama rm <name>`, but keep the embedding model (`nomic-embed-text`): memory and file search need it.
- Studio shows only **Slides** unless you configure an image, music or video provider (they need paid services; see `SETUP_STUDIO.md` if you ever want them).
- Slides can now use one of your uploaded files (for example your resume): choose it in Studio > Slides.

## VEYRA model modes, simulator and tests
- **VEYRA** is the model family. **TARKA Core** (Qwen3-8B, customized for Veya) is the only available mode. **TARKA Deep** and **TARKA Flash** are waitlist-only: users can join or leave the waitlist from the model menu in the composer. The server refuses requests for a waitlisted mode (HTTP 403), whatever the browser sends. Settings live in `veyra_modes.py`. To release a mode later set `VEYA_DEEP_MODEL` and `VEYA_MODE_DEEP=available` (same for Flash) in `.env`.
- New API: `GET /v1/veyra/modes`, `POST /v1/veyra/waitlist`, `DELETE /v1/veyra/waitlist/{mode}`, `GET/POST /v1/privacy/consents`; chat requests accept `veyra` (default `core`) and `show_context`.
- Database changes are applied by `migrations.py` on start (tables `model_waitlist`, `consents`). Existing data is kept.
- Code tutor pictures: `sim` (step-by-step simulator, computed by the app), `complexity` (calculated Big-O numbers), plus flow, array, variables, chart and svg.
- Run the tests: `python -m unittest discover -s tests -t . -v` (needs Node.js for the simulator tests; the HTTP tests need `pip install -r requirements.txt`). Regression suite: `python eval/tutor_regression/run_regression.py --selftest`, then `--model qwen3:8b --release r1` with Ollama running. See `docs/AUDIT_CODE_TUTOR.md`.

## Do my customers need Ollama? No.
Ollama is the engine that runs the AI model, and it must run on the computer where the Veya **server** runs. On your Mac, that is your Mac, so Ollama must be open (`run.sh` now starts it for you; you can also add Ollama to System Settings > General > Login Items). When Veya is hosted on a website, only your server needs a model engine (Ollama on a GPU server, or a hosted model API). Customers only open the website in a browser and install nothing. See `DEPLOY.md`.

## Web search, Thinking panel, photos, diagrams and greetings
- **Web search is manual:** it runs only when you ask for it. Turn on the **Web** button for a chat (it is off again in a new chat or after a reload, so it can never stay on by mistake). If you ask for something live (a price, a score) while Web is off, Veya says it has no live data and shows a one-tap **Search the web** button. In Settings you can choose to let Veya search by itself when a question clearly needs fresh information. That is off for everybody by default, and `VEYA_AUTO_WEB=0` removes the option. The Web button is hidden when the server has no search key (`TAVILY_API_KEY` or `SERPER_API_KEY`). The daily search limit (`VEYA_WEB_LIMIT`) still applies.
- **Greetings:** the home screen greets you by the time of day and changes between visits (for example "Welcome, night owl, Vineet." late at night).
- **Thinking panel:** while Veya works, a "Thinking..." line shows live steps (reading the question, searching the web, writing the answer). Tap it to open. When the answer is ready it becomes "Thought for N s". In Deep think mode it also shows the model's own reasoning text. The steps are saved with the message.
- **Photos:** an attached photo is shown as a small attachment tile (a 320 px preview is saved, encrypted, with the message, up to 4 per message) instead of the text "[photo attached]".
- **Diagrams in every mode:** flow charts, charts and the new `network` picture (layers of nodes with weights, for neural networks and associative memories) work in all modes, not only in Code tutor.

## Abhi nahi hai
Offline installer, Postgres+pgvector, billing, HTTPS (deploy ke waqt Caddy lagao).
Memories ke embeddings (numbers) plain store hote hain; text encrypted hai.
