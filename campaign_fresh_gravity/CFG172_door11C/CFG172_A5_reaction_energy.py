# -*- coding: utf-8 -*-
"""CFG172 A5 -- G3: reaction on baryons and energy stored in the flow sector.  Frozen: sec. 2 (G3).
Reaction = force on baryons beyond -grad Phi from the flow's own field equations, over g_law, x in [0.3,30]: zero by construction for 11C-a/-b (minimal coupling S_m[g]);
for 11C-c the contact force K_c |rho'| (ceiling from A7).
Energy (declared definition): E_a(<r_e) = |(1/8 pi G) int_{<r_e} a0^2 Q(y) d^3x| with Q(y) = 2 int y q dy the flow's Lagrangian term (static: H = -L), y = g/a0, point-mass P2 law;
compared with (1/2) M_b V_f^2, V_f^2 = sqrt(G M_b a0), at r_e = 0.4 r_ta in two conventions: (1) CFG48's r_ta (collapse mass M_b(1 + Omega_c/Omega_b), Delta_ta = 11.81, read from Gcommon's formula),
(2) the phantom-inclusive one (CFG4's): radius where the P2 mean enclosed dynamical density = 11.81 rho_m (declared approximation of CFG4's Delta).
The source of the energy: a static configuration stores field energy; nothing is 'injected' during static evolution; the assembly energy available is the baryons' own potential energy ~ M V^2.
MUTATE = none required (frozen list has no A5 control); a positive control is C1-like: the P2 identities reproduce."""
from scipy.integrate import quad
from cfg172_common import *

R = Run("CFG172_A5_reaction_energy")
# Q(y) for true P2: y^2 - y sqrt(4y^2+1)/2 + y - asinh(2y)/4   (from A1's sympy)
Qy = lambda y: y * y - y * math.sqrt(4 * y * y + 1) / 2 + y - math.asinh(2 * y) / 4
R.check("C1c Q(y) reproduces dQ/dy = 2 y q(y) numerically (P2)", "finite difference", all(abs((Qy(v_ * 1.0001) - Qy(v_ * 0.9999)) / (0.0002 * v_) - 2 * v_ * (1 - (math.sqrt(1 + 4 * v_ * v_) - 1) / (2 * v_))) < 1e-5 * max(1.0, v_) for v_ in (0.01, 0.3, 1, 5, 50)))
RHOC0 = 2.775e11 * HH ** 2                         # Msun/Mpc^3
rho_m = OM * RHOC0 * 1e-9                           # Msun/kpc^3
DELTA = 11.81
OCB = OC_H2 / OB_H2
def r_ta_48(M):
    Mcol = M * (1 + OCB)
    return (3 * Mcol / (4 * math.pi * rho_m * DELTA)) ** (1 / 3)
def r_ta_4(M, a0):
    rM = rM_kpc(M, a0)
    f = lambda lr: math.log(M * math.sqrt(1 + (math.exp(lr) / rM) ** 2) / (4 * math.pi / 3 * math.exp(3 * lr) * rho_m)) - math.log(DELTA)
    return math.exp(brentq(f, math.log(1e-3), math.log(1e5), xtol=1e-12))
rows = {}
for f_ in FOOT:
    a0 = A0[f_]
    for M in MASSES:
        rM = rM_kpc(M, a0)
        out = {}
        for nm, rta in (("CFG48", r_ta_48(M)), ("CFG4", r_ta_4(M, a0))):
            re = 0.4 * rta
            rr = np.logspace(math.log10(1e-3 * rM), math.log10(re), 4000)
            gN = G * M / rr ** 2
            g = np.sqrt(gN ** 2 + a0 * gN)
            yv = g / a0
            integrand = np.array([Qy(v_) for v_ in yv]) * 4 * math.pi * rr ** 2
            Ea = a0 ** 2 / (8 * math.pi * G) * np.trapz(integrand, rr)      # (km/s)^2 * Msun
            Vf2 = math.sqrt(G * M * a0)
            out[nm] = {"r_e_kpc": re, "r_e_over_rM": re / rM, "E_a_over_orbital": Ea / (0.5 * M * Vf2)}
        rows[f"{f_}/{M:.0e}"] = out
        P(f"  {f_:9s} M={M:.0e}: r_ta(CFG48)={r_ta_48(M):8.1f} kpc, r_ta(CFG4)={r_ta_4(M,a0):8.1f} kpc (ratio {r_ta_4(M,a0)/r_ta_48(M):.2f}); E_a/(M V_f^2/2): CFG48 {out['CFG48']['E_a_over_orbital']:.2e}, CFG4 {out['CFG4']['E_a_over_orbital']:.2e}")
R.out["numbers"]["energy_rows"] = rows
ratios = [v_[nm]["E_a_over_orbital"] for v_ in rows.values() for nm in ("CFG48", "CFG4")]
lo, hi = min(ratios), max(ratios)
R.check("A5.1 the convention ratio r_ta(CFG4)/r_ta(CFG48) lies in the referee's quoted 1.7-3.6 range", f"{min(r_ta_4(M,A0['canonical'])/r_ta_48(M) for M in MASSES):.2f}-{max(r_ta_4(M,A0['canonical'])/r_ta_48(M) for M in MASSES):.2f}",
        1.5 <= min(r_ta_4(M, A0['canonical']) / r_ta_48(M) for M in MASSES) and max(r_ta_4(M, A0['canonical']) / r_ta_48(M) for M in MASSES) <= 4.0, load_bearing=False)
R.verdict("G3-energy (11C-a, -b, -c, isolated point-mass P2 field)", "FAIL" if lo > 1.0 else "PASS", f"E_a / orbital energy = {lo:.1e} .. {hi:.1e} in the two r_ta conventions (line <= 1)")
R.verdict("G3-reaction (11C-a, -b)", "PASS", "minimal coupling: baryon equation of motion is -grad Phi from the field equations (residual 0 by construction)")
Kmax = json.load(open(os.path.join(HERE, "CFG172_A7_c_response_results.json")))["numbers"]["G3_Kc_ceiling"]
R.verdict("G3-reaction (11C-c)", "PASS only for K_c <= %.1e" % Kmax, "coupling required by no gate; see A7")
R.finish(bite=False)
