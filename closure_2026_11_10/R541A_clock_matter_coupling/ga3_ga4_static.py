"""R541A GA3 (equivalence principle, Cassini) and GA4 (the law), static standing clock Q = 1/N.

Point body in a static weak field with the standing clock (tau = t, Q = 1/N, v_K = 0), from ga2's expansion:
  L = (1 - alpha b) M v^2/2 + alpha b M (v - v_K)^2/2 - (1 - alpha b) M Phi   [(i-a), (i-c) at leading order, (ii) with b -> b_T]
  => inertia M, passive and active gravitational mass (1 - alpha b) M,  b = B m_N / M (baryon rest-mass fraction).
(i-b) f = (Q-1)^2: extra potential alpha b M (Phi/c^2)^2 c^2 -> extra acceleration -2 alpha b (Phi/c^2) g.
(ii) beta (Q-1) T: integral of -T over a stationary bound body = M (von Laue) -> b_T = 1 for every body.
Atomic masses: AME2020 values (u), natural abundances IUPAC (atom fractions); typed in from memory, PROVISIONAL.
Output: ga3_ga4_static.out (same folder).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(HERE, "ga3_ga4_static.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")

mp, mn, me = 1.007276466621, 1.00866491595, 5.48579909065e-4
uMeV = 931.49410242
iso = {  # element: (Z, [(A, atomic mass u, atom fraction)])
    "Ti": (22, [(46, 45.95262772, .0825), (47, 46.95175879, .0744), (48, 47.94794198, .7372), (49, 48.94786568, .0541), (50, 49.94478689, .0518)]),
    "Pt": (78, [(190, 189.959930, .00012), (192, 191.961039, .00782), (194, 193.962683, .3286), (195, 194.964794, .3378), (196, 195.964955, .2521), (198, 197.967896, .0736)]),
    "Al": (13, [(27, 26.98153841, 1.0)]),
    "V": (23, [(50, 49.94715601, .0025), (51, 50.94395704, .9975)]),
    "Rh": (45, [(103, 102.905498, 1.0)]),
    "Be": (4, [(9, 9.012183065, 1.0)]),
    "H": (1, [(1, 1.00782503223, 1.0)]),
    "He": (2, [(4, 4.00260325413, 1.0)]),
}
def b_of(el, mode="nucleon"):
    Z, lst = iso[el]
    num = den = 0.0
    for A, M, x in lst:
        Bm = Z*mp + (A - Z)*mn if mode == "nucleon" else A*1.0
        num += x*Bm; den += x*M
    return num/den
def alloy(parts, mode="nucleon"):
    return sum(w*b_of(el, mode) for el, w in parts)

P("# R541A GA3 / GA4: static standing clock")
fe = (26*mp + 30*mn + 26*me - 55.93493633)*uMeV/56
P(f"KA: Fe-56 binding energy per nucleon from the table: {fe:.4f} MeV (textbook 8.790)")
P(f"KA: hydrogen b = m_p/m_H = {b_of('H'):.6f} (textbook 0.999456)")
bodies = {"Ti": [("Ti", 1.0)], "Pt": [("Pt", 1.0)], "TA6V": [("Ti", .90), ("Al", .06), ("V", .04)],
          "PtRh10": [("Pt", .90), ("Rh", .10)], "Be": [("Be", 1.0)]}
for mode in ["nucleon", "A m_u"]:
    bs = {k: alloy(v, mode) for k, v in bodies.items()}
    P(f"b (mode {mode}): " + ", ".join(f"{k} {v:.6f}" for k, v in bs.items()))
bs = {k: alloy(v) for k, v in bodies.items()}
dTiPt = bs["Ti"] - bs["Pt"]; dAll = bs["TA6V"] - bs["PtRh10"]
P(f"Delta b: Ti - Pt = {dTiPt:.4e};  TA6V - PtRh10 = {dAll:.4e};  Be - Ti = {bs['Be'] - bs['Ti']:.4e}")

ETA_BOUND = 7.0e-15; GAM_BOUND = 6.7e-5
PhiE_orbit = 3.986004e14/(6371e3 + 710e3)/2.99792458e8**2
PhiS_1AU = 1.32712440018e20/1.495978707e11/2.99792458e8**2
P(f"Q - 1 = -Phi/c^2 in the standing state: Earth at MICROSCOPE altitude {PhiE_orbit:.3e}; Sun at 1 AU {PhiS_1AU:.3e}")

def eta_lin(alpha, b1, b2):
    a1 = 1 - alpha*b1; a2 = 1 - alpha*b2
    return 2*(a1 - a2)/(a1 + a2)
b_sun = 0.73*b_of("H") + 0.25*b_of("He") + 0.02*bs["Ti"]   # rough solar composition by mass (metals as Ti-like)
for foot, R in [("canonical", 5.410), ("alt", 5.412)]:
    A = R/(1 + R)
    P(f"\n## footing {foot}: alpha (naive GA1 value) = {A:.5f}")
    for lab, al in [("as needed", A), ("MU alpha/2", A/2), ("KA alpha=0", 0.0)]:
        e1 = eta_lin(al, bs["TA6V"], bs["PtRh10"]); e2 = eta_lin(al, bs["Ti"], bs["Pt"])
        e3 = eta_lin(al, bs["Be"], bs["Ti"])
        g1 = 2*al*b_sun/(1 - al*b_sun) if al < 1 else float('inf')
        P(f"  (i-a)/(i-c) {lab}: eta(TA6V,PtRh10) = {e1:.3e}, eta(Ti,Pt) = {e2:.3e} -> x{abs(e2)/ETA_BOUND:.2e} the bound;"
          f" MU swap Pt->Be: eta(Be,Ti) = {e3:.3e}; gamma_eff - 1 = {g1:.3e} -> x{g1/GAM_BOUND:.2e} the Cassini bound")
    gT = 2*A/(1 - A)
    P(f"  (ii) beta = {A:.5f}: b_T = 1 for every stationary body -> eta = 0 (classical); gamma_eff - 1 = 2 beta/(1-beta) = {gT:.3e}"
      f" -> x{gT/GAM_BOUND:.2e} the Cassini bound")
    # (i-b): no alpha produces R; give the bound on alpha and the size at alpha = 1
    Phi_tot = PhiE_orbit + PhiS_1AU
    eta_b = 2*1.0*abs(dTiPt)*Phi_tot
    P(f"  (i-b) at alpha = 1: eta(Ti,Pt) = 2 alpha Delta b |Phi|/c^2 = {eta_b:.3e} (Earth + Sun potential only) -> alpha <= {ETA_BOUND/eta_b:.2e}")
    # GA4: deep-regime amplitude. a = (1-alpha) g_field; g_field = sqrt(G (1-alpha) M a0); a0 from G rho_DE = 3 H0^2 Omega_L/8pi (G-free)
    for lab, al in [("as needed", A), ("MU alpha/2", A/2), ("KA alpha=0", 0.0)]:
        G_lab_ratio = (1 - al)**2
        a0eff = (1 - al)**3/G_lab_ratio
        P(f"  GA4 {lab}: law form kept (same mu); deep-regime v^4 = (1-alpha)^3 G M a0 = {a0eff:.4f} x G_lab M a0 ->"
          f" a0_eff/a0 = {a0eff:.4f}; |a0_eff/a0 - 1| = {abs(a0eff - 1):.3f} vs 0.10 line")
out.close()
