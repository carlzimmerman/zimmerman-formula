#!/usr/bin/env python3
"""XF1 Stage B: axisymmetric (ln r, theta) flow of the khronon charge past a hosted body, the Stage A system (A1) evolved
to steady state. Lineage: closure_2026_11_06/MS3_moving_sun_light/hydro_ms3.py (AC15 S2 -> AC24 -> MS3); diff committed
as xf1_hydro.diff. Criteria: FROZEN_CRITERIA.md (8b99d12c42).

Code units: L0 (= the body's Plummer scale a for B1-B4, = R_A = 2GM/V^2 for the point Sun B5), V, rho_h.
  gravity of the body   -gpar m(r)/r^2,  gpar = GM/(L0 V^2) (= 1/2 for B5), m(r) the Plummer enclosed fraction (1 for B5)
  stiffness (AC15)      h = q/M^2, p = q^2/(2 M^2), M = M_inf = V/c_s
  Stage A extras        + grad chi (Legendre force)  - grad Phi_q (gravity of the anomalous charge), both from dq = q - 1 + s,
                        kernel xf1_field.Forces (coupling kappa_q, anisotropy x_e); updated every --nforce steps; --reduced drops them (AC15's system)
  tracer s              the signed static phantom of the HEDGEHOG start (galaxy cells), advected with the frame; the physical
                        charge is q + s; the stiffness acts on q (p(q + s) - p(q) <= 1e-9 of the inertia in every galaxy cell)
Cells, rows, footings and V readings come from xf1_cells.json (xf1_cells.py).

  python3 xf1_hydro.py --cell B1 --foot canonical --row 0 --vi 1 --start uniform --res coarse [--bc transmit] [--reduced]
                       [--nograv] [--nowind] [--tend T] [--rin R] [--rout R] [--nforce N]
Writes parts/<tag>/{state.npz (checkpoint), snap_XX.npz, static.npz, done.json}. SIGTERM -> checkpoint and exit 3; rerun resumes.
One thread, RSS guard, nice it from the launcher. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, time, signal, argparse, resource, math
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import xf1_field as XF                                                        # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--cell", required=True, choices=("B1", "B2", "B3", "B4", "B5"))
ap.add_argument("--foot", required=True, choices=("canonical", "alt"))
ap.add_argument("--row", type=int, default=0); ap.add_argument("--vi", type=int, default=1, choices=(0, 1))
ap.add_argument("--bc", choices=("absorb", "reflect", "transmit"), default="transmit")
ap.add_argument("--start", choices=("uniform", "hedgehog"), required=True)
ap.add_argument("--res", choices=("coarse", "medium", "fine"), required=True)
ap.add_argument("--reduced", action="store_true", help="AC15's equations: no Legendre force, no charge self-gravity")
ap.add_argument("--nograv", action="store_true"); ap.add_argument("--nowind", action="store_true")
ap.add_argument("--tend", type=float, default=None); ap.add_argument("--rin", type=float, default=None); ap.add_argument("--rout", type=float, default=None)
ap.add_argument("--nforce", type=int, default=None); ap.add_argument("--chunk", type=int, default=64); ap.add_argument("--rss_mb", type=float, default=900.0)
ap.add_argument("--hhstart", choices=("d10", "linear"), default=None, help="HEDGEHOG start of the galaxy cells: the record's nonlinear static EFE phantom (D10, default with the wind) or the code's linear fixed point (default for --nowind, KB2)")
ap.add_argument("--suffix", default=""); ap.add_argument("--Mover", type=float, default=None, help="override M_inf (KB1: AC15's exact M)")
a = ap.parse_args()

CELLS = json.load(open(os.path.join(HERE, "xf1_cells.json"))); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
cell = CELLS["cells"][a.foot][a.cell]; row = cell["rows"][a.row]; dv = row["derived"][a.vi]
POINT = row["a_pc"] <= 0
GPAR = float(dv["gpar"]); MINF = float(dv["M_inf"]) if a.Mover is None else float(a.Mover); XE = float(row["x_e"]); KQ = float(dv["kappa_q"])
A_CODE = 0.0 if POINT else 1.0
HHSTART = a.hhstart if a.hhstart is not None else ("linear" if a.nowind else "d10")
DEF = {"B5": (2.0, 2000.0, 3000.0), "B1": (0.05, 50.0, 20.0), "B2": (0.05, 50.0, 20.0), "B3": (0.05, 100.0, 50.0), "B4": (0.05, 100.0, 50.0)}[a.cell]
RIN = a.rin if a.rin is not None else DEF[0]; ROUT = a.rout if a.rout is not None else DEF[1]; TEND = a.tend if a.tend is not None else DEF[2]
NFORCE = a.nforce if a.nforce is not None else 10
tag = f"{a.cell}_{a.foot}_r{a.row}_V{a.vi}_{a.bc}_{a.start}_{a.res}" + ("_REDUCED" if a.reduced else "") + ("_NOGRAV" if a.nograv else "") \
      + ("_NOWIND" if a.nowind else "") + (f"_t{TEND:g}" if TEND != DEF[2] else "") + (f"_M{a.Mover:g}" if a.Mover is not None else "") + (f"_{HHSTART}" if (a.start == "hedgehog" and not POINT) else "") + a.suffix
D = os.path.join(HERE, "parts", tag); os.makedirs(D, exist_ok=True)
if os.path.exists(os.path.join(D, "done.json")):
    print("already done", tag); sys.exit(0)
PAR = dict(tag=tag, cell=a.cell, foot=a.foot, row=a.row, row_name=row["name"], vi=a.vi, V_kms=dv["V_kms"], gpar=GPAR, M_inf=MINF, x_e=XE, kappa_q=KQ,
           a_code=A_CODE, L0_pc=dv["L0_pc"], R_A_pc=dv["R_A_pc"], r_read_code=[r_ / dv["L0_pc"] for r_ in row["r_read_pc"]], rin=RIN, rout=ROUT, tend=TEND,
           reduced=a.reduced, nograv=a.nograv, nowind=a.nowind, bc=a.bc, start=a.start, res=a.res, nforce=NFORCE, hhstart=HHSTART)

M2 = MINF ** 2
dln, NT = {"coarse": (0.05, 80), "medium": (0.025, 160), "fine": (0.0125, 320)}[a.res]
NR = int(round(np.log(ROUT / RIN) / dln))
re = RIN * np.exp(dln * np.arange(NR + 1))                # radial edges
te = np.linspace(0, np.pi, NT + 1)
G = 2
lr = np.log(RIN) + dln * (np.arange(-G, NR + G) + 0.5)
rcg = np.exp(lr)
dth = np.pi / NT
tcg = (np.arange(-G, NT + G) + 0.5) * dth
Rg, Tg = np.meshgrid(rcg, tcg, indexing="ij")
rm, rp = re[:-1][:, None], re[1:][:, None]
cm, cp = np.cos(te[:-1])[None, :], np.cos(te[1:])[None, :]
VOL = (rp ** 3 - rm ** 3) / 3 * (cm - cp)
RC = 0.75 * (rp ** 4 - rm ** 4) / (rp ** 3 - rm ** 3) * np.ones_like(cm)   # volume centroid radius
TC = 0.5 * (te[:-1] + te[1:])[None, :] * np.ones_like(rm)
AR = (re ** 2)[:, None] * (cm - cp)
AT = np.sin(te)[None, :] * ((rp ** 2 - rm ** 2) / 2)
SRC_R = (AR[1:] - AR[:-1]) / VOL
SRC_T = (AT[:, 1:] - AT[:, :-1]) / VOL
MFRAC = XF.plummer_mass_frac(A_CODE)
gsign = 0.0 if a.nograv else 1.0
GRID = XF.Grid(re, te)
FV = XF.FVForces(GRID, XE, KQ)                             # one FV operator family for the body, the static start and the two Stage A forces
GRAV_T = np.zeros((NR, NT))
if POINT:
    GRAV = gsign * GPAR * MFRAC(RC) / RC ** 2             # inward point-mass gravity at the centroids (AC15: 0.5/RC^2, bitwise)
    RHO_B = np.zeros((NR, NT))
else:
    RHO_B = 4 * np.pi * GPAR / KQ * (3 / (4 * np.pi)) * (1 + GRID.rc[:, None] ** 2) ** (-2.5) * np.ones((1, NT))   # Plummer, rho_h units
    F_IN = GPAR * float(MFRAC(re[0])) / re[0] ** 2          # the body's flux through the excised inner face (its enclosed mass)
    PHI_B, gbr, gbt = FV.body(RHO_B, F_IN)
    GRAV = gsign * gbr; GRAV_T = gsign * gbt              # inward body gravity (radial) and its theta part from the FV solve (consistent with the static start)
    GRAV_ANALYTIC_MAXREL = float(np.max(np.abs(gbr[:, 0] - GPAR * MFRAC(GRID.rc) / GRID.rc ** 2) / (GPAR * MFRAC(GRID.rc) / GRID.rc ** 2)))
I = (slice(G, G + NR), slice(G, G + NT))
_tm, _tp = te[:-1], te[1:]
SC = ((_tp - _tm) / 2 - (np.sin(2 * _tp) - np.sin(2 * _tm)) / 4) / (np.cos(_tm) - np.cos(_tp))
CC = ((np.sin(_tp) ** 2 - np.sin(_tm) ** 2) / 2) / (np.cos(_tm) - np.cos(_tp))
SCg = np.concatenate([-SC[:G][::-1], SC, -SC[-G:][::-1]]); CCg = np.concatenate([CC[:G][::-1], CC, CC[-G:][::-1]])
SING = np.ones_like(Tg) * SCg[None, :]
wind_u = -CCg; wind_v = np.abs(SCg)
SINF = np.concatenate([np.zeros(G - 2), np.sin(te), np.zeros(G - 2)])
up_mask = np.cos(tcg) > 0
FORCES_ON = not (a.reduced or a.nograv)


def hedgehog_q(r):
    return 1.0 + M2 * GPAR / r                            # AC15: gamma q = c^2 + Phi_N -> q/rho0 = 1 + M^2 GM/(r V^2)


# static start of the galaxy cells: the record's nonlinear static EFE phantom (D10, A2) or the code's linear fixed point (A1h), plus
# the r^-3 continuation into the outer ghosts
S_STATIC = np.zeros((NR, NT)); S_GHOST = np.zeros((G, NT + 2 * G)); STATIC_INFO = None
if a.start == "hedgehog" and not POINT:
    t0_ = time.monotonic()
    s_lin, phi_t = FV.static_start(RHO_B, F_IN)
    PCm = 3.0856775814913673e16; MSUNkg = 1.989e30
    s_d10, info_d10 = XF.d10_static_phantom(GRID, float(row["y_plummer"]), XE, float(row["Lam_floor"]), float(CELLS["a0"][a.foot]), row["a_pc"] * PCm,
                                            row["rho_h_Msun_pc3"] * MSUNkg / PCm ** 3, REPO)
    S_STATIC = (s_d10 if HHSTART == "d10" else s_lin).copy()
    fr_, ft_, _ = FV.frame_forces(s_lin)
    STATIC_INFO = dict(hhstart=HHSTART, linear=dict(s_min=float(s_lin.min()), s_max=float(s_lin.max()),
                       fixed_point_residual=float(np.sqrt(np.mean((fr_ - GRAV) ** 2 + (ft_ - GRAV_T) ** 2)) / np.max(GRAV))), d10=info_d10,
                       min_total_charge=float(1 + S_STATIC.min()), kernel_extrapolated=bool(1 + S_STATIC.min() <= 0), wall_s=time.monotonic() - t0_,
                       body_gravity_FV_vs_analytic_maxrel=GRAV_ANALYTIC_MAXREL)
    S_GHOST = np.zeros((G, NT))
    for k in range(G):
        S_GHOST[k] = S_STATIC[-1] * (RC[-1, 0] / rcg[G + NR + k]) ** 3
    S_GHOST = np.concatenate([S_GHOST[:, :G][:, ::-1], S_GHOST, S_GHOST[:, -G:][:, ::-1]], axis=1)   # theta-ghost padding (even)
    np.savez(os.path.join(D, "static.npz"), s=S_STATIC, s_linear=s_lin, s_d10=s_d10, re=re, te=te, info=json.dumps(STATIC_INFO))
    print(f"{tag} static start: {STATIC_INFO}", flush=True)


def bc(W):
    q, u, v, c = W
    for k in range(G):                                    # theta axes: reflect v, even for the rest
        for f_ in (q, u, c):
            f_[:, G - 1 - k] = f_[:, G + k]; f_[:, G + NT + k] = f_[:, G + NT - 1 - k]
        v[:, G - 1 - k] = -v[:, G + k]; v[:, G + NT + k] = -v[:, G + NT - 1 - k]
    for k in range(G):                                    # inner
        q[G - 1 - k] = q[G + k]; v[G - 1 - k] = v[G + k]; c[G - 1 - k] = c[G + k]
        if a.bc == "reflect":
            u[G - 1 - k] = -u[G + k]
        elif a.bc == "absorb":
            u[G - 1 - k] = np.minimum(u[G], 0.0)
        else:                                             # transmit: q log-linear (index capped at 2), u, v, c zero-gradient
            sl_ = np.log(np.maximum(q[G + 1], 1e-14) / np.maximum(q[G], 1e-14))
            sl_ = np.clip(sl_, -2 * dln, 2 * dln)
            q[G - 1 - k] = q[G] * np.exp(-(k + 1) * sl_); v[G - 1 - k] = v[G]; u[G - 1 - k] = u[G]; c[G - 1 - k] = c[G]
    for k in range(G):                                    # outer
        i = G + NR + k
        if a.nowind:
            q[i] = hedgehog_q(rcg[i]) if (POINT and a.start == "hedgehog") else 1.0
            u[i] = 0.0; v[i] = 0.0; c[i] = S_GHOST[k] / q[i]
        else:
            q[i] = np.where(up_mask, 1.0, q[G + NR - 1]); u[i] = np.where(up_mask, wind_u, np.maximum(u[G + NR - 1], 0.0))
            v[i] = np.where(up_mask, wind_v, v[G + NR - 1]); c[i] = np.where(up_mask, 0.0, c[G + NR - 1])
    return W


def minmod(a_, b_):
    return np.where(a_ * b_ > 0, np.sign(a_) * np.minimum(np.abs(a_), np.abs(b_)), 0.0)


def hll(qL, uL, vL, qR, uR, vR, cL=None, cR=None):
    """normal velocity u, tangential v; optional tracer concentration c (upwinded by the mass flux)."""
    cs_L = np.sqrt(qL / M2); cs_R = np.sqrt(qR / M2)
    SL = np.minimum(uL - cs_L, uR - cs_R); SR = np.maximum(uL + cs_L, uR + cs_R)
    pL = qL ** 2 / (2 * M2); pR = qR ** 2 / (2 * M2)
    FL = (qL * uL, qL * uL * uL + pL, qL * uL * vL); FR = (qR * uR, qR * uR * uR + pR, qR * uR * vR)
    UL = (qL, qL * uL, qL * vL); UR = (qR, qR * uR, qR * vR)
    out = []
    for fl, fr, ul, ur in zip(FL, FR, UL, UR):
        fh = (SR * fl - SL * fr + SL * SR * (ur - ul)) / (SR - SL)
        out.append(np.where(SL >= 0, fl, np.where(SR <= 0, fr, fh)))
    if cL is not None:
        out.append(out[0] * np.where(out[0] > 0, cL, cR))
    return out


assert G == 2


def recon_(f, ax):
    d = np.diff(f, axis=ax)
    if ax == 0:
        s = minmod(d[:-1], d[1:])
        fL = f[1:-1] + 0.5 * s; fR = f[1:-1] - 0.5 * s
        return fL[:-1], fR[1:]
    s = minmod(d[:, :-1], d[:, 1:])
    fL = f[:, 1:-1] + 0.5 * s; fR = f[:, 1:-1] - 0.5 * s
    return fL[:, :-1], fR[:, 1:]


FR_R = np.zeros((NR, NT)); FR_T = np.zeros((NR, NT)); FPARTS = None       # Stage A extra forces at the centroids (code units)


def force_update(q, c):
    global FR_R, FR_T, FPARTS
    if not FORCES_ON:
        return
    dq = (q[I] - 1.0) + c[I] * q[I]
    FR_R, FR_T, FPARTS = FV.frame_forces(dq)


def rhs_chunked(W, CHK):
    W = bc(W)
    q, u, v, c = W
    out = [np.empty((NR, NT)) for _ in range(4)]
    js = slice(G, G + NT); st = slice(G - 2, G - 2 + NT + 1)
    for i0 in range(0, NR, CHK):
        i1 = min(NR, i0 + CHK)
        gs = slice(i0, i1 + 2 * G)
        qL, qR = recon_(q[gs], 0); uL, uR = recon_(u[gs], 0); vL, vR = recon_(v[gs], 0); cL, cR = recon_(c[gs], 0)
        Fr = hll(np.maximum(qL[:, js], 1e-14), uL[:, js], vL[:, js], np.maximum(qR[:, js], 1e-14), uR[:, js], vR[:, js], cL[:, js], cR[:, js])
        ts = slice(G + i0, G + i1)
        qL, qR = recon_(q[ts], 1); uL, uR = recon_(u[ts], 1); cL, cR = recon_(c[ts], 1)
        vL, vR = recon_(v[ts] / SING[ts], 1)
        vL = vL * SINF[None, :]; vR = vR * SINF[None, :]
        Ft = hll(np.maximum(qL[:, st], 1e-14), vL[:, st], uL[:, st], np.maximum(qR[:, st], 1e-14), vR[:, st], uR[:, st], cL[:, st], cR[:, st])
        qi, ui, vi = q[ts, js], u[ts, js], v[ts, js]
        pi_ = qi ** 2 / (2 * M2)
        ar, at_, vo, rc_ = AR[i0:i1 + 1], AT[i0:i1], VOL[i0:i1], RC[i0:i1]
        out[0][i0:i1] = -(Fr[0][1:] * ar[1:] - Fr[0][:-1] * ar[:-1] + Ft[0][:, 1:] * at_[:, 1:] - Ft[0][:, :-1] * at_[:, :-1]) / vo
        out[1][i0:i1] = -(Fr[1][1:] * ar[1:] - Fr[1][:-1] * ar[:-1] + Ft[2][:, 1:] * at_[:, 1:] - Ft[2][:, :-1] * at_[:, :-1]) / vo \
            + qi * vi * vi / rc_ + pi_ * SRC_R[i0:i1] - qi * GRAV[i0:i1] + qi * FR_R[i0:i1]
        out[2][i0:i1] = -(Fr[2][1:] * ar[1:] - Fr[2][:-1] * ar[:-1] + Ft[1][:, 1:] * at_[:, 1:] - Ft[1][:, :-1] * at_[:, :-1]) / vo \
            - qi * ui * vi / rc_ + pi_ * SRC_T[i0:i1] - qi * GRAV_T[i0:i1] + qi * FR_T[i0:i1]
        out[3][i0:i1] = -(Fr[3][1:] * ar[1:] - Fr[3][:-1] * ar[:-1] + Ft[3][:, 1:] * at_[:, 1:] - Ft[3][:, :-1] * at_[:, :-1]) / vo
    return out


def to_prim(U):
    q = np.maximum(U[0], 1e-14)
    return q, U[1] / q, U[2] / q, U[3] / q


DT_CAP = 0.4 * float(np.min(re[1:] - re[:-1]))          # the wind-speed CFL (|w| = V): binds only when the frame is at rest (no-wind holds)


def dt_of(W):
    q, u, v = (x_[I] for x_ in W[:3])
    cs = np.sqrt(q / M2)
    drr = (re[1:] - re[:-1])[:, None]
    return min(0.4 * min(np.min(drr / (np.abs(u) + cs)), np.min(RC * dth / (np.abs(v) + cs))), DT_CAP)


# ---------------------------------------------------------------- init / resume
Wg = [np.zeros_like(Rg) for _ in range(4)]
ck = os.path.join(D, "state.npz")
if os.path.exists(ck):
    z_ = np.load(ck); U = [z_["q"], z_["mr"], z_["mt"], z_["s"]]; tnow = float(z_["t"]); nstep = int(z_["n"]); nsnap = int(z_["ns"])
    print(f"resume {tag} at t {tnow:.2f}", flush=True)
else:
    r2 = RC
    if a.start == "hedgehog" and POINT:
        q0 = hedgehog_q(r2)
    else:
        q0 = np.ones_like(r2)
    s0 = S_STATIC.copy() if (a.start == "hedgehog" and not POINT) else np.zeros_like(r2)
    if a.nowind:
        u0 = 0 * r2; v0 = 0 * r2
    else:
        u0 = -CC[None, :] * np.ones_like(r2); v0 = SC[None, :] * np.ones_like(r2)
    U = [q0.copy(), q0 * u0, q0 * v0, s0]; tnow = 0.0; nstep = 0; nsnap = 0

SNAPS = [TEND * f for f in (0.8, 0.85, 0.9, 0.95, 1.0)]
stop = {"flag": False}
signal.signal(signal.SIGTERM, lambda *_: stop.update(flag=True))


def save_ck():
    np.savez(ck + ".tmp.npz", q=U[0], mr=U[1], mt=U[2], s=U[3], t=tnow, n=nstep, ns=nsnap)
    os.replace(ck + ".tmp.npz", ck)


def full(Ui):
    q, u, v, c = to_prim(Ui)
    Wg[0][I] = q; Wg[1][I] = u; Wg[2][I] = v; Wg[3][I] = c
    return Wg


def force_diag():
    if not FORCES_ON or FPARTS is None:
        return dict(on=False)
    gr, gt, cr, ct = FPARTS
    fmax = float(np.max(np.hypot(FR_R, FR_T))); gmax = float(np.max(GRAV)) if gsign else 0.0
    return dict(on=True, max_force=fmax, max_force_over_max_grav=(fmax / gmax if gmax > 0 else None),
                max_grav_of_charge=float(np.max(np.hypot(gr, gt))), max_legendre=float(np.max(np.hypot(cr, ct))),
                max_force_over_V2_L0=fmax)


T0 = time.monotonic(); lastck = T0
W = full(U); force_update(W[0], W[3])
while nsnap < len(SNAPS):
    W = full(U)
    if nstep % NFORCE == 0:
        force_update(W[0], W[3])
    dt = min(dt_of(W), SNAPS[nsnap] - tnow)
    k1 = rhs_chunked(W, a.chunk)
    U1 = [U[k] + dt * k1[k] for k in range(4)]
    W = full(U1)
    k2 = rhs_chunked(W, a.chunk)
    U = [0.5 * (U[k] + U1[k] + dt * k2[k]) for k in range(4)]
    U[0] = np.maximum(U[0], 1e-14)
    tnow += dt; nstep += 1
    if not np.all(np.isfinite(U[0])) or not np.all(np.isfinite(U[3])):
        json.dump(dict(tag=tag, error="non-finite", t=tnow, n=nstep), open(os.path.join(D, "error.json"), "w")); sys.exit(2)
    if tnow >= SNAPS[nsnap] - 1e-12:
        q, u, v, c = to_prim(U)
        force_update(full(U)[0], full(U)[3])
        np.savez(os.path.join(D, f"snap_{nsnap:02d}.npz"), q=q, u=u, v=v, s=c * q, t=tnow, re=re, te=te, M=MINF, gpar=GPAR, xe=XE, kq=KQ,
                 a_code=A_CODE, fr=FR_R, ft=FR_T, par=json.dumps(PAR), fdiag=json.dumps(force_diag()))
        nsnap += 1; save_ck()
        print(f"{tag} snap {nsnap}/{len(SNAPS)} t {tnow:.2f} steps {nstep} wall {time.monotonic() - T0:.0f}s forces {force_diag()}", flush=True)
    if nstep % 2000 == 0:
        rss_ = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
        if rss_ > a.rss_mb:
            save_ck(); print(f"RSS GUARD: peak {rss_:.0f} MB > {a.rss_mb:.0f} MB, checkpointed", flush=True); sys.exit(4)
        if time.monotonic() - lastck > 120:
            save_ck(); lastck = time.monotonic()
        print(f"{tag} t {tnow:.3f} dt {dt:.2e} steps {nstep} wall {time.monotonic() - T0:.0f}s", flush=True)
    if stop["flag"]:
        save_ck(); print("SIGTERM: checkpointed", flush=True); sys.exit(3)
rss_ = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
json.dump(dict(tag=tag, t=tnow, steps=nstep, wall_s=time.monotonic() - T0, NR=NR, NT=NT, par=PAR, static=STATIC_INFO, forces=force_diag(),
               peak_rss_mb=rss_, args=vars(a)), open(os.path.join(D, "done.json"), "w"), indent=1, default=float)
print("done", tag, flush=True)
