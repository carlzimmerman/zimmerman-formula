#!/usr/bin/env python3
r"""FC-AeST: verify the exact kernel bridge (observable mu vs AeST field mu-tilde) + limits + a0(Q).
FC-AeST = AeST chassis (Skordis-Zlosnik 2007.00082, 6 DOF, F(Y,Q) free) with:
  (i) exact-exponential kernel translated via the AeST TWO-FIELD structure g = g_phi + f_G g_N;
  (ii) cosmological lock a0^2(Q) = -kappa^2 c^2 G K(Q), K(Q) = -(1/2)F(0,Q) (Carl's promotion,
       DOI 10.5281/zenodo.22015358).
Matter minimally coupled to g_munu (photons see the same metric => no conformal-lensing trap)."""
import sympy as sp
y=sp.symbols('y',positive=True); fG=sp.Rational(1,2)
P=print; ok=lambda c,l: P(f"  [{'ok' if bool(c) else 'FAIL'}] {l}")
P("="*78); P("FC-AeST kernel bridge (f_G=1/2)"); P("="*78)

mu_obs = 1-sp.exp(-y)                       # OBSERVABLE MOND function (target)
gN_over_g = mu_obs                          # g_N = mu_obs * g  (definition of observable mu)
gphi_over_g = sp.simplify(1 - fG*mu_obs)    # g_phi = g - f_G g_N
x = sp.simplify(gphi_over_g*y)              # x = g_phi/a0 = (g_phi/g)*(g/a0) = gphi_over_g * y
ok(sp.simplify(x - y*(1+sp.exp(-y))/2)==0, f"x = g_phi/a0 = (y/2)(1+e^-y)   [derived: {sp.simplify(x)}]")

mu_tilde = sp.simplify(fG*mu_obs/gphi_over_g)   # mu~ = f_G g_N/g_phi
ok(sp.simplify(mu_tilde - sp.tanh(y/2))==0, f"mu~(x) = f_G mu_obs/(1-f_G mu_obs) = tanh(y/2)   [{sp.simplify(mu_tilde)}]")

dxdy = sp.simplify(sp.diff(x,y))
ok(sp.simplify(dxdy - (1+(1-y)*sp.exp(-y))/2)==0, f"dx/dy = (1/2)[1+(1-y)e^-y]   [{sp.simplify(dxdy)}]")
# monotone: min of 1+(1-y)e^-y over y>=0 is at y=2, value 1-e^-2>0
minval = float((1+(1-2)*sp.exp(-sp.Integer(2))))
ok(minval>0, f"dx/dy > 0 for all y>=0 (min at y=2 = (1-e^-2)/2 = {minval/2:.3f}) => x<->y invertible")

P("\n"+"-"*78); P("Asymptotic limits survive the translation:"); P("-"*78)
ok(sp.limit(mu_obs/y,y,0)==1, "deep-MOND: mu_obs ~ y => g_N=g^2/a0 => g=sqrt(a0 g_N) => v^4=G a0 M (BTFR)")
ok(sp.limit(mu_obs,y,sp.oo)==1, "Newtonian: mu_obs->1 => g_N->g (g_phi->g_N/2, g=g_phi+g_N/2->g_N)")
ok(sp.limit(mu_tilde,y,sp.oo)==1 and sp.limit(mu_tilde/(y/2),y,0)==1,
   "field mu~: ->1 Newtonian, ~ y/2 deep-MOND (healthy interpolation, mu~ in (0,1))")
# constitutive function J'_FC(x^2) = tanh(y(x)/2); note it is NOT the observable mu -- that's the point
P("  J'_FC(x^2) = mu~(x) = tanh(y(x)/2);  J_FC(x^2) = INT_0^{x^2} tanh(y(sqrt u)/2) du  (AeST F-sector)")

P("\n"+"-"*78); P("Cosmological lock (the FC novelty):"); P("-"*78)
P("  a0^2(Q) = -kappa^2 c^2 G K(Q),  K(Q)=-(1/2)F(0,Q)  =>  a0(z)=kappa c sqrt(G rho_DE(z))")
P("  with rho_DE(z) := -K[Qbar(z)]  =>  a0(z)/a0,0 = sqrt(rho_DE(z)/rho_DE,0)  =>  a0 PROPORTIONAL sqrt(rho_DE)")
P("  LIMIT w=-1 (Lambda): rho_DE=const => a0=const (flat, matches STANDING 'nearly flat in MOND regime').")
P("  This SUPERSEDES the naive a0(z) proportional H(z) (STANDING: H(z) reading disfavoured ~2.3 sigma).")
P("  Distinctive ONLY if DE evolves -- exactly what DESI DR2/DR3 probe (evolving-DE preference ~few sigma).")

P("\n"+"="*78); P("HONEST GATE TABLE"); P("="*78)
gates=[
("kernel bridge mu_obs=1-e^-y <-> mu~=tanh(y/2)","PASS (exact, this script)"),
("Newtonian + deep-MOND + BTFR","PASS (exact, this script)"),
("matter minimal coupling to g (photons+matter same metric)","PASS by construction (AeST)"),
("c_T = 1 (GW170817)","INHERITED PASS -- AeST K_B structure, c_gamma=c_GW exact (2007.00082)"),
("gamma_PPN = 1 (lensing = dynamics, Phi=Psi)","INHERITED PASS -- committed typeII_direct_variation: no dark anisotropic stress; AeST lensing 21.2->0.6 sigma"),
("Hamiltonian DOF = 6 (4 first + 4 second class)","INHERITED for general F(Y,Q) (2307.15126); Q-dep J stays in that class => SUPPORTED, must re-run"),
("a0(z) proportional sqrt(rho_DE) (cosmological lock)","STRUCTURAL TARGET (the FC hypothesis); testable vs DESI"),
("low-k stability (AeST has a known unbounded-H low-k mode)","OPEN -- must recompute with Q-dependent a0"),
("oscillatory 3rd quasistatic regime (2304.05134)","OPEN -- must show it sits outside observed radii"),
("clusters, wide-binary gamma_v, cosmo perturbations","OPEN"),
("kappa, Z (a0 normalization)","FITTED, never derived -- a0 is now a FIELD but kappa^2 still fitted"),
("2 DOF","ABANDONED -- FC-AeST is 6 DOF (honest concession; the 2-DOF program is closed, this is a DIFFERENT chassis)"),
]
for g,s in gates: P(f"  {g:56} {s}")
P("\nVERDICT: FC-AeST is AeST + (exact kernel via inverse problem) + (a0(Q) cosmological lock).")
P("The kernel bridge and limits are EXACT (new, verified). The AeST-baseline gates (c_T, gamma_PPN,")
P("lensing, 6 DOF) are inherited/committed. The genuine NEW physics = a0(z) prop sqrt(rho_DE); the")
P("genuine OPEN risks = low-k mode + oscillatory regime under the Q-dependent a0. NOT a completed")
P("theory; it is the first FC candidate that removes BOTH MMG killers (no C_M lapse-constraint; no")
P("conformal-lensing trap) -- at the honest cost of 6 DOF and fitted kappa.")
