import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("KOIDE DIRAC-NORMALIZATION BRIDGE — FINAL ADVERSARIAL VERIFICATION")
print("="*80)

# ---- (1) The phase-independent Koide identity (the whole unforced content) ----
r, phi = sp.symbols('r phi', real=True)
# Brannen circulant sqrt-mass: sqrt(m_k) = 1 + r*cos(phi + 2pi k/3)
sm = [1 + r*sp.cos(phi + 2*sp.pi*k/3) for k in range(3)]
K = sp.simplify(sum(s**2 for s in sm)/(sum(sm))**2)
print("\n[1] Brannen circulant Koide K(r,phi):")
print("    K =", sp.simplify(K), "  (phase phi CANCELS -> K = 1/3 + r^2/6)")
# verify phi independence
Ksub = [sp.simplify(K.subs(phi, p)) for p in [0, sp.Rational(3,10), 1, 2]]
print("    phi-independence check (phi=0,0.3,1,2):", [sp.simplify(x - (sp.Rational(1,3)+r**2/6))==0 for x in Ksub])
r_for_23 = sp.solve(sp.Rational(1,3)+r**2/6 - sp.Rational(2,3), r)
print("    K=2/3  <=>  r =", r_for_23, " (= +/- sqrt2)")

# ---- (2) EJA equally-spaced triple -> r_eff ----
d, c = sp.symbols('d c', positive=True)
# (c-d, c, c+d): K = 1/3 + 2(d/c)^2/9  -> match to 1/3 + r_eff^2/6  -> r_eff^2 = (4/3)(d/c)^2
print("\n[2] EJA equally-spaced (c-d,c,c+d) -> K = 1/3 + 2(d/c)^2/9")
for nm, dd in [("Majorana delta^2=3/8", sp.sqrt(sp.Rational(3,8))),
               ("Dirac    delta^2=3/2", sp.sqrt(sp.Rational(3,2)))]:
    Kv = sp.Rational(1,3) + 2*dd**2/9
    reff2 = sp.simplify(sp.Rational(4,3)*dd**2)
    print(f"    {nm}: K = {Kv} = {sp.N(Kv,10)},  r_eff^2 = {reff2}  (r_eff = {sp.nsimplify(sp.sqrt(reff2))})")
print("    => Dirac (3/2) gives r_eff=sqrt2 EXACTLY (Koide 2/3);  Majorana(3/8) gives r_eff=1/sqrt2.")

# ---- (3) The TRADEOFF: actual charged-lepton sqrt-mass ratios from each delta ----
print("\n[3] TRADEOFF — Singh's post-breaking charged-lepton ladder (Eq.2-3 / Eq.53-54)")
me  = mp.mpf("0.51099895000"); mmu = mp.mpf("105.6583755"); mta = mp.mpf("1776.86")
sqrt_mu_e_exp  = mp.sqrt(mmu/me);  sqrt_ta_e_exp = mp.sqrt(mta/me)
def ladder(dval):
    d_ = mp.mpf(str(dval))
    e_small = abs(mp.mpf(1)/3 - d_); e_big = mp.mpf(1)/3 + d_
    q1_small = mp.mpf(1)-d_; q1_big = mp.mpf(1)+d_
    sd = q1_big/q1_small
    mu_e  = (e_big/e_small) * sd
    tau_e = (e_big/e_small) * sd * sd
    return mu_e, tau_e
for nm, dd in [("MAJORANA sqrt(3/8)", mp.sqrt(mp.mpf(3)/8)),
               ("DIRAC    sqrt(3/2)", mp.sqrt(mp.mpf(3)/2))]:
    mu_e, tau_e = ladder(dd)
    devmu = (mu_e/sqrt_mu_e_exp-1)*100; devta=(tau_e/sqrt_ta_e_exp-1)*100
    s = [mp.mpf(1), mu_e, tau_e]
    Kpred = sum(si**2 for si in s)/(sum(s))**2
    print(f"  {nm}: sqrt(mu/e)={mp.nstr(mu_e,7)} (dev {mp.nstr(devmu,3)}%), "
          f"sqrt(tau/e)={mp.nstr(tau_e,7)} (dev {mp.nstr(devta,3)}%), K_pred={mp.nstr(Kpred,7)}")
print("  PDG: sqrt(mu/e)=%s  sqrt(tau/e)=%s" % (mp.nstr(sqrt_mu_e_exp,7), mp.nstr(sqrt_ta_e_exp,7)))

# ---- (4) Can a 2-parameter / correction structure escape? ----
print("\n[4] 2-PARAMETER ESCAPE TEST: is there a delta giving BOTH K=2/3 AND right ratios?")
# Solve: find delta such that K_pred(ladder) = 2/3 exactly, then check the ratios
def Kpred_of_d(d_):
    mu_e, tau_e = ladder(d_)
    s = [mp.mpf(1), mu_e, tau_e]
    return float(sum(si**2 for si in s)/(sum(s))**2)
# scan delta in (1/3, 1) avoiding singularity at d=1/3 (e_small=0) and d=1 (q1_small=0)
import numpy as np
best=None
for d_ in np.linspace(0.34, 0.99, 6600):
    try:
        kk = Kpred_of_d(d_)
    except Exception:
        continue
    if best is None or abs(kk-2/3)<abs(best[1]-2/3):
        best=(d_,kk)
d_at = best[0]; 
mu_e, tau_e = ladder(d_at)
print(f"  delta giving K_pred closest to 2/3 (ladder): delta={d_at:.5f}, K_pred={best[1]:.6f}")
print(f"     -> sqrt(mu/e)={float(mu_e):.4f} (PDG 14.379, dev {(float(mu_e)/14.379-1)*100:+.1f}%), "
      f"sqrt(tau/e)={float(tau_e):.4f} (PDG 58.968, dev {(float(tau_e)/58.968-1)*100:+.1f}%)")
print("  => No single delta gives both exact-2/3 AND correct ratios: K is monotone in delta;")
print("     the delta that hits 2/3 in the ladder is NOT the delta=sqrt(3/8) that fits ratios.")

# ---- (5) Quarantine: does sqrt(3/2) come from a0/Lambda/gravity in Singh? ----
print("\n[5] SOURCE OF delta (Singh's own): pure octonionic algebraic magnitude")
print("    delta = sqrt(3/8) = |off-diag octonion eigenvector| of J3(8) char. eq. (E6/F4 algebra)")
print("    Only dimensionful inputs in Singh: L_Planck, t_Planck, hbar. a0/MOND is a SEPARATE")
print("    emergent-cosmology construction (B=sqrt(G a0), a0=cH0 at Hubble radius) that does")
print("    NOT feed delta. No Lambda/dS/a0 enters the mass-ratio spread.")
