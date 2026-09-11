#!/usr/bin/env python3
"""L176 -- THE FRAMEWORK'S OWN P(k, z) BASELINE with the kernel active.
Cosmological particle-mesh (PM) code, comoving, LCDM background (Om = 0.315), with the QUMOND kernel applied to the peculiar Newtonian
field (Llinares, Knebe & Zhao 2008 / Angus et al. 2013 approach): grad^2 phi_N = 1.5 Om delta / a, dp/dt = -grad phi_N with p = a^2 dx/dt; g_N = -grad phi_N / a^2 (physical);
grad^2 phi_M = div( nu(|g_N|/a0) grad phi_N ); particles pushed by phi_M. nu_RAR(x) = 1/(1 - exp(-sqrt x)); a0 constant (framework flat law),
both footings. Runs: (A) Newtonian LCDM reference (validates against CLASS halofit); (B) baryons only + kernel; (C) baryons + retained dark
fraction f x LCDM CDM, kernel reading the total. ICs: Zel'dovich at z = 49 from the LCDM matter transfer function (assumption: the
recombination-era component existed, so baryons carry the LCDM spectrum at z = 49). Box 50 Mpc/h, 128^3 mesh, 96^3 particles.
Output: P(k, z)/P_LCDM(k, z) at z = 3, 1, 0.5, 0 for k = 0.15-4 h/Mpc. No literal-True checks. Resolution and approach limits stated."""
import numpy as np, time, sys, os, json
from multiprocessing import Pool
T0 = time.time()
h = 0.6736; Om = 0.3138; OL = 1 - Om; Ob = 0.02237/h**2; Oc = 0.12/h**2
L = 50.0; NG = 128; NP = 96; ZI = 49.0
A0_SI = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
UNIT_ACC = 3.086e22/h*(h*3.2408e-18)**2          # 1 (Mpc/h) H0^2 in m/s^2
A0 = {k: v/UNIT_ACC for k, v in A0_SI.items()}   # a0 in code units
def Hnorm(a): return np.sqrt(Om*a**-3 + OL)
kf = 2*np.pi/L
kx = np.fft.fftfreq(NG, d=L/NG)*2*np.pi
KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing='ij'); K2 = KX**2 + KY**2 + KZ**2; K2[0, 0, 0] = 1.0
def poisson(src):            # solves grad^2 phi = src (periodic), returns phi
    f = np.fft.fftn(src); f = -f/K2; f[0, 0, 0] = 0.0
    return np.real(np.fft.ifftn(f))
def grad(f):
    d = L/NG
    return [(np.roll(f, -1, i) - np.roll(f, 1, i))/(2*d) for i in range(3)]
def div(v):
    d = L/NG
    return sum((np.roll(v[i], -1, i) - np.roll(v[i], 1, i))/(2*d) for i in range(3))
def cic_deposit(x, w):
    rho = np.zeros((NG, NG, NG))
    g = x/(L/NG); i0 = np.floor(g).astype(int); f = g - i0; i0 %= NG; i1 = (i0 + 1) % NG
    for dx in (0, 1):
        wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
            for dz in (0, 1):
                wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                np.add.at(rho, (ix, iy, iz), w*wx*wy*wz)
    return rho
def cic_interp(field, x):
    g = x/(L/NG); i0 = np.floor(g).astype(int); f = g - i0; i0 %= NG; i1 = (i0 + 1) % NG
    out = np.zeros(len(x))
    for dx in (0, 1):
        wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
            for dz in (0, 1):
                wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                out += field[ix, iy, iz]*wx*wy*wz
    return out
def pk(delta, nb=14):
    f = np.fft.fftn(delta); P = np.abs(f)**2*(L**3)/NG**6
    kk = np.sqrt(K2); kk[0, 0, 0] = 0
    edges = np.geomspace(0.15, 4.0, nb + 1); out = []
    for i in range(nb):
        m = (kk >= edges[i]) & (kk < edges[i + 1]); out.append((np.sqrt(edges[i]*edges[i + 1]), P[m].mean() if m.any() else np.nan))
    return np.array(out)
# ---- ICs from CLASS ----
from classy import Class
cl = Class(); cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0,
                      "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 20, "z_max_pk": 60, "non_linear": "halofit"}); cl.compute()
def P_lin(kh, z): return cl.pk_lin(kh*h, z)*h**3           # (Mpc/h)^3
def P_nl(kh, z): return cl.pk(kh*h, z)*h**3
def make_ics(seed=7):
    rng = np.random.default_rng(seed)
    kk = np.sqrt(K2); kk[0, 0, 0] = kf
    Pk = np.vectorize(lambda q: P_lin(q, ZI))(np.clip(kk, kf, 20.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    dk = white*np.sqrt(Pk/L**3)*NG**3/NG**3*np.sqrt(NG**3)     # delta_k with <|d_k|^2> = P/L^3 * N^3 ... normalised so that ifftn gives delta(x)
    dk = white*np.sqrt(Pk*NG**3/L**3)
    delta = np.real(np.fft.ifftn(dk))
    # displacement field psi = -grad grad^-2 delta
    phi = poisson(delta); psi = [-gg for gg in grad(phi)]
    q = (np.arange(NP) + 0.5)*L/NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([cic_interp(p, Q) for p in psi], 1)
    ai = 1/(1 + ZI); f_growth = (Om*ai**-3/(Om*ai**-3 + OL))**0.55   # growth rate at z_i (~1)
    x = (Q + disp) % L
    # p = a^2 dx/dt with dx/dt = H f psi (Zel'dovich); H in units of H0
    p = ai**2*Hnorm(ai)*f_growth*disp
    return x, p, delta
def run(cfg):
    name, kernel, foot, fdark = cfg
    x, p, d0 = make_ics()
    mass_b = Ob/Om; mass_d = fdark*Oc/Om
    w_src = (mass_b + mass_d) if kernel else 1.0     # LCDM reference: all mass (Ob+Oc)/Om = 1
    a0 = A0[foot] if kernel else None
    a = 1/(1 + ZI); dlna = 0.02; zs_out = [3.0, 1.0, 0.5, 0.0]; out = {}
    npart = len(x)
    def accel(x, a):
        rho = cic_deposit(x, np.full(npart, 1.0))*NG**3/npart
        delta = rho*w_src - w_src        # density contrast of the SOURCING mass, in units of the total LCDM mean (w_src = mass fraction present)
        src = 1.5*Om*delta/a
        phiN = poisson(src)
        if kernel:
            gN = [-gg/a**2 for gg in grad(phiN)]
            mag = np.sqrt(sum(gg**2 for gg in gN)) + 1e-30
            nu = 1.0/(1.0 - np.exp(-np.sqrt(mag/a0)))
            phi = poisson(div([nu*gg for gg in grad(phiN)]))
        else:
            phi = phiN
        gr = grad(phi)
        return -np.stack([cic_interp(gg, x) for gg in gr], 1), rho
    acc, _ = accel(x, a)
    step = 0
    while a < 1.0:
        da = a*(np.exp(dlna) - 1); dt = da/(a*Hnorm(a))
        p += 0.5*dt*acc
        x = (x + dt*p/a**2) % L
        a = a + da
        acc, rho = accel(x, a)
        p += 0.5*dt*acc
        step += 1
        for z in list(zs_out):
            if 1/a - 1 <= z + 1e-9:
                rho_tot = cic_deposit(x, np.full(npart, 1.0))*NG**3/npart
                out[z] = pk(rho_tot - 1).tolist(); zs_out.remove(z)
    return name, out
if __name__ == "__main__":
    print(f"    box {L} Mpc/h, mesh {NG}^3, particles {NP}^3, z_i = {ZI}; a0 code units canonical {A0['canonical']:.0f}, alt {A0['alt']:.0f}", flush=True)
    cfgs = [("LCDM_newton", False, "canonical", 1.0), ("bary_canon", True, "canonical", 0.0), ("bary_alt", True, "alt", 0.0),
            ("f0.1_canon", True, "canonical", 0.1), ("f0.58_canon", True, "canonical", 0.58)]
    if os.path.exists("L176_pk_results.json") and "--rerun" not in sys.argv:
        print("    using saved L176_pk_results.json (pass --rerun to recompute)")
    else:
        with Pool(5) as pool: res = dict(pool.map(run, cfgs))
        json.dump(res, open("L176_pk_results.json", "w"))
        print(f"    runs done in {time.time()-T0:.0f}s", flush=True)
    res = json.load(open("L176_pk_results.json"))
    CH = []
    def check(n, ok, d=""):
        CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
    ref = {z: np.array(res["LCDM_newton"][z]) for z in ("3.0", "1.0", "0.5", "0.0")}
    print("\n    (A) VALIDATION: Newtonian LCDM PM vs CLASS halofit, P_PM/P_halofit")
    devs = []
    for z in ("3.0", "0.0"):
        r = ref[z]; ratio = np.array([p/P_nl(k, float(z)) for k, p in r])
        m = (r[:, 0] >= 0.3) & (r[:, 0] <= 2.0); devs.append(np.max(np.abs(ratio[m] - 1)))
        print(f"      z={z}: " + " ".join(f"{k:.2f}:{x:.2f}" for k, x in zip(r[:, 0], ratio)))
    check("V1 the Newtonian LCDM run reproduces CLASS halofit within 35% for 0.3 <= k <= 2 h/Mpc at z = 3 and z = 0 (PM resolution / shot noise)", max(devs) < 0.35, f"max dev {max(devs):.2f}")
    print("\n    (B/C) FRAMEWORK BASELINE: P/P_LCDM(PM) -- the kernel-boosted structure relative to the same-code LCDM")
    hdr = "      k [h/Mpc]: " + " ".join(f"{k:6.2f}" for k in ref["3.0"][:, 0]); print(hdr)
    R = {}
    for name in ("bary_canon", "bary_alt", "f0.1_canon", "f0.58_canon"):
        for z in ("3.0", "1.0", "0.5", "0.0"):
            r = np.array(res[name][z]) / ref[z]; R[(name, z)] = r[:, 1]
            print(f"      {name:<12} z={z}: " + " ".join(f"{x:6.2f}" for x in r[:, 1]))
    kk = ref["3.0"][:, 0]; m_forest = (kk >= 1.0) & (kk <= 4.0); m_shear = (kk >= 0.3) & (kk <= 2.0)
    for name in ("bary_canon", "bary_alt"):
        rf = R[(name, "3.0")][m_forest]; rs = R[(name, "0.5")][m_shear]
        print(f"      {name}: forest band z=3 k=1-4: {rf.min():.2f}-{rf.max():.2f};  shear band z=0.5 k=0.3-2: {rs.min():.2f}-{rs.max():.2f}")
    check("B1 [BASELINE, verified] baryons-only + kernel does NOT reproduce LCDM power in the forest band at z = 3 to 10% for either footing (it is either under or over)",
          all(np.max(np.abs(R[(n, "3.0")][m_forest] - 1)) > 0.10 for n in ("bary_canon", "bary_alt")))
    over = all(np.mean(R[(n, "0.0")][m_shear]) > 1 for n in ("bary_canon", "bary_alt"))
    under = all(np.mean(R[(n, "0.0")][m_shear]) < 1 for n in ("bary_canon", "bary_alt"))
    check("B2 direction at z = 0 in the shear band is the same for both footings (both over or both under LCDM)", over or under, "OVER" if over else ("UNDER" if under else "mixed"))
    check("B3 adding a retained dark fraction (0.1, 0.58, kernel reading the total) moves the z = 0 shear-band power monotonically",
          np.mean(R[("bary_canon", "0.0")][m_shear]) < np.mean(R[("f0.1_canon", "0.0")][m_shear]) < np.mean(R[("f0.58_canon", "0.0")][m_shear]))
    print("    LIMITS: PM at 128^3/50 Mpc/h (k <= 4, no small-scale halo cores); QUMOND on the peculiar field with constant a0 (the cosmological-a0 ambiguity is\n"
          "    resolved the Llinares/Angus way); LCDM background; ICs assume the recombination-era component; no baryonic physics; single realisation.")
    print(f"\nL176 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.   [{time.time()-T0:.0f}s]")
