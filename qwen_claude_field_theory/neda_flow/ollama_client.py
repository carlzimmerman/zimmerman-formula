#!/usr/bin/env python3
"""Ollama client for the autoresearch loop. Local only; no cloud APIs; no silent model substitution."""
import json, os, urllib.request, urllib.error, time

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("QWEN_MODEL", "Qwen-Physics")   # Carl's local model; override via env only
TIMEOUT = int(os.environ.get("QWEN_TIMEOUT", "900"))


class OllamaUnavailable(RuntimeError):
    pass


def verify():
    """Startup check: server reachable AND requested model installed. Raise otherwise (record + exit
    BLOCKED upstream; never pretend research occurred)."""
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=10) as r:
            tags = json.load(r)
    except Exception as e:
        raise OllamaUnavailable(f"Ollama not reachable at {OLLAMA_URL}: {e}")
    names = [m.get("name", "") for m in tags.get("models", [])]
    if not any(n == MODEL or n.split(":")[0] == MODEL for n in names):
        raise OllamaUnavailable(f"model '{MODEL}' not installed; found: {names}")
    return True


def chat(system, user, temperature=0.7, max_retries=3):
    """One chat call. Returns assistant text. Retries transient failures; raises on hard failure."""
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": int(os.environ.get("QWEN_CTX", "16384")),
                    "num_predict": int(os.environ.get("QWEN_PREDICT", "8000"))},  # room for think+answer
    })
    _b = json.loads(payload)
    if os.environ.get("QWEN_THINK", "0") == "1":
        _b["think"] = True
    payload = json.dumps(_b).encode()
    body = json.loads(payload.decode())
    last = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(f"{OLLAMA_URL}/api/chat",
                                         data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                out = json.load(r)
            return out["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 400:   # payload field rejected OR context overflow: adapt and retry immediately
                try:
                    err_body = e.read().decode()
                except Exception:
                    err_body = ""
                # context overflow (prompt > num_ctx): raise num_ctx to fit prompt + predict headroom (capped).
                # keeps the loop robust as the architect context (knowledge graph, dead classes) grows.
                if "context" in err_body.lower() or "n_prompt_tokens" in err_body:
                    import re as _re
                    m = _re.search(r'"n_prompt_tokens"\s*:\s*(\d+)', err_body)
                    cur = body.setdefault("options", {}).get("num_ctx", 16384)
                    need = int(m.group(1)) if m else cur * 2
                    pred = body["options"].get("num_predict", 8000)
                    newctx = min(int(os.environ.get("QWEN_CTX_CAP", "40960")), need + pred + 1024)
                    if newctx > cur:
                        body["options"]["num_ctx"] = newctx; continue
                if "think" in body:
                    body.pop("think"); continue
                if "num_predict" in body.get("options", {}):
                    body["options"].pop("num_predict"); continue
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            last = e
            time.sleep(5 * (attempt + 1))
    raise OllamaUnavailable(f"chat failed after {max_retries} attempts: {last}")


def extract_json(text):
    """Pull the first top-level JSON object out of a model reply (handles ```json fences and prose).
    Returns dict or None. Never guesses: if it doesn't parse, the candidate is rejected upstream."""
    import re
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)   # strip Qwen3 thinking blocks
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    cands = [m.group(1)] if m else []
    # fallback: first balanced {...}
    depth = 0; start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                cands.append(text[start:i + 1]); break
    for c in cands:
        try:
            return json.loads(c)
        except Exception:
            continue
    return None


def extract_candidates(text):
    """Return a list of candidate dicts from a reply that may contain a JSON array,
    {"candidates":[...]}, or a single object. Empty list if nothing parses."""
    import re
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    m = re.search(r"```(?:json)?\s*([\[{].*?[\]}])\s*```", text, re.S)
    blobs = [m.group(1)] if m else []
    for opener, closer in (("[", "]"), ("{", "}")):
        depth = 0; start = None
        for i, ch in enumerate(text):
            if ch == opener:
                if depth == 0: start = i
                depth += 1
            elif ch == closer and depth:
                depth -= 1
                if depth == 0 and start is not None:
                    blobs.append(text[start:i + 1]); break
    for b in blobs:
        try:
            obj = json.loads(b)
        except Exception:
            continue
        if isinstance(obj, list):
            return [x for x in obj if isinstance(x, dict)]
        if isinstance(obj, dict):
            if isinstance(obj.get("candidates"), list):
                return [x for x in obj["candidates"] if isinstance(x, dict)]
            return [obj]
    return []
