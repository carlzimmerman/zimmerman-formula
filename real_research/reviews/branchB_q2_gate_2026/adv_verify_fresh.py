#!/usr/bin/env python3
"""
ADVERSARIAL VERIFICATION (fresh session) of laneB_q2_solve.py -- Branch B medium Q2 gate.
==========================================================================================
Written independently of the lane's code (no import, no closed-form rho_ph, different
integrator choices). Three jobs:

(1) FRESH RE-DERIVATION of the two most load-bearing numbers:
    - the corrected AQUAL/QUMOND-class baseline: simple-nu at Desmond fiducial
      (a0=1.2e-10, g_ext=2.32e-10). Lane claims Q2 = 3.515e-26 (banked script's
      4.776e-26 inflated 1.36x by a spurious /sqrt(D) -- verified against the arXiv
      PDF text: eq 12 integrand is (nu-1)[eN(3xi-5xi^3)+v^2(1-3xi^2)], NO /sqrt(D)).
    - the ALIVE member: 0.982*delta-family d=5 at canonical a0=9.362e-11,
      g_ext=2.2 a0. Lane claims Q2 = 1.25e-27 (0.24x ceiling).
    METHOD (independent): rho_ph = -div[delta(|gN|/a0) gN]/(4piG) evaluated by
    CENTRAL FINITE DIFFERENCES of the vector field (no analytic gradient), P2
    projection by SIMPSON on a uniform xi grid (not Gauss-Legendre), radial Green
    integrals by Simpson on a fresh log grid, Q2_eff = -3 phi2/r^2 at Saturn via
      phi2(r) = -(4piG/5)[ r^-3 Int_0^r S2 r'^4 dr' + r^2 Int_r^inf S2/r' dr' ].

(2) MANUFACTURED-KILL PROBE: the lane says "the ENTIRE power family sits at
    3.1-8.8x over the ceiling" but only scanned p <= 3. Extend to p = 4,5,6,8,10
    (n=2): does a steeper POWER screen thread gate (b) -- and if so at what RAR
    price? (fresh eq-12 dblquad, written from the paper text.)

(3) MANUFACTURED-PASS PROBE: the lane's "ROBUST PASS across the full g_ext bracket
    AND both footings" for d>=5 ran the ALT footing only at the central physical
    g_ext = 2.06e-10. Worst case is alt a0=1.13e-10 with the LOW physical g_ext
    edge. Compute d=4,5 and exp yc=0.5 on the full physical bracket
    g_ext in {1.78, 1.9, 2.06, 2.43}e-10 under BOTH footings; add the paper's
    AQUAL adder (+<1e-27, footnote 6) as headroom stress.

numpy/scipy only. Exit 0.
"""
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

G = 6.674e-11; Msun = 1.989e30; GM = G*Msun
AU = 1.495978707e11; Mpc = 3.0857e22
c = 2.99792458e8; H0 = 67.4e3/Mpc; OmL = 0.685
Lam = 3*OmL*H0**2/c**2
A0_CAN = c**2*np.sqrt(Lam/(32*np.pi))       # 9.362e-11
A0_ALT = 1.13e-10
Z = np.sqrt(32*np.pi/3); C_DEEP = np.sqrt(Z/6.0)
R_SAT = 9.5826*AU
Q2_CEIL = 1.6e-27 + 2*1.8e-27               # 5.2e-27

# ---------------------------------------------------------------- response functions (fresh)
def delta_simple(y):
    y = np.asarray(y, float)
    return 0.5*(np.sqrt(1.0+4.0/y)-1.0)     # simple nu - 1

def make_delta_fam(d, resc=1.0):
    def f(y):
        y = np.asarray(y, float)
        t = np.clip(y**(d/2.0), 1e-300, 700.0)
        return resc*(np.exp(-np.log(-np.expm1(-t))/d) - 1.0)
    return f

def make_power(p, n=2):
    a = (p-0.5)/n
    def f(y):
        y = np.asarray(y, float)
        return C_DEEP*y**-0.5*(1.0+y**n)**(-a)
    return f

def make_exp(yc):
    def f(y):
        y = np.asarray(y, float)
        return C_DEEP*y**-0.5*np.exp(-np.minimum(y/yc, 700.0))
    return f

# ---------------------------------------------------------------- fresh eq-12 (from the paper text)
def q_eq12(delta, eN, vmax=100.0):
    """q = (3/2) Int_0^vmax dv Int_-1^1 dxi delta(sqrt(eN^2+v^4+2 eN v^2 xi)) *
           [eN(3xi-5xi^3)+v^2(1-3xi^2)]   -- NO /sqrt(D) (arXiv:2401.04796 eq 12)."""
    def ig(xi, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*xi
        if D <= 0: return 0.0
        return float(delta(np.sqrt(D)))*(eN*(3*xi-5*xi**3) + v*v*(1-3*xi*xi))
    val, _ = integrate.dblquad(ig, 0, vmax, lambda v: -1, lambda v: 1,
                               epsabs=1e-12, epsrel=1e-8)
    return 1.5*val

def solve_eN(delta, etilde):
    return brentq(lambda e: e*(1.0+float(delta(e))) - etilde, 1e-9, etilde, xtol=1e-14)

def Q2_of(delta, etilde, a0):
    eN = solve_eN(delta, etilde)
    return -(3.0*a0**1.5)/(2.0*np.sqrt(GM))*q_eq12(delta, eN), eN

# ---------------------------------------------------------------- fresh grid solver (FD divergence)
def Q2_grid_fresh(delta, eN, a0, Nr=3000, Nxi=1601, rmax_f=800.0, frac=1e-4):
    """Fully independent: rho_ph from CENTRAL DIFFERENCES of F = delta(|gN|/a0)*gN
    in spherical (r,theta); P2 projection by Simpson in xi; Green integrals by
    Simpson in log r; evaluate at Saturn."""
    ge = eN*a0
    r_t = np.sqrt(GM/ge)
    r = np.logspace(np.log10(0.5*AU), np.log10(rmax_f*r_t), Nr)
    xi = np.linspace(-1.0, 1.0, Nxi)
    th = np.arccos(xi)
    Rg, Tg = np.meshgrid(r, th, indexing='ij')

    def field(Rm, Tm):
        # gN = -GM/r^2 rhat + ge zhat ; components in spherical basis (r,theta)
        gr = -GM/Rm**2 + ge*np.cos(Tm)
        gt = -ge*np.sin(Tm)
        Y = np.sqrt(gr*gr + gt*gt)/a0
        d = delta(Y)
        return d*gr, d*gt

    # divergence in spherical coords via central differences (r: log-spaced -> use
    # actual coordinate differences; theta: uniform in xi -> nonuniform in theta,
    # use two-sided nonuniform difference)
    hr = Rg*frac
    Fr_p, _ = field(Rg+hr, Tg); Fr_m, _ = field(Rg-hr, Tg)
    Fr, Ft = field(Rg, Tg)
    dFr_dr = (Fr_p - Fr_m)/(2*hr)
    ht = np.minimum(frac, 0.4*np.minimum(Tg, np.pi-Tg) + 1e-12)
    _, Ft_p = field(Rg, Tg+ht); _, Ft_m = field(Rg, Tg-ht)
    dFt_dt = (Ft_p - Ft_m)/(2*ht)
    sinT = np.sin(Tg)
    with np.errstate(divide='ignore', invalid='ignore'):
        divF = dFr_dr + 2.0*Fr/Rg + (dFt_dt*sinT + Ft*np.cos(Tg))/(Rg*sinT)
    divF = np.where(sinT < 1e-8, dFr_dr + 2.0*Fr/Rg + 2*dFt_dt/Rg, divF)
    rho_ph = -divF/(4*np.pi*G)

    P2 = 0.5*(3*xi**2 - 1)
    S2 = 2.5*integrate.simpson(rho_ph*P2[None, :]*(-1), x=th, axis=1)*(-1)  # d(xi) = -sin(th)dth handled: integrate over th with weight sin
    # redo cleanly: Int_-1^1 f dxi = Int_0^pi f sin(th) dth ; th grid descends with xi -> sort
    order = np.argsort(th)
    S2 = 2.5*integrate.simpson((rho_ph*P2[None, :])[:, order]*np.sin(th[order])[None, :],
                               x=th[order], axis=1)

    lnr = np.log(r)
    m_in = r <= R_SAT
    I_in = integrate.simpson(S2[m_in]*r[m_in]**5, x=lnr[m_in]) if m_in.sum() > 5 else 0.0
    m_out = r >= R_SAT
    I_out = integrate.simpson(S2[m_out], x=lnr[m_out])
    return (12*np.pi*G/5.0)*(I_in/R_SAT**5 + I_out)

# ---------------------------------------------------------------- SPARC (fresh loader)
import glob, os
DATADIR = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
def load_sparc(Yd, Yb=0.7):
    kpc = 3.0857e19
    gN, gobs = [], []
    for fn in sorted(glob.glob(os.path.join(DATADIR, "*_rotmod.dat"))):
        d = np.genfromtxt(fn)
        if d.ndim != 2 or d.shape[1] < 6: continue
        R = d[:,0]*kpc; Vo = d[:,1]*1e3; Vg = d[:,3]*1e3; Vd = d[:,4]*1e3; Vb = d[:,5]*1e3
        Vb2 = Vg*np.abs(Vg) + Yd*Vd*np.abs(Vd) + Yb*Vb*np.abs(Vb)
        ok = (R > 0) & (Vo > 0) & (Vb2 > 0)
        gN.append(Vb2[ok]/R[ok]); gobs.append(Vo[ok]**2/R[ok])
    return np.concatenate(gN), np.concatenate(gobs)

def binres(delta, a0, gN, gobs, bins=((0.1,0.3),(0.3,1.0),(1.0,3.0))):
    y = gN/a0; dex = np.log10(gobs/gN); out = []
    for lo, hi in bins:
        m = (y >= lo) & (y < hi)
        ymed = np.median(y[m])
        out.append(np.log10(1+float(delta(ymed))) - np.median(dex[m]))
    return out

# ================================================================ run
print("="*96)
print("(1) FRESH RE-DERIVATION -- independent FD-divergence grid solver vs lane's numbers")
print("="*96)
# anchor: simple nu at Desmond fiducial
a0d, et_d = 1.2e-10, 2.32e-10/1.2e-10
Q2_m, eN_d = Q2_of(delta_simple, et_d, a0d)
print(f"  simple-nu fiducial: eN={eN_d:.4f}  Q2(fresh eq-12)={Q2_m:.4e}  [lane: 3.515e-26]")
Q2_g = Q2_grid_fresh(delta_simple, eN_d, a0d)
print(f"                       Q2(fresh FD grid) ={Q2_g:.4e}   ratio grid/eq12 = {Q2_g/Q2_m:.4f}")
# the alive member
d5 = make_delta_fam(5.0, resc=C_DEEP)
Q2d5_m, eN5 = Q2_of(d5, 2.2, A0_CAN)
print(f"  0.982*delta-fam d=5 @ can 2.2a0: eN={eN5:.4f}  Q2(fresh eq-12)={Q2d5_m:.4e}  [lane: 1.25e-27]")
Q2d5_g = Q2_grid_fresh(d5, eN5, A0_CAN, Nr=4000, Nxi=2401)
print(f"                       Q2(fresh FD grid) ={Q2d5_g:.4e}   ratio grid/eq12 = {Q2d5_g/Q2d5_m:.4f}")
ok1 = abs(Q2_m/3.515e-26 - 1) < 0.02 and abs(Q2_g/Q2_m - 1) < 0.05
ok2 = abs(Q2d5_m/1.25e-27 - 1) < 0.05 and abs(Q2d5_g/Q2d5_m - 1) < 0.08
print(f"  -> baseline {'REPRODUCED' if ok1 else 'MISMATCH'}; alive-member {'REPRODUCED' if ok2 else 'MISMATCH'}")

print()
print("="*96)
print("(2) MANUFACTURED-KILL PROBE -- extend the power family beyond p=3 (n=2), canonical a0")
print("="*96)
gN7, gobs7 = load_sparc(0.7)
gN8, gobs8 = load_sparc(0.8)
print(f"  {'p':>4} {'Q2@1.9a0':>10} {'Q2@2.2a0':>10} {'Q2@2.6a0':>10} {'x-ceil(worst)':>13}"
      f" {'d(6)':>8} {'d(1)':>7}  res[0.3,1)/[1,3) dex @Yd=0.7 | @0.8")
for p in (3.0, 4.0, 5.0, 6.0, 8.0, 10.0):
    f = make_power(p)
    q2s = [Q2_of(f, et, A0_CAN)[0] for et in (1.9, 2.2, 2.6)]
    worst = max(abs(v) for v in q2s)/Q2_CEIL
    r7 = binres(f, A0_CAN, gN7, gobs7); r8 = binres(f, A0_CAN, gN8, gobs8)
    print(f"  {p:>4.0f} {q2s[0]:>10.2e} {q2s[1]:>10.2e} {q2s[2]:>10.2e} {worst:>12.2f}x"
          f" {float(f(6.0)):>8.1e} {float(f(1.0)):>7.3f}  {r7[1]:+.3f}/{r7[2]:+.3f} | {r8[1]:+.3f}/{r8[2]:+.3f}")
d5r7 = binres(d5, A0_CAN, gN7, gobs7); d5r8 = binres(d5, A0_CAN, gN8, gobs8)
fr = lambda y: np.sqrt(1+1/np.asarray(y, float))-1
frr7 = binres(fr, A0_CAN, gN7, gobs7)
print(f"  ref: 0.982*d=5 residuals {d5r7[1]:+.3f}/{d5r7[2]:+.3f} @0.7 | {d5r8[1]:+.3f}/{d5r8[2]:+.3f} @0.8 ;"
      f"  frame-nu @0.7: {frr7[1]:+.3f}/{frr7[2]:+.3f}")

print()
print("="*96)
print("(3) MANUFACTURED-PASS PROBE -- full PHYSICAL g_ext bracket under BOTH footings")
print("    (lane ran alt footing only at the central 2.06e-10; worst case = alt + low edge)")
print("="*96)
G_EXT_PHYS = [1.78e-10, 1.90e-10, 2.06e-10, 2.43e-10]
members = [("0.982*delta-fam d=4", make_delta_fam(4.0, resc=C_DEEP)),
           ("0.982*delta-fam d=5", make_delta_fam(5.0, resc=C_DEEP)),
           ("0.982*delta-fam d=6", make_delta_fam(6.0, resc=C_DEEP)),
           ("delta-fam d=5 (unresc)", make_delta_fam(5.0)),
           ("exp screen yc=0.5", make_exp(0.5))]
AQUAL_ADDER = 1.0e-27   # Desmond footnote 6: AQUAL Q2 larger by < 1e-27 (headroom stress)
for lab, f in members:
    row = f"  {lab:<24}"
    worst = 0.0
    for a0, tag in ((A0_CAN, "can"), (A0_ALT, "alt")):
        for gx in G_EXT_PHYS:
            Q2v, _ = Q2_of(f, gx/a0, a0)
            worst = max(worst, abs(Q2v))
            row += f" {tag}{gx*1e10:.2f}:{abs(Q2v):.2e}"
    verdict = ("ROBUST" if worst <= Q2_CEIL else "EDGE-FAIL") + \
              (" (+AQUAL ok)" if worst + AQUAL_ADDER <= Q2_CEIL else " (+AQUAL MARGINAL)" if worst <= Q2_CEIL else "")
    print(row)
    print(f"      worst |Q2| = {worst:.2e}  vs ceiling {Q2_CEIL:.1e}  -> {verdict}")
print()
print("done. exit 0")
