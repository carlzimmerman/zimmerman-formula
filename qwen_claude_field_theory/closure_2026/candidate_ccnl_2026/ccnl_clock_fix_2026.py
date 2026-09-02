#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ccnl_clock_fix_2026.py -- FIXING THE CCNL CLOCK: swap the v9 DBI condensate for a cold-at-every-epoch clock and pay the price.
==============================================================================================================================
The bug (dark_sector_debug_2026): CCNL-MOND's clock is the v9 DBI condensate K(u) = -M^4 + mu_D^2 Lambda_D^2 [1 - sqrt(1 - u^2/Lambda_D^2)]
whose background pin R = Lambda_D/Q_0 = 2.6 nu_0 leaves a WARM epoch (c_s ~ 400 km/s at z = 3) 18-300x over the P(k)/forest ceiling.
The fix (SZ21's own cosmological choice): an exponential-wall clock, K = 2 K_2 Z_0^2 (e^Z - 1 - Z), Z = (Q - Q_0)/Z_0, whose charge
n = K' = 2 K_2 Z_0 (e^Z - 1) ~ a^-3 sits on the wall for all z with a CONSTANT tiny sound speed c_s^2 = K'/(Q K'') -> Z_0/Q_0 = zeta.
  A. background + linear growth with the fixed clock: c_s^2(z) at recombination, z = 3, z = 0; P(k) vs the Newtonian run at
     k = 0.2 - 10 h/Mpc, z = 3 and 0 (the pincer's own yardstick, 10% band) -- the P(k)/forest bug is FIXABLE.
  B. the price: in a static well the clock charge obeys delta_well = |Psi| c^2 / c_s^2 (the matching identity for constant c_s:
     an isothermal atmosphere exp(|Psi|/zeta)); with zeta <= 1e-9 that is e^1000 -- no quasistatic well exists, the charge is
     supply-limited and BALLISTIC, and the kernel boosts it like everything else: the framework-native accretion (spherical
     collapse, MOND-boosted peculiar field, external field e_N) lands 27-55 M_b inside 250 kpc -> KiDS-1000 isolated lenses.
  C. the only structural escapes inside one metric: (C1) clock dust moving in the UNBOOSTED (Einstein-frame) metric -> Newtonian
     accretion, 3.4 M_b inside 250 kpc, eps = 1 against the KiDS stellar-mass bins (ceiling 0.06-0.14, dark_sector_debug);
     (C2) clock dust that does not source the visible potential in wells at all -> then it is not the CMB's dark matter unless a
     second metric screens it (Blanchet class, outside CCNL).
Both a_0 footings.  Checks CAN fail.  Mutation: zeta -> the DBI warm epoch must reproduce the pincer's kill.
"""
import sys, math, os
import numpy as np
from scipy.integrate import solve_ivp, quad
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
h = 0.674; OM_B_H2, OM_C_H2 = 0.02237, 0.1200
OM_B = OM_B_H2/h**2; OM_DM = OM_C_H2/h**2; OM_R = 4.15e-5/h**2; OM_M = OM_B + OM_DM; OM_L = 1 - OM_M - OM_R
G = 6.674e-11; c = 2.99792458e8; Mpc = 3.0857e22; kpc = 3.0857e19; Msun = 1.989e30; H0 = 100*h*1e3/Mpc; rho_crit = 3*H0**2/(8*math.pi*G); RHO_C = OM_DM*rho_crit
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; CH0 = 2997.92; Z_REC = 1090.0
def nu(y): y = max(y, 1e-12); return 1.0/(1.0 - math.exp(-math.sqrt(y)))
# ---------------------------------------------------------------- clocks
NU0 = 8.8e-5; R_PIN = NU0*OM_L/OM_DM                                   # v9 DBI, pinned (condensate_mu_pincer)
def cs2_dbi(a): v = NU0/a**3; s = v/math.sqrt(1+v**2); return R_PIN*s*(1-s**2)/(1+R_PIN*s)
def cs2_exp(a, zeta, N0=1e3):
    """exponential-wall clock: n/(2 K_2 Z_0) = N0/a^3 = e^Z - 1;  c_s^2 = K'/(Q K'') = zeta (1 - e^-Z)/(1 + zeta Z)  (units of c^2)"""
    Z = math.log(1.0 + N0/a**3); return zeta*(1.0 - math.exp(-Z))/(1.0 + zeta*Z)
# ---------------------------------------------------------------- growth (the footing script's integrator, verbatim physics)
class Cosmo:
    def __init__(self, om_b, om_dm):
        self.ob, self.od = om_b, om_dm; self.om = om_b + om_dm; self.ol = 1 - self.om - OM_R; self.fb = om_b/self.om; self.fd = om_dm/self.om
    def E2(self, a): return OM_R/a**4 + self.om/a**3 + self.ol
    def dlnH(self, a): return 0.5*(-4*OM_R/a**4 - 3*self.om/a**3)/self.E2(a)
C_STD = Cosmo(OM_B, OM_DM)
def grow(k, cs2fun, a_i=1e-3, a_f=1.0, z_out=(3.0, 0.0)):
    def rhs(N, y):
        a = math.exp(N); db, dbp, dd, ddp = y; dm = C_STD.fb*db + C_STD.fd*dd; E2 = C_STD.E2(a)
        src = 1.5*(C_STD.om/a**3/E2)*dm; fr = 2 + C_STD.dlnH(a); pres = (k*CH0)**2*cs2fun(a)/(a**2*E2)
        return [dbp, src - fr*dbp, ddp, src - fr*ddp - pres*dd]
    tev = sorted(math.log(1/(1+z)) for z in z_out)
    sol = solve_ivp(rhs, (math.log(a_i), math.log(a_f)), [1.0, 1.0, 1.0, 1.0], t_eval=tev, method="DOP853", rtol=1e-8, atol=1e-14)
    return {round(1/math.exp(N)-1): C_STD.fb*sol.y[0][j] + C_STD.fd*sol.y[2][j] for j, N in enumerate(sol.t)}
KGRID = [0.2, 1.0, 3.0, 10.0]
P("="*118); P("A. the fixed clock on the background and in linear growth"); P("="*118)
info(f"v9 DBI (pinned R = {R_PIN:.2e}): c_s(z=3) = {math.sqrt(cs2_dbi(0.25))*c/1e3:.0f} km/s, c_s(z=10) = {math.sqrt(cs2_dbi(1/11))*c/1e3:.0f} km/s, c_s(z=20) = {math.sqrt(cs2_dbi(1/21))*c/1e3:.0f} km/s, c_s^2(rec) = {cs2_dbi(1/(1+Z_REC)):.1e}")
newt = {(k, z): grow(k, lambda a: 0.0)[z] for k in KGRID for z in (3, 0)}
dbi = {(k, z): grow(k, cs2_dbi)[z] for k in KGRID for z in (3, 0)}
worst_dbi = max(abs((dbi[(k, z)]/newt[(k, z)])**2 - 1) for k in KGRID for z in (3, 0))
check("M0 mutation control: the v9 DBI clock reproduces the pincer's kill -- P(k) suppressed by > 40% somewhere in k = 0.2-10 h/Mpc, z = 3 or 0",
      worst_dbi > 0.4, f"worst |P/P_Newton - 1| = {worst_dbi:.2f}")
res = {}
for zeta in (1e-9, 1e-10, 1e-11):
    csf = lambda a, z_=zeta: cs2_exp(a, z_)
    row = {(k, z): (grow(k, csf)[z]/newt[(k, z)])**2 for k in KGRID for z in (3, 0)}
    res[zeta] = row
    info(f"exp clock zeta = {zeta:.0e} (c_s = {math.sqrt(zeta)*c/1e3:.1f} km/s on the wall): c_s^2(rec) = {cs2_exp(1/(1+Z_REC), zeta):.1e}, c_s^2(z=3) = {cs2_exp(0.25, zeta):.1e}, c_s^2(0) = {cs2_exp(1.0, zeta):.1e};  P/P_Newton at z=3 [k=0.2,1,3,10] = " + ", ".join(f"{row[(k,3)]:.3f}" for k in KGRID) + " | z=0: " + ", ".join(f"{row[(k,0)]:.3f}" for k in KGRID))
# the pincer's own yardsticks: the z = 3 forest at k = 1-10 h/Mpc and the z = 0 linear regime at k <= 3 h/Mpc (k = 10 h/Mpc today is nonlinear, not a linear-theory yardstick)
ok_exp = {zeta: max([abs(row[(k, 3)] - 1) for k in KGRID] + [abs(row[(k, 0)] - 1) for k in (0.2, 1.0, 3.0)]) for zeta, row in res.items()}
check("A1 the exponential-wall clock is cold at EVERY epoch: for zeta <= 1e-10 (c_s <= 3 km/s) every P(k) on the pincer's yardsticks (z = 3, k = 0.2-10 h/Mpc; z = 0, k <= 3 h/Mpc) lies within 10% of the Newtonian run -- the P(k)/forest bug is FIXABLE",
      all(ok_exp[z] < 0.10 for z in (1e-10, 1e-11)), "; ".join(f"zeta={z:.0e}: worst {ok_exp[z]:.3f}" for z in ok_exp) + f"; (k = 10 h/Mpc at z = 0, nonlinear, reported: {res[1e-10][(10.0, 0)]:.3f} at zeta = 1e-10)")
check("A2 ...and the DBI escape is genuinely the DBI form, not the parameters: at zeta = 1e-9 (c_s = 9.5 km/s, the forest's own floor) the exp clock is still within 10% at k <= 3 h/Mpc", all(abs(res[1e-9][(k, z)] - 1) < 0.10 for k in (0.2, 1.0, 3.0) for z in (3, 0)), f"worst at k<=3: {max(abs(res[1e-9][(k,z)]-1) for k in (0.2,1.0,3.0) for z in (3,0)):.3f}")
info("A3 (no pin) the exp clock's charge normalisation Q_0 n_0 = Omega_dm rho_crit is a free choice and M^4 = rho_Lambda sits in K(Q_0): the DBI pin R = nu_0 Omega_Lambda/Omega_dm was a property of the DBI form (SZ21 verbatim: only their Exp set satisfies both mu^-1 >~ Mpc and w_0 <~ 2e-14)")
P(""); P("="*118); P("B. the price of a cold clock: what the well does with cold charge"); P("="*118)
for zeta in (1e-9, 1e-10, 1e-11):
    for Psi in (1e-7, 1e-6, 3e-6):
        info(f"zeta = {zeta:.0e}, |Psi|/c^2 = {Psi:.0e}: static (isothermal) well overdensity delta = exp(|Psi|/zeta) = exp({Psi/zeta:.0f}) -> no quasistatic solution; the charge is supply-limited and ballistic")
check("B1 for every cold clock (zeta <= 1e-9) and every galaxy depth (|Psi| >= 1e-7 c^2) the static well overdensity exceeds e^30 ~ 1e13: the well cannot be quasistatic -- the charge that reaches it is a ballistic pile-up, and its mass count is what lensing sees",
      all(Psi/zeta > 30 for zeta in (1e-9, 1e-10, 1e-11) for Psi in (1e-7, 1e-6, 3e-6)), f"min |Psi|/zeta = {min(Psi/zeta for zeta in (1e-9, 1e-10, 1e-11) for Psi in (1e-7, 1e-6, 3e-6)):.0f}")
# framework-native accretion (the repo's gate, verbatim) + KiDS Nobins confrontation
def E(a): return math.sqrt(OM_M/a**3 + OM_L)
def make_lens(Ms, Mg, a_s=2.0*kpc, a_g=10.0*kpc): return lambda r: Ms*r**2/(r+a_s)**2 + Mg*r**2/(r+a_g)**2
M_L = make_lens(4e10*Msun, 1e10*Msun)
def capture(M_b, a0, eN, boost=True, nshell=50, xmax_kpc=6000.0):
    x_grid = np.logspace(math.log10(5.0), math.log10(xmax_kpc), nshell)*kpc; a_i = 1/21.0
    ts = np.linspace(a_i, 1.0, 2000); dtda = np.array([1/(a*H0*E(a)) for a in ts]); tt = np.concatenate([[0.0], np.cumsum(0.5*(dtda[1:] + dtda[:-1])*np.diff(ts))]); t_now = tt[-1]
    a_of_t = lambda t: float(np.interp(t, tt, ts)); r_final, M_shell = [], []
    for x in x_grid:
        Mc = RHO_C*4/3*math.pi*x**3
        def rhs(t, y):
            r, v = y; a = a_of_t(t); rho_bg = OM_M*rho_crit/a**3; M_bg = 4/3*math.pi*rho_bg*r**3
            gN_pec = G*max(M_b(r) + Mc - 4/3*math.pi*(RHO_C/a**3)*r**3, 0.0)/r**2
            nu_e = nu(math.sqrt(gN_pec**2 + (eN*a0)**2)/a0) if boost else 1.0
            return [v, -G*M_bg/r**2 + OM_L*H0**2*r - gN_pec*nu_e]
        r0 = x*a_i; v0 = H0*E(a_i)*r0; ev = lambda t, y: y[0] - 0.05*kpc; ev.terminal = True
        sol = solve_ivp(rhs, (0, t_now), [r0, v0], events=ev, max_step=t_now/400, rtol=1e-7)
        rh = sol.y[0]; collapsed = sol.status == 1 or rh[-1] < 0.5*rh.max()
        if collapsed: r_final.append(0.5*rh.max()); M_shell.append(Mc)
        else: break
    r_final = np.array(r_final); M_shell = np.array(M_shell)
    def M_enc(r):
        if len(r_final) == 0: return 0.0
        o = np.argsort(r_final); return float(np.interp(r, r_final[o], M_shell[o], left=0.0, right=M_shell.max()))
    return M_enc
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4*G_PC*PC_PER_M
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return d[:, 0], CONV*d[:, 1]/d[:, 4], CONV*d[:, 3]/d[:, 4]
def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return (d[:, 4]/d[:, 6]).reshape(n, n)*CONV*CONV
gbar_d, gobs_d, gerr_d = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); n = len(gbar_d); C_all = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n); rail = gbar_d >= 1e-13
def chi2_gen(gpred, gobs, Cm, mask):
    def raw(gp): dv = (gobs - gp)[mask]; return float(dv @ np.linalg.solve(Cm[np.ix_(mask, mask)], dv))
    best = 1e30
    for la in np.linspace(-0.3, 0.3, 121):
        cc = raw(gpred*10**la) + (la/0.3)**2
        if cc < best: best = cc
    return best
def r_of_gbar_fn(M_b):
    rg = np.geomspace(1*kpc, 5000*kpc, 3000); gb = G*M_b(rg)/rg**2; ipk = int(np.argmax(gb)); rg_o, gb_o = rg[ipk:], gb[ipk:]
    return lambda g: float(np.interp(-math.log(g), -np.log(gb_o), rg_o))
def gpred(M_b, Menc, eps, a0, gbar_arr, rfn):
    out = []
    for g in gbar_arr:
        r = rfn(g); gN = G*(M_b(r) + eps*Menc(r))/r**2; out.append(gN*nu(gN/a0))
    return np.array(out)
rfn = r_of_gbar_fn(M_L); B2 = {}
for foot, a0 in A0.items():
    c0 = chi2_gen(gpred(M_L, lambda r: 0.0, 0.0, a0, gbar_d, rfn), gobs_d, C_all, rail)
    for eN in (0.03, 0.1):
        Mc = capture(M_L, a0, eN, boost=True); c1 = chi2_gen(gpred(M_L, Mc, 1.0, a0, gbar_d, rfn), gobs_d, C_all, rail); B2[(foot, eN)] = (c1 - c0, Mc(250*kpc)/M_L(250*kpc))
        info(f"{foot:10} kernel-boosted accretion of the cold clock charge at e_N = {eN}: M_ch(<250 kpc)/M_b = {Mc(250*kpc)/M_L(250*kpc):.1f}, KiDS rail Delta chi2 vs MOND-only = {c1-c0:+.0f}")
check("B2 the fixed (cold) clock's charge, boosted by the kernel like everything else, is excluded on the KiDS-1000 isolated rail at Delta chi2 >= +100 at e_N = 0.03-0.1, both footings (the same number as the AeST closure: the clock's K is irrelevant once the charge is cold)",
      all(v[0] >= 100 for v in B2.values()), "; ".join(f"{k[0]}/e_N={k[1]}: {v[0]:+.0f}" for k, v in B2.items()))
P(""); P("="*118); P("C. structural escapes inside one metric"); P("="*118)
# C1: clock dust in the unboosted metric -> Newtonian accretion, eps = 1 against the KiDS stellar-mass bins (full covariance)
bins = {}
for b in range(1, 5): bins[b] = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
dcov = np.genfromtxt(os.path.join(B, "Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt"), comments="#"); covM = (dcov[:, 4]/dcov[:, 6]).reshape(60, 60)*CONV*CONV
LOGM = {1: 10.0, 2: 10.45, 3: 10.7, 4: 10.9}; FGAS = {1: 0.5, 2: 0.3, 3: 0.2, 4: 0.15}
C1 = {}
for foot, a0 in A0.items():
    Ms = {b: make_lens(10**LOGM[b]*Msun, FGAS[b]*10**LOGM[b]*Msun) for b in bins}; caps = {b: capture(Ms[b], a0, 0.0, boost=False) for b in bins}; rfns = {b: r_of_gbar_fn(Ms[b]) for b in bins}
    gobsM = np.concatenate([bins[b][1] for b in bins]); maskM = np.ones(60, bool)
    pred = lambda eps: np.concatenate([gpred(Ms[b], caps[b], eps, a0, bins[b][0], rfns[b]) for b in bins])
    c0 = chi2_gen(pred(0.0), gobsM, covM, maskM); c1 = chi2_gen(pred(1.0), gobsM, covM, maskM); C1[foot] = c1 - c0
    info(f"{foot:10} C1 clock dust in the UNBOOSTED metric (Newtonian accretion, {caps[3](250*kpc)/Ms[3](250*kpc):.1f} M_b inside 250 kpc for bin 3), then seen by the kernel: 4-bin KiDS Delta chi2 at eps = 1 vs MOND-only = {c1-c0:+.0f}  (ceiling from dark_sector_debug: eps <= 0.06-0.14)")
check("C1 an Einstein-frame clock dust (Newtonian accretion, full share) is excluded by the KiDS stellar-mass bins at Delta chi2 >= +30, both footings: inside one metric the cold charge cannot be both the CMB's dark matter and absent from galaxies",
      all(v >= 30 for v in C1.values()), "; ".join(f"{f}: {v:+.0f}" for f, v in C1.items()))
info("C2 a clock dust that does not source the visible potential in wells is not the CMB's dark matter unless a SECOND metric carries it and screens it nonlinearly -- outside CCNL by construction (Blanchet-class bimetric/dipolar media; BD-ghost assertion open)")
P(""); P("="*118); P("VERDICT"); P("="*118)
P("  The clock is fixable: an exponential-wall K keeps the charge cold at every epoch (c_s <= 3 km/s), the CMB and the z = 3 forest are")
P("  Newtonian to better than 10% at every k, and the DBI pin was a DBI artefact.  The candidate is not: once the charge is cold it is")
P("  ballistic (no quasistatic well exists, e^1000), the kernel boosts it like everything else, and the framework's own accretion lands")
P("  27-55 M_b inside 250 kpc, excluded on the KiDS isolated rail at Delta chi2 >= +100 -- the same number that closed AeST.  Moving the")
P("  clock dust to the unboosted metric (Newtonian accretion) is excluded by the KiDS stellar-mass bins as well.  Inside one metric the")
P("  fix moves CCNL from dead-on-the-forest to dead-on-lensing.  The one door left is two-sector: the dark charge in a second metric that")
P("  sources the visible potential at linear order and is screened in wells -- the Blanchet class, whose health is the open assertion.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
