#!/usr/bin/env python3
"""
a0 prop sqrt(rho_DE)  =>  MOND's cosmological strength prop sqrt(Omega_DE(z)): MOND is a LATE-TIME effect.

    a0(z)/[c H(z)]  prop  sqrt(rho_DE(z)/rho_tot(z))  =  sqrt(Omega_DE(z)).

So MOND (relative to cosmic dynamics) is full-strength today (Omega_DE=0.69) and ~0 in the matter era.

HONEST STATUS (two overclaims I tested and RETRACTED, 2026-06-06):
  (1) NOT NOVEL.  This is Limbach, Psaltis & Ozel 2008 (arXiv:0809.2790): they wrote a0 = sqrt(8 pi G rho_DE/3),
      derived exactly this sign behavior (a0 constant for w=-1; a0/cH falls into the past => MOND weakens in the
      matter era), and even marginally favored it over the a0=cH coupling. The framework's KERNEL is their 2008
      proposal; its only fresh parts are the DESI-era evaluation and the non-monotonic bump.
  (2) NOT a CMB advantage.  I claimed the framework is "CMB-safe in a way constant-a0 MOND is not" because a0->0
      at recombination. WRONG: at recombination the characteristic acceleration is g ~ 20 a0 (Sanders
      astro-ph/0509532; RelMOND/AeST literature), so constant-a0 MOND is ALREADY deep-Newtonian there. The real
      MOND-CMB problem is the THIRD-PEAK FORCING (a gravitating dark-matter-like component), which is
      a0-INDEPENDENT and inherited unchanged. Driving a0 smaller fixes a non-problem.

What survives: the clean statement that MOND-strength tracks sqrt(Omega_DE) is correct and pedagogically useful
(it is why a0 ~ cH0 today -- because Omega_DE ~ 1 today), but it is LPO2008's, and it confers no CMB benefit.

C. Zimmerman, 2026-06-06. Pure numpy.
"""
import numpy as np
c=2.998e8; G=6.674e-11
OM,OL,OR=0.3137,0.6863,9.2e-5
W0,WA=-0.752,-0.86

def rhoDE_ratio_CPL(z):
    a=1/(1+z); return a**(-3*(1+W0+WA))*np.exp(-3*WA*(1-a))
def a0_ratio(z): return np.sqrt(rhoDE_ratio_CPL(z))
def Omega_DE(z):
    return OL*rhoDE_ratio_CPL(z)/(OM*(1+z)**3+OR*(1+z)**4+OL*rhoDE_ratio_CPL(z))
def mond_rel(z): return np.sqrt(Omega_DE(z)/Omega_DE(0.0))

print("="*86)
print("MOND-strength prop sqrt(Omega_DE(z))  [Limbach-Psaltis-Ozel 2008, arXiv:0809.2790]")
print("="*86)
print(f"\n{'z':>7} | {'a0/a0(0)':>9} | {'Omega_DE(z)':>11} | {'MOND rel.strength sqrt(Om_DE)':>30}")
print("-"*86)
for z in [0,0.41,1,2,3,5,10,1100]:
    print(f"{z:7.2f} | {a0_ratio(z):9.4f} | {Omega_DE(z):11.2e} | {mond_rel(z):30.4f}")
print("\n  => MOND relative strength falls 1.00 (today) -> ~0 (recombination). MOND is a dark-energy-era effect.")
print("     This is WHY a0 ~ cH0 today (Omega_DE~1 now). [LPO2008 -- not novel to this framework.]")

print("\n"+"="*86)
print("IS THERE A CMB ADVANTAGE FROM a0->0 AT RECOMBINATION?  -- NO (overclaim retracted)")
print("="*86)
print("""  Literature: characteristic acceleration at recombination g ~ 20 a0 (Sanders astro-ph/0509532).
  => constant-a0 MOND is ALREADY deep-Newtonian at z* (MOND boost ~ a0/g ~ 5%); it does NOT modify the
     acoustic peaks via a0. Making a0 smaller (framework) changes g/a0 from ~20 to ~infinity -- both Newtonian.
  => The genuine MOND-CMB problem is the THIRD-PEAK FORCING: a baryon-only fluid lacks the non-oscillating
     gravitating component that lifts the 3rd peak. That is a0-INDEPENDENT and the framework inherits it
     UNCHANGED (it still needs the trilemma's dark sector). So 'MOND switches on late' is NOT a CMB win.""")

print("\n"+"="*86)
print("HONEST POSITIONING")
print("="*86)
print("""  - The coupling a0 prop sqrt(rho_DE) and its 'MOND weakens in the matter era' behavior = LPO2008 (2008).
  - The framework adds: the specific value a0 = c^2 sqrt(Lambda/32pi) (coefficient closed/moot), the DESI-w0wa
    evaluation, and the non-monotonic z~0.4 bump. Those are the only fresh pieces; the kernel is prior art.
  - No CMB advantage over constant-a0 MOND. The clean sqrt(Omega_DE) statement is correct but is not new and
    not a win -- record it as pedagogy + a credit to LPO2008, not as a discovery.""")

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    zg=np.logspace(-2,3.1,400); fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(1+zg,[mond_rel(z) for z in zg],"C0-",lw=2.2,label="MOND rel. strength $\\sqrt{\\Omega_{DE}(z)}$ [LPO2008]")
    ax.plot(1+zg,[a0_ratio(z) for z in zg],"C3--",lw=2,label="$a_0(z)/a_0(0)$ (DESI CPL)")
    ax.axvline(1+1090,color="gray",ls=":",lw=1); ax.text(1+1090,0.5,"recomb. (g~20$a_0$: Newtonian)",rotation=90,fontsize=7,ha="right")
    ax.set_xscale("log"); ax.set_xlabel("1+z"); ax.set_ylabel("relative to today"); ax.set_ylim(0,1.15)
    ax.set_title("MOND-strength tracks $\\sqrt{\\Omega_{DE}}$ (LPO2008); no CMB advantage"); ax.legend(fontsize=9); ax.grid(alpha=.25)
    fig.tight_layout(); out="real_research/a0z_switches_on_late.png"; fig.savefig(out,dpi=130); print(f"\n[figure: {out}]")
except Exception as e: print(f"\n[figure skipped: {e}]")
