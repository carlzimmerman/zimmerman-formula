"""k04: what the offset reading predicts in time, and how it sits on the record's two footings.

READING: rho_off = c a0^2/(8 pi G) is the dark energy, with c = c[mu] a constant of a time-independent mu (k01).
 A  conservation: if the offset is a separately conserved component then w_off = -1 + (2/3) d ln a0 / d ln(1+z).  A flat a0 <=> w = -1.
 B  the rival a0 = xi H(z) is INCOMPATIBLE with the offset being the dark energy: matter + offset with rho_off ~ H^2 is exactly Einstein-de Sitter
    (H ~ (1+z)^(3/2), q = +1/2, w_off = 0); the distance moduli miss LCDM by tenths of a mag (bookkeeping against the SN-Ia scale).
 C  the two footings of the record (rho_Lambda footing: a0 = kappa c sqrt(G rho_L), constant; rho_total footing: a0 = kappa c sqrt(G rho_crit(z))):
    c_req on each; on the rho_total footing the offset reading forces Omega_off(z) = c/(32 pi) = constant, contradicting Omega_Lambda(z).
 D  what a measurement of a0(z) at z ~ 2.5 would bound: |w_off + 1| from the precision of d ln a0/d ln(1+z).
 E  the reading's own assumption: the cosmic vacuum sits at g << a0 (estimate of the large-scale acceleration).
"""
import sys
import numpy as np
import sympy as sp
from scipy import integrate

OK = []


def chk(name, cond):
    OK.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name, flush=True)


c_light = 2.99792458e8
Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc
Om, OL = 0.315, 0.685
A0_SP = 1.1279e-10

# ------------------------------------------------------------------------------------------------ A
print("== A  conservation: w_off and the slope of a0(z)")
z, q = sp.symbols('z q', positive=True)
a0z = sp.Function('a0')(z)
rho_off = a0z ** 2                                         # rho_off = const * a0^2 (c, G fixed)
# continuity: d rho/d ln a + 3 (1+w) rho = 0 with ln a = -ln(1+z):  d rho/d ln(1+z) = 3 (1+w) rho
w_expr = sp.simplify(sp.diff(rho_off, z) * (1 + z) / (3 * rho_off) - 1)
chk("A1 w_off = -1 + (2/3) d ln a0/d ln(1+z) from continuity", sp.simplify(w_expr - (-1 + sp.Rational(2, 3) * (1 + z) * sp.diff(a0z, z) / a0z)) == 0)
w_pow = sp.simplify(w_expr.subs(a0z, (1 + z) ** q).doit())
chk("A2 for a0 ~ (1+z)^q: w_off = -1 + 2q/3 (q = 0 flat -> w = -1; q = 3/2 -> w = 0)", sp.simplify(w_pow - (-1 + 2 * q / 3)) == 0)
# for a0 = xi H(z) in matter domination H ~ (1+z)^(3/2): q = 3/2
chk("A3 MUTATION: if the offset had w = -1 with a0 rising as (1+z)^(3/2), continuity would be violated (rho_off ~ (1+z)^3 needs w = 0)", sp.simplify(w_pow.subs(q, sp.Rational(3, 2))) == 0)

# ------------------------------------------------------------------------------------------------ B
print("\n== B  a0 = xi H(z) with offset = dark energy is Einstein-de Sitter")
def E2_lcdm(zz):
    return Om * (1 + zz) ** 3 + OL
def DL_lcdm(zz):
    return (1 + zz) * integrate.quad(lambda t: 1 / np.sqrt(E2_lcdm(t)), 0, zz)[0]      # in units of c/H0
def DL_eds(zz):
    return 2 * (1 + zz) * (1 - 1 / np.sqrt(1 + zz))
# symbolic: matter + rho_off = kappa_o H^2 (kappa_o = 3 Omega_off/(8 pi G) const) => H^2 (1 - Omega_off) = (8 pi G/3) rho_m0 (1+z)^3
H0s, Oo, Om0 = sp.symbols('H0 Omega_off Omega_m0', positive=True)
Hz2 = sp.Symbol('Hz2', positive=True)
sol = sp.solve(sp.Eq(Hz2 * (1 - Oo), Om0 * H0s ** 2 * (1 + z) ** 3 / 1), Hz2)[0]
# with Omega_m0 = 1 - Omega_off today:  H(z)^2 = H0^2 (1+z)^3
chk("B1 with rho_off = Omega_off * 3H^2/(8 pi G) (Omega_off constant, from a0 ~ H) the expansion law is H^2 = H0^2 (1+z)^3 for ANY Omega_off (matter era forever)",
    sp.simplify(sol.subs(Om0, 1 - Oo) - H0s ** 2 * (1 + z) ** 3 / (1 - Oo) * (1 - Oo)) == 0)
# deceleration parameter q = -1 - d ln H/d ln(1+z)... for H ~ (1+z)^(3/2): q = 1/2
qdec = sp.simplify(-1 + (1 + z) * sp.diff(sp.log(sp.sqrt((1 + z) ** 3)), z))
chk("B2 deceleration parameter q = +1/2 at all z (no acceleration)", sp.simplify(qdec - sp.Rational(1, 2)) == 0)
rows = []
for zz in (0.1, 0.5, 1.0, 2.0):
    dm = 5 * np.log10(DL_eds(zz) / DL_lcdm(zz))
    rows.append((zz, dm))
    print(f"   z = {zz:3.1f}: D_L(EdS)/D_L(LCDM) -> distance-modulus offset {dm:+.3f} mag")
chk("B3 the induced distance moduli differ from LCDM (Omega_m = 0.315) by %.2f mag at z = 0.5 (SN-Ia distances constrain to ~0.02 mag): the offset-as-dark-energy reading with a0 ~ H(z) is excluded by the acceleration itself; a0 ~ H(z) is then a different world (no offset-dark-energy)" % abs(rows[1][1]),
    abs(rows[1][1]) > 0.2)
chk("B4 CONTROL: the same integration reproduces D_L(LCDM) -> EdS when Omega_m = 1 (distance modulus offset 0 at all z)",
    all(abs(5 * np.log10((1 + zz) * integrate.quad(lambda t: (1 + t) ** -1.5, 0, zz)[0] / DL_eds(zz))) < 1e-9 for zz in (0.1, 0.5, 2.0)))

# ------------------------------------------------------------------------------------------------ C
print("\n== C  the record's two footings")
rho_crit0_G = 3 * H0 ** 2 / (8 * np.pi)                     # G rho_crit0 in s^-2
a0_tot = 0.5 * c_light * np.sqrt(rho_crit0_G)               # kappa = 1/2 on rho_total: a0 = (1/2) c sqrt(G rho_crit0)
a0_L = 0.5 * c_light * np.sqrt(rho_crit0_G * OL)            # kappa = 1/2 on rho_Lambda
print(f"   a0(rho_total, kappa = 1/2) = {a0_tot:.4e} m/s^2 ; a0(rho_Lambda, kappa = 1/2) = {a0_L:.4e} ; SPARC-fitted = {A0_SP:.4e}")
chk("C1 on the rho_total footing a0 = (1/2) c sqrt(G rho_crit) = %.4e is within 0.5%% of the SPARC-fitted %.4e; on the rho_Lambda footing it is %.1f%% low" % (a0_tot, A0_SP, 100 * (1 - a0_L / A0_SP)),
    abs(a0_tot / A0_SP - 1) < 0.005 and 0.15 < 1 - a0_L / A0_SP < 0.2)
c_req_L = 32 * np.pi                                          # on the rho_Lambda footing the requirement is exactly 32 pi (k01 F1)
c_req_sp = 3 * OL * (c_light * H0 / A0_SP) ** 2
print(f"   offset reading, c_req: rho_Lambda footing (framework a0) = {c_req_L:.2f}; measured SPARC a0 = {c_req_sp:.2f}")
# rho_total footing + offset reading: rho_off/rho_tot = c/(32 pi) at every z
chk("C2 on the rho_total footing a0^2 = G rho_tot/4 the offset reading gives rho_off/rho_tot = c/(32 pi): a CONSTANT in time; for Omega_off(0) = Omega_Lambda = 0.685 it needs c = 32 pi Omega_L = %.1f (= c_req at the SPARC a0: %.1f)" % (32 * np.pi * OL, c_req_sp),
    abs(32 * np.pi * OL - c_req_sp) / c_req_sp < 0.01)
def OL_z(zz):
    return OL / (Om * (1 + zz) ** 3 + OL)
print("   Omega_Lambda(z) in LCDM: " + "  ".join(f"z={zz}: {OL_z(zz):.3f}" for zz in (0, 0.5, 1, 2, 3)))
chk("C3 LCDM's Omega_Lambda(z) is NOT constant (0.685 at z=0, %.3f at z=1, %.3f at z=2): the rho_total-footing offset (constant Omega_off) cannot be the dark energy" % (OL_z(1), OL_z(2)),
    OL_z(1) < 0.25 and OL_z(2) < 0.08)

# ------------------------------------------------------------------------------------------------ D
print("\n== D  what a0(z) precision buys (offset reading only)")
tab = []
for sig in (0.03, 0.10, 0.30):
    dw = (2 / 3) * np.log(1 + sig) / np.log(3.5)            # z = 2.5 vs z = 0: ln(1+z) = ln 3.5
    tab.append((sig, dw))
    print(f"   a0(2.5)/a0(0) known to {100*sig:3.0f}% -> |w_off + 1| <~ {dw:.3f}")
chk("D1 a 10%% measurement of a0(z=2.5)/a0(0) bounds |w_off + 1| to %.3f (a 30%% one to %.3f): the offset reading turns a0(z) into a dark-energy equation-of-state probe of SN-Ia strength only for percent-level a0(z)" % (tab[1][1], tab[2][1]),
    abs(tab[1][1] - 0.0508) < 0.001)

# ------------------------------------------------------------------------------------------------ E
print("\n== E  the reading's own assumption: the cosmic vacuum sits at g << a0")
g_lss = 0.5 * Om * H0 ** 2 * (10 * Mpc) * 1.0               # g ~ (4 pi G/3) rho_m delta R = (H0^2 Omega_m/2) delta R at R = 10 Mpc, delta ~ 1
print(f"   large-scale peculiar acceleration at R = 10 Mpc, delta ~ 1: g = {g_lss:.2e} m/s^2 = {g_lss / A0_SP:.1e} a0")
chk("E1 large-scale (10 Mpc, delta ~ 1) accelerations are ~%.0e a0: the volume-averaged offset sits at eps(g<<a0) ~ full value, so the reading is consistent on that count; only bound systems (g >~ a0) carry a reduced offset (k01 G3)" % (g_lss / A0_SP),
    g_lss / A0_SP < 0.01)

# ------------------------------------------------------------------------------------------------ F
print("\n== F  where each class of test sits in x = g/a0 (arithmetic; a0 = 1.1279e-10)")
GM_sun, AU, Msun, kpc, Gn = 1.32712440018e20, 1.495978707e11, 1.98847e30, 3.0856775814913673e19, 6.67430e-11
tests = {
    'Saturn (Cassini), solar field': GM_sun / (9.5826 * AU) ** 2,
    'Earth orbit, solar field': GM_sun / AU ** 2,
    'Milky Way at the Sun (v^2/R, 230 km/s, 8.2 kpc)': (230e3) ** 2 / (8.2 * kpc),
    'SPARC data (max)': 62.4 * A0_SP,
    'cluster baryons, 1.5e13 Msun at 500 kpc (Newtonian g_bar)': Gn * 1.5e13 * Msun / (500 * kpc) ** 2,
}
for k_, v_ in tests.items():
    print(f"   {k_:62s} g = {v_:.2e} m/s^2 = {v_ / A0_SP:9.3g} a0")
chk("F1 the tests sit at x ~ 0.05-1 (clusters), 1-60 (galaxies, SPARC) and >= 5e5 (Solar System): there is NO test between x ~ 60 and 5e5, and c gets its weight from that gap (k01 G, k02 D)",
    tests['cluster baryons, 1.5e13 Msun at 500 kpc (Newtonian g_bar)'] / A0_SP < 0.2 and tests['Saturn (Cassini), solar field'] / A0_SP > 5e5 and tests['SPARC data (max)'] / A0_SP < 70)

print(f"\n{sum(OK)}/{len(OK)} checks passed")
sys.exit(0 if all(OK) else 1)
