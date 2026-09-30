# -*- coding: utf-8 -*-
"""CFG252 -- hand-check: dark energy as the void-wall expansion difference (the timescape family), against the
framework's tie a0 = kappa c sqrt(G rho_Lambda).  Frozen criteria: ../CFG252_FROZEN_CRITERIA.md (written before this
script).  Phase 1 only: every timescape number is FROM MEMORY, UNVERIFIED (intended citations in the criteria).

Readings (scored separately, never pooled):
  (a) tie by rate  a0 = kappa' c H, kappa' = kappa sqrt(3 Omega_L_eq / 8 pi), kappa = 1/2 FITTED; a-0 / a-1 / a-2 / a-3
  (b) tie by lapse b1 = c^2 Delta/L (spatial), b2 = c d(gamma)/dt (temporal; POST-HOC-FLAGGED, capped at p*)
  (c) environment  c-own (own-clock H, contrast 0 by the premise), c-common (common clock, voids higher), c-local
Gates G-T1 (value vs the SPARC band), G-T2 (environment vs committed limits), G-T3 (a0(z)), G-T4 (premise, memory only).

MUTATE=1: f_v0 -> 0 at fixed dressed H0 (exact Einstein-de Sitter limit).  The premise check L1 must fail (rc 1);
separate outputs *_MUTATE.out / *_results_MUTATE.json.  Reads committed files only; writes only in this directory."""
import os, sys, re, math, json
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = int(os.environ.get("MUTATE", "0"))
TAG = "" if MUTATE == 0 else "_MUTATE"
OUT = open(os.path.join(HERE, "CFG252_handcheck%s.out" % TAG), "w", encoding="utf-8")
CHECKS = []
FAILS = 0


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


def check(cid, statement, measured, ok, lb=True):
    global FAILS
    CHECKS.append(dict(id=cid, ok=bool(ok), load_bearing=lb, statement=statement, measured=str(measured)))
    FAILS += int((not ok) and lb)
    P("  [%s] %s: %s" % ("PASS" if ok else ("FAIL" if lb else "FAIL(reported)"), cid, statement))
    P("         measured: %s" % measured)


# ------------------------------------------------------------------------------------------------ constants
C = 299792458.0
G = 6.67430e-11
MPC = 3.0856775814913673e22
KMS_MPC = 1e3 / MPC                       # 1 km/s/Mpc in s^-1
GYR = 3.15576e16
KAPPA = 0.5                               # FITTED, never derived
KP_TOT = KAPPA * math.sqrt(3.0 / (8.0 * math.pi))       # kappa' for Omega_L_eq = 1 (total density; the alt footing)

# ------------------------------------------------------------------------------------------------ committed inputs (read-only)
FP0 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP0_core_postulates_results.json")))["numbers"]
A0_CAN, A0_ALT, H_LAM = float(FP0["a0_canonical"]), float(FP0["a0_rho_total"]), float(FP0["H_Lambda"])
KAPPA_NOTE = os.path.join(REPO, "real_research", "reviews", "mi_a0_profile_likelihood_milgrom_footing_2026.out")
ENV_JSON = os.path.join(REPO, "prep_2026", "a0_line", "cosmic_web_environment_results.json")
CFG182_JSON = os.path.join(REPO, "campaign_fresh_gravity", "CFG182_a0_sky_dipole", "cfg182_b_dipole_results.json")
OM_PL = 0.3153                             # CFG7_common.OM_PL (Planck 2018), the rival's E(z) as CFG197/CFG213 use it
KAPPA_WINDOWS = (("BTFR", 0.465, 0.076), ("distance-free", 0.55, 0.17))   # CFG0 F3, as CFG117 uses them (rho_Lambda footing)

# ------------------------------------------------------------------------------------------------ literature (FROM MEMORY, UNVERIFIED)
LIT = {
    "P-A": dict(fv0=0.695, H0=61.7, cite="Wiltshire 2009 PRD 80 123512; Duley, Nazer & Wiltshire 2013 CQG 30 175006",
                recalled=dict(Hbar0=50.1, gam0=1.35, OmM_dressed=0.41)),
    "P-B": dict(fv0=0.76, H0=61.7, cite="Leith, Ng & Wiltshire 2008 ApJ 672 L91 (H0 assumed as P-A)",
                recalled=dict(OmM_dressed=0.33, gam0=1.38)),
}
SWEEP_FV = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85]
SWEEP_H0 = [60.0, 61.7, 64.0]
HUBBLE_VARIANCE = (0.01, 0.05)            # fractional local-H variation within ~100 Mpc; Wiltshire, Smale, Mattsson & Watkins 2013 (memory)
L_MPC = (10.0, 30.0, 50.0)                # wall/void scales for b1 (brief: 10-50 Mpc)
DELTA_VOID = (-0.8, -0.9)                 # primary (the record's DELTA_VOID) and variant
BIAS = (1.0, 1.3)                         # 2MRS galaxy-count bias: primary, variant
ZS = (0.85, 1.5, 2.2, 2.5, 5.0)


class Tracker:
    """Timescape tracker solution (criteria section 3, T1-T7; from memory, unverified). Volume-average time t in s.
    fv0 = 0 is the exact Einstein-de Sitter limit (no voids, gamma = 1)."""

    def __init__(self, fv0, H0_kms):
        self.fv0, self.H0 = float(fv0), H0_kms * KMS_MPC
        if self.fv0 == 0.0:
            self.Hb0 = self.H0
            self.t0 = 2.0 / (3.0 * self.H0)
        else:
            self.Hb0 = 2.0 * (2.0 + fv0) * self.H0 / (4.0 * fv0 ** 2 + fv0 + 4.0)
            self.t0 = (2.0 + fv0) / (3.0 * self.Hb0)
        self.A = 3.0 * self.fv0 * self.Hb0
        self.B = (1.0 - self.fv0) * (2.0 + self.fv0)

    def fv(self, t):
        return 0.0 if self.fv0 == 0.0 else self.A * t / (self.A * t + self.B)

    def Hbar(self, t):
        return (2.0 + self.fv(t)) / (3.0 * t)

    def Hw(self, t):
        return 2.0 / (3.0 * t)

    def Hv(self, t):                       # undefined without voids
        return float("nan") if self.fv0 == 0.0 else 1.0 / t

    def gam(self, t):
        return 1.0 + 0.5 * self.fv(t)

    def dgam_dt(self, t):
        f = self.fv(t)
        return f * (1.0 - f) / (2.0 * t)

    def Hd(self, t):
        f = self.fv(t)
        return (4.0 * f * f + f + 4.0) / (6.0 * t)

    def OmM_bare(self, t):
        f = self.fv(t)
        return 4.0 * (1.0 - f) / (2.0 + f) ** 2

    def OmM_dressed(self, t):
        f = self.fv(t)
        return (1.0 - f) * (2.0 + f) / 2.0

    def onepz(self, t):
        if self.fv0 == 0.0:
            return (self.t0 / t) ** (2.0 / 3.0)
        f = self.fv(t)
        return (2.0 + f) * f ** (1.0 / 3.0) / (3.0 * self.fv0 ** (1.0 / 3.0) * self.Hb0 * t)

    def t_of_z(self, z):
        if z == 0:
            return self.t0
        g = lambda lt: math.log(self.onepz(math.exp(lt))) - math.log(1.0 + z)
        return math.exp(brentq(g, math.log(self.t0 * 1e-9), math.log(self.t0), xtol=1e-14, maxiter=500))


def kms(H):
    return H / KMS_MPC


def band_class(a0, S1, S2):
    return dict(in_S1=bool(S1[0] <= a0 <= S1[1]), in_S2=bool(S2[0] <= a0 <= S2[1]))


# ================================================================================================ header
RUN = dict(LIT["P-A"])
if MUTATE == 1:
    RUN = dict(fv0=0.0, H0=LIT["P-A"]["H0"], cite="MUTATE: f_v0 -> 0 at fixed dressed H0 (Einstein-de Sitter)", recalled={})
P("CFG252 hand-check (MUTATE=%d). Parameter set: f_v0 = %.3f, dressed H0 = %.2f km/s/Mpc [%s] -- FROM MEMORY, UNVERIFIED"
  % (MUTATE, RUN["fv0"], RUN["H0"], RUN["cite"]))
P("kappa = 1/2 FITTED. Footings: canonical %.4e, alt %.4e m/s^2 (FP0, committed). Label: NON-DIAGNOSTIC." % (A0_CAN, A0_ALT))

# ================================================================================================ controls
P("\n== C0: the framework's kappa-to-H conversion reproduces FP0 ==")
a0_can_rec = KAPPA * C * H_LAM * math.sqrt(3.0 / (8.0 * math.pi))
H0_chain = A0_ALT / (KP_TOT * C)
OL_chain = (H_LAM / H0_chain) ** 2
check("C0", "a0_can = kappa c H_Lambda sqrt(3/8pi) reproduces FP0 (rel < 1e-9); alt gives H0 = 67.40 and Omega_L = 0.6847",
      "a0_can %.6e vs FP0 %.6e; H0 = %.4f km/s/Mpc; Omega_L = %.5f; kappa'_can = %.5f, kappa'_tot = %.5f"
      % (a0_can_rec, A0_CAN, kms(H0_chain), OL_chain, KAPPA * math.sqrt(3 * OL_chain / (8 * math.pi)), KP_TOT),
      abs(a0_can_rec / A0_CAN - 1) < 1e-9 and abs(kms(H0_chain) - 67.4) < 0.01 and abs(OL_chain - 0.6847) < 5e-4)
KP_CAN = KAPPA * math.sqrt(3.0 * OL_chain / (8.0 * math.pi))

P("\n== C1: the SPARC band, parsed from the committed kappa like-for-like note ==")
rows = []
with open(KAPPA_NOTE, encoding="utf-8") as fh:
    txt = fh.read()
blk = txt.split("a0 [1e-10]   a0/a0_fw        chi2     Dchi2")[1].split("P3  sigma(a0)")[0]
for line in blk.splitlines():
    m = re.match(r"^\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", line)
    if m:
        rows.append(tuple(float(x) for x in m.groups()))
tab = np.array(rows)
a0g, dchi = tab[:, 0] * 1e-10, tab[:, 3]
INFL2 = 3380.0 / 175.0
CUT = 4.0 * INFL2
imin = int(np.argmin(dchi))
lo_i = max(i for i in range(imin) if dchi[i] > CUT)
hi_i = min(i for i in range(imin, len(dchi)) if dchi[i] > CUT)
S1_lo = a0g[lo_i] + (dchi[lo_i] - CUT) / (dchi[lo_i] - dchi[lo_i + 1]) * (a0g[lo_i + 1] - a0g[lo_i])
S1_hi = a0g[hi_i - 1] + (CUT - dchi[hi_i - 1]) / (dchi[hi_i] - dchi[hi_i - 1]) * (a0g[hi_i] - a0g[hi_i - 1])
S1 = (S1_lo, S1_hi)
BEST = a0g[imin]
S2 = (BEST * (1 - 2 * 0.0544), BEST * (1 + 2 * 0.0544))
d_can = float(dchi[np.argmin(abs(a0g - 0.9361e-10))])
check("C1", "committed table parsed: %d rows; minimum at 1.0766e-10 and Dchi2(0.9361e-10) = 63.90" % len(tab),
      "best %.4e, Dchi2(canonical row) %.2f; S1 (Dchi2/%.3f <= 4) = [%.4e, %.4e]; S2 = [%.4e, %.4e]"
      % (BEST, d_can, INFL2, S1[0], S1[1], S2[0], S2[1]),
      len(tab) == 33 and abs(BEST - 1.0766e-10) < 1e-14 and abs(d_can - 63.90) < 1e-6)
KW = {}
for nm, k, s in KAPPA_WINDOWS:
    KW[nm] = ((k - 2 * s) / KAPPA * A0_CAN, (k + 2 * s) / KAPPA * A0_CAN)
    P("  kappa window %-13s %.3f +- %.3f -> a0 2-sigma [%.3e, %.3e] (reported, not verdict-changing)" % (nm, k, s, KW[nm][0], KW[nm][1]))

P("\n== C2: tracker identities T1-T7 (sympy; internal consistency only, not the literature) ==")
t, f0, Hb0 = sp.symbols("t f0 Hb0", positive=True)
A_, B_ = 3 * f0 * Hb0, (1 - f0) * (2 + f0)
fv_ = A_ * t / (A_ * t + B_)
Hb_ = (2 + fv_) / (3 * t)
Hw_, Hv_ = sp.Rational(2, 3) / t, 1 / t
gam_ = 1 + fv_ / 2
abar3 = t ** 2 * (A_ * t + B_)                       # abar^3 up to a constant
ids = {
    "T1 dfv/dt = fv(1-fv)/t": sp.diff(fv_, t) - fv_ * (1 - fv_) / t,
    "T1 fv(t0) = f0": fv_.subs(t, (2 + f0) / (3 * Hb0)) - f0,
    "T2 abar-rate = Hbar": sp.diff(abar3, t) / (3 * abar3) - Hb_,
    "T2 void volume f_v abar^3 ~ t^3": sp.diff(sp.log(fv_ * abar3), t) - 3 / t,
    "T2 Hbar = (1-fv)Hw + fv Hv": Hb_ - ((1 - fv_) * Hw_ + fv_ * Hv_),
    "T3 gamma = Hbar/Hw": gam_ - Hb_ / Hw_,
    "T4 H = gamma Hbar - dgamma/dt = (4fv^2+fv+4)/(6t)": gam_ * Hb_ - sp.diff(gam_, t) - (4 * fv_ ** 2 + fv_ + 4) / (6 * t),
    "T4 H = gamma d/dt ln(abar/gamma)": gam_ * (sp.diff(abar3, t) / (3 * abar3) - sp.diff(gam_, t) / gam_) - (4 * fv_ ** 2 + fv_ + 4) / (6 * t),
    "T6 bare sum rule": (4 * (1 - fv_) + 9 * fv_ - fv_ * (1 - fv_)) / (2 + fv_) ** 2 - 1,
    "T6 dressed OmM = gamma^3 bare OmM": gam_ ** 3 * 4 * (1 - fv_) / (2 + fv_) ** 2 - (1 - fv_) * (2 + fv_) / 2,
    "T6 bare OmM ~ rho_bar/Hbar^2 (ratio t-independent)": sp.diff(sp.simplify((4 * (1 - fv_) / (2 + fv_) ** 2) / (1 / (abar3 * Hb_ ** 2))), t),
    "T7 Hbar0 from dressed H0": ((4 * f0 ** 2 + f0 + 4) / (6 * (2 + f0) / (3 * Hb0))) * 2 * (2 + f0) / (4 * f0 ** 2 + f0 + 4) - Hb0,
}
bad = [k for k, v in ids.items() if sp.simplify(sp.together(v)) != 0]
tr_chk = Tracker(0.695, 61.7)
z_err = []
for tt in (0.05, 0.3, 0.7):
    T = tt * tr_chk.t0
    lhs = tr_chk.onepz(T)
    abar = lambda x: (x ** 2 * (tr_chk.A * x + tr_chk.B)) ** (1 / 3.0)
    rhs = (abar(tr_chk.t0) / tr_chk.gam(tr_chk.t0)) / (abar(T) / tr_chk.gam(T))
    z_err.append(abs(lhs / rhs - 1))
check("C2", "all %d tracker identities hold symbolically; T5 (1+z) equals a(t0)/a(t), a = abar/gamma, numerically" % len(ids),
      "failed identities: %s; T5 max rel error %.1e" % (bad or "none", max(z_err)), not bad and max(z_err) < 1e-12)

P("\n== C3 (reported): the recalled literature sets are internally consistent with the tracker (memory check only) ==")
c3 = {}
for nm, s in LIT.items():
    tr = Tracker(s["fv0"], s["H0"])
    got = dict(Hbar0=kms(tr.Hb0), gam0=tr.gam(tr.t0), OmM_dressed=tr.OmM_dressed(tr.t0), OmM_bare=tr.OmM_bare(tr.t0),
               t0_vol_Gyr=tr.t0 / GYR)
    c3[nm] = got
    P("  %s f_v0 %.3f H0 %.1f -> Hbar0 %.2f, gamma0 %.4f, OmM dressed %.3f, bare %.3f, t0(volume) %.2f Gyr; recalled %s"
      % (nm, s["fv0"], s["H0"], got["Hbar0"], got["gam0"], got["OmM_dressed"], got["OmM_bare"], got["t0_vol_Gyr"], s["recalled"]))
okA = abs(c3["P-A"]["Hbar0"] / 50.1 - 1) < 0.01 and abs(c3["P-A"]["gam0"] - 1.35) < 0.01 and abs(c3["P-A"]["OmM_dressed"] - 0.41) < 0.02
okB = abs(c3["P-B"]["OmM_dressed"] - 0.33) < 0.02 and abs(c3["P-B"]["gam0"] - 1.38) < 0.01
check("C3", "P-A and P-B reproduce the recalled derived values (memory consistency, not literature verification)",
      "P-A %s; P-B %s" % (okA, okB), okA and okB, lb=False)

# ================================================================================================ the run's tracker
TR = Tracker(RUN["fv0"], RUN["H0"])
t0 = TR.t0
P("\n== The run's tracker at z = 0 ==")
Hs = dict(H1=TR.Hd(t0), H2=TR.Hbar(t0), H3=TR.Hv(t0), H4=TR.gam(t0) * TR.Hv(t0), H5=TR.Hw(t0))
HNAME = dict(H1="dressed H0 (wall observer, global)", H2="bare Hbar0 (volume average; own-clock rate everywhere)",
             H3="void rate, volume time (1/t0)", H4="void rate timed by wall clocks (gamma0/t0)", H5="wall rate, volume time (2/(3 t0))")
for k in Hs:
    P("  %s = %8.3f km/s/Mpc   %s" % (k, kms(Hs[k]), HNAME[k]))
P("  f_v0 %.3f; gamma0 %.4f; OmM dressed %.4f; OmM bare %.4f; non-matter share dressed %.4f, bare %.4f; t0(volume) %.3f Gyr"
  % (TR.fv0, TR.gam(t0), TR.OmM_dressed(t0), TR.OmM_bare(t0), 1 - TR.OmM_dressed(t0), 1 - TR.OmM_bare(t0), t0 / GYR))
# numeric round trips on the run's own tracker
rt = max(abs(TR.onepz(TR.t_of_z(z)) / (1 + z) - 1) for z in ZS)
check("C2n", "run's tracker: fv(t0) = f_v0, z(t0) = 0, H_dressed(t0) = input H0, Hbar decomposition, t(z) round trip",
      "fv(t0) %.6f; 1+z(t0) %.12f; Hd(t0) %.4f km/s/Mpc; round-trip max rel %.1e" % (TR.fv(t0), TR.onepz(t0), kms(TR.Hd(t0)), rt),
      abs(TR.fv(t0) - TR.fv0) < 1e-12 and abs(TR.onepz(t0) - 1) < 1e-12 and abs(kms(TR.Hd(t0)) - RUN["H0"]) < 1e-9 and rt < 1e-9)

P("\n== L1 (load-bearing premise): the parameter set is inhomogeneous, so the mutation has something to tie to ==")
check("L1", "f_v0 > 0, a non-matter Friedmann share 1 - OmM > 0 and a lapse gamma0 - 1 > 0",
      "f_v0 %.3f; 1 - OmM_dressed %.4f; gamma0 - 1 %.4f" % (TR.fv0, 1 - TR.OmM_dressed(t0), TR.gam(t0) - 1),
      TR.fv0 > 0 and (1 - TR.OmM_dressed(t0)) > 0 and (TR.gam(t0) - 1) > 0)


# ================================================================================================ readings
def rate_rows(tr, t):
    """All (a) rows and the b rows at time t on tracker tr. Returns dict name -> (a0, meta)."""
    fvt = tr.fv(t)
    omd, omb = tr.OmM_dressed(t), tr.OmM_bare(t)
    Hv = tr.Hv(t)
    novoid = tr.fv0 == 0.0
    R = {}
    R["a-0 literal (Omega_L_eq = 0)"] = (0.0, dict(H="any", kp=0.0))
    for k, H in (("H1", tr.Hd(t)), ("H2", tr.Hbar(t)), ("H3", Hv), ("H4", tr.gam(t) * Hv), ("H5", tr.Hw(t))):
        a = 0.0 if (novoid and k in ("H3", "H4")) else KP_TOT * C * H
        R["a-1 total density x %s" % k] = (a, dict(H=k, kp=KP_TOT))
    R["a-2 non-matter x H1 (dressed, 1-OmM)"] = (KAPPA * math.sqrt(3 * max(1 - omd, 0) / (8 * math.pi)) * C * tr.Hd(t), dict(H="H1", kp=KAPPA * math.sqrt(3 * max(1 - omd, 0) / (8 * math.pi))))
    R["a-2 non-matter x H2 (bare, Omk+OmQ)"] = (KAPPA * math.sqrt(3 * max(1 - omb, 0) / (8 * math.pi)) * C * tr.Hbar(t), dict(H="H2", kp=KAPPA * math.sqrt(3 * max(1 - omb, 0) / (8 * math.pi))))
    R["a-2 non-matter x H3 (void, OmM=0)"] = (0.0 if novoid else KP_TOT * C * Hv, dict(H="H3", kp=KP_TOT))
    R["a-2 non-matter x H4 (void, wall clock)"] = (0.0 if novoid else KP_TOT * C * tr.gam(t) * Hv, dict(H="H4", kp=KP_TOT))
    R["a-2 non-matter x H5 (wall, OmM=1 locally)"] = (0.0, dict(H="H5", kp=0.0))
    for k, H in (("H1", tr.Hd(t)), ("H3", Hv), ("H4", tr.gam(t) * Hv)):
        a = 0.0 if (novoid and k != "H1") else KP_CAN * C * H
        R["a-3 borrowed Omega_L 0.6847 x %s" % k] = (a, dict(H=k, kp=KP_CAN, borrowed=True))
    R["b2 c dgamma/dt (volume time)"] = (C * tr.dgam_dt(t), dict(posthoc=True))
    R["b2 c gamma dgamma/dt (wall time)"] = (C * tr.gam(t) * tr.dgam_dt(t), dict(posthoc=True))
    return R


def classify(a0, twin, meta):
    if not (a0 > 0) or math.isnan(a0):
        return "DIES"
    if abs(math.log10(a0 / A0_CAN)) > 1.0:
        return "DIES"
    if not (S1[0] <= a0 <= S1[1]):
        return "FAIL"
    if meta.get("borrowed") or meta.get("posthoc"):
        return "p*"
    if twin > 0 and abs(twin / a0 - 1) < 0.01:
        return "p*"
    return "PASS(G-T1 only)"


P("\n== (a) and (b2): a0 = kappa' c H (kappa' fixed a priori) and the lapse rate; G-T1 against S1 ==")
TWIN = Tracker(0.0, RUN["H0"])            # the homogeneous twin at the same dressed H0 (the restatement test)
rows_now = rate_rows(TR, t0)
rows_twin = rate_rows(TWIN, TWIN.t0)
READ = {}
P("  %-44s %6s %8s %11s %7s %7s %6s %5s %5s  %s" % ("reading", "H", "kappa'", "a0 [m/s2]", "/can", "/alt", "k_eq", "S1", "S2", "class"))
for nm, (a0, meta) in rows_now.items():
    twin = rows_twin[nm][0]
    cl = classify(a0, twin, meta)
    bc = band_class(a0, S1, S2) if a0 > 0 else dict(in_S1=False, in_S2=False)
    kw = {w: bool(KW[w][0] <= a0 <= KW[w][1]) for w in KW}
    READ[nm] = dict(a0=a0, twin_EdS=twin, meta={k: v for k, v in meta.items()}, cls=cl, **bc, kappa_windows=kw,
                    over_can=a0 / A0_CAN, over_alt=a0 / A0_ALT, kappa_eq_rhoL=KAPPA * a0 / A0_CAN)
    P("  %-44s %6s %8s %11.4e %7.3f %7.3f %6.3f %5s %5s  %s"
      % (nm, meta.get("H", "-"), ("%.5f" % meta["kp"]) if "kp" in meta else "-", a0, a0 / A0_CAN, a0 / A0_ALT,
         KAPPA * a0 / A0_CAN, "in" if bc["in_S1"] else "out", "in" if bc["in_S2"] else "out", cl))
P("  (class p* = restatement: borrowed Omega_L, post-hoc b2, or the same a0 within 1%% in the homogeneous twin; S1 = [%.4e, %.4e])" % S1)

P("\n== robustness sweep over the premise's own literature uncertainty (verdicts stay at the run's set) ==")
fv_list = [0.0] if MUTATE == 1 else SWEEP_FV
sweep = {nm: {} for nm in READ}
for fv0 in fv_list:
    for H0 in SWEEP_H0:
        tr = Tracker(fv0, H0)
        tw = Tracker(0.0, H0)
        rn, rw = rate_rows(tr, tr.t0), rate_rows(tw, tw.t0)
        for nm in READ:
            cl = classify(rn[nm][0], rw[nm][0], rn[nm][1])
            sweep[nm][cl] = sweep[nm].get(cl, 0) + 1
            sweep[nm].setdefault("_a0", []).append(rn[nm][0])
for nm in READ:
    a0s = [x for x in sweep[nm].pop("_a0") if x > 0]
    counts = dict(sweep[nm])
    READ[nm]["sweep_counts"] = counts
    READ[nm]["sweep_a0_range"] = [min(a0s), max(a0s)] if a0s else [0.0, 0.0]
    READ[nm]["parameter_dependent"] = len(counts) > 1
    P("  %-44s a0 range [%.3e, %.3e]; classes %s%s" % (nm, READ[nm]["sweep_a0_range"][0], READ[nm]["sweep_a0_range"][1], counts,
                                                      "  -> PARAMETER-DEPENDENT" if len(counts) > 1 else ""))

P("\n== (b1): spatial lapse gradient a = c^2 Delta / L ==")
B1 = []
novoid = TR.fv0 == 0.0
for dn, D in (("gamma0 - 1 (wall vs volume average)", TR.gam(t0) - 1), ("Hv/Hw - 1 (wall vs void)", 0.0 if novoid else TR.Hv(t0) / TR.Hw(t0) - 1)):
    for L in L_MPC:
        a = C ** 2 * D / (L * MPC)
        dv = a * GYR / 1e3
        cl = "DIES" if (a <= 0 or abs(math.log10(a / A0_CAN)) > 1) else ("FAIL" if not (S1[0] <= a <= S1[1]) else "PASS(G-T1 only)")
        B1.append(dict(Delta=dn, D=D, L_Mpc=L, a=a, over_can=a / A0_CAN, dex=(math.log10(a / A0_CAN) if a > 0 else None), dv_1Gyr_kms=dv, cls=cl))
        P("  %-38s Delta %.4f L %4.0f Mpc: a = %.3e m/s^2 = %9.2f a0_can (%s dex); dv in 1 Gyr = %.3e km/s; %s"
          % (dn, D, L, a, a / A0_CAN, ("%+.2f" % math.log10(a / A0_CAN)) if a > 0 else "-inf", dv, cl))
P("  (reported only: observed void outflows are a few hundred km/s -- from memory, unverified; c = 3.0e5 km/s)")

P("\n== (c) environment ==")
ENV = json.load(open(ENV_JSON))
prim = ENV["slopes"]["2M++ real-space|CLEAN (z-indep)"]
sec = ENV["slopes"]["2MRS counts|CLEAN (z-indep)"]
n_void_clean = ENV["counts"]["clean_deep_voids"]
ratio_vw = 1.0 if novoid else TR.Hv(t0) / TR.Hw(t0)
dlog_vw = math.log10(ratio_vw)
dw = TR.fv0 / (1 - TR.fv0)
GT2 = []
P("  c-own   : own-clock H is Hbar in every region (tracker postulate) -> contrast 0 (p*, premise-enforced); its a0 is the H2 rows above")
P("  c-common: void/wall a0 ratio Hv/Hw = %.4f -> voids higher by %+.4f dex; two-phase delta_w = f_v0/(1-f_v0) = %.4f" % (ratio_vw, dlog_vw, dw))
P("  c-local : wall regions have OmM = 1 locally -> Omega_L_eq,wall = 0 -> a0 = 0 where the idealised model puts every galaxy: DIES" if not novoid
  else "  c-local : no voids: a0 = 0 everywhere under the non-matter tie: DIES")
for dv_ in DELTA_VOID:
    s_pred = 0.0 if novoid else -dlog_vw / (math.log10(1 + dw) - math.log10(1 + dv_))
    for lim_nm, lim, bset in (("2M++ clean (primary)", prim, (1.0,)), ("2MRS clean (secondary)", sec, BIAS)):
        for b in bset:
            sp_ = s_pred / b
            z = (sp_ - lim["slope"]) / lim["se"]
            cls = "FAIL" if abs(z) >= 3 else ("TENSION" if abs(z) >= 2 else "CONSISTENT")
            under = abs(sp_) / lim["se"] < 2
            GT2.append(dict(delta_void=dv_, limit=lim_nm, bias=b, pred_slope=sp_, meas=lim["slope"], se=lim["se"], N=lim["N"], z=z,
                            cls=cls, underpowered=bool(under)))
            P("  c-common delta_v %.1f  %-22s b=%.1f: predicted slope %+.4f vs %+.4f +- %.4f (N=%d): z = %+.2f -> %s%s"
              % (dv_, lim_nm, b, sp_, lim["slope"], lim["se"], lim["N"], z, cls, ", UNDERPOWERED" if under else ""))
P("  the record's clean sample has %d deep-void galaxies (committed); N needed for 3 sigma on the alt-sized slope: %d (committed)"
  % (n_void_clean, ENV["power"]["N_needed_3sig_alt"]))
P("  rho_local exclusion (13 sigma SBeff, ~34 sigma kNN, ~7.5 sigma UMa; slope +0.5): opposite sign to c-common -> N/A (reported)")
P("  SPARC-self kNN slope -0.010 +- 0.015: not mapped (kNN density among SPARC galaxies is not 1+delta of matter) -> reported only")
A95 = json.load(open(CFG182_JSON))["numbers"]["upper_limit"]["A95"]
dip_cls = "CONSISTENT, NON-DIAGNOSTIC" if HUBBLE_VARIANCE[1] < A95 / 2 else "check"
P("  sky dipole: a rate-tied a0 inherits a local-H anisotropy of %.2f-%.2f (memory, unverified) vs CFG182 A95 = %.3f -> %s"
  % (HUBBLE_VARIANCE[0], HUBBLE_VARIANCE[1], A95, dip_cls))
P("  global void-rate ties (a-1/a-2 x H3, H4): every galaxy reads the cosmic void rate -> contrast 0 by construction; read locally they")
P("  become c-common, and a wall galaxy then reads the wall rate (the a-1 x H5 row).")

P("\n== reported only: the 'slip' as a differential expansion speed (Hv - Hw) R ==")
SLIP = []
for R_ in (10.0, 30.0):
    v_vol = 0.0 if novoid else (TR.Hv(t0) - TR.Hw(t0)) * R_ * MPC / 1e3
    v_wall = v_vol * TR.gam(t0)
    SLIP.append(dict(R_Mpc=R_, v_volume_kms=v_vol, v_wallclock_kms=v_wall))
    P("  R = %4.0f Mpc: %.1f km/s (volume time), %.1f km/s (wall clocks)" % (R_, v_vol, v_wall))

P("\n== G-T3: a0(z)/a0(0) for each reading with a0 > 0, vs flat (1) and the rival E(z) (Om = %.4f) ==" % OM_PL)
E = lambda z: math.sqrt(OM_PL * (1 + z) ** 3 + 1 - OM_PL)
GT3 = {}
tz = {z: TR.t_of_z(z) for z in ZS}
hdr = "  %-44s" % "reading" + "".join(" z=%-5s" % z for z in ZS) + "  class@1.5   z=5 vs E(5)"
P(hdr)
P("  %-44s" % "rival E(z) [dex]" + "".join(" %+7.3f" % math.log10(E(z)) for z in ZS))
for nm in READ:
    if READ[nm]["a0"] <= 0:
        continue
    vals = []
    for z in ZS:
        rz = rate_rows(TR, tz[z])[nm][0]
        vals.append(math.log10(rz / READ[nm]["a0"]))
    d15 = vals[ZS.index(1.5)]
    cls = "flat-like" if abs(d15) <= 0.05 else ("rising" if d15 > 0.05 else "falling")
    if cls == "rising":
        cls += " (rival-like)" if abs(d15 - math.log10(E(1.5))) <= 0.1 else (" (steeper than rival)" if d15 > math.log10(E(1.5)) else " (shallower than rival)")
    d5 = vals[ZS.index(5.0)]
    inherit = "INHERITS CFG213" if d5 >= math.log10(E(5.0)) - 0.1 else ("partially bears" if d5 > 0 else "-")
    GT3[nm] = dict(dlog=dict(zip([str(z) for z in ZS], vals)), cls=cls, cfg213=inherit)
    P("  %-44s" % nm + "".join(" %+7.3f" % v for v in vals) + "  %-24s %s" % (cls, inherit))
flat_any = any(v["cls"] == "flat-like" for v in GT3.values())
P("  dressed H(z)/H0 vs LCDM E(z): " + ", ".join("z=%s: %.3f vs %.3f" % (z, TR.Hd(tz[z]) / TR.Hd(t0), E(z)) for z in ZS))
P("  any reading flat-like: %s%s" % (flat_any, "" if flat_any else " -> the premise swap FORFEITS the framework's distinctive flat a0(z)"))
P("  committed a0(z) results bearing: KURVS z~1.5 lean to the rival, fragile and calibration-bound (CFG140-194); CFG213 z~5 rival")
P("  DISFAVOURED-under on the fit route, ROUTE-DEPENDENT; z~1.4 no separation; CFG197 z>3.5 both consistent (one-sided); CFG196")
P("  z~2.2 cannot discriminate; MUSE-DARK nothing established (CFG190/198). Grade for every reading: NOT DECIDED.")

P("\n== G-T4: premise (from memory, unverified; not tested here) -> PREMISE CONTESTED; see README for the list ==")

# ================================================================================================ headline
in_band = [nm for nm, r in READ.items() if r["cls"] in ("p*", "PASS(G-T1 only)")]
passes = [nm for nm, r in READ.items() if r["cls"] == "PASS(G-T1 only)"]
restate = [nm for nm, r in READ.items() if r["cls"] == "p*"]
dies = [nm for nm, r in READ.items() if r["cls"] == "DIES"] + (["b1 (all cells)"] if all(b["cls"] == "DIES" for b in B1) else []) + ["c-local"]
fails = [nm for nm, r in READ.items() if r["cls"] == "FAIL"]
prim_rows = [g for g in GT2 if g["limit"].startswith("2M++") and g["delta_void"] == DELTA_VOID[0]]
P("\n== HEADLINE (MUTATE=%d) ==" % MUTATE)
# distinct PASS values (a-1 and a-2 coincide on the void rows by construction: OmM = 0 in a void gives kappa' = kappa'_tot)
pv = {}
for nm in passes:
    pv.setdefault(round(READ[nm]["a0"], 16), []).append(nm)
pass_txt = []
for v, nms in sorted(pv.items()):
    r = READ[nms[0]]
    m_lo, m_hi = v / S1[0] - 1, v / S1[1] - 1
    pass_txt.append("%.4e = %.3f a0_can (%s; S1 margin %+.1f%% / %+.1f%%; in S1 in %d of %d sweep cells%s)"
                    % (v, v / A0_CAN, " and ".join(nms), 100 * m_lo, 100 * m_hi, r["sweep_counts"].get("PASS(G-T1 only)", 0),
                       sum(r["sweep_counts"].values()), ", PARAMETER-DEPENDENT" if r["parameter_dependent"] else ""))
a1h1 = READ["a-1 total density x H1"]["a0"]
if MUTATE == 0:
    HL = ("HEADLINE: at P-A, PASS(G-T1 only) at %d distinct value(s): %s. p* = [%s] (a-1 x H1 is the a0/(cH0) coincidence: "
          "unchanged in the homogeneous twin). FAIL = %d rows; DIES = [%s]. c-common: %s%s on the primary limit. "
          "Every reading with a0 > 0 RISES with z (no reading flat-like: %s). G-T4 PREMISE CONTESTED. NON-DIAGNOSTIC."
          % (len(pv), " | ".join(pass_txt) or "none", "; ".join(restate) or "none", len(fails), "; ".join(dies),
             prim_rows[0]["cls"], ", UNDERPOWERED" if prim_rows[0]["underpowered"] else "", not flat_any))
else:
    HL = ("HEADLINE (MUTATE, f_v0 -> 0): no voids, no lapse, no non-matter share: every a-2 row, b1, b2, c-common and c-local "
          "give 0 and the void-rate rows vanish; the premise check L1 FAILS. The only in-band rows are [%s], all equal to "
          "a-1 x H1 = %.4e, the same value the inhomogeneous run gives for that row: the a0/(cH0) coincidence in an "
          "Einstein-de Sitter universe. Without the void-wall structure the tie has nothing timescape-specific to tie to."
          % ("; ".join(in_band) or "none", a1h1))
P(HL)

n = len(CHECKS)
npass = sum(1 for c_ in CHECKS if c_["ok"])
P("\nSUMMARY CFG252 (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d" % (MUTATE, npass, n, FAILS))
json.dump(dict(lane="CFG252", mutate=MUTATE, parameter_set=RUN, label="NON-DIAGNOSTIC", kappa="1/2 FITTED",
               footings=dict(canonical=A0_CAN, alt=A0_ALT), S1=list(S1), S2=list(S2), best=BEST, kappa_windows=KW,
               H_kms={k: kms(v) for k, v in Hs.items()}, readings=READ, b1=B1, gt2=GT2, clean_deep_voids=n_void_clean,
               dipole=dict(A95=A95, input=HUBBLE_VARIANCE, cls=dip_cls), slip=SLIP, gt3=GT3, flat_any=flat_any,
               c3=c3, headline=HL, checks=CHECKS),
          open(os.path.join(HERE, "CFG252_handcheck_results%s.json" % TAG), "w"), indent=1, default=str)
OUT.close()
sys.exit(1 if FAILS else 0)
