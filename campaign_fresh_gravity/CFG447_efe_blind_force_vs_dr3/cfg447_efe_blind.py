#!/usr/bin/env python3
"""CFG447: EFE-blind force injected into the frozen DR4 pipeline's mock + estimator (imported read-only) vs the DR3 dry run.
Run: python3 cfg447_efe_blind.py [--mutate]   (FROZEN_CRITERIA.md)"""
import os, sys, json, hashlib, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
PIPE = os.path.join(REPO, "prep_2026", "gaia_dr4_prep", "wide_binary_pipeline.py")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
sys.argv = [sys.argv[0]]
sha0 = hashlib.sha256(open(PIPE, "rb").read()).hexdigest()
sys.path.insert(0, os.path.dirname(PIPE)); sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import wide_binary_pipeline as W
    import CFG4_common as C
OUT = []
def P(s=""): print(s); OUT.append(str(s))
def nu_p2(y): return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-12))
def nu_mono(y): return C.nu_mono(np.maximum(y, 1e-12))
def vt_custom(pop, a0, gfun):
    gam = gfun(pop["g_true"] / a0)
    vX = (gam * pop["pmx"] + pop["npmx"]) * 4.74e3 * (pop["d_obs"] / 1000.)
    vY = (gam * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.)
    return np.hypot(vX, vY) / pop["vc_obs"]
DR3 = {"canonical": (W.A0_CAN, 1.0750, 0.0550, 1.1175, 0.0625), "alt": (W.A0_ALT, 1.0775, 0.0512, 1.0875, 0.0537)}
rng = np.random.default_rng(4470)
with contextlib.redirect_stdout(io.StringIO()):
    pop_m = W.make_population(1_000_000, rng, dr4=True)
    mods = {f: W.model_medians(pop_m, DR3[f][0], W.GRID, rng) for f in DR3}
P(f"CFG447 EFE-blind force vs DR3 dry run{' [MUTATE: Newton injected]' if MUT else ''}; master pairs {len(pop_m['s_obs'])}")
def recover(gfun_of_a0, foot, seeds):
    a0 = DR3[foot][0]; gs = []
    for s in seeds:
        r = np.random.default_rng(s)
        with contextlib.redirect_stdout(io.StringIO()):
            pd = W.make_population(int(6210 * 2.7), r, dr4=False)
            keep = r.permutation(len(pd["s_obs"]))[:6210]; pd = {k: v[keep] for k, v in pd.items()}
            vt = gfun_of_a0(pd, a0)
            g, sg, *_ = W.run_fit(np.log10(pd["g_proj"] / a0), vt, mods[foot], r, "x")
        gs.append(g)
    return np.array(gs)
seeds = list(range(47001, 47011)); res = {}
# K1: the pipeline's own EFE-saturated boost at Arm A
k1 = recover(lambda pd, a0: W.vtilde_of(pd, W.GAMMA_TARGET, a0), "canonical", seeds[:5])
k1ok = abs(np.median(k1) - W.GAMMA_TARGET) < max(2 * np.std(k1), 0.02)
P(f"K1 Arm A injection {W.GAMMA_TARGET}: recovered median {np.median(k1):.4f} (spread {np.std(k1):.4f}) -> {'PASS' if k1ok else 'FAIL'}")
for kern, nf in (("nu_mono", nu_mono), ("nu_P2", nu_p2)):
    for foot in DR3:
        gfun = (lambda y: np.ones_like(y)) if MUT else (lambda y, nf=nf: np.sqrt(nf(y)))
        g = recover(lambda pd, a0, gfun=gfun: vt_custom(pd, a0, gfun), foot, seeds)
        med, spr = float(np.median(g)), float(np.std(g))
        _, gb, sb, gl, sl = DR3[foot]
        zb = (med - gb) / np.hypot(sb, spr); zl = (med - gl) / np.hypot(sl, spr)
        pinned = int((g >= W.GRID[-1] - 1e-9).sum())
        v = "EXCLUDED BY DR3" if zb > 5 else "NOT EXCLUDED"
        res[f"{kern}|{foot}"] = dict(median=med, spread=spr, pinned=pinned, z_builder=float(zb), z_literal=float(zl), verdict=v)
        P(f"  {kern:7s} {foot:9s}: recovered gamma_hat median {med:.4f} (spread {spr:.4f}; {pinned}/10 pinned at grid top {W.GRID[-1]:.2f}) | vs DR3 builder {gb} +- {sb}: {zb:+.1f} sigma, literal {gl}: {zl:+.1f} sigma -> {v}")
sha1 = hashlib.sha256(open(PIPE, "rb").read()).hexdigest()
P(f"K2 pipeline sha256 unchanged: {sha0 == sha1} ({sha0[:16]}...)")
json.dump(dict(res=res, K1=dict(recovered=k1.tolist(), ok=bool(k1ok)), K2=sha0 == sha1), open(os.path.join(HERE, f"cfg447_efe_blind{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg447_efe_blind{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    ok = abs(res["nu_mono|canonical"]["median"] - 1.0) < 0.03; P(f"MUTATE: Newton recovered -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if (k1ok and sha0 == sha1) else 1)
