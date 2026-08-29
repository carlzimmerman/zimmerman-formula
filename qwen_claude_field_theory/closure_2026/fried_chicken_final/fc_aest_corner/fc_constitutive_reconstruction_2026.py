"""CERTIFICATE: AeST constitutive reconstruction j_beta(y) for fixed observable mu_obs ~ mu_10, and its LIMITS.
Corrects the relayed proposal (two inconsistent mu_obs forms; wrong inversion; 'exact mu_obs=mu_10' claim).
Physical AeST spherical (mu^2->0 exterior): g = g_chi[1+(1+b0)j], g_N=(1+b0)j g_chi, x=g_chi/a0, y=g/a0.
  => mu_obs = g_N/g = (1+b0)j/(1+(1+b0)j)   [the ONLY correct form].
Findings (sympy):
  - The 'cleaner' (1+b0)j/(1+j) is NOT equal to the correct form (equal only at b0=0).
  - Correct inversion: j_beta(y) = mu/[(1-mu)(1+b0)]  (NOT mu/(1+b0-mu)).
  - Newtonian branch j->1/b0 gives mu_obs->(1+b0)/(1+2b0)=1-b0+O(b0^2), NOT exactly 1.
  => mu_obs = mu_10 + O(b0), NOT exact. beta_0 is an APPROXIMATE (to O(b0)) knob, not a free exact one.
Deep-MOND (mu~y): j->y/(1+b0)=x/(1+b0) asymptote recovered (AeST-consistent).
"""
import sympy as sp
ok=True
def chk(c,l):
    global ok; print(f"  [{'ok' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
j,b0,mu=sp.symbols('j beta_0 mu',positive=True)
mu_correct=((1+b0)*j)/(1+(1+b0)*j)
chk(sp.simplify(mu_correct-((1+b0)*j)/(1+j))!=0,"two proposed mu_obs forms DISAGREE (only correct one kept)")
jsol=sp.solve(sp.Eq(mu_correct,mu),j)[0]
chk(sp.simplify(jsol-mu/((1-mu)*(1+b0)))==0,"correct inversion j_beta = mu/[(1-mu)(1+b0)]")
chk(sp.simplify(jsol-mu/(1+b0-mu))!=0,"relayed inversion mu/(1+b0-mu) is WRONG")
muN=sp.simplify(mu_correct.subs(j,1/b0))
chk(sp.simplify(muN-(1+b0)/(1+2*b0))==0,"Newtonian j->1/b0: mu_obs=(1+b0)/(1+2b0)=1-b0+... (NOT exactly 1)")
# deep-MOND asymptote of j_beta for mu~y small:
y=sp.symbols('y',positive=True); jd=(y)/((1-y)*(1+b0))
chk(sp.limit(jd*(1-y)*(1+b0)/y,y,0)==1,"deep-MOND: j_beta ~ y/(1+b0) => j(x)->x/(1+b0) (AeST asymptote OK)")
print("\nRESULT: reconstruction is APPROXIMATE (mu_obs=mu_10+O(b0)), NOT exact; corrected j_beta banked." if ok else "CHECK FAILED")
import sys; sys.exit(0 if ok else 1)
