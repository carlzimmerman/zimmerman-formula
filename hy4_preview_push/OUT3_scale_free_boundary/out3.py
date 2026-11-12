#!/usr/bin/env python3
"""
OUT-3 (SCALE-FREE BOUNDARY):  kappa = 1/2  <=>  N_f = N_v

    N_f = the formation normalisation (the cold sector's dimensionless normalisation
          pinned on the fold Sigma_f)
    N_v = the vacuum value of the same dimensionless normalisation

Three admissible unit-matched pairs:
    A = (F1,V1) energy density    N_f = G rho_c(Sigma_f) c^2/a0^2   N_v = G rho_L c^2/a0^2 = 1/kappa^2
    B = (F2,V2) column            N_f = Sigma_c/(a0/G) = X/(4 pi u)  N_v = rho_L R_L/(a0/G) = 1/(Z kappa)
    C = (F3,V3) share             N_f = X(u_f)                       N_v = Omega_L/Omega_b

Gates G1..G6 are in PREREGISTER.md.  Footings never pooled.  kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

# ---------------------------------------------------------------- constants
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.989e30
KPC = 3.0856775814913673e19

H0_H = 0.674                      # Planck h
H0 = H0_H * 1.0e5 / (3.0856775814913673e22)   # s^-1
OM_L = 0.685
OM_B = 0.0493
RHO_CRIT = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
RHO_L = OM_L * RHO_CRIT
RHO_CRIT_ALT = RHO_CRIT          # alt footing's density reading for M1

A0_CANON = 9.3603e-11
A0_ALT = 1.1312e-10
FOOTING_SPREAD = 0.5 * math.log10(A0_ALT / A0_CANON)     # 0.0411 dex
Z_SQ = math.sqrt(8.0 * math.pi / 3.0)                    # 2.8944
CSQRTGL = C * math.sqrt(G * RHO_L)                       # c sqrt(G rho_Lambda)

BAND5 = math.log10(1.05)                                 # 0.0212 dex

# FLD1 fold table (canonical; alt differs by < 0.5 % in R_fold)
# log M_b : (R_fold z=0, z=1, z=2, z=4) kpc , R_ta(z=0) kpc
FLD1 = {
    7.0:  ([10, 5, 3, 0.9], 19),
    8.0:  ([21, 11, 7, 2.5], 40),
    9.0:  ([46, 25, 16, 5.6], 88),
    9.4:  ([62, 34, 21, 7.6], 120),
    10.0: ([99, 54, 34, 12.1], 190),
    10.45: ([139, 76, 48, 17.2], 268),
    10.7: ([169, 92, 58, 21.0], 325),
    10.9: ([197, 108, 68, 24.5], 378),
    11.2: ([248, 136, 85, 31.0], 476),
    11.5: ([312, 171, 107, 39.2], 600),
}
ZS = [0, 1, 2, 4]
REF_LM = 10.45

# ---------------------------------------------------------------- helpers
def X_of_u(u):
    """FLD1's exact share: X(1+X) = u."""
    return (math.sqrt(1.0 + 4.0 * u) - 1.0) / 2.0

def dlnX_dlnu(u):
    """d ln X / d ln u at u; = u/(X sqrt(1+4u))."""
    X = X_of_u(u)
    return u / (X * math.sqrt(1.0 + 4.0 * u))

def rho_c_fold(a0, M_b, R_f):
    """cold (sector) mean energy-equivalent mass density inside the fold, kg/m^3."""
    u = a0 * R_f ** 2 / (G * M_b)
    X = X_of_u(u)
    return 3.0 * X * M_b / (4.0 * math.pi * R_f ** 3)

# ---------------------------------------------------------------- arms
def armA(a0, M_b, R_f, rho_vac=RHO_L):
    """(F1,V1): rho_c(Sigma_f) = rho_vac.  Exact inversion via X(1+X)=u."""
    q = 4.0 * math.pi * rho_vac * R_f ** 3 / (3.0 * M_b)     # required share
    a0_root = G * M_b * q * (1.0 + q) / R_f ** 2
    kap = a0_root / (C * math.sqrt(G * rho_vac))
    u_root = q * (1.0 + q)
    return dict(q=q, a0_root=a0_root, kappa=kap, u_root=u_root)

def armB(a0, M_b, R_f, rho_vac=RHO_L):
    """(F2,V2): X/(4 pi u) = 1/(Z kappa)."""
    uu = C * math.sqrt(G * rho_vac) * R_f ** 2 / (G * M_b)   # kappa-free
    kap = ((1.0 + 8.0 * math.pi * uu / Z_SQ) ** 2 - 1.0) / (4.0 * uu)
    return dict(utilde=uu, kappa=kap)

def armC(a0, M_b, R_f, rho_vac=RHO_L, q_c=None):
    """(F3,V3): X(u_f) = Omega_L/Omega_b."""
    if q_c is None:
        q_c = OM_L / OM_B
    uu = C * math.sqrt(G * rho_vac) * R_f ** 2 / (G * M_b)
    kap = q_c * (1.0 + q_c) / uu
    return dict(utilde=uu, q_c=q_c, kappa=kap)

# ---------------------------------------------------------------- main run
def run(mutate=False):
    R = {}
    foot = "canonical"
    a0 = A0_CANON
    R["constants"] = dict(G=G, c=C, H0=H0, Omega_L=OM_L, Omega_b=OM_B,
                          rho_crit=RHO_CRIT, rho_Lambda=RHO_L,
                          a0_canonical=A0_CANON, a0_alt=A0_ALT,
                          footing_spread_dex=FOOTING_SPREAD,
                          Z=Z_SQ, c_sqrt_G_rhoL=CSQRTGL,
                          kappa_canonical=a0 / CSQRTGL,
                          kappa_alt=A0_ALT / CSQRTGL)

    # ---- G1: the IFF, exact
    kap_c = a0 / CSQRTGL
    R["G1"] = dict(Nv_V1_at_canonical=1.0 / kap_c ** 2,
                   Nv_V1_at_half=1.0 / 0.5 ** 2,
                   kappa_from_Nv4=1.0 / math.sqrt(4.0),
                   statement="N_v(V1)=4 <=> kappa=1/2  (identity from a0 = kappa c sqrt(G rho_L))",
                   result="PASS")

    # ---- G2: G_lambda weights at the MEASURED a0.
    # rho = d ln R_f / d ln a_0 is the fold's own response; the general weights are
    #   w_F1 = -2 + s*(1+2rho) - 3*rho ,  w_V1 = -2
    #   w_F2 = -1 + s*(1+2rho)          ,  w_V2 = -1
    #   w_F3 =      s*(1+2rho)          ,  w_V3 =  0        with s = d ln X/d ln u
    rho = -0.5 if mutate else 0.0          # MUTATE twin: the fold rescales as R_f ~ a0^{-1/2}
    R["rho_fold"] = rho
    w_rows = []
    for lm in sorted(FLD1):
        Rf0 = FLD1[lm][0][0] * KPC
        Mb = 10.0 ** lm * MSUN
        u = a0 * Rf0 ** 2 / (G * Mb)
        s = dlnX_dlnu(u)
        t = s * (1.0 + 2.0 * rho)
        w_rows.append(dict(logM=lm, u_f=u, dlnX_dlnu=s,
                           w_F1=-2.0 + t - 3.0 * rho, w_V1=-2.0,
                           w_F2=-1.0 + t, w_V2=-1.0,
                           w_F3=t, w_V3=0.0))
    R["G2_weights"] = w_rows
    # flat-direction conditions (rho solving w_F = w_V in the deep-field limit s = 1/2)
    R["G2_counter"] = dict(
        statement=("the condition is a FLAT DIRECTION when the two sides carry the same G_lambda "
                   "weight; solving w_F = w_V for rho = d ln R_f/d ln a_0 gives "
                   "rho = +1/4 for arm A and rho = -1/2 for arms B and C (deep-field s = 1/2)"),
        rho_flat_A=0.25, rho_flat_B=-0.5, rho_flat_C=-0.5,
        measured_dlnRf_dlna0_dex_per_dex=2.9e-3,
        source="FINAL-18 (log M_b 10.45, z=0)")
    gaps = [min(abs(r["w_F1"] - r["w_V1"]),
                abs(r["w_F2"] - r["w_V2"]),
                abs(r["w_F3"] - r["w_V3"])) for r in w_rows]
    R["G2"] = dict(min_weight_gap=min(gaps),
                   result="PASS (real constraint, not a flat direction)"
                          if min(gaps) >= 0.1 else "FAIL (flat direction)")

    # ---- the three arms over the mass grid, z = 0
    arms = {}
    for name, fn in (("A", armA), ("B", armB), ("C", armC)):
        rows = []
        for lm in sorted(FLD1):
            Rf0 = FLD1[lm][0][0] * KPC
            Mb = 10.0 ** lm * MSUN
            r = fn(a0, Mb, Rf0)
            r["logM"] = lm
            r["R_fold_kpc"] = Rf0 / KPC
            r["dex_from_half"] = math.log10(r["kappa"] / 0.5)
            # the mismatch N_f/N_v AT the measured a0 (both footings, separately)
            u = a0 * Rf0 ** 2 / (G * Mb)
            X = X_of_u(u)
            rho_c = 3.0 * X * Mb / (4.0 * math.pi * Rf0 ** 3)
            r["Nf_over_Nv_canonical"] = rho_c / RHO_L
            r["Nf_F1_canonical"] = G * rho_c * C ** 2 / a0 ** 2
            u_alt = A0_ALT * Rf0 ** 2 / (G * Mb)
            rho_c_alt = 3.0 * X_of_u(u_alt) * Mb / (4.0 * math.pi * Rf0 ** 3)
            r["Nf_over_Nv_alt"] = rho_c_alt / RHO_L
            rows.append(r)
        ks = [r["kappa"] for r in rows]
        lms = [r["logM"] for r in rows]
        drift = max(ks) / min(ks)
        # best (closest to 1/2) row
        best = min(rows, key=lambda r: abs(r["dex_from_half"]))
        arms[name] = dict(rows=rows,
                          kappa_at_ref=[r["kappa"] for r in rows if r["logM"] == REF_LM][0],
                          dex_from_half_at_ref=[r["dex_from_half"] for r in rows if r["logM"] == REF_LM][0],
                          best_row_logM=best["logM"],
                          best_kappa=best["kappa"],
                          best_dex_from_half=best["dex_from_half"],
                          drift_dex=math.log10(drift),
                          logM_span=lms[-1] - lms[0])
    R["arms"] = arms

    # ---- G3 number; G4 mass drift; G5 epoch drift
    R["G3"] = {}
    for n in ("A", "B", "C"):
        a = arms[n]
        ok = min(abs(r["dex_from_half"]) for r in a["rows"]) <= BAND5
        R["G3"][n] = dict(best_dex=a["best_dex_from_half"], at_logM=a["best_row_logM"],
                          best_kappa=a["best_kappa"],
                          threshold=BAND5, result="PASS" if ok else "FAIL")
    R["G4"] = {}
    for n in ("A", "B", "C"):
        a = arms[n]
        ok = abs(a["drift_dex"]) <= FOOTING_SPREAD
        R["G4"][n] = dict(drift_dex=a["drift_dex"], threshold=FOOTING_SPREAD,
                          result="PASS" if ok else "FAIL")
    # G5: epoch drift, reference mass
    R["G5"] = {}
    Rf = [x * KPC for x in FLD1[REF_LM][0]]
    Mb = 10.0 ** REF_LM * MSUN
    for n, fn in (("A", armA), ("B", armB), ("C", armC)):
        ks = [fn(a0, Mb, r)["kappa"] for r in Rf]
        d = math.log10(max(ks) / min(ks))
        R["G5"][n] = dict(kappa_by_z={str(z): k for z, k in zip(ZS, ks)},
                          drift_dex=d, threshold=FOOTING_SPREAD,
                          result="PASS" if d <= FOOTING_SPREAD else "FAIL")

    # ---- error bar on the primary arm (fold-radius systematics dominate)
    Rf_ref = FLD1[REF_LM][0][0] * KPC
    Mb_ref = 10.0 ** REF_LM * MSUN
    base = armA(a0, Mb_ref, Rf_ref)
    sens = []
    for label, mult in (("FLD1 at-rest-vs-Hubble-flow +22.3%", 1.223),
                        ("FLD1 start-redshift 20/30 +1.4%", 1.014),
                        ("FLD1 shell N 1200->4800 (<0.1 kpc)", 1.0007)):
        k2 = armA(a0, Mb_ref, Rf_ref * mult)["kappa"]
        sens.append(dict(source=label, R_mult=mult,
                         kappa=k2, dex_shift=math.log10(k2 / base["kappa"])))
    rho_1p5 = armA(a0, Mb_ref, Rf_ref, rho_vac=RHO_L * 1.015)
    sens.append(dict(source="Planck rho_Lambda +1.5%", R_mult=1.0,
                     kappa=rho_1p5["kappa"],
                     dex_shift=math.log10(rho_1p5["kappa"] / base["kappa"])))
    err = math.sqrt(sum(s["dex_shift"] ** 2 for s in sens))
    R["primary_error"] = dict(kappa_A=base["kappa"],
                              log10_kappa_A=math.log10(base["kappa"]),
                              sigma_dex=err, sources=sens,
                              plus_minus_dex=err,
                              kappa_A_range=[base["kappa"] * 10 ** (-err), base["kappa"] * 10 ** err])

    # ---- headline mismatch at the measured a0
    R["mismatch_at_measured_a0"] = dict(
        canonical=dict(Nf_over_Nv=arms["A"]["rows"][5]["Nf_over_Nv_canonical"],
                       dex=math.log10(arms["A"]["rows"][5]["Nf_over_Nv_canonical"]),
                       N_f_F1=arms["A"]["rows"][5]["Nf_F1_canonical"], N_v=1.0 / kap_c ** 2),
        alt=dict(Nf_over_Nv=arms["A"]["rows"][5]["Nf_over_Nv_alt"],
                 dex=math.log10(arms["A"]["rows"][5]["Nf_over_Nv_alt"])))

    # ---- G6 mutation arms (frozen in PREREGISTER.md §5)
    mut = {}
    mut["M1_rhoL_to_rhocrit"] = dict(
        kappa=armA(a0, Mb_ref, Rf_ref, rho_vac=RHO_CRIT_ALT)["kappa"],
        expected="up by (1/Omega_L)^{3/2} = 1.77", base=base["kappa"])
    Rta = FLD1[REF_LM][1] * KPC
    mut["M2_Rf_to_0.52Rta"] = dict(
        kappa=armA(a0, Mb_ref, 0.52 * Rta)["kappa"],
        expected="moves through R_f^4", base=base["kappa"])
    mut["M3_mass_x10"] = dict(
        kappa=armA(a0, 10.0 ** (REF_LM + 1) * MSUN, FLD1[11.45][0][0] * KPC if 11.45 in FLD1 else Rf_ref * 10 ** (1 / 3.0))["kappa"],
        expected="up by 10^{1/3} = 2.15", base=base["kappa"])
    mut["M4_z4"] = dict(
        kappa=armA(a0, Mb_ref, FLD1[REF_LM][0][3] * KPC)["kappa"],
        expected="down by (R_f(0)/R_f(4))^4", base=base["kappa"])
    for k, v in mut.items():
        v["ratio"] = v["kappa"] / v["base"]
        v["bites"] = abs(math.log10(v["ratio"])) >= math.log10(1.05)
    R["G6"] = dict(arms=mut,
                   n_bite=sum(1 for v in mut.values() if v["bites"]),
                   result="PASS" if sum(1 for v in mut.values() if v["bites"]) >= 3 else "FAIL")

    # ---- mismatched (unit-inconsistent) pairs, recorded, not graded
    R["mismatched_pairs"] = [
        "(F1,V2) energy density vs de Sitter column  -- INADMISSIBLE",
        "(F1,V3) energy density vs cosmic share      -- INADMISSIBLE",
        "(F2,V1) column vs vacuum energy density     -- INADMISSIBLE",
        "(F2,V3) column vs cosmic share              -- INADMISSIBLE",
        "(F3,V1) share vs vacuum energy density      -- INADMISSIBLE",
        "(F3,V2) share vs de Sitter column           -- INADMISSIBLE",
    ]

    # ---- P6: the radius at which the sector's mean cold density equals the vacuum value.
    #      The boundary condition N_f = N_v is a statement about a DENSITY, so it does pick a
    #      radius; this is where that radius is, at the measured a0. Unmeasured: no profile is
    #      traced this far out.
    r_rows = []
    for lm in sorted(FLD1):
        Rf0 = FLD1[lm][0][0] * KPC
        Mb = 10.0 ** lm * MSUN
        f = lambda r: (3.0 * X_of_u(a0 * r ** 2 / (G * Mb)) * Mb / (4.0 * math.pi * r ** 3)) - RHO_L
        lo, hi = 1e18, 1e28
        for _ in range(300):
            m = (lo + hi) / 2
            if f(m) > 0: lo = m
            else: hi = m
        r = (lo + hi) / 2
        r_rows.append(dict(logM=lm, r_match_kpc=r / KPC, r_match_Mpc=r / (KPC * 1e3),
                           r_over_Rfold=r / Rf0, X_at_r=X_of_u(a0 * r ** 2 / (G * Mb))))
    R["r_match"] = dict(rows=r_rows,
                        at_ref=[x for x in r_rows if x["logM"] == REF_LM][0],
                        dex_span=math.log10(max(x["r_match_Mpc"] for x in r_rows) /
                                            min(x["r_match_Mpc"] for x in r_rows)))

    # ---- headline label
    gates = [str(R["G2"]["result"])] + [str(R["G3"][n]["result"]) for n in "ABC"] + \
            [str(R["G4"][n]["result"]) for n in "ABC"] + [str(R["G5"][n]["result"]) for n in "ABC"]
    gate_names = ["G2"] + [f"G3.{n}" for n in "ABC"] + [f"G4.{n}" for n in "ABC"] + \
                 [f"G5.{n}" for n in "ABC"]
    R["gate_table"] = dict(zip(gate_names, gates))
    derived = all(g.startswith("PASS") for g in gates)
    R["LABEL"] = "DERIVED" if derived else "NOT DERIVED (FITTED)"
    R["failing_gates"] = [f"{n}:{g}" for n, g in zip(gate_names, gates)
                          if not g.startswith("PASS")]
    return R


def main():
    mutate = os.environ.get("out3_MUTATE", "0") == "1"
    R = run(mutate=mutate)
    tag = "MUTATE" if mutate else ""
    with open(f"out3{tag}.json", "w") as f:
        json.dump(R, f, indent=1, default=str)

    L = []
    P = L.append
    P("=" * 100)
    P(f"OUT-3 (SCALE-FREE BOUNDARY): kappa = 1/2 <=> N_f = N_v{tag and '   [MUTATE]'}")
    P("=" * 100)
    P(f"rho_Lambda = {RHO_L:.4e} kg/m^3 (Planck h={H0_H}, Omega_L={OM_L});  "
      f"footings a0 = {A0_CANON:.4e} (canonical) / {A0_ALT:.4e} (alt), NEVER pooled")
    P(f"kappa at the footings: canonical {R['constants']['kappa_canonical']:.6f}, "
      f"alt {R['constants']['kappa_alt']:.6f};  footing spread {FOOTING_SPREAD:.4f} dex")
    P("")
    P("G1  the IFF  " + "-" * 60)
    P(f"  N_v(V1) = G rho_L c^2/a0^2 = 1/kappa^2.  At kappa=1/2, N_v = {R['G1']['Nv_V1_at_half']:.1f}.")
    P(f"  At the canonical footing N_v = {R['G1']['Nv_V1_at_canonical']:.4f} "
      f"(kappa = {R['constants']['kappa_canonical']:.6f}); 1/sqrt(4) = {R['G1']['kappa_from_Nv4']:.1f}.")
    P(f"  => {R['G1']['result']}  (an identity, not a measurement)")
    P("")
    P(f"G2  real constraint or flat direction?  (G_lambda weights, rho = d ln R_f/d ln a0 = {R['rho_fold']:+.2f})" + "-" * 8)
    P(f"  {'logM':>6} {'u_f':>10} {'dlnX/dlnu':>10} {'w_F1':>8} {'w_V1':>6} {'w_F2':>8} {'w_V2':>6} {'w_F3':>8} {'w_V3':>6}")
    for r in R["G2_weights"]:
        P(f"  {r['logM']:6} {r['u_f']:10.3f} {r['dlnX_dlnu']:10.4f} "
          f"{r['w_F1']:8.4f} {r['w_V1']:6.1f} {r['w_F2']:8.4f} {r['w_V2']:6.1f} "
          f"{r['w_F3']:8.4f} {r['w_V3']:6.1f}")
    P(f"  smallest weight gap across the grid = {R['G2']['min_weight_gap']:.4f} (>= 0.1 required)")
    P(f"  => {R['G2']['result']}")
    P(f"  counter-theorem: {R['G2_counter']['statement']}")
    P(f"  what decides it: d ln R_f/d ln a0 = {R['G2_counter']['measured_dlnRf_dlna0_dex_per_dex']} dex/dex "
      f"({R['G2_counter']['source']}); measured at ONE mass and ONE epoch only.")
    P("")
    P("The mismatch at the measured a0 (arm A, canonical, log M_b 10.45)" + "-" * 30)
    m = R["mismatch_at_measured_a0"]
    P(f"  N_f(F1) = G rho_c(Sigma_f) c^2/a0^2 = {m['canonical']['N_f_F1']:.1f}")
    P(f"  N_v(V1) = 1/kappa^2                 = {m['canonical']['N_v']:.4f}")
    P(f"  N_f/N_v = rho_c(fold)/rho_Lambda    = {m['canonical']['Nf_over_Nv']:.1f}  "
      f"({m['canonical']['dex']:.3f} dex)   [alt footing: {m['alt']['Nf_over_Nv']:.1f}, {m['alt']['dex']:.3f} dex]")
    P("")
    P("G3  the number (root of N_f = N_v, exact inversion, no deep-field approximation)" + "-" * 12)
    P(f"  {'arm':>4} {'slot':>16} {'kappa @10.45':>13} {'dex @10.45':>11} "
      f"{'best kappa':>13} {'best dex':>10} {'at logM':>8} {'verdict':>7}")
    for n in "ABC":
        a = R["arms"][n]
        g3 = R["G3"][n]
        slot = {"A": "energy density", "B": "column", "C": "share"}[n]
        P(f"  {n:>4} {slot:>16} {a['kappa_at_ref']:13.5e} {a['dex_from_half_at_ref']:11.4f} "
          f"{g3['best_kappa']:13.5e} {g3['best_dex']:10.4f} {g3['at_logM']:8} {g3['result']:>7}")
    P(f"  threshold: |log10(kappa/0.5)| <= {BAND5:.4f} dex (5 %) at SOME mass in the grid")
    P("")
    P("G4  universality in mass  (log M_b 7 -> 11.5, z = 0)" + "-" * 37)
    P(f"  {'arm':>4} {'kappa(7)':>12} {'kappa(11.5)':>12} {'drift dex':>10} {'verdict':>7}")
    for n in "ABC":
        a = R["arms"][n]
        P(f"  {n:>4} {a['rows'][0]['kappa']:12.4e} {a['rows'][-1]['kappa']:12.4e} "
          f"{a['drift_dex']:10.4f} {R['G4'][n]['result']:>7}")
    P(f"  threshold: |drift| <= {FOOTING_SPREAD:.4f} dex (the canonical/alt footing spread)")
    P("")
    P("G5  universality in epoch  (log M_b 10.45, z = 0,1,2,4)" + "-" * 38)
    for n in "ABC":
        g = R["G5"][n]
        P(f"  arm {n}: " + "  ".join(f"z{z}={v:.4e}" for z, v in
                                     [(z, g['kappa_by_z'][str(z)]) for z in ZS]) +
          f"   drift {g['drift_dex']:.4f} dex  {g['result']}")
    P("")
    P("Error bar on the primary arm (A)  " + "-" * 55)
    e = R["primary_error"]
    P(f"  kappa_A = {e['kappa_A']:.4e}   log10 = {e['log10_kappa_A']:.4f}  +/- {e['sigma_dex']:.3f} dex")
    P(f"  range    [{e['kappa_A_range'][0]:.3e}, {e['kappa_A_range'][1]:.3e}]")
    for s in e["sources"]:
        P(f"    {s['source']:42s} R x{s['R_mult']:.4f}  shift {s['dex_shift']:+.4f} dex")
    P("")
    P("G6  mutation  " + "-" * 66)
    for k, v in R["G6"]["arms"].items():
        P(f"  {k:22s} kappa {v['kappa']:.4e}  ratio {v['ratio']:.4g}  "
          f"expected {v['expected']:32s} {'BITES' if v['bites'] else 'no bite'}")
    P(f"  arms that bite: {R['G6']['n_bite']}/4  => {R['G6']['result']}")
    P("")
    P("Inadmissible (unit-mismatched) pairs, recorded not graded:" + "-" * 32)
    for s in R["mismatched_pairs"]:
        P("  " + s)
    P("")
    P("P6  where the boundary condition would actually be satisfied  " + "-" * 32)
    rm = R["r_match"]
    P("  the radius r* at which the halo's MEAN cold density equals rho_Lambda (measured a0, z = 0):")
    P(f"  {'logM':>6} {'r* (Mpc)':>10} {'r*/R_fold':>10}")
    for x in rm["rows"]:
        P(f"  {x['logM']:6} {x['r_match_Mpc']:10.3f} {x['r_over_Rfold']:10.1f}")
    P(f"  span over the grid: {rm['dex_span']:.3f} dex (scales as M_b^(1/4)); "
      f"NOT the fold radius")
    P("")
    P("=" * 100)
    P(f"LABEL: {R['LABEL']}")
    P(f"failing gates: {', '.join(R['failing_gates'])}")
    P("kappa = 1/2 FITTED; not theory closed.")
    P("=" * 100)
    txt = "\n".join(L)
    print(txt)
    with open(f"out3{tag}.out", "w") as f:
        f.write(txt + "\n")

    # ---- the full menu: every admissible (arm, mass, epoch) row, nothing hidden
    M = []
    M.append("# OUT-3 menu: every admissible unit-matched row. Nothing is selected post hoc.")
    M.append("# columns: arm  logM_b  z  R_fold(kpc)  kappa_root  log10(kappa/0.5)")
    Rf_all = {}
    for lm in sorted(FLD1):
        for zi, z in enumerate(ZS):
            Rf_all[(lm, z)] = FLD1[lm][0][zi] * KPC
    a0 = A0_CANON
    for n, fn in (("A", armA), ("B", armB), ("C", armC)):
        for lm in sorted(FLD1):
            Mb = 10.0 ** lm * MSUN
            for z in ZS:
                Rf = Rf_all[(lm, z)]
                k = fn(a0, Mb, Rf)["kappa"]
                M.append(f"{n} {lm:6.2f} {z:2d} {Rf/KPC:9.1f} {k:14.6e} {math.log10(k/0.5):+11.4f}")
    M.append("")
    M.append("# inadmissible (unit-mismatched) pairs: not computed, not graded, not counted")
    for s in R["mismatched_pairs"]:
        M.append("#   " + s)
    with open("out3_menu.out", "w") as f:
        f.write("\n".join(M) + "\n")


if __name__ == "__main__":
    main()
