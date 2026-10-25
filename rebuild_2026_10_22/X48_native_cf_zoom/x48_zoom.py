#!/usr/bin/env python3
"""X48_native_cf_zoom: direct-summation collisionless collapse of a constrained peak on the record's own P(k) and background;
measures the formation-epoch concentration c_f natively. Follows compute_queue/JOB_CONTRACT.md (preemptible).

Physics: collisionless dust, Newtonian gravity between particles (Plummer softening) + the background Lambda term, physical
coordinates, isolated Lagrangian sphere of radius RS * q_M around a Hoffman-Ribak constrained peak (smoothed height nu and
curvature <x|nu> at the centre, nu set so the half-mass object M/2 collapses at its Lacey-Cole z_f, as X45 A1). Background A
(EM1's CLASS refit). This is route E's cold dark energy without the a0 floor; NOT v3s dynamics.

  python3 x48_zoom.py --mass 1e14 --seed 1 --ng 48 --work DIR [--resume]
Outputs (atomic): DIR/ckpt.npz (rolling, every --ckpt-s seconds and on SIGTERM), DIR/snap_zf.npz (final), DIR/done.json.
Exit 0 complete; 75 checkpointed on SIGTERM/SIGINT (resume with --resume).
"""
import argparse, io, contextlib, json, math, os, signal, sys, time
import numpy as np

YIELD_EXIT = int(os.environ.get("HEAVYQ_YIELD_EXIT", "75"))
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
G = 4.30091e-9                       # Mpc (km/s)^2 / Msun
KMS_MPC_TO_GYR = 977.792             # 1 / (km/s/Mpc) in Gyr


def atomic_npz(path, **arrs):
    tmp = path + ".tmp.npz"
    with open(tmp, "wb") as f:
        np.savez(f, **arrs); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def cosmology():
    """Background A: CLASS P(k) at z=0 (1/Mpc, Mpc^3), D(z), H(z), Lacey-Cole sigma(M) - read from EM1's code read-only."""
    src = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(src).read()
    NE = {"__file__": src, "__name__": "em1_ro"}; a0 = sys.argv; sys.argv = [src]
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(TE[:TE.index("# ---------------- halo profiles")], src, "exec"), NE)
    sys.argv = a0
    bg = NE["BGS"]["A_c2b_refit"]; cc = bg["c"]; h = bg["h"]; Om = float(cc.Omega_m()); OL = 1 - Om
    K = np.logspace(-4, 2.14, 3000); PK = np.array([cc.pk_lin(k, 0.0) for k in K])
    ZG = np.concatenate([np.linspace(0, 10, 1001), np.geomspace(10.01, 200, 300)])
    DG = np.array([cc.scale_independent_growth_factor(z) for z in ZG]); DG /= DG[0]
    sig = bg["cB"].__defaults__[1]
    return dict(h=h, Om=Om, OL=OL, H0=100 * h, K=K, PK=PK, ZG=ZG, DG=DG, sig=sig, rhom=Om * 2.775e11 * h ** 2)


def lacey_cole_zf(C, M):
    lM = np.linspace(7, 16.5, 191); s2 = np.array([float(C["sig"](10 ** l)[0]) ** 2 for l in lM])
    S = math.sqrt(float(np.interp(math.log10(M / 2), lM, s2)) - float(np.interp(math.log10(M), lM, s2)))
    Df = 1.686 / (1.686 + 0.974 * S); return float(np.interp(-Df, -C["DG"], C["ZG"])), Df


def Hz(C, z): return C["H0"] * math.sqrt(C["Om"] * (1 + z) ** 3 + C["OL"])
def t_of_z(C, z):
    zz = np.geomspace(1 + z, 1e4, 4000) - 1
    f = 1 / ((1 + zz) * np.array([Hz(C, x) for x in zz]))
    return float(np.trapz(f, zz)) * KMS_MPC_TO_GYR      # Gyr


def constrained_field(C, M, seed, ng, RS):
    """Hoffman-Ribak constrained Gaussian field (comoving Mpc, z=0 linear) on a periodic grid of side 4 q_M; returns
    (q positions inside RS q_M, Zel'dovich displacement at z=0 linear amplitude, meta)."""
    zf, Df = lacey_cole_zf(C, M); Mf = M / 2; rho = C["rhom"]
    qM = (3 * Mf / (4 * math.pi * rho)) ** (1 / 3); RG = (Mf / ((2 * math.pi) ** 1.5 * rho)) ** (1 / 3)
    L = 4 * qM; dx = L / ng
    k1 = 2 * np.pi * np.fft.fftfreq(ng, d=dx); kz = 2 * np.pi * np.fft.rfftfreq(ng, d=dx)
    KX, KY, KZ = np.meshgrid(k1, k1, kz, indexing="ij"); KK = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2); KK[0, 0, 0] = 1e-30
    Pk = np.interp(np.log(KK), np.log(C["K"]), C["PK"], left=0.0, right=0.0); Pk[0, 0, 0] = 0.0
    V = L ** 3; rng = np.random.default_rng(seed)
    amp = np.sqrt(Pk * ng ** 6 / V / 2)
    dk = amp * (rng.standard_normal(KK.shape) + 1j * rng.standard_normal(KK.shape))
    dk[0, 0, 0] = 0
    d_r = np.fft.irfftn(dk, s=(ng, ng, ng))                 # random field (unit-consistent)
    W = np.exp(-(KK * RG) ** 2 / 2)
    # constraint functionals at the origin: C1 = delta_s(0), C2 = lap delta_s(0)
    def corr(fk):                                            # <delta(x) C>(x) on the grid
        return np.fft.irfftn(fk * Pk * ng ** 3 / V, s=(ng, ng, ng))
    xi1 = corr(W); xi2 = corr(-(KK ** 2) * W)
    s0 = math.sqrt(float(np.sum(_herm(Pk * W ** 2)) / V)); s1 = math.sqrt(float(np.sum(_herm(Pk * W ** 2 * KK ** 2)) / V))
    s2 = math.sqrt(float(np.sum(_herm(Pk * W ** 2 * KK ** 4)) / V))
    CC = np.array([[s0 ** 2, -s1 ** 2], [-s1 ** 2, s2 ** 2]])
    c1r = float(np.fft.irfftn(dk * W, s=(ng, ng, ng))[0, 0, 0]); c2r = float(np.fft.irfftn(dk * W * (-(KK ** 2)), s=(ng, ng, ng))[0, 0, 0])
    gam = s1 ** 2 / (s0 * s2)
    # nu from the X45-A1 condition (enclosed linear mean inside q_M = delta_c / D(z_f)) on the MEAN constrained field
    xs = np.linspace(1e-4, 30, 30001)
    from scipy.special import erf
    def fB(x): return ((x ** 3 - 3 * x) / 2 * (erf(math.sqrt(2.5) * x) + erf(math.sqrt(2.5) * x / 2))
                       + math.sqrt(2 / (5 * math.pi)) * ((31 * x ** 2 / 4 + 1.6) * np.exp(-5 * x ** 2 / 8) + (x ** 2 / 2 - 1.6) * np.exp(-5 * x ** 2 / 2)))
    def xmean(nu):
        w = fB(xs) * np.exp(-(xs - gam * nu) ** 2 / (2 * (1 - gam ** 2))); return float(np.trapz(xs * w, xs) / np.trapz(w, xs))
    idx = np.fft.fftfreq(ng) * ng; IX, IY, IZ = np.meshgrid(idx, idx, idx, indexing="ij"); R = np.sqrt(IX ** 2 + IY ** 2 + IZ ** 2) * dx
    inM = R <= qM
    CCi = np.linalg.inv(CC)
    def mean_field(nu):
        x = xmean(nu); cvec = np.array([nu * s0, -x * s2])
        w = CCi @ cvec; return w[0] * xi1 + w[1] * xi2, x
    from scipy.optimize import brentq
    thr = 1.686 / Df
    nu = brentq(lambda n: float(mean_field(n)[0][inM].mean()) - thr, 0.05, 50.0, xtol=1e-10)
    mf, xbar = mean_field(nu)
    cvec = np.array([nu * s0, -xbar * s2]); rvec = np.array([c1r, c2r])
    w = CCi @ (cvec - rvec); delta = d_r + w[0] * xi1 + w[1] * xi2       # HR: random + correction
    # Zel'dovich displacement Psi = grad(laplacian^-1) ... Psi_k = i k delta_k / k^2
    dkc = np.fft.rfftn(delta); psi = [np.fft.irfftn(1j * Kc * dkc / KK ** 2, s=(ng, ng, ng)) for Kc in (KX, KY, KZ)]
    sel = R <= RS * qM
    q = np.stack([IX[sel], IY[sel], IZ[sel]], axis=1) * dx; ps = np.stack([p[sel] for p in psi], axis=1)
    check = dict(c1=float(np.fft.irfftn(np.fft.rfftn(delta) * W, s=(ng, ng, ng))[0, 0, 0]) / (nu * s0) - 1,
                 c2=float(np.fft.irfftn(np.fft.rfftn(delta) * W * (-(KK ** 2)), s=(ng, ng, ng))[0, 0, 0]) / (-xbar * s2) - 1)
    meta = dict(M=M, Mf=Mf, zf=zf, Df=Df, nu=nu, xbar=xbar, gamma=gam, qM=qM, RG=RG, L=L, ng=ng, RS=RS, N=int(sel.sum()),
                mpart=float((4 * math.pi / 3) * rho * (RS * qM) ** 3 / sel.sum() * ((4 * math.pi / 3) * (RS * qM) ** 3 / (sel.sum() * dx ** 3)) ** -1),
                constraint_check=check)
    meta["mpart"] = float(rho * dx ** 3)                    # each lattice point carries one cell of mean density
    return q, ps, meta


def _herm(a):
    """sum over the full k-space from an rfft half-space array (double the interior planes)."""
    w = np.full(a.shape[-1], 2.0); w[0] = 1.0
    if a.shape[-1] > 1 and (2 * (a.shape[-1] - 1)) == a.shape[0]: w[-1] = 1.0
    return a * w[None, None, :]


def accel(x, m, eps, OLH2, chunk=512):
    """direct-summation softened gravity (Mpc (km/s)^2 / Msun units -> (km/s)^2/Mpc) + Lambda term."""
    N = len(x); a = np.zeros_like(x)
    for i in range(0, N, chunk):
        d = x[None, :, :] - x[i:i + chunk, None, :]
        r2 = (d * d).sum(-1) + eps * eps
        inv = r2 ** -1.5
        a[i:i + chunk] = G * m * (d * inv[..., None]).sum(1)
    return a + OLH2 * x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mass", type=float, required=True); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--ng", type=int, default=48); ap.add_argument("--rs", type=float, default=1.5)
    ap.add_argument("--zi", type=float, default=40.0); ap.add_argument("--eta", type=float, default=0.2)
    ap.add_argument("--eps-frac", type=float, default=0.01); ap.add_argument("--ckpt-s", type=float, default=600.0)
    ap.add_argument("--max-steps", type=int, default=200000)
    ap.add_argument("--work", required=True); ap.add_argument("--resume", action="store_true")
    a = ap.parse_args(); os.makedirs(a.work, exist_ok=True)
    ck, snap, done = (os.path.join(a.work, n) for n in ("ckpt.npz", "snap_zf.npz", "done.json"))
    if a.resume and os.path.exists(done):
        print("complete: nothing to do", flush=True); return 0
    stop = dict(sig=None)
    def on_sig(s, f): stop["sig"] = s
    signal.signal(signal.SIGTERM, on_sig); signal.signal(signal.SIGINT, on_sig)
    C = cosmology()
    if a.resume and os.path.exists(ck):
        Z = np.load(ck, allow_pickle=False); x, v = Z["x"], Z["v"]; t, step = float(Z["t"]), int(Z["step"])
        meta = json.loads(str(Z["meta"])); print(f"resumed at step {step}, t {t:.4f} Gyr", flush=True)
    else:
        q, ps, meta = constrained_field(C, a.mass, a.seed, a.ng, a.rs)
        zi = a.zi; ai = 1 / (1 + zi); Di = float(np.interp(zi, C["ZG"], C["DG"])); Hi = Hz(C, zi)
        Om_i = C["Om"] * (1 + zi) ** 3 / (C["Om"] * (1 + zi) ** 3 + C["OL"]); f_i = Om_i ** 0.55
        x = ai * (q + Di * ps)                                            # physical Mpc
        v = Hi * x + ai * Hi * f_i * Di * ps                              # km/s (Hubble flow + Zel'dovich growing mode)
        x -= x.mean(0); v -= v.mean(0)
        t = t_of_z(C, zi); step = 0
        meta.update(zi=zi, t_i=t, eta=a.eta, eps_frac=a.eps_frac, seed=a.seed)
        print(json.dumps({k: meta[k] for k in ("M", "zf", "nu", "xbar", "N", "constraint_check")}), flush=True)
    N = len(x); m = meta["mpart"]
    rf_phys = (3 * meta["Mf"] / (4 * math.pi * 18 * math.pi ** 2 * C["rhom"] * (1 + meta["zf"]) ** 3)) ** (1 / 3)
    eps = a.eps_frac * rf_phys; OLH2 = C["OL"] * C["H0"] ** 2
    t_end = t_of_z(C, meta["zf"]); GYR = 1 / KMS_MPC_TO_GYR                # Gyr -> Mpc/(km/s)
    acc = accel(x, m, eps, OLH2); last = time.time()
    while t < t_end and step < a.max_steps:
        amax = float(np.sqrt((acc * acc).sum(1)).max())
        dt = min(a.eta * math.sqrt(eps / max(amax, 1e-30)) / GYR, t_end - t)   # Gyr
        dts = dt * GYR
        v += 0.5 * dts * acc; x += dts * v; acc = accel(x, m, eps, OLH2); v += 0.5 * dts * acc
        t += dt; step += 1
        if stop["sig"] is not None or time.time() - last > a.ckpt_s:
            atomic_npz(ck, x=x, v=v, t=np.array(t), step=np.array(step), meta=np.array(json.dumps(meta)))
            last = time.time()
            if stop["sig"] is not None:
                print(f"signal {stop['sig']}: checkpoint at step {step}, exit {YIELD_EXIT}", flush=True); return YIELD_EXIT
        if step % 200 == 0:
            print(f"step {step} t {t:.4f}/{t_end:.4f} Gyr dt {dt:.2e}", flush=True)
    if t < t_end:                                                            # max-steps reached: NOT complete
        atomic_npz(ck, x=x, v=v, t=np.array(t), step=np.array(step), meta=np.array(json.dumps(meta)))
        print(f"max-steps {a.max_steps} reached at t {t:.4f} < t_end {t_end:.4f}: checkpoint only, not complete", flush=True); return 3
    meta.update(eps=eps, rf_phys=rf_phys, t_end=t_end, steps=step)
    atomic_npz(snap, x=x, v=v, m=np.array(m), meta=np.array(json.dumps(meta)))
    atomic_json(done, dict(steps=step, t_end=t_end, N=N))
    print(f"done: {step} steps", flush=True); return 0


if __name__ == "__main__":
    sys.exit(main())
