#!/usr/bin/env python3
"""QX2 clusters (criteria 2f84fed672): every static term of v3s / AC2q graded on X-COP (gate G-X).
    python3 qx2.py            # graded, writes qx2.json / qx2.out
    python3 qx2.py --mutate   # each iteration's MUTATE, writes qx2_MUTATE.json / .out
X-COP builder copied in content from rebuild_2026_10_22/LW1_law_scorecard/lw1_xcop.py (CS2's builder).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv; TAG = "qx2_MUTATE" if MUT else "qx2"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

G, MS, PC, C = 6.674e-11, 1.989e30, 3.0857e16, 2.99792458e8
KPC, MPC = 1e3 * PC, 1e6 * PC
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
KAPPA = 0.5
XS = (0.1, 0.2, 0.3, 0.5, 0.7)

def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))

R5J = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
XC = []
for name in sorted(os.listdir(os.path.join(DATA, "xcop"))):
    p_ = os.path.join(DATA, "xcop", name)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    rows = []
    for x in XS:
        r = x * r500; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(gas["RADIUS"] * rg500, gas["MGAS"], r); ms = li(st["RADIUS"], st["MSTAR"], r)
        em = li(hm["RADIUS"], hm["EM_FORW"], r)
        if np.all(np.isfinite([mh, mg, ms])): rows.append(dict(x=x, r_kpc=r, M_HSE=mh, M_b=mg + ms, eM=em))
    XC.append(dict(name=name, rows=rows, hm=hm, r500=r500, R200_kpc=1e3 * R5J[name]["R200"] if name in R5J else 1.5 * r500))

def law_M(Mb_msun, r_kpc, a0):
    r = r_kpc * KPC; gN = G * Mb_msun * MS / r ** 2
    g = 0.5 * gN + math.sqrt(0.25 * gN ** 2 + a0 * gN); return g * r ** 2 / G / MS, gN, g

def gate(model):  # model(cluster, row, a0) -> M_model [Msun]
    res = {}
    for f, a0 in A0.items():
        d, se = [], []
        for c in XC:
            for z in c["rows"]:
                d.append(math.log10(z["M_HSE"] / model(c, z, a0))); se.append(z["eM"] / z["M_HSE"] / math.log(10))
        d = np.array(d); se = np.array(se); sem = float(np.sqrt((se ** 2).sum()) / len(se))
        res[f] = dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d), sem_stat=sem,
                      PASS=bool(abs(d.mean()) <= 0.05 and np.sqrt((d ** 2).mean()) <= 0.10),
                      fail_significant=bool(abs(d.mean()) > 0.05 + 5 * sem))
    return res

def show(tag, R):
    for f, r in R.items():
        P(f"  [{f}] {tag}: mean {r['mean']:+.4f}, rms {r['rms']:.4f}, n {r['n']}, stat sem {r['sem_stat']:.4f} -> {'PASS' if r['PASS'] else 'FAIL'}"
          + ("" if r["PASS"] else f" (significant: {r['fail_significant']})"))

OUTJ = dict(tag=TAG, clusters=[c["name"] for c in XC], note="kappa = 1/2 FITTED; not theory closed")
P(f"QX2 {TAG}: X-COP {len(XC)} clusters, {sum(len(c['rows']) for c in XC)} points; Delta = log10(M_HSE/M_model), + = model short; gate |mean| <= 0.05, rms <= 0.10")

# ---------- iter 1: plain law ----------
a0m = 1.5 if MUT else 1.0
I1 = gate(lambda c, z, a0: law_M(z["M_b"], z["r_kpc"], a0 * a0m)[0])
P("ITER 1 plain law" + (" [MUTATE a0 x 1.5]" if MUT else "")); show("law", I1)
LW1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "LW1_law_scorecard", "lw1_xcop.json")))
if not MUT:
    k = {f: max(abs(I1[f]["mean"] - LW1[f]["fits"]["mean"]), abs(I1[f]["rms"] - LW1[f]["fits"]["rms"])) for f in A0}
    P(f"  K-LW1 |d| vs LW1 fits builder: {k} -> {'PASS' if max(k.values()) <= 1e-3 else 'FAIL'}"); OUTJ["K_LW1"] = k
else:
    mv = {f: I1[f]["mean"] - LW1[f]["fits"]["mean"] for f in A0}; P(f"  MUTATE moves mean by {mv} (must be <= -0.03: {'BITES' if max(mv.values()) <= -0.03 else 'NO BITE'})"); OUTJ["I1_mut_move"] = mv
OUTJ["iter1"] = I1

# ---------- iter 2: universal nu from SPARC ----------
def sparc_rar():
    Q, INC = {}, {}
    for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        t = ln.split()
        if len(t) < 18: continue
        try: nm = t[0]; inc = float(t[5]); q = int(t[17])
        except ValueError: continue
        Q[nm] = q; INC[nm] = inc
    pts = []
    for fn in os.listdir(os.path.join(DATA, "sparc_data")):
        if not fn.endswith("_rotmod.dat"): continue
        nm = fn[:-11]
        if nm not in Q or Q[nm] > 2 or INC[nm] < 30: continue
        a = np.loadtxt(os.path.join(DATA, "sparc_data", fn), comments="#")
        if a.ndim == 1: a = a[None]
        R, V, eV, Vg, Vd, Vb = a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5]
        vb2 = np.sign(Vg) * Vg ** 2 + 0.5 * np.sign(Vd) * Vd ** 2 + 0.7 * np.sign(Vb) * Vb ** 2
        ok = (V > 0) & (eV / np.maximum(V, 1e-9) <= 0.1) & (vb2 > 0) & (R > 0)
        r = R[ok] * KPC; pts += list(zip((vb2[ok] * 1e6 / r), (V[ok] ** 2 * 1e6 / r)))
    return np.array(pts)
RAR = sparc_rar(); P(f"ITER 2 universal nu: SPARC points after cuts {len(RAR)}")
I2 = {}
for f, a0 in A0.items():
    ly = np.log10(RAR[:, 0] / a0); ln_ = np.log10(RAR[:, 1] / RAR[:, 0])
    edges = np.arange(math.floor(ly.min() * 10) / 10, ly.max() + 0.1, 0.1); cen, med = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (ly >= lo) & (ly < hi)
        if m.sum() >= 20: cen.append(0.5 * (lo + hi)); med.append(float(np.median(ln_[m])))
    cen, med = np.array(cen), np.array(med)
    def nuS(y):
        l = math.log10(y)
        if l < cen[0] or l > cen[-1]: return None
        return 10 ** float(np.interp(l, cen, med))
    mult = 3.0 if MUT else 1.0
    d, outside, Eb = [], 0, {}
    for c in XC:
        for z in c["rows"]:
            gN = G * z["M_b"] * MS / (z["r_kpc"] * KPC) ** 2; y = gN / a0; nv = nuS(y)
            need = math.log10(z["M_HSE"] / z["M_b"])
            if nv is None: outside += 1; continue
            d.append(math.log10(z["M_HSE"] / (z["M_b"] * nv * mult)))
            b = round(math.floor(math.log10(y) * 10) / 10, 1); Eb.setdefault(b, []).append(need - math.log10(nv * mult))
    d = np.array(d)
    E = {f"{b:+.1f}": dict(n=len(v), E=float(np.median(v))) for b, v in sorted(Eb.items()) if len(v) >= 3}
    dead = bool(E) and all(e["E"] > 0.15 for e in E.values())
    I2[f] = dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d), outside=outside, PASS=bool(abs(d.mean()) <= 0.05 and np.sqrt((d ** 2).mean()) <= 0.10),
                 sparc_y_range=[float(10 ** cen[0]), float(10 ** cen[-1])], excess_by_bin=E, class_DEAD=dead, min_bin_excess=min(e["E"] for e in E.values()) if E else None)
    r = I2[f]; P(f"  [{f}] nu_SPARC{' x3 [MUTATE]' if MUT else ''} on X-COP: mean {r['mean']:+.4f}, rms {r['rms']:.4f}, n {r['n']} (outside SPARC y {outside}) -> {'PASS' if r['PASS'] else 'FAIL'}; "
                f"SPARC y in [{r['sparc_y_range'][0]:.3g}, {r['sparc_y_range'][1]:.3g}]; bin excess min {r['min_bin_excess']:+.3f} over {len(E)} bins -> class {'DEAD' if dead else 'not dead'}")
    P("     bins: " + ", ".join(f"{k}:{v['E']:+.2f}(n{v['n']})" for k, v in E.items()))
OUTJ["iter2"] = I2

# ---------- iter 3: clock source ----------
rmult = 1e4 if MUT else 1.0
def rho_de(a0): return a0 ** 2 / (KAPPA ** 2 * C ** 2 * G)  # kg/m^3
def m3(c, z, a0):
    Ms = 4 * math.pi / 3 * (z["r_kpc"] * KPC) ** 3 * 4 * rho_de(a0) * rmult / MS
    z.setdefault("_Ms", {})[a0] = Ms
    return law_M(z["M_b"] + Ms, z["r_kpc"], a0)[0]
I3 = gate(m3); P(f"ITER 3 clock source (<= 4 rho_DE){' [MUTATE rho_DE x 1e4]' if MUT else ''}; rho_DE canonical {rho_de(A0['canonical']):.3e}, alt {rho_de(A0['alt']):.3e} kg/m^3")
show("law + clock", I3)
for f, a0 in A0.items():
    sh = max(c["rows"][-1]["_Ms"][a0] / c["rows"][-1]["M_b"] for c in XC); I3[f]["max_Ms_over_Mb"] = sh; P(f"  [{f}] largest M_s/M_b (x 0.7): {sh:.3e}; gamma s^2 corrections <= 4.0e-17 relative (AC9), not added")
OUTJ["iter3"] = I3

# ---------- iter 4: switched stiffness ----------
LST = 90 * PC * (1e4 if MUT else 1.0)
def m4(c, z, a0):
    ML, gN, g = law_M(z["M_b"], z["r_kpc"], a0); x = g / a0; k = 10 / (z["r_kpc"] * KPC)
    bnd = (LST ** 2 * k ** 2 / 2) / x; z.setdefault("_b4", {})[a0] = bnd
    return z["M_b"] + (ML - z["M_b"]) * (1 + bnd)
I4 = gate(m4); P(f"ITER 4 stiffness bound (Lstar {LST / PC:.3g} pc, k = 10/r){' [MUTATE]' if MUT else ''}"); show("law + stiffness bound", I4)
for f, a0 in A0.items():
    b = max(z["_b4"][a0] for c in XC for z in c["rows"]); I4[f]["max_rel_bound"] = b; P(f"  [{f}] largest relative change of phantom mass: {b:.3e}")
OUTJ["iter4"] = I4

# ---------- iter 5: K(Q) dust ----------
def psi_profile(c):  # potential of the measured HSE mass, zero at 3 R200 (power-law tail beyond the data)
    hm = c["hm"]; r = np.array(hm["RADIUS"], float); M = np.array(hm["M_FORW"], float)
    rmax = 3 * c["R200_kpc"]; rr = np.geomspace(1.0, rmax, 4000)
    lr, lm = np.log10(r), np.log10(M); sl = (lm[-1] - lm[-6]) / (lr[-1] - lr[-6])
    Mr = np.where(rr <= r[-1], 10 ** np.interp(np.log10(rr), lr, lm), M[-1] * (rr / r[-1]) ** sl)
    Mr = np.where(rr < r[0], M[0] * (rr / r[0]) ** 3, Mr)
    gacc = G * Mr * MS / (rr * KPC) ** 2
    seg = 0.5 * (gacc[1:] + gacc[:-1]) * np.diff(rr * KPC)
    psi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])  # psi(r) = -Int_r^rmax g dr
    return rr, psi
for c in XC:
    rr, psi = psi_profile(c); integ = np.concatenate([[0.0], np.cumsum(0.5 * (np.abs(psi[1:]) * (rr[1:] * KPC) ** 2 + np.abs(psi[:-1]) * (rr[:-1] * KPC) ** 2) * np.diff(rr * KPC))])
    c["_IK"] = (rr, integ)  # Int_0^r |psi| r^2 dr  [m^5/s^2]
def MK(c, r_kpc, muK_per_mpc):
    rr, integ = c["_IK"]; mu = muK_per_mpc / MPC
    return mu ** 2 / G * float(np.interp(r_kpc, rr, integ)) / MS
MUK = 10.0 if MUT else 0.1
I5 = gate(lambda c, z, a0: law_M(z["M_b"], z["r_kpc"], a0)[0] + MK(c, z["r_kpc"], MUK)); P(f"ITER 5 K(Q) dust, mu_K = {MUK} Mpc^-1 (generous: HSE potential, no back-reaction){' [MUTATE BS cap]' if MUT else ''}")
show("law + K(Q) dust", I5)
if not MUT:
    for f, a0 in A0.items():
        def mean_at(mu):
            return float(np.mean([math.log10(z["M_HSE"] / (law_M(z["M_b"], z["r_kpc"], a0)[0] + MK(c, z["r_kpc"], mu))) for c in XC for z in c["rows"]]))
        lo, hi = 0.1, 1e3
        for _ in range(80):
            mid = math.sqrt(lo * hi); lo, hi = (mid, hi) if mean_at(mid) > 0 else (lo, mid)
        mid = math.sqrt(lo * hi); rr_ = gate(lambda c, z, a: law_M(z["M_b"], z["r_kpc"], a)[0] + MK(c, z["r_kpc"], mid))[f]
        I5[f]["muK_for_mean0"] = mid; I5[f]["rms_at_muK_mean0"] = rr_["rms"]
        P(f"  [{f}] REPORTED: mu_K for mean 0 = {mid:.3f} Mpc^-1 = {mid / 0.1:.1f} x the galaxy bound 0.1 (BS cap 10); rms there {rr_['rms']:.3f}")
OUTJ["iter5"] = I5

# ---------- closing ----------
allfail = all(not OUTJ[f"iter{i}"][f]["PASS"] for i in range(1, 6) for f in A0)
OUTJ["door_label"] = "FAIL (action on the table: no static term of v3s/AC2q supplies X-COP's mass)" if (allfail and not MUT) else ("MUTATE run" if MUT else "a term passes G-X: later gates owed")
P(f"DOOR: {OUTJ['door_label']}")
json.dump(OUTJ, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
