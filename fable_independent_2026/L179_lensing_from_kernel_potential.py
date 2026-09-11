#!/usr/bin/env python3
"""L179 -- LENSING ON THE FRAMEWORK'S OWN TERMS: the observable is the kernel-boosted POTENTIAL, not the density. Same PM code/ICs as L176;
for every run the lensing-effective contrast is delta_lens = a grad^2 phi_M / (1.5 Om), with phi_M the potential the particles actually feel
(Newtonian for LCDM, MONDified for the framework). Runs: LCDM reference; baryons + kernel (both footings); baryons + 0.1 dark, kernel reading
total; TEMPORAL SEPARATION: full dark component until t_* = 5 Gyr then removed (coupling -> 0, no heating), kernel on baryons after.
Output: forest band (baryon density, z = 3), shear band (lensing potential power, z = 0.5), S8 proxy from lensing power at 0.15-0.5 h/Mpc, z = 0."""
import numpy as np, json, sys, os, time
from multiprocessing import Pool
from L176_framework_pk_baseline import (poisson, grad, div, cic_deposit, cic_interp, pk, make_ics, Hnorm, A0, Om, Ob, Oc, L, NG, NP, ZI, K2)
GYR_T = 977.792/67.36     # 1/H0 in Gyr
def run3(cfg):
    name, kernel, foot, fdark, read_total, t_star = cfg
    a0 = A0[foot]; x, p, _ = make_ics(); xb, pb = x.copy(), p.copy(); xd, pd = x.copy(), p.copy()
    npart = len(x); wb, wd = Ob/Om, Oc/Om
    from scipy.integrate import quad
    t_of_a = lambda a: quad(lambda aa: 1/(aa*Hnorm(aa)), 1e-6, a)[0]*GYR_T
    def gdark(a): return fdark*(1.0 if (t_star is None or t_of_a(a) < t_star) else 0.0)
    def accel(xb, xd, a):
        rb = cic_deposit(xb, np.full(npart, 1.0))*NG**3/npart; rd = cic_deposit(xd, np.full(npart, 1.0))*NG**3/npart
        gd = gdark(a)
        if not kernel:
            phi = poisson(1.5*Om*(wb*(rb - 1) + gd*wd*(rd - 1))/a)
        elif read_total:
            phiN = poisson(1.5*Om*(wb*(rb - 1) + gd*wd*(rd - 1))/a)
            gN = [-gg/a**2 for gg in grad(phiN)]; mag = np.sqrt(sum(gg**2 for gg in gN)) + 1e-30
            nu = 1.0/(1.0 - np.exp(-np.sqrt(mag/a0))); phi = poisson(div([nu*gg for gg in grad(phiN)]))
        else:
            phiNb = poisson(1.5*Om*wb*(rb - 1)/a); phid = poisson(1.5*Om*gd*wd*(rd - 1)/a)
            gN = [-gg/a**2 for gg in grad(phiNb)]; mag = np.sqrt(sum(gg**2 for gg in gN)) + 1e-30
            nu = 1.0/(1.0 - np.exp(-np.sqrt(mag/a0))); phi = poisson(div([nu*gg for gg in grad(phiNb)])) + phid
        gr = grad(phi); acc = lambda xx: -np.stack([cic_interp(gg, xx) for gg in gr], 1)
        dlens = np.real(np.fft.ifftn(-K2*np.fft.fftn(phi)))*a/(1.5*Om)       # a grad^2 phi / (1.5 Om): the contrast lensing sees
        return acc(xb), acc(xd), rb, dlens
    a = 1/(1 + ZI); dlna = 0.02; zs_out = [3.0, 0.5, 0.0]; out = {}
    ab, ad, rb, dl = accel(xb, xd, a)
    while a < 1.0:
        da = a*(np.exp(dlna) - 1); dt = da/(a*Hnorm(a))
        pb += 0.5*dt*ab; pd += 0.5*dt*ad
        xb = (xb + dt*pb/a**2) % L; xd = (xd + dt*pd/a**2) % L
        a = a + da
        ab, ad, rb, dl = accel(xb, xd, a)
        pb += 0.5*dt*ab; pd += 0.5*dt*ad
        for z in list(zs_out):
            if 1/a - 1 <= z + 1e-9:
                out[str(z)] = {"lens": pk(dl).tolist(), "bary": pk(rb - 1).tolist()}; zs_out.remove(z)
    return name, out
if __name__ == "__main__":
    T0 = time.time()
    cfgs = [("LCDM", False, "canonical", 1.0, False, None), ("bary_kernel_canon", True, "canonical", 0.0, False, None), ("bary_kernel_alt", True, "alt", 0.0, False, None),
            ("f0.1_kernel_total", True, "canonical", 0.1, True, None), ("tempsep_t5_kernel_bary", True, "canonical", 1.0, False, 5.0), ("tempsep_t5_kernel_total", True, "canonical", 1.0, True, 5.0)]
    if not os.path.exists("L179_results.json") or "--rerun" in sys.argv:
        with Pool(6) as pool: res = dict(pool.map(run3, cfgs))
        json.dump(res, open("L179_results.json", "w")); print(f"    runs done in {time.time()-T0:.0f}s", flush=True)
    res = json.load(open("L179_results.json")); ref = res["LCDM"]
    CH = []
    def check(n_, ok, d=""):
        CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n_}" + (f"\n           ({d})" if d else ""))
    kk = np.array(ref["3.0"]["lens"])[:, 0]; mS = (kk >= 0.15) & (kk <= 0.5); mSh = (kk >= 0.3) & (kk <= 2.0); mF = (kk >= 1.0) & (kk <= 4.0)
    print("    LENSING = potential power (a grad^2 phi_M), ratio to same-code LCDM; S8 proxy = 0.8415 x sqrt(mean lensing ratio, 0.15-0.5 h/Mpc, z = 0)")
    print(f"    {'run':<26} {'forest z=3 (bary dens)':>22} {'shear z=0.5 (lens)':>19} {'lens z=0 0.15-0.5':>18} {'S8 proxy':>9}")
    S8p, sh = {}, {}
    for name in res:
        if name == "LCDM": continue
        r = res[name]; f3 = np.array(r["3.0"]["bary"])[:, 1]/np.array(ref["3.0"]["bary"])[:, 1]
        s05 = np.array(r["0.5"]["lens"])[:, 1]/np.array(ref["0.5"]["lens"])[:, 1]; l0 = np.array(r["0.0"]["lens"])[:, 1]/np.array(ref["0.0"]["lens"])[:, 1]
        S8p[name] = 0.8415*np.sqrt(np.mean(l0[mS])); sh[name] = (s05[mSh].min(), s05[mSh].max())
        print(f"    {name:<26} {f3[mF].min():10.2f}-{f3[mF].max():<10.2f} {s05[mSh].min():9.2f}-{s05[mSh].max():<8.2f} {l0[mS].min():8.2f}-{l0[mS].max():<8.2f} {S8p[name]:9.3f}")
    check("L1 [LCDM-yardstick correction] on the framework's own lensing (potential power) the kernel-boosted baryons ALONE give a z = 0 lensing amplitude within a factor 2 of LCDM for at least one footing (the density comparison gave 0.3-0.9)",
          any(0.5 < S8p[n]/0.8415 < 2.0 for n in ("bary_kernel_canon", "bary_kernel_alt")), ", ".join(f"{n}: {S8p[n]/0.8415:.2f}" for n in ("bary_kernel_canon", "bary_kernel_alt")))
    ok = [n for n in ("tempsep_t5_kernel_bary", "tempsep_t5_kernel_total") if 0.767 <= S8p[n] <= 0.90 and sh[n][0] > 0.7]
    check("L2 [VERDICT] temporal separation (component removed at t_* = 5 Gyr, no heating) on the framework's own lensing: S8 proxy in [0.767, 0.90] AND shear band at z = 0.5 above 0.7 of LCDM for some kernel reading (PASS = the door is OPEN again)",
          len(ok) > 0, ", ".join(f"{n}: S8={S8p[n]:.3f}, shear {sh[n][0]:.2f}-{sh[n][1]:.2f}" for n in ("tempsep_t5_kernel_bary", "tempsep_t5_kernel_total")))
    print("    LIMITS: as L176; the forest is still a DENSITY statistic (gas follows the potential, but optical depth is set by density) and is unchanged by this correction.")
    print(f"\nL179 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.   [{time.time()-T0:.0f}s]")
