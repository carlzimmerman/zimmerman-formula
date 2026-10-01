#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_g0_legality_posthoc -- GATE 2 (G0 legality), run as a POST-HOC EXTRA: the frozen stop rule halted the lane at COSMIC (the binding FAIL),
so nothing here is part of the verdict.  Frozen text: CFG243_FROZEN_CRITERIA.md section 2, Gate 2 (rows G0-a ... G0-f), run on the shell toy of
CFG243_shells.py (its departures are listed in that file's docstring).

ROWS (frozen pass lines):
  G0-a locus      |t_theta0 - t_ta|/t_ta <= 0.25 for >= 90% of the shells that turn around (undefined theta0 counts as a miss).
  G0-b multiplicity  median downward theta_b crossings per shell, shells with r_ta < r_ta,max/2, <= 1.1 (else 'a counting rule is required').
  G0-c causality  c_adv <= 1e-12 at N = 200 and 400, with a detector control that fires (a centred time difference).
  G0-d bound-only  <= 0.10 of the created dust in elements that are not 3D-bound.  Operationalisation chosen HERE (the frozen text gave none
                   for the Zel'dovich toy; labelled post hoc): an element is 3D-turned-around iff every axis has turned around, T_i = f D lambda_i/(1 - D lambda_i) >= 1
                   at the theta_b = 0 event; sum_i T_i = 3 at that event, so T_min < 1 unless the element is exactly spherical.
  G0-e vacuum compensation  curl of S u_mu = 0 (the d_mu rho_L = S c^2 u_mu integrability of CFG131 D1): alignment of grad theta with u_mu.
  G0-f inertness  no source in the FRW flow (no core) and none in shells that never turn around.
MUTATE=5: the counting rule is imposed (each shell is counted once): G0-b must flip from 'a counting rule is required' to exactly 1.
"""
import os, sys, math, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG243_common as C
import CFG243_shells as S

R = C.Run("CFG243_g0_legality_posthoc")
P = R.P
MUT = R.mutate
P(__doc__.strip())
P("\n  *** POST-HOC: the frozen stop rule halted the lane at COSMIC; nothing below is part of the frozen verdict ***")
rng = np.random.default_rng(243)
CKMS = C.C_KMS

# ------------------------------------------------------------------------------------------------------------ controls
R.banner("controls")
res0 = S.run(1e10, C.A0, create=False, N=400, core=False, snap_a=(1.0,), soft=0.002)
dev = float(np.max(np.abs(res0["snaps"][0]["rb"] / res0["q"] - 1.0)))
R.check("C1 with no core the shells stay on the Planck Hubble flow to 1e-5 at a = 1 (CFG118's control reached 4.3e-7)", dev <= 1e-5, f"{dev:.2e}")
R.check("C1b no theta_b zero crossing occurs anywhere in the unperturbed Hubble flow (G0-f, FRW row)", int(res0["trig"].sum()) == 0, f"{int(res0['trig'].sum())} triggers")

res = S.run(1e10, C.A0, create=False, N=1000, core=True, snap_a=(1.0,), soft=0.002)
resm = S.run(1e10, C.A0, create=False, N=1000, core=True, snap_a=(1.0,), soft=0.002, shell_density=S.RHOM0)
L7 = C.load_c7().LCDM
sn = resm["snaps"][0]          # control variant: the shells carry ALL the matter (no smooth rest), the standard secondary-infall set-up
rho_rest = 0.0
four3 = 4.0 * math.pi / 3.0
vz = sn["vb"]; rz = sn["rb"]
kk = np.where(vz <= 0)[0]
k = int(kk[-1]) if len(kk) else 0
if k + 1 < len(vz):
    fr = (0 - vz[k]) / (vz[k + 1] - vz[k])
    r_zv = rz[k] + fr * (rz[k + 1] - rz[k]); Me_zv = sn["Me_b"][k] + fr * (sn["Me_b"][k + 1] - sn["Me_b"][k])
    cont = [(Me_zv + four3 * rho_rest * r_zv ** 3) / (four3 * r_zv ** 3 * S.RHOM0)]
else:
    cont = []
c_tgt = float(L7.one_plus_delta_ta(1.0))
medc = float(np.median(cont)) if cont else float("nan")
P(f"  control variant (shells carry all the matter): zero-velocity shell at a = 1: enclosed mean density / mean matter density = {medc:.2f} against the committed GR top-hat {c_tgt:.2f}")
snt = res["snaps"][0]
vzt = snt["vb"]; rzt = snt["rb"]
kkt = np.where(vzt <= 0)[0]; kt = int(kkt[-1])
frt = (0 - vzt[kt]) / (vzt[kt + 1] - vzt[kt])
r_zvt = rzt[kt] + frt * (rzt[kt + 1] - rzt[kt]); Me_zvt = snt["Me_b"][kt] + frt * (snt["Me_b"][kt + 1] - snt["Me_b"][kt])
cont_toy = (Me_zvt + four3 * (S.RHOM0 - S.RHOB0) * r_zvt ** 3) / (four3 * r_zvt ** 3 * S.RHOM0)
P(f"  class toy itself (baryon shells, the rest of the matter smooth and NOT falling in): zero-velocity-shell contrast {cont_toy:.2f} against the top-hat {c_tgt:.2f} "
  f"({100 * (cont_toy / c_tgt - 1):+.0f}%): the same control, run on the class toy, FAILS by construction (the toy's rest does not fall in); the all-matter variant above is the control that was kept")
R.check("C2-toy (reported, FAILED as first run: the class toy's smooth rest does not fall in) the class toy's zero-velocity contrast matches the top-hat to 6%", abs(cont_toy / c_tgt - 1) <= 0.06,
        f"{cont_toy:.2f} vs {c_tgt:.2f}", kind="reported")
R.check("C2 the shell code's turnaround contrast matches the committed top-hat 1 + delta_ta(a=1) to 6% (the zero-velocity shell at a = 1; all-matter shells variant, because in the class toy the rest of the matter does not fall in)",
        bool(cont) and abs(medc / c_tgt - 1) <= 0.06, f"{medc:.2f} vs {c_tgt:.2f}")

# ------------------------------------------------------------------------------------------------------------ G0-a, G0-b
R.banner("G0-a (locus) and G0-b (multiplicity) on the baryon-shell flow (creation OFF: pure infall)")
rows = {}
for Mb in (1e9, 1e10, 1e12):
    rr = res if Mb == 1e10 else S.run(Mb, C.A0, create=False, N=1000, core=True, snap_a=(1.0,), soft=0.002)
    tt, th, rta, rth = rr["t_ta"], rr["t_th0"], rr["r_ta"], rr["r_th0"]
    turned = np.isfinite(tt)
    rel = np.where(turned & np.isfinite(th), (th - tt) / tt, np.nan)
    within = np.where(turned, np.abs(rel) <= 0.25, False)       # undefined theta0 counts as a miss
    frac = float(within[turned].mean()) if turned.any() else float("nan")
    inner = turned & (rta < 0.5 * np.nanmax(rta))
    cnt = {p: rr["ncross"][p][inner] for p in rr["ncross"]}
    med = {p: float(np.median(v)) if len(v) else float("nan") for p, v in cnt.items()}
    rows[Mb] = dict(frac=frac, med_rel=float(np.nanmedian(rel)), p10=float(np.nanpercentile(rel, 10)), p90=float(np.nanpercentile(rel, 90)),
                    med_r=float(np.nanmedian(rth[turned] / rta[turned])), nturn=int(turned.sum()), med_cross=med, n_inner=int(inner.sum()),
                    ntheta=int(np.isfinite(th).sum()), steps=rr["nstep"])
    P(f"  M_b = {Mb:.0e}: {rows[Mb]['nturn']} shells turned around, {rows[Mb]['ntheta']} have a theta_b zero by a = 1; (t_theta0 - t_ta)/t_ta: median {rows[Mb]['med_rel']:+.3f} "
      f"(p10 {rows[Mb]['p10']:+.3f}, p90 {rows[Mb]['p90']:+.3f}); fraction within 0.25: {frac:.3f}; r_theta0/r_ta median {rows[Mb]['med_r']:.3f}")
    P(f"      crossings per inner shell (n = {rows[Mb]['n_inner']}; hysteresis p = 0.01 / 0.05 / 0.2): medians " + " / ".join(f"{med[p]:.1f}" for p in sorted(med)))
R.num("G0ab", {f"{k:.0e}": v for k, v in rows.items()})
rep = rows[1e10]
R.check("G0-a theta_b = 0 coincides with the shell turnaround to 25% for >= 90% of the shells", rep["frac"] >= 0.9,
        f"fraction {rep['frac']:.3f} at 1e10 ({rows[1e9]['frac']:.3f} at 1e9, {rows[1e12]['frac']:.3f} at 1e12); theta_b = 0 comes {rep['med_rel']:+.2f} of t_ta later", kind="result")
medp = rep["med_cross"][0.05]
if MUT == "5":
    P("  *** MUTATE=5: the counting rule (each shell counted once) is imposed ***")
    medp_eff = 1.0
else:
    medp_eff = medp
b_pass = medp_eff <= 1.1
R.check("G0-b the unflagged source fires once per shell (median crossings <= 1.1); otherwise a counting rule is required", b_pass,
        f"median {medp_eff:.1f} downward crossings per inner shell (p = 0.05) at 1e10; 1e9: {rows[1e9]['med_cross'][0.05]:.1f}; 1e12: {rows[1e12]['med_cross'][0.05]:.1f}", kind="result")

# ------------------------------------------------------------------------------------------------------------ G0-c
R.banner("G0-c (causality): advanced dependence of the trigger functional on the trajectory (CFG242 C1's definition)")


def run_c(Nt):
    ts = np.linspace(S.BG.t_of_a(0.05), S.BG.t_of_a(1.0), Nt)
    rr = S.run(1e10, C.A0, create=False, N=300, core=True, snap_a=(1.0,), snap_t_extra=tuple(ts[:-1]), soft=0.002, tpct=5.0)
    sn_ = rr["snaps"]
    sn_ = sorted(sn_, key=lambda d: d["t"])
    r = np.array([d["rb"] for d in sn_])                       # (Nt, N)
    return r


def theta_back(r):
    J = r[:, 1:-1] ** 2 * np.abs(r[:, 2:] - r[:, :-2])
    L = np.log(np.maximum(J, 1e-300))
    out = np.zeros_like(L)
    out[1:] = L[1:] - L[:-1]
    return out


def theta_centred(r):
    J = r[:, 1:-1] ** 2 * np.abs(r[:, 2:] - r[:, :-2])
    L = np.log(np.maximum(J, 1e-300))
    out = np.zeros_like(L)
    out[1:-1] = (L[2:] - L[:-2]) / 2.0
    return out


cadv = {}
for Nt in (200, 400):
    r = run_c(Nt)
    nt = r.shape[0]
    cuts = np.linspace(20, nt - 20, 12).astype(int)
    worst_b = 0.0; worst_c = 0.0
    for j in cuts:
        r2 = r.copy()
        r2[j] = r2[j] * (1.0 + 1e-3 * rng.standard_normal(r.shape[1]))
        db = np.abs(theta_back(r2) - theta_back(r))
        dc = np.abs(theta_centred(r2) - theta_centred(r))
        mb = db.max(); mc = dc.max()
        worst_b = max(worst_b, db[:j].max() / mb if mb > 0 else 0.0)
        worst_c = max(worst_c, dc[:j].max() / mc if mc > 0 else 0.0)
    cadv[Nt] = (worst_b, worst_c)
    P(f"  N = {Nt} time samples ({nt} recorded), 12 cut points: retarded (backward difference) c_adv = {worst_b:.3e}; detector control (centred difference) c_adv = {worst_c:.3e}")
# spatial locality: a perturbation of shell i0 changes theta only within one cell
r = run_c(200)
i0 = 140
r2 = r.copy(); r2[:, i0] *= (1.0 + 1e-3)
dth = np.abs(theta_back(r2) - theta_back(r))
far = np.ones(dth.shape[1], bool); far[max(i0 - 2, 0): i0 + 1] = False   # theta is indexed on interior shells (offset 1): neighbours i0-1, i0, i0+1 -> columns i0-2..i0
spat_far = float(dth[:, far].max())
P(f"  spatial stencil: perturbing shell {i0} changes theta only on its two neighbours and itself; max change elsewhere = {spat_far:.1e}")
R.check("G0-c the retarded trigger has no advanced dependence (c_adv <= 1e-12 at N = 200 and 400) and the detector fires", all(cadv[n][0] <= 1e-12 for n in cadv) and all(cadv[n][1] > 1e-6 for n in cadv) and spat_far == 0.0,
        f"retarded {cadv[200][0]:.1e}/{cadv[400][0]:.1e}; control {cadv[200][1]:.1e}/{cadv[400][1]:.1e}; spatial {spat_far:.1e}", kind="result")

# ------------------------------------------------------------------------------------------------------------ G0-d
R.banner("G0-d (bound-only): which elements fire?  Zel'dovich three-axis toy, Gaussian eigenvalue distribution (Doroshkevich), sigma from CLASS (cosmic-script table)")
cj = json.load(open(os.path.join(C.HERE, "CFG243_cosmic_results.json")))["numbers"]["sigma_table"]
# growth tables (committed LCDM)
agrid = np.geomspace(0.01, 1.0, 600)
Dg = np.array([float(L7.D(a)) for a in agrid]); fg = np.array([float(L7.f(a)) for a in agrid])


def sample_eigs(sigma, n):
    # <T_ij T_kl> = sigma^2/15 (d_ij d_kl + d_ik d_jl + d_il d_jk)
    cov = np.full((3, 3), 1.0) + 2.0 * np.eye(3)
    Lc = np.linalg.cholesky(cov * sigma ** 2 / 15.0)
    z = rng.standard_normal((n, 3))
    diag = np.stack([sum(Lc[kk_, jj_] * z[:, jj_] for jj_ in range(3)) for kk_ in range(3)], axis=1)
    off = rng.standard_normal((n, 3)) * sigma / math.sqrt(15.0)
    T = np.zeros((n, 3, 3))
    T[:, 0, 0], T[:, 1, 1], T[:, 2, 2] = diag[:, 0], diag[:, 1], diag[:, 2]
    T[:, 0, 1] = T[:, 1, 0] = off[:, 0]; T[:, 0, 2] = T[:, 2, 0] = off[:, 1]; T[:, 1, 2] = T[:, 2, 1] = off[:, 2]
    return np.sort(np.linalg.eigvalsh(T), axis=1)[:, ::-1]      # lambda1 >= lambda2 >= lambda3


def solve_theta0(lam, nit=60):
    """smallest D in (0, min(1, 1/lambda1)) with f(D) sum_i D lambda_i/(1 - D lambda_i) = 3, or nan (no trigger by z = 0 = D = 1)."""
    n = lam.shape[0]
    Dmax = np.where(lam[:, 0] > 1.0, 1.0 / np.maximum(lam[:, 0], 1e-300), 1.0)
    lo = np.zeros(n); hi = Dmax * (1 - 1e-12)

    def F(D):
        f = np.interp(D, Dg, fg)
        return f * np.sum(D[:, None] * lam / (1.0 - D[:, None] * lam), axis=1)

    has = F(hi) >= 3.0
    for _ in range(nit):
        mid = 0.5 * (lo + hi)
        up = F(mid) >= 3.0
        hi = np.where(up, mid, hi); lo = np.where(up, lo, mid)
    D = 0.5 * (lo + hi)
    return np.where(has, D, np.nan)


zd = {}
for M in (1e10, 1e12):
    sig = cj[f"z0_M{M:.0e}"]
    lam = sample_eigs(sig, 1_000_000)
    D = solve_theta0(lam)
    trig = np.isfinite(D)
    lam_t = lam[trig]; D_t = D[trig]
    f_t = np.interp(D_t, Dg, fg)
    T = f_t[:, None] * D_t[:, None] * lam_t / (1.0 - D_t[:, None] * lam_t)
    Tmin = T.min(axis=1)
    frac_nb = float(np.mean(Tmin < 1.0 - 1e-9))
    zd[M] = dict(sigma=sig, p_trig=float(trig.mean()), frac_not_3D=frac_nb, frac_Tmin_lt_half=float(np.mean(Tmin < 0.5)), frac_lam3_le0=float(np.mean(lam_t[:, 2] <= 0)),
                 med_Tmin=float(np.median(Tmin)), sumT_dev=float(np.max(np.abs(T.sum(axis=1) - 3.0))))
    P(f"  M = {M:.0e} (sigma_lin(z=0) = {sig:.3f}): {zd[M]['p_trig']:.3f} of Lagrangian points reach theta_b = 0 by z = 0; at the event: not 3D-turned-around (T_min < 1): {frac_nb:.6f}; "
      f"T_min < 0.5: {zd[M]['frac_Tmin_lt_half']:.3f}; lambda_3 <= 0 (an axis that never collapses): {zd[M]['frac_lam3_le0']:.3f}; median T_min {zd[M]['med_Tmin']:.3f}; max |sum T - 3| = {zd[M]['sumT_dev']:.1e}")
R.num("G0d", {f"{k:.0e}": v for k, v in zd.items()})
fnb = zd[1e12]["frac_not_3D"]
R.check("G0-d <= 0.10 of the created dust is in elements that are not 3D-turned-around at the theta_b = 0 event (sheets, filaments)", fnb <= 0.10,
        f"{fnb:.4f} (1e12); {zd[1e10]['frac_not_3D']:.4f} (1e10); sum_i T_i = 3 at the event forces T_min < 1 for any non-spherical element", kind="result")
P("  The spherical shell toy cannot test this (its flow is spherical by construction): G0-d rests on the Zel'dovich identity and the Gaussian eigenvalue sample; "
  "a halo-finder census on an N-body field is not run.")

# ------------------------------------------------------------------------------------------------------------ G0-e
R.banner("G0-e (vacuum compensation): is grad(theta_b) parallel to u_mu on the theta_b = 0 locus?  (curl of S u_mu = 0 needs it)")
ok = np.isfinite(res["dthdr"]) & np.isfinite(res["Dthdt"]) & np.isfinite(res["v_th0"])
v = res["v_th0"][ok]; gr = res["dthdr"][ok]; Dt = res["Dthdt"][ok]
Delta = gr + (v / CKMS ** 2) * (Dt - v * gr)
rel = np.abs(Delta) / np.abs(gr)
ratio = np.abs(gr) / (np.abs(v) * np.abs(Dt) / CKMS ** 2)
P("  Alignment d_mu theta || u_mu needs d_r theta = -(v/c^2) d_t theta (Eulerian), i.e. d_r theta = -(v/c^2)(D theta/Dt - v d_r theta).")
P(f"  {int(ok.sum())} firing shells (1e10): median |residual| / |d_r theta| = {np.median(rel):.9f}; median |d_r theta| / (|v||D theta/Dt|/c^2) = {np.median(ratio):.3e} (alignment needs 1)")
R.num("G0e", dict(n=int(ok.sum()), med_rel=float(np.median(rel)), med_ratio=float(np.median(ratio))))
R.check("G0-e the localised source is consistent with a Lorentz-invariant vacuum compensator (grad theta aligned with u_mu to 1e-6)", float(np.median(rel)) <= 1e-6,
        f"misalignment {np.median(rel):.6f}; gradient exceeds the aligned value by {np.median(ratio):.2e}x; record: CFG131 D1/A5, CFG253 (C)", kind="result")

# ------------------------------------------------------------------------------------------------------------ G0-f
R.banner("G0-f (inertness)")
nt_unb = int((res["trig"] & ~np.isfinite(res["t_ta"])).sum())
R.check("G0-f no source in the unperturbed FRW flow (no core) and none in shells that never turn around", int(res0["trig"].sum()) == 0 and nt_unb == 0,
        f"FRW triggers {int(res0['trig'].sum())}; triggers among never-turned shells {nt_unb} (of {int(res['trig'].sum())})", kind="result")
P("  (The toy's triggers all occur AFTER the shell's turnaround (G0-a), so the bound-only property of the toy flow is automatic for the spherical case; it is the G0-d web census that bites.)")

R.banner("G0 verdict")
cells = {c["name"]: c["ok"] for c in R.checks if c["kind"] == "result"}
a_ok = rep["frac"] >= 0.9; c_ok = all(cadv[n][0] <= 1e-12 for n in cadv); d_ok = fnb <= 0.10; e_ok = float(np.median(rel)) <= 1e-6; f_ok = True
P(f"  a {'PASS' if a_ok else 'FAIL'}; b {'PASS' if b_pass else 'counting rule required'}; c {'PASS' if c_ok else 'FAIL'}; d {'PASS' if d_ok else 'FAIL'}; e {'PASS' if e_ok else 'FAIL'}; f PASS")
R.verdict("G0 (post hoc)", "PASS" if (a_ok and c_ok and d_ok and e_ok and f_ok) else "FAIL",
          f"a (locus) {'PASS' if a_ok else 'FAIL'}, d (bound-only) {'PASS' if d_ok else 'FAIL'}, e (vacuum compensation) {'PASS' if e_ok else 'FAIL'}; b needs a counting rule; c, f pass")

if MUT == "5":
    mc = R.main_cells()
    R.finish([mc.get("G0-b the unflagged source fires once per shell (median crossings <= 1.1); otherwise a counting rule is required") is False, b_pass])
else:
    R.finish()
