#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG26 -- THE INFALL WITH THE GALAXY'S OWN SURROUNDINGS: does spherical collapse from the CONSTRAINED mean initial profile (the
peak's own correlated environment, not a power-law seed) reproduce KiDS's outer signal -- for a standard halo, and for the framework?

WHY.  CFG25 re-ran FG016's collapse engine (power-law seeds) and scored it as a standard halo.  It misses KiDS's outer signal
(R >= 0.6 Mpc) for standard halos too: best chi^2 149-173 against 99-105 for good fits.  So the KiDS side of FG016's kill of the
inflow-derived edge -- the computed answer to "where does the cold fluid go?" -- is not framework-specific.  The untested
ingredient is the surroundings the fluid falls in from.  The constrained mean linear profile around a region of mass M that turns
around at z_l,
      dL(<q) = dL_ta sigma^2(q, R) / sigma^2(R, R)      (CFG7_common.ics_constrained),
is the linear-theory expectation of a peak's own surroundings.  It carries the correlated environment a power-law seed lacks, and
it fixes the accretion rate from the cosmology (no scan).  The same engine (reading N: collisionless; FG016's angular momentum,
seeds, shells, integrator) evolves those surroundings nonlinearly to z_l = 0.25.

THE TWO PROFILES, scored with CFG23's exact KiDS fitter (exec'd read-only):
  (S) a STANDARD halo.  The collapse's mean enclosed mass minus the mean density (FG016's convention), held constant past the
      simulation's reach.  The mass scale is free per KiDS bin: runs at M_ta = 1e12 ... 3.2e13 Msun (factors of 2), each scaled
      locally (lambda in 10^[-0.15, 0.15], self-similar).  A = 0 (the collapse's own surroundings carry the outer profile), or
      A in [0, b_Tinker] (CFG23's parallel treatment).
  (F) the FRAMEWORK's profile (FG016's derived profile).  The law inside the splashback caustic (x_sp87 r_ta), the collapse's own
      infall outside, normalised by T5 (the law's enclosed mass at the caustic), no free amplitude.  For each M_b the run whose
      T5 scaling is closest to 1 is used.  A = 0, or A <= 2 (FG016's convention).
  Environments: t_env = 0 (the mean; operative, no constant) and t_env = -1 (a 1-sigma underdense surrounding, the direction
  KiDS's isolation criterion selects; reported).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  the engine with constrained seeds: in every t_env = 0 run the zero-velocity turnaround radius matches the top-hat one
      within 3%, and the guard (crossed shells beyond r_ta) is <= 0.5%.
  C2  CONTROL  CFG23's fitter reproduces BASE (139.800) and CFG21's framework best (104.686).
  H1  [HEADLINE; MUTATE must fail] (S) with the mean environment (t_env = 0, A = 0) fits KiDS within +9 of the framework's best
      (chi^2 <= 113.7).
  H2  [the framework] (F) with the mean environment (t_env = 0, A = 0) fits KiDS within +9 of 104.7, canonical footing, P2 and
      nu_mono.
  READING (declared): H1 FAIL -> spherical collapse cannot reproduce KiDS's outer profile even from the peak's own surroundings;
  no reading for the framework (a non-spherical treatment is needed).  H1 PASS + H2 PASS -> the inflow-derived edge fits KiDS,
  and the collapse conserves mass, so there is no separate budget cost: the budget-vs-KiDS tension (CFG23/24) was the machinery.
  H1 PASS + H2 FAIL -> the tension is real and framework-specific.
  R1  (reported) t_env = -1; A <= b_Tinker for (S), A <= 2 for (F); both footings; the derived edge x_e (T5 closure at Delta_sp87,
      M_b = 6e10) against CFG24's association-level budget edge (0.390 canonical P2); the accretion rates the cosmology gives.
MUTATE=1: (S)'s halo scale capped at log M_ta <= 11.0 -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG26_constrained_infall.py   (MUTATE=1 for the control; ~10 min, 12 processes)
"""
import os, sys, math, json, time, io, contextlib
import numpy as np
from scipy.optimize import brentq
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
NPROC = int(os.environ.get("NPROC", "12"))
R = C7.Report("CFG26_constrained_infall", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: (S)'s halo scale capped at log M_ta <= 11.0 -- H1 must FAIL ***")
np.seterr(all="ignore")
t0 = time.time()
C24 = json.load(open(os.path.join(HERE, "CFG24_budget_associations_results.json")))["numbers"]["edges"]


# ================================================================================================ the pooled collapse job with constrained seeds
def job_constrained(spec):
    """C7.job_pooled's structure (several seeds, pooled splashback, per-seed profiles at a_obs) with C7.ics_constrained seeds."""
    t_ = time.time()
    cos = C7.LCDM
    ao = spec["a_obs"]
    a_end = ao * math.exp(0.12)
    runs = []
    ics = C7.ics_constrained(spec["M_ta_obs"], ao, cos, N=spec["N"], a_i=0.002, span=(3e-3, 12.0), dcap=0.25, t_env=spec["t_env"])
    for sd in spec["seeds"]:
        sn = C7.run_shells(ics, cos, snaps=(ao, a_end), mode="N", jf=(0.15, 0.35), seed=sd, eta=0.03, n_resolve=10 ** 9)
        runs.append({round(x["a"], 6): x for x in sn})
    pairs = [(d[round(ao, 6)], d[round(a_end, 6)]) for d in runs]
    mres = C7.measure_pooled(pairs, ao, cos)
    mres["s_ta"] = C7.s_ta(ics, ao, cos)
    mres["eps_ics"] = ics.get("eps")
    profs = []
    for sn_obs, _ in pairs:
        o = np.argsort(sn_obs["r"]); rs = sn_obs["r"][o]; cm = sn_obs["M_core"] + np.cumsum(sn_obs["m"][o])
        rg = np.geomspace(max(rs[0], 1e-3 * mres["r_ta_dta"]), rs[-1], 600)
        profs.append(dict(r=rg.tolist(), M=np.interp(rg, rs, cm).tolist()))
    mres["profiles"] = profs
    return dict(spec=spec, res=mres, seconds=time.time() - t_)


# ================================================================================================ CFG23's fitter and KiDS machinery (exec'd read-only)
C23P = os.path.join(HERE, "CFG23_lcdm_control.py")
s23 = open(C23P).read()
cut = s23.index("# ================================================================================================ the halo tables")
g23 = {"__file__": C23P, "__name__": "cfg23_prefix"}
_env = os.environ.get("MUTATE")
os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s23[:cut], C23P, "exec"), g23)
if _env is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _env
ns16 = g23["ns"]
GK, FIX, BASE = g23["GK"], g23["FIX"], g23["BASE"]
LM, NPB, RPK, MPCK, MSK, RRK, Rd, Ed, Sd, Ci, DAT, PMd = (g23[k] for k in ("LM", "NPB", "RPK", "MPCK", "MSK", "RRK", "Rd", "Ed", "Sd",
                                                                          "Ci", "DAT", "PMd"))
per_bin, kfit_best, chi2_full, bias_tinker = g23["per_bin"], g23["kfit_best"], g23["chi2_full"], g23["bias_tinker"]
C21, FWB = g23["C21"], g23["FW"]
fw_best = FWB[("canonical", "P2")]

R.banner("C2  CONTROL: CFG23's fitter reproduces BASE and CFG21's framework best")
Tb = ns16["table"](ns16["M_law"](ns16["KERN"]["P2"]), "canonical")
v_a = chi2_full([per_bin(Tb[0][None], np.zeros((1, 4)))[b]["mod"][0] for b in range(4)])
xk = C21["canonical|P2|1.145e+11"]["kids_best_x"]
Tx = ns16["table"](ns16["M_trunc_xta"](ns16["KERN"]["P2"], xk), "canonical")
pbx = per_bin(Tx[0][None], np.array([ns16["caps_at"]("canonical", "P2", xk)]))
v_b = chi2_full([pbx[b]["mod"][0] for b in range(4)])
check("C2 CONTROL: CFG23's fitter reproduces BASE (139.800) and CFG21's framework best (104.686)",
      f"{v_a:.6f} vs {BASE[('canonical', 'P2')]:.6f}; {v_b:.6f} vs {fw_best:.6f}",
      abs(v_a - BASE[("canonical", "P2")]) < 1e-9 and abs(v_b - fw_best) < 1e-6)

# ================================================================================================ the collapse runs
R.banner("THE COLLAPSE RUNS: constrained mean seeds (the peak's own surroundings), reading N, z_l = 0.25 (process pool)")
MRUNS = [1e12, 2e12, 4e12, 8e12, 1.6e13, 3.2e13]
TENV = [0.0, -1.0]
specs = [dict(tag=f"{te}|{M:.1e}", M_ta_obs=M, a_obs=0.8, t_env=te, N=2000, seeds=(7, 8, 9)) for te in TENV for M in MRUNS]
RES = {}
with get_context("fork").Pool(NPROC) as pool:
    for r in pool.imap_unordered(job_constrained, specs):
        RES[(r["spec"]["t_env"], r["spec"]["M_ta_obs"])] = r
        m_ = r["res"]
        P(f"    t_env {r['spec']['t_env']:+.0f} M_ta {r['spec']['M_ta_obs']:.1e} done ({r['seconds']:.0f} s): s = {m_['s_ta']:.2f} (seed slope "
          f"{m_['eps_ics']:.3f}), r_ta {m_['r_ta_dta']:.3f} / zero-velocity {m_['r_ta_zv']:.3f} Mpc, x_sp87 {m_['x_sp87']:.3f}, Delta_sp87 "
          f"{m_['Delta_sp87']:.1f}, M200m {m_['M200m']:.3e}, guard {m_['guard_frac_beyond_rta']:.4f}")
dz = max(abs(RES[(0.0, M)]["res"]["r_ta_zv"] / RES[(0.0, M)]["res"]["r_ta_dta"] - 1) for M in MRUNS)
gd = max(RES[(0.0, M)]["res"]["guard_frac_beyond_rta"] for M in MRUNS)
check("C1 CONTROL: every t_env = 0 run's zero-velocity turnaround radius matches the top-hat one within 3%, guard <= 0.5%",
      f"max |r_zv / r_ta - 1| {dz:.3f}; max guard {gd:.4f}", dz <= 0.03 and gd <= 0.005)

MPC_M = C7.MPC_M
MSUN_KG = 1.98840987e30
RHOM_SIM = float(C7.LCDM.rhom(0.8))
r_mpc = RRK / MPC_M


def mean_profile(te, M):
    m_ = RES[(te, M)]["res"]
    rg = np.geomspace(1e-3, 30.0, 900)
    Ms = [np.interp(rg, np.array(p["r"]), np.array(p["M"]), left=np.nan, right=np.nan) for p in m_["profiles"]]
    with np.errstate(all="ignore"):
        Mm = np.nanmean(np.array(Ms), axis=0)
    ok = np.isfinite(Mm)
    return rg[ok], Mm[ok], m_


# ================================================================================================ (S) the standard halo
R.banner("(S)  THE STANDARD HALO: the collapse's own interior and surroundings, mass free per KiDS bin")
LAMS = np.round(np.arange(-0.15, 0.1501, 0.05), 3)


def S_tables(te):
    items = []
    for M in MRUNS:
        rg, Mg, m_ = mean_profile(te, M)
        for dl in LAMS:
            lmt = math.log10(M) + dl
            if MUTATE and lmt > 11.0:
                continue
            items.append((M, dl, lmt, rg, Mg, float(m_["M200m"])))
    if MUTATE:                                                                         # the capped grid: the smallest run scaled down
        rg, Mg, m_ = mean_profile(te, MRUNS[0])
        items = [(MRUNS[0], lmt - 12.0, lmt, rg, Mg, float(m_["M200m"])) for lmt in np.round(np.arange(10.5, 11.0001, 0.05), 3)]
    TT = np.zeros((len(items), len(LM), 4, NPB)); caps = np.zeros(len(items))
    for k, (M, dl, lmt, rg, Mg, M200) in enumerate(items):
        lam = 10 ** dl
        r_lim = lam ** (1 / 3.0) * rg[-1]
        rr_ = np.minimum(r_mpc, r_lim)
        Mh = np.maximum(lam * np.interp(rr_ / lam ** (1 / 3.0), rg, Mg) - 4 * math.pi / 3 * rr_ ** 3 * RHOM_SIM, 0.0) * MSK
        dh = FIX(Mh, 0.0)
        hd = np.array([np.interp(Rd[b], RPK / MPCK, dh) for b in range(4)])
        TT[k] = hd[None] + (10.0 ** LM)[:, None, None] * MSK * PMd[None]
        caps[k] = bias_tinker(lam * M200)
    return TT, caps, items


SRES = {}
for te in TENV:
    TT, caps, items = S_tables(te)
    for lab, cp in (("A=0", np.zeros((len(items), 4))), ("A<=b", np.repeat(caps[:, None], 4, 1))):
        pb = per_bin(TT, cp)
        chi, ks = kfit_best(pb)
        mods = [pb[b]["mod"][ks[b]] for b in range(4)]
        bands = np.zeros(3)
        for b in range(4):
            rr = Rd[b]; ee = (Ed[b] - mods[b]) / Sd[b]
            bands += [np.sum(ee[rr < 0.15] ** 2), np.sum(ee[(rr >= 0.15) & (rr < 0.6)] ** 2), np.sum(ee[rr >= 0.6] ** 2)]
        SRES[(te, lab)] = dict(chi2=chi, lmta=[items[k][2] for k in ks],
                               lm200m=[math.log10(10 ** items[k][1] * items[k][5]) for k in ks],
                               run=[items[k][0] for k in ks], A=[float(pb[b]["A"][ks[b]]) for b in range(4)],
                               bands=[float(v) for v in bands])
        v = SRES[(te, lab)]
        P(f"    t_env {te:+.0f} {lab:5s}: chi^2 {v['chi2']:7.2f} (bands R<0.15 / 0.15-0.6 / >=0.6: " + " / ".join(f"{x:.1f}" for x in v["bands"]) +
          "); log M200m " + ", ".join(f"{x:.2f}" for x in v["lm200m"]) + "; A " + ", ".join(f"{x:.2f}" for x in v["A"]))
cS = SRES[(0.0, "A=0")]["chi2"]
h1 = cS <= fw_best + 9.0
check("H1 [HEADLINE] the standard halo from the peak's own mean surroundings (t_env = 0, A = 0) fits KiDS within +9 of the framework's "
      "best" + ("  [MUTATE: log M_ta <= 11]" if MUTATE else ""), f"chi^2 {cS:.2f} vs {fw_best:.2f} + 9", h1)

# ================================================================================================ (F) the framework's profile
R.banner("(F)  THE FRAMEWORK: the law inside the splashback caustic, the collapse's own infall outside (T5), no free amplitude")
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
A0S = C.A0


def F_Mfun(te, kern):
    """FG016's derived profile (CFG7_edge_fg016.py main(): derived_Mfun), with the run chosen per M_b by the T5 scaling closest to 1."""
    kf = C7.KERNELS[kern]
    runs = []
    for M in MRUNS:
        rg, Mg, m_ = mean_profile(te, M)
        r_sp = m_["x_sp87"] * m_["r_ta_dta"]
        runs.append((rg, Mg, r_sp, float(np.interp(r_sp, rg, Mg))))

    def f_(Mb_kg, a0_si):
        Mb = Mb_kg / MSUN_KG
        a0u = a0_si / C7.SI_ACC
        best = None
        for rg, Mg, r_sp, M_sp in runs:
            g = lambda ll: math.log(math.exp(ll) * M_sp) - math.log(float(C7.M_law(Mb, math.exp(ll / 3.0) * r_sp, a0u, kf)))
            ll = brentq(g, -40.0, 40.0)
            if best is None or abs(ll) < abs(best[0]):
                best = (ll, rg, Mg, r_sp, M_sp)
        ll, rg, Mg, r_sp, M_sp = best
        lam = math.exp(ll); r_e = lam ** (1 / 3.0) * r_sp
        M_in = C7.M_law(Mb, r_mpc, a0u, kf)
        M_e = float(C7.M_law(Mb, r_e, a0u, kf))
        r_lim = lam ** (1 / 3.0) * rg[-1]
        rr_ = np.minimum(r_mpc, r_lim)
        M_sim = lam * np.interp(rr_ / lam ** (1 / 3.0), rg, Mg)
        M_out = M_e + (M_sim - lam * M_sp) - 4 * math.pi / 3 * (rr_ ** 3 - r_e ** 3) * RHOM_SIM
        return np.where(r_mpc <= r_e, M_in, np.maximum(M_out, 0.0)) * MSUN_KG
    return f_


def kids_chi2_fg016(Mfun, foot, Amax=0.0):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, A0S[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return GK["kfit"]({foot: T}, foot, W0, Amax)[0]


FRES = {}
for te in TENV:
    for foot in C.FOOTS:
        for kern in ("P2", "nu_mono"):
            mf = F_Mfun(te, kern)
            for A in (0.0, 2.0):
                FRES[(te, foot, kern, A)] = kids_chi2_fg016(mf, foot, A)
            P(f"    t_env {te:+.0f} {foot:9s} {kern:8s}: chi^2 A = 0 {FRES[(te, foot, kern, 0.0)]:7.2f}; A <= 2 {FRES[(te, foot, kern, 2.0)]:7.2f}  "
              f"(the framework's best with a sharp edge + linear 2-halo, CFG21: {FWB[(foot, kern)]:.2f})")
h2 = all(FRES[(0.0, "canonical", kn, 0.0)] <= fw_best + 9.0 for kn in ("P2", "nu_mono"))
check("H2 [the framework] the law inside the splashback caustic with the collapse's own infall from the peak's mean surroundings "
      "(t_env = 0, A = 0) fits KiDS within +9 of 104.7, canonical, P2 and nu_mono",
      "; ".join(f"{kn}: {FRES[(0.0, 'canonical', kn, 0.0)]:.2f}" for kn in ("P2", "nu_mono")), h2)
reading = ("no reading for the framework: spherical collapse misses KiDS's outer profile even from the peak's own surroundings" if not h1
           else "the inflow-derived edge fits KiDS with no separate budget cost: the budget-vs-KiDS tension was the machinery" if h2
           else "the budget-vs-KiDS tension is real and framework-specific")
P(f"\n    READING (declared): {reading}")

# ================================================================================================ R1 the derived edge and the accretion rates
R.banner("R1  THE DERIVED EDGE (T5 closure at Delta_sp87, M_b = 6e10) AND THE ACCRETION RATES")
XE = {}
a0u = C.A0["canonical"] / C7.SI_ACC
for te in TENV:
    for M in MRUNS:
        m_ = RES[(te, M)]["res"]
        XE[(te, M)] = dict(s=m_["s_ta"], Delta87=m_["Delta_sp87"], x_e=float(C7.x_edge_from_Delta(m_["Delta_sp87"], 6e10, a0u, C7.nu_p2, 0.8)))
    P(f"    t_env {te:+.0f}: " + "; ".join(f"M_ta {M:.1e}: s {XE[(te, M)]['s']:.2f}, x_e {XE[(te, M)]['x_e']:.3f}" for M in MRUNS))
ebud = C24["op|canonical|P2"]["associations"]["edge"]
check("R1 (reported) the derived edge against CFG24's association-level budget edge; t_env = -1; the capped/2-halo variants",
      f"x_e (t_env 0) {min(v['x_e'] for k, v in XE.items() if k[0] == 0.0):.3f}-{max(v['x_e'] for k, v in XE.items() if k[0] == 0.0):.3f} "
      f"vs budget edge {ebud:.3f}; (S) t_env -1: {SRES[(-1.0, 'A=0')]['chi2']:.1f}; (S) A<=b: {SRES[(0.0, 'A<=b')]['chi2']:.1f}; "
      f"(F) t_env -1 canonical P2: {FRES[(-1.0, 'canonical', 'P2', 0.0)]:.1f}", True, load_bearing=False)
R.num("runs", {f"{k[0]}|{k[1]:.1e}": {kk: v["res"][kk] for kk in ("s_ta", "eps_ics", "r_ta_dta", "r_ta_zv", "x_sp87", "Delta_sp87",
                                                                 "M200m", "M_ta", "guard_frac_beyond_rta")} for k, v in RES.items()})
R.num("S", {f"{k[0]}|{k[1]}": v for k, v in SRES.items()})
R.num("F", {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": v for k, v in FRES.items()})
R.num("edges", {f"{k[0]}|{k[1]:.1e}": v for k, v in XE.items()})
R.num("summary", dict(S_chi2=cS, F_chi2={kn: FRES[(0.0, "canonical", kn, 0.0)] for kn in ("P2", "nu_mono")}, framework_best=fw_best,
                      reading=reading, budget_edge=ebud))
P(f"    ({time.time() - t0:.0f} s)")
nf = R.write()
sys.exit(1 if nf else 0)
