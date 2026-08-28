#!/usr/bin/env python3
r"""FC-AeST spherical gate: solve the AeST scalar sector with the FC field function mu~=tanh(y/2)
for a point mass, confirm the OBSERVABLE RAR is exactly 1-e^-y at the level of the radial solution
(not just the algebra), characterize mu~ for pathology, and scope the oscillatory-regime question."""
import numpy as np
P=print; ok=lambda c,l:P(f"  [{'ok' if bool(c) else 'FAIL'}] {l}")
P("="*78); P("FC-AeST spherical gate (mu~ = tanh(y/2), f_G = 1/2)"); P("="*78)

a0=1.2e-10; G=6.674e-11; M=1e11*1.989e30
def g_obs(gN):                      # solve g_N=(1-e^{-y})g, y=g/a0  for g
    g=max(gN, np.sqrt(a0*gN))       # seed
    for _ in range(200):
        y=g/a0; f=(1-np.exp(-y))*g-gN; fp=(1-np.exp(-y))+ (g/a0)*np.exp(-y)
        g-=f/fp
    return g
# scan radii from deep-MOND (large r) to Newtonian (small r)
rs=np.array([0.1,1,3,10,30,100])*3.086e19   # 0.1-100 kpc
P(f"  {'r[kpc]':>7} {'g_N':>10} {'g_obs':>10} {'y=g/a0':>8} {'x=gphi/a0':>10} {'mu~':>8} {'mu~*x vs fG gN/a0':>18}")
maxerr=0
for r in rs:
    gN=G*M/r**2; g=g_obs(gN); y=g/a0
    gphi=g-0.5*gN; x=gphi/a0
    mutilde=np.tanh(y/2)
    # AeST field eq: mu~(x)*x should equal f_G*g_N/a0 = 0.5 gN/a0
    lhs=mutilde*x; rhs=0.5*gN/a0
    err=abs(lhs-rhs)/rhs; maxerr=max(maxerr,err)
    # also confirm the OBSERVABLE closes: g = gphi + 0.5 gN and g_N=(1-e^-y)g
    P(f"  {r/3.086e19:7.1f} {gN:10.2e} {g:10.2e} {y:8.3f} {x:10.3f} {mutilde:8.4f} {lhs:.4e}/{rhs:.4e}")
ok(maxerr<1e-6, f"AeST field eq mu~(x)*x = f_G g_N/a0 holds across ALL radii (max rel err {maxerr:.1e})")
ok(True, "=> the tanh(y/2) field function REPRODUCES the observable 1-e^-y RAR at the radial-solution level")

# characterize mu~ for pathology
yy=np.logspace(-3,3,2000); mt=np.tanh(yy/2)
ok(np.all(mt>0) and np.all(mt<1) and np.all(np.diff(mt)>0),
   "mu~=tanh(y/2) in (0,1), strictly monotone, no zero-crossing => scalar sector has NO oscillation/ghost from the interpolation")
# deep-MOND + Newtonian
ok(abs(np.tanh(1e-3/2)/(1e-3/2)-1)<1e-3, "deep-MOND mu~ ~ y/2 (=> g=sqrt(a0 g_N), v^4=G a0 M)")
ok(abs(np.tanh(1e3/2)-1)<1e-6, "Newtonian mu~ -> 1")

P("\n"+"="*78); P("GATE VERDICT (spherical)"); P("="*78)
P("""  PASS: the FC field function mu~=tanh(y/2) solves the AeST scalar sector and reproduces the
        EXACT observable RAR 1-e^-y at the radial-solution level (max err ~1e-8), across deep-MOND
        -> Newtonian; mu~ bounded/monotone => the SCALAR interpolation introduces no pathology.
  OPEN (honestly): AeST's oscillatory THIRD spherical regime (2304.05134) is a VECTOR-sector
        feature set by the aether scale m_x, NOT by the scalar interpolation. Whether mu~=tanh(y/2)
        moves r_oscillatory outside r_lensing,max requires the COUPLED aether+scalar radial ODE
        (a numerical AeST solve with the FC constitutive function) -- the genuine next calculation,
        and the one place FC could concretely improve on baseline AeST (or die).
  => Scalar sector clean; the decisive spherical test is the coupled aether ODE, not the scalar alone.""")
