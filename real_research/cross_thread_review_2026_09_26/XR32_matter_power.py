#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR32 (1/3) -- THE CHAIN'S MATTER POWER WITH ITS LATE-TIME DARK-FLUID CONVERSION: P(k, z) and sigma_8(z) for z = 0-3.

WHY.  XR19 found that FK1/FP10's dark fluid converts through the collapsed and turned-around web at z <~ 1.5 (converted
fraction of the whole fluid 0.36/0.55/0.81/0.91 at z = 3/2/1/0, nominal delta_t0 = 5.31), that the daughters stream at
200-400 km/s today and leave galaxies and groups, and that the linear S8 ratio is 0.931.  It did not score cosmic shear.
This part builds the chain's matter power to the scales a lensing survey uses; XR32_survey_s8.py projects it into KiDS-1000
and DES-Y3 shear, and XR32_consistency.py scores CMB lensing, cluster counts, RSD and sum m_nu.

THE MODEL (nothing fitted; no constant added)
  LINEAR, TWO COMPONENTS.  L319's validated linear solver (exec'd via L357's committed head, unedited): the cold phase
    (baryons + unconverted or retained carrier) and the daughters, kicked at v_k in the local frame, Hubble-cooled as 1/a,
    each birth cohort free-streaming through its own j0 kernel, all coupled through Poisson.  The survival history is
    XR19's S(a) = 1 - F_esc(a), F_esc = the bias-weighted escaped halo fraction + the web part (rebuilt exactly as
    XR19_web_runaway.py builds it from its results JSON).  Histories: halo only; nominal (delta_t0 = 5.31); every O(1)
    choice at its conservative end; pump = full density; delta_t0 = 7.54 (forest floor), 14.6 (canonical top), 22.8 (alt
    top), 25 (FK1 upper); v_k 575 and 650 (XR19's census variants, with the same kick in the solver).
  NONLINEAR: A HALO-MODEL RESPONSE ON A CALIBRATED LCDM P_NL.  P_chain(k, z) = R(k, z) x P_HMcode2020(k, z; Planck 2018),
    R = [P_lin,chain (I_1 + B_ph)^2 + P_1h,chain] / [P_lin,LCDM I_1^2 + P_1h,LCDM]; Sheth-Tormen, NFW (Duffy+08 c_vir),
    HMcode-2020's 1-halo damping; P_lin,chain = T^2_tot(k, z) P_lin from the solver.  Every halo holds its baryons and a
    retained carrier fraction ret(M, z) of its LCDM share:
      phase-space recapture (PRIMARY): ret = (1 - F_esc) ret_in + F_esc cap_TG, i.e. the carrier that arrives unconverted
        converts in place (1 - L357's esc(): the whole halo converts, isotropic kick on a Maxwellian parent in the
        truncated NFW), and the free daughters (1D dispersion sigma_d(z) from the history) are recaptured up to the
        Tremaine-Gunn limit rho_d <= f_max (4 pi/3) v_esc(r)^3 (Maxwellian proxy; an UPPER bound on recapture);
      in place (FP10's pessimistic reading for X-COP: escaped daughters all re-accreted before the in-place conversion);
      no recapture (FP10/AT4's optimistic reading: min(ret_in, 1 - F_esc), escaped daughters never return);
      PM (L388): the committed particle-mesh retention by mass at 600 km/s (z-independent).
    Halo population: LCDM's (PRIMARY: the cold field's small-scale variance stays near LCDM's because conversion is recent);
    bracket 'cold': Sheth-Tormen on the solver's cold-field linear power (the cold field's growth suppression).
  THE MOND PHANTOM, a labelled BRACKET only (the separator is under repair, FP19; the chain's KiDS projection is being
    fixed, FP20): (a) none; (b) a STAND-IN: the isolated nu_mono phantom of each halo's GP0 'observed' bound baryons,
    truncated at L = 1.7 Mpc physical (H_Y's z = 0 value, at every z) and compensated there (L363/MS3's region-phantom
    transform), carried by halos of 1e10-10^15.5 Msun (the record's halo-model range), on both a0 footings (9.3603e-11
    and 1.1312e-10 m/s^2).  Reported sensitivities only (canonical): H_Y's running L(z) = 2.46 Omega_L(z) Mpc; H_Y's
    heat-kernel band-pass in place of the truncation (the isolated phantom x (1 - exp(-k^2 L^2/2))).
  NORMALISATION: Planck 2018 LCDM (an ASSUMPTION pending XR26); the solver's own cosmology (L319's CLASS, A_s 2.1e-9,
    massless nu) supplies only ratios.
PRE-DECLARED (written 2026-09-27T14:01Z, before any full run; only timing tests and the exact reproductions of XR19's nominal
S8 and FP10 A8 had run; informed by back-of-envelope estimates)
  H1a [load-bearing; MUTATE must fail] linear sigma8(z=0) ratio in 0.92-0.96 across delta_t0 = 5.31-25 (XR19 0.931-0.950).
  H1b sigma8(z) ratio rises with z; >= 0.95 at z = 2 and >= 0.97 at z = 3 (nominal).
  H1c linear T^2(k = 1 h/Mpc, z = 0.5) <= 0.2 at nominal (XR19: 0.118).
  H1d no phantom: nonlinear response R(k = 1, z = 0.5) < 0.8 in every recapture reading.
  H1e 1.7 Mpc phantom stand-in: R(k = 1, z = 0.5) > 1 in the primary reading, both footings.
  H1f recapture matters: primary (phase-space) R(k = 0.5, z = 0.5) exceeds the no-recapture reading's by >= 0.1.
CHECKS (load-bearing unless marked)
  C1 CONTROL: XR19's seven on-disk S8 values (its X section) reproduced exactly by the component solver's recombination.
  C2 CONTROL: FP10 A8's committed maximal-web S8 ratios (z_web 1.8/1.2/0.5) reproduced exactly.
  C3 CONTROL: the component copy of L319's solve() recombines bit-for-bit to L319's run() (nominal history).
  C4 CONTROL: no conversion gives T^2 = 1 bit-for-bit and R = 1 exactly (phantom off).
  C5 CONTROL: the Planck-2018 normalisation: CAMB's sigma8 and S8 within 0.5 sigma of Planck 2018's quoted values.
  C6 (reported) the halo model's LCDM P(k) against CAMB's HMcode-2020 (why a response, not the raw halo model, is used).
  H1a-H1f as above; tables M1 (sigma8(z), S8), M2 (linear T^2), M3 (R(k, z) by reading, halo population, phantom),
  M4 (P(k, z) of the key configurations) reported.
MUTATE=1: the conversion switched off (F_esc = 0 at every z; every halo keeps its carrier).  S8 returns to LCDM; H1a, H1c
  and H1d must FAIL (rc = 1).  The controls C1-C3 still run on the unmutated histories.
HISTORY (disclosed).  Before the first full run: timing tests of CAMB and the solver; the two exact reproductions above; a
  6 s read of the KiDS catalogue; unit tests of XR32_common in session scratch (nu_mono against nu_RAR; the phantom
  transform against direct quadrature -- a first tabulated version interpolated badly in kappa and was replaced by direct
  integration, agreeing to ~1e-5; the Hankel transform against a Gaussian; the recombination; the retention readings;
  the halo model against HMcode; Limber against CAMB).  No hypothesis was changed after them.
  One smoke run of this script (XR32_OUTDIR in scratch, not for the record) passed 12/12 but showed the phantom stand-in
  at R(1, 0.5) = 42: its 2-halo factor B_ph reached 8-75 at z = 0-1 because every dwarf down to 1e6 Msun carried an
  isolated phantom out to 1.7 Mpc (an isolated-halo sum cannot see MOND's non-additivity).  The record's halo-model range
  (1e10-10^15.5 Msun, L363/MS3) was then adopted.  The truncated (sharp) and heat-kernel edge forms were both computed
  before the stand-in's form was fixed: the sharp truncation is kept as the stand-in because it is the literal 'within L'
  and the record's convention; the heat-kernel form (4.5x LCDM at k = 0.3, z = 0.5) is reported beside it.  H1e was not
  changed.  (A J_4 bug later found by XR32_survey_s8's smoke run lives in the xi+- code, which this part does not use.)

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR32_matter_power.py   (MUTATE=1 first)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import XR32_common as X
import numpy as np

MUTATE = os.environ.get("MUTATE", "0") == "1"
OUTD = os.environ.get("XR32_OUTDIR", HERE)                              # smoke tests write to scratch, never the record
SLUG = "XR32_matter_power"; SUF = "_MUTATE" if MUTATE else ""
P = X.Log(os.path.join(OUTD, SLUG + SUF + ".out"))
T0 = time.time(); CH = []; OUT = {"lane": "XR32", "part": "1/3 matter power", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)
def el(): return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("PRE-DECLARED")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: conversion switched off (F_esc = 0, carrier kept in every halo); H1a, H1c, H1d must FAIL ***")
R = X.record(); LC, S8L = R["LC"], R["S8_LCDM"]
P(f"\n  L357's head loaded (L319's solver, L357's esc()); solver LCDM S8 {S8L!r}   {el()}")

# ================================================================================================ solves
NAMES = [n for n, _, _ in X.HISTORIES]
H = X.solve_histories(NAMES, mutate=False)                           # the unmutated histories (controls; main when not MUTATE)
P(f"  solved {len(H)} histories (two threads)   {el()}")
if MUTATE:
    comp0 = dict(dc=LC.copy(), dd=np.zeros_like(LC), rc=np.ones(LC.shape[1]), rd=np.zeros(LC.shape[1]), tot=LC.copy())
    HM_ = {n: dict(Fz=X.history(k, True), vk=v, comp=comp0, T=X.Transfer(comp0, LC)) for n, k, v in X.HISTORIES}
else:
    HM_ = H

# ================================================================================================ controls
banner("C1-C5  CONTROLS")
X19 = X.xr19()["X"]; dev = 0.0; rows = {}
for n, key in X.XR19_X_KEYS.items():
    s8 = float(R["S8_of"](R["T2f"](H[n]["comp"]["tot"], LC, 0.0)))
    rows[n] = (s8, X19[key]["S8"]); dev = max(dev, abs(s8 - X19[key]["S8"]))
P("    " + "; ".join(f"{n}: {a:.10f} vs {b:.10f}" for n, (a, b) in rows.items()))
OUT["numbers"]["C1"] = {n: dict(mine=a, xr19=b) for n, (a, b) in rows.items()}
check("C1 CONTROL: XR19's seven on-disk S8 values (X section; uncommitted file) reproduced exactly", f"max |dev| {dev:.1e}", dev == 0.0)
F10 = json.load(open(X.FP10_JSON))["numbers"]["A8"]["S8_web"]; d10 = {}
for zw in (1.8, 1.2, 0.5):
    Rw = R["run"](X.fp10_a8_S(zw), 600.0); d10[zw] = (float(R["S8_of"](R["T2f"](Rw, LC, 0.0))) / S8L, F10[str(zw)])
P("    FP10 A8: " + "; ".join(f"z_web {k}: {a!r} vs {b!r}" for k, (a, b) in d10.items()))
OUT["numbers"]["C2"] = {str(k): dict(mine=a, fp10=b) for k, (a, b) in d10.items()}
check("C2 CONTROL: FP10 A8's committed maximal-web S8 ratios reproduced exactly", "; ".join(f"{a - b:.1e}" for a, b in d10.values()),
      all(a == b for a, b in d10.values()))
Rn = R["run"](X.S_of(H["nominal (dt0 5.31)"]["Fz"]), 600.0)
check("C3 CONTROL: the component solver's recombination is bit-identical to L319's run() (nominal history)",
      f"max |diff| {np.max(np.abs(Rn - H['nominal (dt0 5.31)']['comp']['tot'])):.1e}", np.array_equal(Rn, H["nominal (dt0 5.31)"]["comp"]["tot"]))
R0 = R["run"](np.ones(R["N_A"]), 600.0)
base = X.ChainBase(); P(f"  CAMB Planck-2018 base (HMcode-2020) and the halo model ready   {el()}")
Tid = X.Transfer(dict(dc=R0, dd=np.zeros_like(R0), rc=np.ones(R0.shape[1]), rd=np.zeros(R0.shape[1]), tot=R0), LC)
Rid = base.response(Tid, (np.array([0.0, 20.0]), np.array([0.0, 0.0])), 600.0, X.READINGS[0], mutate=True)
check("C4 CONTROL: no conversion gives T^2 = 1 bit-for-bit (L319's run with S = 1) and the response R = 1 exactly",
      f"run(S=1) == LCDM: {np.array_equal(R0, LC)}; max |R - 1| {np.max(np.abs(Rid - 1)):.1e}", np.array_equal(R0, LC) and np.max(np.abs(Rid - 1)) < 1e-12)
s8p = float(base.res.get_sigma8_0()); S8P = s8p * math.sqrt(base.C.Om / 0.3)
check("C5 CONTROL: the Planck-2018 normalisation (posterior means, sum m_nu 0.06 eV): CAMB's sigma8 and S8 within 0.5 sigma of the quoted",
      f"sigma8 {s8p:.4f} (0.8111 +- 0.0060), S8 {S8P:.4f} (0.832 +- 0.013), Om {base.C.Om:.4f}",
      abs(s8p - 0.8111) <= 0.003 and abs(S8P - 0.832) <= 0.0065)
OUT["numbers"]["C5"] = dict(sigma8=s8p, S8=S8P, Om=base.C.Om)
hmr = {}
for z in (0.0, 0.5, 1.0):
    B = base.B[z]; kc = base.kc
    p = base.C.P(kc, z, lin=True) * B["I1"] ** 2 + base.hm.p1h(B); pn = base.C.P(kc, z)
    hmr[z] = {kq: float(np.interp(math.log(kq), np.log(kc), p / pn)) for kq in (0.1, 0.3, 1.0, 3.0, 10.0)}
check("C6 (reported) the raw halo model against HMcode-2020 (LCDM, P_HM/P_HMcode at k = 0.1/0.3/1/3/10 h/Mpc)",
      {z: {k: round(v, 3) for k, v in d.items()} for z, d in hmr.items()}, True,
      "a vanilla halo model misses 10-26% in the 2-halo/1-halo transition, so the chain enters only as a response on HMcode", load_bearing=False)
OUT["numbers"]["C6"] = {str(z): d for z, d in hmr.items()}

# ================================================================================================ M1 sigma8(z)
banner("M1  LINEAR sigma8(z) AND S8 (Planck-2018 normalised) FOR EVERY HISTORY")
ZT = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0)
kk = np.geomspace(1e-4, 50.0, 6000)
M1 = {}
for n in NAMES:
    T = HM_[n]["T"]; rr = {}
    for z in ZT:
        Pl = base.C.P(kk, z, lin=True); x = kk * 8.0; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        rr[z] = math.sqrt(X._trap(kk ** 2 * Pl * W ** 2 * T(kk, z, "tot"), kk) / X._trap(kk ** 2 * Pl * W ** 2, kk))
    s8rec = float(R["S8_of"](R["T2f"](HM_[n]["comp"]["tot"], LC, 0.0))) / S8L
    M1[n] = dict(ratio=rr, S8=S8P * rr[0.0], ratio_record_S8_of=s8rec, Fesc={z: float(np.interp(z, *HM_[n]["Fz"])) for z in (0.0, 1.0, 2.0, 3.0)},
                 sigma_d={z: X.sigma_d(HM_[n]["Fz"], HM_[n]["vk"], z) for z in (0.0, 0.5, 1.0, 2.0)})
    P(f"    {n:26s}: sigma8 ratio z=" + "/".join(f"{z:g}" for z in ZT) + " = " + "/".join(f"{rr[z]:.4f}" for z in ZT)
      + f"; S8 {S8P * rr[0.0]:.4f} (record's S8_of ratio {s8rec:.4f}); F_esc(0/1/2/3) " + "/".join(f"{v:.3f}" for v in M1[n]["Fesc"].values())
      + "; sigma_d(0/0.5/1/2) " + "/".join(f"{v:.0f}" for v in M1[n]["sigma_d"].values()) + " km/s")
OUT["numbers"]["M1"] = {n: dict(ratio={str(z): v for z, v in d["ratio"].items()}, S8=d["S8"], ratio_record_S8_of=d["ratio_record_S8_of"],
                                Fesc={str(z): v for z, v in d["Fesc"].items()}, sigma_d={str(z): v for z, v in d["sigma_d"].items()}) for n, d in M1.items()}
band = ["nominal (dt0 5.31)", "dt0 7.54 (forest floor)", "dt0 14.6 (canonical top)", "dt0 22.8 (alt top)", "dt0 25 (FK1 upper)"]
rb = [M1[n]["ratio"][0.0] for n in band]
check("H1a the conversion lowers the linear sigma8(z = 0) by 4-8% across delta_t0 = 5.31-25 (ratio 0.92-0.96)",
      f"ratio {min(rb):.4f}-{max(rb):.4f} (S8 {S8P * min(rb):.4f}-{S8P * max(rb):.4f})", 0.92 <= min(rb) and max(rb) <= 0.96,
      "the daughters' free-streaming scale (k_fs ~ 0.2-0.3 h/Mpc) sits just above sigma8's window")
rn = M1["nominal (dt0 5.31)"]["ratio"]; mono = all(rn[ZT[i + 1]] >= rn[ZT[i]] - 1e-9 for i in range(len(ZT) - 1))
check("H1b the sigma8 suppression fades with z: monotone, >= 0.95 at z = 2 and >= 0.97 at z = 3 (nominal)",
      f"monotone {mono}; z = 2: {rn[2.0]:.4f}; z = 3: {rn[3.0]:.4f}", mono and rn[2.0] >= 0.95 and rn[3.0] >= 0.97)

# ================================================================================================ M2 linear T^2
banner("M2  THE LINEAR TRANSFER T^2(k, z) (total; cold field) AND THE COLD FRACTION")
M2 = {}
for n in ("halo only", "nominal (dt0 5.31)", "most conservative", "dt0 22.8 (alt top)"):
    T = HM_[n]["T"]
    M2[n] = {z: dict(tot={k: float(T(k, z)[0]) for k in (0.1, 0.3, 1.0, 3.0)}, cold={k: float(T(k, z, "cc")[0]) for k in (0.1, 0.3, 1.0, 3.0)},
                     fcold=T.fcold_z(z)) for z in (0.0, 0.5, 1.0, 2.0, 3.0)}
    for z in (0.0, 0.5, 1.0, 2.0):
        d = M2[n][z]
        P(f"    {n:22s} z={z:3.1f}: T^2_tot(k=0.1/0.3/1/3) " + "/".join(f"{v:.3f}" for v in d["tot"].values())
          + "; cold field " + "/".join(f"{v:.3f}" for v in d["cold"].values()) + f"; cold fraction {d['fcold']:.3f}")
OUT["numbers"]["M2"] = {n: {str(z): d for z, d in v.items()} for n, v in M2.items()}
t2n = M2["nominal (dt0 5.31)"][0.5]["tot"][1.0]
check("H1c the linear small-scale power collapses: T^2(k = 1 h/Mpc, z = 0.5) <= 0.2 at the nominal cell", f"{t2n:.4f} (XR19: 0.118)", t2n <= 0.2,
      "two thirds of the matter is free-streaming daughters at z < 1; only the cold third clusters at k > k_fs")

# ================================================================================================ M3 responses
banner("M3  THE NONLINEAR RESPONSE R(k, z) = P_chain/P_LCDM: recapture readings x halo population x phantom bracket")
PH = {"none": None, "L1.7 canonical": ("canonical", X.L_STANDIN, "sharp"), "L1.7 alt": ("alt", X.L_STANDIN, "sharp"),
      "running L canonical (sensitivity)": ("canonical", "running", "sharp"), "heat-kernel L1.7 canonical (sensitivity)": ("canonical", X.L_STANDIN, "heat")}
KQ = (0.1, 0.3, 0.5, 1.0, 3.0, 10.0); ZQ = (0.0, 0.5, 1.0, 2.0)


def tab(Rg):
    f = X.R_fun(Rg)
    return {z: {k: float(f(np.array([k]), z)[0]) for k in KQ} for z in ZQ}


M3 = {}; RG = {}
nom = HM_["nominal (dt0 5.31)"]
for rd in X.READINGS:
    for sm in ("lcdm", "cold"):
        for pn, ph in PH.items():
            if sm == "cold" and "sensitivity" in pn: continue
            key = f"nominal | {rd} | pop {sm} | phantom {pn}"
            Rg, det = base.response(nom["T"], nom["Fz"], nom["vk"], rd, ph, sm, MUTATE, detail=True)
            RG[key] = Rg; M3[key] = tab(Rg)
    P(f"    {rd:34s}: R(k=0.3/1/3, z=0.5), pop lcdm: phantom none " + "/".join(f"{M3[f'nominal | {rd} | pop lcdm | phantom none'][0.5][k]:.3f}" for k in (0.3, 1.0, 3.0))
      + "; L1.7 can " + "/".join(f"{M3[f'nominal | {rd} | pop lcdm | phantom L1.7 canonical'][0.5][k]:.3f}" for k in (0.3, 1.0, 3.0))
      + "; L1.7 alt " + "/".join(f"{M3[f'nominal | {rd} | pop lcdm | phantom L1.7 alt'][0.5][k]:.3f}" for k in (0.3, 1.0, 3.0))
      + " || pop cold, none " + "/".join(f"{M3[f'nominal | {rd} | pop cold | phantom none'][0.5][k]:.3f}" for k in (0.3, 1.0, 3.0)) + f"   {el()}")
_, detp = base.response(nom["T"], nom["Fz"], nom["vk"], X.READINGS[0], None, "lcdm", MUTATE, detail=True)
retv = {z: {m: float(np.interp(math.log(m), np.log(base.hm.M), detp[z]["ret"])) for m in (1e11, 1e12, 1e13, 1e14, 1e15)} for z in (0.0, 0.5, 1.0)}
for z, d in retv.items():
    P(f"    retained carrier fraction (primary) z = {z}: " + ", ".join(f"1e{math.log10(m):.0f}: {v:.3f}" for m, v in d.items())
      + f"  (sigma_d {detp[z]['sd']:.0f} km/s, F_esc {detp[z]['Fe']:.3f})")
OUT["numbers"]["retained_primary"] = {str(z): {f"{m:.0e}": v for m, v in d.items()} for z, d in retv.items()}
for n in NAMES:
    if n == "nominal (dt0 5.31)": continue
    for pn in ("none", "L1.7 canonical", "L1.7 alt"):
        key = f"{n} | {X.READINGS[0]} | pop lcdm | phantom {pn}"
        RG[key] = base.response(HM_[n]["T"], HM_[n]["Fz"], HM_[n]["vk"], X.READINGS[0], PH[pn], "lcdm", MUTATE); M3[key] = tab(RG[key])
    P(f"    {n:26s} primary: R(k=0.3/1/3, z=0.5) none " + "/".join(f"{M3[f'{n} | {X.READINGS[0]} | pop lcdm | phantom none'][0.5][k]:.3f}" for k in (0.3, 1.0, 3.0))
      + "; L1.7 can " + "/".join(f"{M3[f'{n} | {X.READINGS[0]} | pop lcdm | phantom L1.7 canonical'][0.5][k]:.3f}" for k in (0.3, 1.0, 3.0)) + f"   {el()}")
OUT["numbers"]["M3"] = {k: {str(z): {str(q): v for q, v in d.items()} for z, d in t.items()} for k, t in M3.items()}
r1 = {rd: M3[f"nominal | {rd} | pop lcdm | phantom none"][0.5][1.0] for rd in X.READINGS}
r1c = {rd: M3[f"nominal | {rd} | pop cold | phantom none"][0.5][1.0] for rd in X.READINGS}
check("H1d without the phantom the conversion suppresses the nonlinear power at k = 1 h/Mpc, z = 0.5 by more than 20% in every "
      "recapture reading (both halo populations)", f"R(1, 0.5): pop lcdm {', '.join(f'{k}: {v:.3f}' for k, v in r1.items())}; "
      f"pop cold {', '.join(f'{k}: {v:.3f}' for k, v in r1c.items())}", max(max(r1.values()), max(r1c.values())) < 0.8)
rp = {f: M3[f"nominal | {X.READINGS[0]} | pop lcdm | phantom L1.7 {f}"][0.5][1.0] for f in ("canonical", "alt")}
check("H1e the 1.7 Mpc phantom stand-in more than restores the lensing power at k = 1 h/Mpc, z = 0.5 (R > 1; primary, both footings)",
      f"R(1, 0.5): canonical {rp['canonical']:.3f}, alt {rp['alt']:.3f}", min(rp.values()) > 1.0)
dr = M3[f"nominal | {X.READINGS[0]} | pop lcdm | phantom none"][0.5][0.5] - M3["nominal | no recapture | pop lcdm | phantom none"][0.5][0.5]
check("H1f recapture matters: the primary (phase-space) R(k = 0.5, z = 0.5) exceeds the no-recapture reading's by >= 0.1",
      f"difference {dr:+.3f}", dr >= 0.1)

# ================================================================================================ M4 P(k, z) tables
banner("M4  P(k, z) OF THE KEY CONFIGURATIONS (Planck-2018 normalised; HMcode-2020 base x response)")
KT = np.geomspace(0.01, 10.0, 25); ZTT = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0); M4 = {}
for key in (f"nominal (dt0 5.31) | {X.READINGS[0]} | pop lcdm | phantom none", f"nominal (dt0 5.31) | {X.READINGS[0]} | pop lcdm | phantom L1.7 canonical",
            f"nominal (dt0 5.31) | {X.READINGS[0]} | pop lcdm | phantom L1.7 alt", f"halo only | {X.READINGS[0]} | pop lcdm | phantom none"):
    k2 = key.replace("nominal (dt0 5.31)", "nominal") if key.startswith("nominal") else key
    Rg = RG[k2]; f = X.R_fun(Rg); hn = key.split(" | ")[0]; T = HM_[hn]["T"]
    M4[key] = {str(z): dict(k=KT.tolist(), P_lin_chain=(base.C.P(KT, z, lin=True) * T(KT, z)).tolist(), P_nl_chain=(base.C.P(KT, z) * f(KT, z)).tolist(),
                            P_nl_lcdm=base.C.P(KT, z).tolist()) for z in ZTT}
    P(f"    {key}: P_chain/P_LCDM at k = 0.1/1/10, z = 0/1/2: " + "; ".join(
        "/".join(f"{np.interp(math.log(q), np.log(KT), np.array(M4[key][str(z)]['P_nl_chain']) / np.array(M4[key][str(z)]['P_nl_lcdm'])):.3f}" for q in (0.1, 1.0, 10.0))
        for z in (0.0, 1.0, 2.0)))
OUT["numbers"]["M4"] = M4

# ================================================================================================ summary
banner("SUMMARY")
nm = M1["nominal (dt0 5.31)"]
P(f"""  Linear: the conversion lowers sigma8(0) by {100 * (1 - nm['ratio'][0.0]):.1f}% at the nominal cell (S8 {nm['S8']:.3f} on Planck 2018's normalisation)
  and by {100 * (1 - max(rb)):.1f}-{100 * (1 - min(rb)):.1f}% across delta_t0 = 5.31-25; the suppression fades to {100 * (1 - rn[3.0]):.1f}% at z = 3.  Below the daughters'
  free-streaming scale the linear power drops to T^2(1, 0.5) = {t2n:.3f}.
  Nonlinear: without the phantom the chain's power at k = 1, z = 0.5 is {min(r1.values()):.2f}-{max(r1.values()):.2f} of LCDM's across the recapture readings;
  the 1.7 Mpc phantom stand-in takes it to {rp['canonical']:.2f} (canonical) / {rp['alt']:.2f} (alt).  Which side the chain lands on is set by the
  MOND sector's small-scale lensing, which is under repair (FP19/FP20).""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(n_checks=len(CH), load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
json.dump(OUT, open(os.path.join(OUTD, f"{SLUG}_results{SUF}.json"), "w"), indent=1,
          default=lambda o: (o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, np.floating) else str(o))))
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   {el()}")
sys.exit(1 if n_fail else 0)
