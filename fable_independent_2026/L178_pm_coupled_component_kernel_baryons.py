#!/usr/bin/env python3
"""L178 -- SELF-CONSISTENT PM RUN: baryons + a cold dark component with time-dependent coupling g(a) = 1 - (1-g0) a^n, kernel (nu_RAR, canonical
a0) reading the BARYONS ONLY, dark component Newtonian with weight g(a); both species fall in the total potential. Same PM code/ICs/box
as L176 (reference LCDM run reused from L176_pk_results.json). Output: lensing-mass power (Ob db + g Oc dd) and baryon power relative
to the same-code LCDM. No literal-True checks."""
import numpy as np, json, sys, os, time
from multiprocessing import Pool
from L176_framework_pk_baseline import (poisson, grad, div, cic_deposit, cic_interp, pk, make_ics, Hnorm, A0, Om, Ob, Oc, L, NG, NP, ZI)
def run2(cfg):
    name, g0, n, kernel_on_baryons = cfg
    a0 = A0["canonical"]; g = lambda a: 1 - (1 - g0)*a**n
    x, p, _ = make_ics(); xb, pb = x.copy(), p.copy(); xd, pd = x.copy(), p.copy()      # identical ICs for both species
    npart = len(x); wb, wd = Ob/Om, Oc/Om
    def accel(xb, xd, a):
        rb = cic_deposit(xb, np.full(npart, 1.0))*NG**3/npart; rd = cic_deposit(xd, np.full(npart, 1.0))*NG**3/npart
        phiNb = poisson(1.5*Om*wb*(rb - 1)/a)
        phid = poisson(1.5*Om*g(a)*wd*(rd - 1)/a)
        if kernel_on_baryons:
            gN = [-gg/a**2 for gg in grad(phiNb)]; mag = np.sqrt(sum(gg**2 for gg in gN)) + 1e-30
            nu = 1.0/(1.0 - np.exp(-np.sqrt(mag/a0)))
            phi = poisson(div([nu*gg for gg in grad(phiNb)])) + phid
        else:
            phi = phiNb + phid
        gr = grad(phi)
        acc = lambda xx: -np.stack([cic_interp(gg, xx) for gg in gr], 1)
        return acc(xb), acc(xd), rb, rd
    a = 1/(1 + ZI); dlna = 0.02; zs_out = [3.0, 1.0, 0.5, 0.0]; out = {}
    ab, ad, rb, rd = accel(xb, xd, a)
    while a < 1.0:
        da = a*(np.exp(dlna) - 1); dt = da/(a*Hnorm(a))
        pb += 0.5*dt*ab; pd += 0.5*dt*ad
        xb = (xb + dt*pb/a**2) % L; xd = (xd + dt*pd/a**2) % L
        a = a + da
        ab, ad, rb, rd = accel(xb, xd, a)
        pb += 0.5*dt*ab; pd += 0.5*dt*ad
        for z in list(zs_out):
            if 1/a - 1 <= z + 1e-9:
                lens = (wb*(rb - 1) + g(a)*wd*(rd - 1))          # coupled-mass contrast in units of the total LCDM mean
                out[str(z)] = {"lens": pk(lens).tolist(), "bary": pk(rb - 1).tolist(), "g": float(g(a))}; zs_out.remove(z)
    return name, out
if __name__ == "__main__":
    T0 = time.time()
    cfgs = [("g058_n4_kb", 0.58, 4, True), ("g058_n2_kb", 0.58, 2, True), ("g1_kb", 1.0, 4, True), ("g058_n4_newton", 0.58, 4, False)]
    if not os.path.exists("L178_results.json") or "--rerun" in sys.argv:
        with Pool(4) as pool: res = dict(pool.map(run2, cfgs))
        json.dump(res, open("L178_results.json", "w")); print(f"    runs done in {time.time()-T0:.0f}s", flush=True)
    res = json.load(open("L178_results.json")); ref = json.load(open("L176_pk_results.json"))["LCDM_newton"]
    CH = []
    def check(n_, ok, d=""):
        CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n_}" + (f"\n           ({d})" if d else ""))
    kk = np.array(ref["3.0"])[:, 0]; mS = (kk >= 0.15) & (kk <= 0.5); mSh = (kk >= 0.3) & (kk <= 2.0); mF = (kk >= 1.0) & (kk <= 4.0)
    print("    ratio to same-code LCDM; S8 proxy = sqrt(mean lensing ratio at 0.15-0.5 h/Mpc, z=0) x 0.8415 (LCDM S8)")
    print(f"    {'run':<16} {'g(z=0)':>6} {'forest z=3 (bary)':>18} {'shear z=0.5 (lens)':>19} {'lens z=0 0.15-0.5':>18} {'S8 proxy':>9}")
    S8p = {}
    for name in res:
        r = res[name]; f3 = np.array(r["3.0"]["bary"])[:, 1]/np.array(ref["3.0"])[:, 1]
        s05 = np.array(r["0.5"]["lens"])[:, 1]/np.array(ref["0.5"])[:, 1]; l0 = np.array(r["0.0"]["lens"])[:, 1]/np.array(ref["0.0"])[:, 1]
        S8p[name] = 0.8415*np.sqrt(np.mean(l0[mS]))
        print(f"    {name:<16} {r['0.0']['g']:6.2f} {f3[mF].min():8.2f}-{f3[mF].max():<8.2f} {s05[mSh].min():9.2f}-{s05[mSh].max():<8.2f} {l0[mS].min():8.2f}-{l0[mS].max():<8.2f} {S8p[name]:9.3f}")
    check("P1 control: full coupling (g = 1) with the kernel reading baryons only OVERSHOOTS LCDM lensing power today (the kernel adds on top of a full CDM budget)", S8p["g1_kb"] > 0.8415*1.05, f"S8 proxy {S8p['g1_kb']:.3f}")
    check("P2 [VERDICT] self-consistent g0 = 0.58 with the kernel on baryons: S8 proxy >= 0.767 for the late ramp (n = 4)?  (a PASS keeps the knife-edge alive; a FAIL closes it)", S8p["g058_n4_kb"] >= 0.767, f"n=4: {S8p['g058_n4_kb']:.3f}, n=2: {S8p['g058_n2_kb']:.3f}, Newtonian n=4 (no kernel): {S8p['g058_n4_newton']:.3f}")
    print("    LIMITS: as L176 (PM 128^3/50 Mpc/h, single realisation, constant a0 on the peculiar field, LCDM background); S8 proxy from the 0.15-0.5 h/Mpc band of the box.")
    print(f"\nL178 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.   [{time.time()-T0:.0f}s]")
