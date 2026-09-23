import os
import json
import numpy as np
import sys

def isotropic(rng, n):
    x = rng.normal(size=(n, 3))
    return x / np.linalg.norm(x, axis=1)[:, None]

def thomson_mu(rng, n):
    mu = np.empty(n)
    todo = np.arange(n)
    while len(todo):
        trial = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + trial**2) / 2
        mu[todo[take]] = trial[take]
        todo = todo[~take]
    return mu

def killed_transport(n, tau0, alpha, seed):
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    direction = isotropic(rng, n)
    time = np.zeros(n)
    alive = np.arange(n)
    escaped = np.zeros(n, dtype=bool)
    escape_pos = np.zeros((n, 3))
    escape_dir = np.zeros((n, 3))
    steps = 0
    while len(alive) > 0:
        steps += 1
        if steps > 10000:
            raise RuntimeError("Transport cap exceeded")
        p = pos[alive]
        d = direction[alive]
        pd = np.sum(p * d, axis=1)
        boundary = -pd + np.sqrt(pd*pd + 1 - np.sum(p*p, axis=1))
        scatter_dist = rng.exponential(1/tau0, len(alive))
        absorb_dist = rng.exponential(1/alpha, len(alive))
        min_dist = np.minimum(scatter_dist, absorb_dist)
        is_scatter = min_dist == scatter_dist
        is_absorb = min_dist == absorb_dist
        is_escape = min_dist >= boundary
        ds = np.minimum(min_dist, boundary)
        time[alive] += ds
        pos[alive] += d * ds[:, None]
        new_alive = alive[~is_escape & ~is_absorb]
        escaped[alive[is_escape]] = True
        escape_pos[alive[is_escape]] = pos[alive[is_escape]]
        escape_dir[alive[is_escape]] = d[is_escape]
        alive = new_alive
        if len(alive) == 0:
            break
        p = pos[alive]
        d = direction[alive]
        mu = thomson_mu(rng, len(alive))
        transverse = isotropic(rng, len(alive))
        transverse -= np.sum(transverse * d, axis=1)[:, None] * d
        transverse /= np.linalg.norm(transverse, axis=1)[:, None]
        new_dir = d * mu[:, None] + transverse * np.sqrt(1 - mu*mu)[:, None]
        direction[alive] = new_dir
    D = time[escaped] - np.sum(escape_pos[escaped] * escape_dir[escaped], axis=1)
    return D, int(escaped.sum())

def conservative_transport(n, tau0, alpha, seed):
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    direction = isotropic(rng, n)
    time = np.zeros(n)
    alive = np.arange(n)
    escape_pos = np.zeros((n, 3))
    escape_dir = np.zeros((n, 3))
    steps = 0
    while len(alive) > 0:
        steps += 1
        if steps > 10000:
            raise RuntimeError("Transport cap exceeded")
        p = pos[alive]
        d = direction[alive]
        pd = np.sum(p * d, axis=1)
        boundary = -pd + np.sqrt(pd*pd + 1 - np.sum(p*p, axis=1))
        scatter_dist = rng.exponential(1/tau0, len(alive))
        ds = np.minimum(scatter_dist, boundary)
        is_escape = ds == boundary
        time[alive] += ds
        pos[alive] += d * ds[:, None]
        escaped_idx = alive[is_escape]
        escape_pos[escaped_idx] = pos[escaped_idx]
        escape_dir[escaped_idx] = d[is_escape]
        alive = alive[~is_escape]
        if len(alive) == 0:
            break
        p = pos[alive]
        d = direction[alive]
        mu = thomson_mu(rng, len(alive))
        transverse = isotropic(rng, len(alive))
        transverse -= np.sum(transverse * d, axis=1)[:, None] * d
        transverse /= np.linalg.norm(transverse, axis=1)[:, None]
        new_dir = d * mu[:, None] + transverse * np.sqrt(1 - mu*mu)[:, None]
        direction[alive] = new_dir
    D = time - np.sum(escape_pos * escape_dir, axis=1)
    w = np.exp(-alpha * time)
    mu_hat = np.sum(w * D) / np.sum(w)
    se = np.std(w * (D - mu_hat), ddof=1) / (np.sqrt(n) * np.mean(w))
    return float(mu_hat), float(se), w

def main():
    mode = os.environ["ORCH_MODE"]
    inputs = json.load(open(os.environ["ORCH_INPUTS"]))
    n = 8000
    tau0 = 1.0
    alphas = [0.1, 0.5]
    results = {}
    for alpha in alphas:
        if mode == "negative":
            killed_alpha = alpha / 2
        else:
            killed_alpha = alpha
        D_killed, n_escape = killed_transport(n, tau0, killed_alpha, seed=42)
        mu_killed = float(np.mean(D_killed))
        se_killed = float(np.std(D_killed, ddof=1) / np.sqrt(n_escape))
        mu_conservative, se_conservative, w = conservative_transport(n, tau0, alpha, seed=123)
        diff = float(mu_killed - mu_conservative)
        combined_se = float(np.sqrt(se_killed**2 + se_conservative**2))
        z_score = float(diff / combined_se)
        results[str(alpha)] = {
            "mu_killed": mu_killed,
            "se_killed": se_killed,
            "mu_conservative": mu_conservative,
            "se_conservative": se_conservative,
            "diff": diff,
            "combined_se": combined_se,
            "z_score": z_score,
            "n_escape": n_escape,
            "escape_fraction": float(n_escape / n)
        }
    checks = {}
    for alpha in alphas:
        checks[f"convergence_alpha_{alpha}"] = bool(abs(results[str(alpha)]["z_score"]) < 3.0)
        checks[f"escape_fraction_alpha_{alpha}"] = bool(0.1 < results[str(alpha)]["escape_fraction"] < 0.9)
    print(json.dumps({"protocol": 2, "complete": True, "checks": checks, "measurements": results}))

if __name__ == "__main__":
    main()