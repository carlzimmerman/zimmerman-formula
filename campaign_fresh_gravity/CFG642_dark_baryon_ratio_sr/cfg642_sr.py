#!/usr/bin/env python3
"""
CFG642 -- non-numerology symbolic regression for Omega_c/Omega_b (criteria: FROZEN_CRITERIA.md, committed first).

Buckingham-pi monomials F = P * g1^n1 g2^n2 g3^n3 g4^n4 kappa^n5 at a named epoch, with
  g1 = G rho_b/H^2, g2 = G rho_r/H^2, g3 = G rho_DE/H^2, g4 = a0/(c H), all at that epoch;
exponents -2..2 step 1/2; 11 declared geometric prefactors; epochs today / z* / z_eq / BBN; two footings never
pooled. Gates: (a) FDR vs random decoy targets and shuffled inputs; (b) interlock; (c) omega_c elasticity;
epoch rule; (d) BBN omega_b and SH0ES h. kappa = 1/2 FITTED. Nothing here derives 5.364.

MUTATE=1 replaces the target with one planted grammar member at 0.001% precision (writes *_MUTATE outputs).
"""
import json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = open(os.path.join(HERE, f"cfg642{TAG}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


RNG = np.random.default_rng(642)
LN2 = math.log(2.0)

# ------------------------------------------------------------------------------------------------ inputs
WB, SWB = 0.02237, 0.00015          # Planck 2018 TT,TE,EE+lowE+lensing
WC, SWC = 0.1200, 0.0012
H_P, OL_P = 0.6736, 0.6847
T0 = 2.7255
WG = 2.4728e-5 * (T0 / 2.7255) ** 4
NEFF = 3.046
WNU = 0.06 / 93.14
ZSTAR_P = 1089.92
KAPPA = 0.5                          # FITTED
fp0 = json.load(open(os.path.join(ROOT, "real_research/derivation_chain_2026/FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": fp0["a0_canonical"], "alt": fp0["a0_rho_total"]}
C_LIGHT, MPC = 2.99792458e8, 3.0856775814913673e22
KB_MEV = 8.617333262e-11
Z_BBN = 0.07 / (KB_MEV * T0) - 1.0
H_SHOES = 0.7304                     # Riess+22 (on disk: CFG493)
OM_DESI, SOM_DESI = 0.2975, 0.0086   # DESI DR2 BAO alone (on disk: nbody_2026/routeB_dust_to_dark_energy_2026.py)
SH_P = 0.0054

R = WC / WB
SR = R * math.hypot(SWC / WC, SWB / WB)
REL = SR / R

PREF_NAMES = ["1", "2", "1/2", "pi", "1/pi", "4pi", "1/(4pi)", "8pi", "1/(8pi)", "8pi/3", "3/(8pi)"]
PREF = np.log10(np.array([1, 2, .5, math.pi, 1 / math.pi, 4 * math.pi, 1 / (4 * math.pi), 8 * math.pi,
                          1 / (8 * math.pi), 8 * math.pi / 3, 3 / (8 * math.pi)]))
EPOCHS = ["today", "recombination", "equality", "BBN"]
GNAMES = ["G rho_b/H^2", "G rho_r/H^2", "G rho_DE/H^2", "a0/(cH)", "kappa"]
STEPS = np.arange(-4, 5) / 2.0
EXP = np.array(np.meshgrid(*([STEPS] * 5), indexing="ij")).reshape(5, -1).T     # (59049, 5)
NK, NP_, NE = EXP.shape[0], len(PREF), len(EPOCHS)
CPLX = (2 * np.abs(EXP).sum(1))[:, None] + (np.arange(NP_) != 0)[None, :]        # (NK, NP)
CPLX = np.broadcast_to(CPLX[None], (NE, NK, NP_)).ravel().astype(int)


def hs_zstar(wb, wm):
    g1 = 0.0783 * wb ** -0.238 / (1 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * wb ** 1.81)
    return 1048 * (1 + 0.00124 * wb ** -0.738) * (1 + g1 * wm ** g2)


def groups(footing, wb=WB, wc=WC, h=H_P, wg=WG, OL=None, a0=None, kappa=KAPPA, shuffle=False):
    """log10 of the 5 basis groups at each epoch -> (NE, 5); also the epoch slopes d ln g/d ln a."""
    wr = wg * (1 + 0.2271 * NEFF)
    Om, Or = (wb + wc + WNU) / h ** 2, wr / h ** 2
    Om_P, Or_P = (WB + WC + WNU) / H_P ** 2, wr / H_P ** 2
    if OL is None:                                   # flatness-anchored on Planck's Omega_Lambda
        OL = OL_P + (Om_P + Or_P) - (Om + Or)
    if a0 is None:                                   # footing rebuilt from its own definition
        a0 = A0[footing] * (h / H_P) * (math.sqrt(OL / OL_P) if footing == "canonical" else 1.0)
    H0 = h * 1e5 / MPC
    zstar = ZSTAR_P * hs_zstar(wb, wb + wc + WNU) / hs_zstar(WB, WB + WC + WNU)
    zeq = (wb + wc) / wr - 1.0
    zs = [0.0, zstar, zeq, Z_BBN]
    Ob = wb / h ** 2

    def lg(a):
        E2 = Or * a ** -4 + Om * a ** -3 + OL
        k = 3 / (8 * math.pi)
        return np.log10([k * Ob * a ** -3 / E2, k * Or * a ** -4 / E2, k * OL / E2,
                         a0 / (C_LIGHT * H0 * math.sqrt(E2)), kappa])
    out, slope = [], []
    for z in zs:
        a = 1 / (1 + z)
        out.append(lg(a))
        slope.append((lg(a * 1.001) - lg(a / 1.001)) / (2 * math.log10(1.001)) * 1.0)   # d log g / d log a
    return np.array(out), np.array(slope), dict(zstar=zstar, zeq=zeq, zBBN=Z_BBN, OL=OL, a0=a0)


def logF_all(lg):
    """(NE*NK*NP,) log10 F for every grammar member."""
    base = lg @ EXP.T                                 # (NE, NK)
    return (base[:, :, None] + PREF[None, None, :]).ravel()


def neff_table(logF, cplx, mask=None):
    """distinct values (log10 rounded to 1e-10) with complexity <= C, for C = 0..max."""
    v, c = (logF, cplx) if mask is None else (logF[mask], cplx[mask])
    key = np.round(v * 1e10).astype(np.int64)
    order = np.lexsort((c, key))
    ks, cs = key[order], c[order]
    first = np.ones(len(ks), bool); first[1:] = ks[1:] != ks[:-1]
    minc = cs[first]
    cmax = int(cplx.max())
    tab = np.array([(minc <= C).sum() for C in range(cmax + 1)], float)
    uniq_vals = ks[first] / 1e10
    return tab, uniq_vals, minc


def best_L(logF, Lmod, T, sT):
    z = (10.0 ** logF - T) / sT
    L = Lmod + z * z / (2 * LN2)
    i = int(np.argmin(L))
    return float(L[i]), i, float(z[i])


def decoy_best_random(uniq_vals, minc, tab, targets, rel):
    """best MDL over the grammar for many targets, via per-complexity sorted nearest values."""
    best = np.full(len(targets), np.inf)
    for C in range(len(tab)):
        vals = np.sort(10.0 ** uniq_vals[minc == C])
        if len(vals) == 0:
            continue
        j = np.searchsorted(vals, targets)
        cand = np.full(len(targets), np.inf)
        for jj in (j - 1, j):
            ok = (jj >= 0) & (jj < len(vals))
            d = np.full(len(targets), np.inf)
            d[ok] = np.abs(vals[jj[ok]] - targets[ok])
            cand = np.minimum(cand, d)
        z = cand / (rel * targets)
        best = np.minimum(best, math.log2(tab[C]) + z * z / (2 * LN2))
    return best


def round_sig(x, n):
    e = np.floor(np.log10(np.abs(x)))
    return np.round(x / 10 ** (e - n + 1)) * 10 ** (e - n + 1)


def member_desc(idx):
    e, rem = divmod(idx, NK * NP_)
    k, p = divmod(rem, NP_)
    terms = [f"({GNAMES[i]})^{EXP[k, i]:g}" for i in range(5) if EXP[k, i] != 0]
    return f"{PREF_NAMES[p]} * " + (" * ".join(terms) if terms else "1") + f"  @ {EPOCHS[e]}", e, k, p


# ================================================================================================ build
t0 = time.time()
P(__doc__.strip())
P(f"\nTARGET  R = omega_c/omega_b = {R:.4f} +- {SR:.4f} (rel {REL*100:.3f}%)   footings never pooled; kappa = {KAPPA} FITTED")
P(f"epochs: z* = {ZSTAR_P}, z_eq = {(WB+WC)/(WG*(1+0.2271*NEFF))-1:.1f}, z_BBN = {Z_BBN:.4e};  grammar members per footing = {NE*NK*NP_:,}")

# BBN omega_b (gate d1)
import camb.bbn as cbbn
from scipy.optimize import brentq
DH_OBS, SDH_OBS = 2.527e-5, 0.030e-5
BBN = {}
for name, tab in [("PRIMAT 2024", cbbn.BBN_table_interpolator("PRIMAT_Yp_DH_ErrorMC_2024.dat", function_of=("Ombh2", "DeltaN"))),
                  ("PArthENoPE 2017", cbbn.BBN_table_interpolator("PArthENoPE_880.2_standard.dat"))]:
    wbb = brentq(lambda w: float(tab.DH(w, 0.0)) - DH_OBS, 0.015, 0.03)
    dlnD = (math.log(float(tab.DH(wbb * 1.001, 0.0))) - math.log(float(tab.DH(wbb / 1.001, 0.0)))) / (2 * math.log(1.001))
    sth = float(tab.get("sig(D/H)", wbb, 0.0)) if name.startswith("PRIMAT") else 0.0
    srel = math.hypot(SDH_OBS / DH_OBS, sth / DH_OBS) / abs(dlnD)
    BBN[name] = dict(omega_b=wbb, sigma=wbb * srel, dlnDH_dlnwb=dlnD, theory_sigDH=sth)
WBB, SWBB = BBN["PRIMAT 2024"]["omega_b"], BBN["PRIMAT 2024"]["sigma"]
R_BBN = WC / WBB
SR_BBN = R_BBN * math.hypot(SWC / WC, SWBB / WBB)
P(f"BBN omega_b (Cooke+18 D/H): PRIMAT {WBB:.5f} +- {SWBB:.5f} -> R_BBN = {R_BBN:.4f} +- {SR_BBN:.4f};  "
  f"PArthENoPE bracket {BBN['PArthENoPE 2017']['omega_b']:.5f} -> {WC/BBN['PArthENoPE 2017']['omega_b']:.4f}")

# grammar positive-control: the original law is expressible
lg_c, _, _ = groups("canonical")
law_idx = np.where((EXP == np.array([0, 0, .5, 0, 1])).all(1))[0][0]
law_val = 10 ** (lg_c[0] @ EXP[law_idx])
law_true = A0["canonical"] / (C_LIGHT * H_P * 1e5 / MPC)
P(f"grammar control: kappa*g3^(1/2) today = {law_val:.6f}  vs a0_canonical/(cH0) = {law_true:.6f}  "
  f"({'EXPRESSIBLE' if abs(law_val/law_true-1) < 1e-3 else 'NOT EXPRESSIBLE'})")

TARGET, STARGET, MUT = R, SR, None
if MUTATE:
    lgm, _, _ = groups("canonical")
    mi = int(np.where((EXP == np.array([.5, -.5, 0, 0, 1])).all(1))[0][0])
    planted = 10 ** (lgm[1] @ EXP[mi] + PREF[5])
    TARGET, STARGET = planted, planted * 1e-5
    MUT = dict(planted=f"4pi * g1^0.5 g2^-0.5 kappa @ recombination", value=planted, rel=1e-5)
    P(f"\n*** MUTATE: target replaced by planted member {MUT['planted']} = {planted:.6f} at 0.001% precision ***")
REL_T = STARGET / TARGET

results = dict(target=dict(R=R, sigma=SR, rel=REL, R_BBN=R_BBN, sigma_BBN=SR_BBN, BBN=BBN, mutate=MUT,
                           used=TARGET, used_sigma=STARGET),
               grammar=dict(members_per_footing=NE * NK * NP_, exponents=STEPS.tolist(), prefactors=PREF_NAMES,
                            epochs=EPOCHS, law_expressible=bool(abs(law_val / law_true - 1) < 1e-3)),
               footings={})

N_RAND, N_SHUF = 4000, 2000
dec_T = round_sig(10 ** RNG.uniform(0, 1, N_RAND), 4)

for footing in ["canonical", "alt"]:
    other = "alt" if footing == "canonical" else "canonical"
    P(f"\n{'='*100}\nFOOTING {footing}  (a0 = {A0[footing]:.4e})")
    lg, sl, info = groups(footing)
    logF = logF_all(lg)
    tab, uv, minc = neff_table(logF, CPLX)
    Lmod = np.log2(tab[CPLX])
    in_rng = int(((uv >= 0) & (uv <= 1)).sum())
    P(f"N_eff (distinct values) = {int(tab[-1]):,}  of {len(logF):,} members;  distinct in [1,10] = {in_rng:,}")

    # elasticities (gate c) and epoch slopes, linear in exponents
    def dlg(**kw):
        return groups(footing, **kw)[0]
    eps_g = (dlg(wc=WC * 1.01) - dlg(wc=WC / 1.01)) / (2 * math.log10(1.01))     # d log g / d log wc  (NE,5)
    epsF = ((eps_g @ EXP.T)[:, :, None] + np.zeros(NP_)[None, None, :]).ravel()
    slopeF = ((sl @ EXP.T)[:, :, None] + np.zeros(NP_)[None, None, :]).ravel()
    ep_idx = np.repeat(np.arange(NE), NK * NP_)
    epoch_ok = (ep_idx != 0) | (np.abs(slopeF) <= 0.01)
    clean = (np.abs(epsF) <= 0.05) & epoch_ok
    tabc, uvc, mincc = neff_table(logF, CPLX, clean)
    Lmodc = np.full(len(logF), np.inf)
    # clean code table indexed by complexity
    Lmodc[clean] = np.log2(tabc[CPLX[clean]])
    in_rng_c = int(((uvc >= 0) & (uvc <= 1)).sum())
    P(f"clean subspace (|eps_c| <= 0.05 and epoch rule): {int(clean.sum()):,} members, N_eff = {int(tabc[-1]):,}, in [1,10] = {in_rng_c:,}")
    P(f"group elasticities d ln g/d ln omega_c by epoch (g1..g5):")
    for e in range(NE):
        P(f"   {EPOCHS[e]:14s} " + "  ".join(f"{x:+.3f}" for x in eps_g[e]))

    # real search
    Lb, ib, zb = best_L(logF, Lmod, TARGET, STARGET)
    Lbc, ibc, zbc = best_L(logF, Lmodc, TARGET, STARGET)
    n1s = int((np.abs(10 ** uv - TARGET) <= STARGET).sum())
    n1s_c = int((np.abs(10 ** uvc - TARGET) <= STARGET).sum())
    P(f"distinct values within 1 sigma of target: full {n1s:,}, clean {n1s_c:,}")
    P(f"best MDL full : L = {Lb:.2f} bits  z = {zb:+.3f}  {member_desc(ib)[0]}")
    P(f"best MDL clean: L = {Lbc:.2f} bits  z = {zbc:+.3f}  {member_desc(ibc)[0]}")

    # gate (a): random decoy targets
    dbest = decoy_best_random(uv, minc, tab, dec_T, REL_T)
    dbest_c = decoy_best_random(uvc, mincc, tabc, dec_T, REL_T)
    p_rand = (1 + int((dbest <= Lb).sum())) / (N_RAND + 1)
    p_rand_c = (1 + int((dbest_c <= Lbc).sum())) / (N_RAND + 1)
    # gate (a): shuffled inputs on the real target
    sh, shc = np.empty(N_SHUF), np.empty(N_SHUF)
    Lmod_f = Lmod.copy()
    for s in range(N_SHUF):
        f = 10 ** RNG.uniform(-1, 1, 4)
        lgs, _, _ = groups(footing, wb=WB * f[0], wg=WG * f[1], OL=OL_P * f[2], a0=A0[footing] * f[3],
                           kappa=KAPPA * 10 ** RNG.uniform(-.5, .5))
        lF = logF_all(lgs)
        z = (10.0 ** lF - TARGET) / STARGET
        q = z * z / (2 * LN2)
        sh[s] = np.min(Lmod_f + q)
        shc[s] = np.min(Lmodc + q)
    p_shuf = (1 + int((sh <= Lb).sum())) / (N_SHUF + 1)
    p_shuf_c = (1 + int((shc <= Lbc).sum())) / (N_SHUF + 1)
    pa = p_rand < 5e-4 and p_shuf < 5e-4
    pac = p_rand_c < 5e-4 and p_shuf_c < 5e-4
    P(f"GATE (a) full : p_rand = {p_rand:.4f}  p_shuf = {p_shuf:.4f}  -> {'PASS' if pa else 'FAIL'}")
    P(f"GATE (a) clean: p_rand = {p_rand_c:.4f}  p_shuf = {p_shuf_c:.4f}  -> {'PASS' if pac else 'FAIL'}")
    P(f"decoy best-L distribution (random targets, full): median {np.median(dbest):.2f}, 1% {np.percentile(dbest,1):.2f}, "
      f"0.1% {np.percentile(dbest,0.1):.2f}, real {Lb:.2f};  clean: median {np.median(dbest_c):.2f}, real {Lbc:.2f}")
    P(f"decoy best-L distribution (shuffled inputs, full): median {np.median(sh):.2f}, 1% {np.percentile(sh,1):.2f}; clean median {np.median(shc):.2f}")

    # per-candidate gates (b), (c), epoch, (d)
    lg_o, _, _ = groups(other)
    lg_d1, _, _ = groups(footing, wb=WBB)
    lg_d2, _, _ = groups(footing, h=H_SHOES)

    def gate_row(idx):
        desc, e, k, p = member_desc(idx)
        n = EXP[k]
        val = 10 ** logF[idx]
        z = (val - TARGET) / STARGET
        v_o = 10 ** (lg_o[e] @ n + PREF[p])
        v_d1 = 10 ** (lg_d1[e] @ n + PREF[p])
        v_d2 = 10 ** (lg_d2[e] @ n + PREF[p])
        z_o = (v_o - TARGET) / STARGET
        z_d1 = (v_d1 - R_BBN) / SR_BBN
        z_d2 = (v_d2 - R) / SR
        h2 = H_P ** 2
        om_pred = (WB * (1 + val) + WNU) / h2
        s_om = om_pred * 2 * SH_P / H_P
        z_b2 = (om_pred - OM_DESI) / math.hypot(SOM_DESI, s_om)
        has_a0 = n[3] != 0
        g = dict(member=desc, value=val, z=z, complexity=int(CPLX[idx]), L_bits=float(Lmod[idx] + z * z / (2 * LN2)),
                 eps_c=float(epsF[idx]), epoch_slope=float(slopeF[idx]),
                 c_pass=bool(abs(epsF[idx]) <= 0.05), epoch_pass=bool(epoch_ok[idx]),
                 b1=("n/a" if not has_a0 else bool(abs(z_o) <= 1)), z_other_footing=(float(z_o) if has_a0 else None),
                 b3="UNAVAILABLE (no mechanism)", b_pass=False,
                 b2_info=dict(Om_pred=om_pred, z=z_b2, within_2sigma=bool(abs(z_b2) <= 2)),
                 d1_pass=bool(abs(z_d1) <= 1), z_d1=float(z_d1), d2_pass=bool(abs(z_d2) <= 1), z_d2=float(z_d2))
        g["all_but_a_b"] = g["c_pass"] and g["epoch_pass"] and g["d1_pass"] and g["d2_pass"]
        return g

    # top candidates: best L per distinct value
    Lall = Lmod + ((10.0 ** logF - TARGET) / STARGET) ** 2 / (2 * LN2)
    order = np.argsort(Lall)
    seen, top = set(), []
    for i in order:
        key = round(float(logF[i]), 9)
        if key in seen:
            continue
        seen.add(key); top.append(int(i))
        if len(top) >= 15:
            break
    Lallc = np.where(clean, Lmodc + ((10.0 ** logF - TARGET) / STARGET) ** 2 / (2 * LN2), np.inf)
    orderc = np.argsort(Lallc)
    seen, topc = set(), []
    for i in orderc:
        key = round(float(logF[i]), 9)
        if key in seen:
            continue
        seen.add(key); topc.append(int(i))
        if len(topc) >= 10:
            break
    rows = [gate_row(i) for i in top]
    rowsc = [gate_row(i) for i in topc]
    # survivors of c + epoch + d among all 1-sigma members
    hits = np.where(np.abs(10 ** logF - TARGET) <= STARGET)[0]
    surv = []
    for i in hits:
        if not clean[i]:
            continue
        g = gate_row(int(i))
        if g["all_but_a_b"]:
            surv.append(g)
    surv_vals = sorted({round(g["value"], 9) for g in surv})
    P(f"\nTop 15 (full search, by MDL):")
    P(f"  {'L':>6} {'z':>7} {'C':>3} {'eps_c':>7} {'slope':>7}  c  E  d1 d2 b1   member")
    for g in rows:
        P(f"  {g['L_bits']:6.2f} {g['z']:+7.3f} {g['complexity']:3d} {g['eps_c']:+7.3f} {g['epoch_slope']:+7.2f}  "
          f"{'Y' if g['c_pass'] else 'n'}  {'Y' if g['epoch_pass'] else 'n'}  {'Y' if g['d1_pass'] else 'n'}  "
          f"{'Y' if g['d2_pass'] else 'n'}  {str(g['b1'])[:3]:3s}  {g['member']}")
    P(f"Top 10 (clean subspace):")
    for g in rowsc:
        P(f"  {g['L_bits']:6.2f} {g['z']:+7.3f} {g['complexity']:3d} {g['eps_c']:+7.3f} {g['epoch_slope']:+7.2f}  "
          f"{'Y' if g['c_pass'] else 'n'}  {'Y' if g['epoch_pass'] else 'n'}  {'Y' if g['d1_pass'] else 'n'}  "
          f"{'Y' if g['d2_pass'] else 'n'}  {str(g['b1'])[:3]:3s}  {g['member']}")
    P(f"1-sigma members passing (c)+epoch+(d1)+(d2): {len(surv)} members, {len(surv_vals)} distinct values; "
      f"(b) passes for none (b3 unavailable).")
    for g in sorted(surv, key=lambda g: g["L_bits"])[:8]:
        P(f"    L {g['L_bits']:.2f} z {g['z']:+.3f}  {g['member']}  (b1 {g['b1']}, z_other {g['z_other_footing']})")

    results["footings"][footing] = dict(
        a0=A0[footing], N_eff=int(tab[-1]), N_eff_in_1_10=in_rng, N_eff_clean=int(tabc[-1]), N_eff_clean_in_1_10=in_rng_c,
        clean_members=int(clean.sum()), n_1sigma_distinct=n1s, n_1sigma_distinct_clean=n1s_c,
        best=dict(L=Lb, z=zb, member=member_desc(ib)[0]), best_clean=dict(L=Lbc, z=zbc, member=member_desc(ibc)[0]),
        gate_a=dict(p_rand=p_rand, p_shuf=p_shuf, pass_=pa, p_rand_clean=p_rand_c, p_shuf_clean=p_shuf_c, pass_clean=pac,
                    decoy_rand_quantiles={q: float(np.percentile(dbest, q)) for q in (0.1, 1, 5, 50, 95)},
                    decoy_rand_clean_quantiles={q: float(np.percentile(dbest_c, q)) for q in (0.1, 1, 5, 50, 95)},
                    decoy_shuf_quantiles={q: float(np.percentile(sh, q)) for q in (0.1, 1, 5, 50, 95)},
                    decoy_shuf_clean_quantiles={q: float(np.percentile(shc, q)) for q in (0.1, 1, 5, 50, 95)}),
        group_eps_c=eps_g.tolist(), top_full=rows, top_clean=rowsc,
        survivors_c_epoch_d=dict(n_members=len(surv), n_distinct=len(surv_vals),
                                 best=sorted(surv, key=lambda g: g["L_bits"])[:20]))

    if footing == "canonical" and not MUTATE:
        # injected positive controls: power of gate (a) vs precision
        P(f"\nINJECTED POSITIVE CONTROLS (200 clean members, C <= 6, value in [1,10]; full canonical search):")
        pool = np.where(clean & (CPLX <= 6) & (logF >= 0) & (logF <= 1))[0]
        pick = RNG.choice(pool, size=min(200, len(pool)), replace=False)
        power = {}
        for rel in (REL, 1e-3, 1e-5, 1e-7):
            nsig = 4 if rel > 1e-3 else (6 if rel > 1e-6 else 9)
            dT = round_sig(10 ** RNG.uniform(0, 1, N_RAND), nsig)
            db = np.sort(decoy_best_random(uv, minc, tab, dT, rel))
            npass = 0
            for i in pick:
                Tt = 10 ** logF[i] * (1 + rel * RNG.standard_normal())
                Lr, _, _ = best_L(logF, Lmod, Tt, rel * Tt)
                pr = (1 + np.searchsorted(db, Lr, side="right")) / (N_RAND + 1)
                npass += pr < 5e-4
            power[f"{rel:.3g}"] = npass / len(pick)
            P(f"   precision {rel:.3g}: gate (a, random-decoy half) certifies {npass}/{len(pick)} planted true formulas")
        results["positive_controls"] = dict(n=int(len(pick)), pool=int(len(pool)), power_vs_precision=power)

# TRUE-VALUE control
om_true = (WB * (1 + R) + WNU) / H_P ** 2
results["true_value_control"] = dict(
    b2_Om_pred=om_true, b2_z=(om_true - OM_DESI) / math.hypot(SOM_DESI, om_true * 2 * SH_P / H_P),
    d1_z=(R - R_BBN) / SR_BBN, d2_z=0.0)
P(f"\nTRUE-VALUE control (F = R): b2 Om_pred {om_true:.4f} (z {results['true_value_control']['b2_z']:+.2f} vs DESI), "
  f"d1 z {results['true_value_control']['d1_z']:+.2f}, d2 z 0 (h-free)")

# naive-space illustration
if not MUTATE:
    atoms = {**{str(i): float(i) for i in range(1, 11)}, "pi": math.pi, "e": math.e, "phi": (1 + 5 ** .5) / 2,
             "sqrt2": 2 ** .5, "sqrt3": 3 ** .5, "ln2": math.log(2)}
    forms = []
    for k, v in atoms.items():
        forms += [(k, v), (f"sqrt({k})", v ** .5), (f"{k}^2", v * v), (f"1/{k}", 1 / v)]
    fv = np.array([v for _, v in forms])
    A, B = np.meshgrid(fv, fv, indexing="ij")
    naive = np.concatenate([(A + B).ravel(), (A - B).ravel(), (A * B).ravel(), (A / B).ravel()])
    nhit = int((np.abs(naive - R) <= SR).sum())
    z_e7 = (math.e + 7 ** .5 - R) / SR
    nv = np.sort(naive)
    j = np.searchsorted(nv, dec_T)
    dmin = np.minimum(np.abs(nv[np.clip(j - 1, 0, len(nv) - 1)] - dec_T), np.abs(nv[np.clip(j, 0, len(nv) - 1)] - dec_T)) / (REL * dec_T)
    zbest = float(np.min(np.abs(naive - R)) / SR)
    p_best = (1 + int((dmin <= zbest).sum())) / (N_RAND + 1)
    p_e7 = (1 + int((dmin <= abs(z_e7)).sum())) / (N_RAND + 1)
    frac1 = float((dmin <= 1).mean())
    P(f"\nNAIVE SPACE illustration ({len(naive):,} expressions; e, phi, sqrt7 allowed): {nhit} within 1 sigma; "
      f"best |z| = {zbest:.4f}; e + sqrt7 = {math.e + 7**.5:.5f}, z = {z_e7:+.4f}")
    P(f"   decoy p (fraction of 4000 random targets with a match at least as close): best {p_best:.3f}, e+sqrt7 {p_e7:.3f}; "
      f"{frac1*100:.1f}% of decoys have a 1-sigma match")
    results["naive_illustration"] = dict(n_expr=int(len(naive)), n_1sigma=nhit, best_abs_z=zbest, e_plus_sqrt7=math.e + 7 ** .5,
                                         z_e_plus_sqrt7=z_e7, p_best=p_best, p_e_plus_sqrt7=p_e7, frac_decoys_with_1sigma_hit=frac1)

# verdict
fa = [results["footings"][f]["gate_a"] for f in ("canonical", "alt")]
any_a = any(g["pass_"] for g in fa)
if MUTATE:
    verdict = "MUTATE: planted member " + ("CERTIFIED by gate (a)" if any_a else "NOT certified by gate (a)")
elif not any_a:
    verdict = "CHANCE-LEVEL"
else:
    verdict = "gate (a) passed somewhere -- see per-candidate gates; (b) unavailable => SURVIVOR WITHOUT INTERLOCK at most"
results["verdict"] = verdict
results["runtime_s"] = time.time() - t0
P(f"\nVERDICT: {verdict}   (runtime {results['runtime_s']:.0f} s; kappa FITTED; not a derivation; not theory closed)")
json.dump(results, open(os.path.join(HERE, f"cfg642{TAG}_results.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
