#!/usr/bin/env python3
"""
est_indep.py -- THE PER-GALAXY-INDEPENDENT LANE of the a0-line M/L-prior run.

Re-runs the a0-line model-based iterated GLS (reusing ../a0_line/fire_common.py
READ-ONLY for data, cuts, fiducials, and the a0 estimator), then SPLITS the
Upsilon (stellar M/L) systematic -- currently a single GLOBAL COHERENT number
sysU = KU*a0*SIG_LNU (SIG_LNU=0.23 nat = 0.0999 dex) that does NOT average down --
into two physically distinct pieces:

  (i)  a COHERENT SPS/IMF zero-point floor sU_coh = KU*a0*(sig_coh*ln10).
       Same for every galaxy; an offset in the IMF/SPS zero-point shifts every
       Upsilon together. EXTERNAL colours cannot touch it. Does NOT average down.
       (Schombert-McGaugh-Lelli 2019; McGaugh-Schombert 2014; Meidt+2014: the
       [3.6] M/L is SPS-tight with a coherent floor.)

  (ii) a PER-GALAXY RELATIVE part sU_pg = sqrt(sum_gal (cU_gal*sig_pg*ln10)^2),
       cU_gal = a0*sum_{pts in gal}(w*gb^2*phi*(2y+1))/S  (sum_gal cU_gal = KU*a0).
       Reducible with external per-galaxy colour/SPS M/L; RSS in quadrature so it
       AVERAGES DOWN ~1/sqrt(N_gal). External priors shrink sig_pg from its pre
       value to a residual. (Bell-de Jong 2001; SML19.)

  sysU_total = hypot(sU_coh, sU_pg).  sysG/sysD/sysI/sysEst/stat UNCHANGED.

phi = stellar share of g_bar per point, so the WHOLE Upsilon lever acts only
through the stellar mass model; deep gas-only points (phi->0) are already immune.

NO local external per-galaxy colour/SPS M/L vector exists for SPARC (L36 is a
luminosity, rotmods ship ONE fixed M/L). So the DEFENSIBLE LITERATURE
DECOMPOSITION is used and flagged (calibration-preserving: coherent (+) per-galaxy
in quadrature ~ banked 0.0999 dex; it REDISTRIBUTES, does not inflate):
  BALANCED       coherent 0.060 dex + per-galaxy 0.080 -> residual 0.040 dex
  NIR-REALISTIC  coherent 0.075 dex + per-galaxy 0.065 -> residual 0.035 dex
NIR caveat (load-bearing): at [3.6] the reducible per-galaxy part is intrinsically
small; most of the 0.1 dex is the coherent SPS/IMF zero-point external colours
CANNOT touch -> the lever's ceiling is low BY CONSTRUCTION.

Both footings: canonical a0 = cH_Lambda/Z = 9.355e-11 ; ALT = cH0/Z = 1.1305e-10
(20.9% apart). TRGB/Cepheid split (fD in {2,3}) + full gas. Ud in {0.5, 0.7}.

HONEST BOTH WAYS: this estimator caught a FAKE 3.3e-11 deficit before (raw
observed-error weighting) -> the model-based/iterated-GLS guard is re-applied
(biased=False). The honest a0 is a box straddling BOTH footings; the per-point
a0=E/g_bar DECLINES with g_bar (nu-shape leaking into magnitude) -- carried as a
caveat. a0's VALUE and the s=-1 sign remain POSTULATES regardless. No 'proves'.
Exit 0. Writes ONLY to a0_line_mlpriors/. Frozen repo READ-ONLY.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
import fire_common as fc

OUT = "/Users/carlzimmerman/new_physics/prep_2026/a0_line_mlpriors"
A0C, A0A = fc.A0C, fc.A0A            # canonical 9.355e-11 / ALT 1.1305e-10
SC, SA = fc.SC, fc.SA               # Planck anchor widths
LN10 = np.log(10.0)
SIG_LNU = fc.SIG_LNU               # 0.23 nat = 0.0999 dex, the banked GLOBAL coherent prior
HQ = {2, 3}                        # TRGB + Cepheid distance quality

DELTA = A0A - A0C                   # footing gap 1.95e-11
HALF = 0.5 * abs(DELTA)            # ~0.976e-11 : tot at/below this splits footings at 2 sigma

# The two defensible literature decompositions (dex). quadrature ~ banked 0.0999.
SCEN = {
    "balanced":      dict(sig_coh=0.060, sig_pg_pre=0.080, sig_pg_res=0.040),
    "nir_realistic": dict(sig_coh=0.075, sig_pg_pre=0.065, sig_pg_res=0.035),
}

con = []
def p(s=""):
    con.append(s); print(s)


def budget_split(gals, gas_only, sig_coh, sig_pg):
    """fc.budget re-implemented byte-for-byte on the SAME algebra, but with the
    Upsilon systematic SPLIT into a coherent floor + a per-galaxy-independent part.
    Everything else (a0 GLS, stat, sysD, sysI, sysG, sysEst) is identical to
    fire_common.budget. Returns None if the set is too small."""
    GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, gas_only)
    if len(GB) < 10:
        return None
    a0, fint, c2n, w = fc.gls(GB, GO, FV)               # model-based iterated GLS (the guard)
    med = float(np.median((GO**2 - GB**2) / GB))
    S = np.sum(w * GB**2)
    sig_stat = np.sqrt(1 / S)
    yq = GB / a0
    # per-galaxy distance + inclination systematics (unchanged from fc.budget)
    varD = varI = 0.0
    cU_gal = []                                          # per-galaxy Upsilon coefficient
    for k in sorted(set(GAL.tolist())):
        m = GAL == k
        cD = a0 * np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S
        cI = a0 * np.sum(w[m] * GB[m]**2 * 4 * (yq[m] + 1) * CTI[m]) / S
        varD += (cD * SLD[m][0])**2
        varI += (cI * fc.SIG_INC)**2
        cU_gal.append(a0 * np.sum(w[m] * GB[m]**2 * PHI[m] * (2 * yq[m] + 1)) / S)
    cU_gal = np.array(cU_gal)
    # ---- the Upsilon SPLIT ----
    KU_a0 = np.sum(w * GB**2 * PHI * (2 * yq + 1)) / S * a0   # == sum_gal cU_gal == fc.budget KU*a0
    sU_coh = KU_a0 * (sig_coh * LN10)                        # coherent floor: does NOT average down
    sU_pg = np.sqrt(np.sum((cU_gal * (sig_pg * LN10))**2))    # per-galaxy indep: averages ~1/sqrt(N)
    sysU = float(np.hypot(sU_coh, sU_pg))
    # banked (fully-coherent) sysU for reference: KU*a0*SIG_LNU
    sysU_banked = float(KU_a0 * SIG_LNU)
    # per-galaxy-independent floor if the SAME banked 0.0999 dex were fully independent
    sU_indep_full = float(np.sqrt(np.sum((cU_gal * SIG_LNU)**2)))
    # gas-cal (unchanged, coherent)
    KG_a0 = np.sum(w * GB**2 * (1 - PHI) * (2 * yq + 1)) / S * a0
    sG = float(KG_a0 * fc.SIG_LNG)
    sEst = abs(a0 - med) / 2.0
    tot = float(np.sqrt(sig_stat**2 + varD + varI + sysU**2 + sG**2 + sEst**2))
    return dict(N=int(len(GB)), Ngal=len(cU_gal), a0hat=float(a0), a0med=med,
                fint=float(fint), stat=float(sig_stat), sysD=float(np.sqrt(varD)),
                sysI=float(np.sqrt(varI)), sysU=sysU, sU_coh=float(sU_coh),
                sU_pg=float(sU_pg), sysU_banked=sysU_banked,
                sU_indep_full=sU_indep_full, sysG=sG, sysEst=float(sEst), tot=tot)


def logB_logflat(a0hat, tot, astar, s_anchor, lo=1e-11, hi=1e-9):
    """log10 Bayes factor M0(a0==astar)/M1(log-flat prior), log-space, fractional
    errors (verbatim shape of the banked fire_occam.logB). Returns (bans, t_sigma).
    Positive bans => data favour the anchor; t_sigma is the convention-robust number."""
    xhat = np.log(a0hat); s_meas = tot / a0hat; s_anch = s_anchor / astar
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anch)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff)**2 - np.log(np.sqrt(2*np.pi)*s_eff)
    Lx = np.exp(-0.5*((xg - xhat)/s_meas)**2) / (np.sqrt(2*np.pi)*s_meas)
    lnZ1 = np.log(np.trapz(Lx / (np.log(hi)-np.log(lo)), xg))
    return float((lnZ0 - lnZ1)/LN10), float((np.log(astar)-xhat)/s_eff)


p("=" * 82)
p("PER-GALAXY-INDEPENDENT LANE -- a0-line Upsilon split (coherent floor + reducible pg)")
p(f"footings: canonical={A0C:.4e} (cH_L/Z)  ALT={A0A:.4e} (cH0/Z)  gap={100*DELTA/A0C:.1f}%")
p(f"|Delta|/2 = {HALF*1e12:.3f}e-12  <- tot at/below this splits footings at 2 sigma")
p(f"banked Upsilon prior: SIG_LNU={SIG_LNU} nat = {SIG_LNU/LN10:.4f} dex, FULLY COHERENT (floor)")
p("credit: Schombert-McGaugh-Lelli 2019; Meidt+2014; McGaugh-Schombert 2014;")
p("        Bell-de Jong 2001; Lelli-McGaugh-Schombert 2016 (SPARC). a0 value + s=-1 POSTULATES.")
p("=" * 82)

summary = {}
for Ud in (0.5, 0.7):
    gals = fc.load(Ud)
    gals_hq = [g for g in gals if g["fD"] in HQ]
    for setname, gset in (("ALLgas", gals), ("TRGB", gals_hq)):
        base = fc.budget(gset, gas_only=True)            # banked (fully-coherent sysU) reference
        p(f"\n{'#'*74}")
        p(f"## Ud={Ud}  set={setname}  "
          f"(N={base['N']} pts / Ngal={base['Ngal']} gal, a0_hat={base['a0hat']*1e10:.4f}e-10)")
        p(f"   BANKED (fully-coherent Upsilon): sysU={base['sysU']*1e12:.2f}  "
          f"sysG={base['sysG']*1e12:.2f}  sysEst={base['sysEst']*1e12:.2f}  "
          f"sysD={base['sysD']*1e12:.2f}  sysI={base['sysI']*1e12:.2f}  "
          f"stat={base['stat']*1e12:.2f} -> tot={base['tot']*1e12:.2f}e-12")
        a0 = base["a0hat"]
        # HARD LIMIT: zero the Upsilon systematic ENTIRELY (perfect external M/L,
        # coherent floor included) -- the irreducible non-Upsilon wall.
        tot_noU = float(np.sqrt(base["stat"]**2 + base["sysD"]**2 + base["sysI"]**2
                                + base["sysG"]**2 + base["sysEst"]**2))
        sep_ban_noU = abs(logB_logflat(a0, tot_noU, A0C, SC)[0]
                          - logB_logflat(a0, tot_noU, A0A, SA)[0])
        sep_sig_noU = abs(logB_logflat(a0, tot_noU, A0C, SC)[1]
                          - logB_logflat(a0, tot_noU, A0A, SA)[1])
        p(f"   HARD LIMIT sysU->0 (perfect external M/L): tot={tot_noU*1e12:.2f}e-12 "
          f"(<= |Delta|/2={HALF*1e12:.2f}? {'YES' if tot_noU<=HALF else 'NO'}); "
          f"footing sep {sep_sig_noU:.2f} sigma / {sep_ban_noU:.2f} bans "
          f"-> Upsilon is {'THE wall' if tot_noU<=HALF else 'NOT the binding wall'}")
        skey = f"{Ud}|{setname}"
        summary[skey] = dict(Ud=Ud, set=setname, N=base["N"], Ngal=base["Ngal"],
                             a0hat=a0, banked=base, tot_noU=tot_noU,
                             sep_sig_noU=sep_sig_noU, sep_ban_noU=sep_ban_noU,
                             upsilon_is_wall=bool(tot_noU <= HALF), scenarios={})
        for scen, pr in SCEN.items():
            b = budget_split(gset, True, pr["sig_coh"], pr["sig_pg_res"])
            # shift of a0_hat: NONE (the split touches only the error budget, not a0);
            # report it explicitly so the reader sees a0 is unmoved.
            a0_shift = b["a0hat"] - a0
            # footing bans + sigma at the NEW total error
            bc, tc = logB_logflat(a0, b["tot"], A0C, SC)
            ba, ta = logB_logflat(a0, b["tot"], A0A, SA)
            sep_ban = abs(bc - ba)
            sep_sig = abs(tc - ta)                       # separation of the two footings in sigma
            cross2 = (sep_ban >= 2.0) and (b["tot"] <= HALF)
            p(f"\n  [{scen}] coherent {pr['sig_coh']:.3f} dex + per-gal residual "
              f"{pr['sig_pg_res']:.3f} dex (pre {pr['sig_pg_pre']:.3f}):")
            p(f"     sysU: banked {b['sysU_banked']*1e12:.2f} -> SPLIT "
              f"coh {b['sU_coh']*1e12:.2f} (+) pg_res {b['sU_pg']*1e12:.2f} "
              f"= {b['sysU']*1e12:.2f}e-12  "
              f"(fully-indep floor of 0.0999dex would be {b['sU_indep_full']*1e12:.2f})")
            p(f"     tot: {base['tot']*1e12:.2f} -> {b['tot']*1e12:.2f}e-12   "
              f"(<= |Delta|/2={HALF*1e12:.2f}? {'YES' if b['tot']<=HALF else 'NO'})")
            p(f"     a0_hat={a0*1e10:.4f}e-10 (shift {a0_shift*1e12:+.3f}e-12, the split "
              f"moves ONLY the error budget)")
            p(f"     footing bans (log-flat): canon {bc:+.2f} | alt {ba:+.2f} "
              f"-> separation {sep_ban:.2f} bans")
            p(f"     footing sigma (robust) : canon {tc:+.2f}s | alt {ta:+.2f}s "
              f"-> separation {sep_sig:.2f} sigma")
            fav = "canonical" if bc > ba else "ALT"
            p(f"     leans {fav}; CROSS 2 bans AND tot<=|Delta|/2 (2 sigma)? "
              f"{'YES -- DECIDES' if cross2 else 'NO -- non-decisive'}")
            summary[skey]["scenarios"][scen] = dict(
                sig_coh=pr["sig_coh"], sig_pg_res=pr["sig_pg_res"],
                sysU_banked=b["sysU_banked"], sU_coh=b["sU_coh"], sU_pg=b["sU_pg"],
                sysU=b["sysU"], sysG=b["sysG"], sysEst=b["sysEst"], sysD=b["sysD"],
                sysI=b["sysI"], stat=b["stat"], tot=b["tot"], tot_banked=base["tot"],
                a0hat=a0, a0_shift=a0_shift, tot_below_half=bool(b["tot"] <= HALF),
                bans_canon=bc, bans_alt=ba, sep_ban=sep_ban, t_canon=tc, t_alt=ta,
                sep_sig=sep_sig, leans=fav, cross2=bool(cross2))

# ---- caveat: per-point a0 = E/gb DECLINES with gb (nu-shape leaking into magnitude) ----
p(f"\n{'='*82}")
p("CAVEAT (carried, both ways): per-point a0=E/g_bar trend, Ud=0.7 TRGB gas-dom terciles")
gals = fc.load(0.7)
GBh, GOh, FVh, GALh = ([], [], [], [])
for g in [g for g in gals if g["fD"] in HQ]:
    m = g["gasdom"]
    GBh += list(g["gb"][m]); GOh += list(g["go"][m])
GBh, GOh = np.array(GBh), np.array(GOh)
per = (GOh**2 - GBh**2) / GBh
edges = np.percentile(GBh, [0, 33.33, 66.67, 100])
tr = []
for i in range(3):
    mm = (GBh >= edges[i]) & (GBh <= edges[i+1])
    tr.append(float(np.median(per[mm])))
    p(f"   gb tercile {i+1}: median a0=E/gb = {tr[i]*1e10:.3f}e-10 (n={mm.sum()})")
p(f"   -> a0(E/gb) {'DECLINES' if tr[-1] < tr[0] else 'rises'} with g_bar "
  f"({tr[0]*1e10:.2f}->{tr[-1]*1e10:.2f}e-10): nu-SHAPE curvature leaking into the "
  f"magnitude; the box straddles BOTH footings, NOT a clean single-footing detection.")

json.dump(summary, open(os.path.join(OUT, "est_indep_results.json"), "w"), indent=1)
open(os.path.join(OUT, "_est_indep_console.txt"), "w").write("\n".join(con))
p(f"\n{'='*82}")
p("[est_indep_results.json + _est_indep_console.txt written]  EXIT 0 (not a verdict).")
