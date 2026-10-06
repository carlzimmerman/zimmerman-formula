"""CFG373: the khronon's instantaneous (lapse) mode as carrier and reaction sink of fluid settling. Criteria: FROZEN_CRITERIA.md (c3bcfdafa).
Analytic / symbolic (sympy) + order-of-magnitude budgets. Run: python3 cfg373_lapse_channel.py ; MUTATE=1 sets alpha_c x 1e12 (G3 must flip; rc 1).
"""
import json, math, os, sys
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

say("CFG373 lapse channel" + ("  (MUTATE: alpha_c x 1e12)" if MUTATE else ""))
say("=" * 78)

# ---------------- C1: mass-shell inverse of P2
a0 = 1.0; aL = a0 / 2
y = np.logspace(-3, 3, 2001)
gN = y * a0; g = np.sqrt(gN**2 + gN * a0)                        # P2: nu = sqrt(1 + 1/y)
gN_back = np.sqrt(g**2 + aL**2) - aL
check("C1 mass-shell inverse g_N = sqrt(g^2 + a_L^2) - a_L reproduces P2 (1e-3 <= y <= 1e3)", np.max(abs(gN_back / gN - 1)) < 1e-12,
      f"max rel {np.max(abs(gN_back/gN-1)):.1e}")

# ---------------- G1: symbolic
say("\nG1 carrier (symbolic)")
G_, M, r, A0 = sp.symbols("G M r a0", positive=True)
gNs = G_ * M / r**2
gs = sp.sqrt(gNs**2 + gNs * A0)                                  # P2 total field (point mass)
AL = A0 / 2
Mtarget = r**2 * (gs + AL - sp.sqrt(gs**2 + AL**2)) / G_          # M_target(<r) from the LOCAL functional of g
x = sp.symbols("x", positive=True)
rM = sp.sqrt(G_ * M / A0)
cfg44 = M * (sp.sqrt(1 + x**2) - 1)                              # CFG44's exact point-mass target, x = r/r_M
# The key identity is a perfect square: g^2 + a_L^2 = (g_N + a_L)^2 for P2. (A first run used sp.simplify on the nested sqrt and
# reported a nonzero 'difference' M(x^2 - sqrt(x^4+4x^2+4) + 2)/2, which is identically 0; sympy did not denest it. Fixed, disclosed.)
ident = sp.expand(gs**2 + AL**2 - (gNs + AL)**2)
Mtarget_exact = r**2 * (gs + AL - (gNs + AL)) / G_
diff1 = sp.simplify(Mtarget_exact.subs(r, x * rM) - cfg44)
num_ok = all(abs(float((Mtarget.subs({G_: 1.3, M: 2.1, A0: 0.7, r: rv}) - cfg44.subs({M: 2.1, x: rv / math.sqrt(1.3 * 2.1 / 0.7)}))) ) < 1e-12 for rv in (0.1, 0.9, 3.0, 27.0))
ok_i = (ident == 0) and (sp.simplify(diff1) == 0) and num_ok
# AQUAL identity: mu g = g_N with mu = g_N/g; div(mu g) = div(g_N) = 4 pi G rho_b (point mass: flux of g_N through a sphere = 4 pi G M)
flux = sp.simplify(4 * sp.pi * r**2 * ((gNs + AL) - AL))       # sqrt(g^2 + a_L^2) = g_N + a_L by the identity above
ok_ii = (ident == 0) and sp.simplify(flux - 4 * sp.pi * G_ * M) == 0
check("G1(i) local target rho_target[g] (via the mass-shell inverse) reproduces CFG44's exact point-mass target M(sqrt(1+x^2)-1)", ok_i, f"identity g^2+a_L^2-(g_N+a_L)^2 = {ident}; difference = {diff1}; numeric check {num_ok}")
check("G1(ii) AQUAL identity: the flux of sqrt(g^2+a_L^2)-a_L equals 4 pi G M_b, i.e. the law, with zero new constants", ok_ii, "symbolic")
say("  Carrier: in the chassis' weak-field limit the lapse gradient c^2 grad ln N is the total acceleration g (G renormalised by the alpha_c term,")
say("  G_N = G/(1 - alpha_c/2); alpha_c <= 3.2e-9 so the factor is 1 to 1.6e-9). The lapse is set by the leaf-elliptic (instantaneous) equation")
say("  (CFG292), so a fluid element reads its target LOCALLY from the time field: the nonlocality CFG60 requires is supplied by gravity's elliptic solve.")
G1 = ok_i and ok_ii

# ---------------- G2: cited
say("\nG2 relaxation toward rho_target: CITED STATUS (CFG245 = this construction): Gate T rate FAIL; T-RAR precision FAIL; Gate C pincer")
say("  (no declared rate); E1 energy FAIL; A0 knife-edge; no ownership. New: CFG369/370 cooling-keyed rate sits in the pincer only in R2/fhot1 cells.")

# ---------------- G3: reaction sink
say("\nG3 reaction sink (MW-like: V = 200 km/s, r = 10 kpc, M_b = 6e10 Msun)")
Gc, c, kpc = 6.674e-11, 2.998e8, 3.0857e19
V, R0, Mb = 2.0e5, 10 * kpc, 6e10 * 1.989e30
a0c = 9.3603e-11; aLc = a0c / 2
gN0 = Gc * Mb / R0**2; g0 = math.sqrt(gN0**2 + gN0 * a0c)
# phantom (target) density at r from the point-mass P2 target: rho = (1/4 pi r^2) dM_c/dr
def Mc(rr):
    gn = Gc * Mb / rr**2; gg = math.sqrt(gn**2 + gn * a0c); return rr**2 * (gg - gn) / Gc
dr = 1e-4 * R0
rho_c = (Mc(R0 + dr) - Mc(R0 - dr)) / (2 * dr) / (4 * math.pi * R0**2)
w = 121.6e3                                                       # CFG245 E2 max drift
HL = 67.4e3 / 3.0857e22 * math.sqrt(0.6847)
GAMMAS = {"CFG370-corrected MW cooling (3.21 H_L)": 3.21 * HL, "CFG245 needed (5.4 H_L)": 5.4 * HL}
ALPHA = (9.62e-14, 3.2e-9); C2 = (7.29e-3, 0.0667)
scale = 1e12 if MUTATE else 1.0
G3 = {}
for lab, Gam in GAMMAS.items():
    f_req = rho_c * Gam * w
    fa = [s * scale * g0**2 / (8 * math.pi * Gc * R0) for s in ALPHA]          # static alpha-channel stress force density
    fc = [s * c**2 * Gam**2 / (8 * math.pi * Gc * R0) for s in C2]              # K^2 channel with K ~ Gamma/c (upper bracket)
    Ra = [f / f_req for f in fa]; Rc = [f / f_req for f in fc]
    G3[lab] = dict(f_req=f_req, R_alpha=Ra, R_c2_bracket=Rc)
    say(f"  {lab}: f_req = {f_req:.2e} N/m^3 | alpha channel R = {Ra[0]:.1e} .. {Ra[1]:.1e} | c_2 / K~Gamma bracket R = {Rc[0]:.1e} .. {Rc[1]:.1e}")
alpha_pass = all(max(v["R_alpha"]) >= 1 for v in G3.values())
c2_pass = all(max(v["R_c2_bracket"]) >= 1 for v in G3.values())
G3v = "PASS" if alpha_pass else ("CONDITIONAL" if c2_pass else "FAIL")
say(f"  G3: {G3v}  (alpha_c channel {'reaches' if alpha_pass else 'misses'} 1; the c_2 channel needs a relaxation-induced congruence expansion K ~ Gamma/c,")
say("   i.e. a local expansion-rate perturbation of order the cooling rate, which is an ASSUMED upper bracket, not derived)")
# dimensional check C2
kg, m_, s_ = sp.symbols("kg m s", positive=True)
dim_f = (kg / m_**3) * (1 / s_) * (m_ / s_)                      # rho Gamma w
dim_a = (m_ / s_**2) ** 2 / ((m_**3 / (kg * s_**2)) * m_)         # g^2/(G r)
check("C2 dimensional check: rho*Gamma*w and g^2/(G r) are both force densities (kg m^-2 s^-2)", sp.simplify(dim_f / dim_a) == 1, f"{sp.simplify(dim_f)}")

# ---------------- G4: energy into the vacuum
say("\nG4 energy into the vacuum")
rho_crit = 3 * (67.4e3 / 3.0857e22) ** 2 / (8 * math.pi * Gc)
rho_L = 0.6847 * rho_crit
G4 = {}
for lab, q, Vt in (("E1 x 19, V 200 km/s", 19 * 0.5, 2e5), ("CFG70 x 318, V 200 km/s", 318 * 0.5, 2e5), ("CFG70 x 318, V 1000 km/s (clusters)", 318 * 0.5, 1e6)):
    frac = q * (0.10 * 0.0493 * rho_crit) * Vt**2 / (rho_L * c**2)
    G4[lab] = frac
    say(f"  {lab}: exchange energy / (rho_Lambda c^2) = {frac:.1e}")
G4v = all(v <= 1e-3 for v in G4.values())
say(f"  G4: {'PASS' if G4v else 'FAIL'} (all <= 1e-3)")
say("\nG5 criterion B: PASS by citation (CFG292: the lapse's leaf-elliptic factor propagates instantaneously within a leaf; cones centred on the leaf normal).")
say("G6 local tests: by citation of the L340 window; the alpha channel's G3 needs alpha_c ~ 1e7-1e11 x the window ceiling (outside it).")
say("Screen Q1: FAIL as expected (a0, hence kappa, is an input; the construction does not fix it).")

if G1 and G3v == "FAIL":
    V_ = "CARRIER FOUND, SINK FAILS"
elif G1 and G3v == "CONDITIONAL" and G4v:
    V_ = "CONDITIONAL"
elif G1 and G3v == "PASS" and G4v:
    V_ = "VIABLE CHANNEL (not a derivation: Q1 fails)"
else:
    V_ = "OTHER"
say(f"\nLANE VERDICT: {V_}")
check("T-MUT main-run marker (MUTATE alpha_c x1e12 must flip G3 to PASS)", (not MUTATE) or G3v == "PASS", G3v)
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": G3v})
n = sum(c_["pass"] for c_ in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG373", "mutate": MUTATE, "verdict": V_, "G1": G1, "G3": G3, "G3v": G3v, "G4": G4, "G4v": G4v, "rho_c_MW_10kpc": rho_c,
           "checks": checks}, open(os.path.join(HERE, f"cfg373_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg373{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
