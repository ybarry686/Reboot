import requests

from config import Config

GEMINI_URL_TMPL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
FALLBACK_MESSAGE = (
    "We couldn't reach the recommendation engine right now -- browse the "
    "studios below and compare services directly."
)


def get_recommendation(goal, studios, model="gemini-2.5-flash"):
    if not Config.GEMINI_API_KEY:
        return FALLBACK_MESSAGE
    if not studios:
        return "No studios matched yet -- try a broader search."

    studio_lines = "\n".join(
        f"- {s['name']}: {', '.join(sv['name'] for sv in s.get('services', [])) or 'services vary'}"
        for s in studios
    )
    prompt = (
        "A user is choosing a recovery service. Their goal: "
        f'"{goal}".\n\nHere are their nearby options:\n{studio_lines}\n\n'
        "In 2-3 sentences, recommend which option(s) best fit their goal "
        "and briefly say why. Be specific and concise, no bullet points."
    )

    url = GEMINI_URL_TMPL.format(model=model)
    try:
        resp = requests.post(
            url,
            params={"key": Config.GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        print(f"[gemini_client] recommendation failed: {exc}")
        return FALLBACK_MESSAGE