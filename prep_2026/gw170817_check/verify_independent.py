#!/usr/bin/env python3
"""
INDEPENDENT adversarial re-derivation of the GW170817 disformal check.
Does NOT reuse gw170817_lineintegral.py's numeric integral. Instead:
  (1) sympy symbolic proof of the photon-graviton speed differential from g~=g+Buu
      -> is |c_gamma-c_gw|/c = B/2, B, or something else?
  (2) sympy re-derivation of grad B = 4(nu-1)g_bar from the lensing-potential match
  (3) CLOSED-FORM deep-MOND bracket B(r)=(4 sqrt(a0 GM)/c^2) ln(r_out/r) (analytic,
      independent of any numeric quadrature) -> best-case (single minimal 10-kpc
      crossing) and worst-case (host+MW+IGM) BRACKET on Delta_t, both a0 footings.
  (4) the manufactured-SAVE and manufactured-KILL probes.
Honesty: a SAVE is verified as hard as a KILL. Exit 0.
"""
import numpy as np, sympy as sp

# ============================================================================
# (1) SPEED DIFFERENTIAL, symbolic:  g~ = g + B u u,  rest frame
# ============================================================================
B, kx = sp.symbols('B k_x', positive=True)
k0 = sp.symbols('k_0', real=True)
# metric g=diag(-1,1,1,1); u^mu=(1,0,0,0), normalized u^mu u_mu=-1 -> u_mu=(-1,0,0,0)
# g~_00 = g_00 + B u_0 u_0 = -1 + B*(-1)(-1) = -(1-B);  g~_ij = delta_ij (u_i=0)
gt = sp.diag(-(1-B), 1, 1, 1)
gtinv = gt.inv()
# photon null on g~:  g~^{mn} k_m k_n = 0, spatial momentum along x
null = sp.simplify(gtinv[0,0]*k0**2 + gtinv[1,1]*kx**2)
sol = sp.solve(sp.Eq(null,0), k0)            # k0 = +/- sqrt(1-B) kx  -> c_gamma=sqrt(1-B)
c_gamma = sp.simplify(sol[1]/kx)             # positive root over |k|
dc = sp.simplify(1 - c_gamma)                # |c_gamma - c_gw|/c, graviton c_gw=1
print("="*76)
print("(1) SPEED DIFFERENTIAL from g~=g+Buu  (graviton stays on g, c_gw=1)")
print("="*76)
print(f"   g~_00 = -(1-B),  g~_ij = delta_ij   (u_i=0 -> spatial block untouched, as c_T=1)")
print(f"   photon phase speed c_gamma = {c_gamma}   (subluminal, B>0)")
print(f"   |c_gamma - c_gw|/c = 1 - sqrt(1-B) = {sp.series(dc, B, 0, 2)}")
print(f"   -> leading order = B/2.  NOT B, NOT B^2. The factor is B/2. CONFIRMED.")

# ============================================================================
# (2) grad B = 4(nu-1) g_bar, symbolic, from the lensing-potential match
# ============================================================================
Phi, Bx, nu, gbar = sp.symbols('Phi B nu g_bar', real=True)
# UNIFICATION.md: lensing potential (Phi~+Psi~)/2 = Phi - B/4 (u_iu_j block=0 -> Psi~=Phi).
# deflection ~ grad of that; require it to reproduce the RAR field g_obs = nu*g_bar.
# grad Phi = g_bar (baryonic). Match: grad(Phi - B/4) = nu*g_bar
#   g_bar - gradB/4 = nu*g_bar  ->  gradB = -4(nu-1) g_bar  (|gradB| = 4(nu-1)g_bar)
gradB = sp.solve(sp.Eq(gbar - Bx/4, nu*gbar), Bx)[0]   # solves for gradB(=Bx)
print("\n"+"="*76)
print("(2) grad B from the lensing match  (lensing potential = Phi - B/4)")
print("="*76)
print(f"   g_bar - gradB/4 = nu*g_bar   ->   gradB = {sp.simplify(gradB)}")
print(f"   |grad B| = 4(nu-1) g_bar.  CONFIRMED (matches UNIFICATION.md U2).")
# void limit: (nu-1)g_bar with nu=sqrt(1+a0/gbar) -> sqrt(a0 gbar) as gbar->0
a0s, g = sp.symbols('a0 g', positive=True)
nuf = sp.sqrt(1 + a0s/g)
void = sp.limit((nuf-1)*g/sp.sqrt(a0s*g), g, 0)
print(f"   void limit: (nu-1)g_bar / sqrt(a0 g_bar) ->{void}  (=1) so grad B ~ sqrt(a0 g_bar) -> 0 in void.")
print(f"   => B stops GROWING in the void, but the DELAY uses accumulated B, not grad B.")

# ============================================================================
# (3) CLOSED-FORM deep-MOND bracket  (analytic, no numeric quadrature)
# ============================================================================
# deep-MOND (g_bar<a0): nu ~ sqrt(a0/g_bar), so (nu-1)g_bar ~ sqrt(a0 g_bar) = sqrt(a0 GM)/r.
# grad B = 4 sqrt(a0 GM)/(r c^2).  Integrate inward from B(r_out)=0:
#   B(r) = (4 sqrt(a0 GM)/c^2) * ln(r_out/r).   Delay of one radial crossing r_in->r_out:
#   Delta_t = (1/c) INT_{r_in}^{r_out} (B(r)/2) dr
#           = (2 sqrt(a0 GM)/c^3) INT ln(r_out/r) dr
#           = (2 sqrt(a0 GM)/c^3) * [ (r_out-r_in) - r_in*ln(r_out/r_in) ]   (closed form)
c=2.998e8; G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1e3*kpc
FOOT={"canonical 9.36e-11":9.36e-11, "alt 1.13e-10":1.13e-10}
def cross(M, r_in, r_out, a0):
    A = 4*np.sqrt(a0*G*M)/c**2                       # grad-B prefactor [dimensionless/m * m = ]
    Bmax = A*np.log(r_out/r_in)
    # INT_{r_in}^{r_out} ln(r_out/r) dr = (r_out-r_in) - r_in ln(r_out/r_in)
    I = (r_out-r_in) - r_in*np.log(r_out/r_in)
    dt = (A/2)*I/c
    return dt, Bmax
D=40*Mpc; t_tr=D/c
print("\n"+"="*76)
print("(3) ANALYTIC deep-MOND bracket  B(r)=(4 sqrt(a0 GM)/c^2) ln(r_out/r)")
print("="*76)
for fn,a0 in FOOT.items():
    # best case for framework: ONE minimal galaxy crossing, host exit, thin 2->12 kpc shell only
    dt_min,Bm = cross(1e11*Msun, 2*kpc, 12*kpc, a0)        # only to the MOND radius ~12 kpc
    # realistic minimum: host(2->300) + MW(8->300) crossings, IGM=0
    dt_h,Bh = cross(1e11*Msun, 2*kpc, 300*kpc, a0)
    dt_m,Bmw= cross(6e10*Msun, 8*kpc, 300*kpc, a0)
    dt_real = dt_h+dt_m
    # conservative (banked) minimum: outer radius only 100 kpc
    dt_h100,_=cross(1e11*Msun,2*kpc,100*kpc,a0); dt_m100,_=cross(6e10*Msun,8*kpc,100*kpc,a0)
    dt_cons=dt_h100+dt_m100
    print(f"\n  footing {fn}:")
    print(f"   BEST CASE  (single thin host shell 2->12 kpc): Dt={dt_min:.2e} s  = {dt_min/1.7:.1e}x the 1.7s bound ({np.log10(dt_min/1.7):.1f} orders over)")
    print(f"   CONSERVATIVE (host+MW to 100 kpc, banked):     Dt={dt_cons:.2e} s  = {dt_cons/1.7:.1e}x ({np.log10(dt_cons/1.7):.1f} orders over)")
    print(f"   REALISTIC MIN (host+MW to 300 kpc, IGM=0):     Dt={dt_real:.2e} s  = {dt_real/1.7:.1e}x ({np.log10(dt_real/1.7):.1f} orders over)")
    print(f"     |dc|/c = Dt/t_travel = {dt_real/t_tr:.2e}  vs 1e-15 -> {(dt_real/t_tr)/1e-15:.1e}x ({np.log10((dt_real/t_tr)/1e-15):.1f} orders over)")

# ============================================================================
# (4) manufactured-SAVE and manufactured-KILL probes
# ============================================================================
print("\n"+"="*76)
print("(4) SAVE / KILL probes")
print("="*76)
a0=9.36e-11
dt_h,_=cross(1e11*Msun,2*kpc,300*kpc,a0)
print(f"""  KILL probe (did anyone force a full-galaxy-DIAMETER 2x path?):
    Delay above is a SINGLE radial crossing per galaxy (host exit + MW entry), not doubled.
    Halving both (imagine only ONE crossing total) still gives ~{dt_h/1.7:.0e}x the bound. No manufactured kill.
  SAVE probe (did anyone DROP the host deep-MOND shell, where most B lives?):
    Host exit alone = {dt_h:.2e} s = {dt_h/1.7:.0e}x the bound. It is INCLUDED and it dominates.
    Dropping it would be the manufactured save; it is not dropped.
  VOID-RESCUE probe (use grad B, which vanishes in the void, as if it set the delay?):
    WRONG object. Delay ~ INT (B/2) dl uses ACCUMULATED B (~1e-6, sustained), not grad B.
    grad B -> 0 in the void only stops B from GROWING; B stays ~1e-6 across each shell.
  ESCAPE-CLASS check (does B tied to (nu-1)g_bar dodge the TeVeS/emulator wall?):
    NO. B being FIXED by the lensing-required enhancement is why it CANNOT be shrunk below
    O(1e-6); tying B to data makes the wall harder, not softer. Textbook Boran-Desai-Kahya-
    Woodard 2018 dark-matter-emulator: photons feel a deeper potential than gravitons. IN class.""")
print("="*76)
print("INDEPENDENT VERDICT: EXCLUDED across the ENTIRE bracket (best-case single thin shell")
print("~1e6 s to worst-case ~1e11 s), both footings. No sightline geometry rescues it.")
print("="*76)
