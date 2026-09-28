#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG25 -- THE LCDM CONTROL FOR FG016's INFALL: is FG016's KiDS kill of the inflow-derived edge specific to the framework?

WHY.  "Where does the cold fluid go?" has one computed answer in the record: FG016 (CFG7_edge_fg016).  Outside a bound system the
cold fluid falls in like CDM; inside the edge it IS the phantom (T5).  FG016 put the edge at the splashback caustic of spherical
collisionless infall, with the accretion rate set by the law's own demand, and scored KiDS with the law inside the edge and the
collapse's own infall outside, no free amplitude: d chi^2 +50 to +95 against the untruncated law (+14 to +54 with CFG4's linear
2-halo on top) -- killed.  CFG23 then showed that the same KiDS machinery shortchanges standard NFW halos at R >= 0.6 Mpc (the
vanilla halo model's transition region).  The fair test of FG016's kill is the same spherical-collapse engine and the same runs,
scored as a STANDARD halo: the collapse's own collisionless interior AND its infall, with the mass scale free per KiDS bin (as CFG23
gave NFW).

THE CONTROL MODEL (per KiDS bin).  M(r) = M_b (point) + lambda M_c(r lambda^(-1/3)) - (4 pi/3) r^3 rho_m, where M_c is the
collapse's mean enclosed mass (reading N, 3 seeds, a = 0.8 = z_l; FG016's six runs re-run bit for bit), rho_m the mean density
subtracted as FG016 did for its infall, the whole held constant past the simulation's reach and clipped at zero (FG016's
conventions).  lambda is free (log M_ta = log(4e12 lambda) on 10.5-14.5, step 0.05); M_b is profiled on FP1's grid; the 2-halo
amplitude A = 0 (FG016's decisive setting: the collapse's own infall carries the outer profile) or A in [0, b_Tinker(lambda M200m)]
(CFG23's parallel treatment); every accretion rate of FG016's grid (s = 0.6-2.2).  The fitter is CFG23's (exec'd read-only).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  the re-run collapse reproduces FG016's committed TABLE (reading N, a = 0.8: s, x_sp87, Delta_sp87, all six runs) to
      1e-9 relative, and FG016's committed KiDS d chi^2 for its derived profile (reading N, canonical P2, A = 0 and 2, all six runs)
      to 1e-6.
  C2  CONTROL  CFG23's fitter reproduces BASE (139.800) and CFG21's framework best (104.686).
  H1  [HEADLINE; MUTATE must fail] the collapse's own profile as a standard halo (A = 0) fits KiDS within +9 of the framework's best
      (chi^2 <= 113.7) at some accretion rate of FG016's grid.  Expectation: uncertain.
  H1b (reported) the same with A in [0, b_Tinker].
  READING (declared): H1 PASS -> FG016's KiDS kill is specific to the framework (the law's interior plus the same infall fails where
  the collapse's own profile succeeds); H1 FAIL -> the spherical-infall engine misses KiDS for standard halos too, so the KiDS side
  of FG016's kill is not framework-specific (FG016's H1 -- the edge 0.18-0.27 below CFG4's window -- is untouched by this lane).
  R1  (reported) chi^2 against s (A = 0 and capped); the best-fit halo masses; the misfit by radius band; FG016's framework numbers.
MUTATE=1: the halo scale is capped at log M_ta <= 11.0 -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG25_fg016_lcdm_control.py   (MUTATE=1 for the control; ~12 min, 6 processes)
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
NPROC = int(os.environ.get("NPROC", "6"))
R = C7.Report("CFG25_fg016_lcdm_control", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the halo scale capped at log M_ta <= 11.0 -- H1 must FAIL ***")
np.seterr(all="ignore")
t0 = time.time()
F16 = json.load(open(os.path.join(HERE, "CFG7_edge_fg016_results.json")))["numbers"]

# ================================================================================================ CFG23's fitter and KiDS machinery (exec'd read-only)
C23P = os.path.join(HERE, "CFG23_lcdm_control.py")
s23 = open(C23P).read()
cut = s23.index("# ================================================================================================ the halo tables")
g23 = {"__file__": C23P, "__name__": "cfg23_prefix"}
_env = os.environ.get("MUTATE")
os.environ["MUTATE"] = "0"                                                             # CFG23's own mutation must not leak in
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
C21 = g23["C21"]
FWB = g23["FW"]
fw_best = FWB[("canonical", "P2")]

# ================================================================================================ C2 the fitter
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

# ================================================================================================ the collapse runs (FG016's reading-N specs, bit for bit)
R.banner("THE COLLAPSE RUNS: FG016's six reading-N configurations re-run (process pool)")
EPS = [0.195, 0.269, 0.358, 0.43, 0.5375, 0.717]
base = dict(M_ta_obs=4e12, a_norm=0.8, a_obs_list=[0.8, 1.0], N=2000, seeds=(7, 8, 9))
specs = [dict(base, tag=f"N|{e}", eps=e, mode="N") for e in EPS]
RES = {}
with get_context("fork").Pool(NPROC) as pool:
    for r in pool.imap_unordered(C7.job_pooled, sorted(specs, key=lambda s: -s["eps"])):
        RES[r["spec"]["tag"]] = r
        m8 = r["res"]["0.8000"]
        P(f"    {r['spec']['tag']:10s} done ({r['seconds']:.0f} s): s = {m8['s_ta']:.4f}, x_sp87 {m8['x_sp87']:.4f}, Delta_sp87 {m8['Delta_sp87']:.2f}, "
          f"M200m {m8['M200m']:.3e}, r_ta {m8['r_ta_dta']:.4f}")
tab = {round(row["eps"], 6): row for row in F16["TABLE"]["N|0.8000"]}
dev_t = 0.0
for e in EPS:
    m8 = RES[f"N|{e}"]["res"]["0.8000"]; ref = tab[round(e, 6)]
    for mine, theirs in ((m8["s_ta"], ref["s"]), (m8["x_sp87"], ref["x87"]), (m8["Delta_sp87"], ref["D87"])):
        dev_t = max(dev_t, abs(mine / theirs - 1))

# FG016's derived profile (CFG7_edge_fg016.py main(): mean_profile, derived_Mfun), copied with attribution, to reproduce its KiDS numbers
MPC_M = C7.MPC_M
MSUN_KG = 1.98840987e30
RHOM_SIM = float(C7.LCDM.rhom(0.8))
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
A0S = C.A0


def mean_profile(e):
    m_ = RES[f"N|{e}"]["res"]["0.8000"]
    rg = np.geomspace(1e-3, 30.0, 900)
    Ms = [np.interp(rg, np.array(p["r"]), np.array(p["M"]), left=np.nan, right=np.nan) for p in m_["profiles"]]
    M = np.nanmean(np.array(Ms), axis=0)
    ok = np.isfinite(M)
    return rg[ok], M[ok], m_


def derived_Mfun(e, kern):
    rg, Mg, m_ = mean_profile(e)
    r_sp = m_["x_sp87"] * m_["r_ta_dta"]
    M_sp = float(np.interp(r_sp, rg, Mg))
    kf = C7.KERNELS[kern]
    r_mpc = RRK / MPC_M

    def f_(Mb_kg, a0_si):
        Mb = Mb_kg / MSUN_KG
        a0u = a0_si / C7.SI_ACC
        g = lambda ll: math.log(math.exp(ll) * M_sp) - math.log(float(C7.M_law(Mb, math.exp(ll / 3.0) * r_sp, a0u, kf)))
        ll = brentq(g, -40.0, 40.0)
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


dev_k = 0.0
FW16 = {}
for e in EPS:
    for A in (0.0, 2.0):
        mine = kids_chi2_fg016(derived_Mfun(e, "P2"), "canonical", A) - BASE[("canonical", "P2")]
        ref = F16["KIDS"][f"N|{e}|canonical|P2|{A}"]
        dev_k = max(dev_k, abs(mine - ref))
        FW16[(e, A)] = mine
R.banner("C1  CONTROL: FG016's committed collapse table and KiDS numbers reproduced")
P("    FG016's framework profile (law inside the splashback edge, the collapse's infall outside), canonical P2, d chi^2 vs the "
  "untruncated law (A = 0 / A <= 2): " + "; ".join(f"s {RES[f'N|{e}']['res']['0.8000']['s_ta']:.2f}: {FW16[(e, 0.0)]:+.1f} / {FW16[(e, 2.0)]:+.1f}"
                                                   for e in EPS))
check("C1 CONTROL: the re-run collapse reproduces FG016's committed TABLE (s, x_sp87, Delta_sp87; six runs) to 1e-9 relative, and "
      "FG016's committed KiDS d chi^2 for its derived profile (canonical P2, A = 0 and 2) to 1e-6",
      f"table max rel {dev_t:.1e}; KiDS max |d| {dev_k:.1e}", dev_t <= 1e-9 and dev_k <= 1e-6)

# ================================================================================================ the LCDM control: the collapse's own profile as a halo
R.banner("THE CONTROL: the collapse's own profile (interior + infall) as a standard halo, mass scale free per KiDS bin")
LMTA = np.round(np.arange(10.5, 14.5001, 0.05), 3)
if MUTATE:
    LMTA = LMTA[LMTA <= 11.0]
K = len(LMTA)
r_mpc = RRK / MPC_M


def halo_tables(e):
    rg, Mg, m_ = mean_profile(e)
    M200 = float(m_["M200m"])
    TT = np.zeros((K, len(LM), 4, NPB)); caps = np.zeros(K)
    for k, lmt in enumerate(LMTA):
        lam = 10 ** lmt / 4e12
        r_lim = lam ** (1 / 3.0) * rg[-1]
        rr_ = np.minimum(r_mpc, r_lim)
        Mh = np.maximum(lam * np.interp(rr_ / lam ** (1 / 3.0), rg, Mg) - 4 * math.pi / 3 * rr_ ** 3 * RHOM_SIM, 0.0) * MSK
        dh = FIX(Mh, 0.0)
        hd = np.array([np.interp(Rd[b], RPK / MPCK, dh) for b in range(4)])
        TT[k] = hd[None] + (10.0 ** LM)[:, None, None] * MSK * PMd[None]
        caps[k] = bias_tinker(lam * M200)
    return TT, caps, M200


CTRL = {}
for e in EPS:
    TT, caps, M200 = halo_tables(e)
    s_ = RES[f"N|{e}"]["res"]["0.8000"]["s_ta"]
    for lab, cp in (("A=0", np.zeros((K, 4))), ("A<=b", np.repeat(caps[:, None], 4, 1))):
        pb = per_bin(TT, cp)
        chi, ks = kfit_best(pb)
        mods = [pb[b]["mod"][ks[b]] for b in range(4)]
        bands = np.zeros(3)
        for b in range(4):
            rr = Rd[b]; ee = (Ed[b] - mods[b]) / Sd[b]
            bands += [np.sum(ee[rr < 0.15] ** 2), np.sum(ee[(rr >= 0.15) & (rr < 0.6)] ** 2), np.sum(ee[rr >= 0.6] ** 2)]
        CTRL[(e, lab)] = dict(s=s_, chi2=chi, lmta=[float(LMTA[k]) for k in ks], lm200m=[float(np.log10(10 ** LMTA[k] / 4e12 * M200)) for k in ks],
                              lmb=[float(LM[pb[b]["im"][ks[b]]]) for b in range(4)], A=[float(pb[b]["A"][ks[b]]) for b in range(4)],
                              bands=[float(v) for v in bands], at_edge=any(LMTA[k] in (LMTA[0], LMTA[-1]) for k in ks))
    v0, v1 = CTRL[(e, "A=0")], CTRL[(e, "A<=b")]
    P(f"    s = {s_:.2f}: chi^2 A = 0 {v0['chi2']:7.2f} (bands R<0.15 / 0.15-0.6 / >=0.6: " + " / ".join(f"{x:.1f}" for x in v0["bands"]) +
      f"), log M200m " + ", ".join(f"{x:.2f}" for x in v0["lm200m"]) + f"; A <= b {v1['chi2']:7.2f} (A " +
      ", ".join(f"{x:.2f}" for x in v1["A"]) + f"); grid edge {v0['at_edge'] or v1['at_edge']}")
best0 = min(EPS, key=lambda e: CTRL[(e, "A=0")]["chi2"])
best1 = min(EPS, key=lambda e: CTRL[(e, "A<=b")]["chi2"])
c0, c1 = CTRL[(best0, "A=0")]["chi2"], CTRL[(best1, "A<=b")]["chi2"]
h1 = c0 <= fw_best + 9.0
check("H1 [HEADLINE] the collapse's own profile as a standard halo (A = 0) fits KiDS within +9 of the framework's best at some "
      "accretion rate of FG016's grid" + ("  [MUTATE: log M_ta <= 11]" if MUTATE else ""),
      f"best chi^2 {c0:.2f} at s = {CTRL[(best0, 'A=0')]['s']:.2f} vs {fw_best:.2f} + 9", h1)
check("H1b (reported) the same with A in [0, b_Tinker]", f"best chi^2 {c1:.2f} at s = {CTRL[(best1, 'A<=b')]['s']:.2f}",
      c1 <= fw_best + 9.0, load_bearing=False)
fw_abs = {e: FW16[(e, 0.0)] + BASE[("canonical", "P2")] for e in EPS}
reading = ("FG016's KiDS kill is specific to the framework: the collapse's own profile fits where the law's interior plus the same "
           "infall fails" if h1 else
           "the spherical-infall engine misses KiDS for standard halos too: the KiDS side of FG016's kill is not framework-specific")
P(f"\n    FG016's framework profile, absolute chi^2 (A = 0) at the same runs: " + "; ".join(f"s {CTRL[(e, 'A=0')]['s']:.2f}: {fw_abs[e]:.1f}"
                                                                                       for e in EPS))
P(f"    READING (declared): {reading}")
check("R1 (reported) chi^2 against s for the control and FG016's framework profile",
      "; ".join(f"s {CTRL[(e, 'A=0')]['s']:.2f}: LCDM {CTRL[(e, 'A=0')]['chi2']:.1f} / {CTRL[(e, 'A<=b')]['chi2']:.1f}, framework "
                f"{fw_abs[e]:.1f}" for e in EPS), True, load_bearing=False)
R.num("control", {f"{k[0]}|{k[1]}": v for k, v in CTRL.items()})
R.num("fg016_framework", {f"{e}|{A}": v for (e, A), v in FW16.items()})
R.num("summary", dict(best_A0=dict(eps=best0, chi2=c0), best_capped=dict(eps=best1, chi2=c1), framework_best=fw_best, reading=reading,
                      controls=dict(table=dev_t, kids=dev_k, fitter=[v_a, v_b])))
P(f"    ({time.time() - t0:.0f} s)")
nf = R.write()
sys.exit(1 if nf else 0)
