#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG168 attacks (a), (b), (c) and the scale scan (d1), as frozen in CFG168_FROZEN_CRITERIA.md section 6.
    ZF_REPO=<repo> python3 cfg168_attacks.py > CFG168_attacks.out ; rc 0 always (labelled sensitivity grids).
Interpretation of the ambiguous frozen phrase 'anchor uncorrected': the SPARC anchor's own pressure correction switched off (sp_anchor = P0);
the anchor OFFSET removed altogether is the M3 control."""
import sys
import json
import math
sys.dont_write_bytecode = True
from cfg168_common import *      # noqa

S0 = load_S("inc_star_deg")
A0_ = load_A()
OUT = {}
NAMES = ["K21", "D&S 2010", "P3 (fixed height)", "Price 2022 (n=1)", "P2 (self-grav.)"]


def spec_k21b(s, refac=1.0, refac_a=None):
    return M.spec("P4", scale=float(s), Refac=refac, Refac_anchor=(refac if refac_a is None else refac_a))


def kcell(S, A, s, mu=0.67, refac=1.0, refac_a=None, sp_anchor_p0=False, **kw):
    sp = spec_k21b(s, refac, refac_a)
    return cellx(S, A, sp, mu, sp_anchor=(M.spec("P0") if sp_anchor_p0 else None), **kw)


def cross(S, A, mu=0.67, refac=1.0, refac_a=None, sp_anchor_p0=False, **kw):
    c = lambda s: kcell(S, A, s, mu, refac, refac_a, sp_anchor_p0, **kw)
    smid = root(lambda s: (lambda r: r["flat"]["dprime"] + r["H"]["dprime"])(c(s)), 0.0, 4.0)
    sf2 = root(lambda s: (lambda r: r["flat"]["dprime"] - 2 * r["flat"]["sigma"])(c(s)), 0.0, 4.0)
    sh2 = root(lambda s: (lambda r: r["H"]["dprime"] + 2 * r["H"]["sigma"])(c(s)), 0.0, 4.0)
    q = None if smid is None else c(smid)["f_press"]
    return dict(s_mid=smid, s_f2=sf2, s_h2=sh2, q_mid=q)


def place_all(S, A, mu=0.67, refac=1.0, refac_a=None, which="flat", sp_anchor_p0=False, **kw):
    """s_eq of the five prescriptions in the variant's own K21 units (matching Delta'_flat or Delta'_H at gas mu)"""
    res = {}
    for nm in NAMES:
        if nm == "K21":
            res[nm] = 1.0
            continue
        sp = PRESC[nm]
        c = cellx(S, A, sp, mu, sp_anchor=(M.spec("P0") if sp_anchor_p0 else None), **kw)
        tgt = c[which]["dprime"]
        res[nm] = root(lambda s: kcell(S, A, s, mu, refac, refac_a, sp_anchor_p0, **kw)[which]["dprime"] - tgt, 0.0, 6.0)
    return res


def f_press_presc(S, A, nm, mu=0.67):
    c = cellx(S, A, PRESC[nm] if nm != "K21" else spec_k21b(1.0), mu)
    return c["f_press"]


BASE_SIDE = None
P("CFG168 attacks; repo = <repo>")

# ============================================================================= (a)
P("\n=== (a) placement variants (each recomputes the six s_eq and the crossings in the variant's own units) ===")
base_c = cross(S0, A0_)
base_p = place_all(S0, A0_)
P("base: s_mid %.4f s_f2 %.4f s_h2 %.4f q_mid %.4f;  s_eq " % (base_c["s_mid"], base_c["s_f2"], base_c["s_h2"], base_c["q_mid"]) + ", ".join(f"{k} {v:.3f}" for k, v in base_p.items()))
VA = {"base": dict(cross=base_c, place=base_p)}


def report(name, cr, pl, unit_note=""):
    smid = cr["s_mid"]
    parts = []
    ok_side = True
    ok_move = True
    for nm in NAMES[1:]:
        s = pl[nm]
        side = None if s is None or smid is None else s > smid
        mv = None if s is None else abs(s - base_p[nm])
        lim = max(0.15, 0.15 * base_p[nm])
        parts.append(f"{nm} {fmt(s,3)} ({'above' if side else 'BELOW'}; move {fmt(mv,3)})")
        ok_side &= bool(side)
        ok_move &= (mv is not None and mv <= lim)
    P(f"  {name:38s} s_mid {fmt(smid,3)} K21@1 {'above' if (smid is not None and 1.0 > smid) else 'BELOW/at'} s_mid | " + " | ".join(parts) + f"  -> side {'ok' if ok_side else 'FLIP'}, move {'<=line' if ok_move else 'OVER LINE'} {unit_note}")
    return dict(cross=cr, place=pl, ok_side=bool(ok_side), ok_move=bool(ok_move))


# A1
pl = place_all(S0, A0_, which="H")
VA["A1 match Delta'_H"] = report("A1 match Delta'_H", base_c, pl)
# A2 physical axis: mean pressure fraction
f1 = f_press_presc(S0, A0_, "K21")
fp = {nm: f_press_presc(S0, A0_, nm) for nm in NAMES}
P(f"  A2 mean pressure fraction <Vc2/V2 - 1> per prescription (unweighted mean over the ten): " + ", ".join(f"{k} {v:.3f}" for k, v in fp.items()) + f"; q_mid (K21 at s_mid) = {base_c['q_mid']:.3f}")
pl = {nm: fp[nm] / f1 for nm in NAMES}
qratio = {nm: fp[nm] / base_c["q_mid"] for nm in NAMES}
VA["A2 mean pressure fraction axis"] = report("A2 f_press ratio (K21 units)", base_c, pl)
VA["A2 mean pressure fraction axis"]["f_press"] = fp
VA["A2 mean pressure fraction axis"]["ratio_to_q_mid"] = qratio
# A3 median / geometric mean of alpha ratio
med, geo = {}, {}
for nm in NAMES:
    sp = PRESC[nm] if nm != "K21" else spec_k21b(1.0)
    C, _ = M.corr(S0, sp)
    C1, _ = M.corr(S0, spec_k21b(1.0))
    r = C / C1
    med[nm] = float(np.median(r)); geo[nm] = float(np.exp(np.mean(np.log(r))))
VA["A3 median alpha ratio"] = report("A3 median alpha_presc/alpha_K21", base_c, med)
VA["A3 geometric-mean alpha ratio"] = report("A3 geometric-mean ratio", base_c, geo)
# A4 gas dependence of the placement + direct check
P("  A4 placement s_eq(mu) and the direct check |Delta'_flat(prescription, mu) - Delta'_flat(s_eq(0.67) K21, mu)|:")
A4 = {}
for mu in (0.25, 0.67, 1.5, 4.0):
    pl_mu = place_all(S0, A0_, mu=mu)
    cr_mu = cross(S0, A0_, mu=mu)
    dd = {}
    for nm in NAMES[1:]:
        dp = cellx(S0, A0_, PRESC[nm], mu)["flat"]["dprime"]
        dk = kcell(S0, A0_, base_p[nm], mu)["flat"]["dprime"]
        c_dir = cellx(S0, A0_, PRESC[nm], mu); c_k = kcell(S0, A0_, base_p[nm], mu)
        dd[nm] = dict(diff=dp - dk, cls_direct=M.classify(c_dir["flat"]["z"], c_dir["H"]["z"]), cls_placed=M.classify(c_k["flat"]["z"], c_k["H"]["z"]),
                      side_direct=None)
    A4[mu] = dict(s_eq=pl_mu, s_mid=cr_mu["s_mid"], direct=dd)
    P(f"   mu={mu}: s_mid {fmt(cr_mu['s_mid'],3)}; s_eq " + ", ".join(f"{k} {fmt(v,3)}" for k, v in pl_mu.items()) + " | direct-placed diff " + ", ".join(f"{k} {v['diff']:+.4f}" for k, v in dd.items()))
    P("        classes direct vs placed: " + "; ".join(f"{k}: {v['cls_direct']} / {v['cls_placed']}" for k, v in dd.items() if v['cls_direct'] != v['cls_placed']) + ("(none differ)" if all(v['cls_direct'] == v['cls_placed'] for v in dd.values()) else ""))
maxdiff = max(abs(v["diff"]) for m in A4.values() for v in m["direct"].values())
P(f"   max |direct - placed| over prescriptions and mu: {maxdiff:.4f} (frozen line 0.02) -> {'PASS' if maxdiff <= 0.02 else 'FAIL'}")
# does the direct (prescription itself) side vs s_mid(mu) match the placed one? use direct Delta'_flat vs Delta'_flat(s_mid(mu))
for mu in (0.67, 1.5, 4.0):
    smid = A4[mu]["s_mid"]
    dmid = kcell(S0, A0_, smid, mu)["flat"]["dprime"]
    sides = {nm: (cellx(S0, A0_, PRESC[nm], mu)["flat"]["dprime"] > dmid) for nm in NAMES[1:]}
    sides["K21"] = kcell(S0, A0_, 1.0, mu)["flat"]["dprime"] > dmid
    A4[mu]["side_direct_above_smid"] = sides
    P(f"   mu={mu}: prescriptions ABOVE s_mid by their own direct Delta'_flat: " + ", ".join(f"{k} {v}" for k, v in sides.items()))
VA["A4"] = dict(per_mu={str(k): v for k, v in A4.items()}, max_direct_diff=maxdiff)
# A5 R_e variants
for rf in (1.5, 2.0):
    cr_ = cross(S0, A0_, refac=rf)
    pl_ = place_all(S0, A0_, refac=rf)
    VA[f"A5 R_e = {rf} R_eff (both)"] = report(f"A5 R_e = {rf} R_eff (KURVS+anchor)", cr_, pl_, f"[q_mid {cr_['q_mid']:.3f}; K21 s=1 vs s_mid {cr_['s_mid']:.3f}]")
# A6 anchor pressure correction off
cr_ = cross(S0, A0_, sp_anchor_p0=True); pl_ = place_all(S0, A0_, sp_anchor_p0=True)
VA["A6 anchor pressure correction off"] = report("A6 anchor pressure correction off", cr_, pl_)
# A7 sigma_0 instead of sigma_out
S7 = clone(S0, sig=S0.sig0.copy(), esig=S0.esig0.copy(), grad2=np.zeros_like(S0.grad2))
cr_ = cross(S7, A0_); pl_ = place_all(S7, A0_)
VA["A7 sigma_0 (grad2 = 0)"] = report("A7 sigma_0, grad2=0", cr_, pl_)
# bootstrap probabilities
res, none, _ = bootstrap(S0, A0_, 2000, 168)
bs = np.array(res["s_mid"])
P("  bootstrap (N=2000, seed 168): P(s_mid < placement) = " + ", ".join(f"{k} {float(np.mean(bs < v)):.3f}" for k, v in base_p.items()) + f"; P(s_mid < 0.6) = {float(np.mean(bs < 0.6)):.3f}; P(s_mid < 1.4) = {float(np.mean(bs < 1.4)):.3f}")
VA["boot_prob"] = {k: float(np.mean(bs < v)) for k, v in base_p.items()}
VA["boot_prob"]["K21 band lo 0.6"] = float(np.mean(bs < 0.6)); VA["boot_prob"]["K21 band hi 1.4"] = float(np.mean(bs < 1.4))
noncore = [k for k in VA if k.startswith("A1") or k.startswith("A2") or k.startswith("A3") or k.startswith("A6") or k.startswith("A7")]
ok_a = all(VA[k]["ok_side"] and VA[k]["ok_move"] for k in noncore) and maxdiff <= 0.02 and all(VA[k]["ok_side"] for k in VA if k.startswith("A5"))
P("\n(a) VERDICT (frozen: A1-A3, A6, A7 keep side and move <= max(0.15, 15%); A4 direct diff <= 0.02; A5 non-K21 stay above s_mid): " + ("PASS" if ok_a else "FAIL"))
for k in noncore + [k for k in VA if k.startswith("A5")]:
    P(f"   {k}: side {'ok' if VA[k]['ok_side'] else 'FLIP'}; move {'ok' if VA[k]['ok_move'] else 'over line'}")
OUT["a"] = dict(VA={k: v for k, v in VA.items()}, verdict=("PASS" if ok_a else "FAIL"))

# ============================================================================= (b)
P("\n=== (b) stability of the crossings to definitions (decision cell) ===")
bc = cross(S0, A0_)
VB = {"base": bc}
def show(name, c):
    dm = None if c["s_mid"] is None else c["s_mid"] - bc["s_mid"]
    df = None if c["s_f2"] is None else c["s_f2"] - bc["s_f2"]
    dh = None if c["s_h2"] is None else c["s_h2"] - bc["s_h2"]
    P(f"  {name:44s} s_mid {fmt(c['s_mid'],3)} ({fmt(dm,3) if dm is not None else '-'}) s_f2 {fmt(c['s_f2'],3)} ({fmt(df,3) if df is not None else '-'}) s_h2 {fmt(c['s_h2'],3)} ({fmt(dh,3) if dh is not None else '-'}) q_mid {fmt(c['q_mid'],3)}")
    VB[name] = dict(c, d_mid=dm, d_f2=df, d_h2=dh)

show("base (inc_star, R_e=R_eff)", bc)
Ssfr = load_S("inc_sfr_deg"); show("inclination column inc_sfr_deg", cross(Ssfr, A0_))
for d in (3.0, 8.0):
    show(f"inclination error {d:.0f} deg", cross(clone(S0, einc=np.full(10, math.radians(d))), A0_))
for me in (0.10, 0.20):
    show(f"KURVS mass error {me:.2f} dex", cross(clone(S0, mass_err=me), A0_))
for gs in (1.0, 3.0):
    show(f"gas disc scale {gs:.0f} R_d", cross(S0, A0_, gas_scale=gs))
for sg in (7.0, 15.0):
    A_ = clone(A0_, sig=np.full(len(A0_.R), sg), sig0=np.full(len(A0_.R), sg), tag=f"sig{sg}")
    show(f"anchor sigma {sg:.0f} km/s", cross(S0, A_))
show("anchor pressure correction off", cross(S0, A0_, sp_anchor_p0=True))
show("anchor offset = median (not pooled)", cross(S0, A0_, anchor_mode="median"))
m45 = np.degrees(A0_.inc) >= 45.0
A45 = subset(A0_, m45, "inc45"); P(f"   (anchor inc>=45: {int(m45.sum())} of {len(m45)})")
show("anchor inclination >= 45 deg", cross(S0, A45))
mM = A0_.logM >= 10.0
AM = subset(A0_, mM, "logM10"); P(f"   (anchor logM>=10: {int(mM.sum())} of {len(mM)})")
show("anchor log M* >= 10", cross(S0, AM))
for rf in (1.5, 2.0):
    show(f"R_e = {rf} R_eff (KURVS and anchor)", cross(S0, A0_, refac=rf))
show("R_e = 2 R_eff KURVS only (anchor 1.68 Rdisk)", cross(S0, A0_, refac=2.0, refac_a=1.0))
jk = jackknife(S0, A0_)
P(f"  jackknife s_mid (leave one disc out, ids {S0.ids}): " + ", ".join(fmt(x, 3) for x in jk) + f";  range {max(jk)-min(jk):.3f}, max shift {max(abs(x-bc['s_mid']) for x in jk):.3f}")
VB["jackknife"] = jk
resA, noneA, _ = bootstrap(S0, A0_, 2000, 168, boot_anchor=True)
pA = {k: pct(v) for k, v in resA.items()}
P(f"  bootstrap with the anchor ALSO resampled (seed 168): s_mid 16/50/84 = {pA['s_mid'][0]:.3f}/{pA['s_mid'][1]:.3f}/{pA['s_mid'][2]:.3f} (fixed anchor: {pct(res['s_mid'])[0]:.3f}/{pct(res['s_mid'])[1]:.3f}/{pct(res['s_mid'])[2]:.3f}); no-root {noneA}")
VB["boot_anchor"] = pA
nonR = [k for k in VB if k not in ("base", "jackknife", "boot_anchor") and "R_e" not in k]
bad = [(k, VB[k]["d_mid"], VB[k]["d_f2"], VB[k]["d_h2"]) for k in nonR if any(v is None or abs(v) > 0.05 for v in (VB[k]["d_mid"], VB[k]["d_f2"], VB[k]["d_h2"]))]
qs = [VB[k]["q_mid"] for k in VB if "R_e" in k] + [bc["q_mid"]]
qspread = (max(qs) - min(qs)) / bc["q_mid"]
jr = max(jk) - min(jk)
P("\n(b) VERDICT: non-R_e variants moving s_mid/s_f2/s_h2 by > 0.05: " + (str([(k, *(fmt(x, 3) for x in v)) for k, *v in bad]) if bad else "none"))
P(f"    jackknife range {jr:.3f} (line 0.085): {'ok' if jr <= 0.085 else 'OVER'};  q_mid spread over R_e variants {100*qspread:.1f}% of base (line 15%): {'ok' if qspread <= 0.15 else 'OVER'}  (q_mid values {[round(q,3) for q in qs]})")
ok_b = (not bad) and jr <= 0.085 and qspread <= 0.15
P("    (b) overall: " + ("PASS" if ok_b else "FAIL"))
OUT["b"] = dict(VB=VB, bad=bad, jack_range=jr, q_spread=qspread, verdict=("PASS" if ok_b else "FAIL"))

# ============================================================================= (c)
P("\n=== (c) the (s, mu) map: regions, break-evens vs s ===")
sg = np.arange(0.0, 4.0001, 0.05)
mg = np.exp(np.linspace(math.log(0.25), math.log(4.0), 60))
ZF = np.zeros((len(sg), len(mg))); ZH = np.zeros_like(ZF); SEP = np.zeros_like(ZF)
for i, s in enumerate(sg):
    for j, m in enumerate(mg):
        c = K21cell(S0, A0_, float(s), float(m))
        ZF[i, j] = c["flat"]["z"]; ZH[i, j] = c["H"]["z"]
        SEP[i, j] = (c["flat"]["dprime"] - c["H"]["dprime"]) / (0.5 * (c["flat"]["sigma"] + c["H"]["sigma"]))
R1 = (np.abs(ZF) <= 1) & (np.abs(ZH) <= 1)
R2 = (np.abs(ZF) <= 2) & (np.abs(ZH) <= 2)
MX = np.maximum(np.abs(ZF), np.abs(ZH))
i0, j0 = np.unravel_index(np.argmin(MX), MX.shape)
P(f"  (c1) R1 (both within 1 sigma) grid-area fraction: {R1.mean():.4f};  min over the map of max(|z_flat|,|z_H|) = {MX.min():.3f} at s={sg[i0]:.2f}, mu={mg[j0]:.2f}")
P(f"       minimum separation (Delta'_flat-Delta'_H)/mean-sigma over the map: {SEP.min():.3f} (R1 needs <= 2 for both within 1 sigma: {'empty by the bound' if SEP.min() > 2 else 'not excluded'});  maximum {SEP.max():.3f}")
P(f"  (c2) R2 (both within 2 sigma) grid-area fraction of the box (uniform in s and ln mu): {R2.mean():.4f}")
for m in (0.25, 0.67, 1.5, 4.0):
    j = int(np.argmin(abs(np.log(mg) - math.log(m))))
    ii = np.where(R2[:, j])[0]
    P(f"       at mu~{mg[j]:.2f}: R2 s-range {'none' if len(ii) == 0 else f'{sg[ii[0]]:.2f}-{sg[ii[-1]]:.2f}'} ({len(ii)} grid points of 0.05)")
cell24 = {}
for s in np.arange(0, 4.0001, 0.25):
    n1 = n2 = 0
    for mu in MUS:
        for dl in DELS:
            for ft in FOOTS:
                c = K21cell(S0, A0_, float(s), mu, dl, ft)
                n1 += int(abs(c["flat"]["z"]) <= 1 and abs(c["H"]["z"]) <= 1)
                n2 += int(abs(c["flat"]["z"]) <= 2 and abs(c["H"]["z"]) <= 2)
    cell24[float(s)] = (n1, n2)
P("  24-cell grid at s = 0..4 step 0.25: (both within 1 sigma, both within 2 sigma) = " + ", ".join(f"{s:g}:{v}" for s, v in cell24.items()))
P("  (c3) break-even gas curves (continuous root on log mu in [0.05, 60]; 'none' = no sign change):")
BE = {}
for s in np.arange(0.0, 4.0001, 0.25):
    bf = breakeven_mu(lambda m: K21cell(S0, A0_, float(s), m)["flat"]["dprime"])
    bh = breakeven_mu(lambda m: K21cell(S0, A0_, float(s), m)["H"]["dprime"])
    BE[float(s)] = (bf, bh)
    P(f"       s={s:4.2f}: mu_f {fmt(bf,2):>6}  mu_h {fmt(bh,2):>6}")
P("  (c4) README claim 'published prescriptions (s = 1.0-1.7): flat fits if mu ~ 2.1-3.7, rival if mu ~ 0.6-1.7', with the DIRECT (prescription itself) break-evens:")
C4 = {}
for nm in NAMES:
    sp = PRESC[nm] if nm != "K21" else spec_k21b(1.0)
    bf = breakeven_mu(lambda m: cellx(S0, A0_, sp, m)["flat"]["dprime"])
    bh = breakeven_mu(lambda m: cellx(S0, A0_, sp, m)["H"]["dprime"])
    via = (breakeven_mu(lambda m: kcell(S0, A0_, base_p[nm], m)["flat"]["dprime"]), breakeven_mu(lambda m: kcell(S0, A0_, base_p[nm], m)["H"]["dprime"]))
    C4[nm] = dict(direct=(bf, bh), via=via)
    P(f"       {nm:20s} direct flat {fmt(bf,2)} rival {fmt(bh,2)};  via s_eq flat {fmt(via[0],2)} rival {fmt(via[1],2)};  |direct-via| {abs(bf-via[0]):.3f} / {abs(bh-via[1]):.3f}")
okc4 = all(abs(C4[k]["direct"][0] - C4[k]["via"][0]) <= 0.3 and abs(C4[k]["direct"][1] - C4[k]["via"][1]) <= 0.3 for k in NAMES)
P(f"  (c4) direct vs placed within 0.3 in mu for all six: {okc4}")
P(f"  (c) scope statements: R1 area {R1.mean():.4f} (empty: {not R1.any()}); R2 area {R2.mean():.3f}")
OUT["c"] = dict(R1_area=float(R1.mean()), R2_area=float(R2.mean()), min_max_z=float(MX.min()), min_at=(float(sg[i0]), float(mg[j0])), sep_min=float(SEP.min()), sep_max=float(SEP.max()),
                cell24={str(k): v for k, v in cell24.items()}, breakeven_vs_s={str(k): v for k, v in BE.items()}, c4=C4, c4_ok=bool(okc4))

# ============================================================================= (d1)
P("\n=== (d1) scale scan of KURVS v_last (V and eV scaled together) ===")
D1 = {}
for fct in (0.85, 0.9, 1.0, 1.1, 1.26, 1.5, 1.995):
    T = clone(S0, V=S0.V * fct, eV=S0.eV * fct)
    c = cross(T, A0_)
    ck = K21cell(T, A0_, 1.0)
    D1[fct] = dict(cross=c, K21=dict(flat=ck["flat"]["dprime"], zf=ck["flat"]["z"], zh=ck["H"]["z"], cls=M.classify(ck["flat"]["z"], ck["H"]["z"])))
    P(f"  V x {fct:5.3f}: s_mid {fmt(c['s_mid'],3)} s_f2 {fmt(c['s_f2'],3)} s_h2 {fmt(c['s_h2'],3)};  K21 (s=1): flat {ck['flat']['z']:+.2f}s H {ck['H']['z']:+.2f}s {D1[fct]['K21']['cls']}")
OUT["d1"] = {str(k): v for k, v in D1.items()}

# ============================================================================= extra (post hoc, labelled): sigma permutation spread (M5 bit in the main MUTATE)
P("\n=== EXTRA (post hoc, not frozen): 200 permutations of sigma_out across the ten discs ===")
rng = np.random.default_rng(1680)
vals = []
for _ in range(200):
    p = rng.permutation(10)
    T = clone(S0, sig=S0.sig[p], esig=S0.esig[p], grad2=S0.grad2[p])
    r = crossings(T, A0_)["s_mid"]
    vals.append(r)
vv = np.array([v for v in vals if v is not None])
P(f"  s_mid under permuted sigma: 16/50/84 = {np.percentile(vv,16):.3f}/{np.percentile(vv,50):.3f}/{np.percentile(vv,84):.3f}; frac within 0.05 of 0.669: {float(np.mean(abs(vv-0.6693)<=0.05)):.2f}; none {len(vals)-len(vv)}")
OUT["extra_perm"] = dict(p16_50_84=[float(np.percentile(vv, q)) for q in (16, 50, 84)], within05=float(np.mean(abs(vv - 0.6693) <= 0.05)))

with open("CFG168_attacks_results.json", "w") as f:
    json.dump(OUT, f, indent=1, default=lambda o: None if o is None else (float(o) if isinstance(o, (np.floating,)) else (bool(o) if isinstance(o, np.bool_) else str(o))))
P("\nsaved CFG168_attacks_results.json")
