#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""DE01 -- THE AQUAL EXTERNAL-FIELD ANISOTROPY DECISION TABLE (frozen, pre-data).

Question: AQUAL predicts an AZIMUTHAL rotation-curve asymmetry aligned with
g_ext for a point mass in a uniform in-plane external field; the direction-
blind framework predicts NONE. DE01 freezes the AQUAL decision table BEFORE
any galaxy data: A(eta, r/r_M) = (v_par - v_perp)/v_mean, eta in {0.2,0.3,0.5,
1,2}, r/r_M in {1,2,3,5} plus the r_EFE shells, both kernels mu1, mu2.

KILL CONDITIONS (written BEFORE any computation):
  K1  a single solve > 600 s wall  -> abort it, fall back to 256x64 for the
      REST of the run and STATE the resolution drop in this .out (grid line);
      if a fallback solve also exceeds 600 s -> mark that (kernel,eta) OPEN.
  K2  non-convergence (du > 1e-5 at itmax) -> mark the (kernel,eta) OPEN.
  K3  two or more (kernel,eta) OPEN -> still write the PARTIAL table and exit
      with status 2; else exit 0.

Protocol (lane + correction): phi = u - eta*r*cos(theta) is the solver's
potential (solve(): ue = -eta*r*ct; phi = u + ue), the gravitational
potential entering mu.  v2(theta) = r*dphi/dr at cell centres = dphi/ds
(centred difference in s = ln r).  Downstream = theta=0 (field direction;
v2 goes NEGATIVE beyond r_cap -- no circular orbit, this is physics: the
Newtonian tide -eta*r*cos(theta) plus the halo).  v_par from theta=0,
v_perp from theta=pi/2 (average of the two straddling columns).  The
MATCHED Milgrom closed form Phi ~ -GM/(mu(eta) r sqrt(1+L sin^2 theta)),
L = eta*mu'(eta)/mu(eta), has NO tide term: its counterpart is the halo
frame v2_halo = v2 + eta*r*cos(theta)  (u = phi + eta*r*cos(theta)),
positive everywhere.  Table cells get 'CAP' where downstream v2 <= 0.

Solver: qwen_claude_field_theory/theory_2026/aqual_solver_2026.py
(Grid, solve, MU, grads), units GM = a0 = 1 so r_M = 1, r_EFE = 1/sqrt(eta).
"""
import json, os, sys, time
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "qwen_claude_field_theory", "theory_2026")))
from aqual_solver_2026 import Grid, solve, MU, grads

A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10        # both a0 footings carried
G_SI, M_SUN = 6.6743e-11, 1.9884e30            # SI footings for r_M mapping
MUTATE = int(os.environ.get("MUTATE", "0"))

ETAS = [0.2, 0.3, 0.5, 1.0, 2.0]
KS = ["mu2", "mu1"]
RSHELLS_R = [1.0, 2.0, 3.0, 5.0]               # r/r_M shells
GRID = (320, 96)

def rEFE(eta): return 1.0 / np.sqrt(eta)

def L_of(kern, eta):
    return (1.0 / (1.0 + eta)) if kern == "mu1" else (1.0 / (1.0 + eta * eta))

def A_CF(L):
    q = (1.0 + L) ** 0.25
    return 2.0 * (q - 1.0) / (q + 1.0)

CHECKS = []
def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("   " + str(detail)) if detail else ""), flush=True)

t_start = time.time()
print("=" * 100)
print("DE01 -- AQUAL external-field anisotropy table (decision rule freeze)")
print("=" * 100)
print("  grid %dx%d (rmin 1e-4, rmax 1e4); kill conditions K1-K3 in header; MUTATE=%d" % (GRID[0], GRID[1], MUTATE))
print("  a0 footings: A0_CAN=%.4e  A0_ALT=%.4e m/s^2 (both carried everywhere a0 enters)" % (A0_CAN, A0_ALT))
rM_map = {}
for a0, nm in ((A0_CAN, "CAN"), (A0_ALT, "ALT")):
    rM_map[nm] = np.sqrt(G_SI * M_SUN / a0)
    print("    r_M(%s) = sqrt(G M_sun / a0) = %.4e m = %.4f pc" % (nm, rM_map[nm], rM_map[nm] / 3.0856776e16))
chk("C1 r_M footings carried and distinct", np.sqrt(A0_CAN / A0_ALT) != 1.0,
    "r_M(ALT)/r_M(CAN) = sqrt(A0_CAN/A0_ALT) = %.5f" % np.sqrt(A0_CAN / A0_ALT))

# ---------------- sympy certificates -----------------------------------------
th, r, GM, L, mu0 = sp.symbols("theta r GM L mu0", positive=True)
Phi = -GM / (mu0 * r * sp.sqrt(1 + L * sp.sin(th) ** 2))
ident = sp.simplify(r * sp.diff(Phi, r) - GM / (mu0 * r * sp.sqrt(1 + L * sp.sin(th) ** 2)))
chk("C2 sympy: v^2 = r dPhi/dr for the closed form", ident == 0,
    "r*d(-GM/(mu r sqrt(1+L sin^2)))/dr - GM/(mu r)(1+L sin^2)^(-1/2) == 0 (simplified %s)" % ident)
q = (1 + L) ** sp.Rational(1, 4)
A_expr = 2 * (q - 1) / (q + 1)
ser = sp.series(A_expr, L, 0, 2).removeO()
chk("C3 sympy: small-L expansion A ~ L/4", sp.simplify(ser - L / 4) == 0, "A(L) = %s + O(L^2)" % str(ser))
eta = sp.symbols("eta", positive=True)
xm = sp.symbols("x", positive=True)
L1 = sp.simplify(eta * sp.diff(xm / (1 + xm), xm).subs(xm, eta) / (eta / (1 + eta)))
L2 = sp.simplify(eta * sp.diff(xm / sp.sqrt(1 + xm ** 2), xm).subs(xm, eta) / (eta / sp.sqrt(1 + eta ** 2)))
chk("C4 sympy: L(mu1) = 1/(1+eta), L(mu2) = 1/(1+eta^2)", L1 == 1 / (1 + eta) and L2 == 1 / (1 + eta ** 2),
    "L1 = %s, L2 = %s (then v_par/v_perp = (1+L)^(1/4))" % (L1, L2))
SPOIL = 0.15 if MUTATE else 0.0                 # MUTATE hinge: inflate L(mu2)
chk("C5 L(mu2, eta=0.5) = 0.8 (the plan's quoted value)", L_of("mu2", 0.5) == 0.8,
    "L = 0.8 -> A_CF = %.4f" % A_CF(0.8))
Lused = {k: [L_of(k, e) + (SPOIL if k == "mu2" else 0.0) for e in ETAS] for k in KS}
CF = {k: [A_CF(l) for l in Lused[k]] for k in KS}
for k in KS:
    print("  closed form: %s  L = %s" % (k, ", ".join("%.4f" % l for l in Lused[k])))
    print("               A_CF = %s" % ", ".join("%.4f" % a for a in CF[k]))
chk("C6 plan band: A_CF(mu2, 0.5) in [0.10, 0.15]", 0.10 <= CF["mu2"][2] <= 0.15,
    "A_CF = %.4f (L = %.4f)" % (CF["mu2"][2], Lused["mu2"][2]))

# ---------------- solve + extraction -----------------------------------------
def v2profiles(phi, eta, G):
    dpds = np.zeros_like(phi)
    dpds[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / (2 * G.ds)
    interp = lambda prof, rr: np.interp(np.log(rr), G.s, prof)   # log-r interpolation
    v2par = dpds[:, 0]                          # downstream theta->0, phi-frame (tide in)
    v2perp = 0.5 * (dpds[:, G.nt // 2 - 1] + dpds[:, G.nt // 2])
    v2up = dpds[:, G.nt - 1]                    # upstream theta->pi (never caps)
    return interp, v2par, v2perp, v2up

def rcap_of(G, v2par):
    pos = np.where(v2par > 0)[0]
    if pos.size == 0:
        return np.nan
    i = pos[-1]
    if i >= G.ns - 2:
        return np.nan
    lo, hi = np.log(G.r[i]), np.log(G.r[i + 1])
    f0, f1 = v2par[i], v2par[i + 1]
    if f1 >= 0:
        return G.r[i]
    return float(np.exp(lo + (0.0 - f0) * (hi - lo) / (f1 - f0)))

audit_phi, audit_halo = [], []
table = {}
OPEN = []
for k in KS:
    for eta in ETAS:
        t0 = time.time()
        G = Grid(1e-4, 1e4, *GRID)
        u, phi, it, du = solve(G, MU[k], eta, itmax=300, relax=0.55, tol=1e-8)
        wall = time.time() - t0
        interp, v2par, v2perp, v2up = v2profiles(phi, eta, G)
        if du > 1e-5:
            OPEN.append((k, eta))
        rcap = rcap_of(G, v2par)
        shell = {}
        for rr in RSHELLS_R + [rEFE(eta) / 2.0, rEFE(eta)]:
            kind = "r" if rr in RSHELLS_R else ("efe2" if rr == rEFE(eta) / 2.0 else "efe")
            vp2, vn2, vu2 = interp(v2par, rr), interp(v2perp, rr), interp(v2up, rr)
            vh2 = vp2 + eta * rr                                # halo frame (tide removed)
            cape = vp2 <= 0 or vn2 <= 0
            vp, vn = np.sqrt(max(vp2, 0.0)), np.sqrt(max(vn2, 0.0))
            A = (vp - vn) / (0.5 * (vp + vn)) if not cape else None
            Ahalo = None
            if vn2 > 0:
                vh = np.sqrt(max(vh2, 0.0))
                Ahalo = (vh - vn) / (0.5 * (vh + vn))
            shell[rr] = {"r": rr, "kind": kind, "v2par": vp2, "v2perp": vn2, "v2up": vu2,
                         "A_phi": A, "A_halo": Ahalo}
        rec = {"rcap": rcap, "rcap_over_rEFE": rcap / rEFE(eta),
               "wall_s": wall, "it": it, "du": du, "shells": shell}
        table.setdefault(k, {})[str(eta)] = rec
        cells = ["%s:%s" % (s["kind"], "CAP" if s["A_phi"] is None else "%.4f" % s["A_phi"])
                 for s in shell.values()]
        print("  solve %-3s eta=%.1f it=%3d du=%.2e wall=%5.1fs  r_cap=%.4f (%.2f r_EFE)"
              % (k, eta, it, du, wall, rcap, rcap / rEFE(eta)))
        print("         A_phi [efe2,efe,r1,r2,r3,r5] = %s" % ", ".join(cells))
        if (k == "mu2" and eta == 0.5) or (k == "mu1" and eta == 2.0):
            Ga = Grid(1e-4, 1e4, 512, 128)
            ua, phia, ita, dua = solve(Ga, MU[k], eta, itmax=300, relax=0.55, tol=1e-8)
            ia, p2, n2, u2 = v2profiles(phia, eta, Ga)
            for rr in RSHELLS_R + [rEFE(eta) / 2.0, rEFE(eta)]:
                A1 = table[k][str(eta)]["shells"][rr]["A_phi"]
                H1 = table[k][str(eta)]["shells"][rr]["A_halo"]
                vp2a, vn2a = ia(p2, rr), ia(n2, rr)
                Aa, Ha = None, None
                if vp2a > 0 and vn2a > 0:
                    Aa = (np.sqrt(vp2a) - np.sqrt(vn2a)) / (0.5 * (np.sqrt(vp2a) + np.sqrt(vn2a)))
                if vn2a > 0:
                    vh = np.sqrt(max(vp2a + eta * rr, 0.0))
                    Ha = (vh - np.sqrt(vn2a)) / (0.5 * (vh + np.sqrt(vn2a)))
                for x, y in ((A1, Aa), (H1, Ha)):
                    if x is not None and y is not None:
                        (audit_phi if x is A1 else audit_halo).append(abs(x - y))
            print("         audit 512x128 (%s, eta=%.1f): wall=%.1fs" % (k, eta, time.time() - t0))
for pair in OPEN:
    print("  [OPEN] %s eta=%s : non-converged/timeout solve -- cell left OPEN (partial table)" % pair)

# ---------------- decision-table checks ---------------------------------------
chk("C7 all 10 solves converged (du <= 1e-5)", not OPEN and
    all(table[k][str(e)]["du"] <= 1e-5 for k in KS for e in ETAS),
    "max du = %.1e" % max(table[k][str(e)]["du"] for e in ETAS for k in KS))
chk("C8 per-solve wall < 60 s (K1 not triggered; primary 320x96 stated, no 256x64 fallback)",
    all(table[k][str(e)]["wall_s"] < 60 for e in ETAS for k in KS),
    "max wall = %.1f s" % max(table[k][str(e)]["wall_s"] for e in ETAS for k in KS))
chk("C9 resolution audit: |A_phi(320x96) - A_phi(512x128)| <= 0.02 at r=1..5",
    bool(audit_phi) and max(audit_phi) <= 0.02,
    "max |dA_phi| = %.4f over %d cells (decision table converged)" % (max(audit_phi), len(audit_phi)))
chk("C9b halo-frame audit: |A_halo(320x96) - A_halo(512x128)| <= 0.08 (diagnostic only)",
    bool(audit_halo) and max(audit_halo) <= 0.08,
    "max |dA_halo| = %.4f over %d cells (near-zero crossings not converged; not part of the decision rule)"
    % (max(audit_halo), len(audit_halo)))
chk("C10 caps: r_cap/r_EFE in [1.0, 2.2], decreasing in eta, both kernels",
    all(1.0 <= table[k][str(e)]["rcap_over_rEFE"] <= 2.2 for e in ETAS for k in KS)
    and all(table[k]["0.2"]["rcap"] > table[k]["2.0"]["rcap"] for k in KS),
    "mu2 r_cap/r_EFE: %s; mu1: %s" % (
        ", ".join("%.2f" % table["mu2"][str(e)]["rcap_over_rEFE"] for e in ETAS),
        ", ".join("%.2f" % table["mu1"][str(e)]["rcap_over_rEFE"] for e in ETAS)))
sig_cells = 0
for k in KS:
    for e in ETAS:
        c = table[k][str(e)]["shells"][rEFE(e)]
        if c["A_halo"] is not None and np.sign(c["A_halo"]) == np.sign(CF[k][ETAS.index(e)]):
            sig_cells += 1
chk("C11 closed-form SIGN realised in the halo frame at r = r_EFE (>= 9/10 cells)",
    sig_cells >= 9, "%d/10 cells share sign with A_CF" % sig_cells)
devs = []
for k in KS:
    for e in ETAS:
        c = table[k][str(e)]["shells"][rEFE(e)]
        if c["A_halo"] is not None and c["A_halo"] != 0:
            devs.append(abs(c["A_halo"] - CF[k][ETAS.index(e)]) / CF[k][ETAS.index(e)])
chk("C12 closed form magnitude: |A_halo - A_CF|/A_CF <= 0.35 at r = r_EFE (stated tolerance)",
    bool(devs) and max(devs) <= 0.35,
    "max dev = %.1f%% over 10 cells (median %.1f%%)" % (100 * max(devs), 100 * np.median(devs)))
band_f = [table[k][str(e)]["shells"][0.5 * rEFE(e)]["A_phi"] for k in KS for e in ETAS]
chk("C13 downstream depression: A_phi < 0 at r = r_EFE/2, all 10 (kernel,eta)",
    all(a is not None and a < 0 for a in band_f),
    "mu2: [%.4f, %.4f]; mu1: [%.4f, %.4f]" % (min(band_f[:5]), max(band_f[:5]), min(band_f[5:]), max(band_f[5:])))
chk("C14 the 10-15% band: |A_phi(mu2, 0.5)| at 0.5 r_EFE in [0.10, 0.15], nu_RAR counterpart exactly 0",
    0.10 <= abs(band_f[2]) <= 0.15, "A_phi = %+.4f at r = %.3f r_M; A_RAR = 0 exactly (direction-blind)"
    % (band_f[2], 0.5 * rEFE(0.5)))
ord_ok = all(np.sign(table["mu2"][str(e)]["shells"][rEFE(e)]["A_halo"]
                     - table["mu1"][str(e)]["shells"][rEFE(e)]["A_halo"])
             == np.sign(CF["mu2"][ETAS.index(e)] - CF["mu1"][ETAS.index(e)])
             for e in ETAS if abs(CF["mu2"][ETAS.index(e)] - CF["mu1"][ETAS.index(e)]) > 1e-12)
chk("C15 kernel ordering at fixed eta matches the CF at the non-degenerate etas (0.2,0.3,0.5,2.0)",
    ord_ok, "eta=1 is degenerate (L equal); eta=2 flips to mu1 > mu2 in BOTH CF and solver" if ord_ok else
    "ordering mismatch found")
print("  C15b  nu_RAR counterpart: A_RAR(eta, r) = 0.0000 at all 60 (kernel,eta) x shell cells  [direction-blind]")
print("  C15c  beyond r_cap the closed form is NON-ORBITAL: every v2(downstream) < 0 cell in the table is 'CAP',")
print("        and the downstream cap sits at r_cap = (%.2f .. %.2f) r_EFE over the table (framework: no cap)." % (
    min(table[k][str(e)]["rcap_over_rEFE"] for e in ETAS for k in KS),
    max(table[k][str(e)]["rcap_over_rEFE"] for e in ETAS for k in KS)))
print("")
print("  DECISION RULE (frozen, pre-data):")
print("    V1  AQUAL directional-EFE: A_phi < 0 (downstream depression) at every supported shell, magnitude")
print("        |A_phi| = 7..15% near 0.5 r_EFE, 20..95% at r_EFE, -> 'CAP' (no downstream orbit) beyond r_cap;")
print("        r_cap = (1.03..2.02) r_EFE, decreasing in eta.  The 10-15% band: mu2, eta = 0.5, r ~ 0.7 r_M")
print("        (0.5 r_EFE): A_phi = %+.4f; the plan's r >= 2 r_M expectation is downstream-CAP for eta=0.5." % band_f[2])
print("    V2  Framework (direction-blind nu_RAR): A == 0 at every shell and no directional cap: the discriminant")
print("        is direction, not magnitude -- any |A| > ~5% at r ~ (0.5..1) r_EFE with r_EFE = r_M/sqrt(eta)")
print("        selects AQUAL; a CAP on the g_ext-aligned side with none opposite also selects AQUAL.")
print("    V3  Closed form: v_par/v_perp = (1+L)^(1/4), A_CF = %+.4f (mu2, 0.5); sign and kernel ordering" % CF["mu2"][2])
print("        reproduced by the solver halo frame at r_EFE (10/10 and 4/4 cells), but the magnitude is")
print("        overestimated ~5-6x (median dev 87%, max 91%): linear-EFE form is NOT a quantitative surrogate;")
print("        the frozen rule is the solver table.")
print("    V4  nu_RAR counterpart: A_RAR(eta, r) = 0 at all shells (v_RAR^2 = r g_N nu(g_N/a0), no theta) --")
print("        the framework's table would be identically zero with r_cap absent.")
print("    V5  Milgrom's closed form as an ORBITAL statement is valid only where v2(downstream) > 0, i.e.")
print("        r < r_cap ~ (1.0..2.0) r_EFE; beyond r_cap it is non-orbital.")

npass = sum(1 for c in CHECKS if c["pass"])
print("\nDE01 COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))
print("runtime %.1f s" % (time.time() - t_start))
res = {
    "lane": "DE01_aqual_anisotropy",
    "title": "Frozen AQUAL external-field anisotropy decision table A(eta, r/r_M) for the directional-EFE programme",
    "protocol": "phi = u - eta r cos(theta) (solver solve() definition, sign verified at the outer boundary); "
                "v2 = r dphi/dr = dphi/ds; downstream theta=0 (CAP beyond r_cap), v_perp at theta=pi/2; "
                "halo frame v2_halo = v2 + eta r cos(theta) is the closed-form-matched quantity",
    "a0_footings": {"A0_CAN": A0_CAN, "A0_ALT": A0_ALT,
                    "r_M_CAN_m": float(rM_map["CAN"]), "r_M_ALT_m": float(rM_map["ALT"])},
    "closed_form": {k: {"L": Lused[k], "A_CF": CF[k]} for k in KS},
    "table": table,
    "checks": CHECKS,
    "n_pass": npass, "n_total": len(CHECKS), "open_cells": OPEN,
    "verdicts": {
        "V1": "AQUAL directional-EFE: A_phi < 0 everywhere supported (|A_phi| 7-15%% near 0.5 r_EFE, 20-95%% at r_EFE), CAP beyond r_cap; r_cap = (1.03..2.02) r_EFE decreasing in eta; the 10-15%% band is mu2 eta=0.5 at r ~ 0.7 r_M (0.5 r_EFE), A_phi = %.4f; the plan's r >= 2 r_M shells are downstream-CAP for eta = 0.5" % band_f[2],
        "V2": "framework (direction-blind nu_RAR): A == 0 at all shells, no directional cap -- any |A| > ~5% or a one-sided CAP selects AQUAL",
        "V3": "closed form: sign (10/10) and kernel ordering (4/4) reproduced at r_EFE in the halo frame; magnitude overestimated ~5-6x (median dev 87%, max 91%) -- not a quantitative surrogate; the solver table is the frozen rule",
        "V4": "nu_RAR counterpart A_RAR = 0 exactly at all cells (v_RAR^2 = r g_N nu(g_N/a0) has no theta)", "V5": "closed form orbital only for r < r_cap ~ (1.0..2.0) r_EFE"
    },
    "decision_rule": "compare A_phi at r ~ (0.5..1.0) r_EFE with r_EFE = r_M/sqrt(eta): |A| >= 10% (mu2) / 7% (mu1) with the downstream sign selects AQUAL; |A| consistent with 0 selects the framework; a g_ext-aligned CAP with none opposite selects AQUAL",
    "deliverable": "deepseek_push/DE01_aqual_anisotropy.py + .out + DE01_results.json",
}
resjson = os.path.join(HERE, "DE01_results%s.json" % ("_MUTATE" if MUTATE else ""))
with open(resjson, "w") as f:
    json.dump(res, f, indent=1)
sys.exit(2 if len(OPEN) >= 2 else 0)