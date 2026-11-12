#!/usr/bin/env python3
"""SS3 (FROZEN_CRITERIA.md 3a8a5a9fce): variant J's local gates and Bullet through SS1's machinery, read-only. J's retention is
injected into SS1's ss1v module inside this process only (monkeypatch); no SS1 / SS2 file is edited.
    python3 ss3.py local <V>    V in J (primary), Jsrc (source g bracket), MJ2 (v_stiff -> 0)   -> parts/local_V<V>.json, uma_V<V>.json
    python3 ss3.py bullet <V>                                                                    -> parts/vbullet_<V>.json
J: f(r, tau) = 0.5 e^-tau + 0.5 exp(-tau (v_stiff / sigma_1D(r))^2); converted mass leaves as vacuum (no daughter mass).
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1)
W = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else "J"
os.environ["SS1V"] = V; os.environ["SS1V_OPT"] = ""
sys.dont_write_bytecode = True
import numpy as np
CRIT = "3a8a5a9fce"; PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
import ss1v as SV
sys.argv = _a
SV.PARTS = PARTS; SV.VAR = V

def vparJ(Vx, f):
    F = SV.footing(f)
    return dict(z_dec=F["z_q0"], alpha=F["alpha_G"], kick=0.0, base="H", v_stiff=(0.0 if Vx == "MJ2" else F["v_stiff"]), F=F, force_x0_zero=False,
                hfull=False, iform=False, J=True, gform=("src" if Vx == "Jsrc" else "halo"))
def h_profileJ(p, H, tau):
    """J's per-radius retention on the pre-conversion halo: sigma_1D^2 = V^2/2 (SIS), isotropic Jeans (NFW), or the source's
    g = sigma^2 / v_vir^2 = u/(0.08 + u)/(1 + 2.5 u^1.5); bound = False everywhere (no daughter mass: the product is vacuum)."""
    R5, R2 = H["R500"], H["R200"]; rg = np.geomspace(1e-3 * R5, R2, 300); M0 = H["Menc"](rg); dM = np.diff(np.concatenate([[0.0], M0]))
    M200 = H["M200"]; V2 = SV.G_KPC * M200 / R2; v = math.sqrt(SV.G_KPC * H["M500"] / R5)
    if H.get("c200") is None: sig2 = np.full_like(rg, V2 / 2)
    else:
        c = H["c200"]; rs = R2 / c; mu = lambda x: np.log1p(x) - x / (1 + x); A = M200 / mu(c)
        xg = np.geomspace(1e-4, 2000.0, 6000); rho = 1 / (xg * (1 + xg) ** 2); Mx = A * mu(xg); integ = rho * SV.G_KPC * Mx / (xg * rs) ** 2 * rs
        cum = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(xg))[::-1])[::-1], [0.0]]); sig2 = np.interp(rg / rs, xg, cum / rho)
    if p.get("gform") == "src": u = rg / R5; sig2 = v * v * u / (0.08 + u) / (1 + 2.5 * u ** 1.5)
    if tau > 0: f = 0.5 * math.exp(-tau) + 0.5 * np.exp(-tau * p["v_stiff"] ** 2 / np.maximum(sig2, 1e-30))
    else: f = np.ones_like(rg)
    return rg, dM, f, np.zeros(len(rg), bool), v
SV.vpar = vparJ; SV.h_profile = h_profileJ

if __name__ == "__main__":
    print(f"SS3 {W} {V}. Criteria {CRIT}. kappa = 1/2 FITTED; not theory closed; adopts nothing.", flush=True)
    if W == "local":
        import ss1; ss1.PARTS = PARTS
        ss1.MUT = "primary-only"                                         # one set per pass (disk); the NFW bracket is the pass V = J_NFW
        if V.endswith("_NFW"):
            _VC = SV.VComp
            class VN(_VC):
                def __init__(self, f, kind="SIS", am=False, zero=False): super().__init__(f, kind=("SIS" if zero else "NFW"), am=am, zero=zero)
            SV.VComp = VN
        SV.run_local(V)
    elif W == "bullet": SV.run_bullet(V)
    elif W == "ka":
        out = {}
        for f in SV.FOOTS:
            p = vparJ("J", f); F = p["F"]; rows = []
            for Mb in (1e11, 1e13, 1e14):
                H = C.halo(Mb, F["R"], F["h"], F["Om"], z=p["z_dec"]); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]
                rg, dM, fr, b, v = h_profileJ(p, H, p["alpha"]); code = float(np.sum(dM * fr) / np.sum(dM))
                formula = 0.5 * math.exp(-p["alpha"]) + 0.5 * math.exp(-2 * p["alpha"] * (p["v_stiff"] / v) ** 2); rows.append(dict(Mb=Mb, v_vir=v, code=code, formula=formula, dev=abs(code - formula)))
            out[f] = rows; print(f, [(r["Mb"], round(r["v_vir"]), round(r["code"], 5), round(r["formula"], 5)) for r in rows])
        import json; json.dump(dict(KA_J1=out, pass_=bool(all(r["dev"] < 1e-12 for f in out for r in out[f]))), open(os.path.join(PARTS, "ka_J1.json"), "w"), indent=1, default=float)
