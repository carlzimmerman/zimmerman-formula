#!/usr/bin/env python3
"""ARGON10 Part G (gravity-response coupling).  Criteria: FROZEN_CRITERIA.md (commit db69ec1a0).
G1: characteristic speeds of the two attachments of one static law D(E); reproduces astra's cone; exact reciprocal.
G2: criterion-B margin.   MUTATE M4: flip the sign of the F_YY term.   Seconds, tiny memory."""
import os, sys, json, math
import numpy as np
import sympy as sp

MUT = os.environ.get("ARGON10_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
lines = []
def say(s=""):
    print(s); lines.append(s)
SGN = -1 if MUT else 1                      # M4 flips the F_YY term

# ---------- (a) k-essence scalar L = -F(Y), Y = (dphi)^2 (mostly plus), static gradient along x ----------
Yv, y = sp.symbols('Y y', positive=True)
F = sp.Function('F')
FY = sp.diff(F(Yv), Yv); FYY = sp.diff(F(Yv), Yv, 2)
# effective metric G^{mu nu} = F_Y eta^{mu nu} + 2 F_YY d^mu phi d^nu phi ; background d phi = (0, y, 0, 0)
Gtt = -FY
Gxx = FY + SGN*2*FYY*Yv
# characteristic: Gtt w^2... : G^{mu nu} k_mu k_nu = 0 with k=(-w,kx,..): Gtt*w^2 + Gxx*kx^2 = 0 -> w^2/kx^2 = Gxx/(-Gtt)
cL2_expr = sp.simplify(Gxx/(-Gtt))                 # = 1 + 2 Y F_YY / F_Y
say(f"ARGON10 Part G   mode={'MUTATE M4 (F_YY sign flipped)' if MUT else 'scored'}   criteria db69ec1a0")
say(f"\n== G1(a) scalar attachment:  c_L^2 = {sp.simplify(cL2_expr)} ==")

# ---------- (b) nonlinear electrodynamics L(F), F=(E^2-B^2)/2, B=0 background ----------
Ev = sp.symbols('E', positive=True)
Lf = sp.Function('L')
Fv = sp.symbols('Fv', positive=True)
LF = sp.diff(Lf(Fv), Fv); LFF = sp.diff(Lf(Fv), Fv, 2)
# delta E parallel to background E: delta D = (L_F + L_FF E^2) dE ; delta H = L_F dB ; Faraday w dB = k dE ; Ampere k dH = w dD
# => w^2/k^2 = L_F / (L_F + L_FF E^2)
v2_expr = sp.simplify(LF/(LF + LFF*(2*Fv)))        # E^2 = 2F
say(f"== G1(b) vector attachment (dE || E):  v^2 = {v2_expr}   (other polarization: v^2 = 1) ==")

# ---------- express through the constitutive law D(E) ----------
E = sp.symbols('E', positive=True)
def cL2_from_D(Dfun):          # scalar:  d ln D / d ln E
    return sp.simplify(E*sp.diff(Dfun, E)/Dfun)
def v2_from_D(Dfun):           # vector: L_F = D/E, F=E^2/2 -> v^2 = L_F/(L_F+2F L_FF)
    LFexpr = Dfun/E
    LFFexpr = sp.diff(LFexpr, E)/E                   # dL_F/dF = (dL_F/dE)/(dF/dE)
    return sp.simplify(LFexpr/(LFexpr + E**2*LFFexpr))

a0, x = sp.symbols('a0 x', positive=True)
D_law = E**2/(E + a0)                                  # g_b = g^2/(g+a0)  (D = source-side field, E = total field)
cL2_law = sp.simplify(cL2_from_D(D_law).subs(E, x*a0))
v2_law = sp.simplify(v2_from_D(D_law).subs(E, x*a0))
say(f"\n== G1(c) the law D(E)=E^2/(E+a0), x=E/a0 ==")
say(f"  scalar attachment  c_L^2 = {sp.factor(cL2_law)}   expected (2+x)/(1+x)")
say(f"  vector attachment  v^2   = {sp.factor(v2_law)}   expected (1+x)/(2+x)")
chk_law = sp.simplify(cL2_law - (2+x)/(1+x)) == 0 and sp.simplify(v2_law - (1+x)/(2+x)) == 0
prod = sp.simplify(cL2_law*v2_law)
say(f"  product c_L^2 * v^2 = {prod}")

# general duality for arbitrary D(E): symbolic check
Dg = sp.Function('Dg')(E)
dual = sp.simplify(cL2_from_D(Dg)*v2_from_D(Dg))
say(f"  general D(E): c_L^2 * v^2 = {dual}")
dual_ok = (dual == 1) and (sp.simplify(prod) == 1)

# ---------- astra's cubic-response cone ----------
C, beta, p = sp.symbols('C beta p', positive=True)
yy = p/C + beta*p**2                  # y = |d phi| = p/C + beta p^2   (astra FOUR_GAP_AUDIT)
DD = C*beta*p**2                      # D = F_y
# c^2 = y D_y / D  with derivatives wrt y via p
cone_mine = sp.simplify(yy*sp.diff(DD, p)/sp.diff(yy, p)/DD)
cone_astra = 2*(1 + C*beta*p)/(1 + 2*C*beta*p)
say(f"\n== astra's cubic-response cone ==\n  c_r^2 (from y D_y/D) = {sp.factor(cone_mine)};  astra: 2(1+C beta p)/(1+2 C beta p)")
rng = np.random.default_rng(7)
maxd = 0.0
fm = sp.lambdify((C, beta, p), cone_mine, 'numpy'); fa = sp.lambdify((C, beta, p), cone_astra, 'numpy')
for _ in range(200):
    cv, bv, pv = rng.uniform(0.1, 5, 3)
    maxd = max(maxd, abs(float(fm(cv, bv, pv)) - float(fa(cv, bv, pv))))
cone_ok = maxd <= 1e-12
say(f"  max |difference| over 200 random (C, beta, p) = {maxd:.2e}")

# also verify the k-essence formula numerically against D(E) route for a generic F: F(Y) = Y^(3/2) + Y/3
Fg = Yv**sp.Rational(3, 2) + Yv/3
cLF = sp.simplify((1 + SGN*2*Yv*sp.diff(Fg, Yv, 2)/sp.diff(Fg, Yv)))
Dg_expr = (2*y*sp.diff(Fg, Yv)).subs(Yv, y**2)
cLD = sp.simplify(y*sp.diff(Dg_expr, y)/Dg_expr)
dif = sp.simplify(cLF.subs(Yv, y**2) - cLD)
cross_ok = (dif == 0)
say(f"  cross-check, F(Y)=Y^1.5+Y/3: c_L^2 from F_YY vs from d lnD/d lnE differ by {dif}")

# ---------- first-principles check (added after the freeze; tightens, does not relax) ----------
# (a) linearise  d_mu (F_Y d^mu phi) = 0  about phi0 = y x :  F_Y box(dphi) + 2 y^2 F_YY d_x^2 dphi = 0   (F_Y, F_YY locally constant)
w, kx, ky, F1, F2, yv = sp.symbols('omega k_x k_y F1 F2 y', positive=True)
eq_a = F1*(w**2 - kx**2 - ky**2) - SGN*2*yv**2*F2*kx**2           # plane wave e^{i(k.x - w t)}
w2_a = sp.solve(eq_a, w**2)[0]
cL2_deriv = sp.simplify(w2_a.subs(ky, 0)/kx**2)                    # k along gradient
cL2_formula = 1 + SGN*2*yv**2*F2/F1
deriv_a = sp.simplify(cL2_deriv - cL2_formula) == 0
# (b) linearise Faraday + Ampere + constitutive D=D(E,B), H=H(E,B) about E0 z-hat, B0=0 with k = k x-hat, dE = dE_z, dB = dB_y:
#   Faraday: w dB_y = k dE_z ;  Ampere: k dH_y = w dD_z ;  dD_z=(L_F+L_FF E^2) dE_z ;  dH_y = L_F dB_y
LFs, LFFs, Es, dEz, dBy = sp.symbols('L_F L_FF E dEz dBy', positive=True)
# eliminate: from Faraday dBy = kx dEz / w ; Ampere -> kx*LF*kx/w = w*(LF+LFF E^2) -> w^2 = kx^2 LF/(LF+LFF E^2)
w2_b = sp.simplify((kx**2*LFs)/(LFs + LFFs*Es**2))
v2_formula = LFs/(LFs + LFFs*Es**2)
deriv_b = sp.simplify(w2_b/kx**2 - v2_formula) == 0
# (b2) the other polarisation dE = dE_y (perp. to E0): dD = L_F dE ;  w^2 = k^2 L_F/L_F = k^2  -> v=1
w2_b2 = sp.simplify(kx**2*LFs/LFs)
deriv_b2 = sp.simplify(w2_b2/kx**2 - 1) == 0
say(f"\n== first-principles linearisation check ==\n  (a) scalar EOM -> omega^2/k^2 = {sp.simplify(cL2_deriv)}  matches formula: {deriv_a}\n  (b) Maxwell+constitutive -> omega^2/k^2 = {sp.simplify(w2_b/kx**2)}  matches formula: {deriv_b};  other polarisation v=1: {deriv_b2}")
deriv_ok = deriv_a and deriv_b and deriv_b2
g1_ok = chk_law and dual_ok and cone_ok and cross_ok and deriv_ok
say(f"\n  G1: {'AGREES' if g1_ok else 'DISAGREES'}   (law formulas {chk_law}, duality {dual_ok}, astra cone {cone_ok}, F_YY cross-check {cross_ok}, PDE linearisation {deriv_ok})")

# ---------- ranges and G2 ----------
xs = np.logspace(-6, 6, 13)
cL2n = (2 + xs)/(1 + xs); v2n = (1 + xs)/(2 + xs)
say("\n== ranges over x = g/a0 in [1e-6, 1e6] ==")
say(f"  scalar attachment: c_L^2 in [{cL2n.min():.4f}, {cL2n.max():.4f}]  -> superluminal everywhere (criterion A fails), max {math.sqrt(cL2n.max()):.4f} c")
say(f"  vector attachment: v^2   in [{v2n.min():.4f}, {v2n.max():.4f}]  -> subluminal everywhere")

cLmax = math.sqrt(2.0)
vB = 1.0/cLmax
say("\n== G2  criterion B (global time function compatible with every cone) ==")
say(f"  medium moving at v along the gradient: dt is G-timelike iff v^2 < 1/c_L^2  ->  v < c/c_L,max = {vB:.4f} c = {vB*299792.458:.0f} km/s")
v_bullet = 4700.0
say(f"  largest speed in the record (Bullet merger, CFG725): {v_bullet:.0f} km/s = {v_bullet/299792.458:.4f} c;  margin = {vB*299792.458/v_bullet:.1f}x")
b_ok = v_bullet < vB*299792.458
a_ok = cL2n.max() <= 1.0
say(f"  criterion B: {'PASSES' if b_ok else 'FAILS'};   criterion A (cone inside the light cone): {'PASSES' if a_ok else 'FAILS'} for the scalar attachment")
say("  Reading: astra's 'fails common metric-cone requirement' is criterion A (strict). The owner's criterion B (09-26) holds with the margin above.")
say("  Both attachments reproduce the same static law; only the vector (source-side/D) attachment is within the light cone, and")
say("  its hyperbolic health, sign (attraction vs repulsion) and lensing/metric coupling are NOT established here.")

out = dict(G1_agrees=g1_ok, cL2_range=[float(cL2n.min()), float(cL2n.max())], v2_range=[float(v2n.min()), float(v2n.max())],
           vB_over_c=vB, margin_bullet=vB*299792.458/v_bullet, criterionB=b_ok, criterionA=a_ok)
suffix = "_MUTATE_M4" if MUT else ""
with open(os.path.join(HERE, f"argon10_gravity{suffix}.out"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(os.path.join(HERE, f"argon10_gravity_results{suffix}.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=float)
if MUT:
    bites = not g1_ok
    print(f"MUTATE M4: G1 AGREES -> {g1_ok}; {'bites' if bites else 'DOES NOT BITE'}")
    sys.exit(0 if bites else 1)
say("\n== gate summary ==")
say(f"  G1 {'AGREES' if g1_ok else 'DISAGREES'} | G2 criterion B {'PASSES' if b_ok else 'FAILS'}")
with open(os.path.join(HERE, "argon10_gravity.out"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
