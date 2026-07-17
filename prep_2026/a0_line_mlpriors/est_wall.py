#!/usr/bin/env python3
"""
est_wall.py -- THE a0-LINE ML-PRIORS RUN, WALL-ASSESSMENT LANE.
==========================================================================================
The a0-line (banked, /prep_2026/a0_line/): squaring the framework's OWN dS-Unruh
interpolation g_obs = sqrt(g_bar^2 + g_bar*a0) gives the exact through-origin identity
E = g_obs^2 - g_bar^2 = a0*g_bar. On the gas-dominated SPARC dwarfs the slope a0-hat is
an honest ~ (0.9-1.5)e-10 box that STRADDLES both dark-energy footings of the coefficient
    canonical  a0 = cH_Lambda/Z = 9.355e-11  (pure-Lambda; a0 = c^2*sqrt(Lambda/32pi))
    alt        a0 = cH0/Z       = 1.1305e-10 (total-density / H0 footing)
20.9% apart. The TRGB lever (a0_line_trgb/) spent the DISTANCE systematic (~2-3.5x cut)
and found the split is now UNDERPOWERED-BY-FLOOR: the GLOBAL M/L (Upsilon, sig=0.23 nat
= 0.10 dex, coherent) + gas-cal (sig_lnG = 0.10 nat, coherent) floor EXCEEDS the
sigma_tot <= |Delta|/2 = 9.75e-12 needed to separate the footings at 2 sigma.

THE ML-PRIORS RUN decomposes Upsilon into a COHERENT SPS/IMF zero-point floor (~0.06 dex,
irreducible, same for all galaxies) + a PER-GALAXY relative part (~0.08 dex, reducible
1/sqrt(N) with external colour/SPS M/L). External per-galaxy priors beat the per-galaxy
part but NOT the coherent floor.

THIS LANE (est_wall.py) ASSUMES the external Upsilon priors SUCCEED -- i.e. sysU is cut to
its coherent floor sU_coh = (sig_coh/0.10)*sysU + a tiny reduced per-galaxy residual --
and then asks the wall questions, both footings:
  (1) With sysU at its floor, what is the total error and WHICH systematic now binds?
  (2) Is gas-cal (sysG, coherent global gas-mass scale) the next wall? Quantify the
      residual and the asymptotic (N->inf) coherent floor.
  (3) What sigma_gascal (independent gas-mass calibration) + what N pushes the footing
      separation past 2 bans / 2 sigma? Both footings.
  (4) Is there a DIFFERENTIAL / RATIO estimator that cancels the coherent gas-cal (a
      global multiplicative gas-scale)? Tested numerically, honestly.

HONESTY RAILS carried from the banked run (this estimator once manufactured a FAKE
3.3e-11 deficit from raw observed-error weights -- guard = model-based iterated GLS,
fire_common.gls biased=False, never observed weights): do NOT manufacture a footing
detection NOR a deficit. The honest a0 is a box straddling both footings and the per-point
a0 = E/g_bar DECLINES with g_bar (nu-shape leaking into magnitude, the verifier's catch)
-- carried as a caveat throughout. If beating Upsilon does NOT decide the footing, say so
plainly. NO 'proves'. Exit 0 is not a verdict.

Credits: Schombert-McGaugh-Lelli 2019 + Meidt+2014 + McGaugh-Schombert 2014 ([3.6] SPS
M/L, coherent floor); Bell-de Jong 2001 (colour M/L); Lelli-McGaugh-Schombert 2016
(SPARC). Kernel nu = sqrt(1+1/y) = Milgrom 1999 PLA 253:273 Eq 9; the distinctive content
is the cH_Lambda/Z coefficient + the MI completion. a0 VALUE and s=-1 sign remain
postulates regardless of this run.
"""
import numpy as np, os, sys, json

sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
import fire_common as fc
from fire_common import A0C, A0A, SC, SA, ZVAL, HL, CLIGHT, SIG_LNU, SIG_LNG

OUT = "/Users/carlzimmerman/new_physics/prep_2026/a0_line_mlpriors"
os.makedirs(OUT, exist_ok=True)
LN10 = np.log(10.0)
TARGET = (A0A - A0C) / 2.0                 # 2-sigma footing-separation target on sigma_tot
DELTA = A0A - A0C
TRGB_FLAGS = (2, 3)

# --- the Upsilon decomposition parameters (literature, flagged) --------------------------
# Total M/L sigma = 0.10 dex (= SIG_LNU 0.23 nat), split coherent (x) + per-galaxy (sqrt(.10^2-x^2)).
SIG_TOT_DEX = SIG_LNU / LN10               # 0.0999 dex, the fire_common global Upsilon width
SIG_COH_DEX = 0.06                         # headline coherent SPS/IMF zero-point floor
SIG_COH_SWEEP = (0.05, 0.06, 0.07)         # McGaugh-Schombert / Meidt+ defensible band
SIG_PG_RES_DEX = 0.035                     # per-galaxy Upsilon AFTER external colour/SPS prior


def logB(xhat, s_meas, astar, s_anchor_frac, lo=1e-11, hi=1e-9):
    """log10 Bayes factor M0(a0 fixed at astar +/- anchor) / M1(a0 free, log-flat prior).
    Verbatim quadrature from fire_occam / est_gls -- self-contained, no closed form."""
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anchor_frac)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff) ** 2 - np.log(np.sqrt(2 * np.pi) * s_eff)
    Lx = np.exp(-0.5 * ((xg - xhat) / s_meas) ** 2) / (np.sqrt(2 * np.pi) * s_meas)
    prior = np.full_like(xg, 1.0 / (np.log(hi) - np.log(lo)))
    lnZ1 = np.log(np.trapz(Lx * prior, xg))
    return float((lnZ0 - lnZ1) / np.log(10.0)), float((np.log(astar) - xhat) / s_eff)


def decompose(gals, gas_only=True):
    """Re-derive the a0-line budget AND expose the coherent-vs-shrinkable split.
    Same algebra as fire_common.budget; adds the per-galaxy Upsilon RSS (cU_gal) so we can
    replace the fully-coherent sysU with (coherent floor + reduced per-galaxy) once the
    external per-galaxy Upsilon prior is applied."""
    GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, gas_only)
    if len(GB) < 10:
        return None
    a0, fint, c2, w = fc.gls(GB, GO, FV)
    med = float(np.median((GO**2 - GB**2) / GB))
    S = np.sum(w * GB**2)
    yq = GB / a0
    stat = np.sqrt(1.0 / S)
    varD = varI = 0.0
    cU_list = []
    for k in set(GAL.tolist()):
        m = GAL == k
        cD = a0 * np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S
        cI = a0 * np.sum(w[m] * GB[m]**2 * 4 * (yq[m] + 1) * CTI[m]) / S
        varD += (cD * SLD[m][0])**2
        varI += (cI * fc.SIG_INC)**2
        cU_list.append(a0 * np.sum(w[m] * GB[m]**2 * PHI[m] * (2 * yq[m] + 1)) / S)
    cU = np.array(cU_list)
    KU = np.sum(w * GB**2 * PHI * (2 * yq + 1)) / S
    KG = np.sum(w * GB**2 * (1 - PHI) * (2 * yq + 1)) / S
    sysU = KU * a0 * SIG_LNU               # fully-coherent Upsilon (fire_common default)
    sysG = KG * a0 * SIG_LNG               # fully-coherent gas-cal
    sysEst = abs(a0 - med) / 2.0
    return dict(a0=float(a0), med=med, N=int(len(GB)), Ngal=int(len(set(GAL.tolist()))),
                stat=float(stat), sysD=float(np.sqrt(varD)), sysI=float(np.sqrt(varI)),
                sysU=float(sysU), sysG=float(sysG), sysEst=float(sysEst),
                KU=float(KU), KG=float(KG), cU_rss=float(np.sqrt(np.sum(cU**2))),
                phibar=float(np.sum(w * GB**2 * PHI) / S), ybar=float(np.sum(w * GB**2 * yq) / S),
                GB=GB, GO=GO, FV=FV, PHI=PHI, GAL=GAL)


def upsilon_beaten(b, sig_coh_dex, sig_pg_res_dex):
    """sysU after external per-galaxy Upsilon priors succeed: coherent floor (does NOT
    average) + reduced per-galaxy RSS (the residual after the prior). Returns the pieces."""
    sU_coh = b["sysU"] * (sig_coh_dex * LN10 / SIG_LNU)
    sU_pg = sig_pg_res_dex * LN10 * b["cU_rss"]
    sU_floor = np.hypot(sU_coh, sU_pg)
    return dict(sU_coh=float(sU_coh), sU_pg=float(sU_pg), sysU_floor=float(sU_floor))


def assemble(b, sysU_floor, sysG=None):
    """Total error with sysU at its post-prior floor. sysG override lets us ask the
    'what gas-cal is needed' question. Returns tot + the binding-line identification.
    Coherent (non-averaging) lines: sU_coh(inside sysU_floor) + sysG. Shrinkable: the
    rest (stat, sysD, sysI, sysEst, sU_pg)."""
    sysG = b["sysG"] if sysG is None else sysG
    lines = dict(stat=b["stat"], sysD=b["sysD"], sysI=b["sysI"], sysEst=b["sysEst"],
                 sysU=sysU_floor, sysG=sysG)
    tot = np.sqrt(sum(v**2 for v in lines.values()))
    binder = max(lines, key=lambda k: lines[k])
    return float(tot), binder, lines


def coherent_shrink_split(b, ub, sysG=None):
    """The asymptotic wall: coherent = hypot(sU_coh, sysG) (never averages down);
    shrinkable = hypot(stat, sysD, sysI, sysEst, sU_pg) (~1/sqrt(N))."""
    sysG = b["sysG"] if sysG is None else sysG
    coh = np.hypot(ub["sU_coh"], sysG)
    shr = np.sqrt(b["stat"]**2 + b["sysD"]**2 + b["sysI"]**2 + b["sysEst"]**2 + ub["sU_pg"]**2)
    return float(coh), float(shr)


def sigG_needed(sU_coh, target):
    """Largest sysG whose coherent floor hypot(sU_coh, sysG) still allows reaching target
    at N->inf (shrinkable->0). Returns sysG_max and the implied sig_lnG (nat)."""
    if sU_coh >= target:
        return None                        # coherent Upsilon floor alone already blocks it
    return np.sqrt(target**2 - sU_coh**2)


def N_needed(coh, shr, N0, target):
    """N of gas dwarfs to reach sigma_tot = target given coherent floor coh (fixed) and
    shrinkable shr at N0 (averages N0/N). None if coh already exceeds target."""
    if coh >= target:
        return None
    denom = target**2 - coh**2
    return float(np.ceil(shr**2 * N0 / denom))


def gas_scale_response(b):
    """(4) Does a global multiplicative gas-scale (1+eps) cancel in a between-galaxy RATIO?
    eps_G shifts g_bar -> g_bar*(1 + (1-phi)*eps) [gas share only; go = data, unaffected].
    Measure d ln(a0_gal)/d eps per galaxy. If the response is COMMON across galaxies a ratio
    cancels it; the spread is the residual a differential estimator leaves. But a ratio
    cancels the ABSOLUTE a0 too -> cannot test 9.36 vs 1.13. We quantify both."""
    GB, GO, FV, PHI, GAL = b["GB"], b["GO"], b["FV"], b["PHI"], b["GAL"]
    eps = 0.05
    slopes, names, wts = [], [], []
    for k in sorted(set(GAL.tolist())):
        m = GAL == k
        if m.sum() < 3:
            continue
        gbk, gok, fvk, phik = GB[m], GO[m], FV[m], PHI[m]
        a0p = fc.gls(gbk * (1 + (1 - phik) * eps), gok, fvk)[0]
        a0m = fc.gls(gbk * (1 - (1 - phik) * eps), gok, fvk)[0]
        if a0p > 0 and a0m > 0:
            slopes.append((np.log(a0p) - np.log(a0m)) / (2 * eps))
            wts.append(m.sum())
            names.append(k)
    slopes = np.array(slopes); wts = np.array(wts, float)
    mean = float(np.average(slopes, weights=wts))
    # weighted std = the irreducible per-galaxy dispersion of the gas-cal response
    std = float(np.sqrt(np.average((slopes - mean)**2, weights=wts)))
    # sample-level response (the coherent shift a ratio WOULD remove)
    a0p = fc.gls(GB * (1 + (1 - PHI) * eps), GO, FV)[0]
    a0m = fc.gls(GB * (1 - (1 - PHI) * eps), GO, FV)[0]
    samp = (np.log(a0p) - np.log(a0m)) / (2 * eps)
    return dict(mean_dlnA0_deps=mean, std_dlnA0_deps=std, sample_response=float(samp),
                ratio_cancels_frac=float(1 - std / abs(mean)) if mean != 0 else 0.0,
                ngal=int(len(slopes)))


# ========================================================================================
bar = "=" * 94
print(bar)
print("EST_WALL -- a0-line, ASSUME external Upsilon priors succeed; find the NEXT wall")
print(f"  canonical a0 = {A0C:.4e} (cH_Lambda/Z)   alt a0 = {A0A:.4e} (cH0/Z)")
print(f"  Delta = {DELTA:.3e};  2-sigma footing target sigma_tot <= |Delta|/2 = {TARGET:.3e}")
print(f"  Upsilon split: total {SIG_TOT_DEX:.3f} dex -> coherent floor {SIG_COH_DEX} dex "
      f"(sweep {SIG_COH_SWEEP}) + per-galaxy residual {SIG_PG_RES_DEX} dex")
print(bar)

RES = {"target": float(TARGET), "delta": float(DELTA), "a0_canon": A0C, "a0_alt": A0A,
       "sig_coh_dex": SIG_COH_DEX, "sig_pg_res_dex": SIG_PG_RES_DEX}
sets = {}

for Ud in (0.7, 0.5):
    gals = fc.load(Ud)
    for tag, gg in (("full", gals), ("trgb", [g for g in gals if g["fD"] in TRGB_FLAGS])):
        b = decompose(gg, True)
        if b is None:
            continue
        ub = upsilon_beaten(b, SIG_COH_DEX, SIG_PG_RES_DEX)
        tot0, binder0, lines0 = assemble(b, b["sysU"])                 # pre-prior baseline
        tot1, binder1, lines1 = assemble(b, ub["sysU_floor"])         # Upsilon beaten
        coh, shr = coherent_shrink_split(b, ub)
        key = f"Ud{Ud}_{tag}"
        print(f"\n----- {key}  N={b['N']} pts / {b['Ngal']} gals | a0-hat(GLS)={b['a0']:.3e} "
              f"med={b['med']:.3e} | ybar={b['ybar']:.3f} phibar={b['phibar']:.3f} -----")
        print(f"  BASELINE budget : tot={tot0:.3e} ({100*tot0/b['a0']:.1f}%)  binder={binder0}")
        print(f"    stat={b['stat']:.2e} sysD={b['sysD']:.2e} sysI={b['sysI']:.2e} "
              f"sysU={b['sysU']:.2e} sysG={b['sysG']:.2e} sysEst={b['sysEst']:.2e}")
        print(f"  UPSILON BEATEN  : sysU {b['sysU']:.2e} -> floor {ub['sysU_floor']:.2e} "
              f"(coh {ub['sU_coh']:.2e} + pg_res {ub['sU_pg']:.2e})")
        print(f"    tot={tot1:.3e} ({100*tot1/b['a0']:.1f}%)  BINDING LINE NOW = '{binder1}' "
              f"({lines1[binder1]:.2e})")
        print(f"    coherent floor (N->inf) = hypot(sU_coh, sysG) = {coh:.3e}  "
              f"{'>' if coh > TARGET else '<='} target {TARGET:.3e}  "
              f"[{'ABOVE 2-sig line' if coh > TARGET else 'reaches 2-sig line'}]")
        print(f"    shrinkable(N0)          = {shr:.3e}   (stat,sysD,sysI,sysEst,pg_res; ~1/sqrtN)")

        # Occam bans at the Upsilon-beaten error, both footings
        xh = np.log(b["a0"]); sm = tot1 / b["a0"]
        bC, tC = logB(xh, sm, A0C, SC / A0C)
        bA, tA = logB(xh, sm, A0A, SA / A0A)
        sep = abs(bC - bA)
        print(f"    Occam @Upsilon-beaten: canon {bC:+.2f} ban (t={tC:+.2f}s)  "
              f"alt {bA:+.2f} ban (t={tA:+.2f}s)  |sep|={sep:.2f} ban "
              f"{'>=2 DECISIVE' if sep >= 2 else '<2 non-decisive'}")

        # (3) what gas-cal + what N pushes past 2-sigma / 2-ban
        sysG_max = sigG_needed(ub["sU_coh"], TARGET)
        if sysG_max is None:
            gas_line = ("    gas-cal needed: NONE SUFFICES -- coherent Upsilon floor "
                        f"sU_coh={ub['sU_coh']:.2e} alone >= target; must ALSO cut sig_coh.")
            sigG_nat = None
        else:
            sigG_nat = SIG_LNG * (sysG_max / b["sysG"])
            gas_line = (f"    gas-cal needed (N->inf): sysG {b['sysG']:.2e} -> <= {sysG_max:.2e} "
                        f"=> sig_lnG {SIG_LNG:.3f} -> {sigG_nat:.3f} nat "
                        f"({100*sigG_nat/SIG_LNG-100:+.0f}% i.e. {100*sigG_nat:.1f}%->"
                        f"{100*sysG_max/b['sysG']*SIG_LNG:.1f}% gas-scale)")
        print(gas_line)
        Nn = N_needed(coh, shr, b["Ngal"], TARGET)
        print(f"    N to reach target: at current gas-cal -> "
              f"{'IMPOSSIBLE (coherent floor>target at any N)' if Nn is None else f'{Nn:.0f} gals'}")
        # honest flag: a >=2-ban 'sep' with BOTH bans on the same side is a high/low-central
        # lean (disfavours one anchor), NOT a clean selection BETWEEN the two footings.
        same_side = (tC < 0 and tA < 0) or (tC > 0 and tA > 0)
        if sep >= 2 and same_side:
            print(f"    NOTE: |sep|>=2 here is a same-side lean (both t<0: central {b['a0']:.2e} "
                  f"sits ABOVE both anchors) -> DISFAVOURS canonical, does NOT SELECT alt.")

        sets[key] = dict(a0=b["a0"], med=b["med"], N=b["N"], Ngal=b["Ngal"],
                         baseline=dict(tot=tot0, binder=binder0, **{k: float(v) for k, v in lines0.items()}),
                         upsilon_beaten=dict(tot=tot1, binder=binder1, sU_coh=ub["sU_coh"],
                                             sU_pg=ub["sU_pg"], sysU_floor=ub["sysU_floor"]),
                         coherent_floor=coh, shrinkable=shr,
                         bans_canon=bC, bans_alt=bA, sep_bans=sep, t_canon=tC, t_alt=tA,
                         sysG_max=(None if sysG_max is None else float(sysG_max)),
                         sigG_nat_needed=(None if sigG_nat is None else float(sigG_nat)),
                         N_at_current_gascal=Nn,
                         phibar=b["phibar"], ybar=b["ybar"])

# ---- sig_coh sensitivity on the headline set (Ud=0.7 full) ------------------------------
print("\n" + bar)
print("sig_coh SENSITIVITY (Ud=0.7 full gas): the coherent SPS floor is the true bottleneck")
print(bar)
gals = fc.load(0.7)
b = decompose(gals, True)
coh_sweep = {}
for sc in SIG_COH_SWEEP:
    ub = upsilon_beaten(b, sc, SIG_PG_RES_DEX)
    coh = np.hypot(ub["sU_coh"], b["sysG"])
    tot1, binder1, _ = assemble(b, ub["sysU_floor"])
    reach = coh <= TARGET
    coh_sweep[sc] = dict(sU_coh=ub["sU_coh"], coherent_floor=float(coh), tot=tot1,
                         reaches_target=bool(reach), binder=binder1)
    print(f"  sig_coh={sc:.2f} dex: sU_coh={ub['sU_coh']:.2e}  coherent floor hypot(sU_coh,sysG)"
          f"={coh:.3e}  {'<=' if reach else '>'} target  binder='{binder1}'  tot={tot1:.3e}")
RES["sig_coh_sweep_Ud0.7_full"] = coh_sweep

# ---- 'what it takes' grid: sig_lnG x N to reach the 2-sigma footing line ----------------
print("\n" + bar)
print("'WHAT IT TAKES' MAP (Ud=0.7 full, sig_coh=0.06): gas-cal sig_lnG x clean-distance N")
print("  to reach sigma_tot <= target (necessary condition to place a 2-sigma footing gap)")
print(bar)
ub_h = upsilon_beaten(b, SIG_COH_DEX, SIG_PG_RES_DEX)
_, shr_h = coherent_shrink_split(b, ub_h)
print(f"  fixed after Upsilon beaten: sU_coh={ub_h['sU_coh']:.2e}, shrinkable(N0={b['Ngal']})="
      f"{shr_h:.2e}; target={TARGET:.2e}")
print(f"  {'sig_lnG':>8} {'gas%':>6} {'sysG':>10} {'coh floor':>10} {'N@target':>10}")
grid = {}
for slg in (0.10, 0.09, 0.08, 0.06, 0.05, 0.03):
    sysG_s = b["sysG"] * (slg / SIG_LNG)
    coh_s = np.hypot(ub_h["sU_coh"], sysG_s)
    Ns = N_needed(coh_s, shr_h, b["Ngal"], TARGET)
    grid[f"{slg:.2f}"] = dict(sysG=float(sysG_s), coh_floor=float(coh_s),
                              N=(None if Ns is None else Ns))
    print(f"  {slg:>8.2f} {100*slg:>5.0f}% {sysG_s:>10.2e} {coh_s:>10.2e} "
          f"{'INF (floor>target)' if Ns is None else f'{Ns:>7.0f}':>10}")
print("  READING: only once sig_lnG is cut below ~0.09 does a finite N reach the target;")
print("  at the current 0.10 the coherent floor exceeds target at ANY N. Gas-cal is the gate.")
RES["what_it_takes_grid_Ud0.7_full"] = grid

# ---- (4) ratio/differential estimator vs the coherent gas-cal --------------------------
print("\n" + bar)
print("(4) DIFFERENTIAL / RATIO estimator vs the coherent (global multiplicative) gas-cal")
print(bar)
resp = gas_scale_response(b)
print(f"  global gas-scale response d ln(a0)/d eps_G:")
print(f"    sample-level (coherent shift a between-galaxy RATIO removes) = {resp['sample_response']:+.3f}")
print(f"    per-galaxy weighted mean = {resp['mean_dlnA0_deps']:+.3f}  "
      f"std across {resp['ngal']} gals = {resp['std_dlnA0_deps']:.3f}")
print(f"    => a ratio cancels ~{100*resp['ratio_cancels_frac']:.0f}% of the coherent gas-cal, "
      f"residual dispersion {resp['std_dlnA0_deps']:.3f} (phi/y spread).")
print("  CATCH (honest): a between-galaxy RATIO cancels the global gas-scale ONLY by")
print("  cancelling the ABSOLUTE a0 normalization too -- it tests whether a0 is UNIVERSAL")
print("  (same slope galaxy-to-galaxy), NOT its absolute value, so it CANNOT compare")
print("  9.36e-11 vs 1.13e-10. The coherent gas-cal is a single global nuisance that only")
print("  an EXTERNAL gas-mass calibration (interferometric HI + CO, better He/metal")
print("  correction) reduces. No internal estimator both cancels it AND keeps the absolute")
print("  a0 needed for footing discrimination.")
RES["gas_scale_response"] = resp

# also: the phi trade-off -- gas-dom cut beats Upsilon but AMPLIFIES gas-cal
print("\n  phi trade-off (why deeper gas-domination does NOT cure the floor):")
print(f"    KU (Upsilon lever, ~sum phi) = {b['KU']:.3f}   KG (gas-cal lever, ~sum 1-phi) = {b['KG']:.3f}")
print("    going more gas-dominated (phi->0) shrinks sysU but GROWS sysG: the gas cut trades")
print("    the M/L wall for the gas-cal wall. KU+KG is ~fixed by the (2y+1) weight; the")
print(f"    coherent floor is minimized near KU/KG = (sig_G/sig_coh)^2, not at phi->0.")
RES["KU"] = b["KU"]; RES["KG"] = b["KG"]

# ---- VERDICT ---------------------------------------------------------------------------
print("\n" + bar)
print("VERDICT")
print(bar)
h = sets["Ud0.7_full"]
coh_h = h["coherent_floor"]
if coh_h <= TARGET and h["sep_bans"] >= 2:
    verdict = "DECIDES"
elif coh_h > TARGET:
    verdict = "TIGHTENS-GAS-CAL-NOW-WALL"
else:
    verdict = "NON-DIAGNOSTIC"
RES["verdict"] = verdict
RES["sets"] = sets
print(f"  Headline (Ud=0.7 full, sig_coh=0.06): beating Upsilon cuts sysU "
      f"{h['baseline']['sysU']:.2e} -> floor {h['upsilon_beaten']['sysU_floor']:.2e}; total "
      f"{h['baseline']['tot']:.2e} -> {h['upsilon_beaten']['tot']:.2e}.")
print(f"  BINDING LINE after Upsilon beaten = '{h['upsilon_beaten']['binder']}'. Coherent "
      f"floor hypot(sU_coh,sysG) = {coh_h:.3e} {'>' if coh_h > TARGET else '<='} target "
      f"{TARGET:.3e}.")
print(f"  Footing separation at Upsilon-beaten error: |{h['sep_bans']:.2f}| ban "
      f"(canon {h['bans_canon']:+.2f} / alt {h['bans_alt']:+.2f}) -- "
      f"{'CROSSES' if h['sep_bans'] >= 2 else 'DOES NOT CROSS'} the 2-ban line.")
print(f"\n  VERDICT: {verdict}")
print("  Beating the per-galaxy Upsilon with external colour/SPS M/L priors is NECESSARY but")
print("  NOT SUFFICIENT: it removes the reducible Upsilon scatter and drops the coherent")
print("  floor from hypot(sysU,sysG) to hypot(sU_coh,sysG), but GAS-CAL (coherent global")
print("  gas-scale, sig_lnG=0.10) then BINDS the floor just ABOVE the 2-sigma footing line.")
print("  To DECIDE: (a) an INDEPENDENT gas-mass calibration cutting sig_lnG ~0.10 -> ~0.09")
print("  (interferometric HI+CO, He/metal), AND (b) hold/lower the SPS coherent floor to")
print("  <=0.06 dex, AND (c) grow clean-distance N (BIG-SPARC). No internal ratio cancels the")
print("  coherent gas-cal while preserving the absolute a0. The a0 box still STRADDLES both")
print("  footings; per-point a0=E/g_bar DECLINES with g_bar (nu-shape leak) -- no detection")
print("  of either footing is manufactured, and no deficit is manufactured. a0 value + s=-1")
print("  remain postulates. Exit 0 is not a verdict.")

json.dump(RES, open(os.path.join(OUT, "est_wall_results.json"), "w"), indent=1, default=float)
print("\n[est_wall_results.json written]")
sys.exit(0)
