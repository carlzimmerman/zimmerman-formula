"""p52: which field g, with a whole-sphere Gauss balance g (4 pi r^2) = 4 pi G S over the a0 horizon (r* = c^2/2a0), reproduces G rho r*^2 = c^2 (p53's pi-free shape)?
For each candidate field (natural accelerations at the horizon) and each candidate pi-free source S built from rho, solve and test against the target.
Fields: kappa = c^2/2r (surface gravity = the hole's own Newtonian field GM/r^2); 2 kappa = c^2/r (centripetal acceleration of light circling at r); the vacuum's own field
g_L = (8 pi G/3) rho r (repulsive; carries pi); the deep-MOND field of the hole sqrt(G M a0)/r.
Sources: the hole's mass M = c^2 r/2G; rho r^3 (vacuum energy in a CUBE of side r); rho x ball volume (4 pi/3) r^3 (re-introduces pi).
Run: python3 p52_gauss_flux_candidates.py  |  MUTATE=1: target G rho r^2 = c^2/2 (check U must change)
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
r, rho, G, c = sp.symbols("r rho G c", positive=True)
M = c**2 * r / (2 * G); a0 = c**2 / (2 * r)
target = sp.Rational(1, 2) if MUTATE else 1
fields = {"kappa = c^2/2r": c**2 / (2 * r), "2 kappa = c^2/r (light circling at r)": c**2 / r, "vacuum field (8 pi G/3) rho r": 8 * sp.pi * G * rho * r / 3,
          "deep-MOND field sqrt(G M a0)/r": sp.sqrt(G * M * a0) / r}
sources = {"rho r^3 (cube)": rho * r**3, "rho (4 pi/3) r^3 (ball)": rho * 4 * sp.pi * r**3 / 3, "hole mass M": M}
hits = []
print(f"   {'field':40s} {'source':26s} -> G rho r^2/c^2")
for fn, g in fields.items():
    for sn, S in sources.items():
        eq = sp.Eq(g * 4 * sp.pi * r**2, 4 * sp.pi * G * S)
        if not eq.has(rho):
            print(f"   {fn:40s} {sn:26s} -> identity/contradiction without rho ({sp.simplify(eq)})"); continue
        sol = sp.solve(eq, rho)
        val = sp.simplify(G * sol[0] * r**2 / c**2) if sol else None
        print(f"   {fn:40s} {sn:26s} -> {val}")
        if val is not None and sp.simplify(val - target) == 0: hits.append((fn, sn))
print(f"   combinations that give the target: {hits}")
check("U exactly one combination reproduces the puzzle: the field c^2/r = 2 kappa (light circling at r*) with the pi-free source rho r*^3", hits == [("2 kappa = c^2/r (light circling at r)", "rho r^3 (cube)")])
Om_light2 = (c / r)**2; OmK2 = G * M / r**3
check("K equivalently G rho_L = (c/r*)^2 = Omega_light^2 = 2 Omega_Kepler^2(r*): the vacuum's rate equals light's angular frequency on the a0 horizon",
      sp.simplify(Om_light2 - 2 * OmK2) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
