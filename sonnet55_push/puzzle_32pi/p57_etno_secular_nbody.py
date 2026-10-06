"""p57: secular N-particle test of the detached-disk lift with OUR kernel (the VNT24 question, arXiv:2403.09555, in a reduced model).
Model (orbit-averaged / Milankovitch, a fixed, Neptune scattering NOT modelled -- a secular-lift test only):
  state per particle: j = L/sqrt(GM a), e (vectors, ecliptic frame); dj/dt = <r x F>/sqrt(GMa), de/dt = <F x L + v x (r x F)>/GM, <.> = time average via E-sampling.
  F = giant-planet quadrupole (J2R2 = 1/2 sum m a^2, ecliptic ~ invariable plane) + Galactic vertical tide (rho0 = 0.1 Msun/pc^3) + MOND anomaly with the Galactic EFE:
  QUMOND field-equation solution (qumond_efe_multipole.py, Legendre multipoles l <= 8): force relative to the Sun = grad psi(r) - grad psi(0),
  g_Ne toward the Galactic centre with nu(y_e) y_e a0 = 2.146e-10 m/s^2 (233 km/s, 8.2 kpc). Exact field equation, no algebraic shortcut
  (v0 of this script used algebraic QUMOND -- WITHDRAWN, see p57a_ALGEBRAIC_MODEL_WITHDRAWN.py).
Kernels: K0 Newton; K1 exact nu = sqrt(1+1/y) (a0 9.36e-11); K2 OURS nu_fix, y_t = 128.9; K3 VNT24's sharpest AQUAL mu_20 (a0 1.2e-10), which VNT24 found STILL overpopulates the detached disk.
Initial: 300 particles, q U(30,36) AU, a log-U(150,2000) AU, i U(0,25) deg, Omega, omega U(0,360); same set for every kernel; 4.5 Gyr.
Checks (fixed before the run): C1 Newton conserves j.z (axisym. quadrupole only... tide breaks it weakly) -- checked with the tide OFF: |dj_z| < 1e-6;
  C2 radial-only control: K1 keeping only the l = 0 (monopole) part, planets and tide off, changes q by < 0.05 AU (a central force cannot lift perihelia);
  C4 the multipole force at 50 AU reproduces the quadrupole law F_z(r z) - F_x(r x) = Q2 r to 2% (solver self-consistency);
  C3 DECISION (pre-registered): f38(K) = fraction with final q > 38 AU.  If f38(K2) >= f38(K3): our turn-off lifts at least as much as the case VNT24 found excluded
     => 'likely excluded' CONFIRMED in this model.  If f38(K2) <= f38(K0) + 0.02: worry LIFTED.  Else INCONCLUSIVE.  (C3 always 'passes'; the verdict is printed.)
AMENDMENTS after the QUICK timing run (before the full run): (i) particles with q < 25 AU are FROZEN and counted 'lost' (Neptune would scatter them;
  without this the exact-law EFE torque drives e -> 1 within ~0.1 Myr and the integrator stops); (ii) C2's control also switches the planet quadrupole off
  (a radial force changes the precession phase and so the quadrupole's e-i exchange; 0.78 AU in the quick run -- the control was ill-posed);
  (iii) the decision needs the reference to lift: CONFIRMED only if f38(K3) > f38(K0) + 0.02 AND f38(K2) >= f38(K3); if K3 does not lift, this reduced model
  does not reproduce VNT24 and the verdict is MODEL-NOT-CALIBRATED (the quick run's 'CONFIRMED' on 0 = 0 = 0 was this tie bug).
AMENDMENTS after the field-model QUICK run (before the full run): (iv) solver resolution Nr 6000 -> 12000, Nmu 256 -> 512 (C4 read 0.978 at 50 AU at the
  default grid, 0.989 at the finer one; Q2 identical to 4 digits); (v) N 300 -> 150 (run time); (vi) ADDED metric (reported, not the decision):
  detached occupancy = time-average over 46 snapshots of [# with q > 38] / [# surviving, q > 25.5] -- the steady-state-like quantity VNT24's comparison is about.
(vii) MUTATE bug fixed after the full run: v1 passed efe_on = not MUTATE (= False), so the first mutant was identical to the control; the main run is unaffected.
Run: python3 p57_etno_secular_nbody.py | MUTATE=1: C2's control keeps all multipoles (must fail).  QUICK=1: 50 particles, 0.5 Gyr (timing only)
"""
import os, sys, math, time, json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qumond_efe_multipole import Field
MUTATE = os.environ.get("MUTATE") == "1"; QUICK = os.environ.get("QUICK") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n, flush=True)
GM = 4 * math.pi**2                                # AU^3/yr^2
MS2 = (3.15576e7)**2 / 1.495978707e11              # 1 m/s^2 in AU/yr^2
def unit(lam, bet):
    l, b = math.radians(lam), math.radians(bet); return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])
u_gc, n_gp = unit(266.84, -5.54), unit(180.02, 29.81)
k_tide = 4 * math.pi * GM * 0.1 / 206264.806**3
J2R2 = 0.5 * sum(m * a**2 for m, a in [(1/1047.35, 5.2), (1/3497.9, 9.54), (1/22902.9, 19.19), (1/19412.2, 30.07)])
def nu1_exact(y): return 1.0 / (y * (np.sqrt(1 + 1 / y) + 1))
def nu1_fix(y, yt=128.915): return nu1_exact(y) / (1 + (y / yt)**2)
# mu_20 table: x mu(x) = y, mu = x/(1+x^n)^(1/n)
xs = np.logspace(-4, 4, 4000); ys = xs**2 / (1 + xs**20)**(1 / 20); n1 = xs / ys - 1
def nu1_mu20(y):
    v = np.interp(np.log(y), np.log(ys), np.log(np.maximum(n1, 1e-300)))
    return np.where(y > ys[-1], 0.0, np.exp(v))
KER = {"K0": (None, 9.3603e-11), "K1": (nu1_exact, 9.3603e-11), "K2": (nu1_fix, 9.3603e-11), "K3": (nu1_mu20, 1.2e-10)}
def efe(nu1, a0):
    ye = brentq(lambda y: (1 + nu1(np.array(y))) * y - 2.146e-10 / a0, 1e-3, 100)
    return ye, float(nu1(np.array(ye)))
NE = 48
FIELDS = {k: Field(v[0], v[1], Nr=12000, Nmu=512) for k, v in KER.items() if v[0] is not None}
for k, f in FIELDS.items(): print(f"   {k}: y_e = {f.ye:.3f}, nu_e = {f.nue:.3f}, Q2 = {f.Q2:.3e} s^-2 (Cassini: (3 +- 3)e-27, Hees+ 2014)", flush=True)
class MonoView:
    def __init__(self, f): self.f = f
    def force(self, rv, zhat):
        rn = np.linalg.norm(rv, axis=-1); dps = np.interp(np.log(rn), np.log(self.f.r), self.f.dpsi[0])
        return dps[..., None] * rv / rn[..., None]
# C4 solver self-consistency
_f = FIELDS["K1"]; _r = 50.0; _z = np.array([0, 0, 1.0])
_Fz = _f.force(np.array([[0, 0, _r]]), _z)[0, 2]; _Fx = _f.force(np.array([[_r, 0, 0]]), _z)[0, 0]
_Q2u = _f.Q2 * (3.15576e7)**2
c4 = abs((_Fz - _Fx) / (_Q2u * _r) - 1)
Eg = np.linspace(0, 2 * np.pi, NE, endpoint=False); cE, sE = np.cos(Eg), np.sin(Eg)
def make_rhs(kname, a, tide=True, efe_on=True, planets=True):
    nu1, a0 = KER[kname]; a0u = a0 * MS2
    if nu1 is not None:
        fld = FIELDS[kname]
        lmax_save = fld.L
        if not efe_on: fld = MonoView(fld)
    sq = np.sqrt(GM * a)
    def rhs(t, s):
        s = s.reshape(-1, 6); j, e = s[:, :3], s[:, 3:]
        en = np.linalg.norm(e, axis=1); jn = np.linalg.norm(j, axis=1)
        eh = e / en[:, None]; qh = np.cross(j / jn[:, None], eh)
        r = a[:, None, None] * ((cE[None, :, None] - en[:, None, None]) * eh[:, None, :] + (jn[:, None, None] * sE[None, :, None]) * qh[:, None, :])
        w = (1 - en[:, None] * cE[None, :]) / NE
        vf = np.sqrt(GM / a)[:, None, None] / (1 - en[:, None] * cE[None, :])[:, :, None]
        v = vf * (-sE[None, :, None] * eh[:, None, :] + (jn[:, None, None] * cE[None, :, None]) * qh[:, None, :])
        rn = np.linalg.norm(r, axis=2); z = r[..., 2]
        c = GM * J2R2 if planets else 0.0
        F = np.empty_like(r)
        F[..., 0] = -c / 2 * (-15 * z**2 * r[..., 0] / rn**7 + 3 * r[..., 0] / rn**5)
        F[..., 1] = -c / 2 * (-15 * z**2 * r[..., 1] / rn**7 + 3 * r[..., 1] / rn**5)
        F[..., 2] = -c / 2 * (9 * z / rn**5 - 15 * z**3 / rn**7)
        if tide: F += -k_tide * (r @ n_gp)[..., None] * n_gp
        if nu1 is not None:
            F += fld.force(r, u_gc)
        L = (j * sq[:, None])
        tq = np.einsum("pk,pkc->pc", w, np.cross(r, F))
        dj = tq / sq[:, None]
        de = (np.einsum("pk,pkc->pc", w, np.cross(F, L[:, None, :]) + np.cross(v, np.cross(r, F)))) / GM
        live = (a * (1 - en) > 25.0)[:, None]
        return np.hstack([dj * live, de * live]).ravel()
    return rhs
rng = np.random.default_rng(57)
N, T = (50, 5e8) if QUICK else (150, 4.5e9)
a = np.exp(rng.uniform(np.log(150), np.log(2000), N)); q0 = rng.uniform(30, 36, N); e0 = 1 - q0 / a
inc, Om, om = np.radians(rng.uniform(0, 25, N)), np.radians(rng.uniform(0, 360, N)), np.radians(rng.uniform(0, 360, N))
def vecs(e, i, O, w):
    P = np.stack([np.cos(w) * np.cos(O) - np.sin(w) * np.sin(O) * np.cos(i), np.cos(w) * np.sin(O) + np.sin(w) * np.cos(O) * np.cos(i), np.sin(w) * np.sin(i)], 1)
    h = np.stack([np.sin(O) * np.sin(i), -np.cos(O) * np.sin(i), np.cos(i)], 1)
    return np.sqrt(1 - e**2)[:, None] * h, e[:, None] * P
j0, ev0 = vecs(e0, inc, Om, om); s0 = np.hstack([j0, ev0]).ravel()
def qof(s): s = s.reshape(-1, 6); return a * (1 - np.linalg.norm(s[:, 3:], axis=1))
def run(kname, T, **kw):
    t0 = time.time()
    sol = solve_ivp(make_rhs(kname, a, **kw), (0, T), s0, method="DOP853", rtol=1e-7, atol=1e-10, t_eval=np.linspace(0, T, 46))
    qs = np.array([qof(sol.y[:, k]) for k in range(sol.y.shape[1])])
    print(f"   {kname} {kw if kw else ''}: {sol.status} nfev={sol.nfev} {time.time()-t0:.0f}s", flush=True)
    return sol, qs
check(f"C4 multipole force at 50 AU reproduces the Q2 quadrupole law: |ratio - 1| = {c4:.2e} < 0.02", c4 < 0.02)
# C1: Newton, tide off, axisymmetric -> j_z conserved
sol, qs = run("K0", 1e9 if not QUICK else 1e8, tide=False)
djz = np.max(np.abs(sol.y.reshape(N, 6, -1)[:, 2, -1] - sol.y.reshape(N, 6, -1)[:, 2, 0]))
check(f"C1 Newton (planet quadrupole only) conserves j_z: max |dj_z| = {djz:.2e} < 1e-6", djz < 1e-6)
# C2: radial-only MOND (no EFE) cannot change q
sol, qs = run("K1", 2e8 if not QUICK else 5e7, efe_on=True, tide=False, planets=False) if MUTATE else run("K1", 2e8 if not QUICK else 5e7, efe_on=False, tide=False, planets=False)
sol0, qs0 = run("K0", 2e8 if not QUICK else 5e7, tide=False, planets=False)
dq = np.max(np.abs(qs[-1] - qs0[-1]))
check(f"C2 MOND without the external field leaves q unchanged vs Newton: max |dq| = {dq:.3g} AU < 0.05" + ("  [MUTATE: EFE on]" if MUTATE else ""), dq < 0.05)
if MUTATE:
    print(f"\n{sum(res)}/{len(res)} pass  (MUTATE)"); sys.exit(0 if all(res) else 1)
out = {}
for k in ("K0", "K1", "K2", "K3"):
    sol, qs = run(k, T)
    f38 = float(np.mean(qs[-1] > 38)); f50 = float(np.mean(qs[-1] > 50)); fmax = float(np.mean(qs.max(0) > 38)); flow = float(np.mean(qs.min(0) < 20))
    lost = float(np.mean(qs[-1] < 25.5))
    surv = (qs > 25.5).sum(1); occ = float(np.mean(np.where(surv > 0, (qs > 38).sum(1) / np.maximum(surv, 1), 0.0)))
    out[k] = dict(f38=f38, f50=f50, ever38=fmax, lost=lost, q_med_final=float(np.median(qs[-1])), status=int(sol.status), occupancy=occ)
    print(f"   {k}: final q>38 {f38:.3f}, q>50 {f50:.3f}, ever q>38 {fmax:.3f}, lost (q<25) {lost:.3f}, median final q {np.median(qs[-1]):.1f} AU, detached occupancy {occ:.3f}, status {sol.status}", flush=True)
f0, f2, f3 = out["K0"]["f38"], out["K2"]["f38"], out["K3"]["f38"]
if f3 <= f0 + 0.02: verdict = "MODEL-NOT-CALIBRATED (the n=20 reference does not lift here)"
elif f2 >= f3: verdict = "CONFIRMED (ours lifts >= VNT24's excluded n=20 case)"
elif f2 <= f0 + 0.02: verdict = "LIFTED (ours ~ Newton)"
else: verdict = "INCONCLUSIVE"
print(f"   VERDICT: {verdict}")
check("C3 decision computed (verdict printed)", True)
json.dump(dict(out=out, verdict=verdict, N=N, T=T), open("p57_etno_secular_nbody.json" if not QUICK else "p57_quick.json", "w"), indent=1)
print(f"\n{sum(res)}/{len(res)} pass")
sys.exit(0 if all(res) else 1)
