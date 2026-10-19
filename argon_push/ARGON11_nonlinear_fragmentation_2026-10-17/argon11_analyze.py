#!/usr/bin/env python3
"""ARGON11 analysis.  Criteria: FROZEN_CRITERIA.md (commit 2153ca9e0).  Reads logs/snapshots written by frag3d (outside the repo) and
prints every gate K1-K8 and the M5 mutate reading.  Refuses to run while a 1024^3-type run or an overnight_chain script is alive.
usage: argon11_analyze.py [R1 R2 ...]   (default: all runs that have a finished log)"""
import os, sys, re, glob, json, math, subprocess
import numpy as np
from scipy import ndimage as ndi
from argon11_common import coexistence, growth_curve

HERE = os.path.dirname(os.path.abspath(__file__))
W = "/Users/carlzimmerman/new_physics/_external_data/argon11_work"
M = 100
RUNS = {  # id: (s, N, dx, seed, eps, t_end, Lq_flip) -- identical to argon11_run.py / FROZEN_CRITERIA.md
    "R1": (0.1, 96, 1.0, 1, 1e-4, 700, False), "R2": (0.1, 96, 1.0, 2, 1e-4, 700, False),
    "R3": (0.1, 128, 0.75, 1, 1e-4, 700, False), "R4": (0.5, 96, 1.0, 1, 1e-4, 500, False),
    "R5": (0.1, 64, 1.0, 1, 1e-4, 700, True), "R6": (0.1, 64, 1.0, 1, 1e-4, 700, False),
    "R7": (0.1, 64, 1.0, 1, 1e-6, 800, False), "R8": (0.1, 128, 1.0, 3, 1e-4, 700, False),
}
F2 = {0.1: (1.001e5, 5.385e-3), 0.5: (2.572e5, 3.932e-3)}      # (Q_est, S_F2) from ARGON10 F2 output
hbarc = 197.3269804e-15; MeV_kg = 1.78266192e-30

BUSY = re.compile(r"^(nice(\s+-n\s+\d+)?\s+)?(\S*/)?[Pp]ython[\d.]*\s+(\S*/)?(run_650|run_654|cfg6\d\d_pm|cfg596_pm|cfg7\d\d)(\.py)?(\s|$)")
CHAIN = re.compile(r"^(/bin/)?bash\s+\S*overnight_chain/chain\d+\.sh(\s|$)")
def busy():
    out = subprocess.run(["ps", "-axo", "args="], capture_output=True, text=True).stdout.splitlines()
    return any(BUSY.match(l.strip()) or CHAIN.match(l.strip()) for l in out)

lines = []
def say(s=""):
    print(s); lines.append(s)

def nat_to_cm2g(S):      # S = (sigma/m) m_h^3, m_h = 1 MeV
    return S * hbarc**2 / MeV_kg * 10.0
def cls(x):
    return 'BELOW' if x < 0.105 else ('LOW-EDGE' if x < 0.82 else ('ABOVE-LOW' if x <= 10 else 'EXCLUDED'))

# ---------------------------------------------------------------- logs, K1, K2
def read_log(tag):
    fn = f"{W}/log_{tag}.txt"
    hdr = open(fn).readline()
    I0 = float(re.search(r"I0=([0-9.eE+-]+)", hdr).group(1))
    rows = {}
    for line in open(fn):
        if line.startswith('#') or not line.strip():
            continue
        p = [float(x) for x in line.split()]
        rows[round(p[0], 4)] = p                      # resumed runs repeat a few times: the last entry wins
    return I0, np.array([rows[k] for k in sorted(rows)])   # t Q E Ifl Imax Imean

def k1(arr):
    dQ = np.max(np.abs(arr[:, 1]/arr[0, 1] - 1)); dE = np.max(np.abs(arr[:, 2]/arr[0, 2] - 1))
    return dQ, dE, (dQ <= 1e-6 and dE <= 1e-3)

def k2(I0, arr, Lbox, Lq):
    ks = np.arange(0.01, 1.5, 0.0025)
    g = growth_curve(M, I0, ks, Lq)
    k0 = 2*math.pi/Lbox; jm = int(0.9/k0) + 1; modes = set()
    for a in range(0, jm + 1):
        for b in range(0, a + 1):
            for c in range(0, b + 1):
                if a + b + c > 0:
                    k = k0*math.sqrt(a*a + b*b + c*c)
                    if k < 1.5: modes.add(round(k, 6))
    gp = max(float(np.interp(k, ks, g)) for k in modes)
    if gp <= 1e-10:
        return None, gp, None
    t, Ifl = arr[:, 0], arr[:, 3]
    m = (Ifl/I0 >= 1e-4) & (Ifl/I0 <= 1e-2)
    if m.sum() < 4:
        return float('nan'), gp, False
    gm = np.polyfit(t[m], np.log(Ifl[m]), 1)[0]/2
    return float(gm), gp, abs(gm/gp - 1) <= 0.10

# ---------------------------------------------------------------- lumps
def periodic_label(mask):
    lab, n = ndi.label(mask)
    if n == 0:
        return lab, 0
    parent = np.arange(n + 1)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for ax in range(3):
        a = np.take(lab, 0, axis=ax); b = np.take(lab, -1, axis=ax)
        m = (a > 0) & (b > 0)
        for x, y in set(zip(a[m].tolist(), b[m].tolist())):
            rx, ry = find(x), find(y)
            if rx != ry: parent[rx] = ry
    roots = np.array([find(i) for i in range(n + 1)])
    uniq = np.unique(roots[1:]); remap = np.zeros(n + 1, dtype=int); remap[uniq] = np.arange(1, len(uniq) + 1)
    return remap[roots[lab]], len(uniq)

def aspect(zz, yy, xx, N):
    """principal-axis aspect ratio of a periodic cell set (circular-mean centre, minimum-image displacements)"""
    d = []
    for q in (zz, yy, xx):
        ang = 2*math.pi*q/N; c = math.atan2(np.sin(ang).mean(), np.cos(ang).mean())*N/(2*math.pi)
        d.append(((q - c + N/2) % N) - N/2)
    X = np.vstack(d); C = X @ X.T / X.shape[1]
    ev = np.linalg.eigvalsh(C)
    return float(math.sqrt(max(ev[-1], 1e-12)/max(ev[0], 1e-12)))

def analyze_snapshot(fn, N, dx, Istar, nstar):
    I, n, e = np.fromfile(fn, dtype=np.float32).reshape(3, N, N, N).astype(np.float64)
    dV = dx**3
    Qtot = n.sum()*dV; Etot = e.sum()*dV
    core = I > 0.5*Istar
    lab, nc = periodic_label(core)
    out = dict(Qtot=Qtot, Etot=Etot, f_core=0.0, lumps=[], Imax=float(I.max()))
    if nc == 0:
        return out
    idx = np.arange(1, nc + 1)
    Qcore = ndi.sum(n, lab, idx)*dV
    ncell = ndi.sum(core.astype(np.float64), lab, idx)
    out['f_core'] = float(Qcore.sum()/Qtot)
    P = 6
    labp = np.pad(lab, P, mode='wrap')
    d, ind = ndi.distance_transform_edt(labp == 0, return_indices=True)
    near = labp[ind[0], ind[1], ind[2]][P:-P, P:-P, P:-P]
    dist = d[P:-P, P:-P, P:-P]
    assigned = (near > 0) & (((dist <= 4) & (I > 0.05*Istar)) | core)
    asg = np.where(assigned, near, 0)
    Qf = ndi.sum(n, asg, idx)*dV; Ef = ndi.sum(e, asg, idx)*dV
    nhalo = ndi.sum(((I > 0.1*Istar) & assigned).astype(np.float64), asg, idx)
    zz, yy, xx = np.nonzero(lab); ll = lab[zz, yy, xx]; order = np.argsort(ll)
    zz, yy, xx, ll = zz[order], yy[order], xx[order], ll[order]
    bounds = np.searchsorted(ll, idx)
    bounds = list(bounds) + [len(ll)]
    for j in range(nc):
        if Qcore[j] < 1e3:
            continue
        Vc = ncell[j]*dV; Vh = nhalo[j]*dV
        R = (3*Vc/(4*math.pi))**(1/3); Rh = (3*Vh/(4*math.pi))**(1/3)
        sl = slice(bounds[j], bounds[j + 1])
        out['lumps'].append(dict(Q=float(Qf[j]), Qcore=float(Qcore[j]), E=float(Ef[j]), Vcore=float(Vc), R=float(R), Rh=float(Rh),
                                 n_in=float(Qcore[j]/Vc), EQ=float(Ef[j]/Qf[j]), S=float(4*math.pi*R**2/Qf[j]),
                                 Sh=float(4*math.pi*Rh**2/Qf[j]), asp=aspect(zz[sl], yy[sl], xx[sl], N)))
    return out

def med(lst, key):
    v = [l[key] for l in lst]
    return float(np.median(v)) if v else float('nan')

def run_tag(tag):
    s, N, dx, seed, eps, tend, flip = RUNS[tag]
    Lq = (2 + 1.0/M) if flip else (2 - 1.0/M)
    Istar, w2s = coexistence(M)
    wstar = math.sqrt(w2s); nstar = 2*wstar*Istar
    I0, arr = read_log(tag)
    res = dict(tag=tag, s=s, N=N, dx=dx, Lbox=N*dx, eps=eps)
    dQ, dE, ok1 = k1(arr)
    res['K1'] = dict(dQ=dQ, dE=dE, ok=ok1, t_last=float(arr[-1, 0]))
    gm, gp, ok2 = k2(I0, arr, N*dx, Lq)
    res['K2'] = dict(gamma_meas=gm, gamma_pred=gp, ok=ok2)
    snaps = sorted(glob.glob(f"{W}/snap_{tag}_t*.bin"))
    series = []
    for fn in snaps:
        t = float(re.search(r"_t([0-9.]+)\.bin", fn).group(1))
        a = analyze_snapshot(fn, N, dx, Istar, nstar)
        L = a['lumps']
        fr = 1 - sum(l['E'] for l in L)/a['Etot'] if a['Etot'] else float('nan')
        series.append(dict(t=t, Qtot=a['Qtot'], Etot=a['Etot'], f_core=a['f_core'], Nl=len(L), Imax=a['Imax'],
                           Q_med=med(L, 'Q'), R_med=med(L, 'R'), n_ratio=med(L, 'n_in')/nstar if L else float('nan'),
                           EQ_med=med(L, 'EQ'), S_med=med(L, 'S'), Sh_med=med(L, 'Sh'), asp_med=med(L, 'asp'),
                           f_rad=fr, f_max=1 - wstar*a['Qtot']/a['Etot'], Q_out=1 - sum(l['Q'] for l in L)/a['Qtot'] if a['Qtot'] else float('nan'),
                           nndev=float(np.median([abs(l['n_in']/nstar - 1) for l in L])) if L else float('nan')))
    res['series'] = series
    tA = next((r for r in series if r['f_core'] >= 0.5), None)
    res['tA'] = tA['t'] if tA else None
    res['At_tA'] = tA
    res['At_end'] = series[-1] if series else None
    if tA:
        res['K3'] = dict(N=tA['Nl'], nndev=tA['nndev'], EQ=tA['EQ_med'],
                         FRAGMENTS=bool(tA['Nl'] >= 3 and tA['nndev'] <= 0.25 and tA['EQ_med'] < 1))
        Qe, Sf = F2[s] if s in F2 else (float('nan'), float('nan'))
        res['K4'] = dict(r_Q=tA['Q_med']/Qe, r_S=tA['S_med']/Sf,
                         SURVIVES=bool(1/3 <= tA['Q_med']/Qe <= 3 and 1/3 <= tA['S_med']/Sf <= 3))
    else:
        res['K3'] = dict(FRAGMENTS=False, reason='no epoch with >= 50% of the charge in cores')
        res['K4'] = None
    return res, wstar, nstar

def show(res, wstar, nstar):
    tag = res['tag']
    say(f"\n== {tag}: s={res['s']} N={res['N']} dx={res['dx']} L_box={res['Lbox']:g} eps={res['eps']:g} (run to t={res['K1']['t_last']:.1f}) ==")
    k = res['K1']; say(f"  K1 conservation: max|dQ/Q|={k['dQ']:.2e}  max|dE/E|={k['dE']:.2e}  {'PASS' if k['ok'] else 'FAIL'}")
    k = res['K2']
    if k['gamma_meas'] is None:
        say(f"  K2 linear stage: not applicable (gamma_pred={k['gamma_pred']:.1e} <= 1e-10)")
    else:
        say(f"  K2 linear stage: gamma_meas={k['gamma_meas']:.5f} vs gamma_pred={k['gamma_pred']:.5f}  {'PASS' if k['ok'] else 'FAIL'}")
    say(f"  {'t':>6} {'f_core':>7} {'N_lump':>6} {'Q_med':>10} {'R_eff':>6} {'n/n*':>6} {'E/Q':>6} {'S_core':>10} {'S_0.1':>10} {'asp':>5} {'f_rad':>6} {'f_max':>6} {'Q_out':>6}")
    for r in res['series']:
        say(f"  {r['t']:6.0f} {r['f_core']:7.3f} {r['Nl']:6d} {r['Q_med']:10.3e} {r['R_med']:6.2f} {r['n_ratio']:6.3f} {r['EQ_med']:6.3f} {r['S_med']:10.3e} {r['Sh_med']:10.3e} {r['asp_med']:5.2f} {r['f_rad']:6.3f} {r['f_max']:6.3f} {r['Q_out']:6.3f}")
    say(f"  omega* = {wstar:.4f}   n* = {nstar:.2f}")
    k = res['K3']
    if res['tA'] is None:
        say(f"  K3: NO STABLE FRAGMENTS ({k.get('reason')})")
    else:
        say(f"  t_A = {res['tA']:.0f}:  K3 {'FRAGMENTS' if k['FRAGMENTS'] else 'NO STABLE FRAGMENTS'}   (N_lump={k['N']}, median|n_in/n*-1|={k['nndev']:.3f}, median E/Q={k['EQ']:.3f})")
        k4 = res['K4']
        say(f"  K4 vs ARGON10 F2 at t_A: r_Q={k4['r_Q']:.2f}, r_S={k4['r_S']:.2f}  ->  F2 estimate {'SURVIVES' if k4['SURVIVES'] else 'REVISED'}")
        for label, r in (("t_A", res['At_tA']), ("t_end", res['At_end'])):
            row = []
            for eps in (1.0, 1e-3, 1e-6):
                v = nat_to_cm2g(r['S_med']*eps); vh = nat_to_cm2g(r['Sh_med']*eps)
                row.append(f"eps={eps:.0e}: {v:.3g} ({cls(v)}) / halo {vh:.3g}")
            say(f"  sigma/m at {label} (m_h = 1 MeV, cm2/g): " + " | ".join(row))

def rel(a, b):
    return abs(a/b - 1) if b else float('nan')

def main():
    if busy() and os.environ.get("ARGON11_ALLOW_BESIDE") != "1":      # owner 2026-10-18: light analysis may run beside T2x (1 core, nice 19)
        print("a 1024^3-type run or an overnight_chain script is alive: not computing (rule). Exiting."); sys.exit(3)
    tags = sys.argv[1:] or [t for t in RUNS if os.path.exists(f"{W}/log_{t}.txt")]
    allres = {}
    say("ARGON11 analysis   criteria 2153ca9e0")
    for t in tags:
        res, wstar, nstar = run_tag(t)
        allres[t] = res; show(res, wstar, nstar)
    # ---- K5 / K6 cross-run comparisons
    def pair(a, b, label):
        if a in allres and b in allres and allres[a]['At_tA'] and allres[b]['At_tA']:
            A, B = allres[a], allres[b]
            d = dict(tA=rel(A['tA'], B['tA']), N=rel(A['At_tA']['Nl'], B['At_tA']['Nl']), Q=rel(A['At_tA']['Q_med'], B['At_tA']['Q_med']),
                     S=rel(A['At_tA']['S_med'], B['At_tA']['S_med']))
            ok = d['tA'] <= 0.10 and d['N'] <= 0.30 and d['Q'] <= 0.30 and d['S'] <= 0.30
            say(f"  {label} ({a} vs reference {b}): |dt_A|={d['tA']:.2f} |dN|={d['N']:.2f} |dQ_med|={d['Q']:.2f} |dS_med|={d['S']:.2f}  -> {'OK' if ok else 'outside 10/30/30/30 %'}")
            return ok
        say(f"  {label}: not available"); return None
    say("\n== K5 convergence (differences relative to R1) ==")
    c_res = pair("R3", "R1", "resolution"); c_seed = pair("R2", "R1", "seed"); pair("R8", "R1", "box size (reported only)")
    if c_res is None or c_seed is None:
        say("  K5: incomplete")
    else:
        say(f"  K5: {'CONVERGED' if (c_res and c_seed) else 'NOT CONVERGED -> quote ranges over runs'}")
    say("\n== K6 amplitude (R6 eps=1e-4 vs R7 eps=1e-6; informative) ==")
    if "R6" in allres and "R7" in allres and allres["R6"]['At_tA'] and allres["R7"]['At_tA']:
        q6, q7 = allres["R6"]['At_tA']['Q_med'], allres["R7"]['At_tA']['Q_med']
        f = max(q6, q7)/min(q6, q7)
        say(f"  Q_med(t_A): {q6:.3e} vs {q7:.3e}; ratio {f:.2f}; t_A {allres['R6']['tA']:.0f} vs {allres['R7']['tA']:.0f}  -> {'within 1.5' if f <= 1.5 else 'outside 1.5'}")
    else:
        say("  not available")
    say("\n== MUTATE M5 (R5: net quartic repulsive) ==")
    if "R5" in allres:
        r5 = allres["R5"]
        bites = r5['tA'] is None and (r5['K2']['gamma_meas'] is None)
        say(f"  gamma_pred={r5['K2']['gamma_pred']:.1e}; lumps at any snapshot: {max((x['Nl'] for x in r5['series']), default=0)}; t_A={r5['tA']}  ->  {'bites' if bites else 'DOES NOT BITE'}")
    else:
        say("  R5 not run")
    with open(os.path.join(HERE, "argon11_analysis.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(HERE, "argon11_results.json"), "w") as fh:
        json.dump(allres, fh, indent=1, default=float)

if __name__ == "__main__":
    main()
