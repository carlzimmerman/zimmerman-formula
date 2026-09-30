"""CFG237 attack 5: the common-mode tracer-bias control C7 by mocks (frozen section 5.9). What it can and cannot detect.
MUTATE 3: a common-mode +0.30 dex on all gas masses: the 'level unchanged' line must FAIL (exit 1); the 'd_AB unchanged' line must PASS."""
import sys
from CFG237_common import *

t = start("CFG237_c7")
ck = Checks()
R = {}
NG, NMOCK = 20, 2000
RE = 3.0
TAU = 0.30


def gen(rng, fmode, N=NMOCK, nG=NG):
    z = rng.uniform(2, 5, size=(N, nG))
    logM = rng.uniform(10.5, 11.5, size=(N, nG))
    if fmode == "const":
        logit = np.zeros_like(z)
    elif fmode == "low":                  # POST-HOC (added after the first run): gas share 0.2
        logit = np.full_like(z, math.log10(0.2 / 0.8))
    else:
        logit = 0.3 * np.log10((1 + z) / 3.5)
    f = 1 / (1 + 10 ** (-logit))
    e = rng.normal(0, 0.08, size=(N, nG, 3))        # tracer-specific scatter (CO, [CI], dust)
    return z, logM, f, e


def analyse(z, logM, f, e, tau_c=0.0, tau_z=None, only_tracer=None, law_true="FLAT"):
    """true baryons M = 10^logM (gas share f); truth g_obs from law_true; analysis g_bar from M* + mean tracer gas mass (log-mean)."""
    M = 10 ** logM
    Mst = M * (1 - f); Mg = M * f
    r = 2 * RE
    Rd = RE / RD_FAC
    gb_true = disc_g(r, M, Rd)
    gobs = gb_true * nu_mono(gb_true / (A0["canonical"] * LAWS[law_true](z)))
    tz = 0.0 if tau_z is None else tau_z(z)
    bias = np.zeros(e.shape)
    if only_tracer is None:
        bias += (tau_c + tz)[..., None] if np.ndim(tz) else (tau_c + tz)
    else:
        bias[..., only_tracer] += tau_c
    logMt = np.log10(Mg)[..., None] + e + bias                 # the three tracer masses
    dAB = logMt[..., 0] - logMt[..., 2]                        # CO - dust
    dAC = logMt[..., 0] - logMt[..., 1]
    Mg_obs = 10 ** logMt.mean(axis=-1)                         # pooled tracer mean (log)
    gb_obs = disc_g(r, Mst + Mg_obs, Rd)
    dl = np.log10(gobs) - np.log10(gb_obs * nu_mono(gb_obs / A0["canonical"]))
    return dl, dAB, dAC


def slope(z, dl):
    zc = z - z.mean(axis=1, keepdims=True); dc = dl - dl.mean(axis=1, keepdims=True)
    return (zc * dc).sum(axis=1) / (zc ** 2).sum(axis=1)


for fmode in ("const", "rising", "low"):
    rng = np.random.default_rng(SEED)
    z, logM, f, e = gen(rng, fmode)
    dl0, dAB0, dAC0 = analyse(z, logM, f, e, 0.0)
    print(f"\n=== gas share mode: {fmode} (mean f = {f.mean():.2f}; g_bar/a0 median {np.median(disc_g(2 * RE, 10 ** logM, RE / RD_FAC)) / A0['canonical']:.1f}) ===")
    med0 = np.median(dl0, axis=1)
    print(f"   tau_c = 0: group median delta_FLAT mean over mocks {np.mean(med0):+.4f} (SD {np.std(med0):.4f}); slope of delta vs z {np.mean(slope(z, dl0)):+.4f} +- {np.std(slope(z, dl0)) / math.sqrt(NMOCK):.4f}")
    res = {}
    for tc in (-0.3, -0.15, 0.0, 0.15, 0.3):
        dl, dAB, dAC = analyse(z, logM, f, e, tc)
        m = float(np.mean(np.median(dl, axis=1))); s_ = float(np.mean(slope(z, dl)))
        res[tc] = dict(level=m, slope=s_, dAB_shift=float(np.max(np.abs(dAB - dAB0))), dAC_shift=float(np.max(np.abs(dAC - dAC0))))
        print(f"   common-mode tau_c {tc:+.2f}: level {m:+.4f}  slope {s_:+.4f}  max|d_AB shift| {res[tc]['dAB_shift']:.2e}  max|d_AC shift| {res[tc]['dAC_shift']:.2e}")
    dl, _, _ = analyse(z, logM, f, e, TAU)
    # analytic lever at tau_c = +0.3: per-galaxy  -log10(gb_new/gb_old) - dlog nu; use exact mocks vs the small-shift formula for a check
    lev = float(np.mean(np.median(dl, axis=1)) - np.mean(med0))
    dslope = res[TAU]["slope"] - res[0.0]["slope"]
    se = float(np.std(slope(z, dl) - slope(z, dl0)) / math.sqrt(NMOCK))
    print(f"   level shift at +0.30: {lev:+.4f} ; slope change {dslope:+.4f} per unit z (MC s.e. {se:.4f})")
    R[fmode] = dict(res=res, level_shift=lev, dslope=dslope, dslope_se=se)
    tag = "C7 "
    if MODE == "3" and fmode == "const":
        ck.add("M3 level unchanged within 0.01 under the common-mode +0.30 dex (MUTATE: must FAIL, the level moves)", abs(lev) < 0.01, f"{lev:+.4f}")
        ck.add("M3 d_AB unchanged to 1e-9 under the common-mode shift (must PASS)", res[TAU]["dAB_shift"] < 1e-9, f"{res[TAU]['dAB_shift']:.2e}")
    if fmode == "const":
        ck.add("C7 d_AB and d_AC unchanged to 1e-9 under a common-mode +0.30 dex", max(res[TAU]["dAB_shift"], res[TAU]["dAC_shift"]) < 1e-9, f"{res[TAU]['dAB_shift']:.2e}")
        ck.add("C7 within-class slope unchanged (|d slope| < 0.02 per unit z) for z-independent gas share", abs(dslope) < 0.02, f"{dslope:+.4f}")
        ck.add("C7 (frozen H15, P 0.5) level shift at +0.30 within 0.02 of the README's about -0.07", abs(lev - (-0.07)) <= 0.02, f"mine {lev:+.4f} in a regime with gas share 0.5 and g_bar/a0 ~ 4-20; the level depends on the regime")
    elif fmode == "low":
        ck.add("C7 POST-HOC (not frozen): at gas share 0.2 the level shift at +0.30 is within 0.02 of the README's about -0.07", abs(lev - (-0.07)) <= 0.02, f"mine {lev:+.4f}")
    else:
        ck.add("C7 (frozen H15) slope NOT unchanged when the gas share rises with z (expected to change)", abs(dslope) > 2 * se, f"{dslope:+.4f} (s.e. {se:.4f})")

# tracer-specific bias: only CO shifted by +0.3 (C7b): d_AB moves by exactly that amount
rng = np.random.default_rng(SEED)
z, logM, f, e = gen(rng, "const")
dl0, dAB0, dAC0 = analyse(z, logM, f, e, 0.0)
dl, dAB, dAC = analyse(z, logM, f, e, TAU, only_tracer=0)
sh_ab = float(np.mean(dAB - dAB0)); sh_ac = float(np.mean(dAC - dAC0)); sh_bc = 0.0
print(f"\n=== C7b tracer-specific bias: only the CO tracer +0.30 dex: d_AB (CO-dust) shift {sh_ab:+.4f}, d_AC (CO-[CI]) shift {sh_ac:+.4f}; the group-median level moves {np.mean(np.median(dl, axis=1)) - np.mean(np.median(dl0, axis=1)):+.4f} (a third of the common-mode shift: the pooled mean moves by tau/3)")
ck.add("C7b a tracer-specific bias IS detected by d_AB (shift = +0.30 to 1e-9)", abs(sh_ab - TAU) < 1e-9 and abs(sh_ac - TAU) < 1e-9)
R["C7b"] = dict(dAB=sh_ab, dAC=sh_ac)

# z-dependent common-mode bias: which b_z makes FLAT-true mocks mimic H(z)-true (invisible to d_AB)
print("\n=== z-dependent common-mode bias tau_c(z) = b_z log10((1+z)/3.5): the degeneracy with a0 proportional to E(z) ===")
rng = np.random.default_rng(SEED)
z, logM, f, e = gen(rng, "const")
dlH, _, _ = analyse(z, logM, f, e, 0.0, law_true="Hz")                   # truth H(z), analysis FLAT, no bias
sH = float(np.mean(slope(z, dlH))); lH = float(np.mean(np.median(dlH, axis=1)))
def s_for(bz):
    dl, dAB, _ = analyse(z, logM, f, e, 0.0, tau_z=lambda zz: bz * np.log10((1 + zz) / 3.5), law_true="FLAT")
    return float(np.mean(slope(z, dl))), float(np.mean(np.median(dl, axis=1))), float(np.max(np.abs(dAB - analyse(z, logM, f, e, 0.0)[1])))
print(f"   H(z)-true, no bias: mean slope {sH:+.4f} per unit z; level {lH:+.4f}")
lo, hi = -5.0, 5.0
slo = s_for(lo)[0] - sH; shi = s_for(hi)[0] - sH
for _ in range(60):
    mid = 0.5 * (lo + hi); sm = s_for(mid)[0] - sH
    if sm * slo > 0: lo = mid; slo = sm
    else: hi = mid
bz = 0.5 * (lo + hi)
s_b, l_b, dab = s_for(bz)
print(f"   b_z that equalises the FLAT-true slope with the H(z)-true slope: {bz:+.3f} (slope {s_b:+.4f} vs {sH:+.4f}; level {l_b:+.4f} vs {lH:+.4f}); d_AB shift {dab:.2e}")
print(f"   i.e. tau_c(z=2) = {bz * math.log10(3 / 3.5):+.3f}, tau_c(z=5) = {bz * math.log10(6 / 3.5):+.3f} dex on the gas of every tracer; the class-M band (+-0.03 / +-0.093) does not contain it, and d_AB does not see it")
R["b_z"] = dict(b_z=bz, slope_H=sH, slope_bias=s_b, dAB=dab)
ck.add("C7 a z-dependent common-mode bias is invisible to d_AB (<1e-9) yet reproduces the H(z) slope (equalised slope within 1e-3)", dab < 1e-9 and abs(s_b - sH) < 1e-3, f"b_z = {bz:+.3f}")

savejson("CFG237_c7", R)
nf = ck.n_fail("M3 level") if MODE == "3" else ck.n_fail()
print(f"\nSUMMARY: {len(ck.rows)} lines, {ck.n_fail()} FAIL ({nf} counted for the exit code)")
for r_ in ck.rows:
    if not r_[1]: print("   FAILED:", r_[0], "::", r_[2])
if MODE:
    print("MUTATE", MODE, "bites" if nf > 0 else "DOES NOT BITE"); sys.exit(1 if nf > 0 else 0)
sys.exit(0)
