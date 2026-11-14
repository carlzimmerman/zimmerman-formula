#!/usr/bin/env python3
"""BJ1 (FROZEN_CRITERIA.md 9e7ce0dfe6, section 2, G-L): lensing gate G4 with the charge-budget junction at the first,
second and third caustic. A COPY of XJ1's xj1_lens3.py (closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface;
itself a copy of xj1_lens.py, itself of JNT2's jnt2_lens.py, mode "main"): SRH1's srh1_lens.py executed read-only up to
its "# ---------------- runs, checkpointed" marker, XJ1's shell runs in place of FLD1's loaded series (first five columns
checked equal), XJ1's surface reader, JNT2's boundary (the lemma's v_L against v*(z)), ONE1's gate. The only change:
XJ1's profile_E is replaced by profile_B below (criteria section 1 in the lens chain's units, x = r / r_M, masses in M_b):
  C_B(x) = min(Mph(x), X) + rem min(x, x_ta) / x_ta, rem = max(X - min(Mph(x_ta), X), 0)  (FRZ1's mode B)
  C_R(x) = X m_nfw(min(x, x_ta) / x_s) / m_nfw(x_ta / x_s)                                 (the reference)
  x_k = XJ1's caustic column (5, 6, 7 for k = 1, 2, 3) at (z_lens, M_b), capped at x_ta; Q = C_R(x_k).
  under (C_B(x_k) >= Q): x_set = first root of C_B = Q (brentq on the analytic C_B); C = Q on [x_set, x_k].
  over: x_set = first x > x_k with C_B = C_R (a 4001-point log scan, then brentq), else x_ta.
  C = C_B for x <= x_set, C_R(max(x, x_k)) beyond. No factor anywhere.
Anchor (known answer ix; must reproduce, or nothing here is quoted): SRH1's own profile at f = 2 through this script
equals JNT2's stored f2.00 row (z all / late / early, chi2) to 1e-6. Lens-chain checks (reported): x_k forced to x_ta
gives mode B, x_k forced to 0 gives the reference, and C(x_set) = C_R(x_set) in the over branch.
The prefix of this file up to the "JNT2's boundary" marker is executed by bj1_sparc.py and bj1_mw.py.
  nice -n 19 python3 -I -B bj1_lens.py -> bj1_lens.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
XJ1 = os.path.join(REPO, "closure_2026_11_14", "XJ1_exact_junction_zero_velocity_surface")
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
P(f"BJ1 G-L, G4 with the charge-budget junction (criteria 9e7ce0dfe6). SRH1 lens prefix executed. Host-free lenses {n1:,}: late {int((typ1 == 0).sum()):,}, early {int((typ1 == 1).sum()):,}")

# ---------------- the surface reader: SRH1's rfold_kpc with the series column as an argument
MASSES, FTAB = H["MASSES"], H["FT"]; _ST = {}
# AMENDMENT_A5: this lane's shell runs (FLD1's five series columns, checked equal, plus R_1, R_2, R_3) in place of the loaded series
_dev = 0.0
for _ft in ("canonical", "alt"):
    for _M in MASSES:
        _S = np.array(json.load(open(os.path.join(XJ1, "shells", f"xj1_shells_{_ft}_M{_M:g}.json")))["series"]); _old = FTAB[_ft][_M]
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

from scipy.optimize import brentq as _brentq
COLK = {1: 5, 2: 6, 3: 7}
def profile_B(ft, lMb, z, k, force=None):
    """the charge-budget junction at caustic k (1, 2, 3); k = 0 or force 'zero': the reference; force 'rta': x_k = x_ta."""
    X, xs, xta, xf, rM = halo(ft, lMb, z); xt = math.sqrt(X * (X + 1)); mt = float(m_nfw(xta / xs))
    CRf = lambda x: X * m_nfw(np.minimum(np.asarray(x, float), xta) / xs) / mt
    dCR = lambda x: X * dm_nfw(np.asarray(x, float) / xs) / xs / mt
    rem = max(X - float(min(Mph(xta), X)), 0.0)
    CBf = lambda x: np.minimum(Mph(x), X) + rem * np.minimum(np.asarray(x, float), xta) / xta
    if force == "zero" or (force is None and int(k) == 0):
        return [(0.0, xta, dCR)], CRf, dict(branch="none", xset=0.0, xk=0.0, xta=xta, xf=xf, xt=xt, rM=rM)
    xk = xta if force == "rta" else min(surf_kpc(ft, z, lMb, COLK[int(k)]) * 3.0857e19 / rM, xta)
    Q = float(CRf(xk)); CBk = float(CBf(xk))
    if CBk >= Q:
        branch = "under"
        if Q <= 0: xset = 0.0
        elif rem == 0 and Q >= X: xset = min(xt, xk)
        elif CBk == Q: xset = xk if float(CBf(xk * (1 - 1e-12))) < Q else _brentq(lambda x: float(CBf(x)) - Q, 0.0, xk, xtol=1e-15 * xk, rtol=4 * np.finfo(float).eps, maxiter=200)
        else: xset = _brentq(lambda x: float(CBf(x)) - Q, 0.0, xk, xtol=1e-15 * xk, rtol=4 * np.finfo(float).eps, maxiter=200)
    else:
        branch = "over"
        g = np.geomspace(xk, xta, 4001); Dg = CBf(g) - CRf(g); js = np.nonzero(Dg > 1e-12 * X)[0]
        if len(js) == 0: xset = xta
        else:
            j = int(js[0]); i0 = int(np.nonzero(Dg[:j] < 0)[0][-1])
            xset = float(g[i0 + 1]) if Dg[i0 + 1] == 0 else _brentq(lambda x: float(CBf(x) - CRf(x)), float(g[i0]), float(g[i0 + 1]), xtol=1e-15 * float(g[i0 + 1]), rtol=4 * np.finfo(float).eps, maxiter=200)
    xset = min(xset, xta)
    pcs = []
    if xset > 0:
        pcs.append((0.0, min(xset, xt), dMph))
        if rem > 0: pcs.append((0.0, xset, (lambda x, c=rem / xta: np.full_like(np.asarray(x, float), c))))
    xo = max(xk, xset)
    if xo < xta: pcs.append((xo, xta, dCR))
    M3 = lambda x: np.where(np.asarray(x, float) <= xset, CBf(x), CRf(np.maximum(np.asarray(x, float), xk)))
    return pcs, M3, dict(branch=branch, xset=xset, xk=xk, xta=xta, xf=xf, xt=xt, rM=rM, Q=Q, D_k=Q / CBk if CBk > 0 else float("inf"),
                         zero_flux=float(abs(CBf(xset) - CRf(max(xset, xk)))) / X)

# lens-chain checks (reported): forced x_k, the zero-flux identity
_chk = dict(rta=0.0, zero=0.0, zero_flux=0.0)
for _ft in ("canonical", "alt"):
    for _lm in (7.5, 8.5, 9.4, 10.45, 11.2, 12.0):
        for _z in (0.0, 0.3, 0.6):
            _X, _xs, _xta, _xf, _rM = halo(_ft, _lm, _z); _xx = np.geomspace(1e-3, _xta, 300)
            _rem = max(_X - float(min(Mph(_xta), _X)), 0.0); _CB = np.minimum(Mph(_xx), _X) + _rem * _xx / _xta
            _CR = _X * m_nfw(_xx / _xs) / float(m_nfw(_xta / _xs))
            _chk["rta"] = max(_chk["rta"], float(np.max(np.abs(profile_B(_ft, _lm, _z, 1, "rta")[1](_xx) - _CB)) / _X))
            _chk["zero"] = max(_chk["zero"], float(np.max(np.abs(profile_B(_ft, _lm, _z, 1, "zero")[1](_xx) - _CR)) / _X))
            for _k in (1, 2, 3): _chk["zero_flux"] = max(_chk["zero_flux"], profile_B(_ft, _lm, _z, _k)[2]["zero_flux"])
P(f"lens-chain checks: x_k = x_ta against mode B {_chk['rta']:.1e}; x_k = 0 against the reference {_chk['zero']:.1e}; zero-flux identity at x_set or x_k {_chk['zero_flux']:.1e} (of X)")

# ---------------- JNT2's boundary (main mode), copied
VN = {ft: np.array([[C.vL_kms(10 ** float(lm), float(z)) for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
VB = {ft: np.array([[C.vstar_kms(ft, float(z), "main") for z in ZG] for lm in LMG]) for ft in ("canonical", "alt")}
def table(ft, f, exact):
    T = np.empty((len(LMG), len(ZG), len(UT))); Sm = np.empty((len(LMG), len(ZG))); Tm = np.ones((len(LMG), len(ZG)))
    for i, lm in enumerate(LMG):
        for j, z in enumerate(ZG):
            ff = 0.0 if VN[ft][i, j] > VB[ft][i, j] else f
            if exact:
                pc, M3, inf = profile_B(ft, float(lm), float(z), ff); Tm[i, j] = {"under": 0.0, "over": 1.0}.get(inf["branch"], -1.0)
                Sm[i, j] = inf["xset"] / inf["xf"] if inf["branch"] != "none" else np.nan
            else: pc, M3, inf = profile(ft, float(lm), float(z), ff, "S"); Sm[i, j] = inf["s"]
            T[i, j] = dsig_prof(UT, pc, M3) / DINF_T
    return T, Sm, Tm

JN = json.load(open(os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_lens.json")))["cfg"]
CFG = [("J2_anchor", 2.0, False), ("B1", 1, True), ("B2", 2, True), ("B3", 3, True)]
RES = dict(lane="BJ1", part="G-L: G4 with the charge-budget junction", criteria="9e7ce0dfe6", cfg={}, reader_check=ka_r, lens_chain_checks=_chk,
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
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
        if exact:
            below = Tm >= 0
            row = dict(k=f, gate=gt, z=zrow, chi2=chi2, k_fit=kfit, n_cells=int(Tm.size), n_below_vstar=int(below.sum()), share_over=float((Tm == 1).sum() / max(below.sum(), 1)),
                       Rset_over_Rfold_min_max=[float(np.nanmin(Sm)), float(np.nanmax(Sm))] if below.any() else None)
        else: row = dict(f=f, gate=gt, z=zrow, chi2=chi2, k_fit=kfit, s_min_max=[float(Sm.min()), float(Sm.max())])
        extra = ""
        if name == "J2_anchor":
            st = JN[f"{ft}|f2.00"]; dv = max(max(abs(a - b) for a, b in zip(zrow, st["z"])), abs(chi2 - st["chi2"]))
            row.update(JNT2_stored=dict(z=st["z"], chi2=st["chi2"]), max_abs_dev=dv, anchor_ok=bool(dv <= 1e-6)); anchor_ok &= dv <= 1e-6
            extra = f"   anchor against JNT2's stored f2.00 row: max abs dev {dv:.1e} -> {'PASS' if dv <= 1e-6 else 'FAIL'}"
        RES["cfg"][f"{ft}|{name}"] = row
        P(f"[{ft}] {name:9s} gate {gt['status']} {gt['failing']}: z all / late / early " + " / ".join(f"{x:+.4f}" for x in zrow[:3]) + f", chi2 {chi2:.4f}, type diff z {zrow[3]:+.4f}; fitted k "
          + ", ".join(f"{s_} {v:.3f}" for s_, v in kfit.items())
          + (f"; cells below v* {row['n_below_vstar']}/{row['n_cells']}, share over {row['share_over']:.3f}, R_set/R_fold {row['Rset_over_Rfold_min_max'][0]:.3f}-{row['Rset_over_Rfold_min_max'][1]:.3f}" if exact and row["Rset_over_Rfold_min_max"] else "") + extra + f"  [{time.time() - T0:.0f} s]")
RES["anchor_ok"] = bool(anchor_ok)
P(f"anchor: {'PASS' if anchor_ok else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "bj1_lens.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "bj1_lens.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
