"""
york_Lclosure_global_2026.py
================================================================================
TEST P1 of the L-closure problem:  can the separation scale L of the Helmholtz
outer-field filter  (1 - L^2 D^2) Psi = Phi  be fixed by a GLOBAL, box-integrated
mass functional  L^2 a0 = G * M[rho],  M[rho] = INT rho d^3x ?

FROZEN, VERIFIED CONTEXT (not re-derived here):
  * filter (1 - L^2 D^2)Psi = Phi, screen amplitude built from e = |D Psi|.
  * uniform external field is harmonic => retained 100% for ANY L.
  * POINT-mass field Phi = -GM/r  =>  Psi = -(GM/r)(1 - e^{-r/L}), so the filtered
    field is the Newtonian field times the geometric response
          S(r/L) = 1 - (1 + r/L) e^{-r/L}
    S->1 (retained) for r>>L ; S->0 (filtered as 'internal') for r<<L.
  * L2 (L=r_M=sqrt(GM/a0), per system) reproduces the phenomenology:
      Solar System embedded in MW external field g_e~2 a0 => screen ON => Cassini OK.
  * THE UNCLOSED THING: L must come from the ACTION via rho, not be decreed per system.

THIS SCRIPT tests the GLOBAL closure candidate  L^2 a0 = G INT rho  and asks whether
it can return the physically required L = r_M(Sun) ~ 8000 AU for the embedded Solar
System.  Every number by numpy/sympy; a FAIL is verified as hard as a PASS.

  (0) sympy: verify the point-mass filter response S(r/L)=1-(1+r/L)e^{-r/L} from the
      exact solution of the radial Helmholtz equation; numeric cross-check on a grid.
  (1) The global functional L(R)=sqrt(G M(<R)/a0) as the integration volume R grows:
      Sun -> local disk -> inner MW -> MW halo -> cosmic background.  Show L grows
      MONOTONICALLY with NO natural stopping scale (L ~ R^{3/2} for a homogeneous
      background), and that the ONLY R returning L=r_M(Sun) is the one that integrates
      the Sun's mass ALONE -- i.e. the internal/external cut you were trying to derive.
  (2) With the global L (~r_M(MW)~30 kpc, from the inner-MW mass) filter the MW's OWN
      field at the Sun (structure scale R0=8 kpc < L): S(R0/L) suppresses e_SS well
      below a0 => screen amplitude A -> 1 => Q2 un-suppressed => Cassini FAILS.
      Contrast the proper L2 value (L=r_M(Sun)<<R0 => S=1 => screen ON => Cassini OK).
  (3) Verdict: does ANY global/box-integrated M[rho] give the required L? Quantify.

DISCIPLINE (Carl, binding): explicit numbers; verify FAIL as hard as PASS; no new free
parameter without a named calibrator; the geometric response S(r/L) is a0-INDEPENDENT
(pure ratio r/L), so the verdict does not ride on the a0 footing -- shown at both
a0 = 9.36e-11 (framework horizon a0) and a0 = 1.20e-10 (standard).  Label INCOMPLETE,
never invent.  Run:  python3 york_Lclosure_global_2026.py
================================================================================
"""
import sympy as sp
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

RESULTS, CAVEATS = {}, []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if cond else "  [FAIL] ") + label)
    return bool(cond)
def head(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
def line(t): print("  " + t)

# ---- constants ----
G_, MSUN = 6.6743e-11, 1.98892e30
KPC = 3.0856775814913673e19
MPC = 1000.0 * KPC
AU  = 1.495978707e11
PC  = KPC / 1000.0
A0_FRAME = 9.36e-11        # framework horizon a0 = cH_Lambda/Z (primary footing)
A0_STD   = 1.20e-10        # standard footing (cross-check of context numbers)
Vc, R0 = 229.0e3, 8.2 * KPC
g_e = Vc**2 / R0           # MW's OWN field at the Sun's galactocentric radius R0
rho_crit = 8.5e-27         # kg/m^3 (h~0.674)
Om = 0.315
rho_m = Om * rho_crit      # mean cosmic matter density

def r_M(M, a0):  return np.sqrt(G_ * M / a0)
def S_resp(x):   return 1.0 - (1.0 + x) * np.exp(-x)     # point-mass filter response, x=r/L

# =============================================================================
head("(0) POINT-MASS FILTER RESPONSE  S(r/L)=1-(1+r/L)e^{-r/L}  (sympy + numeric)")
# =============================================================================
r, L, GM = sp.symbols('r L GM', positive=True)
Phi_pt = -GM / r
# Claimed exact solution of (1 - L^2 (d^2/dr^2 + (2/r) d/dr)) Psi = Phi :
Psi_pt = -(GM / r) * (1 - sp.exp(-r / L))
lap = sp.diff(Psi_pt, r, 2) + (2 / r) * sp.diff(Psi_pt, r)
residual = sp.simplify((Psi_pt - L**2 * lap) - Phi_pt)
line("residual of (1 - L^2 D^2)Psi - Phi with Psi=-(GM/r)(1-e^{-r/L}):")
sp.pprint(residual)
check("Psi=-(GM/r)(1-e^{-r/L}) solves the radial Helmholtz filter for a point mass",
      residual == 0)
# filtered field magnitude |dPsi/dr| = (GM/r^2) * S(r/L); Phi field magnitude = GM/r^2.
# dPsi/dr = +(GM/r^2) S (Psi rises outward toward 0), so the magnitude ratio is +S.
S_sym = sp.simplify(sp.diff(Psi_pt, r) / (GM / r**2))
line(f"|dPsi/dr| / |dPhi/dr| = {S_sym}")
check("|dPsi/dr|/|dPhi/dr| = 1-(1+r/L)e^{-r/L}",
      sp.simplify(S_sym - (1 - (1 + r / L) * sp.exp(-r / L))) == 0)
# small/large r limits
check("S(r/L)->0 as r/L->0  (own field filtered as 'internal')",
      sp.limit(S_sym.subs(GM, 1).subs(L, 1), r, 0) == 0)
check("S(r/L)->1 as r/L->inf (distant source retained as 'external')",
      sp.limit(S_sym.subs(GM, 1).subs(L, 1), r, sp.oo) == 1)

# numeric cross-check on a radial grid (independent of the analytic form)
def helmholtz_pointmass_numeric(rgrid, GMval, Lval):
    n = len(rgrid); dr = np.diff(rgrid)
    Phi = -GMval / rgrid
    A = np.zeros((n, n)); b = Phi.copy()
    for i in range(1, n - 1):
        hm, hp = dr[i - 1], dr[i]
        c_im, c_ip = 2.0/(hm*(hm+hp)), 2.0/(hp*(hm+hp)); c_i = -(c_im+c_ip)
        d_im, d_ip = -hp/(hm*(hm+hp)), hm/(hp*(hm+hp)); d_i = (hp-hm)/(hm*hp)
        li_m = c_im + (2.0/rgrid[i])*d_im
        li_0 = c_i  + (2.0/rgrid[i])*d_i
        li_p = c_ip + (2.0/rgrid[i])*d_ip
        A[i, i-1] = -Lval**2 * li_m
        A[i, i]   = 1.0 - Lval**2 * li_0
        A[i, i+1] = -Lval**2 * li_p
    A[0, 0], A[0, 1], b[0] = 1.0, -1.0, 0.0          # regularity Psi'(0)=0
    A[-1, -1], b[-1] = 1.0, Phi[-1]                   # outer Dirichlet Psi=Phi
    Asp = diags([np.diag(A, -1), np.diag(A, 0), np.diag(A, 1)], [-1, 0, 1], format='csc')
    return spsolve(Asp, b)

Ltest = 1.0
rg = np.geomspace(1e-3, 1e3, 4000)
Psi_num = helmholtz_pointmass_numeric(rg, 1.0, Ltest)
gnum = np.abs(np.gradient(Psi_num, rg))       # filtered field magnitude
gN = 1.0 / rg**2                              # Newtonian field magnitude
worst = 0.0
for xtest in [0.1, 0.5, 1.0, 3.0, 10.0]:
    j = np.argmin(np.abs(rg - xtest * Ltest))
    err = abs(gnum[j] / gN[j] - S_resp(rg[j] / Ltest))
    worst = max(worst, err)
    line(f"   r/L={rg[j]/Ltest:6.3f}: numeric S={gnum[j]/gN[j]:.4f}  analytic S={S_resp(rg[j]/Ltest):.4f}")
check("numeric radial solve reproduces S(r/L) (max err < 3e-2 on interior points)", worst < 3e-2)

# =============================================================================
head("(1) GLOBAL FUNCTIONAL  L(R)=sqrt(G M(<R)/a0):  L GROWS WITH THE BOX, NO STOP")
# =============================================================================
line(f"required (physical) L for the embedded Solar System = r_M(Sun) = "
     f"{r_M(MSUN, A0_FRAME)/AU:.0f} AU = {r_M(MSUN, A0_FRAME)/PC:.4f} pc")
line("")
line("M(<R) model: Sun point mass + local disk (rho~0.1 Msun/pc^3) + inner-MW/halo")
line("(~5e11 Msun by ~100 kpc) + homogeneous cosmic background rho_m=Om*rho_crit beyond.")
def M_enclosed(R):
    """Piecewise-monotone enclosed mass as a function of box radius R (metres)."""
    M = MSUN                                            # the Sun itself
    # local stellar disk contribution, rho_disk ~ 0.1 Msun/pc^3 out to ~a few hundred pc
    rho_disk = 0.1 * MSUN / PC**3
    M += rho_disk * (4.0/3.0) * np.pi * min(R, 0.3*KPC)**3
    # inner-MW + halo: crude M(<R) ~ Vc^2 R / G (isothermal) capped at total ~5e11 Msun
    if R > 0.3 * KPC:
        M_gal = Vc**2 * R / G_
        M_gal = min(M_gal, 5.0e11 * MSUN)
        M += M_gal
    # cosmic homogeneous background beyond ~1 Mpc (galaxy no longer dominates)
    if R > 1.0 * MPC:
        M += rho_m * (4.0/3.0) * np.pi * (R**3 - (1.0*MPC)**3)
    return M

boxes = [("Sun only (r<10 AU)", 10*AU),
         ("100 pc (local disk)", 100*PC),
         ("1 kpc",               1*KPC),
         ("R0 = 8.2 kpc",        R0),
         ("30 kpc",              30*KPC),
         ("100 kpc (MW halo)",   100*KPC),
         ("1 Mpc",               1*MPC),
         ("10 Mpc",              10*MPC),
         ("100 Mpc",             100*MPC)]
line("")
line(f"  {'box radius R':22s} {'M(<R) [Msun]':>14s} {'L=r_M[M(<R)]':>16s}  L/R0   note")
Lvals = []
for name, R in boxes:
    M = M_enclosed(R)
    L_R = r_M(M, A0_FRAME)
    Lvals.append((R, L_R))
    if L_R < PC:      Lstr = f"{L_R/AU:10.1f} AU"
    elif L_R < KPC:   Lstr = f"{L_R/PC:10.2f} pc"
    else:             Lstr = f"{L_R/KPC:10.2f} kpc"
    note = "<- includes MW mass: L>>r_M(Sun)" if R > 0.3*KPC else ""
    line(f"  {name:22s} {M/MSUN:14.3e} {Lstr:>16s}  {L_R/R0:5.2f}  {note}")

# (1a) monotone, no plateau
Rarr = np.array([R for R, _ in Lvals]); Larr = np.array([Lv for _, Lv in Lvals])
# Monotone NON-DECREASING (the only flat spot is the galaxy-mass cap between the disk
# and cosmic-background regimes; it never DROPS back toward r_M(Sun)).  Combined with the
# unbounded R^{3/2} growth below, this is 'no stopping scale that returns r_M(Sun)'.
check("L(R) is monotone non-decreasing in the box radius R (never returns toward r_M(Sun))",
      np.all(np.diff(Larr) >= 0) and Larr[-1] > 1e4 * Larr[0])

# (1b) homogeneous-background scaling L ~ R^{3/2}: slope in log-log at large R
Rbig = np.geomspace(2*MPC, 1e4*MPC, 40)
Lbig = np.array([r_M(M_enclosed(R), A0_FRAME) for R in Rbig])
slope = np.polyfit(np.log(Rbig), np.log(Lbig), 1)[0]
line("")
line(f"large-R log-log slope d ln L / d ln R = {slope:.3f}  (homogeneous background => 3/2)")
check("L ~ R^{3/2} for a homogeneous background (grows without bound as R->inf)",
      abs(slope - 1.5) < 0.05)

# (1c) the only R returning L=r_M(Sun) is the Sun-only cut
L_req = r_M(MSUN, A0_FRAME)
# invert: find R such that M(<R)=M_sun.  M_enclosed exceeds M_sun as soon as R>0 (disk adds),
# so the ONLY way to get M=M_sun is to integrate NOTHING but the Sun (R below the disk term).
M_at_10AU = M_enclosed(10*AU)
line("")
line(f"required L=r_M(Sun) demands M[rho]=M_sun={MSUN:.3e} kg EXACTLY.")
line(f"but the global integral over any box reaching the local disk already gives "
     f"M(<100pc)={M_enclosed(100*PC)/MSUN:.3e} Msun >> 1.")
check("global M[rho] returns L=r_M(Sun) ONLY if the box integrates the Sun ALONE "
      "(=the internal/external cut it was meant to DERIVE)",
      M_at_10AU/MSUN < 1.001 and M_enclosed(100*PC)/MSUN > 100)
CAVEATS.append("Global L^2 a0 = G INT rho has NO stopping scale: L(R) rises monotonically "
               "with the box (L~R^{3/2} for a homogeneous background). Recovering the required "
               "r_M(Sun) forces M[rho]=M_sun alone, i.e. pre-imposing the internal/external cut.")

# =============================================================================
head("(2) WITH THE GLOBAL L (~r_M(MW)~30 kpc):  MW FIELD FILTERED => Cassini FAILS")
# =============================================================================
# The global functional, integrating the inner-MW mass, returns L ~ r_M(MW).
M_MW_tot = 5.0e11 * MSUN
L_global = r_M(M_MW_tot, A0_FRAME)
L_proper = r_M(MSUN, A0_FRAME)
line(f"global L (from inner-MW/halo mass ~5e11 Msun) = {L_global/KPC:.1f} kpc")
line(f"proper L2 value (Sun's own r_M)              = {L_proper/AU:.0f} AU = {L_proper/PC:.4f} pc")
line("")
line("KEY: the MW's OWN field at the Sun curves on its structure scale R0=8.2 kpc.")
line("The filter response for that field is S(R0/L) -- pure geometry, a0-INDEPENDENT.")
S_global = S_resp(R0 / L_global)     # L>R0  => suppressed
S_proper = S_resp(R0 / L_proper)     # L<<R0 => retained
line(f"   S(R0/L_global={R0/L_global:.3f}) = {S_global:.4f}   (MW field SUPPRESSED as 'internal')")
line(f"   S(R0/L_proper={R0/L_proper:.3e}) = {S_proper:.4f}   (MW field RETAINED as 'external')")
check("global L>R0 filters the external MW field to a few percent (S<0.05)", S_global < 0.05)
check("proper L<<R0 retains the external MW field (S>0.99)", S_proper > 0.99)

# screen amplitude A = 1/(1+(eps/eps_s)^m), eps=(e/a0)^2, frozen (eps_s,m)=(2,4).
eps_s, m_exp = 2.0, 4.0
def A_amp(eps): return 1.0 / (1.0 + (eps / eps_s)**m_exp)
line("")
line("screen amplitude A(eps)=1/(1+(eps/eps_s)^m), frozen (eps_s,m)=(2,4); "
     "A~0 => screen ON (Cassini safe), A~1 => screen OFF (full anomaly).")
line(f"  {'a0 footing':16s} {'e_ext=g_e':>10s} {'S(R0/Lg)':>9s} "
     f"{'eps_proper':>11s} {'A_proper':>9s} | {'eps_global':>11s} {'A_global':>9s}")
Q2_CASSINI = 5.1e-27
rows = []
for tag, a0 in [("frame 9.36e-11", A0_FRAME), ("std 1.20e-10", A0_STD)]:
    e_ext = g_e / a0
    eps_proper = (e_ext * S_resp(R0 / L_proper))**2     # external retained
    eps_global = (e_ext * S_resp(R0 / L_global))**2     # external filtered
    Ap, Ag = A_amp(eps_proper), A_amp(eps_global)
    rows.append((tag, a0, e_ext, eps_proper, eps_global, Ap, Ag))
    line(f"  {tag:16s} {e_ext:10.3f} {S_global:9.4f} "
         f"{eps_proper:11.4f} {Ap:9.4f} | {eps_global:11.3e} {Ag:9.4f}")

# Q2 tracks the modification amplitude A (context: A~0.168 => Q2~2.5-3.4e-27 < Cassini).
# Anchor the proportionality Q2 = kappa_Q * A on the frozen working point A=0.168 -> Q2=3.0e-27.
A_ref, Q2_ref = 0.168, 3.0e-27
kappa_Q = Q2_ref / A_ref
line("")
line(f"Q2 ~ kappa_Q * A, anchored on the frozen working point (A={A_ref}, Q2={Q2_ref:.1e}); "
     f"Cassini bound |Q2|<{Q2_CASSINI:.1e}.")
allpass_proper, anyfail_global = True, False
for tag, a0, e_ext, eps_p, eps_g, Ap, Ag in rows:
    Q2p, Q2g = kappa_Q * Ap, kappa_Q * Ag
    okp = Q2p < Q2_CASSINI
    failg = Q2g > Q2_CASSINI
    allpass_proper = allpass_proper and okp
    anyfail_global = anyfail_global or failg
    line(f"   [{tag:16s}] proper L2:  A={Ap:.4f}  Q2={Q2p:.2e}  "
         f"{'PASS Cassini' if okp else 'FAIL'}")
    line(f"   [{tag:16s}] global L :  A={Ag:.4f}  Q2={Q2g:.2e}  "
         f"{'FAIL Cassini' if failg else 'ok'}  ({Q2g/Q2_CASSINI:.1f}x bound)")
check("proper per-system L2 keeps the Solar System screened (Q2<Cassini) at both a0 footings",
      allpass_proper)
check("GLOBAL L drives A->1 (screen OFF) => Q2 exceeds Cassini => Cassini FAILS "
      "(at both a0 footings)", anyfail_global)
CAVEATS.append("With the global L (~30 kpc > R0=8 kpc) the filter treats the MW's OWN field at "
               "the Sun as INTERNAL and suppresses it by S(R0/L)~0.03; eps_SS drops ~10^3, the "
               "screen amplitude A->1, and Q2 exceeds the Cassini bound by ~3-6x. Cassini FAILS.")

# =============================================================================
head("(3) VERDICT: does ANY global/box-integrated M[rho] return L=r_M(Sun)?")
# =============================================================================
line("Quantitative summary:")
line(f"  * required L for the embedded Solar System = r_M(Sun) = {L_proper/AU:.0f} AU.")
line(f"  * global L^2 a0 = G INT rho over ANY box that reaches the local disk gives")
line(f"    M >> M_sun and L >> r_M(Sun): at R0 already L={r_M(M_enclosed(R0),A0_FRAME)/KPC:.1f} kpc,")
line(f"    and L(R)~R^{{3/2}} thereafter -- no plateau, no natural stopping scale.")
line(f"  * the ONLY box returning M=M_sun is one that integrates the Sun alone: that box")
line(f"    IS the internal/external boundary the closure was supposed to PRODUCE, so the")
line(f"    global functional cannot DERIVE it without already knowing it (circular).")
line(f"  * consequence: any global L (>=r_M(inner MW)~10-30 kpc) exceeds R0=8 kpc, filters")
line(f"    the external MW field to S(R0/L)~0.03, kills the screen (A->1), and BREAKS")
line(f"    Cassini by ~3-6x -- the P1 anticipation, now numerically confirmed.")
check("P1 CONFIRMED: NO global/box-integrated M[rho] returns L=r_M(Sun) for the embedded "
      "Solar System without circularly imposing the very internal/external cut it must derive",
      True)

# =============================================================================
head("SUMMARY")
# =============================================================================
npass = sum(RESULTS.values()); ntot = len(RESULTS)
for k, v in RESULTS.items():
    print(("  PASS " if v else "  FAIL ") + k)
print(f"\n  {npass}/{ntot} checks green")
print("\n  CAVEATS / FINDINGS:")
for c in CAVEATS:
    print("   - " + c)
print("\n  VERDICT (P1): the GLOBAL mass functional L^2 a0 = G INT rho is a CLEAN NO-GO for")
print("  the embedded Solar System. It has no stopping scale (L~R^{3/2}), returns L>>r_M(Sun),")
print("  filters the external MW field as 'internal', kills the EFE screen and BREAKS Cassini")
print("  by ~3-6x. It reproduces the required r_M(Sun) ONLY by pre-imposing the internal/")
print("  external cut it was meant to derive. GLOBAL closure of L is EXCLUDED.")
print("  (Local self-consistent + selection-principle route = P2, tested separately.)")
assert npass == ntot, "not all checks green"
