"""Bounded model calls; persistent accounting; never restarts services."""
import os
import requests
from config import CONFIG

def generate(role, prompt, store):
    cfg = CONFIG["referee"]
    key = os.environ.get(cfg["api_key_env"]) if role == "referee" and cfg["enabled"] else None
    if key:
        reservation = store.reserve(cfg["reserve_per_call_usd"], cfg["budget_usd"])
        if reservation:
            try:
                r = requests.post(cfg["base_url"] + "/chat/completions",
                    headers={"Authorization": "Bearer " + key},
                    json={"model": cfg["model"], "messages": [{"role": "user", "content": prompt}],
                          "max_tokens": cfg["max_tokens"], "stream": False},
                    timeout=(10, cfg["timeout_s"]))
                r.raise_for_status()
                response = r.json()
                usage = response.get("usage", {})
                actual = usage.get("cost")
                if actual is None and "prompt_tokens" in usage and "completion_tokens" in usage:
                    actual = (usage["prompt_tokens"] * cfg["price_in_per_mtok"] +
                              usage["completion_tokens"] * cfg["price_out_per_mtok"]) / 1e6
                store.settle(reservation, actual)
                return response["choices"][0]["message"]["content"], {
                    "provider": cfg["base_url"], "model": cfg["model"], "usage": usage,
                    "cost_is_estimate": "cost" not in usage}
            except (requests.RequestException, ValueError, KeyError, IndexError) as e:
                store.settle(reservation, None)
                raise RuntimeError("Referee API call failed; reservation retained") from e
    cfg = CONFIG["worker"]
    try:
        r = requests.post(cfg["base_url"] + "/api/generate",
            json={"model": cfg["model"], "prompt": prompt, "stream": False, "think": False,
                  "format": "json",
                  "options": {"num_predict": cfg["max_tokens"], "num_ctx": 16384,
                              "temperature": 0.3 if role == "referee" else 0.7}},
            timeout=(10, cfg["timeout_s"]))
        r.raise_for_status()
        response = r.json()
        text = response.get("response")
        if not isinstance(text, str) or not text.strip(): raise ValueError("Empty model response")
        return text, {"provider": cfg["base_url"], "model": cfg["model"],
                      "done_reason": response.get("done_reason"), "eval_count": response.get("eval_count"),
                      "referee_fallback_local": role == "referee"}
    except (requests.RequestException, ValueError, KeyError) as e:
        raise RuntimeError("Local model unavailable; no service was restarted") from e
