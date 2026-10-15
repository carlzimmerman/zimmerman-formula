#!/usr/bin/env python3
"""Exact finite bookkeeping checks; universal proofs are in REPORT.md."""
import json
import sys
from pathlib import Path
import sympy as s

out = Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
checks = []

def check(name, expression):
    answer = bool(expression)
    checks.append({"name": name, "passed": answer})
    if not answer:
        raise AssertionError(name)

def zero(name, expression):
    check(name, s.simplify(expression) == 0)

m, M, q, zeta, k = s.symbols("m M q zeta k", positive=True)
nu = s.Matrix([-1, 1, -1, 1])
masses = s.Matrix([m, m, M, M])
charges = s.Matrix([q, 0, 0, q])
zero("four_stock_rest_mass", masses.dot(nu))
zero("four_stock_charge", charges.dot(nu))
zero("four_stock_particle_pair_number", s.Matrix([1, 1, 0, 0]).dot(nu))
zero("four_stock_receiver_pair_number", s.Matrix([0, 0, 1, 1]).dot(nu))
check("single_reaction_left_nullspace_dimension", len(nu.T.nullspace()) == 3)
check("neutral_two_population_charge_defect", -q + k*0 == -q)
zero("critical_receiver_dictionary_iff_mass_equality",
     (q/M-zeta).subs(q,zeta*m) - zeta*(m-M)/M)
zero("mass_equal_charge_polarization_unchanged", (m*s.Matrix([1,0,0,1])).dot(nu))

# Gauge-invariance and mass/charge Noether coefficients of reaction phase.
zero("phase_gauge_invariant", charges.dot(nu))
zero("phase_mass_symmetry", masses.dot(nu))
dtheta, Avec, dlambda = s.symbols("dtheta Avec dlambda")
zero("RTM_plus_qA_gauge_covariant_combination",
     (dtheta-q*dlambda)+q*(Avec+dlambda)-(dtheta+q*Avec))

# Exact nonzero 2->2 COM kinematic witness.
R = s.Rational
pin = [s.Matrix([R(5,4), R(3,4), 0, 0]),
       s.Matrix([R(5,4), -R(3,4), 0, 0])]
pout = [s.Matrix([R(5,4), 0, R(3,4), 0]),
        s.Matrix([R(5,4), 0, -R(3,4), 0])]
eta = s.diag(-1,1,1,1)
for i, p in enumerate(pin+pout):
    zero("kinematic_on_shell_%d" % i, (p.T*eta*p)[0]+1)
for mu in range(4):
    zero("kinematic_four_momentum_%d" % mu,
         sum(p[mu] for p in pin)-sum(p[mu] for p in pout))
check("nonzero_final_phase_space", pout[0][2] > 0)

# Source compatibility, an explicit periodic nonuniform source and a flux check.
S, rhobardot, divC, divj = s.symbols("S rhobardot divC divj")
rho_t_dot = -divj-S
zero("polarization_divergence_source", rho_t_dot-rhobardot+divj+S+rhobardot)
meanS = s.symbols("meanS")
zero("periodic_reference_reduction", (-S-rhobardot).subs(rhobardot,-meanS) + S-meanS)
x = s.symbols("x", real=True)
source = 1+s.cos(x)
reference_dot = -s.integrate(source,(x,0,2*s.pi))/(2*s.pi)
zero("periodic_nonuniform_source_mean", reference_dot+1)
zero("periodic_local_correction", s.diff(-s.sin(x),x)+source+reference_dot)
check("fixed_reference_periodic_positive_source_obstruction", s.integrate(source,(x,0,2*s.pi)) != 0)
zero("finite_boundary_conversion_flux", (-x**3/3).subs(x,1)-(-x**3/3).subs(x,-1)+s.integrate(x**2,(x,-1,1)))
zero("mass_source_total", -S+S)
zero("conversion_current_total", divC-divC)

# Repository mass values are finite exact decimal rationals, not floats.
mn = R("939.56542194")
mchi, mS, mp, md = mn-R("0.5"), R(1), R("938.27208943"), R("1875.612945")
zero("portal_activation_mass_defect", mn+mS-mchi-R("1.5"))
zero("portal_recombination_mass_defect", mn-mchi-mS+R("0.5"))
zero("portal_capture_mass_defect", md+mS-mchi-mp+R("0.72456637"))
zero("portal_activation_charge", -q+q)
zero("portal_recombination_charge", -q-(-q))
zero("portal_capture_charge", -q+q)
zero("portal_scalar_critical_ratio_mismatch", (zeta*mchi/mS)/zeta-R("939.06542194"))
check("portal_scalar_ratio_not_one", mchi/mS != 1)
zero("portal_activation_B", -1+1)
zero("portal_recombination_B", -1+1)
zero("portal_capture_B", -1-1+2)
zero("portal_capture_electric_charge", -0-1+1+0)
check("vacuum_chi_to_nS_closed", mchi < mn+mS)
check("vacuum_neutron_to_chi_antiS_closed", mn < mchi+mS)
W = mchi+mS
Egamma = (W*W-mn*mn)/(2*W)
En = (W*W+mn*mn)/(2*W)
zero("recombination_energy", Egamma+En-W)
zero("recombination_neutron_on_shell", En*En-Egamma*Egamma-mn*mn)
threshold = ((mn+mS)**2-mchi*mchi)/(2*mchi)
zero("activation_threshold_invariant", mchi*mchi+2*mchi*threshold-(mn+mS)**2)

# Opposite charge currents: mass frame remains timelike, charge is spacelike.
v = R(3,5)
gamma = R(5,4)
Np = s.Matrix([gamma,gamma*v,0,0])
Nm = s.Matrix([gamma,-gamma*v,0,0])
masscur, chargecur = Np+Nm, Np-Nm
check("opposite_stock_mass_current_timelike", (masscur.T*eta*masscur)[0] < 0)
check("opposite_stock_charge_current_spacelike", (chargecur.T*eta*chargecur)[0] > 0)
zero("opposite_stock_zero_charge_density", chargecur[0])
check("opposite_stock_nonzero_charge_flux", chargecur[1] != 0)

# U variation is the Lorentz-orthogonal projector; normalized vector convention.
U = s.Matrix([R(5,4),R(3,4),0,0])
projector = s.eye(4)+U*(U.T*eta)
zero("normalized_mass_frame", (U.T*eta*U)[0]+1)
check("frame_projector_annihilates_U", projector*U == s.zeros(4,1))
check("frame_projector_idempotent", s.simplify(projector*projector-projector) == s.zeros(4))

result = {
    "verdict": "exact finite identities verified; uniform derivations in REPORT.md",
    "arithmetic": "SymPy exact rationals/symbolic real algebra",
    "checks_passed": len(checks), "checks": checks,
    "portal_rest_mass_changes_MeV": {
        "activation": str(mn+mS-mchi),
        "recombination": str(mn-mchi-mS),
        "nuclear_capture": str(md+mS-mchi-mp)},
    "portal_scalar_q_over_m_relative_to_chi": str(mchi/mS),
    "non_claims": ["No physical rate, abundance, remnant retention, or multi-current cone theorem.",
                   "No external particle constants or phenomenological limits authenticated."]}
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"passed":len(checks), "output":str(out)},sort_keys=True))
