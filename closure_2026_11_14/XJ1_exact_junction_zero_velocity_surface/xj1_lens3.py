#!/usr/bin/env python3
"""XJ1 AMENDMENT_A5 cases Ec2 and Ec3 (a copy of xj1_lens.py with the shell runs' caustic columns, the case list changed and the s table left out; outputs xj1_lens3.*). XJ1 (FROZEN_CRITERIA.md ef8ccdde98, section 7, second and third items): lensing gate G4 with the exact junction, and how
far FZS1's junction sits from the law at z = 0. Reported beside the flux-level labels, never a label of this lane.
COPY of JNT2's jnt2_lens.py (closure_2026_11_13/JNT2_crossing_speed_joint), mode "main" only: SRH1's srh1_lens.py is
executed read-only up to its "# ---------------- runs, checkpointed" marker; the boundary is JNT2's (the lemma's v_L
against v*(z)). The only change: the lens's own cold layout is built by profile_E below (inside x_set the law's halo
unscaled; outside C_in + t [C_R(x) - C_R(x_set)], t = (X - C_in) / (X - C_R(x_set))) at R_set = 1, 2, 3 R_fold and at
the zero-velocity surface R_zv(z_lens, M_b) (FLD1's R_ta_kpc column, SRH1's interpolation).
Anchor (must reproduce, or nothing here is quoted): SRH1's own profile at f = 2 through this script equals JNT2's stored
f2.00 row (z all / late / early, chi2) to 1e-6.
  python3 -I -B xj1_lens.py -> xj1_lens.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint")); import jnt2_common as C
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRC = os.path.join(SRH, "srh1_lens.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srh1_lens_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ---------------- runs, checkpointed\n")], SRC, "exec"), S)
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
O, FR, H = S["O"], S["FR"], S["H"]
profile, dsig_prof, DINF_T, LMG, ZG, UT, own_S, nb_sums, fit, gate_of, MK, XP = (S[k] for k in (
    "profile", "dsig_prof", "DINF_T", "LMG", "ZG", "UT", "own_S", "nb_sums", "fit", "gate_of", "MK", "XP"))
halo, Mph, dMph, dm_nfw, m_nfw = S["halo"], S["Mph"], S["dMph"], S["dm_nfw"], S["m_nfw"]
assert FR["VST"] == C.VSTIFF
lMg, zz1, typ1, n1 = S["lMg"], S["zz1"], np.asarray(O["typ1"]), S["n1"]
P(f"XJ1 G4 with the exact junction (criteria ef8ccdde98). SRH1 lens prefix executed. Host-free lenses {n1:,}: late {int((typ1 == 0).sum()):,}, early {int((typ1 == 1).sum()):,}")

# ---------------- the surface reader: SRH1's rfold_kpc with the series column as an argument
MASSES, FTAB = H["MASSES"], H["FT"]; _ST = {}
# AMENDMENT_A5: this lane's shell runs (FLD1's five series columns, checked equal, plus R_1, R_2, R_3) in place of the loaded series
_dev = 0.0
for _ft in ("canonical", "alt"):
    for _M in MASSES:
        _S = np.array(json.load(open(os.path.join(HERE, "shells", f"xj1_shells_{_ft}_M{_M:g}.json")))["series"]); _old = FTAB[_ft][_M]
        assert _S.shape[0] == _old.shape[0] and _S.shape[1] == 8
        _dev = max(_dev, float(np.max(np.abs(_S[:, :5] - _old) / np.maximum(np.abs(_old), 1e-30)))); FTAB[_ft][_M] = _S
assert _dev <= 1e-9, _dev
H["_RT"].clear()
def surf_kpc(ft, z, lM, col):
    key = (ft, round(z, 6), col)
    if key not in _ST:
        def at(Sr):
            o = np.argsort(Sr[:, 1]); return float(np.interp(z, Sr[o, 1], Sr[o, col]))
        _ST[key] = np.array([at(FTAB[ft][M]) for M in MASSES])
    R = _ST[key]
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))
ka_r = max(abs(surf_kpc(ft, z, lm, 2) / H["rfold_kpc"](ft, z, lm) - 1) for ft in ("canonical", "alt") for z in (0.0, 0.2, 0.5, 0.85) for lm in (7.3, 9.4, 10.45, 11.9, 12.6))
P(f"reader on the fold column against SRH1's rfold_kpc: max rel {ka_r:.1e} -> {'PASS' if ka_r <= 1e-12 else 'FAIL'}")
def fzv(ft, z, lM): return surf_kpc(ft, z, lM, 3) / surf_kpc(ft, z, lM, 2)
def fk(ft, z, lM, k): return surf_kpc(ft, z, lM, {2: 6, 3: 7}[k]) / surf_kpc(ft, z, lM, 2)

def profile_E(ft, lMb, z, f):
    """the exact junction. f: a number (R_set = f R_fold), 0 (reference), or 'zv' (R_set = R_zv)."""
    X, xs, xta, xf, rM = halo(ft, lMb, z); xt = math.sqrt(X * (X + 1)); mt = float(m_nfw(xta / xs))
    CRf = lambda x: X * m_nfw(np.minimum(np.asarray(x, float), xta) / xs) / mt
    dCR = lambda x: X * dm_nfw(np.asarray(x, float) / xs) / xs / mt
    xset = min(fzv(ft, z, lMb) * xf, xta) if f == "zv" else min(fk(ft, z, lMb, int(f[1])) * xf, xta) if isinstance(f, str) else min(f * xf, xta)
    if xset <= 0: return [(0.0, xta, dCR)], CRf, dict(s=1.0, t=1.0, xset=0.0, xta=xta, xf=xf, xt=xt, held=0.0)
    Cin = float(min(Mph(xset), X)); CRs = float(CRf(xset)); s = CRs / Cin
    pcs = [(0.0, min(xset, xt), dMph)]
    if xset < xta:
        t = (X - Cin) / (X - CRs)
        pcs.append((xset, xta, (lambda x, t=t: t * dCR(x))))
        M3 = lambda x: np.where(np.asarray(x) <= xset, np.minimum(Mph(x), X), Cin + t * (CRf(x) - CRs))
    else:                                                    # R_set at r_ta: the law's halo, the unused share spread as r (FRZ1's mode B)
        rem = X - Cin; t = 1.0
        if rem > 0: pcs.append((0.0, xta, (lambda x, c=rem / xta: np.full_like(np.asarray(x, float), c))))
        M3 = lambda x: np.minimum(Mph(x), X) + rem * np.minimum(np.asarray(x, float), xta) / xta
    return pcs, M3, dict(s=s, t=t, xset=xset, xta=xta, xf=xf, xt=xt, held=Cin / X)

# ---------------- JNT2's boundary (main mode), copied
VN = {ft: np.array([[C.vL_kms(10 ** float(lm), float(z)) for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
VB = {ft: np.array([[C.vstar_kms(ft, float(z), "main") for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
def table(ft, f, exact):
    T = np.empty((len(LMG), len(ZG), len(UT))); Sm = np.empty((len(LMG), len(ZG))); Tm = np.ones((len(LMG), len(ZG)))
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            ff = 0.0 if VN[ft][i, j] > VB[ft][i, j] else f
            if exact: pc, M3, inf = profile_E(ft, float(lm), float(z), ff); Tm[i, j] = inf["t"]
            else: pc, M3, inf = profile(ft, float(lm), float(z), ff, "S")
            T[i, j] = dsig_prof(UT, pc, M3) / DINF_T; Sm[i, j] = inf["s"]
    return T, Sm, Tm

JN = json.load(open(os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_lens.json")))["cfg"]
CFG = [("J2_anchor", 2.0, False), ("Ec2", "k2", True), ("Ec3", "k3", True)]
RES = dict(lane="XJ1", part="G4 with the exact junction (reported)", criteria="ef8ccdde98", cfg={}, reader_check=ka_r,
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
anchor_ok = True
for ft in ("canonical", "alt"):
    X = XP[ft]; lams = O["lam_grid"](X, extra=[1.0, math.sqrt(O["A0C"] / O["A0"]["alt"])]); lams9 = sorted(set([0.65] + list(map(float, lams)) + [2.57]))
    with contextlib.redirect_stdout(io.StringIO()):
        Tr, Ts, npr = O["neighbours"](X, lams9, O["Htab_of"](X))
    SNB, kval = nb_sums(ft, Tr - Ts[2], lams9)
    P(f"[{ft}] neighbours {npr:,} pairs  [{time.time() - T0:.0f} s]")
    for name, f, exact in CFG:
        T, Sm, Tm = table(ft, f, exact); OS = own_S(ft, T)
        rn = {mk: fit(mk, ft, OS[mk] + SNB[mk], kvalid=kval) for mk in MK}; gt = gate_of(rn); L_ = gt["lines"]
        zrow = [L_["G-K1 all"]["z"], L_["G-K1 late"]["z"], L_["G-K1 early"]["z"], L_["G-K3 type difference"]["z"]]; chi2 = L_["G-K2 all profile"]["chi2"]
        kfit = {sub: float(rn[("KO1", 1.6, sub)]["k"]) for sub in ("all", "late", "early") if rn[("KO1", 1.6, sub)] is not None}
        row = dict(f=f, exact=exact, gate=gt, z=zrow, chi2=chi2, k_fit=kfit, s_min_max=[float(Sm.min()), float(Sm.max())], t_min_max=[float(Tm.min()), float(Tm.max())])
        extra = ""
        if name == "J2_anchor":
            st = JN[f"{ft}|f2.00"]; dv = max(max(abs(a - b) for a, b in zip(zrow, st["z"])), abs(chi2 - st["chi2"]))
            row.update(JNT2_stored=dict(z=st["z"], chi2=st["chi2"]), max_abs_dev=dv, anchor_ok=bool(dv <= 1e-6)); anchor_ok &= dv <= 1e-6
            extra = f"   anchor against JNT2's stored f2.00 row: max abs dev {dv:.1e} -> {'PASS' if dv <= 1e-6 else 'FAIL'}"
        RES["cfg"][f"{ft}|{name}"] = row
        P(f"[{ft}] {name:9s} gate {gt['status']} {gt['failing']}: z all / late / early " + " / ".join(f"{x:+.4f}" for x in zrow[:3]) + f", chi2 {chi2:.4f}, type diff z {zrow[3]:+.4f}; fitted k "
          + ", ".join(f"{s_} {v:.3f}" for s_, v in kfit.items()) + f"; s {Sm.min():.3f}-{Sm.max():.3f}, t {Tm.min():.3f}-{Tm.max():.3f}" + extra + f"  [{time.time() - T0:.0f} s]")
RES["anchor_ok"] = bool(anchor_ok)
P(f"anchor: {'PASS' if anchor_ok else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "xj1_lens3.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "xj1_lens3.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
