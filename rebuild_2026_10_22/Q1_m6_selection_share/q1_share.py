#!/usr/bin/env python3
"""Q1_m6_selection_share: measured share q of the local stellar-mass inventory held by galaxies that need M6 (not a
satellite AND system baryons below X43's crossover mapped through EM1 R1), GAMA G3C v10 + Lambdar v20, 1/Vmax weights;
then M6N1's verdict re-evaluated at the measured q. FROZEN_CRITERIA.md committed alone first (a46adc2f90).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
no LCDM input (G3C MassA is never read); not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I q1_share.py      (Q1_MUTATE=1 twin)
"""
import os, sys, csv, json, hashlib, resource, time
import numpy as np
from astropy.io import fits

MUT = os.environ.get("Q1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.join(REPO, "_external_data", "q1_gama")
T0 = time.time()
OUT = open(os.path.join(HERE, f"q1_share{TAG}.out"), "w")
RES = {"lane": "Q1_m6_selection_share", "criteria": "a46adc2f90", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; no LCDM input; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def dump():
    RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    json.dump(RES, open(os.path.join(HERE, f"q1_share_results{TAG}.json"), "w"), indent=1, default=float)


FOOTS = ("canonical", "alt")
P("Q1_m6_selection_share" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria a46adc2f90; kappa = 1/2 FITTED; footings never pooled; no particle; no LCDM input; not theory closed")

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
SHA = {"G3CGalv10.csv": "051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8",
       "G3CFoFGroupv10.csv": "eb81594ad6994e3fb44d2ee7c2e4eac4a99e3c7c27750bbf620d9f103a5b96c7",
       "StellarMassesLambdarv20.fits": "731170b792f26470ce3d35dffe397979465a16251fe4958f1a6ab8d5c053ca7e"}
if MUT:
    SHA["StellarMassesLambdarv20.fits"] = SHA["StellarMassesLambdarv20.fits"][:-1] + "0"   # m2
POP = os.path.join(REPO, "closure_program_2026_10_27", "population", "run", "results.json")
POP_SHA = "0131d5da47e442c92dfd716fda8b5d036b0808940079fc8e0dd62d2445746323"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


sha_ok = {k: sha(os.path.join(EXT, k)) == v for k, v in SHA.items()}
sha_ok["closure population"] = sha(POP) == POP_SHA
m6 = json.load(open(os.path.join(HERE, "..", "M6N1_minimum_patch_need", "m6n1_need_results.json")))
x58 = json.load(open(os.path.join(HERE, "..", "X58_object_keyed_switch", "x58_x53copy_law_x48_results.json")))
x62 = json.load(open(os.path.join(HERE, "..", "X62_environment_keyed_switch", "x62_x53copy_law_a2_results.json")))
em1 = json.load(open(os.path.join(HERE, "..", "EM1_emergent_dust_law", "em1_emergent_results.json")))
pop = json.load(open(POP))
XMIN = {f: m6["footings"][f]["x_min"] for f in FOOTS}
EPS = {f: m6["footings"][f]["eps_ref"] for f in FOOTS}
FALLOW = {f: m6["footings"][f]["F_allowed"] for f in FOOTS}
FINV = {"stellar": m6["inputs"]["F_inv"]["stellar"], "stars+cold gas": m6["inputs"]["F_inv"]["stars+cold gas"]}
R1A, R1B = em1["rows"]["A_c2b_refit"]["R1"]["a"], em1["rows"]["A_c2b_refit"]["R1"]["b"]
XOVER = {"PRIMARY cf4": {f: x58["crossover_logM"][f"{f}|cf4"] for f in FOOTS},
         "NAT-X48": {f: x58["crossover_logM"][f"{f}|x48"] for f in FOOTS},
         "NAT-A2": {f: x62["crossover_logM"][f"{f}|x48"] for f in FOOTS}}
F_ABOVE_1E8 = pop["gsmf"]["mass_ranges"]["above_1e8"]["fraction_of_fitted_stellar_mass"]
F_ABOVE_1E9 = pop["gsmf"]["mass_ranges"]["above_1e9"]["fraction_of_fitted_stellar_mass"]
RHO_STAR_POP = pop["census"]["rho_star_Msun_Mpc3"]
tgt = [(XMIN["canonical"], 0.835), (XMIN["alt"], 0.977), (EPS["canonical"], 0.191), (EPS["alt"], 0.163),
       (FALLOW["canonical"], 0.0613), (FALLOW["alt"], 0.0490), (FINV["stellar"], 0.0470), (FINV["stars+cold gas"], 0.0598)]
rep_ok = all(abs(a - b) <= 6e-4 for a, b in tgt)
xo_ok = round(XOVER["PRIMARY cf4"]["canonical"], 4) == 12.0945 and round(XOVER["PRIMARY cf4"]["alt"], 4) == 12.4339
r1_ok = (R1A, R1B) == (11.18, 0.9)
s0 = all(sha_ok.values()) and rep_ok and xo_ok and r1_ok
P(f"  sha256: {sha_ok}")
P(f"  M6N1 inputs (3 dp) {rep_ok}: x_min {XMIN}, eps_ref {EPS}, F_allowed {FALLOW}, F_inv {FINV}")
P(f"  X58 cf4 crossover {xo_ok}: {XOVER['PRIMARY cf4']}; EM1 R1 (a, b) = ({R1A}, {R1B}) {r1_ok}")
check("S0", s0, f"sha {all(sha_ok.values())}, M6N1 {rep_ok}, crossover {xo_ok}, R1 {r1_ok}", "all")
RES["inputs"] = {"x_min": XMIN, "eps_ref": EPS, "F_allowed": FALLOW, "F_inv": FINV, "R1": [R1A, R1B],
                 "crossover_logM200": XOVER, "gsmf_above_1e8": F_ABOVE_1E8}
if not s0 and not MUT:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"; dump(); sys.exit(2)


def lmbx(lm200):
    """EM1 R1 inverted: log M_b at which the system's route-E M200 equals the crossover."""
    return 10.0 + (lm200 - R1A) / R1B


LMBX = {v: {f: lmbx(XOVER[v][f]) for f in FOOTS} for v in XOVER}
P("  crossover in system baryons, log M_b,x: " + "; ".join(f"{v} {LMBX[v]['canonical']:.3f} / {LMBX[v]['alt']:.3f}" for v in LMBX))
RES["crossover_logMb"] = LMBX


def needs_m6(is_sat, lmbsys, lmb_x, sat_low=False):
    """The frozen predicate: not a satellite AND system baryons below the crossover."""
    below = lmbsys < lmb_x
    if MUT:
        return is_sat & below                                                  # m1: satellite key inverted
    if sat_low:
        return below
    return (~is_sat) & below


# ============================================================== DATA
P("\n== DATA")
with open(os.path.join(EXT, "G3CGalv10.csv")) as fh:
    rd = csv.reader(fh); hdr = next(rd); rows = list(rd)
ci = {k: i for i, k in enumerate(hdr)}
cat = np.array([int(r[ci["CATAID"]]) for r in rows])
ra = np.array([float(r[ci["RA"]]) for r in rows])
zg = np.array([float(r[ci["Z"]]) for r in rows])
rp = np.array([float(r[ci["Rpetro"]]) for r in rows])
gid = np.array([int(r[ci["GroupID"]]) for r in rows])
rank = np.array([int(r[ci["RankIterCen"]]) for r in rows])
del rows
with open(os.path.join(EXT, "G3CFoFGroupv10.csv")) as fh:
    rd = csv.reader(fh); hdr2 = next(rd); ng_file = sum(1 for _ in rd)
lam = fits.open(os.path.join(EXT, "StellarMassesLambdarv20.fits"), memmap=True)[1].data
L = {k: np.array(lam[k]) for k in ("CATAID", "nQ", "SURVEY_CLASS", "fluxscale", "zmax_19p8", "logmstar")}
o = np.argsort(L["CATAID"]); lc = L["CATAID"][o]
pos = np.clip(np.searchsorted(lc, cat), 0, len(lc) - 1)
hit = lc[pos] == cat
idx = o[pos]
nq = np.where(hit, L["nQ"][idx], 0)
sc = np.where(hit, L["SURVEY_CLASS"][idx], 0)
fs = np.where(hit, L["fluxscale"][idx], np.nan).astype(float)
zmax = np.where(hit, L["zmax_19p8"][idx], np.nan).astype(float)
lms = np.where(hit, L["logmstar"][idx], np.nan).astype(float)
H_NAT, OM_NAT = 0.6856427, 0.2976016
lms_nat = lms + 2 * np.log10(0.7 / H_NAT)
good_m = hit & (nq >= 3) & np.isfinite(lms_nat)
P(f"  G3CGal {len(cat)} galaxies, groups in G3CGal {len(np.unique(gid[gid > 0]))}, G3CFoFGroup rows {ng_file}; "
  f"Lambdar matched {hit.sum()}, with nQ>=3 and finite logmstar {good_m.sum()}")

FIELDS = [(129.0, 141.0), (174.0, 186.0), (211.5, 223.5)]
in_field = np.zeros(len(cat), bool); strip = np.full(len(cat), -1)
for k, (a, b) in enumerate(FIELDS):
    m = (ra >= a) & (ra < b); in_field |= m
    strip[m] = 5 * k + np.minimum(((ra[m] - a) / ((b - a) / 5)).astype(int), 4)
ZLO, ZHI = 0.01, 0.10
base = in_field & (rp <= 19.8) & (zg >= ZLO) & (zg <= ZHI)
k1 = (good_m & base).sum() / base.sum()
check("K1", k1 >= 0.95, f"Lambdar nQ>=3 match fraction {k1:.4f} of {base.sum()} G3C galaxies in the cuts", ">= 0.95")

# Comoving distance on the L1 native background (flat, constant dark-energy density) and the Hubble-law variant
C_KMS = 299792.458
zz = np.linspace(0.0, 0.12, 24001)
Ez = np.sqrt(OM_NAT * (1 + zz) ** 3 + 1 - OM_NAT)
DC_NAT = C_KMS / (100 * H_NAT) * np.concatenate([[0], np.cumsum(0.5 * (1 / Ez[1:] + 1 / Ez[:-1]) * np.diff(zz))])
DC_HL = C_KMS / (100 * H_NAT) * zz


def vc(z, hubble=False):
    return np.interp(z, zz, DC_HL if hubble else DC_NAT) ** 3


# ============================================================== MEASUREMENT
issat = (gid > 0) & (rank != 1)
gidx = np.unique(gid[gid > 0], return_inverse=True)[1]
grp_row = np.full(len(cat), -1); grp_row[gid > 0] = gidx
ngr = grp_row.max() + 1


def system_logmb(mass, su=1.0, sg=1.0):
    """log of Sigma M* over each galaxy's system (all G3C members, any z or mass); the galaxy alone if ungrouped."""
    mm = np.where(np.isfinite(mass), mass, 0.0)
    gs = np.bincount(grp_row[gid > 0], weights=mm[gid > 0], minlength=ngr)
    tot = np.where(gid > 0, gs[np.maximum(grp_row, 0)] * su, mm) * sg
    with np.errstate(divide="ignore"):
        return np.log10(tot)


def weights(zlo=ZLO, zhi=ZHI, hubble=False):
    zm = np.minimum(zmax, zhi)
    v = vc(zm, hubble) - vc(zlo, hubble)
    return np.where(zm > zlo, 1.0 / np.where(v > 0, v, np.inf), 0.0)


M_PRIM = 10 ** lms_nat
fs_ok = np.isfinite(fs) & (fs >= 1) & (fs <= 10)
M_FS = np.where(fs_ok, M_PRIM * np.where(fs_ok, fs, 1.0), M_PRIM)


def sample(mass, floor=8.0, zlo=ZLO, zhi=ZHI):
    return base & good_m & (np.log10(np.where(np.isfinite(mass), mass, 1.0)) >= floor) & (zg >= zlo) & (zg <= zhi) & (zmax > zlo)


def qshare(need, sel, w, mass, drop=None):
    s = sel if drop is None else sel & (strip != drop)
    wm = w[s] * mass[s]
    return float(wm[need[s]].sum() / wm.sum())


def measure(f, lmb_x, mass=M_PRIM, su=1.0, sg=1.0, zlo=ZLO, zhi=ZHI, hubble=False, floor=8.0, sat_low=False, jk=False):
    lsys = system_logmb(mass, su, sg)
    need = needs_m6(issat, lsys, lmb_x, sat_low)
    sel = sample(mass, floor, zlo, zhi)
    w = weights(zlo, zhi, hubble)
    q = qshare(need, sel, w, mass)
    if not jk:
        return q
    qs = np.array([qshare(need, sel, w, mass, d) for d in range(15)])
    sjk = float(np.sqrt(14 / 15 * ((qs - qs.mean()) ** 2).sum()))
    return q, sjk, need, sel, w


P("\n== MEASUREMENT (1/Vmax-weighted stellar-mass share; 0.01 <= z <= 0.10; log M* >= 8.0 native)")
t_tail = 1 - F_ABOVE_1E8
MEAS = {}
for f in FOOTS:
    lx = LMBX["PRIMARY cf4"][f]
    q, sjk, need, sel, w = measure(f, lx, jk=True)
    # K3 partition
    wm = w[sel] * M_PRIM[sel]
    part = abs(wm[need[sel]].sum() + wm[~need[sel]].sum() - wm.sum()) / wm.sum()
    check(f"K3[{f}]", part < 1e-12 and sel.sum() == need[sel].sum() + (~need[sel]).sum(),
          f"partition residual {part:.1e}; {sel.sum()} galaxies, needs {need[sel].sum()}", "< 1e-12, each once")
    sys_terms = {
        "SZ z-split": abs(measure(f, lx, zlo=ZLO, zhi=0.06) - measure(f, lx, zlo=0.06, zhi=ZHI)) / 2,
        "SF fluxscale": abs(measure(f, lx, mass=M_FS) - q) / 2,
        "SU unseen x1.25": abs(measure(f, lx, su=1.25) - q) / 2,
        "SG gas x1.3": abs(measure(f, lx, sg=1.3) - q) / 2,
        "SC Hubble law": abs(measure(f, lx, hubble=True) - q) / 2}
    zsl = (measure(f, lx, zlo=ZLO, zhi=0.06), measure(f, lx, zlo=0.06, zhi=ZHI))
    ssys = float(np.sqrt(sum(v ** 2 for v in sys_terms.values())))
    stot = float(np.hypot(sjk, ssys))
    qlo_full, qhi_full = (1 - t_tail) * q, (1 - t_tail) * q + t_tail
    qlo, qhi = max(0.0, qlo_full - 2 * stot), min(1.0, qhi_full + 2 * stot)
    # ungrouped-only and per-decade
    lm = lms_nat
    ung = sel & (gid == 0)
    q_ung = float((w[ung] * M_PRIM[ung]).sum() / wm.sum())
    q_sat = float((w[sel & issat] * M_PRIM[sel & issat]).sum() / wm.sum())
    dec = {}
    for a in (8, 9, 10, 11):
        m = sel & (lm >= a) & (lm < a + 1)
        if m.sum():
            ww = w[m] * M_PRIM[m]
            dec[f"{a}-{a+1}"] = {"q_in_decade": float(ww[need[m]].sum() / ww.sum()), "share_of_inventory": float(ww.sum() / wm.sum()), "n": int(m.sum())}
    MEAS[f] = {"q_star": q, "sigma_jk": sjk, "systematics_half_diff": sys_terms, "z_slices": zsl, "sigma_sys": ssys,
               "sigma_tot": stot, "tail_below_1e8": t_tail, "q_full_bracket": [qlo_full, qhi_full],
               "q_star_lo_2sigma": qlo, "q_star_hi_2sigma": qhi, "ungrouped_share": q_ung, "satellite_share": q_sat,
               "per_decade": dec, "n_sample": int(sel.sum()), "n_needs": int(need[sel].sum())}
    P(f"\n  [{f}] crossover log M_b,x {lx:.3f}:  q_star = {q:.4f} +- {sjk:.4f} (jk)  +- {ssys:.4f} (sys)  -> sigma_tot {stot:.4f}")
    P("     systematics (half-diff): " + ", ".join(f"{k} {v:.4f}" for k, v in sys_terms.items()) + f"; z slices {zsl[0]:.4f} / {zsl[1]:.4f}")
    P(f"     tail t = {t_tail:.4f} -> q_full in [{qlo_full:.4f}, {qhi_full:.4f}];  2-sigma interval [{qlo:.4f}, {qhi:.4f}]")
    P(f"     ungrouped share {q_ung:.4f} (Alpaslan+2015: 0.30); satellite share {q_sat:.4f}; n {sel.sum()}, needs {need[sel].sum()}")
    P("     per decade: " + "; ".join(f"{k}: q {v['q_in_decade']:.3f}, inv {v['share_of_inventory']:.3f}" for k, v in dec.items()))

# K2 GSMF shape and reported rho*
selg = sample(M_PRIM); wg = weights()
wm_all = wg[selg] * M_PRIM[selg]
fr = wm_all[lms_nat[selg] >= 9].sum() / wm_all.sum()
ref = F_ABOVE_1E9 / F_ABOVE_1E8
check("K2", abs(fr - ref) <= 0.05, f"Vmax mass fraction >1e9 of >1e8 {fr:.4f} vs closure GSMF {ref:.4f}", "|diff| <= 0.05")
omega = 180.0 * (np.pi / 180) ** 2
rho = wm_all.sum() * 3 / omega
P(f"  reported: rho* (log M* >= 8, 180 deg^2) = {rho:.3e} Msun/Mpc^3 vs closure {RHO_STAR_POP:.3e} (ratio {rho / RHO_STAR_POP:.3f})")
RES["rho_star_check"] = {"gama_vmax": rho, "closure": RHO_STAR_POP, "ratio": rho / RHO_STAR_POP}

# K4 predicate unit tests
k4 = True; det = []
for f in FOOTS:
    lx = LMBX["PRIMARY cf4"][f]
    cases = [(False, 10.0, True), (True, np.log10(2e10), False), (False, 12.5, False), (False, lx + 0.1, False), (False, lx - 0.1, True)]
    got = [bool(needs_m6(np.array([s]), np.array([m]), lx)[0]) for s, m, _ in cases]
    ok = got == [e for _, _, e in cases]
    k4 &= ok; det.append(f"{f} {got}")
check("K4", k4, "; ".join(det), "[T, F, F, F, T] per footing")

# ============================================================== VARIANTS (reported)
P("\n== VARIANTS (reported, point q; not the graded verdict)")
VAR = {}
for f in FOOTS:
    lx = LMBX["PRIMARY cf4"][f]
    VAR[f] = {"NAT-X48": measure(f, LMBX["NAT-X48"][f]), "NAT-A2": measure(f, LMBX["NAT-A2"][f]),
              "band +0.5 dex M200": measure(f, lx + 0.5 / R1B), "band -0.5 dex M200": measure(f, lx - 0.5 / R1B),
              "SAT-LOW": measure(f, lx, sat_low=True), "floor 8.5": measure(f, lx, floor=8.5)}
    P(f"  [{f}] " + "; ".join(f"{k} {v:.4f}" for k, v in VAR[f].items()))

# ============================================================== M6N1 RE-EVALUATED
P("\n== M6N1 re-evaluated at the measured q (its formula, its inputs)")
FGAS = FINV["stars+cold gas"] - FINV["stellar"]


def qcold(qs, qg):
    return (FINV["stellar"] * qs + FGAS * qg) / FINV["stars+cold gas"]


def verdict(f, qlo, qhi):
    corners = {"q_lo | stellar": (qlo, FINV["stellar"]), "q_hi | stellar": (qhi, FINV["stellar"]),
               "q_lo | stars+cold gas": (qcold(qlo, qlo), FINV["stars+cold gas"]),
               "q_hi | stars+cold gas": (qcold(qhi, 1.0), FINV["stars+cold gas"])}
    out = {}
    for k, (q, Fi) in corners.items():
        fmin = XMIN[f] * q * Fi
        fref = fmin / EPS[f]
        out[k] = {"q": q, "F_inv": Fi, "F_need_min": fmin, "F_need_eps_ref": fref, "eps_crit": fmin / FALLOW[f],
                  "ratio_to_budget_eps_ref": fref / FALLOW[f], "min_ok": fmin <= FALLOW[f], "ref_ok": fref <= FALLOW[f]}
    mins = [c["min_ok"] for c in out.values()]; refs = [c["ref_ok"] for c in out.values()]
    if not any(mins):
        v = "M6 OVER BUDGET EVEN AT FULL RETENTION"
    elif all(mins) and not any(refs):
        v = "BUDGET BINDS AT RECORD RETENTION"
    elif all(refs):
        v = "BUDGET DOES NOT BIND"
    else:
        v = "MIXED: " + ", ".join(k for k, c in out.items() if c["ref_ok"]) + " within budget at eps_ref"
    return v, out


FOOT = {}
for f in FOOTS:
    m = MEAS[f]
    v, corners = verdict(f, m["q_star_lo_2sigma"], m["q_star_hi_2sigma"])
    qcrit = {k: FALLOW[f] * EPS[f] / (XMIN[f] * Fi) for k, Fi in FINV.items()}
    vv = {}
    for k, qv in VAR[f].items():
        lo = max(0.0, (1 - t_tail) * qv - 2 * m["sigma_tot"]); hi = min(1.0, (1 - t_tail) * qv + t_tail + 2 * m["sigma_tot"])
        vv[k] = verdict(f, lo, hi)[0]
    FOOT[f] = {"measurement": m, "corners": corners, "verdict": v, "q_crit_eps_ref": qcrit, "variant_q": VAR[f], "variant_verdicts": vv}
    P(f"\n  [{f}] q_star 2-sigma [{m['q_star_lo_2sigma']:.4f}, {m['q_star_hi_2sigma']:.4f}];  q_crit(eps_ref) stellar {qcrit['stellar']:.4f}, stars+cold gas {qcrit['stars+cold gas']:.4f}")
    for k, c in corners.items():
        P(f"     {k:24s} q {c['q']:.4f}: F_need,min {c['F_need_min']:.5f}, F_need(eps_ref) {c['F_need_eps_ref']:.5f} = {c['ratio_to_budget_eps_ref']:.2f} x budget; eps_crit {c['eps_crit']:.3f} vs eps_ref {EPS[f]:.3f}")
    P(f"     VERDICT [{f}]: {v}")
    P("     variant verdicts: " + "; ".join(f"{k}: {x}" for k, x in vv.items()))
RES["footings"] = FOOT
RES["verdict"] = {f: FOOT[f]["verdict"] for f in FOOTS}

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("K5", rss < 1.0, f"peak RSS {rss:.3f} GB", "< 1 GB")
allpass = all(c["pass"] for c in RES["checks"].values())
P(f"\nChecks: {sum(c['pass'] for c in RES['checks'].values())}/{len(RES['checks'])} pass" + (" [MUTATE: must fail S0 and K4]" if MUT else ""))
P(f"VERDICT: canonical {RES['verdict']['canonical']} | alt {RES['verdict']['alt']}")
dump()
sys.exit(0 if allpass else 1)
