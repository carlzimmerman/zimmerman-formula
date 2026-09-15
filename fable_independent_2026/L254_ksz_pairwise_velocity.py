#!/usr/bin/env python3
"""L254 -- THE KINEMATIC SUNYAEV-ZEL'DOVICH PAIRWISE VELOCITY: a direct test of who does the clustering,
and an honest accounting of why it cannot be run today.

THE ANGLE.  The kSZ effect measures the BARYON MOMENTUM field: CMB photons scattering off moving free
electrons acquire a temperature shift  (Delta T/T) = -(sigma_T/c) integral n_e v.dl = -tau v_los/c.  The
PAIRWISE estimator stacks pairs of tracers and measures the mean pairwise velocity v_12(r), which on
10-100 Mpc is fixed by the linear growth rate and NOTHING else.  So kSZ is a clean, largely bias-safe
reading of exactly the quantity the framework's field equation modifies.

WHAT THE FRAMEWORK PREDICTS, from this repo's own recorded numbers.  L180 (`L180_hubble_kernel_growth_
prediction.py`, DOI 22706925) fixes the cosmological coupling with no new parameter from a_0 = kappa c
sqrt(G rho_Lambda) and the Hubble-flow prescription for the kernel argument:
        G_eff(z)/G = nu(c H(z)/a_0),   nu(x) = 1/(1 - exp(-sqrt(x))),   c H_0/a_0 = (1/kappa) sqrt(8 pi/(3 Om_L))
giving c H_0/a_0 = 6.99 (canonical) / 5.80 (alt) and f sigma_8 RAISED by 2.7%/3.8% at z = 0.3, 1.9%/2.6%
at z = 0.6, 1.1%/1.6% at z = 1.0.  This lane re-solves that growth equation from scratch and checks it
against L180's recorded table before using it.

WHY kSZ AND NOT S_8.  L197 (`fable_independent_2026/FINDINGS.md`, L197, 2026-09-12) found that the kernel's
lift and the clock-frame kicks' suppression very nearly CANCEL at eight megaparsecs, so S_8 does not
discriminate.  But L197's own particle-mesh table shows the kicks are a SMALL-SCALE effect: P/P_LCDM =
0.999 at k = 0.2 h/Mpc against 0.840 at k = 2 h/Mpc.  Pairwise kSZ lives at r = 10-100 Mpc/h, i.e.
k ~ 0.06-0.6 h/Mpc, where the cancellation has not happened.  kSZ therefore reads the kernel's raise
almost undiluted -- which is the case for looking at it at all.

THE CENTRAL DIFFICULTY, stated up front and not buried.  The kSZ amplitude is measured as tau_bar * v_12.
The mean optical depth tau_bar is set by the baryon profile and feedback and is uncertain at the 10-30%
level (literature; see the LIT block below).  The framework's signal is a 2-4% amplitude shift.  Worse,
because G_eff/G = nu(cH/a_0) depends only on redshift and NOT on scale, the framework's entire kSZ
signature is a PURE AMPLITUDE RESCALING -- exactly the one direction in which tau is degenerate with it.
There is no shape handle.  This lane computes that degeneracy quantitatively and reports the verdict.

METHOD.  Linear theory throughout.  Transfer function: Eisenstein & Hu 1998 (ApJ 496, 605) FULL fitting
form WITH baryon acoustic wiggles, implemented here and validated against (i) the Planck 2018 drag-epoch
sound horizon and (ii) the EH98 no-wiggle shape form, which is implemented independently.  Pairwise
velocity from the pair-conservation equation,
        v_12(r) = -(2/3) a H(z) f(z) r * b xi_bar_m(r,z) / (1 + b^2 xi_m(r,z))
with xi_bar(r) = 3 integral dk/k Delta^2(k) j_1(kr)/(kr) evaluated in k-space directly (exact identity for
the volume average of j_0).  b^1 in the numerator is the halo-matter cross correlation, b^2 in the
denominator the halo auto correlation.

Checks state measurement and threshold separately; the FAIL is the finding; no literal-True conditions.
Both a_0 footings throughout."""
import os, sys, json, warnings
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

warnings.filterwarnings("ignore")
np.seterr(all="ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)

# ------------------------------------------------------------------ cosmology, both footings
h, Om, Obh2, ns, TCMB = 0.6736, 0.3138, 0.02237, 0.9649, 2.7255      # Planck 2018 TT,TE,EE+lowE+lensing
OL = 1.0 - Om
SIG8_LCDM = 0.811                                                     # Planck 2018 sigma_8, the normalisation
Omh2 = Om*h*h; Och2 = Omh2 - Obh2; fb = Obh2/Omh2; fc = Och2/Omh2
cLIGHT, H0_SI = 2.998e8, 100*h*1e3/3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
E = lambda a: np.sqrt(Om*a**-3 + OL)
nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(x)))

# ------------------------------------------------------------------ LITERATURE VALUES (quoted, NOT recomputed here)
LIT = {
 "pairwise_snr": [
   ("Hand et al. 2012, PRL 109 041101 (arXiv:1203.4219), ACT x BOSS -- first detection", 3.8),
   ("Soergel et al. 2016, MNRAS 461 3172 (arXiv:1603.03904), SPT-SZ x DES-Y1 clusters", 4.2),
   ("De Bernardis et al. 2017, JCAP 03 008 (arXiv:1607.02139), ACT x BOSS DR11", 3.8),
   ("Calafut et al. 2021, PRD 104 043502 (arXiv:2101.08374), ACT DR5+Planck x SDSS DR15 LRG", 5.4)],
 "stacked_snr": ("Schaan et al. 2021, PRD 103 063513 (arXiv:2009.05557), ACT DR5 x BOSS, "
                 "velocity-reconstruction stacking (NOT pairwise)", 6.5),
 "tau_frac": [("Battaglia 2016, JCAP 08 058 (arXiv:1607.02442) 'The tau of galaxy clusters': "
               "optical-depth uncertainty ~15% for Planck-like cluster samples; sub-grid physics "
               "systematics <10% when a tau-tSZ relation is used", 0.15),
              ("Amodeo et al. 2021, PRD 103 063514 (arXiv:2009.05558) and the feedback literature that "
               "followed it: hydrodynamic simulations under-predict the measured kSZ/tSZ gas profiles, and "
               "strong- vs weak-feedback models differ by tens of percent", 0.30),
              ("optimistic floor if the gas profile is externally calibrated", 0.10)],
 "note": "Every number in this block is a LITERATURE VALUE quoted from the published source named beside "
         "it. NONE of them is recomputed in this lane. Check them against the sources before publication.",
}
print("L254 -- the kinematic Sunyaev-Zel'dovich pairwise velocity as a test of who does the clustering\n")
print("LITERATURE BLOCK (quoted values, not recomputed here)")
for s, v in LIT["pairwise_snr"]: print(f"    pairwise kSZ detection {v:.1f} sigma  --  {s}")
print(f"    stacked   kSZ detection {LIT['stacked_snr'][1]:.1f} sigma  --  {LIT['stacked_snr'][0]}")
for s, v in LIT["tau_frac"]: print(f"    sigma_tau/tau = {v:.0%}  --  {s}")
OUT["literature"] = {"pairwise_snr": LIT["pairwise_snr"], "stacked_snr": LIT["stacked_snr"],
                     "tau_frac": LIT["tau_frac"], "note": LIT["note"]}

# ------------------------------------------------------------------ V1: the linear machinery, validated
print("\nV1 -- the transfer function and correlation function, validated against known cosmological numbers")
TH = TCMB/2.7
zeq  = 2.50e4*Omh2*TH**-4
keq  = 7.46e-2*Omh2*TH**-2                                            # Mpc^-1
b1_d = 0.313*Omh2**-0.419*(1 + 0.607*Omh2**0.674)
b2_d = 0.238*Omh2**0.223
zd   = 1291*Omh2**0.251/(1 + 0.659*Omh2**0.828)*(1 + b1_d*Obh2**b2_d)
Rof  = lambda z: 31.5*Obh2*TH**-4*(1e3/z)
Rd, Req = Rof(zd), Rof(zeq)
s_eh = (2.0/(3.0*keq))*np.sqrt(6.0/Req)*np.log((np.sqrt(1+Rd)+np.sqrt(Rd+Req))/(1+np.sqrt(Req)))
kSilk = 1.6*Obh2**0.52*Omh2**0.73*(1 + (10.4*Omh2)**-0.95)
a1_ = (46.9*Omh2)**0.670*(1 + (32.1*Omh2)**-0.532)
a2_ = (12.0*Omh2)**0.424*(1 + (45.0*Omh2)**-0.582)
alpha_c = a1_**(-fb)*a2_**(-fb**3)
b1_c = 0.944/(1 + (458*Omh2)**-0.708); b2_c = (0.395*Omh2)**-0.0266
beta_c = 1.0/(1 + b1_c*(fc**b2_c - 1))
yv = (1+zeq)/(1+zd)
Gy = yv*(-6*np.sqrt(1+yv) + (2+3*yv)*np.log((np.sqrt(1+yv)+1)/(np.sqrt(1+yv)-1)))
alpha_b = 2.07*keq*s_eh*(1+Rd)**-0.75*Gy
beta_b = 0.5 + fb + (3 - 2*fb)*np.sqrt((17.2*Omh2)**2 + 1)
beta_node = 8.41*Omh2**0.435

def T_eh98(k_h):                                                      # k in h/Mpc -> EH98 wants Mpc^-1
    k = k_h*h
    q = k/(13.41*keq); ks = k*s_eh
    def T0(ac, bc):
        C = 14.2/ac + 386.0/(1 + 69.9*q**1.08)
        L = np.log(np.e + 1.8*bc*q)
        return L/(L + C*q*q)
    f_ = 1.0/(1.0 + (ks/5.4)**4)
    Tc = f_*T0(1.0, beta_c) + (1-f_)*T0(alpha_c, beta_c)
    st = s_eh/(1 + (beta_node/np.maximum(ks, 1e-12))**3)**(1.0/3.0)
    x = k*st
    j0 = np.where(x < 1e-8, 1.0 - x*x/6.0, np.sin(x)/np.where(x == 0, 1.0, x))
    Tb = (T0(1.0, 1.0)/(1 + (ks/5.2)**2)
          + alpha_b/(1 + (beta_b/np.maximum(ks, 1e-12))**3)*np.exp(-(k/kSilk)**1.4))*j0
    return fb*Tb + fc*Tc

def T_nowiggle(k_h):                                                  # EH98 shape form, independent implementation
    k = k_h*h
    aG = 1 - 0.328*np.log(431*Omh2)*fb + 0.38*np.log(22.3*Omh2)*fb**2
    Gam = Om*h*(aG + (1-aG)/(1 + (0.43*k*s_eh)**4))
    q = k_h*TH**2/Gam
    L0 = np.log(2*np.e + 1.8*q); C0 = 14.2 + 731.0/(1 + 62.5*q)
    return L0/(L0 + C0*q*q)

NK, KMIN, KMAX, RSMOOTH = 400000, 1e-5, 50.0, 0.25                    # h/Mpc; Gaussian smoothing in h^-1 Mpc
kk = np.logspace(np.log10(KMIN), np.log10(KMAX), NK)
dlnk = np.log(kk[1]/kk[0])
def delta2(T):                                                        # dimensionless power, unnormalised
    return kk**(3+ns)*T(kk)**2
def norm_to_sigma8(T, s8):
    x = kk*8.0; W = 3*(np.sin(x) - x*np.cos(x))/x**3
    return s8**2/np.sum(delta2(T)*W**2*dlnk)
AMP_F = norm_to_sigma8(T_eh98, SIG8_LCDM)
AMP_N = norm_to_sigma8(T_nowiggle, SIG8_LCDM)
D2_F = AMP_F*delta2(T_eh98)*np.exp(-(kk*RSMOOTH)**2)
D2_N = AMP_N*delta2(T_nowiggle)*np.exp(-(kk*RSMOOTH)**2)

def xi_and_xibar(D2, r):                                              # r in h^-1 Mpc; exact j1 window for xi_bar
    r = np.atleast_1d(r).astype(float)
    x = np.outer(r, kk)
    j0 = np.sin(x)/x
    j1 = (np.sin(x)/x - np.cos(x))/x
    xi = np.sum(D2*j0*dlnk, axis=1)
    xib = 3.0*np.sum(D2*j1/x*dlnk, axis=1)
    return xi, xib

rr = np.geomspace(1.0, 200.0, 400)
xi_F, xib_F = xi_and_xibar(D2_F, rr)
s_planck = 147.09                                                     # Planck 2018 r_drag, Mpc -- literature value
ibao = np.argmax((rr**2*xi_F)[(rr > 80) & (rr < 130)])
r_bao = rr[(rr > 80) & (rr < 130)][ibao]
Tlow = float(T_eh98(np.array([1e-5]))[0])
msk = (kk > 1e-3) & (kk < 1.0)
ratio_fn = T_eh98(kk[msk])/T_nowiggle(kk[msk])
print(f"    EH98 drag-epoch sound horizon s = {s_eh:.2f} Mpc ({s_eh*h:.2f} h^-1 Mpc); z_d = {zd:.1f}, z_eq = {zeq:.0f}")
print(f"    Planck 2018 r_drag = {s_planck:.2f} Mpc (LITERATURE) -> EH98 differs by {100*abs(s_eh/s_planck-1):.2f}%")
print(f"    T(k -> 0) = {Tlow:.5f} (must be 1); BAO peak of r^2 xi(r) at r = {r_bao:.1f} h^-1 Mpc = {r_bao/h:.1f} Mpc")
print(f"    full-vs-no-wiggle T ratio over k = 1e-3..1 h/Mpc: mean {ratio_fn.mean():.4f}, "
      f"peak-to-peak {ratio_fn.max()-ratio_fn.min():.3f} (the acoustic wiggles)")
OUT["s_eh98_Mpc"] = float(s_eh); OUT["s_planck_Mpc"] = s_planck; OUT["zd"] = float(zd); OUT["zeq"] = float(zeq)
OUT["r_bao_hinvMpc"] = float(r_bao); OUT["T_lowk"] = Tlow
OUT["nowiggle_ratio_mean"] = float(ratio_fn.mean()); OUT["nowiggle_ratio_ptp"] = float(ratio_fn.max()-ratio_fn.min())
check("V1 [THE LINEAR MACHINERY REPRODUCES INDEPENDENT COSMOLOGICAL NUMBERS] the Eisenstein-Hu 1998 sound "
      "horizon is compared with the Planck 2018 drag-epoch value 147.09 Mpc (threshold: 5%), the low-k limit "
      "of the transfer function with unity (threshold: 1%), and the acoustic peak of r^2 xi(r) with the "
      "standard 100 h^-1 Mpc BAO scale (threshold: the 95-115 h^-1 Mpc window)",
      abs(s_eh/s_planck - 1) < 0.05 and abs(Tlow - 1) < 0.01 and 95.0 < r_bao < 115.0,
      f"s = {s_eh:.2f} Mpc, {100*abs(s_eh/s_planck-1):.2f}% from Planck's 147.09; T(0) = {Tlow:.5f}; "
      f"BAO peak at {r_bao:.1f} h^-1 Mpc. The independently coded no-wiggle form agrees in the broadband "
      f"(mean ratio {ratio_fn.mean():.3f}) and differs only by the acoustic oscillation")

# ------------------------------------------------------------------ V2: the growth solver against L180
print("\nV2 -- the framework's growth, re-solved from scratch and checked against L180's recorded table")
def growth(geff):
    def rhs(l, y):
        a = np.exp(l); Oma = Om*a**-3/E(a)**2
        return [y[1], 1.5*Oma*geff(a)*y[0] - (2 - 1.5*Oma)*y[1]]
    ls = np.linspace(np.log(1/101), 0, 2000)
    sol = solve_ivp(rhs, [ls[0], 0], [1.0, 1.0], t_eval=ls, rtol=1e-10, atol=1e-13)
    return np.exp(ls), sol.y[0], sol.y[1]/sol.y[0]
a_, D_L, f_L = growth(lambda a: 1.0)
Dl = interp1d(a_, D_L); fl = interp1d(a_, f_L)
L180_REC = {"canonical": {0.3: 2.7, 0.6: 1.9, 1.0: 1.1}, "alt": {0.3: 3.8, 0.6: 2.6, 1.0: 1.6}}
GR = {}
worst_pp = 0.0
for tag, a0 in A0.items():
    r0 = cLIGHT*H0_SI/a0
    a_, D, f = growth(lambda a: nu(r0*E(a)))
    GR[tag] = (interp1d(a_, D), interp1d(a_, f), r0, float(D[-1]/D_L[-1]))
    row = []
    for z in (0.3, 0.6, 1.0):
        a = 1/(1+z)
        got = 100*((GR[tag][1](a)*GR[tag][0](a))/(fl(a)*Dl(a)) - 1)
        row.append((z, float(got), L180_REC[tag][z]))
        worst_pp = max(worst_pp, abs(got - L180_REC[tag][z]))
    OUT[f"growth_{tag}"] = {"cH0_over_a0": float(r0), "D0_ratio": GR[tag][3],
                            "dfs8_pct": {str(z): g for z, g, _ in row}}
    print(f"    [{tag}] cH_0/a_0 = {r0:.2f}, G_eff/G(z=0) = {nu(r0):.4f}, D(0) ratio = {GR[tag][3]:.4f}; "
          f"d(f sigma_8)/(f sigma_8) = " + ", ".join(f"z={z}: {g:+.1f}% (L180 recorded {rec:+.1f}%)"
                                                     for z, g, rec in row))
OUT["v2_worst_pp"] = float(worst_pp)
print(f"    largest disagreement with L180's recorded table: {worst_pp:.2f} percentage points")
check("V2 [THE GROWTH PREDICTION IS THIS REPO'S OWN, REPRODUCED INDEPENDENTLY] the Hubble-kernel growth "
      "equation of L180 is re-solved here from a_0 = kappa c sqrt(G rho_Lambda) and the six recorded "
      "f sigma_8 boosts (2.7/1.9/1.1% canonical, 3.8/2.6/1.6% alt at z = 0.3/0.6/1.0) are compared with the "
      "values this lane computes; threshold 0.15 percentage points on the worst of the six",
      worst_pp < 0.15,
      f"worst disagreement {worst_pp:.2f} pp over six numbers. The prediction used below is NOT invented "
      "here: it is L180's, re-derived, and the citation is L180_hubble_kernel_growth_prediction.py / .out "
      "and the L180 entry of FINDINGS.md (DOI 22706925)")

# ------------------------------------------------------------------ V3: v_12(r) in linear theory
print("\nV3 -- the mean pairwise velocity v_12(r) at 10-100 Mpc/h, LCDM and framework")
Z_KSZ, B_TRACER = 0.5, 2.0                                            # CMASS/LRG-like: the kSZ samples' regime
RGRID = np.array([10., 15., 20., 30., 40., 60., 80., 100.])           # h^-1 Mpc, comoving
H0_KMS = 100*h
xi0_F, xib0_F = xi_and_xibar(D2_F, RGRID)                             # z = 0, LCDM normalisation
xi0_N, xib0_N = xi_and_xibar(D2_N, RGRID)
def v12(r_h, xi0, xib0, fz, Dz, b):
    a = 1/(1+Z_KSZ); Hz = H0_KMS*E(a)                                 # km/s/Mpc
    return -(2.0/3.0)*a*Hz*(r_h/h)*fz*b*xib0*Dz**2/(1 + b**2*xi0*Dz**2)
a_z = 1/(1+Z_KSZ)
D_Lz, f_Lz = float(Dl(a_z))/float(Dl(1.0)), float(fl(a_z))        # D normalised to the LCDM z = 0 value
v_L = v12(RGRID, xi0_F, xib0_F, f_Lz, D_Lz, B_TRACER)
print(f"    z = {Z_KSZ}, linear bias b = {B_TRACER} (CMASS/LRG-like), LCDM f(z) = {f_Lz:.4f}, "
      f"D(z)/D(0) = {D_Lz:.4f}, sigma_8(z) = {SIG8_LCDM*D_Lz:.4f}")
print(f"    {'r [h^-1 Mpc]':>13} {'xi_m':>10} {'xi_bar_m':>10} {'v_12 LCDM [km/s]':>18}")
for i, r in enumerate(RGRID):
    print(f"    {r:13.0f} {xi0_F[i]*D_Lz**2:10.5f} {xib0_F[i]*D_Lz**2:10.5f} {v_L[i]:18.1f}")
OUT["z_ksz"] = Z_KSZ; OUT["b_tracer"] = B_TRACER
OUT["r_grid_hinvMpc"] = RGRID.tolist(); OUT["v12_lcdm_kms"] = v_L.tolist()
v20 = abs(v_L[RGRID == 20.][0])
print(f"    |v_12| at r = 20 h^-1 Mpc: {v20:.1f} km/s")
print("    (linear theory is known to UNDERSTATE |v_12| below ~20 h^-1 Mpc, where pair-weighting and "
      "nonlinear infall add; the fractional shift below is insensitive to that -- see V4)")
check("V3 [THE PAIRWISE VELOCITY HAS THE AMPLITUDE THE MEASUREMENTS WORK WITH] the linear-theory |v_12| at "
      "r = 20 h^-1 Mpc for a b = 2 tracer at z = 0.5 is computed and compared with the 50-250 km/s band that "
      "published pairwise-kSZ model curves span for LRG-like samples at that separation",
      50.0 < v20 < 250.0,
      f"|v_12(20 h^-1 Mpc)| = {v20:.1f} km/s, inside the 50-250 km/s band; the curve falls from "
      f"{abs(v_L[0]):.0f} km/s at 10 h^-1 Mpc to {abs(v_L[-1]):.0f} km/s at 100 h^-1 Mpc, the standard shape")

# ------------------------------------------------------------------ V4: the shift, and its scale-independence
print("\nV4 -- the framework's fractional shift in v_12, and the fact that it carries NO SHAPE")
print("     convention A: the SAME tracer bias b in both cosmologies  -> v_12 ~ f b sigma_8^2")
print("     convention B: b recalibrated so b*sigma_8 matches the measured galaxy clustering amplitude")
print("                   -> v_12 ~ (f sigma_8)(b sigma_8), i.e. the shift is exactly d(f sigma_8)/(f sigma_8)")
SHIFT = {}
for tag in A0:
    Df, ff, _, _ = GR[tag]
    D_Fz, f_Fz = float(Df(a_z))/float(Dl(1.0)), float(ff(a_z))      # same normalisation (CMB-anchored at a_i)
    vA = v12(RGRID, xi0_F, xib0_F, f_Fz, D_Fz, B_TRACER)
    bB = B_TRACER*D_Lz/D_Fz                                           # b*sigma_8 held at the measured value
    vB = v12(RGRID, xi0_F, xib0_F, f_Fz, D_Fz, bB)
    dA = 100*(vA/v_L - 1); dB = 100*(vB/v_L - 1)
    # the same thing with the independently coded no-wiggle P(k): shape-insensitivity of the fractional shift
    vLn = v12(RGRID, xi0_N, xib0_N, f_Lz, D_Lz, B_TRACER)
    vAn = v12(RGRID, xi0_N, xib0_N, f_Fz, D_Fz, B_TRACER)
    dAn = 100*(vAn/vLn - 1)
    SHIFT[tag] = dict(A=dA, B=dB, A_nowiggle=dAn, f_ratio=f_Fz/f_Lz, D_ratio=D_Fz/D_Lz)
    print(f"    [{tag}] f(z)/f_LCDM = {f_Fz/f_Lz:.5f}, D(z)/D_LCDM = {D_Fz/D_Lz:.5f}")
    print(f"        convention A: " + ", ".join(f"{r:.0f}:{d:+.2f}%" for r, d in zip(RGRID, dA)))
    print(f"        convention B: " + ", ".join(f"{r:.0f}:{d:+.2f}%" for r, d in zip(RGRID, dB)))
    OUT[f"shift_A_pct_{tag}"] = dA.tolist(); OUT[f"shift_B_pct_{tag}"] = dB.tolist()
    OUT[f"shift_A_nowiggle_pct_{tag}"] = dAn.tolist()
spreadA = max(float(np.ptp(SHIFT[t]["A"])) for t in A0)
spreadB = max(float(np.ptp(SHIFT[t]["B"])) for t in A0)
shape_dev = max(float(np.max(np.abs(SHIFT[t]["A"] - SHIFT[t]["A_nowiggle"]))) for t in A0)
OUT["shift_spread_A_pp"] = spreadA; OUT["shift_spread_B_pp"] = spreadB; OUT["shape_dev_pp"] = shape_dev
SH_MEAN = {t: float(np.mean(SHIFT[t]["B"])) for t in A0}
OUT["shift_mean_B_pct"] = SH_MEAN
print(f"    variation of the shift across r = 10-100 h^-1 Mpc: {spreadA:.3f} pp (convention A), "
      f"{spreadB:.3f} pp (convention B)")
print(f"    changing the transfer function entirely (EH98 full -> EH98 no-wiggle) moves the shift by "
      f"{shape_dev:.4f} pp")
print(f"    the headline numbers, convention B: {SH_MEAN['canonical']:+.2f}% (canonical), "
      f"{SH_MEAN['alt']:+.2f}% (alt)")
check("V4 [THE SIGNAL IS A PURE AMPLITUDE AND THEREFORE HAS NO SHAPE HANDLE AGAINST tau] because "
      "G_eff/G = nu(cH(z)/a_0) depends on redshift alone and not on scale, the predicted v_12 shift must be "
      "the same at every separation; the variation of the shift across r = 10-100 h^-1 Mpc is measured and "
      "compared with a 0.3 percentage-point threshold, and the whole transfer function is swapped for an "
      "independently coded one to show the result does not depend on the P(k) shape at all",
      spreadA < 0.3 and spreadB < 0.3 and shape_dev < 0.05,
      f"the shift varies by {spreadA:.3f} pp (A) / {spreadB:.3f} pp (B) over a factor of ten in separation, "
      f"and by {shape_dev:.4f} pp under a complete change of transfer function. THIS IS THE CORE DIFFICULTY, "
      "not a convenience: a constant multiplicative amplitude is exactly what the optical depth tau also is, "
      "so no r-dependence of the measurement can separate them. The small residual in convention A comes "
      "only from the (1 + b^2 xi) pair-weighting denominator")

# ------------------------------------------------------------------ V5: do the clock-frame kicks contaminate kSZ scales?
print("\nV5 -- do L197's clock-frame kicks touch the kSZ scales, as they touch sigma_8 at 8 h^-1 Mpc?")
K197 = np.array([0.2, 0.5, 1.0, 2.0]); R197 = np.array([0.999, 0.989, 0.947, 0.840])   # L197 kicks-only, z=0.3
print("    L197 (FINDINGS.md, 2026-09-12) particle-mesh, kicks only, z = 0.3: P/P_LCDM = "
      + ", ".join(f"{k}:{v}" for k, v in zip(K197, R197)))
lin = interp1d(np.log(K197), np.log(R197), kind="linear", fill_value="extrapolate")
def kick_ratio(mode):
    out = np.ones_like(kk)
    m = kk > K197[0]
    out[m] = np.exp(lin(np.log(kk[m])))
    if mode == "flat":                                                # hold the suppression flat above k = 2
        out[kk > K197[-1]] = R197[-1]
    return np.clip(out, 1e-3, 1.0)
for mode in ("flat", "extrapolated"):
    kr = kick_ratio(mode)
    D2_k = D2_F*kr
    x8 = kk*8.0; W8 = 3*(np.sin(x8) - x8*np.cos(x8))/x8**3
    s8r = np.sqrt(np.sum(D2_k*W8**2*dlnk)/np.sum(D2_F*W8**2*dlnk))
    _, xibk = xi_and_xibar(D2_k, RGRID)
    dv_kick = 100*(xibk/xib0_F - 1)                                   # kicks act on xi_bar; f, D unchanged here
    OUT[f"kick_{mode}_sigma8_ratio"] = float(s8r)
    OUT[f"kick_{mode}_dv12_pct"] = dv_kick.tolist()
    print(f"    [{mode} above k=2] sigma_8 ratio from L197's own P(k) ratios: {s8r:.4f} "
          f"(L197 reported 0.9954 for the kicks alone)")
    print(f"        induced change in v_12: " + ", ".join(f"{r:.0f}:{d:+.2f}%" for r, d in zip(RGRID, dv_kick)))
kr = kick_ratio("flat"); _, xibk = xi_and_xibar(D2_F*kr, RGRID)
dv_kick = 100*(xibk/xib0_F - 1)
kick_at_30 = abs(float(dv_kick[RGRID == 30.][0]))
kick_at_8 = abs(100*(OUT["kick_flat_sigma8_ratio"] - 1))
ratio_dilution = kick_at_8/max(kick_at_30, 1e-6)
OUT["kick_at_r30_pct"] = kick_at_30; OUT["kick_at_8Mpc_pct"] = kick_at_8
OUT["kick_dilution_ratio"] = float(ratio_dilution)
print(f"    the kicks move sigma_8 (8 h^-1 Mpc) by {kick_at_8:.2f}% but v_12 at 30 h^-1 Mpc by only "
      f"{kick_at_30:.2f}% -- a factor {ratio_dilution:.1f} weaker")
check("V5 [kSZ SCALES READ THE KERNEL'S RAISE ALMOST UNDILUTED, WHICH IS WHY THIS PROBE IS WORTH ASKING "
      "ABOUT AT ALL] L197 found the kernel's lift and the clock-frame kicks' suppression cancel at eight "
      "megaparsecs so that S_8 does not discriminate; L197's own P(k) ratios are pushed through the pairwise "
      "integral here and the kick-induced change in v_12 at 30 h^-1 Mpc is compared with the kick-induced "
      "change in sigma_8; a ratio above 3 means the cancellation does not reach the kSZ separations",
      ratio_dilution > 3.0,
      f"the kicks cost {kick_at_8:.2f}% at 8 h^-1 Mpc and {kick_at_30:.2f}% at 30 h^-1 Mpc, a factor "
      f"{ratio_dilution:.1f}. So the framework's distinctive cosmological pattern is a SCALE SPLIT: "
      f"S_8 indistinguishable from LCDM (L197) while the 10-100 Mpc growth is raised "
      f"{SH_MEAN['canonical']:+.1f}% to {SH_MEAN['alt']:+.1f}%. Limit: L197's kick ratios were tabulated at "
      "four wavenumbers in a 100 Mpc/h box and are interpolated here; they are not re-simulated")

# ------------------------------------------------------------------ V6: can current kSZ see it?
print("\nV6 -- THE CENTRAL DIFFICULTY: the optical-depth degeneracy, quantified")
print("     the estimator measures  T_pairwise  proportional to  tau_bar * v_12 : a fractional error on")
print("     tau_bar maps one-for-one onto the inferred v_12, and the framework's signal IS a pure amplitude")
best_snr = max(v for _, v in LIT["pairwise_snr"])
stat_frac = 1.0/best_snr
print(f"    best published PAIRWISE detection: {best_snr:.1f} sigma (Calafut et al. 2021) "
      f"-> statistical fractional error on the amplitude = 1/{best_snr:.1f} = {stat_frac:.1%}")
print(f"    (the 6.5 sigma of Schaan et al. 2021 is a velocity-reconstruction stack, not pairwise: "
      f"{1/LIT['stacked_snr'][1]:.1%} if one is generous and uses it)")
rows = []
for tag in A0:
    d = abs(SH_MEAN[tag])/100.0
    for tname, tfrac in [(n, v) for n, v in [(s.split(",")[0], v) for s, v in LIT["tau_frac"]]]:
        for sname, sfrac in (("current pairwise 5.4 sigma", stat_frac),
                             ("generous stacked 6.5 sigma", 1/LIT["stacked_snr"][1]),
                             ("statistics-free limit", 0.0)):
            tot = np.hypot(sfrac, tfrac)
            rows.append((tag, tname, tfrac, sname, sfrac, tot, d/tot))
print(f"    {'footing':<10} {'tau prior':<28} {'statistics':<28} {'total frac err':>14} {'signal/sigma':>13}")
for r_ in rows:
    print(f"    {r_[0]:<10} {r_[1][:27]:<28} {r_[3]:<28} {r_[5]:14.1%} {r_[6]:13.2f}")
OUT["v6_rows"] = [dict(footing=a, tau_src=b, tau_frac=c, stat_src=d_, stat_frac=e, total=f_, nsigma=g)
                  for a, b, c, d_, e, f_, g in rows]
best_sig = max(r_[6] for r_ in rows)
OUT["v6_best_nsigma"] = float(best_sig)
print(f"    the MOST OPTIMISTIC entry in the whole table -- alt footing, 10% tau, infinite statistics -- "
      f"reaches {best_sig:.2f} sigma")
check("V6 [CURRENT kSZ CANNOT TEST THIS, AND NOT BY A LITTLE] the framework's predicted fractional v_12 "
      "shift is divided by the total fractional amplitude error of a pairwise kSZ measurement, statistical "
      "and optical-depth errors combined in quadrature, over every combination of the published detection "
      "significances and the published tau uncertainties; the threshold for the claim 'current kSZ can see "
      "it' is that the best entry reach 3 sigma",
      best_sig < 3.0,
      f"the best entry in the table reaches {best_sig:.2f} sigma, and that entry already assumes INFINITE "
      f"statistics and the most optimistic 10% optical depth. With the actual best pairwise measurement "
      f"(5.4 sigma, {stat_frac:.0%} statistical) and a 15% tau the significance is "
      f"{[r_[6] for r_ in rows if r_[0]=='canonical' and abs(r_[2]-0.15)<1e-9 and 'current' in r_[3]][0]:.2f} "
      "sigma. THIS IS THE FINDING: the kSZ angle is not a test of this framework today, and the obstacle is "
      "the optical depth, not the photon noise")

# ------------------------------------------------------------------ V7: what would be needed
print("\nV7 -- what it would take: the required tau precision and the required statistics")
for tag in A0:
    d = abs(SH_MEAN[tag])/100.0
    for nsig in (2.0, 3.0):
        tau_need = d/nsig                                             # statistics-free: tau alone must clear it
        snr_need = nsig/d                                             # tau-free: statistics alone must clear it
        nobj = (snr_need/best_snr)**2
        OUT[f"v7_{tag}_{int(nsig)}sig"] = dict(tau_frac_required=float(tau_need),
                                               snr_required=float(snr_need), nobj_factor=float(nobj))
        print(f"    [{tag}] shift {100*d:.2f}%: a {nsig:.0f} sigma statement needs sigma_tau/tau < "
              f"{tau_need:.2%} (with perfect statistics) AND an overall kSZ detection at "
              f"{snr_need:.0f} sigma (with perfect tau) -- naively {nobj:.0f}x the object count of the "
              f"{best_snr:.1f} sigma measurement, since SNR scales as sqrt(N_pairs)")
tau_req = min(OUT[f"v7_{t}_3sig"]["tau_frac_required"] for t in A0)
tau_now = min(v for _, v in LIT["tau_frac"])
gap = tau_now/tau_req
OUT["v7_tau_required_3sig"] = float(tau_req); OUT["v7_tau_gap_factor"] = float(gap)
print(f"    the binding requirement: sigma_tau/tau < {tau_req:.2%}, against an optimistic present-day "
      f"{tau_now:.0%} -- a factor {gap:.0f} in the optical depth alone")
# the one partial handle: the redshift differential, which a redshift-independent tau error cancels out of
for tag in A0:
    ratio_z = (1 + OUT[f"growth_{tag}"]["dfs8_pct"]["0.3"]/100)/(1 + OUT[f"growth_{tag}"]["dfs8_pct"]["1.0"]/100)
    OUT[f"v7_zdiff_{tag}"] = float(100*(ratio_z - 1))
    print(f"    [{tag}] the one partial handle -- the redshift DIFFERENTIAL, which a z-independent tau error "
          f"cancels from: the boost is {OUT[f'growth_{tag}']['dfs8_pct']['0.3']:+.1f}% at z = 0.3 against "
          f"{OUT[f'growth_{tag}']['dfs8_pct']['1.0']:+.1f}% at z = 1.0, a differential of "
          f"{100*(ratio_z-1):+.2f}% -- SMALLER than the signal it was meant to rescue")
check("V7 [THE REQUIREMENT IS STATED, AND IT IS A FACTOR OF SEVERAL IN A SYSTEMATIC NOBODY CONTROLS] the "
      "optical-depth precision needed for a 3 sigma statement about the framework's v_12 shift is solved for "
      "and compared with the most optimistic optical-depth precision the published literature claims; a "
      "factor above 3 means the gap is not closable by better CMB maps",
      gap > 3.0,
      f"sigma_tau/tau < {tau_req:.2%} is required against {tau_now:.0%} claimed at best, a factor {gap:.0f}. "
      "The redshift differential, the only feature of the prediction a constant tau error cannot absorb, is "
      f"{max(abs(OUT[f'v7_zdiff_{t}']) for t in A0):.2f}% -- smaller than the amplitude it would replace, so "
      "it is not a rescue. What WOULD change the verdict is an independent measurement of the electron "
      "column: fast-radio-burst dispersion measures cross-correlated with the same tracers (the Macquart "
      "relation measures the same integral of n_e that tau does, with completely different systematics), or "
      "a jointly calibrated gas profile from tSZ + X-ray + FRB, feeding a CMB-S4-era kSZ measurement. The "
      "photon-noise side is the easy half")

# ------------------------------------------------------------------ V8: the sign, and the S8 direction
print("\nV8 -- the direction of the effect, and how it sits against the S_8 tension")
S8_PLANCK, S8_KIDS, S8_KIDS_E = 0.834, 0.766, 0.020                   # LITERATURE: Planck 2018; Asgari+21 KiDS-1000
sign_v12 = np.sign(SH_MEAN["canonical"])                              # >0 means |v_12| raised: faster infall
S8_F = {t: S8_PLANCK*GR[t][3] for t in A0}
pull_lensing = (S8_KIDS - S8_PLANCK)/S8_KIDS_E                        # negative: the data want LESS growth
print(f"    the framework RAISES the growth rate, so infall is faster and |v_12| is LARGER: "
      f"{SH_MEAN['canonical']:+.2f}% (canonical) / {SH_MEAN['alt']:+.2f}% (alt)")
print(f"    the same kernel raises S_8 to {S8_F['canonical']:.3f} / {S8_F['alt']:.3f} against Planck's "
      f"{S8_PLANCK:.3f}, while KiDS-1000 measures {S8_KIDS:.3f} +- {S8_KIDS_E:.3f} (LITERATURE: Asgari+21)")
print(f"    direct lensing pulls at {pull_lensing:+.1f} sigma relative to Planck -- i.e. DOWNWARD, toward "
      "less growth; the kernel pulls UPWARD. The two probes pull in OPPOSITE directions")
print(f"    but L197's kicks cancel the kernel at 8 h^-1 Mpc, so the FULL framework predicts S_8 ~ LCDM "
      f"(L197: 0.843/0.845 vs LCDM 0.842) while leaving v_12 raised at 10-100 h^-1 Mpc (V5)")
OUT["sign_v12_raised"] = float(sign_v12); OUT["S8_framework"] = {t: float(v) for t, v in S8_F.items()}
OUT["S8_planck"] = S8_PLANCK; OUT["S8_kids"] = S8_KIDS; OUT["pull_lensing_sigma"] = float(pull_lensing)
prod = sign_v12*np.sign(pull_lensing)
OUT["opposite_pull"] = float(prod)
check("V8 [kSZ AND DIRECT LENSING PULL IN OPPOSITE DIRECTIONS, AND THE FRAMEWORK'S OWN SIGNATURE IS A SCALE "
      "SPLIT] the sign of the predicted v_12 shift is multiplied by the sign of the weak-lensing pull "
      "relative to Planck; a product below zero means a kSZ confirmation of raised large-scale growth would "
      "sit against, not with, the low-S_8 direct measurements",
      prod < 0 and ratio_dilution > 3.0,
      f"the v_12 shift is {SH_MEAN['canonical']:+.2f}%/{SH_MEAN['alt']:+.2f}% (UPWARD) while KiDS-1000 sits "
      f"{pull_lensing:+.1f} sigma below Planck (DOWNWARD): product {prod:+.0f}. This is a genuinely useful "
      "consistency statement and it cuts both ways. The framework does NOT resolve the S_8 tension -- it "
      "inherits Planck's side of it (G020, glm53 lane) -- and a future high-precision kSZ that confirmed "
      "raised 10-100 Mpc growth while lensing stayed low would put the framework and LCDM under the SAME "
      "strain, since both would then need scale-dependent growth. The framework's distinctive claim is not "
      "the raise by itself but the SPLIT: LCDM-like at 8 h^-1 Mpc (kernel cancelled by kicks) and raised at "
      "10-100 h^-1 Mpc (kernel alone). That split is the thing to preregister if the tau problem is ever "
      "solved. NOTE the honest cost: the split depends on the clock-frame kicks, which L197 itself records "
      "as carrying a Lyman-alpha forest problem 164x over bound")

# ------------------------------------------------------------------ V9: numerical convergence
print("\nV9 -- numerical convergence of the integrals the verdict rests on")
conv = {}
for nk2, rs2 in ((200000, 0.25), (400000, 0.50), (400000, 0.125)):
    k2 = np.logspace(np.log10(KMIN), np.log10(KMAX), nk2); dl2 = np.log(k2[1]/k2[0])
    x2 = k2*8.0; W2 = 3*(np.sin(x2) - x2*np.cos(x2))/x2**3
    A2 = SIG8_LCDM**2/np.sum(k2**(3+ns)*T_eh98(k2)**2*W2**2*dl2)
    D22 = A2*k2**(3+ns)*T_eh98(k2)**2*np.exp(-(k2*rs2)**2)
    xx = np.outer(RGRID, k2); j1 = (np.sin(xx)/xx - np.cos(xx))/xx
    xib2 = 3.0*np.sum(D22*j1/xx*dl2, axis=1)
    conv[f"nk{nk2}_rs{rs2}"] = float(np.max(np.abs(xib2/xib0_F - 1)))
    print(f"    nk = {nk2}, smoothing = {rs2} h^-1 Mpc: max |xi_bar change| over the r grid = "
          f"{100*conv[f'nk{nk2}_rs{rs2}']:.3f}%")
OUT["convergence"] = conv
worst_conv = max(conv.values())
check("V9 [THE INTEGRALS ARE CONVERGED WHERE IT MATTERS] the volume-averaged correlation function is "
      "recomputed with half the k-samples and with the small-scale Gaussian smoothing doubled and halved, "
      "and the largest change over the separation grid is compared with a 1% threshold; anything larger "
      "would mean the absolute v_12 is not trustworthy (the FRACTIONAL shift cancels this entirely, as V4 "
      "already showed by swapping the whole transfer function)",
      worst_conv < 0.01,
      f"largest change {100*worst_conv:.3f}% under halved sampling and a factor-four range of smoothing")

json.dump(OUT, open(os.path.join(HERE, "L254_results.json"), "w"), indent=1)
print(f"\nL254 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
sys.exit(0 if all(CH) else 1)
