#!/usr/bin/env python3
"""CFG592 PART A (ADDENDUM_2026-10-10.md, commit 65fa05a07): the frozen HMcode track re-run with an EVOLVING dark-energy
background (DESI DR2 + CMB + DES-Y5 CPL chain) for BOTH models, with the framework's a0(z) tracking that dark energy.
REPORTED CONTEXT: the frozen rule makes every framework class of this track NOT DIAGNOSTIC (MUTATE MU2 failed).

  nice -n 10 python3 cfg592_de.py   -> cfg592_de.out, cfg592_de_results.json

It execs cfg592_like.py read-only up to its run block (data, projection, nuisances, fit) and replaces only the background
(distances, kernels, growth for IA) and the P(k, z; T) table. kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "cfg592_like.py")).read().split("# ------------------------------------------------------------------ run\n")[0]
__file__ = os.path.join(HERE, "cfg592_like.py")
exec(compile(_src, __file__, "exec"))
__file__ = os.path.join(HERE, "cfg592_de.py")
import numpy as np
OUT.clear()
def strip(r): return {k: v for k, v in r.items() if k != "t"}
T0 = time.time()

# ------------------------------------------------------------------ DESI DR2 + CMB + DES-Y5 chain points
def chain_points():
    d = os.path.join(REPO, "..", "_external_data", "desi_dr2_chains", "desy5"); fn1 = os.path.join(d, "chain.1.txt")
    hdr = open(fn1).readline().lstrip("#").split(); names = ("weight", "w", "wa", "omegam"); cols = [hdr.index(c) for c in names]
    xs = []
    for kk in range(1, 5):
        x = np.loadtxt(os.path.join(d, f"chain.{kk}.txt"), usecols=cols); xs.append(x[int(0.3 * len(x)):])
    x = np.vstack(xs); w = x[:, 0]
    def wq(v, q):
        o = np.argsort(v); c = np.cumsum(w[o]) / w.sum(); return float(np.interp(q, c, v[o]))
    w0, wa = x[:, 1], x[:, 2]
    r05 = np.sqrt((1.5) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * 0.5 / 1.5))
    pts = {"median": dict(w0=wq(w0, 0.5), wa=wq(wa, 0.5))}
    for lab, q in (("p16_a0ratio", 0.16), ("p84_a0ratio", 0.84)):
        tgt = wq(r05, q); i = int(np.argmin(np.abs(r05 - tgt))); pts[lab] = dict(w0=float(w0[i]), wa=float(wa[i]), a0ratio_z05_target=tgt)
    return pts, int(len(x))
PTS, NCH = chain_points()
def a0ratio(z, w0, wa): return np.sqrt((1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z)))

# ------------------------------------------------------------------ background + P table for one (w0, wa)
import camb
pF = camb.CAMBparams(); pF.set_cosmology(H0=H0, ombh2=OMBH2, omch2=OMCH2, mnu=0.0, omk=0, num_massive_neutrinos=0)
pF.InitPower.set_params(ns=NS, As=2.1e-9); pF.set_matter_power(redshifts=[0.0], kmax=10.0)
rF = camb.get_results(pF); AS_FID = 2.1e-9 * (S8FID / rF.get_sigma8_0()) ** 2          # A_s of the w = -1 fiducial (sigma8 = 0.811)
def setup_bg(w0, wa):
    global CHI, DCHIDZ, KK, KLEN, PREF, WCHI, DZ, logP
    p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=OMBH2, omch2=OMCH2, mnu=0.0, omk=0, num_massive_neutrinos=0)
    if not (w0 == -1.0 and wa == 0.0): p.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    p.InitPower.set_params(ns=NS, As=AS_FID); p.set_matter_power(redshifts=list(np.linspace(3.6, 0.0, 61)), kmax=100.0, nonlinear=True)
    p.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=7.8)
    r = camb.get_transfer_functions(p); r.calc_power_spectra(r.Params)
    CHI = np.array([r.comoving_radial_distance(z) for z in ZG]) * h
    DCHIDZ = 2997.92458 / (np.array([r.hubble_parameter(z) for z in ZG]) / H0)
    _wz = np.gradient(ZG)
    KLEN = np.where(CHI[None, :] > CHI[:, None], (CHI[None, :] - CHI[:, None]) / CHI[None, :], 0.0) * _wz[None, :]
    PREF = 1.5 * OM * (1 / 2997.92458) ** 2 * CHI / AG
    WCHI = DCHIDZ * _wz / CHI ** 2
    KK = (LN[:, None] + 0.5) / CHI[None, :]
    plin = r.get_matter_power_interpolator(nonlinear=False, hubble_units=True, k_hunit=True)
    DZ = np.sqrt(np.array([plin.P(z, 0.01) for z in ZG]) / plin.P(0.0, 0.01))
    s8 = float(r.get_sigma8_0())
    kc = np.clip(KK, 1e-4, KMAXE); G = []
    for T in TGRID:
        r.Params.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=T); r.calc_power_spectra(r.Params)
        pk = r.get_matter_power_interpolator(nonlinear=True, hubble_units=True, k_hunit=True, extrap_kmax=KMAXE * 1.01)
        lp = np.array([np.log(pk.P(ZG[m], kc[:, m])) for m in range(len(ZG))]).T
        G.append(np.where(KK > KMAXE, lp - 3.0 * np.log(KK / KMAXE), lp))
    G = np.array(G)
    def _logP(s8_, T):
        j = int(np.clip(np.searchsorted(TA, T) - 1, 0, len(TA) - 2)); wj = (T - TA[j]) / (TA[j + 1] - TA[j])
        return (1 - wj) * G[j] + wj * G[j + 1]
    logP = _logP
    return s8
def R_track(Rcan, Ralt, foot, w0, wa):
    rc, ra = np.asarray(Rcan, float) - 1, np.asarray(Ralt, float) - 1
    ok = (np.abs(rc) >= 0.01) & (np.sign(rc) == np.sign(ra)) & (ra != 0)
    p = np.where(ok, np.log(np.abs(ra) / np.where(ok, np.abs(rc), 1.0)) / math.log(1.13120 / 0.93603), 0.0)
    Rf = np.asarray(Rcan if foot == "canonical" else Ralt, float)
    r = R_of(Rf, KK); pk = np.interp(np.log(np.clip(KK, KR[0], KR[-1])), np.log(KR), p)
    return 1 + (r - 1) * a0ratio(ZG, w0, wa)[None, :] ** pk, p

MODELS = {"PRIMARY": lambda f: J559["halo_model"][f]["PRIMARY_kin"]["R"], "emergent edge": lambda f: J556["cases"][f"{f}|census|emg"]["R"],
          "r200m scope": lambda f: J556["cases"][f"{f}|census|cen|r200scope"]["R"]}
P("CFG592 PART A: frozen HMcode track with an evolving dark-energy background (both models) and a0(z) tracking it (framework) -- REPORTED CONTEXT")
P("kappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed. Frozen MU2 failed -> all framework classes here NOT DIAGNOSTIC.")
P(f"DESI DR2 + CMB + DES-Y5 chain (n = {NCH}, 30% burn-in): points {json.dumps(PTS)}; A_s held at the w = -1 fiducial value {AS_FID:.4e}")
SURVEYS = {"KiDS": prepare(load_kids()), "DES": prepare(load_des())}
BGS = {"w=-1 (As fixed; check vs frozen mode A)": (-1.0, 0.0)}
BGS.update({f"DESI {k}": (v["w0"], v["wa"]) for k, v in PTS.items()})
RES = dict(lane="CFG592 PART A", date="2026-10-10", addendum_commit="65fa05a07", chain_points=PTS, As=AS_FID, backgrounds={})
for bn, (w0, wa) in BGS.items():
    s8 = setup_bg(w0, wa)
    P(f"\n=== background {bn}: w0 {w0:.3f}, wa {wa:.3f}; sigma8(z=0) {s8:.4f} (S8 {s8 * S8CONV:.4f}); a0(z)/a0(0) at z 0.5 / 1 / 2 = "
      f"{a0ratio(0.5, w0, wa):.3f} / {a0ratio(1.0, w0, wa):.3f} / {a0ratio(2.0, w0, wa):.3f} ===")
    rb = dict(w0=w0, wa=wa, sigma8=s8, a0ratio={str(z): float(a0ratio(z, w0, wa)) for z in (0.5, 1.0, 2.0)}, lcdm={}, framework={})
    for n, S in SURVEYS.items():
        lc = fit(S, np.ones_like(KK)); rb["lcdm"][n] = strip(lc)
        P(f"  {n}: LCDM chi2 {lc['chi2']:.2f} (T {lc['T']:.2f}, A_IA {lc['A_IA']:.2f})")
        for foot in ("canonical", "alt"):
            for mn, getR in MODELS.items():
                Rm, p = R_track(getR("canonical"), getR("alt"), foot, w0, wa)
                fF = fit(S, Rm); d = fF["chi2"] - lc["chi2"]
                rb["framework"].setdefault(foot, {}).setdefault(mn, {})[n] = dict(fit=strip(fF), dchi2=d, p_at_k1=float(np.interp(0.0, np.log(KR), p)))
                P(f"  {n}: {foot} | {mn} (a0 tracking, p(k=1) {np.interp(0.0, np.log(KR), p):+.2f}): chi2 {fF['chi2']:.2f} (T {fF['T']:.2f}) dchi2 {d:+.2f}")
    RES["backgrounds"][bn] = rb
P(f"\ndone in {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, "cfg592_de_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg592_de.out"), "w").write("\n".join(OUT) + "\n")
