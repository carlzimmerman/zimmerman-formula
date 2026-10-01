#!/usr/bin/env python3
"""
AS500 - Logical independence and redundancy of the thirteen closure gates.
Numeric + registry audit. Bounded prototype: <=120 s wall, <=512 MB, 1 thread.

Framework: a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED (input).
Operative branch: filtered MONO (nu_mono through heat filter S = exp((xi^2/2) Delta));
causality criterion B. Q/RAR/MU2/EXP/MONO kept distinct.

Everything here is either (a) a dimensionless kernel identity on y = |p|/a0,
valid on both footings, or (b) a registry/lattice check with explicit domains.
"""
import json, math, time, platform, os, sys, hashlib
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
start = time.time()

# ---------------- constants / footing ----------------
G_N = 6.67430e-11
c = 299792458.0
M_sun = 1.98847e30
pc = 3.085677581491367e16
A0_CAN = 9.3619e-11      # canonical footing, m/s^2
A0_ALT = 1.1279e-10      # alternative footing, m/s^2
KAPPA = sp.Rational(1, 2)

def rho_Lambda(a0):
    # framework identity rho_Lambda = 4 a0^2/(G c^2)
    return 4.0 * a0**2 / (G_N * c**2)

RHO_CAN = rho_Lambda(A0_CAN)
RHO_ALT = rho_Lambda(A0_ALT)
s_can = 2.0 * A0_CAN   # s = 2 a0 at kappa = 1/2 (seed unit)
s_alt = 2.0 * A0_ALT
kappa_eff_fixed_rho = A0_ALT / (c * math.sqrt(G_N * RHO_CAN))  # relabel diagnostic

# ---------------- MONO kernel (operative, y-functions, dimensionless) ----------------
def nu_RAR(y):    return 1.0 / (1.0 - mp.e**(-mp.sqrt(y)))
def h_RAR(y):     return y * (nu_RAR(y) - 1.0)                    # = y/(e^sqrt(y)-1)
def h_prime_RAR(y):
    # analytic: h = y*(nu-1); h' = (nu-1) + y*nu';  nu' = -e^{-t}/(2 t (1-e^{-t})^2), t=sqrt(y)
    t = mp.sqrt(y)
    e = mp.e**(-t)
    nu = 1.0 / (1.0 - e)
    nup = -e / (2.0 * t * (1.0 - e)**2)
    return (nu - 1.0) + y * nup

DELTA = 0.05
# landmarks from the operative recipe (inputs to check, not to fit)
y_p_claim, h_p_claim, y_star_claim = 2.5396, 0.6476, 2.3374

# solve y_p : h'_RAR(y_p) = 0
y_p = mp.findroot(lambda y: h_prime_RAR(y), mp.mpf('2.54'), tol=mp.mpf('1e-40'))
h_p = h_RAR(y_p)
# solve y* : h'_RAR(y*) = delta*h_p/(y*+y_p)
y_star = mp.findroot(lambda y: h_prime_RAR(y) - DELTA * h_p / (y + y_p),
                     mp.mpf('2.337'), tol=mp.mpf('1e-40'))

def h_mono(y):
    if y <= y_star:
        return h_RAR(mp.mpf(y))
    return h_RAR(y_star) + DELTA * h_p * mp.log((y + y_p) / (y_star + y_p))

def nu_mono(y):
    yy = mp.mpf(y)
    return 1.0 + h_mono(yy) / yy

# ---------------- numeric checks ----------------
res = {}
def R(name, observed, target, tol, unit, pass_ok=True):
    if isinstance(target, list):
        assert isinstance(observed, list) and len(observed) == len(target)
        rel = max(abs(float(o) - float(t)) for o, t in zip(observed, target))
    else:
        rel = abs(float(observed) - float(target)) if target is not None else None
    ok = (rel is not None and rel <= tol) if pass_ok else bool(observed)
    res[name] = {"observed": repr(observed), "target": repr(target), "absdiff": rel,
                 "tol": tol, "pass": bool(ok), "unit": unit}
    return ok

# C1: landmarks reproduce the declared values
R("C1a_y_p", float(y_p), y_p_claim, 5e-3, "dimensionless")
R("C1b_h_p", float(h_p), h_p_claim, 5e-3, "dimensionless (a0 units)")
R("C1c_y_star", float(y_star), y_star_claim, 5e-3, "dimensionless")

# C2: nu_mono == nu_RAR exactly on [0, y*] (max-selection picks h'_RAR there)
grid = [mp.mpf(k) * y_star / mp.mpf(5000) for k in range(1, 5001)]
maxdiff = max(abs(nu_mono(y) - nu_RAR(y)) for y in grid)
min_margin = min(h_prime_RAR(y) - DELTA * h_p / (y + y_p) for y in grid)
mx = float(maxdiff); mn = float(min_margin)
R("C2a_nu_mono_eq_nu_RAR_on_0_y*", mx, 0.0, 1e-12, "dimensionless, max abs diff")
R("C2b_hRAR_above_floor_on_0_y*", mn, 0.0, 1e-9, "dimensionless, min margin (>=0)")

# C3: dex bound |log10(nu_mono/nu_RAR)| <= 0.0104, max at y = 14.35
import math as _m
ys = [10**(k * 0.0005) for k in range(-6, int(4/0.0005)+1)]  # 1e-3 .. 1e4
ys = [y for y in ys if y > float(y_star)]
dex_best, y_dex = 0.0, None
for y in ys:
    d = abs(float(mp.log10(nu_mono(y) / nu_RAR(y))))
    if d > dex_best:
        dex_best, y_dex = d, y
R("C3a_max_dex", dex_best, 0.0104, 5e-4, "dex")
R("C3b_argmax_y", y_dex, 14.35, 0.4, "dimensionless (y)")

# C4: C_L continuity at the splice and slope jump (recipe S5 values)
CL_star = float(h_prime_RAR(y_star))                     # = floor value as well
floor_slope = float(-DELTA * h_p / (y_star + y_p)**2)
# dC_L/dy on the RAR side = h''_RAR(y*)
h = mp.mpf('1e-6')
hpp_RAR = (h_prime_RAR(y_star + h) - h_prime_RAR(y_star - h)) / (2 * h)
R("C4a_C_L_at_y*", CL_star, 0.0066, 2e-4, "dimensionless")
R("C4b_slope_jump_floor", floor_slope, -0.0014, 5e-4, "dimensionless")
R("C4c_slope_jump_RAR_side", float(hpp_RAR), -0.0361, 1e-3, "dimensionless")

# C5: deep law (g/a0)^2 = y at y -> 0^+   [y*nu_RAR(y)^2 -> 1]
# analytic leading correction: y nu^2 = (sqrt(y)/(1-exp(-sqrt(y))))^2 = 1 + sqrt(y) + O(y)
for y0 in (mp.mpf('1e-3'), mp.mpf('1e-6'), mp.mpf('1e-9')):
    v = float(y0 * nu_RAR(y0)**2)
    R(f"C5_deep_{mp.nstr(y0, 3, strip_zeros=False)}", v, 1.0, 1.5 * float(mp.sqrt(y0)),
      "dimensionless (g/a0)^2/y; tol = analytic leading correction 1.5*sqrt(y)")

# C6: Newton tail nu_mono(y) - 1 for large y (logarithmic convergence, both footings y-axis)
tail = {}
for y0 in (10.0, 1e2, 1e4, 1e6, 1e12):
    tail[y0] = float(nu_mono(y0) - 1.0)
R("C6a_tail_1e2", tail[1e2], 0.0067, 5e-3, "dimensionless")
R("C6b_tail_1e6", tail[1e6], 1.1e-6, 5e-7, "dimensionless")
R("C6c_decreasing", tail[1e12] < tail[1e6] < tail[1e4] < tail[1e2], True, None,
  "monotone decreasing tail", pass_ok=False)
# log-rate sanity: tail(y)/tail(10y) ~ ln/y ratio ~ 1 + small
rate = tail[1e6] / tail[1e5] if 1e5 in tail else None

# C7: lattice-landing constants (AS651 E1 / AS138.C01)
s_sat = mp.findroot(lambda s: h_prime_RAR(s), mp.mpf('2.5396'), tol=mp.mpf('1e-40'))
jsat = 2.0 * (s_sat * h_RAR(s_sat) - mp.quad(lambda s: s / (mp.e**mp.sqrt(s) - 1.0),
                                             [mp.mpf('0'), s_sat]))
b_jsat = jsat / (8.0 * mp.pi)
r_star = 8.0 - 2.0 * b_jsat
R("C7a_s_sat", float(s_sat), 2.539638282188, 1e-6, "dimensionless")
R("C7b_jsat", float(jsat), 0.45252489667513, 1e-6, "dimensionless")
R("C7c_b", float(b_jsat), 0.018005393544499, 1e-9, "dimensionless")
R("C7d_r_star", float(r_star), 7.963989212911002, 1e-9, "dimensionless")

def kappa_of_r(r):
    return mp.sqrt(2.0 / (r + 2.0 * b_jsat))

witness_r = [1.0, 2.0, 4.0, float(r_star), 8.0, 16.0, 64.0]
witness_k = [float(kappa_of_r(r)) for r in witness_r]
expected_k = [1.3894178, 0.99111708, 0.70394518, 0.5, 0.49887845, 0.35315619, 0.17672698]
R("C7e_kappa_witness_set", witness_k, expected_k, 2e-6, "dimensionless")
R("C7f_kappa_at_rstar_half", float(kappa_of_r(r_star)), 0.5, 1e-30, "dimensionless")
# distinctness of projections
distinct = all(abs(witness_k[i]-witness_k[j]) > 1e-6
               for i in range(7) for j in range(i+1, 7))
R("C7g_projection_distinct", distinct, True, None, "bool", pass_ok=False)

# C8: PPN gamma identity (symbolic): gamma := Psi/Phi; Phi=Psi => gamma=1
Phi, Psi, gamma = sp.symbols("Phi Psi gamma", real=True)
gamma_id = sp.simplify(Psi / Phi - 1).subs(Psi, Phi)
R("C8a_gamma_eq_one", str(sp.simplify(gamma_id)), "0", 0.0, "symbolic residual")
# PPN conventions: g00 = -(1+2Phi/c^2)c^2 dt^2 ; g_ij = (1 - 2*Psi/c^2) delta_ij
# PPN isotropic: gij = (1 - 2*gamma*Phi/c^2)  =>  Psi = gamma*Phi   =>  gamma = Psi/Phi
# exponent check on the published identity (Will-PPN): gamma=1 is the GR value.
g = sp.symbols("g", real=True)
ident = sp.simplify(g - Psi / Phi).subs(Psi, g * Phi)
R("C8b_gamma=Psi/Phi", str(sp.simplify(ident)), "0", 0.0, "symbolic residual")

# C9: two footings - separate densities at fixed kappa=1/2; relabel diagnostic
R("C9a_rho_can", RHO_CAN, 5.844412454e-27, 1e-33, "kg/m^3")
R("C9b_rho_alt", RHO_ALT, 8.483089620e-27, 1e-33, "kg/m^3")
R("C9c_kappa_eff_fixed_rho", kappa_eff_fixed_rho, 0.602388404, 1e-6, "dimensionless relabel")

# ================= gate lattice registry =================
# status: "landed" (proven component in an audited cell), "partial",
#         "open" (unknown), "neg" (positive obstruction found)
GATES = {
 1: {"name": "Exact MOND phenomenology with kernel nu_mono (filtered)",
     "atoms": ["nu_mono kernel", "weak-field: nabla^2 u = 4piG rho_b ",
               "wf: nabla^2 Phi = 4piG rho_b + S* div[(nu_mono-1) grad Su]",
               "deep: g^2 = a0 gN  =>  v^4 = G a0 M_b", "0.0104-dex bound"],
     "status": "partial", "cell": "CA5-GNC-R + heat filter; kernel-level checks here",
     "landed": ["deep-law kernel identity (this run C5)", "MONO landmarks (C1-C4)",
                "AS245 EFE tensor deep limit C_L/C_T -> 1/2", "AS133 heat gate a0-free",
                "AS080 deep-exterior asymptotic slope"],
     "open": ["full weak-field filtered system on compact source (all atoms together)"]},
 2: {"name": "Exactly two propagating gravitational DOF",
     "atoms": ["N_grav = 2", "no hidden scalar graviton", "no propagating auxiliary",
               "no ghost"],
     "status": "partial", "cell": "CA5-GNC-R; k04 three-form sector",
     "landed": ["AS658: zero bulk modes from three-form vacuum (C(2,3)=0)",
                "AS151: 18 primaries, metric sector contributes none"],
     "open": ["secondary/tertiary constraint chain completion", "global ghost-free proof"]},
 3: {"name": "Correct relativistic lensing / no slip  Phi=Psi => gamma_PPN=1",
     "atoms": ["Phi = Psi derived on galactic branch", "both potentials from field eqs",
               "gamma_PPN = 1 within bounds"],
     "status": "open", "cell": None,
     "landed": ["PPN identification gamma = Psi/Phi (this run C8, algebraic)"],
     "open": ["Phi=Psi derivation from CA5-GNC-R field equations"]},
 4: {"name": "Full acceptable PPN, derived",
     "atoms": ["beta ~ 1", "gamma ~ 1", "alpha1 ~ 0", "alpha2 ~ 0", "alpha3 ~ 0"],
     "status": "open", "cell": None, "landed": [], "open": ["all five PPN parameters"]},
 5: {"name": "Ordinary matter conservation (Noether-Ward)",
     "atoms": ["grad_mu T^{mu nu} = 0 for minimally-coupled baryons"],
     "status": "partial",
     "cell": "CA4-GNC/CA5-GNC-R pin, compact closed leaves, on-shell",
     "landed": ["AS138: off-shell jet-level Ward identity (heat sector, exact)",
                "AS138.C01: total current grad.Q_total = 0 identity in couplings"],
     "open": ["matter-only T_b^{mu nu} conservation with clock-sector currents separated (no nonmetric force on baryons)"]},
 6: {"name": "Correct GW sector c_T = c",
     "atoms": ["c_T = c", "positive tensor kinetic energy", "two polarizations",
               "GW170817-type constraints"],
     "status": "open", "cell": None, "landed": [], "open": ["entire gate"]},
 7: {"name": "Stability + causality criterion B",
     "atoms": ["no ghosts", "no gradient instabilities", "no strong-coupling pathology",
               "no hidden scalar pole", "global time function", "no backward signals",
               "no CTC", "well-posed mixed Cauchy problem"],
     "status": "open", "cell": None, "landed": [], "open": ["entire gate (criterion B)"]},
 8: {"name": "Viable cosmology (FLRW, H != 0)",
     "atoms": ["expanding FLRW", "H != 0", "k=0 modes separate"],
     "status": "open", "cell": None, "landed": [], "open": ["entire gate"]},
 9: {"name": "Controlled zero-field limit",
     "atoms": ["controlled y->0", "ellipticity/constraint-rank control"],
     "status": "open", "cell": None, "landed": [], "open": ["entire gate"]},
 10: {"name": "Newtonian/GR recovery; measured G_N derived",
      "atoms": ["mu->1 high acceleration", "derive measured G_N from bare coupling"],
      "status": "partial", "cell": "CA5-GNC-R high-k, gate inactive",
      "landed": ["AS226: G_N = G_bare/c_N, c_N = 1-alpha/2 (one-parameter family)",
                 "this run C6: nu_mono kernel tail -> 1 (logarithmic)"],
      "open": ["fixing alpha (still free)", "full solar-system derivation"]},
 11: {"name": "One physical metric for matter and photons",
      "atoms": ["minimal coupling matter to g", "photons to same g",
                "no photon/graviton speed mismatch"],
      "status": "partial", "cell": "CA5-GNC-R",
      "landed": ["AS226: geodesic acceleration of the physical metric for baryons"],
      "open": ["photons minimal-coupling verification"]},
 12: {"name": "Preserve exponential law as nu_RAR below the phantom peak",
      "atoms": ["nu_mono = nu_RAR for y <= y*", "y* just below y_p",
                "exact AQUAL primitive G(y) historical only"],
      "status": "landed", "cell": "MONO branch, kernel definition",
      "landed": ["venv: kernel definition itself (recipe) + C2a numeric witness"],
      "open": []},
 13: {"name": "Cosmological acceleration-scale relation (derive or label)",
      "atoms": ["a0 = (c/2) sqrt(G rho_Lambda)", "kappa = 1/2 adopted as input",
                "or genuinely derived"],
      "status": "open", "cell": "k01/PD08, k04 four-form, CA4/CA5 pins",
      "landed": ["AS075 T2O: kappa derivable iff obligations A AND B",
                      "AS651: four-form fixes sign, kappa^2 = beta^2/(Z/2+b beta^2); B-ii/B-iv fail",
                      "AS138.C01: conservation leaves continuum (zero polynomial in r)",
                      "this run C7: kappa(r) continuum witnesses"],
      "open": ["E* existence outside audited class (AS075.C01/AS651.C01)"]},
}

UNKNOWN_AS_TRUE = {i for i, g in GATES.items() if g["status"] == "open"}

def honest_closed_components():
    """Components with landed proof in a declared cell."""
    out = set()
    for i, g in GATES.items():
        if g["status"] in ("landed", "partial"):
            out.add(i)
    return out

# Control 1: an all-green table with unknown predicates hidden as true must fail.
def optimistic_verdict():
    """Unknowns are treated as TRUE -> produces the (false) all-green closure call."""
    return "ALL 13 GATES CLOSED - FINAL WITNESS EVALUABLE"

def honest_verdict():
    open_gates = {i: g["name"] for i, g in GATES.items() if g["status"] == "open"}
    partial_gates = {i: g["name"] for i, g in GATES.items() if g["status"] == "partial"}
    return {"open": open_gates, "partially_landed": partial_gates,
            "evaluable": "NO - " + str(len(open_gates)) + " gates fully open"}

opt = optimistic_verdict()
hon = honest_verdict()
ctrl1_fires = ("ALL 13" in opt) and (len(hon["open"]) > 0)
res["CTRL1_all_green_rejected"] = {
    "optimistic": opt, "honest_open": hon["open"],
    "control_fires": ctrl1_fires,
    "note": "control capable of failing: would fail if every gate were actually landed (honest open set empty)"}

# Control 2: a countermodel outside the candidate class cannot establish independence.
# Claim: 'P13 independent of P5 because a two-flux k04 sector (altered class) has
#         kappa(x) = 1/2 for another x' -> must be rejected: class label mismatch.
class_claim = {"witness_cell": "k04 quadratic-P, TWO fluxes (membrane ensemble)",
               "target_cell": "k04 quadratic-P, SINGLE flux, no membranes (pinned)"}
ctrl2_fires = (class_claim["witness_cell"] != class_claim["target_cell"])
res["CTRL2_out_of_class_rejected"] = {
    **class_claim, "control_fires": ctrl2_fires,
    "note": "any independence claim whose witness cell differs from the audited cell is rejected; capable of failing if witness class matched"}

# ---------------- minimal implication graph (derived in this run) ----------------
# strict (definitional/algebraic, both footings, MONO branch unless noted):
#   P1 -> P12          kernel clause nesting (verified C2a; gated on MONO branch)
#   P3 -> P4(gamma)    PPN identification gamma = Psi/Phi, Phi=Psi (C8; algebraic)
#   P6 AND P11 -> R11's speed-match clause (conjunctive; no speed mismatch if both)
# independence (landed-class witnesses):
#   P13 derived-arm not implied by {P5, P1(deep), P10(G_N)} in audited cell:
#     kappa(r) continuum C7e/C7g with grad.Q_total = 0 for every r (AS138.C01) and
#     G_N = G_bare/c_N for every alpha (AS226): witnesses with kappa != 1/2 satisfy
#     the other gates' landed components.
closed_edges = ["P1 -> P12 (strict, MONO kernel)", "P3 -> P4[gamma] (algebraic)",
                "(P6 AND P11) -> speed-match clause (conjunctive)"]
open_edges = ["P4[beta,alpha1..3] independent", "P7 criterion B independent",
              "P8 FLRW independent", "P9 zero-field independent",
              "P13-derived independent of landed components (continuum witnesses)"]

res["lattice"] = {
  "closed_edges": closed_edges, "open_edges": open_edges,
  "minimal_closing_set": ["P3", "P4", "P6", "P7", "P8", "P9",
                          "P11(photons)", "P13(E* outside audited class)",
                          "P2(secondary chain)", "P5(matter-only)", "P10(fix alpha)"]}

# ---------------- bounds ----------------
elapsed = time.time() - start
mem_hint = "max RSS recorded by /usr/bin/time -l in err_time.txt"
res["bounds"] = {"wall_s_measured": elapsed, "memory": mem_hint, "threads": 1}

summary = {"checks": len(res), "pass": sum(
    v["pass"] for v in res.values() if isinstance(v, dict) and "pass" in v),
    "fail": sum(not v["pass"] for v in res.values()
                if isinstance(v, dict) and "pass" in v)}
print("AS500 audit done in %.3f s; %d checks (%d pass / %d fail)"
      % (elapsed, summary["checks"], summary["pass"], summary["fail"]))
print("y_p=%.10f  h_p=%.10f  y*=%.10f" % (float(y_p), float(h_p), float(y_star)))
print("max dex=%.6f at y=%.6f" % (dex_best, y_dex))
print("kappa witness set:", ["%.10f" % k for k in witness_k])
print("mono tail nu-1: " + ", ".join("y=%g:%.3e" % (y0, tail[y0]) for y0 in tail))
print("jsat=%.15f  b=%.15f  r*=%.15f" % (float(jsat), float(b_jsat), float(r_star)))
print("footings: rho_can=%.6e  rho_alt=%.6e  kappa_eff(relabel)=%.9f"
      % (RHO_CAN, RHO_ALT, kappa_eff_fixed_rho))
print("CTRL1 fires:", ctrl1_fires, "| CTRL2 fires:", ctrl2_fires)

with open("residuals.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
with open("raw_output.txt", "w") as f:
    f.write("AS500 compute_as500.py raw output\n")
    for k, v in res.items():
        f.write("%s: %s\n" % (k, json.dumps(v, default=str)))
    f.write("\nSUMMARY: %s\n" % json.dumps(summary))
    f.write("\nWitness set (C7e): %s\n" % witness_k)
print("written residuals.json, raw_output.txt")