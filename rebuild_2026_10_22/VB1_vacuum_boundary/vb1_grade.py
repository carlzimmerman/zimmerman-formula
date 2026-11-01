#!/usr/bin/env python3
"""VB1_vacuum_boundary (FROZEN_CRITERIA.md): same-seed 1e14 ng 48 pair, A (--rs 1.5) against B (--rs 2.0), both continued to z = 0 unchanged.
Statistic: f_out = DeltaSigma_B / DeltaSigma_A in 2.18-3.17 R500 (R500 of run A, 500 rho_c at z = 0 on the native background, as zn1_measure's R200),
f_in = M_B(< 0.7 R500) / M_A(< 0.7 R500). DeltaSigma from the particles directly: three axis projections averaged, M_cyl(< R)/(pi R^2) - Sigma(R) in
eight log annuli across the band. Checks K1-K4, MUTATE (run A's R500 x 1.5). Also writes shape tables (ZN1's measure(), same x grid) for the
post-result key read (vb1_keys.py). ZN1's and X48's files are read only.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -I vb1_grade.py
kappa = 1/2 FITTED; footings never pooled; cold dark energy is a gravitating field component, never a particle; not theory closed."""
import importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN1_zooms_to_z0")
_s = importlib.util.spec_from_file_location("zn1_measure", os.path.join(ZD, "zn1_measure.py")); ZM = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = [_a[0]]; _s.loader.exec_module(ZM); sys.argv = _a
measure, XA, XG, rho_c = ZM.measure, ZM.XA, ZM.XG, ZM.rho_c
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def load(sub, rs, name):
    Z = np.load(os.path.join(HERE, sub, f"M1e14_s1_ng48_rs{rs}", name), allow_pickle=False); return Z["x"], float(Z["m"]), json.loads(str(Z["meta"]))
P("VB1 grade: vacuum boundary, 1e14 seed 1 ng 48, RS 1.5 (A) against 2.0 (B); kappa = 1/2 FITTED; not theory closed")
xA, mA, metaA = load("runs", "1.5", "snap_z0.00.npz"); xB, mB, metaB = load("runs", "2.0", "snap_z0.00.npz")
# K1: run A's collapse equals X48's ng 48 seed-1 1e14 run (same code, same flags)
X48 = np.load(os.path.join(RB, "X48_native_cf_zoom", "runs", "M1e14_s1_ng48", "snap_zf.npz"), allow_pickle=False); zfA = np.load(os.path.join(HERE, "runs_zf", "M1e14_s1_ng48_rs1.5", "snap_zf.npz"), allow_pickle=False)
k1_dx = float(np.abs(X48["x"] - zfA["x"]).max()) if X48["x"].shape == zfA["x"].shape else float("inf")
mX, mV = (measure(X48["x"], float(X48["m"]), json.loads(str(X48["meta"]))["zf"], json.loads(str(X48["meta"]))["eps"]), measure(zfA["x"], float(zfA["m"]), json.loads(str(zfA["meta"]))["zf"], json.loads(str(zfA["meta"]))["eps"])) if np.isfinite(k1_dx) else (None, None)
k1_dm = float(np.abs(np.array(mX["lnm"]) - np.array(mV["lnm"])).max()) if mX else float("inf"); k1 = k1_dx <= 1e-6 and k1_dm <= 1e-6
P(f"  K1 run A z_f against X48 M1e14_s1_ng48: max |dx| {k1_dx:.1e} Mpc, max |d ln m(x)| {k1_dm:.1e}: {'PASS' if k1 else 'FAIL'}")
k2 = abs(metaA["mpart"] / metaB["mpart"] - 1) <= 1e-12 and mA == mB; P(f"  K2 particle mass A {metaA['mpart']:.6e} B {metaB['mpart']:.6e}: {'PASS' if k2 else 'FAIL'}")
k3 = metaA["eps"] == metaB["eps"]; P(f"  K3 softening A {metaA['eps']:.6e} B {metaB['eps']:.6e}: {'PASS' if k3 else 'FAIL'}")
k4r = len(xB) / len(xA); k4 = abs(k4r / (2.0 / 1.5) ** 3 - 1) <= 0.03; P(f"  K4 N_B/N_A {k4r:.4f} against (2.0/1.5)^3 {(2.0/1.5)**3:.4f} ({k4r/(2.0/1.5)**3-1:+.2%}): {'PASS' if k4 else 'FAIL'}")
if not (k1 and k2 and k3 and k4): P("  a check failed: no grade"); open(os.path.join(HERE, "vb1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
oA = measure(xA, mA, 0.0, metaA["eps"]); oB = measure(xB, mB, 0.0, metaB["eps"])
def r500(o):
    thr = 500 * rho_c(0.0); dens = o["Menc"] / (4 / 3 * math.pi * o["r"] ** 3); i = int(np.where(dens >= thr)[0].max())
    return float(math.exp(np.interp(math.log(thr), [math.log(dens[i + 1]), math.log(dens[i])], [math.log(o["r"][i + 1]), math.log(o["r"][i])])))
R5A, R5B = r500(oA), r500(oB)
P(f"  run A: R200 {oA['R200']:.4f} Mpc, lg M200 {math.log10(oA['M200']):.3f}, R500 {R5A:.4f}, x_edge {oA['x_edge']:.2f}; run B: R200 {oB['R200']:.4f}, lg M200 {math.log10(oB['M200']):.3f}, R500 {R5B:.4f}, x_edge {oB['x_edge']:.2f}")
P(f"  band 2.18-3.17 R500(A) = {2.18*R5A:.3f}-{3.17*R5A:.3f} Mpc = {2.18*R5A/oA['R200']:.2f}-{3.17*R5A/oA['R200']:.2f} R200(A); run A holds mass to {oA['x_edge']*oA['R200']:.2f} Mpc (90 % radius)")
def dsig(x, m, R5, nann=8):
    """mean DeltaSigma over the band, three axis projections; returns (mean, Poisson sigma)"""
    c = XA.centre(x, m); d = x - c; E = np.geomspace(2.18 * R5, 3.17 * R5, nann + 1); Rc = np.sqrt(E[:-1] * E[1:]); vals = []; var = []
    for ax in range(3):
        R = np.sqrt(np.delete(d, ax, axis=1).__pow__(2).sum(1)); Rs = np.sort(R)
        ncyl = np.searchsorted(Rs, Rc); nann_ = np.diff(np.searchsorted(Rs, E)); Sig = nann_ * m / (math.pi * (E[1:] ** 2 - E[:-1] ** 2)); Sbar = ncyl * m / (math.pi * Rc ** 2)
        vals.append(Sbar - Sig); var.append((m / (math.pi * (E[1:] ** 2 - E[:-1] ** 2))) ** 2 * nann_ + (m / (math.pi * Rc ** 2)) ** 2 * ncyl)
    v = np.array(vals); return float(v.mean()), float(math.sqrt(np.array(var).mean(0).sum()) / nann), v.mean(0).tolist()
def menc(o, r): return float(np.interp(r, o["r"], o["Menc"]))
def stat(R5):
    dA, eA, pA = dsig(xA, mA, R5); dB, eB, pB = dsig(xB, mB, R5); fo = dB / dA; so = fo * math.hypot(eA / dA, eB / dB)
    fi = menc(oB, 0.7 * R5) / menc(oA, 0.7 * R5); return dict(dsA=dA, dsB=dB, f_out=fo, f_out_sig=so, f_in=fi, prof_A=pA, prof_B=pB)
S = stat(R5A)
P(f"  DeltaSigma in the band: A {S['dsA']:.4e}, B {S['dsB']:.4e} Msun/Mpc^2; f_out {S['f_out']:.4f} +- {S['f_out_sig']:.4f} (shot); M(< 0.7 R500) A {menc(oA, 0.7*R5A):.4e}, B {menc(oB, 0.7*R5A):.4e}: f_in {S['f_in']:.4f}")
P("  per-annulus f_out: " + ", ".join(f"{b/a:.3f}" for a, b in zip(S["prof_A"], S["prof_B"])))
for rr in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0): P(f"    M_B/M_A (< {rr} R200_A = {rr*oA['R200']:.2f} Mpc): {menc(oB, rr*oA['R200'])/menc(oA, rr*oA['R200']):.4f}")
V = "PASS (BOUNDARY MATTERS)" if (S["f_out"] >= 1.28 and abs(S["f_in"] - 1) <= 0.04) else "FAIL (NOT A BOUNDARY ARTEFACT)" if S["f_out"] < 1.15 else "MIXED"
P(f"  VERDICT as frozen: {V}   (PASS f_out >= 1.28 and |f_in - 1| <= 0.04; FAIL f_out < 1.15; else MIXED)")
P(f"  predictions on record: Argon f_out 1.18-1.24 -> {'HIT' if 1.18 <= S['f_out'] <= 1.24 else 'MISS'}; this session 1.05-1.15 and f_in within 2 % -> {'HIT' if 1.05 <= S['f_out'] <= 1.15 and abs(S['f_in']-1) <= 0.02 else 'MISS'}")
SM = stat(1.5 * R5A); mut = abs(SM["f_out"] / S["f_out"] - 1) > 0.10
P(f"  MUTATE R500(A) x 1.5 (band {2.18*1.5:.2f}-{3.17*1.5:.2f} R500): f_out {SM['f_out']:.4f} ({SM['f_out']/S['f_out']-1:+.1%}): {'BITES' if mut else 'DOES NOT BITE, STOP'}")
# shape tables for the post-result key read: ZN1's measure() at z 0.5, 0.25, 0 for A and B, in zn1_shapes.json's layout
for tag, rs in (("A", "1.5"), ("B", "2.0")):
    T = {}
    for zs in ("0.50", "0.25", "0.00"):
        x, m, meta = load("runs", rs, f"snap_z{zs}.npz"); o = measure(x, m, float(zs), meta["eps"])
        T[zs] = dict(n=1, lgM=math.log10(o["M200"]), x_edge=o["x_edge"], lnm=o["lnm"], seeds=[dict(seed=f"M1e14_s1_ng48_rs{rs}", lgM=math.log10(o["M200"]), R200=o["R200"], x_conv=o["x_conv"], x_edge=o["x_edge"], lnm=o["lnm"])], x=XG.tolist())
    json.dump(T, open(os.path.join(HERE, f"vb1_shape_{tag}.json"), "w"))
res = dict(checks=dict(K1=k1, K2=k2, K3=k3, K4=k4, k1_dx=k1_dx, k1_dlnm=k1_dm, N_ratio=k4r), runA=dict(R200=oA["R200"], M200=oA["M200"], R500=R5A, x_edge=oA["x_edge"]), runB=dict(R200=oB["R200"], M200=oB["M200"], R500=R5B, x_edge=oB["x_edge"]), stat=S, mutate=dict(stat=SM, bites=mut), verdict=V)
json.dump(res, open(os.path.join(HERE, "vb1_results.json"), "w"), indent=1); open(os.path.join(HERE, "vb1.out"), "w").write("\n".join(OUT) + "\n")
P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework")
