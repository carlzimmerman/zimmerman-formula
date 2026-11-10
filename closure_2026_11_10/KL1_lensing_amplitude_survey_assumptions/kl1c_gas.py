#!/usr/bin/env python3
"""KL1 PART C (FROZEN_CRITERIA_PARTC.md 190161a7f7): the halo-model side of C1 and C2.
CO1's co1_hm.py above its KA1 section executed unchanged (it executes CFG556's library part read-only); A3's rule copied from
kl1_gas.py (Part A, unchanged there).
  C2  the cold component's response to a gas move: NR (none, A3 as graded) / AD (every cold shell keeps r M(<r)).
  C1  gas from the stellar-mass-selected DESI DR2 x ACT DR6 kSZ stack (GH11 A(1.8) 0.54 +- 0.12, GH10 0.45 +- 0.10), converted to a
      retained fraction with two frozen halo choices ((a) the layout's own SHMR, (b) Zhang's R_vir as R200c), the frozen
      bracket-or-row rule, and the frozen mass interpolation to RB1's ladder; both regimes.
  KC3, KC4; MUTATE MC1, MC2 -> kl1c_gas_MUTATE.json.

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1c_gas.py     -> kl1c_gas.json, kl1c_gas.out, kl1c_gas_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Inherited halo list (CO1's criteria)."""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO1 = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
_src = open(os.path.join(CO1, "co1_hm.py")).read(); _cut = _src.index("# ------------------------------------------------------------------ KA1: CFG556's committed primary table")
NS = {"__file__": os.path.join(CO1, "co1_hm.py"), "__name__": "co1_hm_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "co1_hm.py", "exec"), NS)
L, layout, is_cluster, bar_cum = NS["L"], NS["layout"], NS["is_cluster"], NS["bar_cum"]
h, FB, KK, MM, HBL = L["h"], L["FB"], L["KK"], L["MM"], L["HB"]
RGRID0 = NS["rgrid"]
HMJ = json.load(open(os.path.join(CO1, "co1_hm.json")))
GAS_A = json.load(open(os.path.join(HERE, "kl1_gas.json")))
RB1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "RB1_form_b_hot_systems", "rb1.json")))
GH11 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "GH11_ksz_two_halo_miscentring", "gh11.json")))
GH10 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "GH10_dr2_ksz_published_points", "gh10.json")))
FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
tab = RB1["gate2"]["canonical"]["extended_GS4"]["median_fret_gas_by_mass"]
LMC = np.array([13.25, 13.75, 14.25, 14.75, 15.25]); FRT = np.array([tab[k]["kvm"] for k in ("13.0-13.5", "13.5-14.0", "14.0-14.5", "14.5-15.0", "15.0-15.5")])
def fret_table(lm500): return min(float(np.interp(lm500, LMC, FRT)), 1.0)
RHOC = 2.77536627e11                                          # h^2 Msun / Mpc^3, so (Msun/h) / (Mpc/h)^3

# ------------------------------------------------------------------ layout pieces
def with_points(hb, foot, pts):
    NS["rgrid"] = lambda hb_, rmax: np.unique(np.concatenate([RGRID0(hb_, rmax), [p for p in pts if 0 < p < rmax]]))
    try: return layout(hb, foot, mode="B")
    finally: NS["rgrid"] = RGRID0
def r500_of(hb, r, M):
    rho_c = hb["M200c"] / (200 * 4 / 3 * math.pi * hb["r200c"] ** 3)
    g = lambda x: float(np.interp(x, r, M)) - 500 * rho_c * 4 / 3 * math.pi * x ** 3
    return brentq(g, 1e-3 * hb["r200c"], hb["r200c"], xtol=1e-12 * hb["r200c"])
def parts(hb, foot, r, scope):
    """(stars(<r), gas(<r)) of the layout. scope 'r500': A3's (explicit baryons inside R200c); 'stack': C1's (cluster: + f_b x the
    reference mass beyond R200c; galaxy: condensed baryons as stars, uncondensed as gas)."""
    if is_cluster(hb, foot, "vstiff"):
        R2 = hb["r200c"]; Mbs = FB * hb["M200c"]; ms = min(L["mstar"](hb), Mbs); mg = Mbs - ms
        a = 0.015 * R2 / (1 + math.sqrt(2)); rc = 0.1 * R2; rr = np.minimum(r, R2)
        st = ms * (rr ** 2 / (rr + a) ** 2) / (R2 ** 2 / (R2 + a) ** 2); gs = mg * (rr / rc - np.arctan(rr / rc)) / (R2 / rc - math.atan(R2 / rc))
        if scope == "stack": gs = gs + FB * np.clip(L["M_L"](hb, r) - hb["M200c"], 0, None) * (r > R2)
        return st, gs
    _, _, inf = layout(hb, foot, mode="B"); Mb = inf["Mb"]; Ms = hb["Mta"]; rin = np.minimum(r, hb["rta"])
    return np.full_like(r, Mb), (FB * Ms - Mb) * L["M_L"](hb, rin) / Ms
def move(r, gas, Rin, Rout, f, b_in):
    """scale the gas inside Rin so that baryons inside Rin = f x b_in(Rin); put the removed mass between Rin and Rout, M linear in r."""
    gR = float(np.interp(Rin, r, gas)); sR = float(np.interp(Rin, r, b_in)) - gR
    s = (f * float(np.interp(Rin, r, b_in)) - sR) / gR if gR > 0 else 1.0; short = s < 0; s = min(max(s, 0.0), 1.0); dM = (1 - s) * gR
    delta = -(1 - s) * np.interp(np.minimum(r, Rin), r, gas) + dM * np.clip((r - Rin) / (Rout - Rin), 0.0, 1.0)
    return delta, dict(s=s, dM=dM, short=bool(short))
def adiabatic(r, M, b_i, b_f, rmax):
    """AD: every cold shell keeps r M(<r). Returns the new M(<r) on r."""
    c = M - b_i; RHS = r * M; lo = r.copy(); hi = np.full_like(r, rmax)
    bf = lambda x: np.interp(x, r, b_f)
    for _ in range(80):
        mid = 0.5 * (lo + hi); g = mid * (c + bf(mid)) - RHS; lo = np.where(g < 0, mid, lo); hi = np.where(g < 0, hi, mid)
    rf = 0.5 * (lo + hi); rf[0] = 0.0; rf[-1] = r[-1] if r[-1] <= rmax else rf[-1]
    rf = np.maximum.accumulate(rf)
    cf = np.interp(r, rf, c)
    return cf + b_f
# ------------------------------------------------------------------ C1's conversion (frozen in section 3)
LMS = 10.75 + 0.19 + 0.031                                     # GH10's corrected bin mass
RVIR = float(np.interp(LMS, [10.75, 11.0], [210.0, 295.0]))    # kpc, GH7's table (as gh10_post.py)
RM_KPC = 1.8 * RVIR; MZ = float(GH11["Mneed"])
A_PRI = (GH11["fits"]["primary_1.8"]["b_free"]["A"], GH11["fits"]["primary_1.8"]["b_free"]["s"]); A_EDGE = (GH10["primary"]["1.8"]["A"], GH10["primary"]["1.8"]["s"])
def hb_of_M200c(m200c):                                       # Msun/h
    return L["halo_basics"](brentq(lambda M: L["halo_basics"](M)["M200c"] - m200c, m200c * 0.5, m200c * 5.0, xtol=1e-6 * m200c))
def m200c_from_mstar(lms):                                    # choice (a): CFG556's mstar(hb) (Msun/h in, Msun/h out), inverted
    tgt = 10 ** lms * h
    return brentq(lambda m: L["mstar"](dict(M200c=m)) - tgt, 1e10, 1e15, xtol=1e-3)
def m200c_from_zhang(lms):                                    # choice (b): R200c = Zhang's R_vir (GH7's table)
    Rk = float(np.interp(lms, [9, 9.5, 10, 10.5, 10.75, 11, 11.25, 11.5], [82., 102., 131., 178., 210., 295., 480., 950.]))
    R = Rk * h / 1000.0; return 200 * RHOC * 4 / 3 * math.pi * R ** 3
CHOICE = {"a": m200c_from_mstar, "b": m200c_from_zhang}
def conversion(A):
    out = {}
    for ch, fn in CHOICE.items():
        hb = hb_of_M200c(fn(LMS)); Rm = RM_KPC * h / 1000.0
        Mt = float(L["M_L"](hb, np.array([Rm]))[0]) / h          # Msun
        fs = FB * Mt; Mb = 10 ** LMS + A[0] * MZ
        out[ch] = dict(M200c_Msun=hb["M200c"] / h, R200c_kpc=hb["r200c"] / h * 1000, Rm_over_R200c=Rm / hb["r200c"], Mtot_Rm=Mt, fair=fs, Mb=Mb,
                       f=Mb / fs, sigma_f=A[1] * MZ / fs)
    sf = max(out["a"]["sigma_f"], out["b"]["sigma_f"]); d = abs(out["a"]["f"] - out["b"]["f"])
    out["decision"] = "BRACKET" if d > sf else "ROW"; out["d"] = d; out["sigma_f"] = sf
    return out
CONV = conversion(A_PRI); CONV_E = conversion(A_EDGE)
P("KL1 PART C, halo-model side. kappa = 1/2 FITTED; not theory closed.")
P(f"C1 conversion (stack: log M* {LMS:.3f}, R_vir {RVIR:.1f} kpc, R_m {RM_KPC:.0f} kpc, Zhang's gas inside R_m {MZ:.3e} Msun; A(1.8) {A_PRI[0]:.3f} +- {A_PRI[1]:.3f}):")
for ch in ("a", "b"):
    c = CONV[ch]; P(f"  ({ch}) M200c {c['M200c_Msun']:.3e} Msun, R200c {c['R200c_kpc']:.0f} kpc, R_m/R200c {c['Rm_over_R200c']:.3f}; M_tot(<R_m) {c['Mtot_Rm']:.3e}; fair share "
                    f"{c['fair']:.3e}; measured baryons {c['Mb']:.3e} -> f {c['f']:.3f} +- {c['sigma_f']:.3f}")
P(f"  |f_a - f_b| {CONV['d']:.3f} against sigma_f {CONV['sigma_f']:.3f} -> C1 is a {CONV['decision']}   (GH10's A {A_EDGE[0]:.3f}: f_a {CONV_E['a']['f']:.3f}, f_b {CONV_E['b']['f']:.3f})")

# ------------------------------------------------------------------ the layouts
_ANC = {}
def anchor(foot, ch):
    if (foot, ch) not in _ANC:
        hb_an = hb_of_M200c(CHOICE[ch](LMS)); r_an, M_an, _ = layout(hb_an, foot, mode="B")
        _ANC[(foot, ch)] = (CHOICE[ch](10.0), CHOICE[ch](LMS), math.log10(float(np.interp(r500_of(hb_an, r_an, M_an), r_an, M_an)) / h))
    return _ANC[(foot, ch)]
def lay(hb, foot, gas="A3", resp="NR", ch=None, fixed=None, conv=None, fixed_a3=None):
    """gas: 'none' (CO1), 'A3' (RB1 at R500, edge r_ta), 'C1' (stack rule in its range, A3 above); resp NR / AD."""
    if gas == "none":
        return layout(hb, foot, mode="B")
    r0, M0, _ = layout(hb, foot, mode="B"); R500 = r500_of(hb, r0, M0); M500 = float(np.interp(R500, r0, M0)); lm500 = math.log10(M500 / h)
    rule = "A3" if gas == "A3" else None
    if gas == "C1":
        cv = conv[ch]; m200 = hb["M200c"]; lo, an, lm500_an = anchor(foot, ch)
        if lm500 >= 13.25: rule, f = "A3", None
        elif m200 < lo: rule = "none"
        elif m200 <= an: rule, f = "stack", min(cv["f"], 1.0) if fixed is None else fixed
        else:
            w = (lm500 - lm500_an) / (13.25 - lm500_an) if 13.25 > lm500_an else 1.0
            rule, f = "stack", (min(cv["f"], 1.0) + min(max(w, 0.0), 1.0) * (0.674 - min(cv["f"], 1.0))) if fixed is None else fixed
        if rule == "none": return r0, M0, dict(rule="none")
    if rule == "A3":
        if not is_cluster(hb, foot, "vstiff"): return r0, M0, dict(rule="none (galaxy regime, A3)")
        Rin, Rout = R500, hb["rta"]; scope = "r500"
        f = (fixed if fixed is not None else fret_table(lm500)) if gas == "A3" else (fixed_a3 if fixed_a3 is not None else fret_table(lm500))
    else:
        Rin, Rout = cv["Rm_over_R200c"] * hb["r200c"], hb["rta"]; scope = "stack"
        if Rin >= 0.95 * Rout: return r0, M0, dict(rule="none (R_m beyond r_ta)")
    r, M, inf = with_points(hb, foot, [Rin, Rout])
    st, gs = parts(hb, foot, r, scope); b_i = st + gs
    if scope == "r500" and is_cluster(hb, foot, "vstiff"):
        b_in = b_i
    else: b_in = b_i
    delta, mv = move(r, gs, Rin, Rout, f, b_in); b_f = b_i + delta
    Mn = M + delta if resp == "NR" else adiabatic(r, M, b_i, b_f, hb["rta"])
    return r, Mn, dict(inf if isinstance(inf, dict) else {}, rule=rule, f=f, lgM500=lm500, Rin_over_R200c=Rin / hb["r200c"], regime="cluster" if is_cluster(hb, foot, "vstiff") else "galaxy", **mv)
def R_of(foot, **kw):
    NS["set_population"]()
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UB, infB = L["U_set"](lambda hb: lay(hb, foot, **kw)); PB, _, _ = L["spectra_ta"](UB)
    return 1 + (PB - PLta) / Pstd, infB
KSEL = (0.3, 0.5, 1.0, 2.0, 3.0, 5.0)
def at(R): return {str(k): float(np.interp(k, KK, R)) for k in KSEL}

RES = dict(lane="KL1", part="C halo model", criteria="190161a7f7", note="kappa = 1/2 FITTED; not theory closed; adopts nothing; inherited halo list",
           k=KK.tolist(), C1_conversion=dict(primary_A=A_PRI, edge_A=A_EDGE, LMS=LMS, RVIR_kpc=RVIR, Rm_kpc=RM_KPC, MZ=MZ, primary=CONV, edge=CONV_E), KA={}, rows={})
MUT = dict(lane="KL1", part="C MUTATE (MC1, MC2)", note="kappa = 1/2 FITTED; not theory closed", rows={})
# KC3: point-mass test of the AD solver
rr = np.r_[0.0, np.geomspace(1e-3, 10.0, 2000)]; Mc_ = 1.0 * rr / 10.0; bi = np.where(rr > 0, 1.0, 1.0); bf = np.where(rr > 0, 0.5, 0.5); bi[0] = bf[0] = 0.0
Mi = Mc_ + np.where(rr > 0, 1.0, 0.0); Mf = adiabatic(rr, Mi, bi, bf, 10.0)
# analytic: shell r keeps r (c + 1) = r_f (c + 0.5), c = r/10; check at r = 1: find r_f numerically and compare cold(<r_f) = 0.1
rf1 = 1 * (0.1 + 1.0) / (0.1 + 0.5); kc3_pm = abs(float(np.interp(rf1, rr, Mf)) - (0.1 + 0.5))
for ft in FOOTS:
    ref = np.array(HMJ["primary"][ft]["R_tot"]); refA3 = np.array(GAS_A["rows"][ft]["rta_table"]["R_tot"])
    # KC3: AD with no gas moved; mass conservation and order for every AD layout
    worst0, worstM, mono = 0.0, 0.0, True
    for hb in HBL:
        r0, M0, _ = layout(hb, ft, mode="B")
        if is_cluster(hb, ft, "vstiff"):
            st, gs = parts(hb, ft, r0, "r500"); b = st + gs; worst0 = max(worst0, float(np.max(np.abs(adiabatic(r0, M0, b, b, hb["rta"]) - M0)) / hb["Mta"]))
        for kw in (dict(gas="A3", resp="AD"), dict(gas="C1", resp="AD", ch="a", conv=CONV), dict(gas="C1", resp="AD", ch="b", conv=CONV)):
            r, M, _ = lay(hb, ft, **kw); worstM = max(worstM, abs(M[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(M) >= -1e-9 * hb["Mta"]))
    # KC4: C1 with f = 1
    R1, _ = R_of(ft, gas="C1", resp="NR", ch="a", conv=CONV, fixed=1.0, fixed_a3=1.0); R1b, _ = R_of(ft, gas="A3", resp="NR")
    kc4 = float(np.max(np.abs(R1 / ref - 1)[KK <= 10])); kc4b = float(np.max(np.abs(R1b / refA3 - 1)))
    RES["KA"][ft] = dict(KC3_no_move=worst0, KC3_mass=worstM, KC3_monotone=mono, KC3_point_mass=kc3_pm,
                         KC3_pass=bool(worst0 <= 1e-9 and worstM <= 1e-9 and mono and kc3_pm <= 1e-6), KC4_C1_f1_vs_CO1=kc4, KC4_A3_replay=kc4b, KC4_pass=bool(kc4 <= 2e-3 and kc4b <= 2e-3))
    P(f"\n[{ft}] KC3: AD with nothing moved {worst0:.1e}; M(<r_ta) kept to {worstM:.1e}; non-decreasing {mono}; point-mass test {kc3_pm:.1e} -> {'PASS' if RES['KA'][ft]['KC3_pass'] else 'FAIL'};"
      f"  KC4: C1 with f = 1 everywhere against CO1's R_tot {kc4:.1e}, A3 replay {kc4b:.1e} -> {'PASS' if RES['KA'][ft]['KC4_pass'] else 'FAIL'}")
    rows = {}
    for name, kw in (("A3_NR", dict(gas="A3", resp="NR")), ("A3_AD", dict(gas="A3", resp="AD")),
                     ("C1a_NR", dict(gas="C1", resp="NR", ch="a", conv=CONV)), ("C1a_AD", dict(gas="C1", resp="AD", ch="a", conv=CONV)),
                     ("C1b_NR", dict(gas="C1", resp="NR", ch="b", conv=CONV)), ("C1b_AD", dict(gas="C1", resp="AD", ch="b", conv=CONV)),
                     ("C1a_AD_GH10", dict(gas="C1", resp="AD", ch="a", conv=CONV_E))):
        R, inf = R_of(ft, **kw)
        nrule = {}
        for x in inf: nrule[x.get("rule", "-")] = nrule.get(x.get("rule", "-"), 0) + 1
        rows[name] = dict(R_tot=R.tolist(), at=at(R), over_CO1=at(R / ref), rules=nrule)
        P(f"  {name:12s} R_tot over CO1's: " + "  ".join(f"k {k}: {v:.3f}" for k, v in at(R / ref).items()) + f"   rules {nrule}   [{time.time() - T0:.0f} s]")
    RES["rows"][ft] = rows
    # MUTATE
    Rm1, _ = R_of(ft, gas="C1", resp="NR", ch="a", conv=CONV, fixed=0.2); d1 = float(np.interp(1.0, KK, Rm1) - np.interp(1.0, KK, R1b))
    Rn, _ = R_of(ft, gas="A3", resp="NR", fixed=0.2); Ra, _ = R_of(ft, gas="A3", resp="AD", fixed=0.2); d2 = float(np.interp(1.0, KK, Ra) - np.interp(1.0, KK, Rn))
    MUT["rows"][ft] = dict(MC1=dict(dR_k1=d1, bites=bool(abs(d1) >= 0.02), R_tot=Rm1.tolist()), MC2=dict(dR_k1=d2, bites=bool(abs(d2) >= 0.01)))
    P(f"  MC1 (MUTATE) f = 0.2 in the stack's range: R_tot(k 1) moves {d1:+.3f} -> {'bites' if abs(d1) >= 0.02 else 'DOES NOT BITE'};  MC2 AD against NR at f_ret 0.2: {d2:+.3f} -> "
      f"{'bites' if abs(d2) >= 0.01 else 'DOES NOT BITE'}")
RES["KA_ok"] = bool(all(v["KC3_pass"] and v["KC4_pass"] for v in RES["KA"].values()))
P(f"\nKnown answers KC3, KC4 all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "kl1c_gas.json"), "w"), indent=1, default=float)
json.dump(MUT, open(os.path.join(HERE, "kl1c_gas_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kl1c_gas.out"), "w").write("\n".join(OUT) + "\n")
