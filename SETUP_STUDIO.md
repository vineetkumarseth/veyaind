# Studio setup guide: images, music, video

Slides work out of the box (your local model). Images, music and video need a **provider**,
because these models need a big GPU that a normal laptop or small server does not have.

## Why Replicate asked for money, and why you got a 404

- **Replicate is pay-as-you-go.** You can try a few models, but to keep using the API you add a payment
  method or prepaid credit. There is no large free-credit grant. Each run costs a small amount
  (the price is shown on every model page).
- **HTTP 404 = the model name was not found.** The name in `.env` must be exactly `owner/name`
  as shown on the model page, for example `black-forest-labs/flux-schnell`. A typo, a missing owner,
  or a model that was renamed gives 404. Open the model page on replicate.com, copy the name from the
  top of the page, paste it, restart Veya.
- Veya now shows a clear message for 401, 402, 403, 404, 422 and 429 in the Studio card.

## Option 1: free images with Cloudflare Workers AI (recommended to start)

Cloudflare's free plan includes a daily allowance for Workers AI, with no card needed to start.
The exact daily number changes, so check the current limit on Cloudflare's Workers AI pricing page.

1. Make a free account at https://dash.cloudflare.com
2. Copy your **Account ID** (shown on the Workers AI page / dashboard sidebar).
3. Create an **API token** (My Profile > API Tokens > Create Token). Use the "Workers AI" template if you
   see it, otherwise give it the Workers AI permission.
4. Add to `.env`, then restart Veya:

```
VEYA_IMAGE_PROVIDER=cloudflare
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_token
VEYA_LIMIT_IMAGE=5
```

The default model is `@cf/black-forest-labs/flux-1-schnell`. To use another Cloudflare image model, set
`VEYA_IMAGE_MODEL=` to its name from the Cloudflare model catalog.

## Option 2: images with Replicate (pay per image)

```
REPLICATE_API_TOKEN=r8_your_token
VEYA_IMAGE_PROVIDER=replicate
VEYA_IMAGE_MODEL=black-forest-labs/flux-schnell
VEYA_LIMIT_IMAGE=3
```

Before using any model: open its page, check the **price per run** and the **licence** (some models do not allow
commercial use).

## Music (paid provider needed)

No good free hosted music API exists, so keep a small prepaid balance on Replicate and set a low limit:

```
REPLICATE_API_TOKEN=r8_your_token
VEYA_MUSIC_PROVIDER=replicate
VEYA_MUSIC_MODEL=lucataco/ace-step
VEYA_LIMIT_MUSIC=2
```

`lucataco/ace-step` is an Apache-2.0 open model; at the time of writing its Replicate page showed roughly
3 cents per run. Check the page for the current price. If the model needs extra inputs (for example a duration),
add them as JSON: `VEYA_MUSIC_INPUT={"duration": 30}`.

## Video (most expensive, we suggest waiting)

Video costs the most per run. Turn it on only when you have paying users. To test once:

```
REPLICATE_API_TOKEN=r8_your_token
VEYA_VIDEO_PROVIDER=replicate
VEYA_VIDEO_MODEL=owner/model-name   # pick one on replicate.com and check price + licence
VEYA_LIMIT_VIDEO=1
```

## Run the models yourself?

You can, but it needs an NVIDIA GPU server (rented per hour), plus setup and upkeep. Not worth it until you have
regular users. Start with a provider, measure real usage, then decide.

## Keep costs under control

- `VEYA_LIMIT_IMAGE`, `VEYA_LIMIT_MUSIC`, `VEYA_LIMIT_VIDEO` = per user per day. Keep them small.
- If a job fails, the limit is given back to the user (already built in).
- Never put your provider token in the website code. It stays only in `.env` on the server.

## Quick fixes

| Message in the Studio card | What to do |
|---|---|
| HTTP 401 | Token wrong. Re-copy it, no spaces or quotes, restart. |
| HTTP 402 | Provider account needs billing or credit. |
| HTTP 403 | Token lacks permission, or the model needs terms accepted on its page. |
| HTTP 404 | Model name wrong. Copy `owner/name` from the model page. |
| HTTP 422 | Model needs extra settings. Use `VEYA_<KIND>_INPUT={...}`. |
| HTTP 429 | Provider rate limit. Wait a minute. |

## Responsible use

Tell people when media is AI-made, and add an abuse policy (no deepfakes of real people, no harmful content)
before you open Studio to the public.
