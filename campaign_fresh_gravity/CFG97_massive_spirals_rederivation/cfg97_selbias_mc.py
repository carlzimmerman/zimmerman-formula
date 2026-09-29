"""
CFG97 selection-bias Monte-Carlo (independent re-derivation of the CFG41 selection-bias check).
FROZEN before any run.  Written from the CFG41_selbias_mc docstring statements (the only part of the CFG41 code I was allowed to read) and my own code.
QUESTION.  For a sample selected on OBSERVED speed (>300 km/s) and log M_* >= 11.0, how large is the upward bias of mean log(v_flat/v_law) when the law is TRUE,
           and is CFG41's B = 0.076 +- 0.030 dex (centre of the matched rows 0.067..0.085) reproduced?  Is it ~0.02 too large (referee) once M_* errors are in?
MODEL AS READ (docstring items 1-8): law v^4 = G M_b a0 with a0 = 1.2e-10; M_b = M_*+M_gas; parent Schechter in log M_* (u^(alpha+1) e^-u, x in [11,12.4],
  BASE alpha=-1.0 logMc=10.7; FLAT -0.6/10.9; STEEP -1.2/10.5); log M_gas = 10.3 + 0.3 N(0,1); two-measurement model:
  log v_sel = log v_law + e_int + e_w (cut >log 300), log v_flat = log v_law + e_int + e_f (tested); e_int~N(0,s_int), e_w~N(0,s_w), e_f~N(0,s_f).
  Grid s_int in {.02,.04,.06,.08,.10}; s_w in {.03,.05,.08,.12,.16}; s_f in {.02,.08}.  MATCH row: mean v_flat (arithmetic, selected) in [280,300] AND mean log M_* in [11.20,11.30].
  B_mine := (min+max)/2 of the bias over MATCH rows of the BASE mass function (this is how I read '+0.067 to +0.085 -> 0.076').
  Single-measurement model (item 4) for s in {.02..0.10}, delta in {0, +.05}.
  My own MC uses 2e7 parent draws per grid row (not 2e8: runtime; 3e7 for the injection rows) + exact quadrature (12001 x 801) for the bias, survival fraction and E[log M_*].
PASS LINES (declared).
  M0 (control, null)  selection decoupled from the tested variable -> mean bias 0 within 4 MC-SE.
  M1 (control)  MC vs exact quadrature: bias agrees within 4 MC-SE on every BASE grid row with >= 2000 selected.
  M2 (control)  single-measurement, s -> large: mean(e) among selected >0 and rises with s (monotone in s at delta=0).
  M3 (control, INJECTED OFFSET)  for the central MATCH row, inject delta in {-0.05,0,+0.05,+0.10} into e_int's mean; recovered = mean(e_sel) - bias(delta=0);
        |recovered - delta| <= 0.010 for |delta| <= 0.05 (B is additive to 0.01).  Reported for +0.10 (no line).
  M4 (control) the quadrature and MC survival fractions agree within 3%.
  M5 (MUTATE=1) e_int is drawn independently for the cut and the test (selection decoupled): B_mine must come out < 0.005, so the check 'B_mine within
        0.010 of 0.076' FAILS and the script exits 1.
  R1 (reproduction)  B_mine within 0.010 of 0.076 -> reproduced; the MATCH range compared to 0.067..0.085.  R2: whole-grid range compared to 0.003..0.154.
  ATTACKS (reported, no pass line): A1 add M_* measurement error 0.2 dex (selection on measured M_*>1e11, prediction from measured M_*, true M_* Schechter over
        10.2..12.6) -> B (referee: 0.058); A2 a0 = 9.36e-11 and 1.13e-10 in the mock law; A3 FLAT/STEEP mass functions on the MATCH rows.
  The exact bias formula used in quadrature: for selection m + e_c > c, e_c = e_int+e_w (SD s_c), z=(m-c)/s_c:  E[e_int 1{sel}] = w s_int^2/s_c phi(z), P = Phi(z).
Run: python3 cfg97_selbias_mc.py   (MUTATE=1 for the control).  Seed 20260929.
"""
import os, sys, json, time
import numpy as np
from scipy.special import ndtr
MUT = os.environ.get("MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
G = 6.6743e-11; MSUN = 1.98847e30; A0 = 1.2e-10
CUT = np.log10(300.0)
rng = np.random.default_rng(20260929)
NDRAW = int(os.environ.get("NDRAW", 20_000_000)); CH = 5_000_000
MF = {"BASE": (-1.0, 10.7), "FLAT": (-0.6, 10.9), "STEEP": (-1.2, 10.5)}
SI = [0.02, 0.04, 0.06, 0.08, 0.10]; SW = [0.03, 0.05, 0.08, 0.12, 0.16]; SF = [0.02, 0.08]
out = {"mutate": MUT}
checks = []
def chk(name, ok, detail):
    checks.append((name, bool(ok), detail)); print(("PASS " if ok else "FAIL ") + name + " -- " + detail, flush=True)

def logv_law(x, lg, a0=A0):
    mb = 10.0**x + 10.0**lg
    return 0.25 * np.log10(G * mb * MSUN * a0) - 3.0      # log10 v in km/s

def sampler(alpha, logMc, lo, hi):
    xg = np.linspace(lo, hi, 200001)
    u = 10.0**(xg - logMc)
    pdf = u**(alpha + 1.0) * np.exp(-u)
    cdf = np.cumsum(pdf); cdf = (cdf - cdf[0]) / (cdf[-1] - cdf[0])
    return lambda n: np.interp(rng.random(n), cdf, xg)

def quad_row(alpha, logMc, s_int, s_w, a0=A0, delta=0.0):
    xs = np.linspace(11.0, 12.4, 12001); gs = np.linspace(10.3 - 5*0.3, 10.3 + 5*0.3, 801)
    u = 10.0**(xs - logMc); wx = u**(alpha + 1.0) * np.exp(-u)
    wg = np.exp(-0.5*((gs - 10.3)/0.3)**2)
    X, Gm = np.meshgrid(xs, gs, indexing="ij")
    m = logv_law(X, Gm, a0) + delta
    s_c = np.hypot(s_int, s_w)
    z = (m - CUT) / s_c
    W = wx[:, None] * wg[None, :]
    from scipy.stats import norm
    P = ndtr(z)
    num = (W * (s_int**2 / s_c) * norm.pdf(z)).sum() + delta * (W * P).sum()
    den = (W * P).sum()
    surv = den / W.sum()
    meanx = (W * P * X).sum() / den
    return num / den, surv, meanx

def mc_two(sampler_x, s_int, s_w, s_f, a0=A0, delta=0.0, decouple=False, nd=NDRAW):
    """returns dict with n_sel, mean bias, sd, mean v_flat (arith), mean logMs, SE"""
    n_sel = 0; S1 = 0.0; S2 = 0.0; Sv = 0.0; Sx = 0.0; nt = 0
    for _ in range(nd // CH):
        x = sampler_x(CH); lg = 10.3 + 0.3 * rng.standard_normal(CH)
        m = logv_law(x, lg, a0)
        ei = s_int * rng.standard_normal(CH) + delta
        ew = s_w * rng.standard_normal(CH)
        ef = s_f * rng.standard_normal(CH)
        if decouple:
            ei_t = s_int * rng.standard_normal(CH) + delta
        else:
            ei_t = ei
        sel = (m + (ei - delta) + ew + delta) > CUT if False else (m + ei + ew > CUT)
        e = (ei_t + ef)[sel]
        n_sel += sel.sum(); S1 += e.sum(); S2 += (e**2).sum()
        Sv += (10.0**(m[sel] + e)).sum(); Sx += x[sel].sum(); nt += CH
    mu = S1 / n_sel; sd = np.sqrt(S2 / n_sel - mu**2)
    return dict(n_sel=int(n_sel), bias=mu, sd=sd, se=sd/np.sqrt(n_sel), vmean=Sv/n_sel, xmean=Sx/n_sel, surv=n_sel/nt)

t0 = time.time()
# ---------------- BASE two-measurement grid: MC + quadrature ----------------
res_grid = {}
for name, (al, lm) in MF.items():
    smp = sampler(al, lm, 11.0, 12.4)
    rows = []
    for si in SI:
        for sw in SW:
            for sf in SF:
                if name != "BASE" and sf != 0.02: continue
                r = mc_two(smp, si, sw, sf, decouple=MUT)
                bq, sq, xq = quad_row(al, lm, si, sw)
                r.update(s_int=si, s_w=sw, s_f=sf, bias_quad=bq, surv_quad=sq, xmean_quad=xq,
                         match=bool(280 <= r["vmean"] <= 300 and 11.20 <= r["xmean"] <= 11.30))
                rows.append(r)
    res_grid[name] = rows
    print(name, "done", round(time.time() - t0), "s", flush=True)
out["grid"] = res_grid
def rng_stats(rows, key="bias"):
    m = [r[key] for r in rows if r["match"]]
    return (min(m), max(m), len(m)) if m else (None, None, 0)
base = res_grid["BASE"]
mlo, mhi, nm = rng_stats(base)
alllo = min(r["bias"] for r in base); allhi = max(r["bias"] for r in base)
B_mine = 0.5*(mlo + mhi) if nm else float("nan")
print(f"BASE MATCH rows n={nm}: bias range {mlo}..{mhi}  centre {B_mine};  whole grid {alllo:.3f}..{allhi:.3f}")
out.update(B_mine=B_mine, match_lo=mlo, match_hi=mhi, n_match=nm, grid_lo=alllo, grid_hi=allhi)
for nm_ in ("FLAT", "STEEP"):
    lo, hi, n = rng_stats(res_grid[nm_]); print(nm_, "MATCH", n, lo, hi); out[f"match_{nm_}"] = (lo, hi, n)
# ---------------- controls M1, M4 ----------------
bad = []; badS = []
for r in base:
    if r["n_sel"] >= 2000:
        if abs(r["bias"] - r["bias_quad"]) > 4*r["se"] and not MUT: bad.append((r["s_int"], r["s_w"], r["s_f"], r["bias"], r["bias_quad"], r["se"]))
    if abs(r["surv"]/r["surv_quad"] - 1) > 0.03 and r["n_sel"] > 20000: badS.append((r["s_int"], r["s_w"], r["surv"], r["surv_quad"]))
if not MUT:
    chk("M1 MC vs exact quadrature bias (4 MC-SE)", not bad, f"{len(bad)} discrepant rows {bad[:3]}")
    chk("M4 survival fraction MC vs quadrature (3%)", not badS, f"{len(badS)} discrepant rows {badS[:3]}")
# ---------------- M0 null (decoupled) ----------------
smpB = sampler(-1.0, 10.7, 11.0, 12.4)
r0 = mc_two(smpB, 0.06, 0.08, 0.02, decouple=True, nd=20_000_000)
chk("M0 decoupled selection gives zero bias (4 SE)", abs(r0["bias"]) < 4*r0["se"], f"bias {r0['bias']:+.5f} se {r0['se']:.5f}")
# ---------------- single-measurement ----------------
sm = []
for d in (0.0, 0.05):
    for s in (0.02, 0.04, 0.06, 0.08, 0.10):
        r = mc_two(smpB, s, 0.0 if False else 1e-12, 1e-12, delta=d, decouple=False, nd=20_000_000)   # e_int = the single error
        bq, sq, xq = quad_row(-1.0, 10.7, s, 1e-9, delta=d)
        # single-measurement: e = delta + s N; bias relative to law = mean(e)
        sm.append(dict(delta=d, s=s, mean_e=r["bias"], mean_e_quad=bq, surv=r["surv"], n_sel=r["n_sel"]))
out["single"] = sm
mono = all(sm[i+1]["mean_e"] > sm[i]["mean_e"] for i in range(4))
chk("M2 single-measurement bias>0 and monotone in s (delta=0)", mono and sm[0]["mean_e"] > 0, str([round(x["mean_e"], 4) for x in sm[:5]]))
# ---------------- M3 injected offset, central MATCH row ----------------
match_rows = [r for r in base if r["match"]]
if match_rows:
    cen = min(match_rows, key=lambda r: abs(r["bias"] - B_mine))
else:
    cen = min(base, key=lambda r: abs(r["bias"] - 0.076))
inj = {}
for d in (-0.05, 0.0, 0.05, 0.10):
    r = mc_two(smpB, cen["s_int"], cen["s_w"], cen["s_f"], delta=d, decouple=MUT, nd=30_000_000)
    inj[d] = r["bias"]; print("inject", d, r["bias"], r["se"], flush=True)
b0 = inj[0.0]
rec = {d: (inj[d] - b0) for d in inj}
ok3 = all(abs(rec[d] - d) <= 0.010 for d in (-0.05, 0.05))
chk("M3 injected offset recovered after subtracting the delta=0 bias (|err|<=0.010, |delta|<=0.05)", ok3 and not MUT or (MUT and ok3),
    "central row s_int=%.2f s_w=%.2f: recovered-minus-injected %s" % (cen["s_int"], cen["s_w"], {d: round(rec[d]-d, 4) for d in rec}))
out["inject"] = {str(k): v for k, v in inj.items()}; out["central_row"] = {k: cen[k] for k in ("s_int", "s_w", "s_f", "bias")}
# ---------------- attacks ----------------
att = {}
# A2 other a0 in the mock law (MATCH criteria unchanged; report bias at the central row and the MATCH-range under each a0)
for a0v in (9.36e-11, 1.13e-10):
    rows = []
    for si in SI:
        for sw in SW:
            r = mc_two(smpB, si, sw, 0.02, a0=a0v, nd=10_000_000)
            r["match"] = bool(280 <= r["vmean"] <= 300 and 11.20 <= r["xmean"] <= 11.30); r.update(s_int=si, s_w=sw); rows.append(r)
    lo, hi, n = rng_stats(rows)
    att[f"a0={a0v:.3g}"] = dict(match_lo=lo, match_hi=hi, n=n, centre=None if n == 0 else .5*(lo+hi))
    print("A2 a0", a0v, att[f"a0={a0v:.3g}"], flush=True)
# A1 measured M_* with 0.2 dex error
def mc_mstar_err(s_int, s_w, s_f, sig_x=0.2, nd=NDRAW):
    smp = sampler(-1.0, 10.7, 10.0, 12.6)
    n_sel = 0; S1 = 0.0; S2 = 0.0; Sv = 0.0; Sxm = 0.0; Sxt = 0.0
    for _ in range(nd // CH):
        x = smp(CH); lg = 10.3 + 0.3*rng.standard_normal(CH)
        xm = x + sig_x*rng.standard_normal(CH)
        keep = xm >= 11.0
        x, lg, xm = x[keep], lg[keep], xm[keep]; n = x.size
        mt = logv_law(x, lg); mm = logv_law(xm, lg)
        ei = s_int*rng.standard_normal(n); ew = s_w*rng.standard_normal(n); ef = s_f*rng.standard_normal(n)
        sel = (mt + ei + ew) > CUT
        e = (mt + ei + ef - mm)[sel]
        n_sel += sel.sum(); S1 += e.sum(); S2 += (e**2).sum(); Sv += (10.0**(mt[sel] + ei[sel] + ef[sel])).sum(); Sxm += xm[sel].sum(); Sxt += x[sel].sum()
    mu = S1/n_sel
    return dict(n_sel=int(n_sel), bias=mu, se=np.sqrt(S2/n_sel - mu**2)/np.sqrt(n_sel), vmean=Sv/n_sel, xmean_meas=Sxm/n_sel, xmean_true=Sxt/n_sel)
rowsA = []
for si in SI:
    for sw in SW:
        r = mc_mstar_err(si, sw, 0.02, nd=30_000_000)
        r["match"] = bool(280 <= r["vmean"] <= 300 and 11.20 <= r["xmean_meas"] <= 11.30); r.update(s_int=si, s_w=sw); rowsA.append(r)
lo, hi, n = rng_stats(rowsA)
att["A1_Mstar_err_0.2"] = dict(match_lo=lo, match_hi=hi, n=n, centre=None if n == 0 else .5*(lo+hi), rows=rowsA)
print("A1 M* err 0.2:", lo, hi, n, flush=True)
out["attacks"] = att
out["checks"] = checks
out["runtime_s"] = time.time() - t0
# ---------------- reproduction ----------------
chk("R1 B_mine within 0.010 of CFG41's 0.076", abs(B_mine - 0.076) <= 0.010, f"B_mine {B_mine:.4f}; MATCH range {mlo}..{mhi} (CFG41: 0.067..0.085); grid {alllo:.3f}..{allhi:.3f} (CFG41: 0.003..0.154)")
json.dump(out, open(f"cfg97_selbias_mc{TAG}_results.json", "w"), indent=1, default=float)
fails = [c for c in checks if not c[1]]
print("FAILED:", [c[0] for c in fails]); sys.exit(1 if fails else 0)
