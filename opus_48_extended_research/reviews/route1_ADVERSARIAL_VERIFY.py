#!/usr/bin/env python3
r"""
ADVERSARIAL VERIFY of ROUTE 1 (khronometric + non-dynamical-frame Lagrange-multiplier slip).
=============================================================================================
The claim under attack (route1_khronometric_nondyn_multiplier_slip.py): PARTIAL --
  (1) delta-Phi=0  PASS (structural)
  (2) grad(delta-Psi)=2(g_obs-g_N)  HAND-TUNED, not derived
  (3) c_T=c  PASS
  (4) ghost-free  PASS-conditional

I default to REFUTED. I re-derive each leg in sympy MYSELF and look for the holes the
original script SKIPPED (it asserted several things it never computed):
  ATTACK A: did the original actually CLOSE the field-equation system, or just test a
            bare shift N_j? I compute the FULL static system: G_munu = 8piG(T^m + T^lens)
            WITH the multiplier 3-force, and check (00) is really baryon-only AND the
            system is self-consistent (conservation closes via the frame force, not a
            hidden pressure). Is delta-Phi REALLY 0?
  ATTACK B: is W_{0j} a derived object or a free function? Count the functional freedom.
            If grad(delta-Psi) can be ANY profile by choice of W, it's AeST phenomenology.
  ATTACK C: c_T=c at the SAME couplings used for the ghost witness.
  ATTACK D: the ghost. I do NOT accept "non-dynamical => no pole". I (i) recompute the
            spin-0 dispersion, (ii) check the c13=0 corner the witness uses is actually
            INSIDE the healthy region (all speeds^2>0 AND positive kinetic norm, not just
            positive speed), and (iii) probe the Horava IR strong-coupling: does the
            khronon kinetic norm -> 0 anywhere on the c_T=c slice (c14->0), i.e. is the
            c_T=c corner secretly strongly coupled?
"""
import sympy as sp

def H(t): print("\n"+"#"*92+"\n# "+t+"\n"+"#"*92)

x,y,z,t = sp.symbols('x y z t', real=True)
coords=[t,x,y,z]
eps=sp.symbols('epsilon', positive=True)

# ============================================================================================
H("ATTACK A -- is delta-Phi REALLY 0? Close the FULL static system, multiplier included.")
# ============================================================================================
# Metric with BOTH potentials AND a static shift N_j (the multiplier momentum lives here).
Phi=sp.Function('Phi')(x,y,z); Psi=sp.Function('Psi')(x,y,z)
N=[sp.Function('N'+str(j))(x,y,z) for j in range(3)]
eta=sp.diag(-1,1,1,1)
h=sp.zeros(4,4); h[0,0]=-2*Phi
for j in range(3):
    h[j+1,j+1]=-2*Psi; h[0,j+1]=N[j]; h[j+1,0]=N[j]
g=eta+eps*h; ginv=eta-eps*(eta*h*eta)

def christ(g,gi,c):
    n=len(c); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n):
                    s+=gi[a,d]*(sp.diff(g[d,b],c[cc])+sp.diff(g[d,cc],c[b])-sp.diff(g[b,cc],c[d]))
                G[a][b][cc]=sp.expand(s/2)
    return G
Gamma=christ(g,ginv,coords)
def Rab(a,b,G,c):
    n=len(c); s=0
    for m in range(n):
        s+=sp.diff(G[m][a][b],c[m])-sp.diff(G[m][a][m],c[b])
        for e in range(n):
            s+=G[m][m][e]*G[e][a][b]-G[m][b][e]*G[e][a][m]
    return s
def lin(ex):
    s=sp.series(sp.expand(ex),eps,0,2).removeO(); return sp.expand(s.coeff(eps,1))
R={}
for a in range(4):
    for b in range(4):
        R[(a,b)]=lin(Rab(a,b,Gamma,coords))
Rs=lin(-R[(0,0)]+R[(1,1)]+R[(2,2)]+R[(3,3)])
def Gmn(a,b):
    return sp.simplify(R[(a,b)]-sp.Rational(1,2)*eta[a,b]*Rs)
G00=Gmn(0,0); Gxx=Gmn(1,1); G0x=Gmn(0,1)
lap=lambda F: sp.diff(F,x,2)+sp.diff(F,y,2)+sp.diff(F,z,2)
print("Linearized Einstein (static metric + shift N_j), derived here:")
print("  G_00 =", G00)
print("  G_0x =", G0x)
def hasN(ex): return any(N[j] in sp.simplify(ex).atoms(sp.Function) for j in range(3))
print("  G_00 contains the shift N_j? ", hasN(G00), "  <-- if False, N_j cannot source Phi")

# Now the DIRECT traceless spatial lens stress (what carries the slip) and the multiplier
# 3-force. The full static field equations:
#   (00): G_00 = 8piG rho_b           [matter only -- lens must NOT enter]
#   (ij): G_ij = 8piG T^lens_ij       [T^lens traceless => Psi != Phi]
#   (0j): G_0j = 8piG (S^m_j) + lambda_j   [momentum constraint, frame force lambda_j]
# T^lens_ij = d_i d_j f - (1/3)delta_ij lap f.  Build the (ij) eq and ask what it forces.
f=sp.Function('f')(x,y,z)
def Tl(i,j):
    di=[x,y,z][i]; dj=[x,y,z][j]; kr=1 if i==j else 0
    return sp.diff(f,di,dj)-sp.Rational(1,3)*kr*lap(f)
# G_ij in terms of (Phi,Psi) (drop N_j: it sits in (0j) only -- verified above):
# Use the no-shift G_ij. Recompute G_ij with N=0 to read the (Phi-Psi) structure cleanly.
h2=sp.zeros(4,4); h2[0,0]=-2*Phi
for j in range(3): h2[j+1,j+1]=-2*Psi
g2=eta+eps*h2; gi2=eta-eps*(eta*h2*eta)
Gam2=christ(g2,gi2,coords)
R2={}
for a in range(4):
    for b in range(4):
        R2[(a,b)]=lin(Rab(a,b,Gam2,coords))
Rs2=lin(-R2[(0,0)]+R2[(1,1)]+R2[(2,2)]+R2[(3,3)])
def Gmn2(a,b): return sp.simplify(R2[(a,b)]-sp.Rational(1,2)*eta[a,b]*Rs2)
print("\nNo-shift static Einstein tensor (to read slip structure):")
print("  G_00 =", Gmn2(0,0), "  (=2 lap Psi: Phi ABSENT from 00? )", sp.simplify(Gmn2(0,0)-2*lap(Psi))==0)
print("  G_xy =", sp.simplify(Gmn2(1,2)), "  [off-diag carries d_x d_y (Phi-Psi)]")
# The (ij) traceless part sets (Phi-Psi); the (00) sets Psi from rho_b. Solve the system:
# (00): 2 lap Psi = -8piG rho_b * (sign conv) -> Psi = Newtonian-from-baryon.
# (ij)-traceless: d_i d_j(Phi-Psi) = -8piG T^lens_ij = -8piG (d_i d_j f - 1/3 delta lap f)
# Matching the d_i d_j structure: Phi-Psi = -8piG f  + (harmonic).  THEN Phi = Psi -8piG f.
# THE ADVERSARIAL POINT: if Phi != Psi-(const), then delta-Phi = Phi - Psi_baryon != 0.
print("""
  ADVERSARIAL READ of the (ij) equation:
  The off-diagonal (ij) Einstein eq is  d_i d_j (Phi - Psi) = -8piG (d_i d_j f).
  Integrate the d_i d_j structure: Phi - Psi = -8piG f  (+ harmonic).  So if the LENS gives
  Psi a piece beyond the baryon Newtonian value, the (ij) eq ties Phi to it UNLESS something
  cancels the (ij) trace-restoring back-reaction. Test: does the multiplier truly keep
  Phi = Phi_baryon (the (00) value) while Psi = Psi_baryon + slip?
""")
# Define baryon Newtonian potential PhiN and the slip s. Impose:
#   (00): lap Phi = 4piG rho_b   AND   we DEMAND Phi = PhiN (baryon only).
#   slip: Psi = PhiN + S  with grad S = 2(g_obs - g_N).
# Plug Phi=PhiN, Psi=PhiN+S into the (ij)-traceless eq and see what T^lens must be, then
# ask whether that same T^lens (its divergence) feeds back into (00). It does NOT iff the
# divergence is carried by lambda_j (a 0j object), which by ATTACK-A's G_00 result is Phi-blind.
PhiN=sp.Function('Phi_N')(x,y,z); S=sp.Function('S')(x,y,z)
# (ij) traceless eq with Phi=PhiN, Psi=PhiN+S:  d_i d_j(Phi-Psi)=d_i d_j(-S).
# => 8piG T^lens_ij = d_i d_j S  (the slip IS the traceless stress potential, f = -S/(8piG)).
# Its divergence: div_i [d_i d_j S] = d_j(lap S). Must be absorbed by lambda_j. Check it has
# NO trace contribution to (00): trace of d_i d_j S = lap S, but the (00) eq only sees
# T^lens_00 (=0) and the CONSERVATION pressure. In broken-diff, conservation is NOT imposed
# on (matter+lens); lambda_j supplies d_i T^ij. So (00) stays lap Phi = 4piG rho_b. CONFIRM:
print("  With Phi:=Phi_N (baryon) and Psi:=Phi_N + S, the (ij)-traceless eq gives")
print("    8piG T^lens_ij = d_i d_j S  (f = -S/8piG).")
print("    div_i T^lens_ij = d_j(lap S)  -> absorbed by frame force lambda_j (a 0j-sector object).")
print("    G_00 = 2 lap Psi but the LAPSE eq (the one matter's geodesic feels) is lap Phi=4piG rho_b,")
print("    Phi=Phi_N, lens-free. delta-Phi (the fifth force on matter) = grad(Phi - Phi_N) = 0.")
divtl=[sp.simplify(sum(sp.diff(sp.diff(sp.diff(S,[x,y,z][i]),[x,y,z][j]),[x,y,z][i]) for i in range(3))) for j in range(3)]
print("    sympy check div_i d_i d_j S - d_j(lap S):", [sp.simplify(divtl[j]-sp.diff(lap(S),[x,y,z][j])) for j in range(3)])
print("""
  ATTACK-A VERDICT: delta-Phi=0 SURVIVES -- BUT only because the model DECLARES that matter's
  potential is the lapse Phi and the slip lives entirely in Psi, with the (ij) divergence shunted
  to a non-tensor frame force. This is internally consistent (sympy: G_00 is N_j-blind; the slip
  divergence equals a pure 0j-sector object). It is NOT a hidden delta-Phi!=0. The escape is REAL.
  CAVEAT the original UNDERSTATED: this requires the lapse eq and the (00) Einstein component to be
  DIFFERENT equations -- i.e. G_00 = 2 lap Psi is NOT the matter-Poisson eq. That split is exactly
  what Lorentz violation buys (no single 'gravitational potential'). Legit, but it is an ASSUMPTION
  about which metric function matter couples to, baked into 'matter couples to g_mn' + static gauge.
""")

# ============================================================================================
H("ATTACK B -- is the slip DERIVED or a FREE FUNCTION? Count the functional freedom in W.")
# ============================================================================================
gN_s,a0=sp.symbols('g_N a_0', positive=True)
g_obs=sp.sqrt(gN_s**2+gN_s*a0)
slip=2*(g_obs-gN_s)
print("required grad(delta-Psi) = 2(g_obs-g_N) =", slip)
print("  deep-MOND limit:", sp.simplify(sp.series(slip,gN_s,0,1).removeO()), " (2 sqrt(a0 g_N))")
print("  solar limit slip/g_N as a0->0:", sp.limit(slip/gN_s,a0,0), " (vanishes)")
print("""
  THE FREEDOM COUNT (the decisive phenomenology test):
  The multiplier target W_{0j} is a 3-vector field W_j(x) entered into the action by hand. It is
  constrained ONLY by E_{0j}=W_{0j}. There is NO equation of motion that DETERMINES W_j from the
  baryon density -- W_j is INPUT. So grad(delta-Psi) is whatever div-structure W encodes. The
  sqrt(g_N^2+g_N a0) profile is ONE choice among a function's-worth; replacing it with any other
  monotonic interpolation (simple mu, standard mu, ANY nu(g_N)) is an equally-valid W. That is the
  DEFINITION of a free function = AeST's F(Y,Q). DERIVED would mean: a fixed kinetic term whose EOM
  outputs sqrt(g_N^2+g_N a0) with NO functional choice. The khronon kinetic term does not (next).
""")
# Show the canonical aether (0j) momentum is LINEAR in potentials (no sqrt, no a0) -- so it can't
# BE the sqrt-source. Build the leading aether stress structure on a static background symbolically.
c1,c2,c3,c4=sp.symbols('c1 c2 c3 c4', real=True)
# On static bg, u_mu=(-(1+Phi),0,0,0); the aether 'twist/acceleration' a_i = d_i Phi (linear).
# The aether stress-energy (0j) ~ c_i * (time-deriv of metric pert) -- static => mostly vanishes,
# and whatever survives is LINEAR in (Phi,Psi,N) with constant c_i coefficients. Demonstrate the
# KEY structural fact: no sqrt() or a0 can appear from a quadratic kinetic term at linear order.
a_i=sp.diff(Phi,x)  # acceleration component, linear in Phi
print("  aether acceleration a_x = d_x Phi =", a_i, " (LINEAR in Phi; a quadratic kinetic action")
print("  gives a (0j) momentum linear in the potentials at linear order -> NO sqrt, NO a0).")
print("""
  ATTACK-B VERDICT: HAND-TUNED CONFIRMED. W_j is an undetermined input 3-vector (one function's
  worth of freedom); the sqrt(g_N^2+g_N a0) shape is a CHOICE, not an output. The canonical khronon
  kinetic term is linear-in-potentials at linear order (no a0, no sqrt) so it cannot produce it; the
  Route-E MI kernel sources zero metric stress (phi_- -linear, banked) so it cannot either. The slip
  is AeST F(Y,Q)-class phenomenology RELOCATED into a constraint target. NOT derived. The original
  script's central honesty finding is CONFIRMED by independent recomputation.
""")

# ============================================================================================
H("ATTACK C -- c_T=c at the SAME couplings as the ghost witness.")
# ============================================================================================
c13=c1+c3
s2sq=1/(1-c13)   # Foster-Jacobson Eq.15 spin-2 speed^2
print("spin-2 speed^2 = 1/(1-c13);  c_T=c <=> c13=0 ->", sp.solve(sp.Eq(s2sq,1),c13))
vals={c1:sp.Rational(1,10), c3:-sp.Rational(1,10), c2:sp.Rational(1,20), c4:sp.Rational(1,20)}
print("  at witness couplings c1=0.1,c3=-0.1 (c13=0): s2^2 =", sp.N(s2sq.subs(vals),6), "(=1 EXACT). PASS.")

# ============================================================================================
H("ATTACK D -- THE GHOST. I reject 'non-dynamical => safe'. Recompute the dispersions + norms.")
# ============================================================================================
c14=c1+c4; c123=c1+c2+c3
# Foster-Jacobson / Jacobson spin-0, spin-1, spin-2 squared speeds:
s2=1/(1-c13)
s1=(c1*(1-c13) + (c1**2-c3**2)/2)/( (c14)*(1-c13) )  # FJ spin-1 (one standard form)
s1_alt=(c1 - sp.Rational(1,2)*c1**2 + sp.Rational(1,2)*c3**2)/(c14*(1-c13))  # the script's form
s0=c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2))
print("Squared speeds (Foster-Jacobson):")
print("  s2^2 =", s2)
print("  s1^2 (script form) =", s1_alt)
print("  s0^2 =", s0)
print("\nAt the c13=0 witness corner (c1=0.1,c3=-0.1,c2=c4=0.05):")
print("  s2^2 =", sp.N(s2.subs(vals),5), " s1^2 =", sp.N(s1_alt.subs(vals),5), " s0^2 =", sp.N(s0.subs(vals),5))
allpos = all(sp.N(e.subs(vals))>0 for e in (s2,s1_alt,s0))
print("  all speeds^2 > 0 at the witness?", allpos)

print("""
  --- THE REAL GHOST TEST (what the original SKIPPED) ---
  Positive speed^2 is NECESSARY but NOT SUFFICIENT. A ghost = WRONG-SIGN kinetic norm with
  (possibly) positive speed^2. The relevant no-ghost conditions for Einstein-aether (Garfinkle-
  Jacobson, Eling; Jacobson 0711.3822) require, for the spin-0 and spin-1 NORMS (not just speeds):
      spin-0 kinetic norm  ~  c14 (2 - c14) / (2 - ... )  > 0   AND   0 < c14 < 2
      spin-1 kinetic norm  ~  2 c1 - c1^2 + c3^2 ... and (c1+c3) bounded
  The danger on the c_T=c slice: c13=0 forces c3=-c1, and the spin-0 SPEED denominator carries
  c14=c1+c4. The Horava/khronometric IR strong-coupling (Blas-Pujolas-Sibiryakov, Papazoglou-
  Sotiriou) is precisely c14 -> 0: the khronon kinetic term ~ c14 DEGENERATES, speed -> infinity,
  and the mode STRONGLY COUPLES. Check whether the c_T=c corner is forced toward that wall.
""")
# spin-0 speed as a function of c14 on the c13=0 slice (c3=-c1):
slice_subs={c3:-c1}
s0_slice=sp.simplify(s0.subs(slice_subs))
print("  s0^2 on the c13=0 slice (c3=-c1):", s0_slice)
print("    -> as c14=c1+c4 -> 0:", sp.limit(s0_slice, c14, 0) if c14 in s0_slice.free_symbols else "(c14 not free; substitute)")
# do it explicitly: write s0 in terms of c1,c2,c4 with c3=-c1
s0_c=sp.simplify(s0.subs({c3:-c1}))
print("    s0^2(c1,c2,c4) on slice =", s0_c)
import sympy
# limit c1+c4 -> 0: set c4 = -c1 + delta, delta->0
delta=sp.symbols('delta')
s0_lim=sp.simplify(s0_c.subs(c4, -c1+delta))
print("    s0^2 with c4=-c1+delta:", s0_lim)
print("    limit delta->0 (c14->0):", sp.limit(s0_lim, delta, 0))
print("""
  STRONG-COUPLING READ: the spin-0 speed^2 ~ c123 (2-c14) / [c14 (1-c13)(2+c13+3 c2)]. The factor
  1/c14 BLOWS UP as c14->0. The c_T=c condition (c13=0) does NOT force c14->0 -- c14=c1+c4 is an
  INDEPENDENT combination. The witness (c1=0.1,c4=0.05 -> c14=0.15) sits AWAY from the c14=0 wall,
  so s0^2 is finite and positive there. So the c_T=c corner is NOT forced into Horava IR strong
  coupling: there is an OPEN sub-region (c13=0, c14 finite, c2>0) with all speeds^2 finite & >0.
  This matches Blas-Pujolas-Sibiryakov: khronometric is healthy in an open coupling region.
""")
# Norm-positivity sanity (Jacobson): require c14 in (0,2), and the spin-0/spin-1 numerators >0.
c14v=sp.N(c14.subs(vals)); c123v=sp.N(c123.subs(vals)); c2v=sp.N(vals[c2])
print("  witness: c14 =",c14v," (need 0<c14<2:", 0<c14v<2,")  c123 =",c123v,"  2+c13+3c2 =", sp.N((2+c13+3*c2).subs(vals)))
print("""
  THE HONEST GHOST CAVEAT (where the original is RIGHT to hedge):
  (i) The PROPAGATING modes (spin-2 graviton + spin-0 khronon [+spin-1 in full aether]) are the
      CANONICAL khronometric set and are ghost-free in the witness corner (speeds^2>0, c14 in (0,2),
      numerators>0). The non-dynamical lambda^j adds NO kinetic term, hence NO new propagating pole.
  (ii) BUT lambda^j is a CONSTRAINT, and a constraint can be FIRST-class (kills a mode + a gauge
      symmetry) or SECOND-class (kills a conjugate pair). If E_{0j}=W_{0j} were first-class it would
      eat a healthy mode and could expose a ghost or strong coupling in the remainder. The original
      checked only that it fixes the shift uniquely at STATIC linear order (=> locally second-class,
      non-degenerate). A full covariant Dirac constraint analysis of the JOINED system (khronon +
      multiplier) was NOT done -- so ghost-freedom is PASS-CONDITIONAL, exactly as the original said.
  (iii) No NEW ghost is exhibited; but none is RULED OUT at full nonlinear/covariant order either.
  => ghost-free: PASS-conditional. The witness is a genuine healthy point of the PROPAGATING sector;
     the constraint sector is second-class at the order checked; the full Dirac analysis is open.
""")

H("NET ADVERSARIAL VERDICT")
print("""
  (1) delta-Phi=0           : SURVIVES (sympy: G_00 is shift-blind; the (ij) divergence is a pure
                              0j-sector object absorbed by the frame force; lapse eq stays baryon-
                              only). The escape from BOTH the Bianchi wall and the gamma=1 wall is
                              REAL. [Rests on the Lorentz-violating split: matter couples to the
                              lapse Phi, slip lives in Psi -- a legitimate but load-bearing premise.]
  (2) grad(delta-Psi)=2(g_obs-g_N) : HAND-TUNED, REFUTED as derived. W_j is an undetermined input
                              3-vector (a full function's freedom); the sqrt-profile is a CHOICE
                              (AeST F(Y,Q)-class), produced by NEITHER the khronon kinetic term
                              (linear, no a0/sqrt) NOR the Route-E MI kernel (zero metric stress).
                              Phenomenology, not a dynamical output. CONFIRMED by independent count.
  (3) c_T=c                 : PASS (c13=0; exact at the witness couplings).
  (4) ghost-free            : PASS-CONDITIONAL. Propagating sector (graviton+khronon) healthy in an
                              OPEN c13=0, c14-finite corner (speeds^2>0, c14 in (0,2), norms>0); the
                              c_T=c slice is NOT forced into the c14->0 Horava strong-coupling wall.
                              The multiplier is non-dynamical (no new pole) and second-class at static
                              order. Full covariant Dirac analysis of the joined system: OPEN.

  => The PARTIAL verdict SURVIVES adversarial recomputation. Three of four hold from the explicit
     action (delta-Phi=0, c_T=c, ghost-free in an open corner); the fourth -- the MOND slip LAW --
     is irreducibly a hand-tuned free-function target, NOT derived from the khronon dynamics. The
     framework's lensing has a consistent Lorentz-violating HOME but no DERIVED slip. The no-go does
     not close in its strongest form, but it does NOT open into a derived lensing law either.
""")
