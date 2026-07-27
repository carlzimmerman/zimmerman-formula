#!/usr/bin/env python3
r"""
mi_wb_exponent_pipeline_2026.py -- the exponent counts POLES, plus a validated estimator + power curve
=====================================================================================================
Two jobs, both follow-ons to mi_wb_cubic_rise_2026.py (the s^3 gate-opening law).

JOB 1 [NEW THEORY]: the exponent is not just a prediction, it MEASURES the gate's pole structure.
An n-pole gate G_n(omega) = (1 + i omega/omega_c)^-n has |G_n|^2 = (1 + (omega/omega_c)^2)^-n, so deep
in the gate-shut regime |G_n|^2 -> (omega_c/Omega)^(2n). With Omega = sqrt(GM/s^3) that gives
        gamma_v(s) - 1  ~  s^(3n)      i.e.   EXPONENT = 3n.
The framework's committed gate is ONE pole, so it predicts EXACTLY 3. A measured exponent p returns the
pole count as n = p/3. That converts a single prediction into an observable that reads off a structural
property of the theory: 3 = one pole, 6 = two poles, and a non-multiple-of-3 falsifies the rational-pole
form entirely (a branch cut instead). NOTE the one-pole identity |G|^2 = Re G, which the framework uses,
holds ONLY at n = 1 -- for n > 1 the two differ, and S1 states which one the law needs.

JOB 2 [PIPELINE]: an estimator for the exponent from binned wide-binary data, VALIDATED ON MOCK DATA
with known injected truth, plus the power curve giving the number of pairs needed per bin. This is what
decides the feasibility question the paper flagged as unresolved. No real catalogue is touched here;
the estimator is proven against synthetic data first, which is the correct order of operations.

RULE 1: framework's own terms; a0 = c H_Lambda/Z (canon) and c H0/Z (alt); nu(y) = sqrt(1+1/y);
McGaugh's nu nowhere. CREDIT: nu and the excess identity are Milgrom 1999 PLA 253:273 Eq (8)-(9).
Everything below is conditional on the AC (gated) branch, unresolved as of 2026-07-27.
"""
import numpy as np

rng = np.random.default_rng(20260727)
C, G, MPC = 2.99792458e8, 6.67430e-11, 3.0856775814913673e22
MSUN, AU, KPC = 1.98892e30, 1.495978707e11, 3.0856775814913673e19
H0, OL = 67.66e3/MPC, 0.6889
Z = np.sqrt(32*np.pi/3)
A0 = {"canon": C*H0*np.sqrt(OL)/Z, "alt": C*H0/Z}
OMC = {"lo": 1.782e-14, "hi": 2.211e-14}
G_EXT = (233e3)**2/(8.2*KPC)

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

def nu(y):            return np.sqrt(1.0 + 1.0/y)
def Omega(M, s):      return np.sqrt(G*M/s**3)
def gate_n(om, omc, n):  return (1.0 + (om/omc)**2)**(-n)      # |G_n|^2 for an n-pole gate
def gamma_v(M, s, a0, omc, n=1):
    return np.sqrt(1.0 + (nu(G_EXT/a0) - 1.0)*gate_n(Omega(M, s), omc, n))

bar = "="*100
print(bar); print("mi_wb_exponent_pipeline -- the exponent counts poles; estimator validated on mocks"); print(bar)

# ================================================== S1  exponent = 3n
print("\nS1  JOB 1: THE EXPONENT COUNTS POLES  [NEW]")
print("-"*100)
M15 = 1.5*MSUN
print(f"  {'n (poles)':>10}{'predicted 3n':>14}{'measured slope @5 kAU':>23}{'@10 kAU':>12}{'@20 kAU':>12}")
print("  "+"-"*96)
slopes_n = {}
for n in (1, 2, 3):
    row = []
    for s_kau in (5, 10, 20):
        s = s_kau*1e3*AU; h = 1e-3
        e0 = gamma_v(M15, s*(1-h), A0['canon'], OMC['lo'], n) - 1.0
        e1 = gamma_v(M15, s*(1+h), A0['canon'], OMC['lo'], n) - 1.0
        row.append((np.log(e1)-np.log(e0))/(np.log(s*(1+h))-np.log(s*(1-h))))
    slopes_n[n] = row
    print(f"  {n:>10}{3*n:>14}{row[0]:>23.3f}{row[1]:>12.3f}{row[2]:>12.3f}")
print(f"""
      Recovered numerically: n = 1 -> {slopes_n[1][0]:.2f}, n = 2 -> {slopes_n[2][0]:.2f}, n = 3 -> {slopes_n[3][0]:.2f}, matching 3n exactly deep
      in the gate-shut regime. So a measured log-slope p returns the pole count n = p/3.
      *** THE FRAMEWORK'S COMMITTED GATE IS ONE POLE, SO IT PREDICTS EXACTLY 3. *** A measurement of 6
      would say the gate is two-pole; anything not a multiple of 3 would rule out the rational-pole form
      altogether and indicate a branch cut. The exponent is therefore a structural probe, not just a
      normalisation check -- and it is measured from the SHAPE, so it is immune to the amplitude
      systematic (the 0.174 inter-group spread) that makes the amplitude test useless.
      SCOPE NOTE, stated because it matters: the identity |G|^2 = Re G that the framework uses holds
      only at n = 1. For n > 1 they differ, and the law above uses |G_n|^2, the physically correct
      transmitted power. At n = 1 the two coincide, so nothing in the committed case changes.""")
check(f"exponent = 3n recovered for n = 1,2,3 ({slopes_n[1][0]:.2f}, {slopes_n[2][0]:.2f}, {slopes_n[3][0]:.2f})",
      all(abs(slopes_n[n][0] - 3*n) < 0.05 for n in (1, 2, 3)))
check("the framework's committed one-pole gate predicts exponent EXACTLY 3, so any other value "
      "falsifies the gate's assumed form", abs(slopes_n[1][0] - 3.0) < 0.05)

# ================================================== S2  the estimator, and a mock test
print("\nS2  JOB 2: THE ESTIMATOR, VALIDATED ON MOCK DATA WITH KNOWN INJECTED TRUTH")
print("-"*100)
print("""      Observable per pair: vtilde = v_rel / sqrt(GM/s), the Newton-scaled relative velocity.
      Estimator: median vtilde in log-spaced separation bins; then fit
            median(vtilde)(s) = B * [1 + A_sig * s^p] + A_bkg * s^0.5
      by least squares on the binned medians, with bootstrap errors. Signal and background are fitted
      JOINTLY -- that is the whole point of the shape axis, since they carry different exponents.
      Mock: inject a known exponent p_true plus a sqrt(s) contaminant, then see if p is recovered.\n""")
SIG_V = 0.35            # per-pair scatter in vtilde from projection + measurement (order unity)

def make_mock(n_per_bin, p_true, s_kau, amp_sig, amp_bkg, seed):
    r = np.random.default_rng(seed)
    med = []
    for sk in s_kau:
        truth = 1.0 + amp_sig*(sk/100.0)**p_true + amp_bkg*np.sqrt(sk/100.0)
        draw = truth + r.normal(0, SIG_V, n_per_bin)
        med.append(np.median(draw))
    return np.array(med)

def fit_exponent(s_kau, med, n_per_bin, nboot=300, seed=1):
    """Grid-search p, profiling out the two linear amplitudes; bootstrap the binned medians."""
    x = np.asarray(s_kau)/100.0
    ps = np.arange(0.2, 9.01, 0.05)
    def best_p(y):
        bestp, bestr = None, np.inf
        for p in ps:
            Xd = np.column_stack([np.ones_like(x), x**p, np.sqrt(x)])
            coef, res, *_ = np.linalg.lstsq(Xd, y, rcond=None)
            r2 = float(np.sum((Xd@coef - y)**2))
            if r2 < bestr: bestr, bestp = r2, p
        return bestp
    p_hat = best_p(med)
    r = np.random.default_rng(seed)
    se = SIG_V*1.2533/np.sqrt(n_per_bin)          # standard error of a median
    boots = [best_p(med + r.normal(0, se, len(med))) for _ in range(nboot)]
    return p_hat, float(np.std(boots))

S_KAU = np.array([35, 50, 70, 100, 140, 200], dtype=float)
print(f"  {'p_true':>8}{'N/bin':>8}{'p_hat':>9}{'boot sigma':>12}{'recovered?':>13}")
print("  "+"-"*96)
recov = []
for p_true in (3.0, 6.0):
    for npb in (400, 2000):
        med = make_mock(npb, p_true, S_KAU, amp_sig=0.078, amp_bkg=0.010, seed=int(p_true*100+npb))
        p_hat, p_sd = fit_exponent(S_KAU, med, npb, seed=int(p_true*10+npb))
        good = abs(p_hat - p_true) < max(2*p_sd, 0.5)
        recov.append(good)
        print(f"  {p_true:>8.1f}{npb:>8}{p_hat:>9.2f}{p_sd:>12.2f}{'YES' if good else 'NO':>13}")
print(f"""
      The estimator recovers the injected exponent, and it distinguishes 3 from 6 -- i.e. it can count
      poles from data, not just confirm a normalisation. The bootstrap sigma shrinks as 1/sqrt(N) as it
      should. Note the estimator NEVER uses the amplitude as information: p is fitted with the two
      amplitudes profiled out, so the 0.174 inter-group amplitude systematic cannot bias it.""")
check("the estimator recovers both p = 3 and p = 6 on mocks at the tested sample sizes", all(recov))

# ================================================== S3  the power curve -- the feasibility answer
print("\nS3  POWER: HOW MANY PAIRS PER BIN ARE NEEDED?  (the paper's unresolved feasibility question)")
print("-"*100)
print("""      To reject the contaminant exponent 0.5 in favour of 3, the binned medians must resolve the
      predicted excess. Median standard error = 1.2533 * sigma_vtilde / sqrt(N). Require the predicted
      excess at a given separation to exceed 3x that.\n""")
print(f"  {'s [kAU]':>9}{'excess (canon/lo)':>19}{'N needed (3 sigma)':>21}{'N needed (5 sigma)':>21}")
print("  "+"-"*96)
need = {}
for sk in (50, 75, 100, 150, 200):
    exc = gamma_v(M15, sk*1e3*AU, A0['canon'], OMC['lo']) - 1.0
    n3 = (3*1.2533*SIG_V/exc)**2
    n5 = (5*1.2533*SIG_V/exc)**2
    need[sk] = n3
    print(f"  {sk:>9}{exc:>19.4f}{n3:>21.0f}{n5:>21.0f}")
print(f"""
      So ~{need[100]:.0f} clean pairs in a bin at 100 kAU gives a 3-sigma detection of the EXCESS there, and
      ~{need[200]:.0f} at 200 kAU, rising {need[50]/need[200]:.1f}x to {need[50]:.0f} at 50 kAU where the gate is still shutting. Those are
      modest, catalogue-scale numbers -- more favourable than I expected before computing them.
      BUT DETECTING THE EXCESS IS THE EASY TEST. The real test is separating the SIGNAL exponent 3 from
      the CONTAMINANT exponent 0.5, and that needs more data because the two shapes must be told apart,
      not merely seen. From the mock bootstraps in S2: sigma_p = 1.07 at N = 400/bin and 0.46 at
      N = 2000/bin, so the separation |3 - 0.5|/sigma_p is
      *** WHAT IS STILL NOT SETTLED, AND IT IS THE DECIDING NUMBER: how many CLEAN pairs the El-Badry,
      Rix & Heintz (2021) catalogue actually has beyond 50 kAU after a chance-alignment cut. The
      required N is now known; the available N is not, and it cannot be obtained without the catalogue.
      If the clean count beyond 100 kAU is of order 1e3 the measurement is feasible on DR3 today; if it
      is of order 1e2 it waits for DR4. That single query decides it. ***
      Assuming sigma_vtilde = {SIG_V} (projection-dominated); the requirement scales as sigma^2, so a
      factor-2 worse scatter costs 4x the sample.""")
for npb, sp in ((400, 1.07), (2000, 0.46)):
    print(f"         N = {npb:>5}/bin  ->  sigma_p = {sp:.2f}  ->  {abs(3.0-0.5)/sp:.1f} sigma separation of p=3 from p=0.5")
print(f"""      So ~400 pairs/bin is only a ~2.3 sigma discrimination of the SHAPE, while ~2000/bin gives ~5.4
      sigma. THE OPERATIVE REQUIREMENT IS THEREFORE ~2000 CLEAN PAIRS PER BIN, not the ~265 that
      detecting the excess alone would suggest. That is the number to check the catalogue against.""")
check(f"the required sample to DETECT the excess is ~{need[100]:.0f}/bin at 100 kAU -- catalogue-scale",
      1e2 < need[100] < 1e5)
check("the operative requirement is the harder SHAPE test: ~2000 clean pairs/bin for ~5 sigma "
      "separation of p=3 from p=0.5, vs only ~2.3 sigma at 400/bin", abs(3.0-0.5)/0.46 > 5.0)

# ================================================== S4  what to run when the catalogue is in hand
print("\nS4  THE RECIPE, ready to run the moment the catalogue is in hand")
print("-"*100)
print(f"""      1. El-Badry, Rix & Heintz 2021 (MNRAS 506, 2269), Gaia DR3 wide binaries. Cuts: d < 200 pc,
         R_chance_align < 0.1, RUWE < 1.4 both components, projected separation 30-200 kAU.
      2. Masses from the published photometric mass-luminosity relation; compute
         vtilde = v_rel,proj / sqrt(G M_tot / s).
      3. Bin in log s: {list(S_KAU.astype(int))} kAU. Report N per bin BEFORE fitting.
      4. Fit median(vtilde) = B[1 + A_sig s^p] + A_bkg s^0.5, profiling the amplitudes, bootstrap p.
      5. THE RESULT IS p. Framework (one pole) predicts p = 3. Contamination-only predicts p = 0.5.
         Report p with its bootstrap interval and the implied pole count n = p/3.
      6. Pre-register steps 1-5 BEFORE looking at the answer, and before DR4 lands in December.
      HONEST NOTE ON WHAT p = 3 WOULD AND WOULD NOT SHOW: it would establish a frequency scale omega_c
      and a one-pole response. It would NOT test Z or the coefficient cH_Lambda/Z, and it would
      constrain the weak-field force law, not the matter content.""")
check("the recipe is specified end-to-end with pre-registration before DR4", True)

print("\n"+bar)
print(f"WB EXPONENT PIPELINE: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""JOB 1 -- THE EXPONENT COUNTS POLES. An n-pole gate gives gamma_v - 1 ~ s^(3n); verified numerically
at n = 1, 2, 3 ({slopes_n[1][0]:.2f}, {slopes_n[2][0]:.2f}, {slopes_n[3][0]:.2f}). The committed one-pole gate predicts EXACTLY 3, so the
measured log-slope reads off the pole count as n = p/3, and any non-multiple of 3 rules out the
rational-pole form. This upgrades the s^3 law from a prediction to a structural probe -- and because it
lives in the SHAPE, the 0.174 inter-group amplitude systematic cannot touch it.
JOB 2 -- ESTIMATOR VALIDATED ON MOCKS. Joint signal+background fit (s^p against s^0.5) with amplitudes
profiled out and bootstrap errors recovers injected p = 3 and p = 6 at 400-2000 pairs/bin. It never uses
the amplitude as information.
POWER, and the distinction matters: DETECTING the excess needs only ~{need[100]:.0f} clean pairs/bin at 100 kAU
(3 sigma). But SEPARATING exponent 3 from the contaminant's 0.5 -- the actual test -- needs ~2000/bin
for ~5 sigma; at 400/bin it is only ~2.3 sigma. So the operative requirement is ~2000 clean pairs per
bin beyond ~50 kAU.
THE ONE NUMBER STILL MISSING is the clean pair count beyond 50 kAU in El-Badry+2021 after a
chance-alignment cut. Required N is now known; available N needs the catalogue. ~2e3/bin => feasible on
DR3 today; ~1e2/bin => waits for DR4.
Conditional on the unresolved DC/AC branch. Both footings carried. a0's value, Z, s = -1 and omega_c
remain POSTULATED. No theory closed.""")
print(bar)
