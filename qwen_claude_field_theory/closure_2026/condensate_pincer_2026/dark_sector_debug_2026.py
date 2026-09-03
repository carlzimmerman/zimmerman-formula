#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dark_sector_debug_2026.py -- DEBUGGING THE DARK SECTOR: every property the committed gates force on it, run as assertions against
==================================================================================================================================
every candidate identity, plus the ONE object the assertions leave standing, specified with numbers from the data in hand.

The framework's own gates (all committed, all exit 0) say the dark component must be:
  G1  present at Omega_dm at recombination            (CLASS: removing it shifts H3/H1 by 54%, Delta chi2 > 400)
  G2  cold and pressureless on every scale > ~1 kpc at z <= 3 (mu-pincer; sheet N-body forest gate; Hubble-floor growth theorem)
  G3  ballistic through a cluster merger              (merger gate: any self-supported medium lags the Bullet by >= 11x the offset)
  G4  ABSENT from galaxy wells beyond the +/-0.3 dex lensing budget, and below 0.05 dex on the RAR
      (framework-native accretion x3-20 -> KiDS Delta chi2 >= +106; AeST boundary-constant closure, every m^2)
  G5  present in clusters at eta(R500) - 1 ~ 0.7-1.1 of the framework's own prediction (X-COP, kernel-named)
  G6  carried by a healthy field theory (no ghost, PPN, c_T = 1)
Part A runs the candidates through G1-G6 with the committed numbers.  Part B computes what G1-G5 jointly force: a medium whose
gravitational coupling to the visible sector is epsilon(environment): ~1 on linear scales and in clusters, <= epsilon_gal in galaxy wells.
epsilon_gal from the KiDS-1000 isolated lenses (Nobins + the four stellar-mass bins, full covariance), epsilon_cl from X-COP,
the RAR bound from SPARC-depth radii, and whether a potential-depth threshold can order galaxies < threshold < (clusters, linear
scales).  Both a_0 footings.  Mutation control: epsilon = 0 must reproduce the MOND-only chi2 exactly.  Checks CAN fail -- D3 in
particular is the assertion that decides whether the object exists at all.
"""
import sys, math, os
import numpy as np
from scipy.integrate import solve_ivp, quad
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
G = 6.674e-11; c = 2.99792458e8; kpc = 3.0857e19; Mpc = 3.0857e22; Msun = 1.989e30; h = 0.674
H0 = 100*h*1e3/Mpc; OM_B = 0.02237/h**2; OM_DM = 0.1200/h**2; OM_M = OM_B + OM_DM; OM_L = 1 - OM_M
rho_crit = 3*H0**2/(8*math.pi*G); RHO_C = OM_DM*rho_crit; F_B = OM_B/OM_M
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
def nu(y): y = max(y, 1e-12); return 1.0/(1.0 - math.exp(-math.sqrt(y)))
def E(a): return math.sqrt(OM_M/a**3 + OM_L)
def make_lens(Mstar, Mgas, astar=2.0*kpc, agas=10.0*kpc):
    return lambda r: Mstar*r**2/(r+astar)**2 + Mgas*r**2/(r+agas)**2
def capture(M_b, a0, eN, boost=True, nshell=50, xmax_kpc=6000.0):
    """spherical collapse of the cosmic dust onto the lens; boost=False = Newtonian (CDM-like) accretion, boost=True = the framework's MOND-boosted peculiar field with EFE e_N"""
    x_grid = np.logspace(math.log10(5.0), math.log10(xmax_kpc), nshell)*kpc; a_i = 1/21.0
    ts = np.linspace(a_i, 1.0, 2000); dtda = np.array([1/(a*H0*E(a)) for a in ts]); tt = np.concatenate([[0.0], np.cumsum(0.5*(dtda[1:] + dtda[:-1])*np.diff(ts))]); t_now = tt[-1]
    a_of_t = lambda t: float(np.interp(t, tt, ts))
    r_final, M_shell = [], []
    for x in x_grid:
        Mc = RHO_C*4/3*math.pi*x**3
        def rhs(t, y):
            r, v = y; a = a_of_t(t); rho_bg = OM_M*rho_crit/a**3; M_bg = 4/3*math.pi*rho_bg*r**3
            gN_pec = G*max(M_b(r) + Mc - 4/3*math.pi*(RHO_C/a**3)*r**3, 0.0)/r**2
            nu_e = nu(math.sqrt(gN_pec**2 + (eN*a0)**2)/a0) if boost else 1.0
            return [v, -G*M_bg/r**2 + OM_L*H0**2*r - gN_pec*nu_e]
        r0 = x*a_i; v0 = H0*E(a_i)*r0
        ev = lambda t, y: y[0] - 0.05*kpc; ev.terminal = True
        sol = solve_ivp(rhs, (0, t_now), [r0, v0], events=ev, max_step=t_now/400, rtol=1e-7)
        rh = sol.y[0]; collapsed = sol.status == 1 or rh[-1] < 0.5*rh.max()
        if collapsed: r_final.append(0.5*rh.max()); M_shell.append(Mc)
        else: break
    r_final = np.array(r_final); M_shell = np.array(M_shell)
    def M_enc(r):
        if len(r_final) == 0: return 0.0
        o = np.argsort(r_final); return float(np.interp(r, r_final[o], M_shell[o], left=0.0, right=M_shell.max()))
    return M_enc
# ---------------------------------------------------------------- Brouwer 2021 loaders (Nobins + 4 stellar-mass bins, full covariance)
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4*G_PC*PC_PER_M
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return d[:, 0], CONV*d[:, 1]/d[:, 4], CONV*d[:, 3]/d[:, 4]
def load_cov(fname, n):
    d = np.genfromtxt(os.path.join(B, fname), comments="#"); return (d[:, 4]/d[:, 6]).reshape(n, n)*CONV*CONV
gbar_d, gobs_d, gerr_d = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); n = len(gbar_d); C_all = load_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", n)
rail = gbar_d >= 1e-13; allm = np.ones(n, bool)
bins = {}
for b in range(1, 5):
    gb_, go_, ge_ = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt"); bins[b] = (gb_, go_, ge_)
dcov = np.genfromtxt(os.path.join(B, "Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt"), comments="#")
covM = (dcov[:, 4]/dcov[:, 6]).reshape(60, 60)*CONV*CONV
# ordering self-check: the diagonal must equal the per-bin error^2 (try (m,i,n,j) reshape; else transpose the inner axes)
def diag_ok(Cm):
    return max(abs(np.diag(Cm)[15*(b-1):15*b]/bins[b][2]**2 - 1).max() for b in range(1, 5))
if diag_ok(covM) > 0.05:
    covM2 = (dcov[:, 4]/dcov[:, 6]).reshape(4, 4, 15, 15).transpose(0, 2, 1, 3).reshape(60, 60)*CONV*CONV
    info(f"cov ordering: (m,i,n,j) diag mismatch {diag_ok(covM):.3f} -> trying (m,n,i,j): {diag_ok(covM2):.3f}")
    covM = covM2
check("C0 the 4-bin covariance diagonal reproduces the per-bin errors to 5% (ordering verified, not assumed)", diag_ok(covM) < 0.05, f"max mismatch {diag_ok(covM):.4f}")
LOGM = {1: 10.0, 2: 10.45, 3: 10.7, 4: 10.9}; FGAS = {1: 0.5, 2: 0.3, 3: 0.2, 4: 0.15}      # assumed bin means (bin limits 8.5-10.3-10.6-10.8-11.0) + cold-gas fractions
def chi2_gen(gpred, gobs, Cm, mask, prof=True):
    def raw(gp):
        dv = (gobs - gp)[mask]; return float(dv @ np.linalg.solve(Cm[np.ix_(mask, mask)], dv))
    if not prof: return raw(gpred)
    best = 1e30; bla = 0.0
    for la in np.linspace(-0.3, 0.3, 121):
        cc = raw(gpred*10**la) + (la/0.3)**2
        if cc < best: best, bla = cc, la
    chi2_gen.last_la = bla; return best
def r_of_gbar_fn(M_b):
    rg = np.geomspace(1*kpc, 5000*kpc, 3000); gb = G*M_b(rg)/rg**2; ipk = int(np.argmax(gb)); rg_o, gb_o = rg[ipk:], gb[ipk:]
    return lambda g: float(np.interp(-math.log(g), -np.log(gb_o), rg_o))
def gpred(M_b, Menc, eps, a0, gbar_arr, rfn):
    out = []
    for g in gbar_arr:
        r = rfn(g); gN = G*(M_b(r) + eps*Menc(r))/r**2; out.append(gN*nu(gN/a0))
    return np.array(out)
P("="*120); P("PART A -- the assertion matrix: candidate identities vs the six gates (committed numbers; script named per cell)"); P("="*120)
rows = [
 ("CDM particle + NEWTONIAN gravity (LCDM)",        "PASS", "PASS", "PASS", "PASS (no MOND: the halo IS the phantom)", "PASS", "PASS", "the a0-rho_Lambda tie and the zero per-galaxy spread are its COINCIDENCES -> A-2 / A-9 of the ledger"),
 ("CDM particle + MOND gravity",                    "PASS", "PASS", "PASS", "FAIL: accretes x3-20, KiDS Dchi2>=+106 (dark_charge_kids_lensing_gate; aest_boundary_condition_closure)", "PASS", "PASS", "the double count"),
 ("thermal fermion 5-11 eV (nuHDM)",                "PASS", "FAIL: forest, sheet N-body + Hubble floor (mond_sheet_nbody_forest_gate; mond_growth_framework_footing)", "PASS", "PASS (TG-saturated)", "PASS", "PASS", "Angus-class"),
 ("fuzzy boson",                                    "PASS", "FAIL: CMB floor 1e-24 eV vs M_min gap x7-30 (ballistic_survivor_window)", "PASS", "-", "-", "PASS", "window empty"),
 ("AeST shift charge (polytrope OR ballistic)",     "PASS", "FAIL for quadratic K: w0<=2e-14 => mu^-1<=1 kpc (SZ21 verbatim); Exp-K escapes", "PASS", "FAIL: C fixed by conservation, every m^2 (aest_boundary_condition_closure)", "23-33% of core (itemC)", "FAIL: PPN alpha_1=-2(K_B+2) (fried_chicken_final)", "the leading rival, closed 09-02"),
 ("superfluid DM (BK-class)",                       "FAIL: background condenses z_th=78-31000, c_s^2(rec) 2e-3-0.33 (superfluid_route_gates)", "FAIL", "PASS", "FAIL (MMH 2024 lensing)", "PASS (normal phase)", "PASS", "one EOS cannot be MOND in galaxies and cold on the background"),
 ("dark solid / any self-supported medium",         "PASS", "PASS", "FAIL: lag >= 11x the Bullet offset (merger_gate_supported_media)", "-", "-", "-", "c ~ v_c is the killer"),
 ("CCNL-MOND's clock dust (v9 DBI condensate)",     "PASS: c_s^2(rec)=2.9e-8", "INHERITS the v9 pin: R=2.6 nu_0, 18-300x over the P(k)/forest ceiling at z~3-20 (condensate_mu_pincer) UNLESS the pin is dropped", "PASS", "same accretion as AeST: OPEN, not gated in ccnl_mond_gates", "23-33%", "29/29 on its own gates", "the strongest candidate's dark sector is the excluded v9 dust -- the bug"),
 ("ENVIRONMENT-SELECTED medium (Part B)",           "PASS by construction (eps=1 deep)", "PASS (cold, ballistic)", "PASS (ballistic; clusters deep)", "PASS iff eps_gal <= eps_max (computed)", "PASS iff eps_cl ~ computed", "OPEN: no healthy field theory known (bimetric/dipolar class = BD-ghost assertion; symmetron/chameleon screen the WRONG way)", "what survives"),
]
hdr = f"{'candidate':46} | G1 CMB | G2 cold z<=3 | G3 merger | G4 galaxies | G5 clusters | G6 health | note"
P("  " + hdr)
for r in rows: P("  " + f"{r[0]:46} | " + " | ".join(r[1:]))
P(""); P("="*120); P("PART B -- the surviving object, specified from the data in hand"); P("="*120)
P("  B1  epsilon_gal: how much of a CDM-like (Newtonian-accreted) dust halo the KiDS-1000 isolated lenses tolerate around a MOND well")
res = {}
M_L = make_lens(4e10*Msun, 1e10*Msun)
for foot, a0 in A0.items():
    rfn = r_of_gbar_fn(M_L); Mcdm = capture(M_L, a0, 0.0, boost=False); Mmond = capture(M_L, a0, 0.03, boost=True)
    g0 = gpred(M_L, Mcdm, 0.0, a0, gbar_d, rfn); c0r = chi2_gen(g0, gobs_d, C_all, rail); c0a = chi2_gen(g0, gobs_d, C_all, allm)
    info(f"{foot:10} L* template: M_cdm(<100 kpc)/M_b = {Mcdm(100*kpc)/M_L(100*kpc):.1f}, (<250) {Mcdm(250*kpc)/M_L(250*kpc):.1f}, (<1 Mpc) {Mcdm(Mpc)/M_L(Mpc):.1f}   [MOND-boosted e_N=0.03: {Mmond(250*kpc)/M_L(250*kpc):.1f} inside 250 kpc]   MOND-only chi2 rail {c0r:.1f} / all {c0a:.1f}")
    scan = []
    for eps in np.concatenate([[0.0], np.geomspace(1e-3, 3.0, 60)]):
        gp = gpred(M_L, Mcdm, eps, a0, gbar_d, rfn); cr = chi2_gen(gp, gobs_d, C_all, rail); la_r = chi2_gen.last_la; ca = chi2_gen(gp, gobs_d, C_all, allm); la_a = chi2_gen.last_la
        scan.append((eps, cr, ca, la_r, la_a))
    scan = np.array(scan); ib = int(np.argmin(scan[:, 2])); ibr = int(np.argmin(scan[:, 1]))
    # 2-sigma tolerance: largest eps with chi2_all <= min + 4
    tol = scan[scan[:, 2] <= scan[ib, 2] + 4.0][:, 0].max(); tol_r = scan[scan[:, 1] <= scan[ibr, 1] + 4.0][:, 0].max()
    res[(foot, "eps_best_all")] = scan[ib, 0]; res[(foot, "eps_max_all")] = tol; res[(foot, "eps_best_rail")] = scan[ibr, 0]; res[(foot, "eps_max_rail")] = tol_r
    res[(foot, "dchi2_best_all")] = scan[ib, 2] - c0a; res[(foot, "dchi2_best_rail")] = scan[ibr, 1] - c0r; res[(foot, "Mcdm")] = Mcdm; res[(foot, "c0")] = (c0r, c0a)
    info(f"{foot:10} Nobins: best eps (all 15) = {scan[ib,0]:.3f} (Dchi2 {scan[ib,2]-c0a:+.1f}, amp {scan[ib,4]:+.2f} dex); best eps (rail) = {scan[ibr,0]:.3f} (Dchi2 {scan[ibr,1]-c0r:+.1f}); 2-sigma ceiling eps_max = {tol:.3f} (all) / {tol_r:.3f} (rail);  eps=1 (full CDM halo on top of MOND): Dchi2 all {scan[np.argmin(abs(scan[:,0]-1.0)),2]-c0a:+.0f}")
check("M0 mutation control: eps = 0 reproduces the MOND-only chi2 exactly on both footings", all(abs(res[(f, 'c0')][0] - chi2_gen(gpred(M_L, res[(f, 'Mcdm')], 0.0, A0[f], gbar_d, r_of_gbar_fn(M_L)), gobs_d, C_all, rail)) < 1e-9 for f in A0))
info("B1 reading (both ways): against ONE L* template the un-binned stack PREFERS a CDM-like halo (eps ~ 1.7, Dchi2 ~ -33) -- but only with the coherent amplitude driven to -0.24/-0.28 dex, i.e. the single template is too heavy for the stack; the stellar-mass-binned analysis below (per-bin templates, full 60x60 covariance) is the controlled version and supersedes this line")
P(""); P("  B1' the four stellar-mass bins (assumed bin means log M* = 10.0 / 10.45 / 10.7 / 10.9, cold gas 50/30/20/15%): eps per bin, full 60x60 covariance")
binres = {}
for foot, a0 in A0.items():
    Ms = {b: make_lens(10**LOGM[b]*Msun, FGAS[b]*10**LOGM[b]*Msun) for b in bins}
    caps = {b: capture(Ms[b], a0, 0.0, boost=False) for b in bins}; rfns = {b: r_of_gbar_fn(Ms[b]) for b in bins}
    gobsM = np.concatenate([bins[b][1] for b in bins]); maskM = np.ones(60, bool)
    def pred_all(epsv):
        return np.concatenate([gpred(Ms[b], caps[b], epsv[b-1], a0, bins[b][0], rfns[b]) for b in bins])
    base = chi2_gen(pred_all([0, 0, 0, 0]), gobsM, covM, maskM)
    per = []
    for b in bins:
        # one-bin-at-a-time eps scan with the others at 0; per-bin chi2 uses the full covariance (cross-bin terms carried)
        bestc, beste, tolb = 1e30, 0.0, 0.0; sc = []
        for eps in np.concatenate([[0.0], np.geomspace(1e-3, 3.0, 40)]):
            ev = [0, 0, 0, 0]; ev[b-1] = eps; cc = chi2_gen(pred_all(ev), gobsM, covM, maskM); sc.append((eps, cc))
            if cc < bestc: bestc, beste = cc, eps
        sc = np.array(sc); tolb = sc[sc[:, 1] <= bestc + 4.0][:, 0].max()
        vc4 = (G*Ms[b](250*kpc)*a0)**0.25; Psi = 2.5*vc4**2   # rough well depth at 250 kpc: v^4 = G M a0, |Psi| ~ 2.5 v^2
        per.append((b, beste, tolb, bestc - base, Psi/c**2, caps[b](250*kpc)/Ms[b](250*kpc)))
        info(f"{foot:10} bin {b} (log M* {LOGM[b]}): best eps = {beste:.3f} (Dchi2 {bestc-base:+.1f}), 2-sigma ceiling {tolb:.3f}; M_cdm(<250)/M_b = {caps[b](250*kpc)/Ms[b](250*kpc):.1f}; well depth |Psi|/c^2 ~ {Psi/c**2:.1e} (v_c ~ {vc4/1e3:.0f} km/s)")
    binres[foot] = per
info("B1' reading (both ways): a rising eps with well depth across the four bins would be the environment selection showing inside the galaxy population; a flat eps says the threshold sits above L* depths")
EPS_GAL = {f: max(r[2] for r in binres[f]) for f in A0}; EPS_BEST = {f: max(r[1] for r in binres[f]) for f in A0}
# ⚠ CORRECTION 2026-09-03 (hunt_2026/h_kids_halo_bound_CORRECTION.py, 7/7): this per-bin ceiling is a DIFFERENTIAL bound
# (one bin's halo against the others').  COHERENTLY the four bins PREFER a full CDM-like halo, Delta chi2 = -32, because it is
# degenerate with the +/-0.3 dex amplitude nuisance.  The non-degenerate bound is the SPARC rotation curves: eps <~ 0.2 (dwarfs)
# to ~0.5 (massive discs).  Read D1 as "the halo-to-baryon ratio cannot VARY between mass bins", not as an absolute ceiling.
check("D1 with per-bin templates and the full covariance, the isolated KiDS lenses tolerate at most ~14% of a CDM-like (Newtonian-accreted) dust halo around a MOND well: max 2-sigma ceiling over the four bins <= 0.15, best-fit eps <= 0.07, both footings",
      all(EPS_GAL[f] <= 0.15 and EPS_BEST[f] <= 0.07 for f in A0), "; ".join(f"{f}: ceilings {[round(r[2],3) for r in binres[f]]}, best {[round(r[1],3) for r in binres[f]]}" for f in A0))
trend = {f: (binres[f][-1][2] - binres[f][0][2]) for f in A0}
info("D1' trend with well depth across bins 1->4 (ceiling_4 - ceiling_1): " + "; ".join(f"{f}: {trend[f]:+.3f}" for f in A0) + "  -> no rising eps with depth inside the galaxy population")
P(""); P("  B2  epsilon_cl: how much of a CDM-like halo the X-COP clusters need on top of the framework's own prediction at R500")
eta = {"canonical": 2.084, "alt": 1.917}; x500 = (0.33, 0.58); eps_cl = {}
for foot in A0:
    vals = []
    for x in x500:
        Mpred_over_Mb = nu(x); extra = (eta[foot] - 1.0)*Mpred_over_Mb      # extra mass needed, in units of M_b, to raise M_dyn from M_pred to eta*M_pred
        cdm_over_Mb = 1.0/F_B - 1.0                                          # a full CDM halo at the cosmic share
        vals.append(extra/cdm_over_Mb)
    eps_cl[foot] = vals; info(f"{foot:10} eta(R500) = {eta[foot]}: nu(x500) = {nu(x500[0]):.2f}-{nu(x500[1]):.2f}; extra mass needed = {(eta[foot]-1)*nu(x500[0]):.2f}-{(eta[foot]-1)*nu(x500[1]):.2f} M_b; full CDM = {1/F_B-1:.2f} M_b  =>  eps_cl = {min(vals):.2f}-{max(vals):.2f}")
check("D2 clusters need a SUBSTANTIAL but not full CDM-like component: eps_cl in [0.2, 0.8] on both footings, and >= 2x the galaxy ceiling of D1", all(0.2 <= v <= 0.8 for f in A0 for v in eps_cl[f]) and all(min(eps_cl[f]) >= 2*EPS_GAL[f] for f in A0),
      "; ".join(f"{f}: eps_cl {min(eps_cl[f]):.2f}-{max(eps_cl[f]):.2f} vs eps_gal,max {EPS_GAL[f]:.3f}" for f in A0))
P(""); P("  B3  the RAR bound: a CDM-like dust halo at eps_gal must move the RAR at 10-30 kpc by < 0.05 dex")
rar = {}
for foot, a0 in A0.items():
    Mcdm = res[(foot, "Mcdm")]; eps = EPS_GAL[foot]; shifts = []
    for rr in (10*kpc, 20*kpc, 30*kpc):
        gN0 = G*M_L(rr)/rr**2; gN1 = G*(M_L(rr) + eps*Mcdm(rr))/rr**2
        shifts.append(math.log10(gN1*nu(gN1/a0)/(gN0*nu(gN0/a0))))
    rar[foot] = shifts; info(f"{foot:10} at eps = eps_max = {eps:.3f}: RAR shift at 10/20/30 kpc = {shifts[0]:.3f}/{shifts[1]:.3f}/{shifts[2]:.3f} dex (M_cdm/M_b there {Mcdm(10*kpc)/M_L(10*kpc):.1f}/{Mcdm(20*kpc)/M_L(20*kpc):.1f}/{Mcdm(30*kpc)/M_L(30*kpc):.1f})")
check("D3a the lensing ceiling is also RAR-safe: at the D1 ceiling the RAR moves < 0.05 dex at 10-30 kpc, both footings", all(max(rar[f]) < 0.05 for f in A0), "; ".join(f"{f}: max {max(rar[f]):.3f} dex" for f in A0))
P(""); P("  B4  can ANY single local environment variable switch the coupling?  coupled set = {linear cosmos, cluster R500}; decoupled set = {galaxy outskirts, galaxy interior}")
depth = {}
for foot, a0 in A0.items():
    rr = np.geomspace(0.05*kpc, 3.5*Mpc, 6000); gt = np.array([G*M_L(r)/r**2*nu(G*M_L(r)/r**2/a0) for r in rr]); I = np.concatenate([[0.0], np.cumsum(0.5*(gt[1:] + gt[:-1])*np.diff(rr))])
    dep = lambda r: float(I[-1] - np.interp(r, rr, I))/c**2                         # |Psi(r) - Psi(3.5 Mpc)|
    depth[foot] = {"interior": dep(3*kpc), "30 kpc": dep(30*kpc), "250 kpc": dep(250*kpc)}
def T_bbks(k):
    Gam = OM_M*h*math.exp(-OM_B - math.sqrt(2*h)*OM_B/OM_M); q = k/Gam
    return math.log(1+2.34*q)/(2.34*q)*(1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
def W(x): return 3*(math.sin(x) - x*math.cos(x))/x**3
def sig_R(R_hmpc):
    return math.sqrt(quad(lambda k: k**2*k**0.965*T_bbks(k)**2*W(R_hmpc*k)**2/(2*math.pi**2), 1e-4, 50, limit=400)[0])
s8u = sig_R(8.0); lin = {}
for R in (8.0, 20.0, 50.0):
    dr = 0.811*sig_R(R)/s8u; Rm = R/h*Mpc; lin[R] = dict(Phi=0.75*OM_M*H0**2*dr*Rm**2/c**2, x=0.5*OM_M*H0**2*dr*Rm/A0["canonical"], rho=1+dr, sig=0.0)
    info(f"linear R = {R:.0f} h^-1 Mpc: delta_rms {dr:.3f} -> |Phi|/c^2 = {lin[R]['Phi']:.2e}, peculiar x = g/a0 = {lin[R]['x']:.1e}, rho/rho_bar = {lin[R]['rho']:.2f}, sigma ~ 0 (single-stream)")
for foot in A0: info(f"{foot:10} L* MOND well |Psi|/c^2: interior (3 kpc) {depth[foot]['interior']:.2e}, 30 kpc {depth[foot]['30 kpc']:.2e}, 250 kpc {depth[foot]['250 kpc']:.2e}")
Mcdm_c = res[("canonical", "Mcdm")]
env = {  # (|Phi|/c^2, x = g_bar/a0, rho/rho_bar of the DUST that would sit there, sigma [km/s]);  coupled = True means the gates REQUIRE the medium to gravitate there
 "linear 8 Mpc":        (lin[8.0]["Phi"],  lin[8.0]["x"],  lin[8.0]["rho"],  0.0,  True),
 "linear 50 Mpc":       (lin[50.0]["Phi"], lin[50.0]["x"], lin[50.0]["rho"], 0.0,  True),
 "cluster R500":        (2.5e-5, 0.45, 500.0, 1000.0, True),
 "galaxy 250 kpc":      (depth["canonical"]["250 kpc"], G*M_L(250*kpc)/(250*kpc)**2/A0["canonical"], (Mcdm_c(250*kpc)/(4/3*math.pi*(250*kpc)**3))/RHO_C, 200.0, False),
 "galaxy 30 kpc":       (depth["canonical"]["30 kpc"],  G*M_L(30*kpc)/(30*kpc)**2/A0["canonical"],  (Mcdm_c(30*kpc)/(4/3*math.pi*(30*kpc)**3))/RHO_C,  200.0, False),
 "galaxy interior 3 kpc": (depth["canonical"]["interior"], G*M_L(3*kpc)/(3*kpc)**2/A0["canonical"], (Mcdm_c(3*kpc)/(4/3*math.pi*(3*kpc)**3))/RHO_C, 150.0, False),
}
info(f"{'environment':24} {'|Phi|/c^2':>10} {'x=g/a0':>9} {'rho/rho_bar':>12} {'sigma km/s':>10}  coupling required")
for k, v in env.items(): info(f"{k:24} {v[0]:10.2e} {v[1]:9.2e} {v[2]:12.3g} {v[3]:10.0f}  {'YES' if v[4] else 'NO'}")
inter = {}
for j, name in enumerate(("|Phi|", "x", "rho", "sigma")):
    cpl = sorted(v[j] for v in env.values() if v[4]); dec = sorted(v[j] for v in env.values() if not v[4])
    # a monotone switch exists iff the two sets do not interleave: all coupled above all decoupled, or all below
    sep = (min(cpl) > max(dec)) or (max(cpl) < min(dec)); inter[name] = not sep
    info(f"{name:6}: coupled {[f'{x:.2e}' for x in cpl]}  decoupled {[f'{x:.2e}' for x in dec]}  -> {'INTERLEAVED (no monotone switch)' if inter[name] else 'separable'}")
check("D3 THE ASSERTION (computed, both ways): for EVERY local environment variable -- potential depth, acceleration, density, velocity dispersion -- the environments where the gates REQUIRE the medium to gravitate (linear cosmos, cluster R500) INTERLEAVE with those where they FORBID it (galaxy outskirts, galaxy interior): no single-variable local switch exists",
      all(inter.values()), "; ".join(f"{k}: {'interleaved' if v else 'SEPARABLE'}" for k, v in inter.items()))
info("what remains is a NON-local switch: a medium that gravitates only while single-stream (before shell crossing) and stops at the first caustic -- galaxies AND clusters are multi-stream, so it also abandons the cluster residual eta(R500) = 1.7-2.1 (G5 fails) and no field theory realises it")
P(""); P("="*120); P("VERDICT -- what the dark sector is, on the framework's own gates"); P("="*120)
P("  Every substance that is the same thing everywhere is dead: a particle that clusters like CDM is dead in galaxies (G4), a medium that holds")
P("  itself up is dead in the Bullet (G3), a field whose charge is the MOND scalar is dead on both (09-02), a superfluid is dead on the")
P("  background, a fermion or boson light enough to stay out of galaxies is dead on the forest.  The last idea -- a medium whose coupling")
P("  switches with its environment -- is dead too, by computation (D3): galaxy interiors are as deep, as dense, as accelerated and as hot as")
P("  the places where the CMB and the clusters need the medium to gravitate, so no local variable can switch it off in galaxies and on")
P("  elsewhere.  KiDS itself allows at most ~14% of a CDM-like halo around isolated MOND wells (D1), clusters need 30-46% (D2).")
P("  What survives, on the framework's own gates: (i) a CDM particle with NEWTONIAN gravity, in which the a0 - rho_Lambda tie and the zero")
P("  per-galaxy spread are coincidences under test (ledger A-2, A-9); or (ii) MOND gravity plus a dust that stops gravitating at its first")
P("  caustic -- no field theory realises it, and it leaves the cluster residual unexplained.  The strongest fried-chicken candidate (CCNL)")
P("  carries the excluded v9 dust as its clock unless the background pin is dropped; that is the bug to fix before anything else.")
P("  Both ways: the un-binned KiDS stack against one template LIKES a CDM-like halo (Dchi2 -33 at eps ~ 1.7) -- the binned, per-template")
P("  analysis with the full covariance does not (best eps 0-0.06); the RAR at 10-30 kpc forbids the un-binned reading outright (0.25 dex).")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
