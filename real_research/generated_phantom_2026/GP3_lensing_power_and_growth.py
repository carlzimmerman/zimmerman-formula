#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GP3 -- THE GENERATED PHANTOM ON COSMOLOGICAL SCALES: growth and the forest (Newtonian by construction) and the lensing
power spectrum (the new gate): does the phantom that KiDS needs around every galaxy add lensing power that cosmic
shear would see?

WHY.  GP1's construction keeps the web and the forest Newtonian: the dark component and the unbound gas neither source
nor feel the phantom.  Growth (BK3's failure) and the forest (the L346-L362 pincer) are therefore safe by construction.
But LIGHT sees the phantom.  KiDS-1000 wants each lens's phantom to reach ~1-3 Mpc (GP2: lambda ~ 2-3 Mpc, the external
field of the other bound baryons ~1e-5-1e-4 a0).  In that weak ambient field the kernel's response to ANY fluctuation of
the bound baryons on scales below lambda is boosted by ~nu(e) ~ 100 -- groups, pairs and filaments of galaxies included.
Cosmic shear (KiDS-1000, DES Y3, HSC Y3) measures the lensing power at k ~ 0.1-1 h/Mpc to a few per cent and finds it
at or slightly BELOW LCDM (S_8 ~ 0.76-0.78 vs Planck 0.83).  This lane measures the phantom's lensing power.

METHOD.  A nonlinear mock (the phantom is nonlinear in its source, so a linear estimate is only a cross-check):
  * a Gaussian linear field at z = 0.5 (the cosmic-shear lens epoch) from GP0's Eisenstein-Hu P(k), sigma_8 = 0.8111;
    the matter density a lognormal of the field smoothed at R_s = 1.5 Mpc; halos drawn cell by cell from GP0's
    Sheth-Tormen abundances (1e10-10^15.5 Msun) with lognormal bias b(M); each halo carries GP0's bound baryons;
  * the construction's phantom on the grid, exactly as GP1's action gives it (the Lagrangian form):
      (Lap - 1/lam^2) psi = 4 pi G rho_B,   rho_ph = -S* div[(nu_mono(|grad psi|/a0) - 1)(-grad psi)]/(4 pi G),
    physical units at z = 0.5, S*(k) = (k lam)^2/(1 + (k lam)^2);
  * power spectra of matter, phantom and their cross; the lensing field is matter + phantom (light sees both).
  REFERENCE.  The mock's matter lacks LCDM's one-halo power at k >~ 0.5 h/Mpc, which would inflate a ratio taken
  against it.  The gate therefore uses a CONSERVATIVE ratio against a Sheth-Tormen + NFW halo-model P_NL(k):
      R_cons(k) = 1 + [2 r_x(k) sqrt(P_ph P_NL) + P_ph] / P_NL,   r_x = the mock's matter-phantom correlation,
  i.e. the phantom is compared with LCDM's full nonlinear matter power; the mock-internal ratio is reported too.

CHECKS (gates fixed before this run)
  H1 CONTROL: the halo-model P_NL(k) -> P_lin at low k (within 5% at k = 0.02 h/Mpc) and exceeds it at k = 1 h/Mpc.
  M1 CONTROL: with the kernel switched off (a0 -> 0) the phantom vanishes and R = 1 to 1e-6.
  L1 THE GATE: at a screening length KiDS accepts (lambda = 2 and 3 Mpc, GP2's best; lambda = 1 Mpc reported), the
     construction's lensing power stays within 20% of LCDM's, R_cons(k) <= 1.2 for all k in [0.1, 1] h/Mpc
     (a 20% excess shifts the lensing S_8 by ~10%, several times the surveys' errors).
  L2 (documentary) CONVERGENCE: a 100 Mpc box at twice the resolution.
  L3 (documentary) THE LINEAR CROSS-CHECK: (1 + C_eff beta_B S(k)^2)^2 with C_eff = <nu - 1> + <w nu'>/3 from the mock's
     field distribution, against the mock's ratio at k = 0.1-0.2 h/Mpc.
  L4 (documentary) THE PINCER TABLE: for each lambda, KiDS (GP2: vs the realizable floor with the carrier's halo, and
     against L352's acceptance) beside cosmic shear (L1's R_cons at k = 0.3, 0.5, 1 h/Mpc).
  L6 (documentary) the stars-only and galaxy readings (smaller beta_B), at lambda = 2, 3 Mpc and without screening.
  L5 (documentary) THE REPLACEMENT LEAD: if the dark component is smooth below a scale R_fs at late times (a carrier
     that free-streams, e.g. L319's kicked daughters at 600-1000 km/s), the phantom REPLACES rather than adds to its
     small-scale lensing power.  Mock ratio with the dark share smoothed at R_fs = 1, 2, 3 Mpc.
  G1 (documentary) GROWTH: the web's sigma_8 with the bound baryons feeling the long-mode phantom (linear two-fluid
     model, C_eff and beta_B(z) from the mock and GP0): the change from LCDM.
  F1 (documentary) THE FOREST: the switch variable x_m = (3/2) Omega_m(z)(1 + delta) of forest gas (delta <= 10-20)
     at z = 2-3 against the virial-like threshold x_c = 50: w = 0 (the IGM is kernel-invisible).
MUTATE=1 switches the kernel off (no phantom): L1 then PASSES -- an inverted control (rc = 0) showing that any excess
is the phantom's, not the machinery's.
(Record: a first version of G1's documentary label claimed "< 1%" at sigma_8 scales; the measured changes are
 +0.8 / +2.0 / +3.1% and the label now reports them.  The first L6 run returned NaN without screening -- S*'s k = 0
 element was 0/0 -- fixed before commit; no gate involves L6.)
SCOPE.  One lens epoch (z = 0.5), a lognormal mock with Poisson halos (no halo exclusion, no sub-grid profiles: 0.78 Mpc
cells), the observed reading of "bound" (GP0), isolated-phantom kernel nu_mono; no Limber projection (the gate is
stated on P(k) over the k-range cosmic shear weights).  The carrier's clearing of galaxy halos (L357/L365) lowers the
matter's one-halo power, which would RAISE the phantom's relative share; it is not included (conservative).

Run from the repository root:  python3 real_research/generated_phantom_2026/GP3_lensing_power_and_growth.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")
from scipy.special import sici

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import GP0_bound_baryon_census as GP0                                  # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "GP3_lensing_power_and_growth"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "GP3", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the kernel is switched off (no phantom); L1 must PASS (inverted control, rc = 0) ***")

# ---------------------------------------------------------------------------------- the kernel (L340's nu_mono, via BK1)
P1 = os.path.join(REPO, "real_research", "blind_kernel_2026", "BK1_screened_kernel.py")
NS = {"__name__": "bk1", "__file__": P1}
_src = open(P1).read().split("# ------------------------------------------------------------------ linear LCDM")[0]
_src = _src.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
nu_mono = NS["nu_mono_arr"]
G = 6.67430e-11; MS = 1.98892e30; MPC = 3.0856775814913673e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
h = 0.6736; ZS = 0.5; aS = 1 / (1 + ZS); DZ = GP0.growth(ZS)
LAMS = [1.0, 2.0, 3.0]
KH_GATE = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)

# ============================================================================================ H1 halo model P_NL
banner("H1  THE LCDM REFERENCE: Sheth-Tormen + NFW halo-model P_NL(k) at z = 0.5")
dn, bh, _ = GP0.mass_function(ZS)
sel = (GP0.MM >= 1e7) & (GP0.MM <= 3e15)
lmh = GP0.LM[sel][::4]; dlh = (lmh[1] - lmh[0]) * math.log(10)
rho_c_z = GP0.RHO_CRIT0 * (GP0.Om * (1 + ZS) ** 3 + GP0.OL)


def nfw_uk(M, k):
    c = 10 ** (0.905 - 0.101 * np.log10(M / (1e12 / h))) * (1 + ZS) ** -0.5     # DM14-like, weak z scaling
    r200 = (3 * M / (4 * math.pi * 200 * rho_c_z)) ** (1 / 3) / aS                # comoving Mpc
    rs = r200 / c; x = k * rs
    si1, ci1 = sici((1 + c) * x); si0, ci0 = sici(x)
    mc = np.log(1 + c) - c / (1 + c)
    return (np.sin(x) * (si1 - si0) - np.sin(c * x) / ((1 + c) * x) + np.cos(x) * (ci1 - ci0)) / mc


KHM = np.geomspace(0.01, 3.0, 80) * h                                  # comoving 1/Mpc
I1 = np.zeros_like(KHM); P1h = np.zeros_like(KHM)
for lm in lmh:
    M = 10 ** lm; n = np.interp(lm, GP0.LM, dn); b = np.interp(lm, GP0.LM, bh); uk = nfw_uk(M, KHM)
    I1 += n * b * M * uk * dlh / GP0.RHO_M0; P1h += n * (M * uk) ** 2 * dlh / GP0.RHO_M0 ** 2
I1 += 1 - I1[0]                                                        # unresolved mass carries bias-weighted remainder
PLIN_HM = GP0.Pk0(KHM) * DZ ** 2
PNL = PLIN_HM * I1 ** 2 + P1h
PNL_of = lambda kh: np.interp(np.log(kh * h), np.log(KHM), PNL)
h1_low, h1_1 = float(PNL_of(0.02) / (GP0.Pk0(0.02 * h) * DZ ** 2)), float(PNL_of(1.0) / (GP0.Pk0(1.0 * h) * DZ ** 2))
P(f"    P_NL/P_lin at k = 0.02 / 0.1 / 0.3 / 1 h/Mpc: {h1_low:.3f} / {PNL_of(0.1) / (GP0.Pk0(0.1 * h) * DZ ** 2):.2f} / "
  f"{PNL_of(0.3) / (GP0.Pk0(0.3 * h) * DZ ** 2):.2f} / {h1_1:.2f}")
OUT["numbers"]["H1"] = {"low": h1_low, "k1": h1_1}
check("H1 CONTROL: the halo-model P_NL tends to P_lin at low k (5%) and exceeds it at k = 1 h/Mpc",
      f"{h1_low:.3f} at 0.02 h/Mpc; {h1_1:.2f} at 1 h/Mpc", abs(h1_low - 1) < 0.05 and h1_1 > 1.3)


# ============================================================================================ the mock
def build_mock(L, N, seed, reading="observed", RS=1.5):
    dx = L / N; rng = np.random.default_rng(seed)
    k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi; kz = np.fft.rfftfreq(N, d=dx) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(k1, k1, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2
    Pk = GP0.Pk0(np.sqrt(K2)) * DZ ** 2; Pk[0, 0, 0] = 0
    dk = np.fft.rfftn(rng.standard_normal((N, N, N))) * np.sqrt(Pk / dx ** 3)
    dS = np.fft.irfftn(dk * np.exp(-K2 * RS ** 2 / 2), s=(N, N, N)); sS = dS.std()
    rho_m = GP0.RHO_M0 * np.exp(dS - sS ** 2 / 2)
    edges = np.arange(10.0, 15.6, 0.1); cen = 0.5 * (edges[1:] + edges[:-1]); Vc = dx ** 3
    rhoB = np.zeros((N, N, N))
    for lc in cen:
        n = np.interp(lc, GP0.LM, dn) * 0.1 * math.log(10); b = np.interp(lc, GP0.LM, bh)
        cnt = rng.poisson(n * Vc * np.exp(b * dS - (b * sS) ** 2 / 2))
        rhoB += cnt * float(GP0.M_bound(10 ** lc, ZS, reading)) / Vc
    return {"L": L, "N": N, "dx": dx, "KX": KX, "KY": KY, "KZ": KZ, "K2": K2, "rho_m": rho_m, "rhoB": rhoB, "sS": sS}


def phantom(mk, lam, a0, on=True):
    """the construction's phantom (comoving Msun/Mpc^3) in the Lagrangian form; also |g| and nu - 1 on the grid."""
    N, KX, KY, KZ, K2 = mk["N"], mk["KX"], mk["KY"], mk["KZ"], mk["K2"]
    m2 = (aS / lam) ** 2
    rk = np.fft.rfftn(mk["rhoB"]); den = K2 + m2; den[0, 0, 0] = np.inf
    psik = -(4 * np.pi * G / aS) * rk * (MS / MPC ** 3) / den * MPC ** 2
    g = [-np.fft.irfftn(1j * KK * psik, s=(N, N, N)) / (aS * MPC) for KK in (KX, KY, KZ)]
    gm = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2)
    f = (nu_mono(gm / a0) - 1) if on else np.zeros_like(gm)
    divk = sum(1j * KK * np.fft.rfftn(f * gc) for KK, gc in zip((KX, KY, KZ), g))
    divk = divk * np.where(K2 > 0, K2 / np.maximum(K2 + m2, 1e-300), 0.0)  # S*: the action re-screens the phantom's source
    div = np.fft.irfftn(divk, s=(N, N, N)) / (aS * MPC)
    rho_ph = -div / (4 * np.pi * G) * aS ** 3 / (MS / MPC ** 3)
    return rho_ph, gm, f


def spectra(mk, fields):
    """binned auto/cross spectra of the listed contrast fields (comoving), with k in h/Mpc."""
    N, dx, L = mk["N"], mk["dx"], mk["L"]
    K = np.sqrt(mk["K2"]).ravel(); wz = np.where(mk["KZ"].ravel() == 0, 1.0, 2.0)
    kb = np.geomspace(2 * np.pi / L * 1.01, np.pi / dx, 24); idx = np.digitize(K, kb)
    F = {n: np.fft.rfftn(d).ravel() for n, d in fields.items()}
    def pk(a, b):
        p = (F[a] * np.conj(F[b])).real * dx ** 3 / N ** 3
        out, kk = [], []
        for i in range(1, len(kb)):
            s = idx == i
            if s.any(): out.append(np.sum(p[s] * wz[s]) / np.sum(wz[s])); kk.append(np.sum(K[s] * wz[s]) / np.sum(wz[s]))
        return np.array(kk) / h, np.array(out)
    return pk


def measure(mk, lam, a0, on=True, dark_smooth=None):
    rho_ph, gm, f = phantom(mk, lam, a0, on)
    dm = mk["rho_m"] / GP0.RHO_M0 - 1; dph = rho_ph / GP0.RHO_M0
    fields = {"m": dm, "ph": dph}
    if dark_smooth is not None:                                        # the dark share smoothed below R_fs (L5)
        fd = 1 - GP0.FB
        dmk = np.fft.rfftn(dm) * np.exp(-mk["K2"] * dark_smooth ** 2 / 2)
        fields["lens_rep"] = fd * np.fft.irfftn(dmk, s=dm.shape) + GP0.FB * dm + dph
    pk = spectra(mk, fields)
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    out = {"kh": kh, "Pmm": Pmm, "Pxx": Pxx, "Ppp": Ppp, "gm": gm, "f": f}
    if dark_smooth is not None: out["Prep"] = pk("lens_rep", "lens_rep")[1]
    return out


def ratios(ms):
    kh, Pmm, Pxx, Ppp = ms["kh"], ms["Pmm"], ms["Pxx"], ms["Ppp"]
    R_mock = (Pmm + 2 * Pxx + Ppp) / Pmm
    rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300))
    Pnl = PNL_of(kh)
    R_cons = 1 + (2 * rx * np.sqrt(np.maximum(Ppp, 0) * Pnl) + Ppp) / Pnl
    return kh, R_mock, R_cons, rx


T1 = time.time()
MK = build_mock(200.0, 256, 20260925)
P(f"\n  mock: 200 Mpc, 256^3 (cell {MK['dx']:.2f} Mpc), smoothed sigma {MK['sS']:.2f}; bound-baryon share "
  f"{MK['rhoB'].mean() / GP0.RHO_M0:.4f} (GP0 census f_B {GP0.census(ZS, 'observed')['f_B']:.4f})   [{time.time() - T0:.0f}s]")

# ============================================================================================ M1 control
banner("M1  CONTROL: the kernel switched off gives no phantom and R = 1")
m_off = measure(MK, 2.0, A0["canonical"], on=False)
kh0, Rm0, Rc0, _ = ratios(m_off)
m1 = float(np.max(np.abs(Rm0 - 1)))
P(f"    max |R - 1| with the kernel off: {m1:.1e}")
OUT["numbers"]["M1"] = m1
check("M1 CONTROL: kernel off -> R = 1 to 1e-6", f"{m1:.1e}", m1 < 1e-6)

# ============================================================================================ L1
banner("L1  THE LENSING POWER OF THE CONSTRUCTION: R_cons(k) (vs LCDM's halo-model P_NL) and the mock-internal ratio")
RES = {}
for foot in ("canonical", "alt"):
    for lam in LAMS:
        ms = measure(MK, lam, A0[foot], on=not MUTATE)
        kh, Rm, Rc, rx = ratios(ms)
        RES[(foot, lam)] = {"kh": kh, "R_mock": Rm, "R_cons": Rc, "rx": rx, "gm": ms["gm"], "f": ms["f"]}
        P(f"    {foot:9s} lambda {lam}: R_cons at k = " + ", ".join(f"{q}: {np.interp(q, kh, Rc):.2f}" for q in KH_GATE) +
          f";  mock-internal at 0.3/1: {np.interp(0.3, kh, Rm):.2f}/{np.interp(1.0, kh, Rm):.2f};  r_x(0.3) {np.interp(0.3, kh, rx):.2f}"
          f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["L1"] = {f"{f}|{l}": {str(q): float(np.interp(q, v["kh"], v["R_cons"])) for q in KH_GATE} for (f, l), v in RES.items()}
OUT["numbers"]["L1_mock_internal"] = {f"{f}|{l}": {str(q): float(np.interp(q, v["kh"], v["R_mock"])) for q in KH_GATE} for (f, l), v in RES.items()}
worst = {(f, l): max(float(np.interp(q, v["kh"], v["R_cons"])) for q in KH_GATE) for (f, l), v in RES.items()}
passing = [l for l in (2.0, 3.0) if all(worst[(f, l)] <= 1.2 for f in ("canonical", "alt"))]
check("L1 THE GATE: at a screening length KiDS accepts (lambda = 2 or 3 Mpc) the lensing power stays within 20% of LCDM's "
      "(R_cons <= 1.2 on k = 0.1-1 h/Mpc), both footings",
      {f"{f}|{l}": round(v, 2) for (f, l), v in worst.items()}, len(passing) > 0,
      "the phantom KiDS needs around every galaxy is generated collectively by clustered bound baryons in a weak ambient field")

# ============================================================================================ L2 convergence
banner("L2  CONVERGENCE: a 100 Mpc box at twice the resolution (canonical)")
MK2 = build_mock(100.0, 256, 20260926)
conv = {}
for lam in (2.0, 3.0):
    ms = measure(MK2, lam, A0["canonical"], on=not MUTATE); kh, Rm, Rc, rx = ratios(ms)
    conv[lam] = {str(q): float(np.interp(q, kh, Rc)) for q in (0.3, 0.5, 0.7, 1.0)}
    P(f"    lambda {lam}: R_cons at 0.3/0.5/0.7/1 h/Mpc = " + " / ".join(f"{conv[lam][str(q)]:.2f}" for q in (0.3, 0.5, 0.7, 1.0)) +
      "  (200 Mpc box: " + " / ".join(f"{np.interp(q, RES[('canonical', lam)]['kh'], RES[('canonical', lam)]['R_cons']):.2f}" for q in (0.3, 0.5, 0.7, 1.0)) +
      f")   [{time.time() - T0:.0f}s]")
OUT["numbers"]["L2"] = {str(k): v for k, v in conv.items()}
del MK2
check("L2 (documentary) the ratio in a 100 Mpc box at twice the resolution", {str(k): v for k, v in conv.items()}, True, "",
      load_bearing=False)

# ============================================================================================ L3 linear cross-check
banner("L3  THE LINEAR CROSS-CHECK: (1 + C_eff beta_B S^2)^2 at low k, C_eff from the mock's field distribution")
l3 = {}
beta = GP0.census(ZS, "observed")["beta_B"]
for lam in LAMS:
    r_ = RES[("canonical", lam)]
    gm = r_["gm"].ravel()[::7] / A0["canonical"]
    nu_ = nu_mono(gm); dnu = (nu_mono(gm * 1.001) - nu_mono(gm * 0.999)) / (0.002 * gm)
    ceff = float(np.mean(nu_ - 1) + np.mean(gm * dnu) / 3)
    lin = {}
    for q in (0.1, 0.2):
        kc = q * h; S_ = (kc * lam / aS) ** 2 / (1 + (kc * lam / aS) ** 2)
        lin[str(q)] = {"linear": (1 + ceff * beta * S_ ** 2) ** 2, "mock": float(np.interp(q, r_["kh"], r_["R_mock"]))}
    l3[lam] = {"C_eff": ceff, **lin}
    P(f"    lambda {lam}: C_eff = {ceff:.0f} (beta_B {beta:.4f});  k = 0.1: linear {lin['0.1']['linear']:.3f} vs mock {lin['0.1']['mock']:.3f};  "
      f"k = 0.2: linear {lin['0.2']['linear']:.3f} vs mock {lin['0.2']['mock']:.3f}")
OUT["numbers"]["L3"] = {str(k): v for k, v in l3.items()}
check("L3 (documentary) linear response vs the nonlinear mock at low k", {str(k): f"C_eff {v['C_eff']:.0f}" for k, v in l3.items()},
      True, "", load_bearing=False)

# ============================================================================================ L4 pincer table
banner("L4  THE PINCER: KiDS (GP2) beside cosmic shear (L1), per screening length")
gp2 = json.load(open(os.path.join(HERE, "GP2_kids_bound_source_kernel_results.json")))
l4 = {}
for lam in LAMS:
    w4 = gp2["numbers"]["W4"]; w5 = gp2["numbers"]["W5"]["observed"]
    key = str(lam) if str(lam) in w5 else str(float(lam))
    l4[lam] = {"kids_vs_floor_with_carrier": [w4[f"canonical|{lam}"]["vs_floor_same_fs"], w4[f"alt|{lam}"]["vs_floor_same_fs"]],
               "kids_vs_L352": w5[key], "R_cons": {str(q): float(np.interp(q, RES[("canonical", lam)]["kh"], RES[("canonical", lam)]["R_cons"]))
                                                   for q in (0.3, 0.5, 1.0)}}
    P(f"    lambda {lam} Mpc: KiDS vs floor (+carrier) {l4[lam]['kids_vs_floor_with_carrier'][0]:+.1f}/{l4[lam]['kids_vs_floor_with_carrier'][1]:+.1f}, "
      f"vs L352 {l4[lam]['kids_vs_L352'][0]:+.1f}/{l4[lam]['kids_vs_L352'][1]:+.1f};  cosmic shear R_cons 0.3/0.5/1 h/Mpc: "
      + " / ".join(f"{v:.2f}" for v in l4[lam]["R_cons"].values()))
OUT["numbers"]["L4"] = {str(k): v for k, v in l4.items()}
check("L4 (documentary) the KiDS / cosmic-shear table", {str(k): v["R_cons"] for k, v in l4.items()}, True, "", load_bearing=False)

# ============================================================================================ L5 replacement lead
banner("L5  THE REPLACEMENT LEAD: the dark share smooth below R_fs at late times -- does the phantom replace it?")
l5 = {}
for lam in (2.0, 3.0):
    for Rfs in (1.0, 2.0, 3.0):
        ms = measure(MK, lam, A0["canonical"], on=not MUTATE, dark_smooth=Rfs)
        Rrep = ms["Prep"] / ms["Pmm"]
        l5[(lam, Rfs)] = {str(q): float(np.interp(q, ms["kh"], Rrep)) for q in (0.1, 0.3, 0.5, 0.7, 1.0)}
        P(f"    lambda {lam}, R_fs {Rfs} Mpc: (smoothed dark + baryons + phantom)/matter at 0.1/0.3/0.5/0.7/1 h/Mpc = "
          + " / ".join(f"{v:.2f}" for v in l5[(lam, Rfs)].values()))
OUT["numbers"]["L5"] = {f"{k[0]}|{k[1]}": v for k, v in l5.items()}
check("L5 (documentary) the replacement lead (mock-internal ratio; matter reference = the unsmoothed mock)",
      {f"{k[0]}|{k[1]}": {q: round(v, 2) for q, v in d.items()} for k, d in l5.items()}, True,
      "a dark component smooth below ~lambda lets the phantom stand in for its small-scale lensing power", load_bearing=False)

# ============================================================================================ L6 other readings
banner("L6  OTHER READINGS OF 'BOUND' (canonical): stars only and galaxy (stars + cold gas), incl. no screening")
l6 = {}
for rd in ("stars", "galaxy"):
    MKr = build_mock(200.0, 256, 20260925, reading=rd)
    for lam in (2.0, 3.0, float("inf")):
        ms = measure(MKr, lam, A0["canonical"], on=not MUTATE); kh, Rm, Rc, rx = ratios(ms)
        l6[(rd, lam)] = {str(q): float(np.interp(q, kh, Rc)) for q in (0.1, 0.3, 0.5, 1.0)}
        P(f"    {rd:6s} lambda {lam}: R_cons at 0.1/0.3/0.5/1 h/Mpc = " + " / ".join(f"{v:.2f}" for v in l6[(rd, lam)].values())
          + f"   [{time.time() - T0:.0f}s]")
    del MKr
OUT["numbers"]["L6"] = {f"{k[0]}|{k[1]}": v for k, v in l6.items()}
check("L6 (documentary) the lensing power for the stars-only and galaxy readings (smaller beta_B), with and without screening",
      {f"{k[0]}|{k[1]}": round(max(v.values()), 2) for k, v in l6.items()}, True,
      "a smaller bound-baryon share lowers the collective phantom; without screening every scale is boosted", load_bearing=False)

# ============================================================================================ G1 growth
banner("G1  GROWTH: the web is Newtonian; only bound baryons (f_B) feel the long-mode phantom (linear two-fluid model)")
from scipy.integrate import solve_ivp
Om0 = GP0.Om; OL0 = GP0.OL
zz = np.array([3.0, 2.0, 1.0, 0.5, 0.25, 0.0]); fB_z = np.array([GP0.census(z, "observed")["f_B"] for z in zz])
bB_z = np.array([GP0.census(z, "observed")["b_B"] for z in zz])
ceff_mock = l3[2.0]["C_eff"]
g1 = {}
for lam in LAMS:
    def rhs(N_, y, kc):
        a = math.exp(N_); z = 1 / a - 1
        E2 = Om0 / a ** 3 + OL0; Omz = Om0 / a ** 3 / E2; dlnH = -1.5 * Omz
        fB = float(np.interp(z, zz[::-1], fB_z[::-1])); bB = float(np.interp(z, zz[::-1], bB_z[::-1]))
        S_ = (kc * lam / a) ** 2 / (1 + (kc * lam / a) ** 2)
        dW, vW, dB, vB = y
        src = 1.5 * Omz * ((1 - fB) * dW + fB * dB)
        extra = 1.5 * Omz * ceff_mock * fB * dB * S_ ** 2 * (0.0 if MUTATE else 1.0)
        return [vW, -(2 + dlnH) * vW + src, vB, -(2 + dlnH) * vB + src + extra]
    out_k = {}
    for kh_ in (0.05, 0.1, 0.2, 0.5):
        a_i = 1 / 21
        sol = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i, a_i, a_i, a_i], args=(kh_ * h,), rtol=1e-8, atol=1e-12)
        sol0 = solve_ivp(lambda N_, y, kc: [y[1], -(2 - 1.5 * (Om0 / math.exp(N_) ** 3 / (Om0 / math.exp(N_) ** 3 + OL0))) * y[1]
                                            + 1.5 * (Om0 / math.exp(N_) ** 3 / (Om0 / math.exp(N_) ** 3 + OL0)) * y[0], 0, 0],
                         [math.log(a_i), 0.0], [a_i, a_i, 0, 0], args=(kh_ * h,), rtol=1e-8, atol=1e-12)
        fB0 = fB_z[-1]
        dm = (1 - fB0) * sol.y[0, -1] + fB0 * sol.y[2, -1]
        out_k[str(kh_)] = float(dm / sol0.y[0, -1] - 1)
    g1[lam] = out_k
    P(f"    lambda {lam}: fractional change of the matter growth D(z=0) by k (h/Mpc): " + ", ".join(f"{k}: {v:+.1e}" for k, v in out_k.items()))
OUT["numbers"]["G1"] = {str(k): v for k, v in g1.items()}
check("G1 (documentary) the change of the web's linear growth D(z = 0) at k = 0.2 h/Mpc (sigma_8 scales), per lambda",
      {str(k): f"{v['0.2']:+.1e}" for k, v in g1.items()}, True,
      "small but not nil: the bound baryons feel the long-mode phantom and pull the web a little (a +1-3% sigma_8 shift)",
      load_bearing=False)

# ============================================================================================ F1 forest
banner("F1  THE FOREST: forest gas is below the switch threshold (kernel-invisible)")
f1 = {}
for z in (2.0, 3.0):
    Omz = GP0.Om * (1 + z) ** 3 / (GP0.Om * (1 + z) ** 3 + GP0.OL)
    f1[z] = {str(d): 1.5 * Omz * (1 + d) for d in (10, 20)}
    P(f"    z = {z}: x_m = (3/2) Omega_m(z)(1 + delta) = {f1[z]['10']:.1f} (delta 10), {f1[z]['20']:.1f} (delta 20) vs x_c = 50")
OUT["numbers"]["F1"] = {str(k): v for k, v in f1.items()}
check("F1 (documentary) forest absorbers (delta <= 20) sit below a virial-like threshold x_c = 50 at z = 2-3: w = 0",
      {str(k): v for k, v in f1.items()}, all(v["20"] < 50 for v in f1.values()), "", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  Growth and the forest are Newtonian by construction up to the bound baryons' share (G1: D(z=0) at k = 0.2 h/Mpc changes by
  {g1[1.0]['0.2']:+.1%} / {g1[2.0]['0.2']:+.1%} / {g1[3.0]['0.2']:+.1%} at lambda = 1 / 2 / 3 Mpc; F1: the IGM is below the switch).
  THE LENSING POWER, conservative ratio against LCDM's halo-model P_NL (z = 0.5), canonical:""")
for lam in LAMS:
    r_ = RES[("canonical", lam)]
    P(f"    lambda {lam} Mpc: " + ", ".join(f"k {q}: {np.interp(q, r_['kh'], r_['R_cons']):.2f}" for q in KH_GATE))
P(f"""  KiDS (GP2) wants lambda ~ 2-3 Mpc (and accepts 1-10 against L352's reference); at those lengths the phantom raises the
  lensing power by factors {min(worst[('canonical', 2.0)], worst[('canonical', 3.0)]):.1f}-{max(worst[('canonical', 2.0)], worst[('canonical', 3.0)]):.1f} on k <= 1 h/Mpc.  Gate L1 (<= 1.2): {'PASS' if passing else 'FAIL'} ({passing}).
  The replacement lead (L5): with the dark share smooth below R_fs the lensing power returns toward the matter's --
  the phantom must REPLACE the dark component's small-scale power, not add to it.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
