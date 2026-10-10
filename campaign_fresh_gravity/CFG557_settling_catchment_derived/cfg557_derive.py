#!/usr/bin/env python3
"""CFG557 task 1 (FROZEN_CRITERIA.md, criteria commit 5149a12f1): which cold energy can have settled by today?
D1 switch B on a spherical halo (tidal eigenvalues) -> the turnaround ball; D2 stationary state (CFG541 V4, cited); D3 the dynamical
catchment s_c = M_c/M_ta (cfg557_lib) for alpha = 0.5, 1, 2 and the free-fall ceiling (alpha -> inf), both footings; derivation verdict.
Writes the s_c grid used by the tests (log M_ta 8-16, z = 0, census baryons).
  OMP_NUM_THREADS=4 nice -n 10 python3 cfg557_derive.py              -> cfg557_derive.out, cfg557_derive_results.json
  CFG557_MUTATE=1 OMP_NUM_THREADS=4 nice -n 10 python3 cfg557_derive.py -> *_MUTATE.* (MU3 infinite age; exit 1 = the tooth bites)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg557_lib as L

MUTATE = os.environ.get("CFG557_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
FOOTS = ("canonical", "alt")
ALPHAS = {"ff": math.inf, "a2": 2.0, "a1": 1.0, "a05": 0.5}

# CFG556 extended NFW (Duffy08 c200m, Delta_ta = 11.81), copied from cfg556_halo_model.py
DTA = 11.81
m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def conc(M): return 10.14 * (M / 2e12) ** -0.081
def r200m(M): return (3 * M / (4 * math.pi * 200 * L.RHO_M)) ** (1 / 3)
def halo_basics(M):
    c = conc(M); r2 = r200m(M); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - DTA / 200.0, 1.0, 50.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc)
LM200 = np.linspace(8.0, 16.0, 321)
HB = [halo_basics(10 ** l) for l in LM200]
LMTA = np.log10([hb["Mta"] for hb in HB])
def hb_of_lMta(l):
    return halo_basics(10 ** float(np.interp(l, LMTA, LM200)))
def r_of_M(hb, M):
    """radius holding M in the extended NFW."""
    return brentq(lambda r: hb["M"] * m_nfw(r / hb["rs"]) / hb["mc"] - M, 1e-6 * hb["rs"], 50 * hb["rta"], xtol=1e-12)

res = dict(lane="CFG557", script="cfg557_derive", date="2026-10-10", mutate=MUTATE, criteria_commit="5149a12f1",
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; G9; no EFE; cold energy mass required; not theory closed",
           controls={}, D1={}, table={}, grid={}, verdict={})
P(f"CFG557 derivation {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (5149a12f1). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")

E0 = L.Epoch(0.0)
if not MUTATE:
    # ---------------------------------------------------------------- controls
    t0g = L.T0 * L.GYR_PER_HINV
    k1 = abs(E0.Delta_ta / 11.816 - 1); k2 = 1.670 <= E0.d_c <= 1.690; k3 = abs(t0g / 13.796 - 1)
    P(f"\nK1 Delta_ta(z=0) from the shell ODE {E0.Delta_ta:.4f} vs 11.816 (CFG541): rel {k1:.1e} (<= 5e-3) -> {'PASS' if k1 <= 5e-3 else 'FAIL'}")
    P(f"K2 delta_c(z=0) {E0.d_c:.4f} in [1.670, 1.690] -> {'PASS' if k2 else 'FAIL'};  delta_ta,lin(z=0) {E0.d_ta:.4f}")
    P(f"K3 t0 {t0g:.4f} Gyr vs 13.796 (CFG547): rel {k3:.1e} (<= 3e-3) -> {'PASS' if k3 <= 3e-3 else 'FAIL'}")
    res["controls"].update(K1=k1, K1_pass=k1 <= 5e-3, Delta_ta=E0.Delta_ta, K2_dc=E0.d_c, K2_pass=bool(k2), d_ta=E0.d_ta, K3=k3, K3_pass=k3 <= 3e-3, t0_gyr=t0g)
    # K5 (reported): main-progenitor collapsed-mass history M(z=1)/M0 (barrier omega = d_c D(1)/D(a))
    k5 = {}
    for lm in (12.0, 14.0):
        X, dL = E0.mah(10 ** lm, xmin=0.005)
        om1 = E0.d_c * L.Dgrow(1.0) / L.Dgrow(0.5)
        x_c0 = float(np.interp(E0.d_c, dL[::-1], X[::-1])); x_c1 = float(np.interp(om1, dL[::-1], X[::-1]))
        k5[str(lm)] = x_c1 / x_c0
    P(f"K5 (reported) main-progenitor M(z=1)/M(0): log M_ta 12 {k5['12.0']:.3f}, 14 {k5['14.0']:.3f}")
    res["controls"]["K5_Mz1_over_M0"] = k5

    # ---------------------------------------------------------------- D1: lambda_2 on the extended NFW
    P("\nD1 tidal eigenvalues of the spherical extended NFW (CFG556): radius where lambda_2 = (Delta_ta - 1)/3 vs r_ta")
    d1max = 0.0
    for lm in (11, 12, 13, 14, 15):
        hb = halo_basics(10.0 ** lm)
        def lam(r):
            Menc = hb["M"] * m_nfw(r / hb["rs"]) / hb["mc"]
            dbar = Menc / (4 / 3 * math.pi * r ** 3 * L.RHO_M) - 1
            x = r / hb["rs"]; rho = hb["M"] / hb["mc"] / (4 * math.pi * hb["rs"] ** 3 * x * (1 + x) ** 2)
            dloc = rho / L.RHO_M - 1
            ev = sorted([dbar / 3, dbar / 3, dloc - 2 * dbar / 3], reverse=True)
            return ev[1], dloc - 2 * dbar / 3, dbar / 3
        rB = brentq(lambda r: lam(r)[0] - (DTA - 1) / 3, hb["r200"], 20 * hb["r200"], xtol=1e-12)
        dev = abs(rB / hb["rta"] - 1); d1max = max(d1max, dev)
        lr, lt = lam(hb["rta"])[1:]
        P(f"  log M200m {lm}: r_B/r_ta = {rB / hb['rta']:.6f}; at r_ta radial {lr:+.3f} vs tangential {lt:+.3f} (lambda_2 = tangential = delta_bar/3)")
        res["D1"][str(lm)] = dict(rB_over_rta=rB / hb["rta"], radial=lr, tangential=lt)
    P(f"  max |r_B/r_ta - 1| = {d1max:.1e} (<= 1e-3) -> {'PASS' if d1max <= 1e-3 else 'FAIL'}: B n C = the turnaround ball (mobility region = candidate a)")
    res["controls"].update(D1=d1max, D1_pass=d1max <= 1e-3)

    # ---------------------------------------------------------------- D3 table, log M_ta 11-15
    P("\nD3 dynamical catchment s_c = M_c/M_ta at z = 0 (census baryons; fixed point with the edge).  r_c from the extended NFW of the same M_ta.")
    P("   cols: alpha | s_c | r_c/r_ta | r_c/r200m | M_c/M200m | r_e/r_ta (Mpc/h r_e) | t_cap Gyr")
    conv_all = True
    LTAB = np.arange(11.0, 15.01, 0.5)
    for ft in FOOTS:
        res["table"][ft] = {}
        for lt in LTAB:
            hb = hb_of_lMta(lt); Mta = hb["Mta"]; f = L.fret_of(math.log10(Mta)); Mb = f * L.FB * Mta
            mah = E0.mah(Mta); row = {}
            for an, a in ALPHAS.items():
                o = L.s_catch(E0, Mta, Mb, ft, a, mah=mah, full=True)
                conv_all &= o["converged"]
                rc = r_of_M(hb, o["sc"] * Mta)
                row[an] = dict(sc=o["sc"], rc_over_rta=rc / hb["rta"], rc_over_r200m=rc / hb["r200"], Mc_over_M200m=o["sc"] * Mta / hb["M"],
                               re_over_rta=o["re"] / hb["rta"], re=o["re"], tcap_gyr=o["tcap_gyr"], iters=o["iters"], converged=o["converged"])
            # context: collapsed shell (delta_L = delta_c), q bracket for the ceiling, More+15 splashback
            X, dL = mah
            xcol = float(np.interp(E0.d_c, dL[::-1], X[::-1]))
            qb = {}
            for qq in (1.6, 3.0):
                qb[str(qq)] = L.s_catch(E0, Mta, Mb, ft, math.inf, mah=E0.mah(Mta, q=qq))
            Xc, dLc = E0.mah(Mta, xmin=0.005)
            om05 = E0.d_c * L.Dgrow(1.0) / L.Dgrow(1 / 1.5)
            Mz0 = float(np.interp(E0.d_c, dLc[::-1], Xc[::-1])); Mz05 = float(np.interp(om05, dLc[::-1], Xc[::-1]))
            Gam = math.log(Mz0 / Mz05) / math.log(1.5)
            Omz = L.Om
            Msp = 0.59 * (1 + 0.35 * Omz) * (1 + 0.92 * math.exp(-Gam / 4.54)) * hb["M"]
            rsp = 0.54 * (1 + 0.53 * Omz) * (1 + 1.36 * math.exp(-Gam / 3.04)) * hb["r200"]
            row["context"] = dict(x_collapsed=xcol, r_collapsed_over_rta=r_of_M(hb, xcol * Mta) / hb["rta"], sc_ff_q16=qb["1.6"], sc_ff_q30=qb["3.0"],
                                  Gamma_acc=Gam, Msp_over_Mta_More15=Msp / Mta, rsp_over_rta_More15=rsp / hb["rta"], r200m_over_rta=hb["r200"] / hb["rta"],
                                  M200m_over_Mta=hb["M"] / Mta, fret=f)
            res["table"][ft][f"{lt:.1f}"] = row
            P(f"  [{ft:9s}] log M_ta {lt:4.1f} (f_ret {f:.2f}; r200m/r_ta {hb['r200'] / hb['rta']:.3f}, M200m/M_ta {hb['M'] / Mta:.3f})")
            for an in ALPHAS:
                o = row[an]
                P(f"      {an:4s} s_c {o['sc']:.4f} | r_c/r_ta {o['rc_over_rta']:.3f} | r_c/r200m {o['rc_over_r200m']:.3f} | M_c/M200m {o['Mc_over_M200m']:.3f} | "
                  f"r_e/r_ta {o['re_over_rta']:.3f} ({o['re']:.3f}) | t_cap {o['tcap_gyr']:.2f}")
            c = row["context"]
            P(f"      context: collapsed shell (delta_c) x {c['x_collapsed']:.3f} (r/r_ta {c['r_collapsed_over_rta']:.3f}); ceiling at q 1.6/3.0: {c['sc_ff_q16']:.3f}/{c['sc_ff_q30']:.3f}; "
              f"Gamma_acc {c['Gamma_acc']:.2f} -> More+15 M_sp/M_ta {c['Msp_over_Mta_More15']:.3f}, r_sp/r_ta {c['rsp_over_rta_More15']:.3f}")
    res["controls"]["K4_converged_table"] = bool(conv_all)

    # ---------------------------------------------------------------- full grid for the tests (log M200m 8-16, CFG556's grid)
    P("\nGrid for the tests (CFG556 mass grid, z = 0, census baryons) ...")
    conv_g = True
    for ft in FOOTS:
        g = {an: [] for an in ALPHAS}
        for hb in HB:
            Mta = hb["Mta"]; f = L.fret_of(math.log10(Mta)); Mb = f * L.FB * Mta
            mah = E0.mah(Mta)
            for an, a in ALPHAS.items():
                o = L.s_catch(E0, Mta, Mb, ft, a, mah=mah, full=True); conv_g &= o["converged"]; g[an].append(o["sc"])
        res["grid"][ft] = dict(log10_M200m=LM200.tolist(), log10_Mta=LMTA.tolist(), **g)
    res["controls"]["K4_converged_grid"] = bool(conv_g)
    P(f"K4 fixed point converged: table {conv_all}, grid {conv_g} -> {'PASS' if conv_all and conv_g else 'FAIL'}")

    # ---------------------------------------------------------------- verdict
    P("\nDerivation verdict (frozen rule):")
    ceil = [res["table"][ft][k]["ff"]["sc"] for ft in FOOTS for k in res["table"][ft]]
    excl = max(ceil) < 0.95
    ratios = {f"{ft}|{k}": res["table"][ft][k]["a05"]["sc"] / res["table"][ft][k]["a2"]["sc"] for ft in FOOTS for k in res["table"][ft]}
    A = min(ratios.values()); kA = min(ratios, key=ratios.get)
    derived = A >= 0.90
    P(f"  (a) kinematically excluded at z = 0 (free-fall ceiling < 0.95 at every log M_ta 11-15, both footings): {excl} (max ceiling {max(ceil):.3f})")
    P(f"  alpha-sensitivity A = min s_c(0.5)/s_c(2) = {A:.3f} at {kA} -> {'CATCHMENT DERIVED (c), tested = alpha 1' if derived else 'NOT DERIVABLE exactly (needs alpha); tested = the alpha-free free-fall ceiling (DERIVED UPPER BOUND)'}")
    res["verdict"] = dict(a_excluded=bool(excl), max_ceiling=max(ceil), A=A, A_at=kA, ratios=ratios, derived_exact=bool(derived),
                          label=("CATCHMENT DERIVED (c)" if derived else "NOT DERIVABLE exactly (needs alpha); DERIVED UPPER BOUND = free-fall ceiling"),
                          tested=("a1" if derived else "ff"))
else:
    P("\nMU3: infinite age (t_obs -> 1e3 t0): s_c must be 1 at every grid mass")
    Einf = L.Epoch(0.0, t_obs_override=1e3 * L.T0)
    worst = {}
    for ft in FOOTS:
        w = 1.0
        for lt in np.arange(11.0, 15.01, 0.5):
            hb = hb_of_lMta(lt); Mta = hb["Mta"]; f = L.fret_of(math.log10(Mta)); Mb = f * L.FB * Mta
            for an, a in ALPHAS.items():
                w = min(w, L.s_catch(Einf, Mta, Mb, ft, a))
        worst[ft] = w
        P(f"  [{ft}] min s_c over masses and alphas = {w:.6f} -> {'BITES' if abs(w - 1) <= 1e-3 else 'FAILS'}")
    res["teeth"] = dict(MU3_min_sc=worst, MU3_bites=all(abs(v - 1) <= 1e-3 for v in worst.values()))

json.dump(res, open(os.path.join(HERE, f"cfg557_derive_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg557_derive{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if res["teeth"]["MU3_bites"] else 0)
