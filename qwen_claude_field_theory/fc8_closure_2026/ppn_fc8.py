"""
G2 — FC-8R PPN.  Status: OPEN (not derived from the FC-8R field equations).
==========================================================================
REQUIREMENT: DERIVE the FC-8R 1PN metric from the action; map to PPN gauge; extract
gamma,beta,alpha_1,alpha_2,alpha_3,xi,zeta_1..4. Do NOT import Einstein-aether PPN formulas unless the
FC-8R->EA parameter map is derived explicitly. Then scan the healthy space; per surviving point report
K_B, lambda_s, K2, mu, V0, m_chi, alpha_1, alpha_2, beta-1, gamma-1, c_T^2-1, all kinetic eigenvalues,
all propagation speeds. (GW170817: EA c_13 ~ 1e-15, 1802.04303; 2026 pulsar preferred-frame bounds.)
"""
import sympy as sp
P = print
P("="*94); P("G2  FC-8R PPN"); P("="*94)

# derivable context (NOT a PASS): at Solar-System accelerations the MOND operator is ultra-suppressed.
y = sp.symbols('y', positive=True)
one_minus_mu = sp.series(1 - y/(1+y**10)**sp.Rational(1,10), y, sp.oo, 3)
P(f"  context: 1 - mu10(y) = {one_minus_mu}  (y=g/a0 >> 1 at 1 AU) => MOND term ~ (a0/g)^10, negligible.")
P("  => the FC-8R 1PN metric is dominated by the AeST baseline + the constant background a0=sqrt(kappa^2 G V0).")
P("  BUT per REQUIREMENTS.md: 'A statement inherited from ordinary AeST is NOT an FC-8R PASS.' The AeST")
P("  preferred-frame sector (alpha_1,alpha_2) is nonzero in general and must be DERIVED for FC-8R, not")
P("  imported. The chi background (chi=chi0, chi-dot cosmological) may enter alpha_2 via the frame; unproven.")

P("\n  [OPEN] Required and NOT done here:")
for s in ["Derive the FC-8R 1PN metric (Phi,Psi,phi,A_0,A_i,chi) directly from delta S_FC8R = 0.",
          "Map FC-8R -> Einstein-aether parameters (c_1..c_4) EXPLICITLY; only then may EA PPN formulas be used.",
          "Extract gamma,beta,alpha_1,alpha_2,alpha_3,xi,zeta_1..4 from the mapped/derived metric.",
          "Scan {K_B,K2,Q0,mu,V0,m_chi} healthy space; per point print alpha_1,alpha_2,beta-1,gamma-1,c_T^2-1,",
          "  all scalar/vector kinetic eigenvalues, all propagation speeds.",
          "Confront GW170817 (c_13~1e-15) and 2026 strong-field pulsar preferred-frame bounds NON-parametrically."]:
    P(f"         - {s}")
P("\n  DISCIPLINE: do NOT report 'PPN PASS' by inheriting AeST. Do NOT add a PPN counterterm. OPEN stays OPEN.")
P("\n"+"="*94); P("G2 STATUS: OPEN.")
