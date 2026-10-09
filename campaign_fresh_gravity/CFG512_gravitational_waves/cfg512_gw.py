#!/usr/bin/env python3
"""CFG512 -- gravitational waves as tests of the framework (criteria: FROZEN_CRITERIA.md, committed alone first).

Four parts, offline only (on-disk DESI DR2 chains + forecasts; nothing downloaded):
  1. standard sirens -> (w0, wa) -> the law's a0(z)/a0(0) = sqrt(f_DE(z)) at z = 0.5, 1, 2.5;
  2. d_GW / d_EM on the C-H/K chassis (sympy tensor action on FRW), the MOND-sector halo phase bound, Shapiro equality;
  3. the nu_mono phantom around massive black holes and the EMRI dephasing of a cold-energy dress;
  4. pulsar timing: the ultralight-field oscillation at the CFG474 mass-window edges.
Forecast inputs are RECALLED from the literature and UNVERIFIED (flagged in the output).  kappa = 1/2 is FITTED; the cold
energy's mass is still required; not theory closed.

Run:  nice -n 15 python3 cfg512_gw.py            (main:   cfg512_gw.out, cfg512_results.json)
      CFG512_MUTATE=1 nice -n 15 python3 cfg512_gw.py (MUTATE: cfg512_gw_MUTATE.out, cfg512_results_MUTATE.json)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import sys, json, math, io, importlib.util, contextlib
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("CFG512_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
OUTF = os.path.join(HERE, f"cfg512_gw{TAG}.out")
JSONF = os.path.join(HERE, f"cfg512_results{TAG}.json")


class Tee:
    def __init__(self, fh): self.fh, self.so = fh, sys.__stdout__
    def write(self, s): self.fh.write(s); self.so.write(s)
    def flush(self): self.fh.flush(); self.so.flush()


_fh = open(OUTF, "w"); sys.stdout = Tee(_fh)
CHECKS, OUT = [], {"mutate": MUT}


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)


def hdr(s):
    print("\n" + "=" * 110 + f"\n{s}\n" + "=" * 110, flush=True)


# ------------------------------------------------------------------ constants (SI)
G, C = 6.674e-11, 2.99792458e8
MSUN, PC, YR = 1.989e30, 3.0857e16, 3.156e7
MPC, KPC = 1e6 * PC, 1e3 * PC
HBAR_EVS, EV_J = 6.582119569e-16, 1.602176634e-19
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
WALL_DEX = 0.30            # the galaxy-route calibration wall at z ~ 2.5 (CFG240 / PAPER38)
ZS = [0.5, 1.0, 2.5]
print("CFG512 -- gravitational waves as tests of the framework" + ("   [MUTATE: beta = 0.01 chassis; a0 forced flat]" if MUT else ""))
print("kappa = 1/2 FITTED; cold energy mass required; forecast inputs RECALLED/UNVERIFIED; not theory closed.")

# ================================================================== PART 1
hdr("PART 1. standard sirens -> (w0, wa) -> the law's a0(z)/a0(0) = sqrt(f_DE(z))")
THIN = os.path.join(ROOT, "fable_independent_2026", "data", "desi_dr2_w0wa_thinned")
BR = ("pantheonplus", "union3", "desy5sn")
NICE = {"pantheonplus": "Pantheon+", "union3": "Union3", "desy5sn": "DESY5", "lcdm": "LCDM fid"}
L275_MED25 = {"pantheonplus": -0.083, "union3": -0.107, "desy5sn": -0.098}   # L275 density mapping, z = 2.5


def f_DE(z, w0, wa):
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))


def dloga0(z, w0, wa):
    """framework prediction log10 a0(z)/a0(0); MUTATE M2 forces it flat."""
    if MUT:
        return 0.0 * np.asarray(w0, float)
    return 0.5 * np.log10(f_DE(z, w0, wa))


def dloga0_track(z, w0, wa):           # always the tracking law (for the M2 comparison)
    return 0.5 * np.log10(f_DE(z, w0, wa))


def wpct(x, wt, q):
    i = np.argsort(x); cx = np.cumsum(wt[i]) / wt.sum(); return np.interp(np.asarray(q) / 100.0, cx, x[i])


chains, fid = {}, {}
for b in BR:
    d = np.loadtxt(os.path.join(THIN, f"{b}.txt")); chains[b] = d
    wt, w, wa, om = d.T
    mu = np.array([np.average(om, weights=wt), np.average(w, weights=wt), np.average(wa, weights=wt)])
    X = np.vstack([om, w, wa]) - mu[:, None]
    cov = (X * wt) @ X.T / wt.sum()
    fid[b] = dict(om=mu[0], w0=mu[1], wa=mu[2], cov=cov)
fid["lcdm"] = dict(om=0.3111, w0=-1.0, wa=0.0, cov=fid["pantheonplus"]["cov"])
H0F = 67.7

print("\n1a. current baseline: the DESI DR2 chains (CMB + BAO + SN) propagated sample by sample")
print(f"    {'branch':10s} " + "  ".join(f"z={z:<4} 16/50/84 [dex]          " for z in ZS))
band = {}
for b in BR:
    wt, w, wa, om = chains[b].T
    row = {}
    for z in ZS:
        x = dloga0_track(z, w, wa)
        p = wpct(x, wt, [16, 50, 84]); row[z] = dict(p16=p[0], p50=p[1], p84=p[2], sig=0.5 * (p[2] - p[0]))
    band[b] = row
    print(f"    {NICE[b]:10s} " + "  ".join(f"{row[z]['p50']:+.3f} [{row[z]['p16']:+.3f},{row[z]['p84']:+.3f}] s={row[z]['sig']:.3f}" for z in ZS))
check("K1 the chains reproduce L275's density-mapping medians at z = 2.5 within 0.005 dex",
      all(abs(band[b][2.5]["p50"] - L275_MED25[b]) < 0.005 for b in BR),
      "; ".join(f"{NICE[b]} {band[b][2.5]['p50']:+.4f} vs {L275_MED25[b]:+.3f}" for b in BR))
OUT["chain_band"] = {b: {str(z): v for z, v in band[b].items()} for b in BR}

# ---- distances
ZG = np.concatenate([np.linspace(0, 0.2, 2001), np.linspace(0.2001, 8.0, 6000)])


def Ez(z, om, w0, wa):
    return np.sqrt(om * (1 + z) ** 3 + (1 - om) * f_DE(z, w0, wa))


def dL_grid(H0, om, w0, wa):
    inv = 1.0 / Ez(ZG, om, w0, wa)
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(ZG))])
    return (C / 1e3 / H0) * (1 + ZG) * chi      # Mpc


def Xi(z, Xi0, n=2.5):
    return Xi0 + (1 - Xi0) / (1 + z) ** n


def dGW(zev, p):
    H0, om, w0, wa, Xi0 = p
    return np.interp(zev, ZG, dL_grid(H0, om, w0, wa)) * Xi(zev, Xi0)


def sig_lens(z):
    return 0.066 * ((1 - (1 + z) ** -0.25) / 0.25) ** 1.8


def sig_pv(z, p, sv=200e3):
    H0, om, w0, wa, _ = p
    d = dGW(z, p); Hz = H0 * Ez(z, om, w0, wa)
    return np.abs(1 - (C / 1e3) * (1 + z) ** 2 / (Hz * d)) * sv / C


def qgrid(pdf, zmax, n, zmin=1e-3):
    zz = np.linspace(zmin, zmax, 20001); cdf = np.cumsum(pdf(zz)); cdf /= cdf[-1]
    return np.interp((np.arange(n) + 0.5) / n, cdf, zz)


def dVdz(z):
    zz = np.atleast_1d(z); inv = 1 / Ez(zz, 0.3111, -1, 0)
    chi = np.interp(zz, ZG, np.concatenate([[0], np.cumsum(0.5 * (1 / Ez(ZG[1:], .3111, -1, 0) + 1 / Ez(ZG[:-1], .3111, -1, 0)) * np.diff(ZG))]))
    return chi ** 2 * inv


def sfr_md(z):
    return (1 + z) ** 2.7 / (1 + ((1 + z) / 2.9) ** 5.6)


bns_pdf = lambda z: dVdz(z) * sfr_md(z) / (1 + z)
SCEN = {
    "S0": dict(label="LVK GW170817 (1 bright siren)", z=np.array([0.0098]), inst=lambda z, p: 0.14 + 0 * z, pv=True, lens=False),
    "S1": dict(label="LVK O5 bright BNS (30)", z=np.linspace(0.02, 0.15, 30), inst=lambda z, p: 0.10 + 0 * z, pv=True, lens=False),
    "S2": dict(label="LISA MBHB + counterpart (25)", z=qgrid(lambda z: z ** 2 * np.exp(-z / 1.0), 8.0, 25), inst=lambda z, p: 0.02 + 0 * z, pv=False, lens=True),
    "S3": dict(label="ET BNS + GRB/KN (1000)", z=qgrid(bns_pdf, 2.0, 1000), inst=None, k=0.10, pv=False, lens=True),
    "S3p": dict(label="ET pessimistic (200)", z=qgrid(bns_pdf, 2.0, 200), inst=None, k=0.10, pv=False, lens=True),
    "S4": dict(label="ET+CE optimistic (3000)", z=qgrid(bns_pdf, 3.0, 3000), inst=None, k=0.05, pv=False, lens=True),
}


def sig_d(sc, p):
    z = sc["z"]
    if sc["inst"] is None:
        d1 = dGW(np.array([1.0]), p)[0]
        s = np.maximum(sc["k"] * dGW(z, p) / d1, 0.01)
    else:
        s = sc["inst"](z, p)
    tot = s ** 2
    if sc["lens"]: tot = tot + sig_lens(z) ** 2
    if sc["pv"]: tot = tot + sig_pv(z, p) ** 2
    return np.sqrt(tot) * dGW(z, p)


def fisher(sc, p0, free):
    """Gaussian Fisher on the GW luminosity distances; free = indices of (H0, om, w0, wa, Xi0) varied."""
    sd = sig_d(sc, p0); J = []
    for i in free:
        h = 1e-4 * max(abs(p0[i]), 0.1); pp, pm = list(p0), list(p0); pp[i] += h; pm[i] -= h
        J.append((dGW(sc["z"], pp) - dGW(sc["z"], pm)) / (2 * h))
    J = np.array(J)
    return (J / sd) @ (J / sd).T


def prior_block(cov, free):
    """chain prior on (om, w0, wa) -> embedded in the free-parameter Fisher (H0 left free)."""
    P = np.zeros((len(free), len(free))); inv = np.linalg.inv(cov); m = {1: 0, 2: 1, 3: 2}
    for a, i in enumerate(free):
        for bb, j in enumerate(free):
            if i in m and j in m: P[a, bb] = inv[m[i], m[j]]
    return P


def grad_a0(z, w0, wa):
    h = 1e-5
    return np.array([(dloga0(z, w0 + h, wa) - dloga0(z, w0 - h, wa)) / (2 * h), (dloga0(z, w0, wa + h) - dloga0(z, w0, wa - h)) / (2 * h)])


# K2 Fisher sanity
p_l = [H0F, 0.3111, -1.0, 0.0, 1.0]
F1 = fisher(dict(z=np.array([0.05]), inst=lambda z, p: 0.05 + 0 * z, pv=False, lens=False), p_l, [0])
sH = 1 / math.sqrt(F1[0, 0])
Fa = fisher(dict(z=SCEN["S3"]["z"], inst=lambda z, p: 1e-3 + 0 * z, pv=False, lens=False), p_l, [0, 1, 2, 3])
Fb = fisher(dict(z=SCEN["S3"]["z"], inst=lambda z, p: 1e-6 + 0 * z, pv=False, lens=False), p_l, [0, 1, 2, 3])
ra = np.sqrt(np.diag(np.linalg.inv(Fa))) / np.sqrt(np.diag(np.linalg.inv(Fb)))
check("K2 Fisher sanity: one event at z = 0.05 with 5% distance error gives sigma(H0)/H0 within 10% of 5%; errors scale linearly with sigma_d (ratio 1000 over 1e-3/1e-6)",
      abs(sH / H0F / 0.05 - 1) < 0.10 and np.all(np.abs(ra / 1000 - 1) < 0.02), f"sigma(H0)/H0 = {sH / H0F:.4f}; scaling ratios {np.round(ra, 2)}")

print("\n1b. siren forecasts (inputs RECALLED, UNVERIFIED): 1-sigma on w0, wa and on the predicted Dlog10 a0(z) [dex]")
print("    'alone' = sirens only, (H0, Om, w0, wa) free;  '+prior' = sirens + the branch's DESI DR2 chain prior on (Om, w0, wa), H0 free")
sir = {}
free = [0, 1, 2, 3]
for fk in list(BR) + ["lcdm"]:
    f0 = fid[fk]; p0 = [H0F, f0["om"], f0["w0"], f0["wa"], 1.0]
    Pr = prior_block(f0["cov"], free)
    covP = np.linalg.inv(Pr[1:, 1:])            # prior alone on (om, w0, wa)
    res = {"prior_only": {}}
    gw = {z: grad_a0(z, f0["w0"], f0["wa"]) for z in ZS}
    for z in ZS:
        res["prior_only"][str(z)] = float(np.sqrt(gw[z] @ covP[1:, 1:] @ gw[z]))
    for sk, sc in SCEN.items():
        Fs = fisher(sc, p0, free)
        out = {}
        for lab, FF in (("alone", Fs), ("prior", Fs + Pr)):
            try:
                Cv = np.linalg.inv(FF + 1e-12 * np.eye(4))
            except np.linalg.LinAlgError:
                Cv = np.full((4, 4), np.inf)
            sw0, swa = math.sqrt(abs(Cv[2, 2])), math.sqrt(abs(Cv[3, 3]))
            sa = {str(z): float(np.sqrt(abs(gw[z] @ Cv[2:, 2:] @ gw[z]))) for z in ZS}
            out[lab] = dict(sw0=sw0, swa=swa, sa=sa)
        res[sk] = out
    sir[fk] = res
    print(f"\n    fiducial {NICE[fk]} (w0 {f0['w0']:+.3f}, wa {f0['wa']:+.3f}, Om {f0['om']:.4f}); chain prior alone: sigma Dlog a0 = " +
          ", ".join(f"z{z}: {res['prior_only'][str(z)]:.4f}" for z in ZS))
    print(f"      {'scenario':32s} {'alone: s(w0)  s(wa)   s_a0 z.5/1/2.5':42s} {'+prior: s(w0) s(wa)   s_a0 z.5/1/2.5'}")
    for sk, sc in SCEN.items():
        a, pr = res[sk]["alone"], res[sk]["prior"]
        fa = lambda v: f"{v:7.3f}" if v < 1e3 else "  >1e3 "
        print(f"      {sk:4s} {sc['label']:27s} {fa(a['sw0'])} {fa(a['swa'])}  " + "/".join(f"{min(a['sa'][str(z)], 999):.3f}" for z in ZS) +
              f"    {pr['sw0']:6.3f} {pr['swa']:6.3f}  " + "/".join(f"{pr['sa'][str(z)]:.4f}" for z in ZS))
OUT["sirens"] = sir

# rivals and comparisons at z
print("\n1c. the framework's prediction vs flat a0 and the a0 ∝ H(z) rival [dex], and the galaxy wall")
cmp_ = {}
for fk in list(BR) + ["lcdm"]:
    f0 = fid[fk]
    rows = {}
    for z in ZS:
        tr = float(dloga0_track(z, f0["w0"], f0["wa"])); pr_ = float(dloga0(z, f0["w0"], f0["wa"]))
        hz = float(np.log10(Ez(z, f0["om"], f0["w0"], f0["wa"])))
        rows[str(z)] = dict(framework=pr_, tracking=tr, flat=0.0, H_rival=hz, track_minus_flat=tr)
    cmp_[fk] = rows
    print(f"    {NICE[fk]:10s} " + "   ".join(f"z{z}: F {rows[str(z)]['framework']:+.3f} (track {rows[str(z)]['tracking']:+.3f}) flat 0  H {rows[str(z)]['H_rival']:+.3f}" for z in ZS))
OUT["predictions"] = cmp_

s_chain25 = {b: sir[b]["prior_only"]["2.5"] for b in BR}
s_S3p25 = {b: sir[b]["S3"]["prior"]["sa"]["2.5"] for b in BR}
P1a = all(s_S3p25[b] <= 0.5 * s_chain25[b] for b in BR)
P1b = all(band[b][2.5]["sig"] <= WALL_DEX / 3 for b in BR)
d_tf = {b: cmp_[b]["2.5"]["tracking"] for b in BR}
P1c = all(abs(d_tf[b]) >= 3 * WALL_DEX for b in BR)
print(f"\n    P1a sirens (S3 + prior) halve the chain-only sigma at z = 2.5 on every branch: {P1a}  "
      + "; ".join(f"{NICE[b]} {s_chain25[b]:.4f} -> {s_S3p25[b]:.4f}" for b in BR))
print(f"    P1b chain-only prediction sigma at z = 2.5 <= 0.10 dex (1/3 of the 0.3 dex wall): {P1b}  " + "; ".join(f"{NICE[b]} {band[b][2.5]['sig']:.3f}" for b in BR))
print(f"    P1c DESI-tracking minus flat at z = 2.5 resolvable by galaxies (>= 0.9 dex): {P1c}  " + "; ".join(f"{NICE[b]} {d_tf[b]:+.3f}" for b in BR))
# disclosed POST-HOC variant (not frozen): add an H0 prior of 0.5% to S4 + chain prior (does the P1a answer depend on H0 being free?)
hv = {}
for b in BR:
    f0 = fid[b]; p0 = [H0F, f0["om"], f0["w0"], f0["wa"], 1.0]
    FF = fisher(SCEN["S4"], p0, free) + prior_block(f0["cov"], free); FF[0, 0] += 1 / (0.005 * H0F) ** 2
    Cv = np.linalg.inv(FF); gz = grad_a0(2.5, f0["w0"], f0["wa"]); hv[b] = float(np.sqrt(abs(gz @ Cv[2:, 2:] @ gz)))
print("    post-hoc (not frozen): S4 + chain prior + H0 known to 0.5%: sigma(z = 2.5) = " + "; ".join(f"{NICE[b]} {hv[b]:.4f} (chain {s_chain25[b]:.4f})" for b in BR))
OUT["P1_posthoc_H0prior"] = hv
OUT["P1"] = dict(P1a=P1a, P1b=P1b, P1c=P1c, chain_sigma_z25=s_chain25, S3prior_sigma_z25=s_S3p25, track_minus_flat_z25=d_tf)

# M2 statement (holds in both modes, it is about the comparison): tracking - flat is 0 at LCDM, non-zero at DESI branches
lc = abs(dloga0_track(2.5, -1.0, 0.0)); de = [abs(d_tf[b]) for b in BR]
check("M2-statement: forcing a0 flat changes the siren-route prediction only where w != -1 (0 at the LCDM fiducial to 1e-12; > 0.01 dex at z = 2.5 on every DESI branch)",
      lc < 1e-12 and min(de) > 0.01, f"LCDM {lc:.1e}; DESI {[round(x, 3) for x in de]}")
check("C-TRACK the framework's prediction tracks rho_DE: at z = 2.5 it differs from flat by > 0.01 dex on every DESI branch and siren errors propagate (sigma > 0)",
      all(abs(cmp_[b]["2.5"]["framework"]) > 0.01 for b in BR) and all(sir[b]["S3"]["prior"]["sa"]["2.5"] > 0 for b in BR),
      "; ".join(f"{NICE[b]} {cmp_[b]['2.5']['framework']:+.3f}" for b in BR))

# ================================================================== PART 2
hdr("PART 2. d_GW / d_EM on the C-H/K chassis: the tensor action on FRW (sympy)")
t, x3, k = sp.symbols("t z k", real=True)
beta, c2, alph = sp.symbols("beta c_2 alpha", real=True)
a = sp.Function("a")(t); hf = sp.Function("h")(t, x3); M2f = sp.Function("M2")(t)
X = [t, sp.Symbol("x"), sp.Symbol("y"), x3]
g = sp.diag(-1, a ** 2 * sp.exp(hf), a ** 2 * sp.exp(-hf), a ** 2)
gi = g.inv()


def ricci_scalar(g, gi, X):
    n = 4
    Gam = [[[sp.simplify(sum(gi[l, s] * (sp.diff(g[s, m], X[nn]) + sp.diff(g[s, nn], X[m]) - sp.diff(g[m, nn], X[s])) for s in range(n)) / 2)
             for nn in range(n)] for m in range(n)] for l in range(n)]
    R = 0
    for m in range(n):
        for nn in range(n):
            Ric = 0
            for l in range(n):
                Ric += sp.diff(Gam[l][m][nn], X[l]) - sp.diff(Gam[l][m][l], X[nn])
                for s in range(n):
                    Ric += Gam[l][l][s] * Gam[s][m][nn] - Gam[l][nn][s] * Gam[s][m][l]
            R += gi[m, nn] * Ric
    return sp.simplify(R)


Rs = ricci_scalar(g, gi, X)
sqrtg = a ** 3                                     # exact: det g = -a^6
Kij = sp.diag(0, sp.diff(g[1, 1], t) / 2, sp.diff(g[2, 2], t) / 2, sp.diff(g[3, 3], t) / 2)   # lapse 1, shift 0, u = d_t
Kup = gi * Kij * gi
K = sp.simplify(sum(gi[i, i] * Kij[i, i] for i in range(1, 4)))
KK = sp.simplify(sum(Kij[i, i] * Kup[i, i] for i in range(1, 4)))
H = sp.diff(a, t) / a
acc2 = 0                                           # u = d_t with g_tt = -1: a_mu = (1/2) d_mu g_tt... = 0 exactly
print(f"    K = {sp.simplify(K - 3 * H)} + 3H;   K_ij K^ij - 3H^2 = {sp.simplify(KK - 3 * H ** 2)};   a.a = {acc2} (khronon acceleration vanishes on this background)")
BETA_VAL = sp.Rational(1, 100) if MUT else 0


def tensor_eom(lag):
    """linearised h-equation from the full Lagrangian density lag(h); returns (coef_hdd, coef_hd, coef_hzz, coef_h)."""
    eq = sp.euler_equations(lag, [hf], [t, x3])[0].lhs
    eps = sp.Symbol("eps")
    lin = sp.diff(eq.subs(hf, eps * hf).doit(), eps).subs(eps, 0)
    lin = sp.expand(sp.simplify(lin))
    D = {"hdd": sp.Derivative(hf, (t, 2)), "hd": sp.Derivative(hf, t), "hzz": sp.Derivative(hf, (x3, 2))}
    w = sp.Symbol("W"); sub = {}
    co = {}
    rest = lin
    for key in ("hdd", "hzz", "hd"):
        co[key] = sp.simplify(rest.coeff(D[key])); rest = sp.expand(rest - co[key] * D[key])
    co["h"] = sp.simplify(rest.coeff(hf)); rest = sp.simplify(rest - co["h"] * hf)
    co["rest"] = rest
    return co


# aether/khronon convention (Jacobson-Mattingly; L340/CFG292): L = R - beta K_ij K^ij - c_2 K^2 + alpha a.a, beta = c13
# (run 1 used +beta here, a sign-convention bug that gave c_T^2 = 1/(1+beta); kept as cfg512_gw_run1.out, disclosed)
L_full = sqrtg * (Rs - beta * KK - c2 * K ** 2 + alph * acc2)
co = tensor_eom(L_full)
fric = sp.simplify(co["hd"] / co["hdd"]); cT2 = sp.simplify(-co["hzz"] / co["hdd"] * a ** 2); mass = sp.simplify(co["h"] / co["hdd"])
print(f"    linear tensor equation:  h_tt + [{fric}] h_t - [{cT2}] h_zz / a^2 + [{mass}] h = 0   (remainder {co['rest']})")
alphaM = sp.simplify((fric - 3 * H) / H)
print(f"    alpha_M = (friction - 3H)/H = {alphaM};  c_T^2 = {cT2};  mass term = {mass}")
check("T1 friction is exactly 3H (alpha_M = 0) for symbolic (beta, c_2, alpha): no running tensor Planck mass, so Xi(z) = d_GW/d_EM = 1 exactly",
      alphaM == 0, f"alpha_M = {alphaM}")
check("T2 no tensor mass term on FRW (h-coefficient zero; residual zero)", mass == 0 and co["rest"] == 0, f"mass = {mass}, residual = {co['rest']}")
cT2_used = cT2.subs(beta, BETA_VAL)
dcT = float(sp.sqrt(cT2_used) - 1)
check("T3 c_T^2 = 1/(1 - beta) symbolically", sp.simplify(cT2 - 1 / (1 - beta)) == 0, f"c_T^2 = {cT2}")
check(f"T4 the chassis used (beta = {BETA_VAL}) is consistent with GW170817/GRB170817A: -3e-15 < c_T - 1 < 7e-16 (Abbott et al. 2017, recalled)",
      -3e-15 < dcT < 7e-16, f"c_T - 1 = {dcT:.3e}")
# K3 controls: GR limit and running-Planck-mass control
coGR = tensor_eom(sqrtg * Rs)
ok_gr = sp.simplify(coGR["hd"] / coGR["hdd"] - 3 * H) == 0 and sp.simplify(-coGR["hzz"] / coGR["hdd"] * a ** 2 - 1) == 0
coM = tensor_eom(M2f * sqrtg * Rs)
fM = sp.simplify(coM["hd"] / coM["hdd"])
ok_m = sp.simplify(fM - 3 * H - sp.diff(M2f, t) / M2f) == 0
check("K3 controls: GR gives h_tt + 3H h_t - h_zz/a^2 = 0; a time-dependent M_T^2(t) gives friction 3H + dln M_T^2/dt (= H(3 + alpha_M)), so the engine sees a running Planck mass when one exists",
      ok_gr and ok_m, f"GR ok {ok_gr}; running-mass friction = {fM}")
# Xi from friction
zz = np.linspace(0, 5, 501); delta = np.zeros_like(zz)            # delta = -alpha_M/2 = 0
Xi_z = np.exp(np.concatenate([[0], np.cumsum(0.5 * (delta[1:] / (1 + zz[1:]) + delta[:-1] / (1 + zz[:-1])) * np.diff(zz))]))
print(f"    Xi(z) on [0, 5]: min {Xi_z.min():.6f}, max {Xi_z.max():.6f}")

# MOND-sector halo phase bound: quadratic-in-h piece of the filtered a.a term ~ (g/c^2)^2 (coefficient bounded by 1)
gh, Lh = 1e-9, 100 * KPC
phase = {}
for lab, f in (("LVK 100 Hz", 100.0), ("LISA 1 mHz", 1e-3), ("PTA 10 nHz", 1e-8)):
    kk = 2 * math.pi * f / C; m2 = (gh / C ** 2) ** 2; phase[lab] = m2 * Lh / (2 * kk)
print("    MOND-sector bound inside a halo (g <= 1e-9 m/s^2, L = 100 kpc, coefficient <= 1): " + "; ".join(f"{k_}: dphi <= {v:.1e} rad" for k_, v in phase.items()))
check("T5 the filtered MOND sector changes GW phase by < 1e-6 rad through a 100 kpc halo at LVK, LISA and PTA frequencies", max(phase.values()) < 1e-6,
      f"max {max(phase.values()):.1e} rad")
# Shapiro: single metric; the emulator counterfactual (GWs blind to the phantom/cold mass)
vf, r0, re = 150e3, 8 * KPC, 300 * KPC
dt_emul = 2 * vf ** 2 / C ** 3 * (re - r0 - r0 * math.log(re / r0))
print(f"    Shapiro: in candidate B the phantom is filled by cold energy (real mass on the one metric), so photons and GWs share it: dt_GW-EM = 0.")
print(f"    counterfactual dark-matter emulator (GWs blind to the MW phantom; v_f 150 km/s, edge 300 kpc): dt = {dt_emul / 86400:.0f} days vs observed 1.7 s (Boran et al. 2018 class)")
OUT["part2"] = dict(alpha_M=str(alphaM), cT2=str(cT2), cT_minus_1_used=dcT, beta_used=str(BETA_VAL), Xi_minmax=[float(Xi_z.min()), float(Xi_z.max())],
                    halo_phase_bound=phase, shapiro_emulator_days=dt_emul / 86400, shapiro_framework=0.0)

print("\n2b. measurement forecast for Xi0 (Xi = Xi0 + (1 - Xi0)/(1+z)^2.5), sirens + Pantheon+ chain prior, H0 free")
xi_fc = {}
f0 = fid["pantheonplus"]; p0 = [H0F, f0["om"], f0["w0"], f0["wa"], 1.0]
fr5 = [0, 1, 2, 3, 4]; Pr5 = prior_block(f0["cov"], fr5)
for sk, sc in SCEN.items():
    FF = fisher(sc, p0, fr5) + Pr5
    s = math.sqrt(abs(np.linalg.inv(FF + 1e-12 * np.eye(5))[4, 4])); xi_fc[sk] = s
    print(f"    {sk:4s} {sc['label']:30s} sigma(Xi0) = " + (f"{s:.3g}" if s < 1e3 else "> 1e3 (unconstrained)"))
OUT["xi_forecast"] = xi_fc

# ================================================================== PART 3
hdr("PART 3. the nu_mono phantom around massive black holes and the EMRI dephasing of a cold-energy dress")
spec = importlib.util.spec_from_file_location("cfg5c", os.path.join(ROOT, "campaign_fresh_gravity", "CFG5_common.py"))
c5 = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(c5)
sys.stdout = Tee(_fh) if not isinstance(sys.stdout, Tee) else sys.stdout


def _h_rar(y):
    s = np.sqrt(y); return y / np.expm1(s)


from scipy.optimize import brentq
_dh = lambda tt: (2 * np.expm1(math.sqrt(tt)) - math.sqrt(tt) * (1 + np.expm1(math.sqrt(tt)))) / (2 * np.expm1(math.sqrt(tt)) ** 2)
YP = brentq(_dh, 1.0, 5.0); HP = float(_h_rar(YP)); DEL = 0.05
YS = brentq(lambda tt: _dh(tt) - DEL * HP / (tt + YP), 1.0, YP)


def h_mono(y):
    y = np.asarray(y, float)
    return np.where(y <= YS, _h_rar(np.maximum(y, 1e-300)), _h_rar(YS) + DEL * HP * np.log((y + YP) / (YS + YP)))


def h_rarexp(y):
    y = np.asarray(y, float); s = np.sqrt(y)
    return np.where(s > 700, 0.0, y / np.expm1(np.minimum(s, 700)))


yy = np.logspace(0, 6, 25)
dev = np.max(np.abs((1 + h_mono(yy) / yy) - c5.nu_mono(yy)))
check("K4 the direct h_mono(y) = (nu - 1) y reproduces CFG5_common.nu_mono at y = 1 .. 1e6 to 1e-6", dev < 1e-6, f"max |dnu| = {dev:.1e}; y* = {YS:.4f}, y_p = {YP:.4f}, h_p = {HP:.4f}")
print(f"    tail: h(1e8) = {float(h_mono(1e8)):.3f}, h(1e14) = {float(h_mono(1e14)):.3f}, h(1e20) = {float(h_mono(1e20)):.3f}: the phantom acceleration a0 h(y) GROWS (log) as y -> inf;"
      f" nu_RAR exp tail h(1e4) = {float(h_rarexp(1e4)):.1e}")

a0 = FOOT["canonical"]
MSIG = lambda M: 200e3 * (M / 3.1e8) ** (1 / 4.38)          # M-sigma (Kormendy & Ho 2013 form, recalled)


def host(M):
    sig = MSIG(M); rh = G * M * MSUN / sig ** 2
    return dict(M=M, sig=sig, rh=rh, Rs=2 * G * M * MSUN / C ** 2, risco=6 * G * M * MSUN / C ** 2)


def Mstar(r, hs):
    return 2 * hs["M"] * MSUN * (r / hs["rh"]) ** 1.25


def rho_phantom(r, hs, own, kern, a0v=a0):
    """rho_ph = (1/4 pi G r^2) d/dr [r^2 a0 h(y)], spherical; own O1: BH in g_b; O2: stars only."""
    def gb(rr):
        Mb = Mstar(rr, hs) + (hs["M"] * MSUN if own == "O1" else 0.0)
        return G * Mb / rr ** 2
    hk = h_mono if kern == "mono" else h_rarexp
    e = 1e-4
    f = lambda rr: rr ** 2 * a0v * hk(gb(rr) / a0v)
    return (f(r * (1 + e)) - f(r * (1 - e))) / (2 * e * r) / (4 * math.pi * G * r ** 2)


def gs_spike(r, hs, rho0, r0, gam, heated=False, rel=False):
    """Gondolo-Silk 1999 adiabatic spike (alpha_gamma ~ 0.122 for gamma = 1, recalled), (1 - 4R_s/r)^3 cut (zero at 8GM/c^2);
    rel=True: the relativistic inner edge at 4GM/c^2 (Sadeghian et al. 2013 form, recalled), (1 - 2R_s/r)^3."""
    Mbh = hs["M"] * MSUN
    Rsp = 0.122 * r0 * (Mbh / (rho0 * r0 ** 3)) ** (1 / (3 - gam))
    gsp = 1.5 if heated else (9 - 2 * gam) / (4 - gam)
    rhoR = rho0 * (Rsp / r0) ** (-gam)
    cut = np.clip(1 - (2 if rel else 4) * hs["Rs"] / r, 0, None) ** 3
    return np.where(r < Rsp, rhoR * (Rsp / r) ** gsp * cut, rho0 * (r0 / r) ** gam), Rsp


RHOC = 3 * (67.7e3 / MPC) ** 2 / (8 * math.pi * G)


def nfw_seed(M):
    M200 = 1e12 * (M / 4.3e6) ** (1 / 1.65) * MSUN; c = 10.0                 # M_BH-M_halo (recalled), c = 10 declared
    r200 = (3 * M200 / (4 * math.pi * 200 * RHOC)) ** (1 / 3); rs = r200 / c
    rhos = 200 * RHOC / 3 * c ** 3 / (math.log(1 + c) - c / (1 + c))
    return rhos, rs, M200


m_co = 10.0 * MSUN


def dephase(hs, rho_fn, T=4 * YR):
    M = hs["M"] * MSUN; Mt = M + m_co; ri = hs["risco"]
    K_ = (64 / 5) * G ** 3 * M * m_co * Mt / C ** 5
    rs = (ri ** 4 + 4 * K_ * T) ** 0.25
    r = np.logspace(math.log10(ri), math.log10(rs), 40001)
    Om = np.sqrt(G * Mt / r ** 3); v = Om * r
    rdot_gw = K_ / r ** 3
    lnL = math.log(math.sqrt(M / m_co))
    rho = rho_fn(r)
    P_df = 4 * math.pi * G ** 2 * m_co ** 2 * rho * lnL / v
    P_acc = 16 * math.pi * G ** 2 * m_co ** 2 * rho / C ** 2 * v
    rdot_x = (P_df + P_acc) * 2 * r ** 2 / (G * M * m_co)
    integ = 2 * Om * (1 / rdot_gw - 1 / (rdot_gw + rdot_x))
    dphi = np.sum(0.5 * (integ[1:] + integ[:-1]) * np.diff(r))
    phi_vac = np.sum(0.5 * (2 * Om[1:] / rdot_gw[1:] + 2 * Om[:-1] / rdot_gw[:-1]) * np.diff(r))
    phi_an = 2 * math.sqrt(G * Mt) / K_ * (2 / 5) * (rs ** 2.5 - ri ** 2.5)
    return dict(dphi=float(dphi), phi_vac=float(phi_vac), phi_an=float(phi_an), r_start=rs, rho_at_risco=float(rho_fn(np.array([ri]))[0]),
                rho_at_rstart=float(rho_fn(np.array([rs]))[0]), eps_max=float(np.max(rdot_x / rdot_gw)))


HOSTS = {"MW-like 4.3e6": 4.3e6, "LISA 1e6": 1e6, "LISA 1e5": 1e5}
PCU = MSUN / PC ** 3
k5 = dephase(host(1e6), lambda r: 0 * r)
check("K5 dephasing engine: rho = 0 gives dPhi = 0 and the 4-yr vacuum GW phase matches the analytic quadrupole result within 1e-3",
      k5["dphi"] == 0 and abs(k5["phi_vac"] / k5["phi_an"] - 1) < 1e-3, f"Phi_vac {k5['phi_vac']:.4e} vs {k5['phi_an']:.4e} rad")
p3 = {}
print(f"\n    {'host':15s} {'reading':38s} {'rho(r_ISCO) [Msun/pc3]':>23s} {'rho(r_4yr)':>11s} {'dPhi_4yr [rad]':>15s}")
for hn, M in HOSTS.items():
    hs = host(M); rows = {}
    A_seed = rho_phantom(np.array([hs["rh"]]), hs, "O1", "mono")[0]
    rhos, rsn, M200 = nfw_seed(M)
    readings = {
        "D1/O1 relaxed phantom, nu_mono": lambda r: rho_phantom(r, hs, "O1", "mono"),
        "D1/O2 relaxed phantom (BH owns none)": lambda r: rho_phantom(r, hs, "O2", "mono"),
        "D1 nu_RAR exp tail (comparator)": lambda r: rho_phantom(r, hs, "O1", "rar"),
        "D2 GS spike seeded by the phantom": lambda r: gs_spike(r, hs, A_seed, hs["rh"], 1.0)[0],
        "D2h heated spike r^-3/2 (phantom seed)": lambda r: gs_spike(r, hs, A_seed, hs["rh"], 1.0, heated=True)[0],
        "MOND (phantom = field, no matter)": lambda r: 0 * r,
        "LCDM NFW-seeded GS spike": lambda r: gs_spike(r, hs, rhos * rsn / hs["rh"], hs["rh"], 1.0)[0],
        "LCDM heated spike r^-3/2": lambda r: gs_spike(r, hs, rhos * rsn / hs["rh"], hs["rh"], 1.0, heated=True)[0],
        "D2rel phantom-seeded spike, 4GM/c^2 edge": lambda r: gs_spike(r, hs, A_seed, hs["rh"], 1.0, rel=True)[0],
        "LCDM GS spike, 4GM/c^2 edge": lambda r: gs_spike(r, hs, rhos * rsn / hs["rh"], hs["rh"], 1.0, rel=True)[0],
    }
    for rn, fn in readings.items():
        d = dephase(hs, fn); rows[rn] = d
        print(f"    {hn:15s} {rn:38s} {d['rho_at_risco'] / PCU:23.3e} {d['rho_at_rstart'] / PCU:11.3e} {d['dphi']:15.3e}")
    # static phantom (conservative) effect: dOmega^2/Omega^2 = h/y at r_start; bound on phase
    rs_ = rows["MOND (phantom = field, no matter)"]["r_start"]
    yst = G * M * MSUN / rs_ ** 2 / a0
    stat = 0.5 * float(h_mono(yst)) / yst * rows["MOND (phantom = field, no matter)"]["phi_vac"]
    rows["static_phantom_phase_bound"] = stat
    rows["seed_surface_density_phantom_kg_m2"] = float(A_seed * hs["rh"]); rows["seed_surface_density_nfw_kg_m2"] = float(rhos * rsn)
    rows["host"] = dict(M=M, sigma_kms=hs["sig"] / 1e3, r_h_pc=hs["rh"] / PC, M200=M200 / MSUN)
    print(f"    {hn:15s} static phantom orbit shift (MOND and framework alike): dPhi <= {stat:.1e} rad;  1/r-seed surface density rho*r: phantom {A_seed * hs['rh']:.3f} kg/m^2 vs NFW rho_s r_s {rhos * rsn:.3f} kg/m^2;  r_h {hs['rh'] / PC:.2f} pc")
    p3[hn] = rows
OUT["part3"] = p3
d1max = max(max(p3[h]["D1/O1 relaxed phantom, nu_mono"]["dphi"], p3[h]["D1/O2 relaxed phantom (BH owns none)"]["dphi"]) for h in HOSTS)
d1min = min(min(p3[h]["D1/O1 relaxed phantom, nu_mono"]["dphi"], p3[h]["D1/O2 relaxed phantom (BH owns none)"]["dphi"]) for h in HOSTS)
verdict3 = "NO DETECTABLE DRESS" if d1max < 0.1 else ("DETECTABLE DRESS" if d1max >= 1 else "MARGINAL")
print(f"\n    frozen rule on the recipe's headline (D1 relaxed, O1 and O2): max dPhi = {d1max:.2e} rad, min {d1min:.2e} -> {verdict3}")
d2 = {h: max(p3[h]["D2 GS spike seeded by the phantom"]["dphi"], p3[h]["D2rel phantom-seeded spike, 4GM/c^2 edge"]["dphi"]) for h in HOSTS}
lc3 = {h: max(p3[h]["LCDM NFW-seeded GS spike"]["dphi"], p3[h]["LCDM GS spike, 4GM/c^2 edge"]["dphi"]) for h in HOSTS}
print("    disclosed D2 (no relaxation in the nucleus): " + "; ".join(f"{h} {d2[h]:.2e}" for h in HOSTS) + "  |  LCDM GS spike: " + "; ".join(f"{h} {lc3[h]:.2e}" for h in HOSTS))
OUT["part3_verdict"] = dict(D1_max=d1max, D1_min=d1min, verdict=verdict3, D2=d2, LCDM_spike=lc3)

# ================================================================== PART 4
hdr("PART 4. pulsar timing: the ultralight-field oscillation at the CFG474 window edges")
rho_loc = 0.4e9 * EV_J / C ** 2 / 1e-6                          # 0.4 GeV/cm^3 in kg/m^3


def kr(m_ev, rho=rho_loc):
    w = m_ev / HBAR_EVS; Psi = math.pi * G * rho / w ** 2; f = 2 * w / (2 * math.pi)
    return Psi, f, Psi / (2 * math.pi * f)


Pk, fk_, _ = kr(1e-22)
check("K6 the Khmelnitsky-Rubakov amplitude reproduces Psi_c ~ 6.1e-18 at m = 1e-22 eV, rho = 0.4 GeV/cm^3 (within 10%)", abs(Pk / 6.1e-18 - 1) < 0.10, f"Psi_c = {Pk:.2e}, f = {fk_:.2e} Hz")
p4 = {}
for m in (3.0e-19, 3.9e-19, 5.3e-17):
    Ps, f, dt = kr(m); p4[str(m)] = dict(Psi=Ps, f_Hz=f, residual_s=dt, in_PTA_band=bool(1e-9 <= f <= 1e-7))
    print(f"    m = {m:.1e} eV: f = {f:.2e} Hz (PTA band 1e-9..1e-7: {1e-9 <= f <= 1e-7}), Psi_c = {Ps:.1e}, residual ~ {dt:.1e} s (PTA noise ~1e-7 s)")
check("P4 every surviving cold-energy wave mass (CFG474) puts the oscillation outside the PTA band with a residual < 1e-15 s: no PTA oscillation signal",
      all((not v["in_PTA_band"]) and v["residual_s"] < 1e-15 for v in p4.values()))
OUT["part4"] = p4

# ================================================================== summary
hdr("SUMMARY")
npass = sum(ok for _, ok in CHECKS)
print(f"    checks: {npass}/{len(CHECKS)} pass")
for n_, ok in CHECKS:
    if not ok: print(f"      FAILED: {n_}")
OUT["checks"] = {n_: ok for n_, ok in CHECKS}
with open(JSONF, "w") as fh:
    json.dump(OUT, fh, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else (o.tolist() if isinstance(o, np.ndarray) else str(o)))
print(f"    wrote {os.path.basename(OUTF)}, {os.path.basename(JSONF)}")
print("    kappa = 1/2 FITTED; cold energy mass required; supply per galaxy a postulate; forecasts RECALLED/UNVERIFIED; not theory closed.")
_fh.flush()
sys.exit(0 if npass == len(CHECKS) else 1)
