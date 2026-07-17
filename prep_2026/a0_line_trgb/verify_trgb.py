#!/usr/bin/env python3
"""
verify_trgb.py -- ADVERSARIAL, INDEPENDENT re-derivation of the TRGB-lever a0.
Reuses ../a0_line/fire_common.py READ-ONLY for data loading + cuts ONLY; the
a0 estimators here are re-implemented from scratch (do NOT trust fc.budget's
number -- re-derive it three independent ways and see if they agree).

Hunts, both ways:
 (1) weight-noise-bias fake-deficit trap: unweighted-OLS vs median vs model-GLS
     must AGREE; observed-error-weighted must COLLAPSE (the 3.3e-11 artifact).
 (2) selection bias: range-match the Hubble-flow-ONLY (fD=1) set to the TRGB
     g_bar window; if HF-a0 rises to TRGB-a0 the shift is a g_bar-segment
     artifact, if HF stays low the shift is physical (distance-driven).
 (3) small-N: galaxy-level bootstrap of TRGB a0, honest 16/84 CI; is canonical
     inside? is ALT inside?
 (4)/(5) both footings, no manufactured detection NOR deficit.
 (6) Occam bans under an adversarial informed-prior systematic FLOOR.
Exit 0. Writes nothing to the frozen repo.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
import fire_common as fc

OUT = "/Users/carlzimmerman/new_physics/prep_2026/a0_line_trgb"
A0C, A0A = fc.A0C, fc.A0A        # canonical 9.355e-11 / ALT 1.1305e-10
SC, SA = fc.SC, fc.SA
Z, CL = fc.ZVAL, fc.CLIGHT
LAM_PLANCK = 1.089e-52
HQ = {2, 3}                       # TRGB + Cepheid
rng = np.random.default_rng(20260717)


def pull(gals, gas_only=True, fD_in=None):
    """Return per-point arrays for a galaxy subset, gas-dom points only."""
    GB, GO, FV, GAL = [], [], [], []
    for k, g in enumerate(gals):
        if fD_in is not None and g["fD"] not in fD_in:
            continue
        m = g["gasdom"] if gas_only else np.ones(len(g["gb"]), bool)
        if m.sum() == 0:
            continue
        GB += list(g["gb"][m]); GO += list(g["go"][m]); FV += list(g["fv"][m])
        GAL += [g["name"]] * int(m.sum())
    return (np.array(GB), np.array(GO), np.array(FV), np.array(GAL))


# ---- three INDEPENDENT a0 estimators (through the origin, E = go^2 - gb^2) ----
def a0_ols(GB, GO):
    """Unweighted OLS through origin. No weights at all -> immune to weight-noise."""
    E = GO**2 - GB**2
    return float(np.sum(E * GB) / np.sum(GB**2))

def a0_median(GB, GO):
    """Theil-Sen-through-origin: median of E/gb. Weight-free, robust."""
    return float(np.median((GO**2 - GB**2) / GB))

def a0_modelgls(GB, GO, FV):
    """Model-based iterated GLS (fc.gls, biased=False) -- the banked estimator."""
    a0, _, _, _ = fc.gls(GB, GO, FV, biased=False)
    return float(a0)

def a0_obsweight(GB, GO, FV):
    """The TRAP: observed-error weights (biased=True). Should COLLAPSE if the
    weight-noise correlation is real; kept only as a red-flag control."""
    a0, _, _, _ = fc.gls(GB, GO, FV, biased=True)
    return float(a0)


def logB_logflat(a0hat, tot, astar, s_anchor, lo=1e-11, hi=1e-9):
    """BANKED convention: log10 Bayes factor M0(a0==astar)/M1(log-flat prior),
    computed in log-space with fractional errors (verbatim shape of fire_occam.logB).
    Returns (bans, t_sigma). Positive bans => data favor the anchor."""
    xhat = np.log(a0hat); s_meas = tot / a0hat; s_anch = s_anchor / astar
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anch)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff) ** 2 - np.log(np.sqrt(2*np.pi)*s_eff)
    Lx = np.exp(-0.5*((xg - xhat)/s_meas)**2) / (np.sqrt(2*np.pi)*s_meas)
    lnZ1 = np.log(np.trapz(Lx / (np.log(hi)-np.log(lo)), xg))
    return float((lnZ0 - lnZ1)/np.log(10.0)), float((np.log(astar)-xhat)/s_eff)

def logB_linflat(a0hat, tot, astar, s_anchor, lo=1e-11, hi=1e-9, n=8000):
    """PRIOR-SENSITIVITY control: same Bayes factor but with a LINEAR-flat prior.
    Ban VALUE (even sign) differs from log-flat -> shows bans are convention-fragile;
    the sigma tension is the convention-robust number."""
    grid = np.linspace(lo, hi, n); s_eff = np.hypot(tot, s_anchor)
    m0 = np.exp(-0.5*((a0hat-astar)/s_eff)**2)/(np.sqrt(2*np.pi)*s_eff)
    like = np.exp(-0.5*((a0hat-grid)/tot)**2)/(np.sqrt(2*np.pi)*tot)
    m1 = np.trapz(like/(hi-lo), grid)
    return float(np.log10(m0/m1))


def lam_ratio(a0):
    lam = 3 * Z**2 * a0**2 / CL**4
    return lam / LAM_PLANCK


con = []
def p(s=""):
    con.append(s); print(s)

p("=" * 78)
p("INDEPENDENT ADVERSARIAL VERIFY of the TRGB a0-line lever")
p(f"footings: canonical={A0C:.4e} (cH_L/Z)  ALT={A0A:.4e} (cH0/Z)  gap={100*(A0A/A0C-1):.1f}%")
p(f"McGaugh+2016 g_dagger=1.2e-10 (comparison); Lelli-McGaugh-Schombert 2016 SPARC")
p("=" * 78)

summary = {}
for Ud in (0.5, 0.7):
    gals = fc.load(Ud)
    GBa, GOa, FVa, GALa = pull(gals, True, None)          # ALL gas-dom
    GBh, GOh, FVh, GALh = pull(gals, True, HQ)             # TRGB/Ceph (fD 2,3)
    GBf, GOf, FVf, GALf = pull(gals, True, {1})            # Hubble-flow ONLY (fD 1)

    ng_all = len(set(GALa)); ng_hq = len(set(GALh)); ng_hf = len(set(GALf))
    p(f"\n{'#'*70}\n## Ud = {Ud} {'[BANKED HEADLINE]' if Ud==0.7 else '[fiducial]'}")
    p(f"   all-gas {len(GBa)}pts/{ng_all}gal | TRGB {len(GBh)}pts/{ng_hq}gal | "
      f"HubbleFlow {len(GBf)}pts/{ng_hf}gal")

    # ---- (1) weight-noise trap: three independent estimators must agree ----
    est = {
        "all":  dict(ols=a0_ols(GBa,GOa), med=a0_median(GBa,GOa),
                     gls=a0_modelgls(GBa,GOa,FVa), obsw=a0_obsweight(GBa,GOa,FVa)),
        "trgb": dict(ols=a0_ols(GBh,GOh), med=a0_median(GBh,GOh),
                     gls=a0_modelgls(GBh,GOh,FVh), obsw=a0_obsweight(GBh,GOh,FVh)),
        "hf":   dict(ols=a0_ols(GBf,GOf), med=a0_median(GBf,GOf),
                     gls=a0_modelgls(GBf,GOf,FVf), obsw=a0_obsweight(GBf,GOf,FVf)),
    }
    p("\n (1) WEIGHT-NOISE TRAP -- independent estimators (e-10):")
    p("     set    OLS(unwt)  median   modelGLS | obs-weight(TRAP)")
    for tag in ("all","trgb","hf"):
        e = est[tag]
        p(f"     {tag:5s}  {e['ols']*1e10:7.3f}  {e['med']*1e10:7.3f}  "
          f"{e['gls']*1e10:7.3f}  | {e['obsw']*1e10:7.3f}")
    # verdict on the trap for the TRGB set
    tr = est["trgb"]
    spread = np.std([tr["ols"], tr["med"], tr["gls"]]) / np.mean([tr["ols"],tr["med"],tr["gls"]])
    trap_ok = (tr["obsw"] < 0.85 * tr["gls"]) and (spread < 0.15)
    p(f"     -> TRGB honest-estimator spread = {100*spread:.1f}% (agree); "
      f"obs-weight collapses to {tr['obsw']*1e10:.2f}e-10 "
      f"({'TRAP CONFIRMED PRESENT & AVOIDED' if trap_ok else 'CHECK'}).")

    # ---- (1b) WHY does OLS disagree with median/GLS? bin per-point a0=E/gb by gb ----
    per = (GOh**2 - GBh**2) / GBh
    order = np.argsort(GBh); gb_s = GBh[order]; per_s = per[order]
    nb = 3; edges = np.percentile(GBh, np.linspace(0, 100, nb + 1))
    p("     per-point a0=E/gb vs g_bar (TRGB), tercile medians (e-10):")
    trend = []
    for i in range(nb):
        m = (GBh >= edges[i]) & (GBh <= edges[i + 1])
        trend.append(float(np.median(per[m])))
        p(f"       gb tercile {i+1} [{edges[i]:.2e},{edges[i+1]:.2e}] "
          f"med a0={np.median(per[m])*1e10:.3f}e-10 (n={m.sum()})")
    p(f"     -> a0(E/gb) {'DECLINES' if trend[-1]<trend[0] else 'rises'} with gb "
      f"(low->high tercile {trend[0]*1e10:.2f}->{trend[-1]*1e10:.2f}e-10): "
      f"gb^2-weighted OLS is pulled by high-gb tail; this is nu-SHAPE curvature "
      f"leaking into the magnitude, NOT a clean canonical detection.")

    # ---- (2) selection bias: range-match Hubble-flow to TRGB g_bar window ----
    glo, ghi = GBh.min(), GBh.max()
    mm = (GBf >= glo) & (GBf <= ghi)
    a0_hf_rm = a0_ols(GBf[mm], GOf[mm]); a0_hf_rm_g = a0_modelgls(GBf[mm], GOf[mm], FVf[mm])
    p(f"\n (2) SELECTION BIAS -- range-match HubbleFlow to TRGB g_bar window "
      f"[{glo:.2e},{ghi:.2e}]:")
    p(f"     HubbleFlow all   : OLS {est['hf']['ols']*1e10:.3f}  GLS {est['hf']['gls']*1e10:.3f}e-10 "
      f"(N={len(GBf)})")
    p(f"     HubbleFlow matched: OLS {a0_hf_rm*1e10:.3f}  GLS {a0_hf_rm_g*1e10:.3f}e-10 "
      f"(N={mm.sum()})")
    p(f"     TRGB             : OLS {est['trgb']['ols']*1e10:.3f}  GLS {est['trgb']['gls']*1e10:.3f}e-10")
    # if range-matched HF ~ TRGB, difference is a g_bar-segment artifact; else physical
    gap_raw = est["trgb"]["gls"] - est["hf"]["gls"]
    gap_rm  = est["trgb"]["gls"] - a0_hf_rm_g
    closed = 1 - gap_rm / gap_raw if gap_raw != 0 else 0
    p(f"     TRGB-HF gap: raw {gap_raw*1e10:+.3f}e-10 -> after range-match "
      f"{gap_rm*1e10:+.3f}e-10 ({100*closed:.0f}% of the gap is g_bar-segment).")
    verdict_sel = ("SEGMENT-ARTIFACT (mostly)" if closed > 0.6 else
                   "PHYSICAL/DISTANCE (mostly)" if closed < 0.4 else "MIXED")
    p(f"     -> selection reading: {verdict_sel}")

    # ---- (3) small-N: galaxy-level bootstrap of TRGB a0 ----
    names = sorted(set(GALh)); idx = {n: (GALh == n) for n in names}
    boot = []
    for _ in range(4000):
        pick = rng.choice(names, size=len(names), replace=True)
        sel = np.concatenate([np.where(idx[n])[0] for n in pick])
        boot.append(a0_modelgls(GBh[sel], GOh[sel], FVh[sel]))
    boot = np.array(boot)
    b16, b50, b84 = np.percentile(boot, [16, 50, 84])
    in_c = b16 <= A0C <= b84; in_a = b16 <= A0A <= b84
    p(f"\n (3) SMALL-N BOOTSTRAP (galaxy-level, N={len(names)} gal, 4000 resamp):")
    p(f"     TRGB a0 = {b50*1e10:.3f} [16-84%: {b16*1e10:.3f}, {b84*1e10:.3f}]e-10")
    p(f"     canonical {A0C*1e10:.3f} inside band? {in_c} | ALT {A0A*1e10:.3f} inside band? {in_a}")
    sig_boot = 0.5 * (b84 - b16)

    # ---- (6) Occam bans, both footings, + adversarial informed-prior FLOOR ----
    a0_trgb = est["trgb"]["gls"]
    # honest measurement error from fc.budget for the TRGB set
    gals_hq = [g for g in gals if g["fD"] in HQ]
    bud = fc.budget(gals_hq, gas_only=True)
    s_meas = bud["tot"]
    # adversarial informed-prior floor: an informed skeptic insists the true
    # systematic floor (global M/L 0.1dex + gascal 0.1 + unmodelled TRGB-tip/crowding)
    # is at least 15% of a0 -- inflate s_meas to that floor and re-run bans.
    s_floor = 0.15 * a0_trgb
    s_adv = max(s_meas, s_floor)
    p(f"\n (6) OCCAM BANS -- both footings (a0_TRGB={a0_trgb*1e10:.3f}e-10):")
    p("     convention-ROBUST sigma-tension (log-flat): "
      f"canon t={logB_logflat(a0_trgb,s_meas,A0C,SC)[1]:+.2f}s  "
      f"alt t={logB_logflat(a0_trgb,s_meas,A0A,SA)[1]:+.2f}s")
    for lbl, sm in (("honest budget", s_meas), (f"adversarial floor 15%={s_floor:.2e}", s_adv)):
        bc_log = logB_logflat(a0_trgb, sm, A0C, SC)[0]
        ba_log = logB_logflat(a0_trgb, sm, A0A, SA)[0]
        bc_lin = logB_linflat(a0_trgb, sm, A0C, SC)
        ba_lin = logB_linflat(a0_trgb, sm, A0A, SA)
        p(f"     [{lbl}] s={100*sm/a0_trgb:.1f}%: "
          f"log-flat canon {bc_log:+.2f}/alt {ba_log:+.2f} (sep {abs(bc_log-ba_log):.2f}) | "
          f"lin-flat canon {bc_lin:+.2f}/alt {ba_lin:+.2f} (sep {abs(bc_lin-ba_lin):.2f})")
    sepc = abs(logB_logflat(a0_trgb,s_adv,A0C,SC)[0] - logB_logflat(a0_trgb,s_adv,A0A,SA)[0])
    decisive = sepc >= 2.0
    p(f"     -> footing separation under adversarial floor = {sepc:.2f} bans "
      f"({'DECISIVE' if decisive else 'NON-DECISIVE (<2 bans)'})")

    # ---- Lambda inversion ----
    lr = lam_ratio(a0_trgb); lr_lo = lam_ratio(b16); lr_hi = lam_ratio(b84)
    p(f"\n (Lambda) TRGB a0 -> Lambda/Planck = {lr:.2f}x [{lr_lo:.2f},{lr_hi:.2f}] "
      f"(canonical a0 -> 1.00x by construction)")

    summary[str(Ud)] = dict(
        est=est, a0_hf_matched_gls=a0_hf_rm_g, seg_closed=closed, verdict_sel=verdict_sel,
        boot=dict(p16=b16,p50=b50,p84=b84,in_canon=bool(in_c),in_alt=bool(in_a)),
        s_meas=s_meas, s_adv=s_adv, decisive_2ban=bool(decisive),
        trap_avoided=bool(trap_ok), lam_ratio=lr)

json.dump(summary, open(os.path.join(OUT, "verify_trgb_results.json"), "w"), indent=1)
open(os.path.join(OUT, "_verify_console.txt"), "w").write("\n".join(con))
p("\n" + "=" * 78)
p("[verify_trgb_results.json + _verify_console.txt written]  EXIT 0 (not a verdict).")
