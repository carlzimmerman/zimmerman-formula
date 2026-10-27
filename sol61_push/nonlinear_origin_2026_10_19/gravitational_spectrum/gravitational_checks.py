#!/usr/bin/env python3
"""Small deterministic checks of the stated two-body Coulomb contract."""
import json
import sys
from pathlib import Path
import mpmath as mp

mp.mp.dps = 110
D = mp.mpf
ROOT = Path(__file__).resolve().parent
OUT = ROOT / sys.argv[1] / "results.json"
def s(x):
    return mp.nstr(x, 40)
def near(a, b, tol="1e-70"):
    assert abs(a-b) <= D(tol)*max(abs(a), abs(b), D("1e-200")), (s(a), s(b))

# Declared SI inputs, rather than a fit or a prediction of G.
G = D("6.67430e-11")
c = D("299792458")
eVJ = D("1.602176634e-19")
h = D("6.62607015e-34")
hbarJs = h/(2*mp.pi)
hbar = hbarJs/eVJ
hbarc = hbar*c
m = D("1e6")
u = D(".02")
g = D(".002168")*m
lam = D(".00587528")
M = 2*m*mp.sqrt(1+u*u)
delta = 2*m*u*u/(mp.sqrt(1+u*u)+1)
alpha = G*(m*eVJ/c**2)**2/(hbarJs*c)
a = 2/(m*alpha)
B = m*alpha**2/4
c3 = g/(2*m*mp.sqrt(2*M))
A = g*g/(16*mp.pi**2*M*mp.sqrt(m))
w1 = 2*c3*c3/(mp.pi*a**3)
J0 = g*g*alpha/(16*mp.pi*M)
near(w1, 2*B*J0)
near(B, 1/(m*a*a))
asct = lam/(8*mp.pi*m)
g2 = lam/(2*m*m)
near(g2, 4*mp.pi*asct/m)
near(g2/(mp.pi*a**3)/B, 4*asct/a)

# Hydrogenic radial normalization and contact residue, independent integral.
radial = []
for n in [1, 2, 3, 7]:
    def R(x):
        return 2*mp.exp(-x/n)*mp.laguerre(n-1, 1, 2*x/n)/D(n)**D("2.5")
    norm = mp.quad(lambda x: x*x*R(x)**2, [0, 1, 10, 100, mp.inf])
    contact = R(0)**2/(4*mp.pi)
    near(norm, 1, "1e-65")
    near(contact, 1/(mp.pi*n**3))
    radial.append({"n":n, "norm":s(norm), "dimensionless_contact":s(contact)})

# Sommerfeld factor: hypergeometric normalization versus closed expression.
sommerfeld = []
for eta in [D(".01"), D(".3"), D("3"), D("20")]:
    S_gamma = mp.exp(mp.pi*eta)*abs(mp.gamma(1-1j*eta))**2
    S_closed = 2*mp.pi*eta/(-mp.expm1(-2*mp.pi*eta))
    near(S_gamma, S_closed)
    sommerfeld.append({"eta":s(eta), "S":s(S_closed)})
threshold = []
for ratio in [D("1e-4"), D(".01"), D("1"), D("100")]:
    eps = B*ratio
    x = mp.pi*alpha*mp.sqrt(m/eps)
    JC = A*mp.sqrt(eps)*x/(-mp.expm1(-x))
    near(JC/J0, 1/(-mp.expm1(-2*mp.pi/mp.sqrt(ratio))))
    threshold.append({"epsilon_over_B":s(ratio), "J_C_over_J0":s(JC/J0)})

# Positive/negative threshold logs cancel in the complete spectral measure.
# The bound sum is evaluated by an independent digamma identity.
digamma = []
for t in [D(".01"), D("1"), D("10")]:
    aa = 1/mp.sqrt(t)
    value = (mp.digamma(1+1j*aa)+mp.digamma(1-1j*aa)+2*mp.euler)/2
    direct = mp.nsum(lambda n: 1/(n*(1+t*n*n)), [1, mp.inf])
    near(value.real, direct, "1e-65")
    digamma.append({"epsilon_over_B":s(t), "bound_sum_over_w1_div_B":s(value.real)})

# Source-state bound projection at leading weak dressing, with an infinite-tail bound.
N = 10000
sumN = mp.fsum(D(1)/n**3 for n in range(1,N+1))
tailLo = D(1)/(2*(N+1)**2)
tailHi = D(1)/(2*N**2)
assert sumN+tailLo < mp.zeta(3) < sumN+tailHi
Wlo = w1*mp.zeta(3)/(delta+B)**2
Whi = w1*mp.zeta(3)/delta**2
assert Wlo <= Whi
x_on_shell = mp.pi*alpha*mp.sqrt(m/delta)
Son = x_on_shell/(-mp.expm1(-x_on_shell))
near(Son-1, x_on_shell/2, "1e-40")

# Finite-cell and time-resolution diagnostics, without asserting formation.
T = D("1e18")
sizes = []
for Rm in [D("1"), D("1e22"), D("1e26"), c*T]:
    xx = Rm/(a*hbarc)
    # Accurate small-x integral, not subtracting nearly equal O(1) terms.
    prob = 4*xx**3*mp.quad(lambda y: y*y*mp.exp(-2*xx*y), [0,1])
    with mp.workdps(250):
        closed_prob = 1-mp.exp(-2*xx)*(1+2*xx+2*xx*xx)
    near(prob, closed_prob, "1e-65")
    sizes.append({"R_m":s(Rm),"R_over_aB":s(xx),"ground_pair_probability_inside_R":s(prob),"no_negative_Dirichlet_pair_energy_bound_applies":bool(xx<D(".5"))})

# Ground-state even form factor, independent radial integral at fixed kaB.
even = []
for ka in [D(".1"),D("1"),D("4")]:
    q = ka/2
    form = mp.quad(lambda x: 4*x*x*mp.exp(-2*x)*mp.sin(q*x)/(q*x), [0,1,10,100,mp.inf])
    near(form, (1+(ka/4)**2)**-2, "1e-65")
    even.append({"k_aB":s(ka),"mass_form_factor_over_2m":s(form),"odd_sine_source":s(mp.sin(ka/2)+mp.sin(-ka/2))})

result = {
 "outcome":"implementation and finite assertion verified in the stated range",
 "software":{"python":sys.version,"mpmath":mp.__version__,"decimal_precision":mp.mp.dps},
 "SI_inputs":{"G_m3_kg-1_s-2":s(G),"c_m_s":s(c),"eV_J":s(eVJ),"h_J_s":s(h)},
 "benchmark":{"m_eV":s(m),"M_eV":s(M),"delta_eV":s(delta),"g_eV":s(g),"lambda_rep":s(lam),"alpha_G":s(alpha),"aB_eV-1":s(a),"aB_m":s(a*hbarc),"B_eV":s(B),"c3_eV-1_2":s(c3),"bound_coupling_residue_n1_eV2":s(w1),"J_C_threshold_eV":s(J0),"source_bound_weight_lower":s(Wlo),"source_bound_weight_upper":s(Whi),"source_bound_weight_n1_leading":s(w1/(delta+B)**2),"Coulomb_S_minus_1_at_delta_NR":s(Son-1),"scattering_length_m":s(asct*hbarc),"a_s_over_aB":s(asct/a),"contact_relative_ground_shift_leading":s(4*asct/a),"binding_time_s":s(hbar/B),"ground_Kepler_period_s":s(mp.pi*hbar/B)},
 "age_diagnostic":{"declared_time_s":s(T),"hbar_over_T_eV":s(hbar/T),"formal_n_binding_resolution_max":s(mp.sqrt(B*T/hbar)),"formal_n_adjacent_resolution_max_asymptotic":s((2*B*T/hbar)**(D(1)/3)),"causal_radius_m":s(c*T)},
 "finite_size_diagnostics":sizes,"radial_checks":radial,"sommerfeld_checks":sommerfeld,"threshold_checks":threshold,"bound_digamma_checks":digamma,"even_form_checks":even,
 "finite_sum":{"N":N,"partial_zeta3":s(sumN),"remaining_tail_lower":s(tailLo),"remaining_tail_upper":s(tailHi)},
 "non_claims":["No formation calculation, thermal population, cosmic abundance, or universal normalization is established.","Coulomb residues use leading canonical short-distance source matching; contact/local-operator corrections need a regulator and matching.","Finite-cell no-binding bound applies to an explicitly confined Dirichlet relative coordinate, not to all free-space or many-body states.","A finite observation time does not remove exact mathematical eigenstates."]
}
OUT.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result["benchmark"],indent=2))
print("All declared finite checks passed.")
