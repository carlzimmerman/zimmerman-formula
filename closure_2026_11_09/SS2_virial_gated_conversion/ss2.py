#!/usr/bin/env python3
"""SS2 (FROZEN_CRITERIA.md 390a1dc5ff): variant G (virial-gated late conversion) through SS1's machinery, read-only
(closure_2026_11_09/SS1_self_shielded_conversion: ss1v.py, ss1.py, ss1_cosmo.py, ss1_bullet.py), outputs redirected here.
    python3 ss2.py ka                     known answers (ss1v K0 / K-G / Lovisari + x_crit at the footing alpha)
    python3 ss2.py local <V> [opt]        gates 1, 2, 3, 4, 5, 5b, 10   V in G, Gsrc (source constants), MG1-MG4, Gz2; opt obs | local
    SS1_FOOT=<f> python3 ss2.py cosmo <V> gates 6, 8; 7(b) reading (graded only if 'valid' passes)
    SS1_FOOT=<f> python3 ss2.py valid     section 4: CLASS smooth-fluid run vs the ratio method at fc = 0.20
    python3 ss2.py bullet <V>             gate 9
    python3 ss2.py predict                the frozen lens-redshift prediction and the lane's own version
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1)
W = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 and W != "valid" else "G"
os.environ["SS1V"] = V; os.environ["SS1V_OPT"] = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("SS1V_OPT", "")
sys.dont_write_bytecode = True
import numpy as np
CRIT = "390a1dc5ff"; PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
import ss1v as SV
sys.argv = _a
SV.PARTS = PARTS; SV.VAR = V; SV.OPT = os.environ["SS1V_OPT"]
_footing = SV.footing; _vpar = SV.vpar
def footing(f):
    F = _footing(f)
    if V == "Gsrc": F = dict(F, z_q0=0.642, alpha_G=4.39, v_stiff=286.0)                       # bracket G-source (never grades)
    return F
def tlb(f, z):
    F = _footing(f); zz = np.linspace(0, z, 20001); Or = 2.469e-5 * (1 + 0.2271 * 3.046) / F["h"] ** 2
    E = np.sqrt(F["Om"] * (1 + zz) ** 3 + Or * (1 + zz) ** 4 + F["Ode"]); return 977.792 / (100 * F["h"]) * np.trapz(1 / ((1 + zz) * E), zz)
def vpar(Vx, f):
    p = _vpar("G" if Vx in ("Gsrc", "Gz2") else Vx, f)
    if Vx == "Gz2": p["z_dec"] = 2.0; p["alpha"] = _footing(f)["Gamma0_G"] * tlb(f, 2.0)            # M5: onset z 2, the same Gamma0
    return p
SV.footing = footing; SV.vpar = vpar
def P(s=""): print(s, flush=True)

def ka():
    SV.run_ka(); k = json.load(open(os.path.join(PARTS, "v_ka.json")))
    k["x_crit_footing"] = {f: SV.x_crit(_footing(f)["alpha_G"]) for f in SV.FOOTS}; k["x_crit_4p39"] = SV.x_crit(4.39); k["criteria"] = CRIT
    json.dump(k, open(os.path.join(PARTS, "v_ka.json"), "w"), indent=1, default=float)
    P(f"x_crit at 4.39 {k['x_crit_4p39']:.4f}; footing " + ", ".join(f"{f} {v:.4f}" for f, v in k["x_crit_footing"].items()))

def load_cosmo_ns():
    src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
    ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_ss2"}; a_ = sys.argv; sys.argv = ["ss1_cosmo.py"]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
    sys.argv = a_; return ns

def growth_ratio(ns, fc_of):
    """the ratio-method ODE, identical in structure to ss1v.run_cosmo's solve(): record's two-fluid growth (WD1 k-dependent form)
    on the reference background, source = OB delta_b + OD (1 - fc) delta_c; fc_of(z) -> array over KG (or None)."""
    REFBG = ns["REFBG"]; KG, ZG = ns["KG"], ns["ZG"]; OD, OB = ns["OD"], ns["OB"]; z = REFBG["z"]
    lna_t = np.log(1 / (1 + z)); o = np.argsort(lna_t); lna_t = lna_t[o]; lnH = np.log(REFBG["H"][o]); dlnH = np.gradient(lnH, lna_t)
    ai = 1 / 3401.0; adec = 1 / 1091.0; nk = len(KG); grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), np.log(1 / (1 + ZG))])); tset = {float(x): i for i, x in enumerate(np.log(1 / (1 + ZG)))}
    I4 = np.eye(4)[None, :, :]
    def solve(on):
        y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai; rec = {}
        for n in range(len(grid) - 1):
            h_ = grid[n + 1] - grid[n]; lm = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lm); zz = 1 / a - 1
            E2 = math.exp(2 * np.interp(lm, lna_t, lnH)) / 100.0 ** 2; dl = float(np.interp(lm, lna_t, dlnH))
            fc = fc_of(zz) if on else np.zeros(nk)
            Od = OD * a ** -3 / E2 * (1 - fc); Ob = OB * a ** -3 / E2
            A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od; A[:, 1, 1] = -(2 + dl)
            if a > adec: A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
            y = np.linalg.solve(I4 - 0.5 * h_ * A, ((I4 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
            if float(grid[n + 1]) in tset: rec[tset[float(grid[n + 1])]] = y.copy()
        outv = np.empty((nk, len(ZG)))
        for jz in range(len(ZG)):
            fc = fc_of(ZG[jz]) if on else np.zeros(nk); outv[:, jz] = OB * rec[jz][:, 2] + OD * (1 - fc) * rec[jz][:, 0]
        return outv
    return solve(True) / solve(False)

def valid():
    f = os.environ.get("SS1_FOOT", "canonical"); ns = load_cosmo_ns(); Q3 = ns["Q3"]; Class = ns["Class"]; c0 = ns["c0"]; X0 = ns["X0"]
    OD, OB, h = ns["OD"], ns["OB"], ns["H_REF"]; FR = 0.20
    p = dict(ns["BASE"]); p.update({'omega_cdm': (1 - FR) * OD, 'Omega_fld': FR * OD / h ** 2, 'w0_fld': -0.001, 'wa_fld': 0.0, 'cs2_fld': 1.0, 'use_ppf': 'no', 'output': 'tCl,lCl'})
    for k_ in ('P_k_max_1/Mpc', 'z_max_pk'): p.pop(k_, None)
    M = Class(); M.set(p); M.compute(); Xc = Q3["X_of"](M); cC, AC = Q3["best_amp_chi2"](Xc); M.struct_cleanup(); M.empty()
    Rr = growth_ratio(ns, lambda zz: np.full(len(ns["KG"]), FR)); S = ns["limber4_bg"](ns["REFBG"], Rr); cM, AM = Q3["best_amp_chi2"](X0 * S)
    tol = 0.15 * abs(cC - c0); ok = abs(cM - cC) <= tol
    Ls = (40, 100, 200, 400)
    out = dict(footing=f, fraction=FR, chi2_CLASS=float(cC), chi2_method=float(cM), baseline=float(c0), tolerance=float(tol), pass_=bool(ok),
               S_L_CLASS={str(L): float(Xc[L] / X0[L]) for L in Ls}, S_L_method={str(L): float(S[L]) for L in Ls}, criteria=CRIT)
    json.dump(out, open(os.path.join(PARTS, f"valid_{f}.json"), "w"), indent=1, default=float)
    P(f"[{f}] lensing validation (20 % smooth matter fluid from the start): CLASS chi2 {cC:.3f}, method {cM:.3f}, baseline {c0:.3f}, tol {tol:.3f} -> {'PASS' if ok else 'FAIL'}; "
      "S_L CLASS/method " + " ".join(f"L{L} {Xc[L]/X0[L]:.3f}/{S[L]:.3f}" for L in Ls))

def predict():
    out = dict(frozen=dict(z_lens=[0.8, 0.6, 0.4, 0.2], excess_dex_0p3Mpc=[0.245, 0.205, 0.078, 0.020], f_ret_claimed=[1.00, 0.826, 0.286, 0.074]),
               lens_z_split_on_disk=False, note="KiDS-bright catalogue (lens redshifts, no shear profiles) is the only lens-z data on disk: recorded, not graded", lane={})
    G = 6.6743e-11; MS = 1.98892e30; KPC = 3.0857e19
    for f in SV.FOOTS:
        p = vpar("G", f); F = _footing(f); a0 = SV.A0H[f]; glaw = lambda g: 0.5 * g + np.sqrt(0.25 * g * g + a0 * g); row = {}
        for tag, am in (("primary_KD1P3", False), ("Moster13", True)):
            Ms = 1e11; z = p["z_dec"]
            if am:
                M200 = C.moster_halo(Ms, z); H = C.halo(Ms, F["R"], F["h"], F["Om"], M200=M200, Mchi=M200 * F["R"] / (1 + F["R"]), z=z)
            else: H = C.halo(Ms, F["R"], F["h"], F["Om"], z=z)
            H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; x0 = SV.x0_of(p, H, "kids"); r = []
            for zl in (0.8, 0.6, 0.4, 0.2):
                if zl >= p["z_dec"]: fr = 1.0
                else: tau = p["alpha"] * (tlb(f, p["z_dec"]) - tlb(f, zl)) / tlb(f, p["z_dec"]); fr = SV.ret(x0, tau)
                gN = G * Ms * MS / (300 * KPC) ** 2; m = fr * float(H["Menc"](300.0)); r.append(dict(z_lens=zl, f_ret=fr, excess_dex=math.log10(glaw(gN + G * m * MS / (300 * KPC) ** 2) / glaw(gN))))
            row[tag] = dict(M200=H["M200"], v_vir=math.sqrt(SV.G_KPC * H["M500"] / H["R500"]), x0=x0, rows=r)
            P(f"[{f}] lens-z prediction, {tag} (M200 {H['M200']:.3g}, x0 {x0:.2f}): " + ", ".join(f"z {q['z_lens']}: f {q['f_ret']:.3f} excess {q['excess_dex']:+.3f}" for q in r))
        out["lane"][f] = row
    json.dump(out, open(os.path.join(PARTS, "predict.json"), "w"), indent=1, default=float)

if __name__ == "__main__":
    P(f"SS2 {W} {V} {SV.OPT}. Criteria {CRIT}. kappa = 1/2 FITTED; not theory closed; adopts nothing.")
    if W == "ka": ka()
    elif W == "local":
        import ss1; ss1.PARTS = PARTS                     # redirect ss1.run_local's dumps to this lane
        SV.run_local(V)
    elif W == "cosmo": SV.run_cosmo(V)
    elif W == "bullet": SV.run_bullet(V)
    elif W == "valid": valid()
    elif W == "predict": predict()
