"""SCS1 stiffness bracket (reported; criteria 5d2870617c: from the hand closed form only).

With the stiffness on (maximal branch F'' = 1, gamma_L = K Lstar^2/2), eliminating delta P gives the law's longitudinal
response m(k) = m/(1 + gamma_L m k^2) (Sherman-Morrison, checked here with sympy for a general symmetric 3x3 Hessian), and
at mu_K = 0 the coupled dispersion becomes omega^2 = G (1 + gamma_L m k^2 - K m)/m (Lean stiffness_form), which rises with k^2
with the sign of G = n_d + D.P.  Evaluated on the primary grid of route 1 (scs1_wkb.json), both footings.
"""
import os, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))

# Sherman-Morrison along khat for H = W-Hessian (inverse of J''), H + g k^2 khat khat^T
a, b, c, d, e, f, g, k2 = sp.symbols("a b c d e f g k2", real=True)
H = sp.Matrix([[a, b, c], [b, d, e], [c, e, f]])
kh = sp.Matrix([1, 0, 0])
lhs = (kh.T * (H + g * k2 * kh * kh.T).inv() * kh)[0]
m0 = (kh.T * H.inv() * kh)[0]
sm_ok = sp.simplify(lhs - m0 / (1 + g * k2 * m0)) == 0
P_(f"Sherman-Morrison khat.(H + g k^2 khat khat)^-1.khat = m/(1 + g k^2 m), general symmetric H: {'PASS' if sm_ok else 'FAIL'}")

G_, CL, PC = 6.6743e-11, 2.99792458e8, 3.0856775814913673e16
LSTAR_PC = {"canonical": 21.7, "alt": 22.9}
W = json.load(open(os.path.join(HERE, "scs1_wkb.json")))
rows = W["configs"]["primary_mu0"]["rows"]
out = []; neg = 0
for r_ in rows:
    if r_["direction"] == "45deg": continue
    u = r_["u"]; rr = r_["r_m"]
    Km = 1 / (1 + u) ** 2 if r_["direction"] == "radial" else 1 / (1 + u)
    Kg = 4 * math.pi * G_ / CL ** 2
    Gc = Kg * r_["divP"] * rr ** 2                              # code units (length r, K = 1)
    gam = (LSTAR_PC[r_["footing"]] * PC) ** 2 / 2 / rr ** 2     # gamma_L in code units
    k = r_["kr"]
    w2_off = Gc * (1 - Km) / Km
    w2_on = Gc * (1 + gam * Km * k ** 2 - Km) / Km
    out.append(dict(footing=r_["footing"], logM=r_["logM"], point=r_["point"], direction=r_["direction"], kr=k,
                    omega2_code_stiffness_off=w2_off, omega2_code_stiffness_on=w2_on,
                    k_Lstar=k * LSTAR_PC[r_["footing"]] * PC / rr))
    neg += w2_on < 0
lab = "STABLE" if neg == 0 else "UNSTABLE ROWS PRESENT"
P_(f"stiffness bracket (mu_K = 0, spherical point mass): {len(out)} rows; omega^2 < 0 in {neg}; label {lab}")
P_(f"  k Lstar spans {min(o['k_Lstar'] for o in out):.3g} to {max(o['k_Lstar'] for o in out):.3g}; "
   f"omega^2 rises with k^2 above k Lstar ~ 1 with the sign of G = D.P > 0")
res = dict(lane="SCS1", item="stiffness bracket", sherman_morrison_pass=bool(sm_ok), rows=out, n_negative=int(neg), label=lab,
           footer="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs1_stiffness.json"), "w") as fh:
    json.dump(res, fh, indent=1)
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs1_stiffness.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
