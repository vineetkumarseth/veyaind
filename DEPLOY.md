# Veya ko cloud par daalna (getveya.in)

**Pehle ye padho:** Docker wali files maine bina Docker chalaye likhi hain (mere paas Docker nahi tha). Pehli baar tumhare server par chalengi, to chhoti dikkat aa sakti hai. Error ka text bhej do.

## Kya chahiye
1. **Domain** (getveya.in): registrar se kharido. Pehle trademark check (IP India ki free search).
2. **Ek chhota server (VPS)**, Ubuntu, 2 GB RAM se shuru. Veya ka app (login, chat, studio) CPU par chal jata hai.
3. **AI model kahan chalega** (sabse bada faisla, neeche table).
4. Firewall: sirf port 22 (SSH), 80, 443 khule.

## AI model kahan chalega
| Raasta | Kaise | Kharcha kiska |
|---|---|---|
| A. Apna GPU server | Ollama ek GPU server par (`OLLAMA_URL=http://gpu-server:11434` .env mein) | GPU ka kiraya (ghante ya mahine), chahe user ho ya na ho |
| B. Hosted model API | Abhi Veya sirf Ollama API bolta hai. OpenAI-compatible adapter alag se banana padega | Per-use, user ke hisaab se |
| C. Sirf Studio providers | Image/music/video ke liye Replicate ya OpenAI ki key (.env) | Per image/video, isliye limits lagi hain |

Chat ke liye A ya B zaroori hai. Studio (image, music, video) ke liye C. Slides ke liye apna chat model hi chalta hai.

## Steps (server par)
```bash
# 1. Docker lagao (Docker ke official steps dekho), code copy karo
scp veya.zip user@SERVER_IP:~ ; ssh user@SERVER_IP
unzip veya.zip && cd veya

# 2. .env banao
cp .env.example .env && nano .env
#   DOMAIN=getveya.in
#   VEYA_BASE_URL=https://getveya.in
#   VEYA_INVITE_CODE=koi-lamba-code        (jab tak public launch nahi)
#   VEYA_ALLOW_RUN=0                       (server par kabhi 1 mat karna)
#   OLLAMA_URL=http://GPU_SERVER:11434
#   keys: TAVILY_API_KEY, REPLICATE_API_TOKEN ... (jo chahiye)

# 3. DNS: domain ka A record server ke IP par. Phir:
docker compose up -d --build
docker compose logs -f veya
```
Browser: https://getveya.in (HTTPS Caddy khud laata hai).

## Backup (har hafte, zaroori)
`veya-data` volume mein database, `.veya_key` (iske bina sab data bekaar) aur media hai.
```bash
docker run --rm -v veya_veya-data:/data -v $PWD:/backup alpine tar czf /backup/veya-backup.tgz /data
```
Backup ko server se alag jagah rakho.

## Launch se pehle (sirf code se nahi hota)
- **Privacy Policy aur Terms** page (kya save hota hai, kaun dekh sakta hai). India ka DPDP Act dekho.
- **AI galat bol sakta hai** (sehat, paise, kanoon par khaaskar): ye saaf likho.
- **Image/video/music:** provider ki safety policy aur apni abuse policy (deepfake, nafrat, bachchon se jude), aur AI-generated media ko AI se bana batana.
- **Kharcha:** `VEYA_LIMIT_IMAGE`, `VEYA_LIMIT_VIDEO`, `VEYA_WEB_LIMIT` roz ki limit hain. Pehle chhoti rakho.
- **Voice reply (bolna)** abhi sirf Mac par chalta hai; Linux server par text hi aayega.
- **Mausam (Open-Meteo)** ki free API sirf non-commercial hai; customers ko dene se pehle unka commercial plan.
- Security: server update rakho, SSH key login, `.env` kisi ko mat do, monitoring.
