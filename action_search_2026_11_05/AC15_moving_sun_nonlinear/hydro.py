#!/usr/bin/env python3
"""AC15 S2: axisymmetric (ln r, theta) barotropic flow of the khronon charge past the moving Sun.

Units: R_A = 2GM/V^2, V, rho0 (GM = 1/2). h = q / M^2, p = q^2 / (2 M^2). Wind w = -z at infinity
(upstream hemisphere = cos theta > 0). Criteria: FROZEN_CRITERIA.md (b089f97024).

  python3 hydro.py --M 234 --bc absorb --start uniform --res coarse [--mutate] [--nograv] [--nowind] [--tend T]

Writes parts/<tag>/{state.npz (checkpoint), snap_XX.npz, done.json}. SIGTERM -> checkpoint and exit 3;
rerun with the same arguments resumes. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time, signal, argparse
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--M", type=float, required=True)
ap.add_argument("--bc", choices=("absorb", "reflect", "transmit"), required=True)
ap.add_argument("--start", choices=("uniform", "hedgehog"), required=True)
ap.add_argument("--res", choices=("coarse", "medium"), required=True)
ap.add_argument("--mutate", action="store_true"); ap.add_argument("--nograv", action="store_true")
ap.add_argument("--nowind", action="store_true"); ap.add_argument("--tend", type=float, default=3000.0)
ap.add_argument("--rin", type=float, default=2.0); ap.add_argument("--rout", type=float, default=2000.0)
a = ap.parse_args()
tag = f"M{a.M:g}_{a.bc}_{a.start}_{a.res}" + ("_MUTATE" if a.mutate else "") + ("_NOGRAV" if a.nograv else "") \
      + ("_NOWIND" if a.nowind else "") + (f"_t{a.tend:g}" if a.tend != 3000.0 else "")
D = os.path.join(HERE, "parts", tag); os.makedirs(D, exist_ok=True)
if os.path.exists(os.path.join(D, "done.json")):
    print("already done", tag); sys.exit(0)

M2 = a.M ** 2
dln, NT = (0.05, 80) if a.res == "coarse" else (0.025, 160)
NR = int(round(np.log(a.rout / a.rin) / dln))
re = a.rin * np.exp(dln * np.arange(NR + 1))            # radial edges
te = np.linspace(0, np.pi, NT + 1)
G = 2
# ghost-extended centres
rc_in = np.sqrt(re[:-1] * re[1:])
lr = np.log(a.rin) + dln * (np.arange(-G, NR + G) + 0.5)
rcg = np.exp(lr)
dth = np.pi / NT
tcg = (np.arange(-G, NT + G) + 0.5) * dth
Rg, Tg = np.meshgrid(rcg, tcg, indexing="ij")
# interior geometry
rm, rp = re[:-1][:, None], re[1:][:, None]
cm, cp = np.cos(te[:-1])[None, :], np.cos(te[1:])[None, :]
VOL = (rp ** 3 - rm ** 3) / 3 * (cm - cp)
RC = 0.75 * (rp ** 4 - rm ** 4) / (rp ** 3 - rm ** 3) * np.ones_like(cm)   # volume centroid radius
TC = 0.5 * (te[:-1] + te[1:])[None, :] * np.ones_like(rm)
AR = (re ** 2)[:, None] * (cm - cp)                       # (NR+1, NT)
AT = np.sin(te)[None, :] * ((rp ** 2 - rm ** 2) / 2)      # (NR, NT+1)
SRC_R = (AR[1:] - AR[:-1]) / VOL
SRC_T = (AT[:, 1:] - AT[:, :-1]) / VOL
gsign = 0.0 if a.nograv else (-1.0 if a.mutate else 1.0)
GRAV = gsign * 0.5 / RC ** 2                             # inward acceleration magnitude GM/r^2, GM = 1/2
I = (slice(G, G + NR), slice(G, G + NT))
# cell averages over the theta cell weighted by sin(theta): <sin> and <cos> of a uniform wind (exact FV state at the axis)
_tm, _tp = te[:-1], te[1:]
SC = ((_tp - _tm) / 2 - (np.sin(2 * _tp) - np.sin(2 * _tm)) / 4) / (np.cos(_tm) - np.cos(_tp))
CC = ((np.sin(_tp) ** 2 - np.sin(_tm) ** 2) / 2) / (np.cos(_tm) - np.cos(_tp))
SCg = np.concatenate([-SC[:G][::-1], SC, -SC[-G:][::-1]]); CCg = np.concatenate([CC[:G][::-1], CC, CC[-G:][::-1]])
SING = np.ones_like(Tg) * SCg[None, :]                 # ghost-extended averaged sin(theta) (negative in axis ghosts)
wind_u = -CCg; wind_v = np.abs(SCg)
SINF = np.concatenate([np.zeros(G - 2), np.sin(te), np.zeros(G - 2)])  # face sin(theta) on the recon face index
up_mask = np.cos(tcg) > 0


def hedgehog_q(r):
    return 1.0 + M2 * 0.5 / r                            # gamma q = c^2 + Phi_N: q/rho0 = 1 + M^2 GM/r


def bc(W):
    q, u, v = W
    # theta axes: reflect v
    for k in range(G):
        q[:, G - 1 - k] = q[:, G + k]; u[:, G - 1 - k] = u[:, G + k]; v[:, G - 1 - k] = -v[:, G + k]
        q[:, G + NT + k] = q[:, G + NT - 1 - k]; u[:, G + NT + k] = u[:, G + NT - 1 - k]; v[:, G + NT + k] = -v[:, G + NT - 1 - k]
    # inner
    for k in range(G):
        q[G - 1 - k] = q[G + k]; v[G - 1 - k] = v[G + k]
        if a.bc == "reflect":
            u[G - 1 - k] = -u[G + k]
        elif a.bc == "absorb":
            u[G - 1 - k] = np.minimum(u[G], 0.0)
        else:                                            # transmit: zero-gradient, both signs
            # transmit: q extrapolated log-linearly in ln r (keeps a power-law atmosphere), u and v zero-gradient
            sl_ = np.log(np.maximum(q[G + 1], 1e-14) / np.maximum(q[G], 1e-14))
            sl_ = np.clip(sl_, -2 * dln, 2 * dln)        # power-law index capped at 2 (hedgehog is 1): no runaway on infall
            q[G - 1 - k] = q[G] * np.exp(-(k + 1) * sl_); v[G - 1 - k] = v[G]; u[G - 1 - k] = u[G]
    # outer
    for k in range(G):
        i = G + NR + k
        if a.nowind:
            q[i] = hedgehog_q(rcg[i]); u[i] = 0.0; v[i] = 0.0
        else:
            q[i] = np.where(up_mask, 1.0, q[G + NR - 1]); u[i] = np.where(up_mask, wind_u, np.maximum(u[G + NR - 1], 0.0))
            v[i] = np.where(up_mask, wind_v, v[G + NR - 1])
    return W


def minmod(a_, b_):
    return np.where(a_ * b_ > 0, np.sign(a_) * np.minimum(np.abs(a_), np.abs(b_)), 0.0)


def hll(qL, uL, vL, qR, uR, vR):
    """normal velocity u, tangential v."""
    cL = np.sqrt(qL / M2); cR = np.sqrt(qR / M2)
    SL = np.minimum(uL - cL, uR - cR); SR = np.maximum(uL + cL, uR + cR)
    pL = qL ** 2 / (2 * M2); pR = qR ** 2 / (2 * M2)
    FL = (qL * uL, qL * uL * uL + pL, qL * uL * vL); FR = (qR * uR, qR * uR * uR + pR, qR * uR * vR)
    UL = (qL, qL * uL, qL * vL); UR = (qR, qR * uR, qR * vR)
    out = []
    for fl, fr, ul, ur in zip(FL, FR, UL, UR):
        fh = (SR * fl - SL * fr + SL * SR * (ur - ul)) / (SR - SL)
        out.append(np.where(SL >= 0, fl, np.where(SR <= 0, fr, fh)))
    return out


def rhs(W):
    W = bc(W)
    q, u, v = W
    # radial reconstruction (faces between i and i+1 for interior faces G-1 .. G+NR-1)
    def recon(f, ax):
        d = np.diff(f, axis=ax)
        if ax == 0:
            s = minmod(d[:-1], d[1:])                     # slopes at cells 1..N-2
            fL = f[1:-1] + 0.5 * s; fR = f[1:-1] - 0.5 * s  # right/left face values of cells 1..N-2
            return fL[:-1], fR[1:]                        # left state, right state at faces between cells 1..N-2
        s = minmod(d[:, :-1], d[:, 1:])
        fL = f[:, 1:-1] + 0.5 * s; fR = f[:, 1:-1] - 0.5 * s
        return fL[:, :-1], fR[:, 1:]
    # radial: faces between ghost-index cells (G-1,G) ... (G+NR-1, G+NR): NR+1 faces; recon gives faces between cells 1..N-2
    qL, qR = recon(q, 0); uL, uR = recon(u, 0); vL, vR = recon(v, 0)
    sl = slice(G - 2, G - 2 + NR + 1)
    js = slice(G, G + NT)
    Fr = hll(np.maximum(qL[sl, js], 1e-14), uL[sl, js], vL[sl, js], np.maximum(qR[sl, js], 1e-14), uR[sl, js], vR[sl, js])
    qL, qR = recon(q, 1); uL, uR = recon(u, 1)
    vL, vR = recon(v / SING, 1)                      # reconstruct v/sin(theta): exact for uniform flow at the axis
    st = slice(G - 2, G - 2 + NT + 1)
    vL = vL * SINF[None, :]; vR = vR * SINF[None, :]
    is_ = slice(G, G + NR)
    Ft = hll(np.maximum(qL[is_, st], 1e-14), vL[is_, st], uL[is_, st], np.maximum(qR[is_, st], 1e-14), vR[is_, st], uR[is_, st])
    # Ft components: (mass, normal(theta)-mom, tangential(r)-mom)
    qi, ui, vi = q[I], u[I], v[I]
    pi_ = qi ** 2 / (2 * M2)
    dq = -(Fr[0][1:] * AR[1:] - Fr[0][:-1] * AR[:-1] + Ft[0][:, 1:] * AT[:, 1:] - Ft[0][:, :-1] * AT[:, :-1]) / VOL
    dmr = -(Fr[1][1:] * AR[1:] - Fr[1][:-1] * AR[:-1] + Ft[2][:, 1:] * AT[:, 1:] - Ft[2][:, :-1] * AT[:, :-1]) / VOL \
          + qi * vi * vi / RC + pi_ * SRC_R - qi * GRAV
    dmt = -(Fr[2][1:] * AR[1:] - Fr[2][:-1] * AR[:-1] + Ft[1][:, 1:] * AT[:, 1:] - Ft[1][:, :-1] * AT[:, :-1]) / VOL \
          - qi * ui * vi / RC + pi_ * SRC_T
    return dq, dmr, dmt


def to_prim(U):
    q = np.maximum(U[0], 1e-14)
    return q, U[1] / q, U[2] / q


def dt_of(W):
    q, u, v = (x_[I] for x_ in W)
    c = np.sqrt(q / M2)
    drr = (re[1:] - re[:-1])[:, None]
    return 0.4 * min(np.min(drr / (np.abs(u) + c)), np.min(RC * dth / (np.abs(v) + c)))


# ---------------------------------------------------------------- init / resume
Wg = [np.zeros_like(Rg) for _ in range(3)]
ck = os.path.join(D, "state.npz")
if os.path.exists(ck):
    z_ = np.load(ck); U = [z_["q"], z_["mr"], z_["mt"]]; tnow = float(z_["t"]); nstep = int(z_["n"]); nsnap = int(z_["ns"])
    print(f"resume {tag} at t {tnow:.2f}", flush=True)
else:
    r2, t2 = RC, TC
    if a.nowind:
        q0 = hedgehog_q(r2); u0 = 0 * r2; v0 = 0 * r2
    else:
        q0 = hedgehog_q(r2) if a.start == "hedgehog" else np.ones_like(r2)
        u0 = -CC[None, :] * np.ones_like(r2); v0 = SC[None, :] * np.ones_like(r2)
    U = [q0.copy(), q0 * u0, q0 * v0]; tnow = 0.0; nstep = 0; nsnap = 0

SNAPS = [a.tend * f for f in (0.8, 0.85, 0.9, 0.95, 1.0)] if a.tend >= 100 else [a.tend]
stop = {"flag": False}
signal.signal(signal.SIGTERM, lambda *_: stop.update(flag=True))


def save_ck():
    np.savez(ck + ".tmp.npz", q=U[0], mr=U[1], mt=U[2], t=tnow, n=nstep, ns=nsnap)
    os.replace(ck + ".tmp.npz", ck)


def full(Ui):
    q, u, v = to_prim(Ui)
    Wg[0][I] = q; Wg[1][I] = u; Wg[2][I] = v
    return Wg


T0 = time.monotonic(); lastck = T0
while nsnap < len(SNAPS):
    W = full(U)
    dt = min(dt_of(W), SNAPS[nsnap] - tnow)
    k1 = rhs(W)
    U1 = [U[k] + dt * k1[k] for k in range(3)]
    W = full(U1)
    k2 = rhs(W)
    U = [0.5 * (U[k] + U1[k] + dt * k2[k]) for k in range(3)]
    U[0] = np.maximum(U[0], 1e-14)
    tnow += dt; nstep += 1
    if not np.all(np.isfinite(U[0])):
        json.dump(dict(tag=tag, error="non-finite", t=tnow, n=nstep), open(os.path.join(D, "error.json"), "w")); sys.exit(2)
    if tnow >= SNAPS[nsnap] - 1e-12:
        q, u, v = to_prim(U)
        np.savez(os.path.join(D, f"snap_{nsnap:02d}.npz"), q=q, u=u, v=v, t=tnow, re=re, te=te, M=a.M)
        nsnap += 1; save_ck()
        print(f"{tag} snap {nsnap}/{len(SNAPS)} t {tnow:.1f} steps {nstep} wall {time.monotonic() - T0:.0f}s", flush=True)
    if nstep % 2000 == 0:
        if time.monotonic() - lastck > 120:
            save_ck(); lastck = time.monotonic()
        print(f"{tag} t {tnow:.2f} dt {dt:.2e} steps {nstep} wall {time.monotonic() - T0:.0f}s", flush=True)
    if stop["flag"]:
        save_ck(); print("SIGTERM: checkpointed", flush=True); sys.exit(3)
json.dump(dict(tag=tag, t=tnow, steps=nstep, wall_s=time.monotonic() - T0, NR=NR, NT=NT, args=vars(a)),
          open(os.path.join(D, "done.json"), "w"), indent=1)
print("done", tag, flush=True)
