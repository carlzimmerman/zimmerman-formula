#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR36 (part 2) -- THE TURNAROUND GATE AROUND BOUND SYSTEMS: KiDS, the Local Group (R0 and the MW-M31 timing), clusters and
splashback, the flagship and SPARC.  How far out is the matter flow around an isolated galaxy turned around, in the chain's
own law, once MOND acts only where it has turned around?

WHY.  Part 1 (XR36_gate_action.py) wrote the gate as an action term and found it ill posed when saturated; this part scores
the gate's PHENOMENOLOGY as a prescribed mask, to say whether a well-posed realisation would be worth finding.  KiDS needs
the phantom around isolated lenses out to ~1 Mpc at z = 0.25 (FP9/FP13/FP19; FP20's exact projector); the Local Group's
zero-velocity radius R0 = 0.93 +- 0.12 Mpc (FP18's bootstrap error) is the edge of its turned-around region.

THE MODEL (the chain's conventions, FP6/FP11/XR4).  A baryonic point mass M_b; the surrounding BARYON flow (the IGM; the gate
reads baryons, MS1 -- part 1 A7) as radial shells started on the Hubble flow at a = 0.02; convention A (point mass + Lambda,
the chain's R0 convention) and B (A + the smooth background's deceleration, FP11's B).  The phantom is the chain's P2 law in
its local QUMOND form, gated shell by shell (spherical symmetry makes the gate local): g = g_N [1 + W(theta) (nu_P2(y) - 1)],
so beyond the gate the enclosed phantom is Gauss-compensated to zero.  theta is read two ways:
  D1 (local, the formal theta_m = div u): theta = dv/dr + 2 v/r on the shells, per axis; a shell that has fallen through the
     centre (crossed) is virialised: theta = 0 there;
  D2 (the shell's own turnaround, spherical collapse's reading): theta = 3 v/r (the sphere-averaged divergence).
The gates: SHARP (W = 1 where theta <= 0; the candidate, no new constant), RAMP (W = clip(1 - theta/(c_w <K>_h)), c_w = 1 its
natural width: no constant), ALL3 (W = 1 only where every axis contracts: 3-D bound), and the H_K1 combination (the sharp D1 gate
times FP19's band-passed phantom, L = 2.9 Omega_L(<K>_h) Mpc).  The yield plays no role at z < 0.635.

PRE-DECLARED (written before this script's first run; the exploratory scratch runs listed under DISCLOSED came first).
 H1 [load-bearing; MUTATE must fail] THE TURNED-AROUND REGION IS SMALL.  Around isolated KiDS lenses at z = 0.25 (M_b = 10^10.5,
    10^11, 10^11.2; both footings; conventions A and B) the sharp local (D1) gate is on only inside r_on <= 0.6 Mpc and the
    zero-velocity radius is R0 <= 0.6 Mpc: MOND is NOT on out to 1 Mpc.  The reason is a bootstrap: the pull that would turn the
    outskirts around is the MOND pull the gate withholds until they have turned around; with baryons alone the Newtonian
    turnaround radius of 1e10.5-1e11.2 Msun is 0.2-0.5 Mpc.
 H2 KiDS (reported gate, FP20's exact projector, the FP13/FP19 setup, d chi^2 <= +9 against the isolated-P2 base): every
    turnaround-keyed variant FAILS (expected +400 to +1100 for sharp/all3 and >= +40 for the natural ramps).
 H3 THE LOCAL GROUP (reported gates): the sharp gate's R0 is the Newtonian baryons-only value (0.4-0.5 Mpc, conventions A/B)
    and FAILS 0.93 +- 0.12 low; the MW-M31 pair cannot turn around on Newtonian baryons before today, so the timing has no
    first-approach solution with M_b in FP11's window [1.145e11, 2.4e11] (expected timing mass > 1e12).
 H4 THE PINCER MAP (reported): widening the ramp (c_w = 1 ... 4) moves KiDS from failing to passing while the LG's R0 moves
    from ~0.6 to > 2 Mpc: no width passes both (FP18's KiDS-R0 pincer survives the gate).
 H5 (reported) MS1: a total-matter reading with an outstreaming daughter fraction f_d pulls the switch-on radius inward.
 H6 (reported) clusters: the gate is on to ~(1-3) R200 when the cluster keeps its carrier (FP16) and X-COP's radii
    (R500 ~ 0.65 R200) sit inside it, so X-COP's MOND share is unchanged; the first-caustic (splashback) radius moves by the
    printed amount.
 H7 (reported gates) the flagship (z = 2.5, y = 0.1) and SPARC (z = 0, y = 0.01-100, 1e9-1e12) sit inside the gate: the galaxy
    law is intact to <= 0.05 dex (flagship) and <= 0.01 dex (SPARC); UNCERTAIN for the flagship at z = 2.5 (young, small
    turned-around regions) and for SPARC's 1e12 outer points.
 H8 (reported gate; ADDED after the first debug run, on the coordinator's request, before any recorded run) WHICH FIELD THE
    KERNEL SEES.  Without a band-pass the kernel's argument carries the web's Newtonian field at the lens (~5e-3-1e-2 a0,
    unfiltered, all-matter), >= 10x KiDS's tolerance (FP1 E3: a few 1e-4 a0): the MOND external-field downturn fails KiDS
    even for the ungated law.  The free-fall-frame reading -- the kernel reads g - A_Omega, A_Omega the bound region's mean
    field -- removes the uniform part exactly (a tidal residual ~1e-4 a0 remains at r_on ~ 0.3 Mpc).  It does NOT come out
    of the gate's action: it has to be posited, as a per-region auxiliary vector A_Omega varied in the action
    (dS/dA_Omega = 0 makes it the q'-weighted mean field over the region Omega = a connected component of theta <= 0).

CHECKS
  K  K1 CONTROL: FP19's committed H_K1 headline (sigma_8 x4, forest x4, flagship x4, SPARC x2, KiDS at z = 0.25/0.4/0.7 x2)
     reproduced with FP19's own definitions on FP13's machinery; K2 CONTROL: FP20's exact projector reproduces FP20's committed
     R3 numbers for FP13's H_S (z = 0.25, 0.4, both footings) and the isolated-P2 base; H_K1 with the exact projector reported;
     K3 CONTROL: FP6's loaded lg_R0 reproduces FP11 K5's committed plain-P2 R0 (1.9247 / 2.0180); this lane's flow engine at
     W = 1 (no softening) reproduces it and at W = 0 the Newtonian R0 of lg_R0 (<= 1%); the gated band-passed phantom equals FP6's
     phantom() at W = 1 (<= 1e-12); K4 (reported) convergence (shells x2, steps x2).
  G  G1 [H1, headline]; G2 [H2] KiDS; G3 [H3] LG R0; G4 [H3] MW-M31 timing (FP11's two-body force and shooter, the pair's own
     turnaround gating its MOND); G5 [H4] the pincer map; G6 [H5] MS1; G7 [H6] clusters and splashback; G8 [H7] flagship, SPARC;
     G9 [H8] the external field in the kernel: KiDS against a uniform field, the web's field at KiDS lenses (CLASS, the chain's
     sigma_8), and the free-fall-frame reading.
  F  [load-bearing] every score finite.   W  the ledger.
MUTATE=1: the gate is on at theta <= 3H (the expanding Hubble flow counts as turned around) in G1's headline: G1 must FAIL.

SCOPE.  Spherical, radial (J = 0) shells; massless tracers of the baryon flow (conventions A/B: no local self-gravity of the
IGM or the carrier; a self-gravitating infall or a pre-conversion carrier halo would enlarge the turned-around regions -- the
cluster rows carry the carrier as XR4's Newtonian mass); point-mass baryons; the P2 kernel in its local QUMOND form (AQUAL =
QUMOND in spherical symmetry for P2, FP7).  The MW-M31 timing uses FP11's committed two-body force (no separator) with the gate
on the pair's own turnaround (D2).  kappa = 1/2 is FITTED (Z = kappa = 5.7888) and does not enter; both a0 footings carried.

DISCLOSED.  Exploratory scratch runs (not in the repository) came first: the spherical flow model under conventions A, B, a
self-gravitating variant and XR4's carrier-decay history (R0 and theta = 0 radii for 1e10.5-1e11.2 and the LG), KiDS d chi^2
for the sharp, ramp and all-axes gates with FP20's projector, the ramp-width scan (c_w = 1-4) and the carrier variant (the
LG R0 reaches 0.98 Mpc only where KiDS fails by +506).  H1-H7 were written after them.  A first debug run of this file (MUTATE=1)
exposed an engine defect (shells frozen where they first overtook a neighbour turned the rest into a wall, and the zero-velocity
transition of convention A is sharper in Lagrangian radius than a log grid resolves): the engine was rewritten (a shell is
multistream only once it passes through the softened centre; a second pass concentrates shells at each row's transition) and
its K3 control was restated against FP1's committed R0 (FP11 K5's reference column), and the MW-M31 timing now uses FP11's own
branch finder (exec'd from its source) instead of a coarse re-typed one that missed the narrow first-approach branch.  Numbers
of the debug run are superseded; the hypotheses were not changed.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR36_bound_regions.py   (MUTATE=1 for the
control; ~10-15 min, one thread of numpy).  Writes XR36_bound_regions[_MUTATE].out and _results[_MUTATE].json next to itself.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import sys, io, json, math, time, builtins, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
_trap_ = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR36_bound_regions"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()


class _Tee:
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()


sys.stdout = _Tee(TXT)
OUT = {"lane": "XR36", "part": "2: bound regions", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T_START:.0f} s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"XR36 refuses to write {file!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: G1's gate is on at theta <= 3H (the expanding Hubble flow counts as turned around) -- G1 must FAIL ***")

# ================================================================================================ machinery (read-only)
P13 = os.path.join(CHAIN, "FP13_separator_from_state.py")
_src = open(P13).read()
_mod = _src[:_src.index("\ndef main():")]
_body = _src[_src.index("\ndef main():") + len("\ndef main():"):
             _src.index('    banner("K  CONTROLS: the reused machinery reproduces the record; the halofit, the state, FP11\'s hook")')]
_body = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in _body.split("\n"))
NS = {"__file__": P13, "__name__": "fp13_machinery", "open": _ro_open}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_mod, P13, "exec"), NS)
        exec(compile(_body, P13, "exec"), NS)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
M6 = NS["M6"]
A0, FOOTS, MODES = NS["A0"], NS["FOOTS"], NS["MODES"]
kids_class, kids_chi2, KB6, YIELD = NS["kids_class"], M6["kids_chi2"], NS["KB"], NS["YIELD"]
s8_aq, forest_aq, law_dev_dex, model_of = NS["s8_aq"], NS["forest_aq"], NS["law_dev_dex"], NS["model_of"]
OmL_a, two_q, H0c, Om_c, Or_c, Mpc_c = NS["OmL_a"], NS["two_q"], NS["H0"], NS["Om"], NS["Or"], NS["Mpc"]
Z_KIDS, Z_FLAG = NS["Z_KIDS"], NS["Z_FLAG"]
RR, RP, MPCm, PCm, MS6, G6 = M6["RR"], M6["RP"], M6["MPCm"], M6["PCm"], M6["MS6"], M6["G6"]
RG, Fmat, gfrac_smooth, nu_p2 = M6["RG"], M6["Fmat"], M6["gfrac_smooth"], M6["nu_p2"]
LM = M6["LM"]
# FP20's exact projector, exec'd from its committed source (shell_mats + ESDFix)
P20 = os.path.join(CHAIN, "FP20_esd_projection_fix.py"); _s20 = open(P20).read()
NS20 = {"np": np, "math": math}
exec(_s20[_s20.index("def shell_mats("):_s20.index("class M2Fix:")], NS20)
FIX1 = NS20["ESDFix"](RR, RP, PCm, MS6)
ESD_BUG = M6["esd_of_M"]
ESD_FIX = lambda M, Mb: (RP / MPCm, FIX1(M, Mb))
F19 = json.load(open(os.path.join(CHAIN, "FP19_hs_repair_results.json")))["numbers"]
F20 = json.load(open(os.path.join(CHAIN, "FP20_esd_projection_fix_results.json")))["numbers"]
F11 = json.load(open(os.path.join(CHAIN, "FP11_local_group_flyby_results.json")))["numbers"]
P(f"\n  machinery: FP13's module + main() body to its K banner (FP9/FP6 inside), FP20's shell_mats/ESDFix, FP11's module (via "
  f"FP13's loader); a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2   {el()}")

# ================================================================================================ the flow engine (this lane)
G_ = 6.6743e-11; MS_ = 1.98892e30; MPC_ = 3.0857e22; KPC_ = MPC_ / 1e3
LG_h = M6["LG_h"]; LG_H0, LG_OM, LG_OL = M6["LG_H0"], M6["LG_OM"], M6["LG_OL"]


def Hof(a): return LG_H0*math.sqrt(LG_OM/a**3+LG_OL)
def _run(rc, Mb, a0, gate, read, conv, cw, zs, nstep, a_start, s2, fd, vk, carrier, mut_tol):
    """one pass of the flow engine on per-row comoving Lagrangian radii rc [m] (rows = masses); radial shells of the baryon
    flow started on the Hubble flow at a_start; the gated local P2 phantom g = g_N [1 + W (nu_P2 - 1)]; convention A (point
    mass + Lambda) or B (+ the smooth background's deceleration); carrier: an extra Newtonian mass carrier x M_b.  A shell
    that passes through the (softened) centre is multistream ('crossed', virialised: theta = 0); single-stream shells carry
    theta = dv/dr + 2 v/r (D1, the radial derivative in Lagrangian order) or 3 v/r (D2)."""
    nb, N = rc.shape
    r = rc*a_start; v = Hof(a_start)*r
    crossed = np.zeros((nb, N), bool)
    lna = np.linspace(math.log(a_start), 0.0, nstep+1); hs = lna[1]-lna[0]
    lnz = [math.log(1/(1+z_)) for z_ in zs]; outs = {}
    def theta_of(r, v):
        rad = np.abs(r); vr = np.sign(r)*v
        ok = ~crossed
        drf = rad[:, 1:]-rad[:, :-1]; dvf = vr[:, 1:]-vr[:, :-1]
        okf = ok[:, 1:] & ok[:, :-1] & (drf > 0)
        gf = np.where(okf, dvf/np.where(okf, drf, 1.0), np.nan)
        left = np.full_like(r, np.nan); right = np.full_like(r, np.nan)
        left[:, 1:] = gf; right[:, :-1] = gf
        er = np.where(np.isnan(left), right, np.where(np.isnan(right), left, 0.5*(left+right)))
        er = np.where(np.isnan(er), 0.0, er)
        et = vr/np.maximum(rad, 1e-30)
        th = (er+2*et) if read == "D1" else 3*et
        if fd > 0: th = (1-fd)*th + fd*2*vk*1e3/np.maximum(rad, 1e-30)
        th = np.where(crossed, 0.0, th); er = np.where(crossed, 0.0, er); et = np.where(crossed, 0.0, et)
        return th, er, et
    def W_of(th, er, et, a):
        K = 3*Hof(a)
        if gate == "sharp": return (th <= 0).astype(float)
        if gate == "ramp": return np.clip(1-th/(cw*K), 0.0, 1.0)
        if gate == "all3": return (np.maximum(er, et) <= 0).astype(float)
        if gate == "mut": return (th <= K*(1+mut_tol)).astype(float)
        if gate == "on": return np.ones_like(th)
        return np.zeros_like(th)
    def acc(l, r, v):
        a = math.exp(l); th, er, et = theta_of(r, v); W = W_of(th, er, et, a)
        rad = np.maximum(np.abs(r), 1e-6*MPC_); y = G_*Mb/(rad**2*a0)
        Me = Mb*(1+W*(np.sqrt(1+1/np.maximum(y, 1e-300))-1)) + carrier*Mb
        ac = -G_*Me*r/(r**2+s2)**1.5 + LG_OL*LG_H0**2*r
        if conv == "B": ac = ac - 0.5*LG_OM*LG_H0**2/a**3*r
        return ac
    for i in range(nstep):
        l = lna[i]
        H1, H2, H3 = Hof(math.exp(l)), Hof(math.exp(l+hs/2)), Hof(math.exp(l+hs))
        k1r, k1v = v/H1, acc(l, r, v)/H1
        r2, v2 = r+hs*k1r/2, v+hs*k1v/2; k2r, k2v = v2/H2, acc(l+hs/2, r2, v2)/H2
        r3, v3 = r+hs*k2r/2, v+hs*k2v/2; k3r, k3v = v3/H2, acc(l+hs/2, r3, v3)/H2
        r4, v4 = r+hs*k3r, v+hs*k3v; k4r, k4v = v4/H3, acc(l+hs, r4, v4)/H3
        rn = r+hs*(k1r+2*k2r+2*k3r+k4r)/6; v = v+hs*(k1v+2*k2v+2*k3v+k4v)/6
        crossed |= (np.sign(rn) != np.sign(r)) | (rn <= 0)                         # passed through the centre: multistream
        r = rn
        for zo, lo in zip(zs, lnz):
            if abs(lna[i+1]-lo) < hs/2 and zo not in outs:
                a = math.exp(lna[i+1]); th, er, et = theta_of(r, v); W = W_of(th, er, et, a)
                outs[zo] = dict(r=np.abs(r)/MPC_, vr=np.sign(r)*v, thK=th/(3*Hof(a)), W=W, crossed=crossed.copy())
    return outs
def summarize(o):
    """R0: the outermost v sign change (inward -> outward) along the single-stream shells in Lagrangian order; r_x: the
    multistream (crossed) region's extent, counted inside R0 only (a radial orbit's later excursions through the softened
    centre are not a physical virialised region); r_on: the outermost radius with W >= 0.5 (the crossed region counts as on)."""
    nb = o["r"].shape[0]; R0s, rons, rxs, edges = [], [], [], []
    for j in range(nb):
        ok = ~o["crossed"][j]; rr = o["r"][j][ok]; vv = o["vr"][j][ok]; W = o["W"][j][ok]
        idx = np.where((vv[:-1] < 0) & (vv[1:] >= 0))[0]
        R0 = float(np.interp(0.0, [vv[idx[-1]], vv[idx[-1]+1]], [rr[idx[-1]], rr[idx[-1]+1]])) if len(idx) else float("nan")
        R0s.append(R0)
        rc_ = o["r"][j][~ok]
        lim = R0 if R0 == R0 else (float(rr[np.where(vv < 0)[0].max()]) if (vv < 0).any() else float(rr.min()) if len(rr) else 0.0)
        rc_ = rc_[rc_ <= lim]
        rx = float(np.max(rc_)) if len(rc_) else 0.0; rxs.append(rx)
        on = np.where(W >= 0.5)[0]
        rons.append(max(rx, float(np.max(rr[on])) if len(on) else 0.0))
        exp_ = np.where(vv >= 0)[0]
        edges.append(float(rr[exp_.min()]) if len(exp_) else float("nan"))
    return np.array(R0s), np.array(rons), np.array(rxs), np.array(edges)
def flow_batch(Mb_msun, a0, gate="sharp", read="D1", conv="A", cw=1.0, z_out=(0.25,), N1=300, N2=200, nstep=3000, rlo=0.003, rhi=15.0,
         a_start=0.02, soft_kpc=10.0, fd=0.0, vk=600.0, carrier=0.0, mut_tol=0.01, refine=True):
    """two passes: a log grid of N1 shells (0.003-15 Mpc comoving), then N2 extra shells concentrated (per row) around the
    zero-velocity transition found in the first pass (the chain's convention-A flow turns around sharply in Lagrangian radius).
    Returns per output z: r [Mpc], v_r, theta/<K>, W, crossed, R0 (the outermost single-stream v sign change), r_on (W >= 0.5,
    the crossed region counting as on), r_x (the crossed region inside R0), R0_edge (the inner edge of the expanding flow)."""
    Mb = np.atleast_1d(np.asarray(Mb_msun, float))[:, None]*MS_; nb = Mb.shape[0]
    zs = sorted(z_out, reverse=True)
    rc1 = np.geomspace(rlo, rhi, N1)
    args = (Mb, a0, gate, read, conv, cw, zs, nstep, a_start, (soft_kpc*KPC_)**2, fd, vk, carrier, mut_tol)
    rc = np.tile(rc1, (nb, 1))*MPC_
    o1 = _run(rc, *args)
    if not refine:
        out = o1
    else:
        rows = []
        for j in range(nb):
            lo_i, hi_i = N1-1, 0
            for z_ in zs:
                o = o1[z_]; vv = o["vr"][j]; cr = o["crossed"][j]
                inside = np.where((~cr) & (vv < 0))[0]
                if len(inside):
                    jj = inside.max()
                else:
                    ncr = np.where(~cr)[0]; jj = ncr.min() if len(ncr) else 0
                lo_i = min(lo_i, max(jj-3, 0)); hi_i = max(hi_i, min(jj+3, N1-1))
            dense = np.geomspace(rc1[lo_i], rc1[hi_i], N2)
            rows.append(np.sort(np.concatenate([rc1, dense])))
        rc = np.array(rows)*MPC_
        out = _run(rc, *args)
    res = {}
    for z_ in zs:
        R0, ron, rx, edge = summarize(out[z_]); o = out[z_]; o.update(R0=R0, r_on=ron, r_x=rx, R0_edge=edge); res[z_] = o
    return res
def W_on(o, j, rgrid_m):
    ok = ~o["crossed"][j]; rr = o["r"][j][ok]*MPC_; WW = o["W"][j][ok]; rx = o["r_x"][j]*MPC_
    if len(rr) == 0: return np.ones_like(rgrid_m)
    order = np.argsort(rr); rr, WW = rr[order], WW[order]
    out = np.interp(rgrid_m, rr, WW, left=1.0, right=WW[-1])
    return np.where(rgrid_m <= rx, 1.0, out)


def phantom_W(Mb_kg, a0, L_m, W_RG):
    """FP6's phantom() (band-passed P2, xi -> 0, no yield) re-typed with the raw phantom gated by W on FP6's RG grid."""
    gN = G6 * Mb_kg / RG ** 2
    gbp = gN if L_m is None else gN * (1.0 - gfrac_smooth(RG / L_m))
    y = gbp / a0
    Mraw = W_RG * (nu_p2(y) - 1.0) * gbp * RG ** 2 / G6
    if L_m is None:
        return Mraw
    dM = np.diff(Mraw)
    return Mraw - (Fmat(L_m) @ dM + Mraw[0] * gfrac_smooth(RG / L_m))


def kids_gated(a0, gate, read, conv, z=0.25, cw=1.0, band_L=None, carrier_lens=0.0, **kw):
    """KiDS chi^2 (M6's kids_chi2 with the esd projector currently installed) of the gated profile, the 21 masses in one batch."""
    Mbs = 10 ** LM
    o = flow_batch(Mbs, a0, gate=gate, read=read, conv=conv, cw=cw, z_out=(z,), **kw)[z]
    cache = {}
    for j, lm in enumerate(LM):
        Mb = Mbs[j] * MS6
        if band_L is None:
            W = W_on(o, j, RR); y = G6 * Mb / (RR ** 2 * a0)
            M = Mb * (1 + W * (nu_p2(y) - 1))
        else:
            Mph = phantom_W(Mb, a0, band_L * MPCm, W_on(o, j, RG))
            M = Mb + np.interp(RR, RG, Mph)
        cache[round(float(lm), 6)] = M + carrier_lens * Mb
    chi = kids_chi2(lambda Mb_kg: cache[round(math.log10(Mb_kg / MS6), 6)])
    return chi, o


P(f"  the flow engine: two passes of 300 log-spaced radial shells (0.003-15 Mpc comoving) + 200 concentrated at each row's zero-velocity "
  f"transition, RK4 in ln a from a = 0.02, 3000 steps, 10 kpc softening   {el()}")

# ================================================================================================ K controls
banner("K  CONTROLS: FP19's H_K1 headline; FP20's exact projector; FP11/FP6's R0 machinery and this lane's engine")
tK = time.time()
ZQ = 0.0
L_K = lambda a: 2.9 * OmL_a(a)
fourpiGrho = lambda a: 1.5 * H0c ** 2 * (Om_c / a ** 3 + Or_c / a ** 4)
y_tied = {f: (lambda a, f=f: 2.0 * max(0.0, two_q(a)) * fourpiGrho(a) * L_K(a) * Mpc_c / A0[f]) for f in FOOTS}
k1 = {"s8": {}, "forest": {}, "flag": {}, "sparc": {}, "kids": {}, "kids@0.4": {}, "kids@0.7": {}}
for f in FOOTS:
    mod = model_of(L_K, y_tied[f])
    for m in MODES:
        k1["s8"][str((f, m))] = s8_aq(mod, f, m, rtol=1e-6)
        k1["forest"][str((f, m))] = forest_aq(mod, f, m)
    for Mv in (1e10, 1e11):
        k1["flag"][str((f, Mv))] = law_dev_dex(Mv, A0[f], 0.1, L_K(1 / (1 + Z_FLAG)), y_tied[f](1 / (1 + Z_FLAG)), YIELD)
    k1["sparc"][f] = max(abs(law_dev_dex(Mv, A0[f], yv, L_K(1.0), y_tied[f](1.0), YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12)
                         for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
    for key_, zz in (("kids", 0.25), ("kids@0.4", 0.4), ("kids@0.7", 0.7)):
        k1[key_][f] = kids_class(A0[f], L_K(1 / (1 + zz)), y_tied[f](1 / (1 + zz)), YIELD) - KB6[f]
ref = F19["H1"]
dev1 = 0.0
for key_ in ("s8", "forest", "flag"):
    for kk_, vv_ in k1[key_].items():
        dev1 = max(dev1, abs(vv_ - ref[key_][kk_]))
for key_ in ("sparc", "kids", "kids@0.4", "kids@0.7"):
    for kk_, vv_ in k1[key_].items():
        dev1 = max(dev1, abs(vv_ - ref[key_][kk_]))
P(f"    FP19 H_K1 (FP6 projection, as committed): sigma_8 {min(k1['s8'].values()):.6f}-{max(k1['s8'].values()):.6f}; forest "
  f"{max(k1['forest'].values()):.2g}; flagship {min(k1['flag'].values()):+.5f}..{max(k1['flag'].values()):+.5f}; SPARC "
  f"{max(k1['sparc'].values()):.2e}; KiDS z = 0.25 " + "/".join(f"{k1['kids'][f]:+.3f}" for f in FOOTS) + ", 0.4 "
  + "/".join(f"{k1['kids@0.4'][f]:+.3f}" for f in FOOTS) + ", 0.7 " + "/".join(f"{k1['kids@0.7'][f]:+.1f}" for f in FOOTS) + f"   ({time.time() - tK:.0f} s)")
check("K1 CONTROL: FP19's committed H_K1 headline (L = 2.9 Omega_L(<K>_h) Mpc, the tied yield c_y = 2) is reproduced with FP19's "
      "own definitions on FP13's machinery: sigma_8 (x4), the forest proxy (x4), the flagship (x4), SPARC (x2) and KiDS at z = 0.25, "
      "0.4, 0.7 (x2, FP6's projection as committed)", f"max |deviation| {dev1:.1e} over 20 numbers", dev1 <= 1e-9)
OUT["numbers"]["K1"] = k1
# K2 FP20's exact projector
M6["esd_of_M"] = ESD_FIX
KB = {f: kids_class(A0[f]) for f in FOOTS}
L_table, fun_of, yth_state = NS["L_table"], NS["fun_of"], NS["yth_state"]
LH_tab = L_table(NS["HEAD_S"], NS["HEAD_READ"]); Lh = fun_of(LH_tab)
yh = yth_state(LH_tab, NS["HEAD_READ"], NS["HEAD_SWITCH"], NS["HEAD_CY"])[0]
k2 = {}
for f in FOOTS:
    for zz in (0.25, 0.4):
        a_ = 1 / (1 + zz); k2[f"{f}/{zz}"] = kids_class(A0[f], Lh(a_), yh[f](a_), YIELD) - KB[f]
ref20 = F20["R3_FP13"]["headline"]
kb_rows = {}
dev2 = max(abs(k2[f"{f}/{zz}"] - ref20[f"{f}/{zz}"][1]) for f in FOOTS for zz in (0.25, 0.4))
hk1_exact = {f: {zz: kids_class(A0[f], L_K(1 / (1 + zz)), y_tied[f](1 / (1 + zz)), YIELD) - KB[f] for zz in (0.25, 0.4, 0.7)} for f in FOOTS}
P(f"    FP20's exact projector: FP13 H_S d chi^2 " + ", ".join(f"{k_}: {v:+.4f}" for k_, v in k2.items()) + f"; the isolated-P2 base KB = "
  + "/".join(f"{KB[f]:.4f}" for f in FOOTS) + " (FP20: +141.6/+134.9)")
P(f"    (reported) H_K1 with the exact projector (not in the record: FP19 predates FP20): " + "; ".join(
    f"{f}: z = 0.25 {v[0.25]:+.2f}, 0.4 {v[0.4]:+.2f}, 0.7 {v[0.7]:+.1f}" for f, v in hk1_exact.items()))
check("K2 CONTROL: FP20's exact projector (its committed shell_mats/ESDFix) reproduces FP20's committed R3 re-score of FP13's H_S "
      "(KiDS at z = 0.25 and 0.4, both footings) and the isolated-P2 base 141.6/134.9 -- the projector every KiDS number below uses",
      f"max |d chi^2 dev| {dev2:.1e}; KB {KB['canonical']:.3f}/{KB['alt']:.3f}", dev2 <= 1e-6 and abs(KB["canonical"] - 141.6466) < 1e-3 and abs(KB["alt"] - 134.9155) < 1e-3)
OUT["numbers"]["K2"] = dict(HS=k2, KB=KB, HK1_exact={f: {str(z_): v_ for z_, v_ in d_.items()} for f, d_ in hk1_exact.items()})
# K3 FP6's lg_R0 and this lane's engine
lg_R0 = M6["lg_R0"]; LG_MB = M6["LG_MB"]; LG_G = M6["LG_G"]; LG_Msun = M6["LG_Msun"]
F1J = json.load(open(os.path.join(CHAIN, "FP1_static_sector_results.json")))["numbers"]
ref_R0e0 = F11["K5"]
r0_p2 = {}
for f in FOOTS:
    Mb_ = LG_MB * LG_Msun
    r0_p2[f] = lg_R0(lambda r, a, f=f: Mb_ * nu_p2(LG_G * Mb_ / (r ** 2 * A0[f])))
r0_n = lg_R0(lambda r, a: LG_MB * LG_Msun * np.ones_like(r))
eng_on = {f: float(flow_batch([LG_MB], A0[f], gate="on", conv="A", z_out=(0.0,))[0.0]["R0"][0]) for f in FOOTS}
eng_off = float(flow_batch([LG_MB], A0["canonical"], gate="off", conv="A", z_out=(0.0,))[0.0]["R0"][0])
Wtest = np.ones_like(RG)
ph_dev = max(float(np.max(np.abs(phantom_W(1e11 * MS6, A0[f], 1.532 * MPCm, Wtest) - M6["phantom"](1e11 * MS6, A0[f], 1.532 * MPCm, None, 4))))
             / float(np.max(np.abs(M6["phantom"](1e11 * MS6, A0[f], 1.532 * MPCm, None, 4)))) for f in FOOTS)
refs_ = {f: ref_R0e0[f"P2/{f}"][1] for f in FOOTS}                                   # FP1's committed R0_e0 (FP11 K5's reference column)
P(f"    FP6's lg_R0 (loaded): plain P2 R0 = {r0_p2['canonical']:.6f} / {r0_p2['alt']:.6f} (FP1's committed R0_e0 via FP11 K5: "
  f"{refs_['canonical']:.6f} / {refs_['alt']:.6f}, FP1's own tabulated implementation); Newtonian (baryons only) R0 = {r0_n:.4f} Mpc")
P(f"    this lane's engine (convention A, 10 kpc softening): W = 1 R0 = {eng_on['canonical']:.4f} / {eng_on['alt']:.4f}; W = 0 R0 = {eng_off:.4f}; "
  f"gated band-passed phantom at W = 1 vs FP6's phantom(): max rel dev {ph_dev:.1e}")
k3_ok = (all(abs(r0_p2[f] / refs_[f] - 1) < 1e-5 for f in FOOTS) and all(abs(eng_on[f] / r0_p2[f] - 1) < 0.01 for f in FOOTS)
         and abs(eng_off / r0_n - 1) < 0.01 and ph_dev < 1e-12)
check("K3 CONTROL: FP6's lg_R0 (loaded read-only) reproduces FP1's committed plain-P2 R0 (R0_e0, FP11 K5's reference) to 1e-5 (two "
      "implementations of the same shell model); this lane's two-pass flow engine at W = 1 (10 kpc softening) reproduces it and at W = 0 the "
      "Newtonian (baryons-only) R0 of the same machinery to <= 1%; the gated band-passed phantom equals FP6's phantom() at W = 1 to <= 1e-12",
      f"lg_R0/FP1 - 1: {r0_p2['canonical'] / refs_['canonical'] - 1:+.1e}/{r0_p2['alt'] / refs_['alt'] - 1:+.1e}; engine/lg_R0 - 1: W=1 "
      f"{eng_on['canonical'] / r0_p2['canonical'] - 1:+.2e}/{eng_on['alt'] / r0_p2['alt'] - 1:+.2e}, W=0 {eng_off / r0_n - 1:+.2e}; phantom {ph_dev:.1e}", k3_ok)
OUT["numbers"]["K3"] = dict(lgR0_P2=r0_p2, FP1_R0e0=refs_, lgR0_newton=r0_n, engine_on=eng_on, engine_off=eng_off, phantom_dev=ph_dev)
P(f"    {el()}")

# ================================================================================================ G1 the turned-around region
banner("G1  THE TURNED-AROUND REGION AROUND ISOLATED KiDS LENSES (z = 0.25)" + ("  [MUTATE: on at theta <= 3H]" if MUTATE else ""))
MB_K = [10 ** 10.5, 1e11, 10 ** 11.2]
G1 = {}
g1_gate = "mut" if MUTATE else "sharp"
for f in FOOTS:
    for conv in ("A", "B"):
        for rd in ("D1", "D2"):
            o = flow_batch(MB_K, A0[f], gate=g1_gate, read=rd, conv=conv, z_out=(0.25,))[0.25]
            G1[f"{f}/{conv}/{rd}"] = dict(R0=o["R0"].tolist(), r_on=o["r_on"].tolist(), r_x=o["r_x"].tolist())
            P(f"    {f:9s} conv {conv} {rd} ({g1_gate}): M_b = 10^10.5 / 10^11 / 10^11.2: R0 = " + "/".join(f"{x:.3f}" for x in o["R0"])
              + " Mpc; gate on to r_on = " + "/".join(f"{x:.3f}" for x in o["r_on"]) + " Mpc; multistream core " + "/".join(f"{x:.3f}" for x in o["r_x"]))
g1_ok = all(max(v["r_on"]) <= 0.6 and np.nanmax(v["R0"]) <= 0.6 for v in G1.values())
check("G1 [H1, HEADLINE; MUTATE must fail] THE TURNED-AROUND REGION IS SMALL: around isolated KiDS lenses at z = 0.25 (10^10.5-10^11.2 "
      "Msun, both footings, conventions A and B, local D1 and regional D2 readings) the gate is on only inside r_on <= 0.6 Mpc and the "
      "zero-velocity radius is R0 <= 0.6 Mpc -- MOND is NOT on to 1 Mpc: the pull that would turn the outskirts around is the MOND pull "
      "the gate withholds until they have turned around",
      f"max r_on {max(max(v['r_on']) for v in G1.values()):.3f} Mpc; max R0 {max(np.nanmax(v['R0']) for v in G1.values()):.3f} Mpc", g1_ok,
      reading=("MUTATE: counting the expanding Hubble flow as turned around switches MOND on everywhere: the gate never closes"
               if MUTATE else "the gate cannot bootstrap its own turnaround: with baryons alone the Newtonian turnaround radius is small"))
OUT["numbers"]["G1"] = G1
P(f"    {el()}")

# ================================================================================================ G2 KiDS
banner("G2  KiDS (reported gate): FP20's exact projector, the FP13/FP19 KiDS setup, d chi^2 against the isolated-P2 base")
VARS = [("A", "sharp", "D1", None), ("A", "sharp", "D2", None), ("A", "ramp", "D2", None), ("B", "sharp", "D1", None), ("B", "sharp", "D2", None),
        ("B", "ramp", "D1", None), ("B", "ramp", "D2", None), ("B", "all3", "D1", None), ("B", "sharp", "D1", "HK1")]
G2 = {}
for f in FOOTS:
    for conv, gt, rd, bp in VARS:
        if True:
            L25 = L_K(1 / 1.25) if bp else None
            chi, o = kids_gated(A0[f], gt, rd, conv, z=0.25, band_L=L25)
            G2[f"{f}/{conv}/{gt}/{rd}/{bp or '-'}"] = chi - KB[f]
    P(f"    {f}: " + "; ".join(f"{k_.split('/', 1)[1]}: {v:+.1f}" for k_, v in G2.items() if k_.startswith(f)))
G2z = {}
for f in FOOTS:
    for zz in (0.4, 0.7):
        chi, _ = kids_gated(A0[f], "sharp", "D1", "B", z=zz)
        G2z[f"{f}/{zz}"] = chi - KB[f]
P("    (reported) the sharp D1 gate (convention B) at z = 0.4 / 0.7: " + ", ".join(f"{k_}: {v:+.1f}" for k_, v in G2z.items())
  + f"  (H_K1, exact projector: z = 0.7 {hk1_exact['canonical'][0.7]:+.0f}/{hk1_exact['alt'][0.7]:+.0f})")
P(f"    {el()}")
g2_all_fail = all(v > 9.0 for v in G2.values())
check("G2 [H2] (reported gate) KiDS within +9 of the isolated-P2 base for the turnaround-keyed gates (sharp D1/D2, ramp D1/D2 at the "
      "natural width, the 3-D-bound all-axes gate, the sharp gate on H_K1's band-passed phantom), both footings, conventions A and B",
      f"d chi^2 {min(G2.values()):+.1f} .. {max(G2.values()):+.1f} (all {len(G2)} > +9: {g2_all_fail}); H_K1 itself (exact projector, K2) "
      f"{hk1_exact['canonical'][0.25]:+.1f}/{hk1_exact['alt'][0.25]:+.1f}", max(G2.values()) <= 9.0,
      reading="KiDS FAILS for every turnaround-keyed variant: the phantom is truncated where the gate closes (0.1-0.6 Mpc)",
      load_bearing=False)
OUT["numbers"]["G2"] = dict(z025=G2, other_z=G2z)

# ================================================================================================ G3 LG R0
banner("G3  THE LOCAL GROUP'S R0 (reported gate): 0.93 +- 0.12 Mpc (FP18's bootstrap error), M_b = 1.145e11 (the chain's LG value)")
R0_T, R0_E = 0.93, 0.12
G3 = {}
for f in FOOTS:
    for conv in ("A", "B"):
        for gt, rd in (("off", "D1"), ("sharp", "D1"), ("sharp", "D2"), ("ramp", "D1"), ("ramp", "D2"), ("all3", "D1")):
            o = flow_batch([LG_MB, 1.65e11], A0[f], gate=gt, read=rd, conv=conv, z_out=(0.0,))[0.0]
            G3[f"{f}/{conv}/{gt}/{rd}"] = dict(R0=o["R0"].tolist(), edge=o["R0_edge"].tolist())
    P(f"    {f}: " + "; ".join(f"{k_.split('/', 1)[1]}: {v['R0'][0]:.3f}" + (f" [flow edge {v['edge'][0]:.3f}]" if v['R0'][0] != v['R0'][0] else "")
                              for k_, v in G3.items() if k_.startswith(f)))
sharp_rows = [v["R0"][0] for k_, v in G3.items() if "/sharp/" in k_]
check("G3 [H3] (reported gate) THE LG's R0 within 2 sigma of 0.93 +- 0.12 Mpc for the sharp gate (both readings, conventions A/B, both "
      "footings); the ramps, the all-axes gate and the Newtonian (baryons-only) R0 printed alongside (nan: the gate's feedback empties the "
      "zero-velocity zone -- the flow either falls in or keeps expanding -- and the inner edge of the expanding flow is printed)",
      f"sharp R0 {min(sharp_rows):.3f}-{max(sharp_rows):.3f} Mpc ({(max(sharp_rows) - R0_T) / R0_E:+.1f} sigma at best); Newtonian "
      f"{G3['canonical/A/off/D1']['R0'][0]:.3f} (A) / {G3['canonical/B/off/D1']['R0'][0]:.3f} (B); ramp D2 (B) {G3['canonical/B/ramp/D2']['R0'][0]:.3f}",
      all(abs(x - R0_T) <= 2 * R0_E for x in sharp_rows),
      reading="the sharp gate's R0 is the Newtonian baryons-only value: the R0 shell never turned around, so it never felt MOND",
      load_bearing=False)
OUT["numbers"]["G3"] = G3
P(f"    {el()}")

# ================================================================================================ G4 MW-M31 timing
banner("G4  THE MW-M31 TIMING (reported gate): FP11's two-body force (no separator) and FP11's branch finder, the pair's own turnaround "
       "gating its MOND")
ns11 = NS["fp11"]()
force_table, Acc11, MSUN11, KPC11, MPC11 = ns11["force_table"], ns11["Acc"], ns11["MSUN"], ns11["KPC"], ns11["MPC"]
FMW, D0_LG, VR_LG = ns11["FMW"], ns11["D0_LG"], ns11["VR_LG"]
L_OL_H02, LG_H0_11, LG_OM_11, LG_OL_11 = ns11["L_OL_H02"], ns11["LG_H0"], ns11["LG_OM"], ns11["LG_OL"]
GATE = {"g": "none"}


def shoot(acc, ri, nstep=8000, a_start=0.02, bg=False, store=False):
    """FP11's radial shooter, re-typed with the pair's MOND multiplied by the gate W on the pair's own turnaround (D2: the
    separation's radial velocity sign(x) u; ramp: clip(1 - sign(x) u/(|x| H))); GATE['g'] = none/sharp/ramp/off."""
    x = ri.copy(); u = LG_H0_11 * math.sqrt(LG_OM_11 / a_start ** 3 + LG_OL_11) * x
    lna = np.linspace(math.log(a_start), 0.0, nstep + 1); h = lna[1] - lna[0]
    nc = np.zeros_like(x, dtype=int); gt = GATE["g"]

    def f(l, xx, uu):
        a = math.exp(l); H = LG_H0_11 * math.sqrt(LG_OM_11 / a ** 3 + LG_OL_11)
        d = np.abs(xx); ur = np.sign(xx) * uu
        if gt == "none":
            W = 1.0
        elif gt == "sharp":
            W = (ur <= 0).astype(float)
        elif gt == "ramp":
            W = np.clip(1 - ur / (np.maximum(d, 1e-30) * H), 0.0, 1.0)
        else:
            W = 0.0
        newt = G_ * acc.M * d / (d ** 2 + acc.soft ** 2) ** 1.5
        ac = -(newt + W * acc.mond(l, d)) * np.sign(xx) + L_OL_H02 * xx
        if bg:
            ac = ac - 0.5 * LG_OM_11 * LG_H0_11 ** 2 / a ** 3 * xx
        return uu / H, ac / H
    for i in range(nstep):
        l = lna[i]
        k1x, k1u = f(l, x, u); k2x, k2u = f(l + h / 2, x + h * k1x / 2, u + h * k1u / 2)
        k3x, k3u = f(l + h / 2, x + h * k2x / 2, u + h * k2u / 2); k4x, k4u = f(l + h, x + h * k3x, u + h * k3u)
        xn = x + h * (k1x + 2 * k2x + 2 * k3x + k4x) / 6; u = u + h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        nc += (np.sign(xn) != np.sign(x)).astype(int); x = xn
    return x, u, nc


# FP11's branch finder, exec'd from its committed source against this lane's gated shooter
_s11 = open(os.path.join(CHAIN, "FP11_local_group_flyby.py")).read()
NSB = {"np": np, "math": math, "shoot": shoot, "KPC": KPC11, "MPC": MPC11, "D0_LG": D0_LG}
exec(_s11[_s11.index("def branches("):_s11.index("def orbit2d(")], NSB)
branches = NSB["branches"]
MBS_T = [1.145e11, 1.65e11, 2.4e11, 1e12, 1.5e12, 2e12, 4e12]
G4 = {}
tT = time.time()
for f in FOOTS:
    for Mb in MBS_T:
        m1, m2 = FMW * Mb * MSUN11, (1 - FMW) * Mb * MSUN11
        dg, ln_, T = force_table(m1, m2, A0[f], False, False)
        acc = Acc11(dg, ln_, T, m1 + m2)
        for gt in (("none", "sharp", "ramp", "off") if f == "canonical" else ("sharp",)):
            GATE["g"] = gt
            br = [b for b in branches(acc, nstep=4000) if b["k"] == 0]
            G4[f"{f}/{gt}/{Mb:.3e}"] = [dict(vr=b["vr"], d=b["d"]) for b in br]
    P(f"    {f}: first-branch v_r at D0 = {D0_LG} Mpc (convention A) [km/s] by M_b: " + "; ".join(
        f"{gt}: " + ", ".join(f"{Mb:.2e}: " + ("/".join(f"{b['vr']:+.1f}" for b in G4[f'{f}/{gt}/{Mb:.3e}']) or "none") for Mb in MBS_T)
        for gt in (("none", "sharp", "ramp", "off") if f == "canonical" else ("sharp",))) + f"   ({time.time() - tT:.0f} s)")


def tmass(f, gt):
    pts = []
    for Mb in MBS_T:
        app = [b["vr"] for b in G4.get(f"{f}/{gt}/{Mb:.3e}", []) if b["vr"] < 0]
        rec = [b["vr"] for b in G4.get(f"{f}/{gt}/{Mb:.3e}", []) if b["vr"] >= 0]
        pts.append((Mb, min(app) if app else (min(rec) if rec else float("nan"))))
    pts = [(m, v) for m, v in pts if v == v]
    for (ma, va), (mb, vb) in zip(pts[:-1], pts[1:]):
        if (va - VR_LG) * (vb - VR_LG) <= 0 and va != vb:
            return float(math.exp(math.log(ma) + (VR_LG - va) / (vb - va) * (math.log(mb) - math.log(ma))))
    return None


TM = {f"{f}/{gt}": tmass(f, gt) for f in FOOTS for gt in (("none", "sharp", "ramp", "off") if f == "canonical" else ("sharp",))}
P("    timing masses (first-branch v_r = -109.3 km/s): " + ", ".join(f"{k_}: {('%.3e' % v) if v else 'not bracketed in 1.1e11-8e12'}" for k_, v in TM.items()))
g4_ok = all((TM.get(f"{f}/sharp") is not None and 1.145e11 <= TM[f"{f}/sharp"] <= 2.4e11) for f in FOOTS)
check("G4 [H3] (reported gate) THE MW-M31 TIMING with the sharp gate (the pair's MOND on only once the pair itself has turned around): "
      "the first approach reaches -109.3 km/s with M_b inside FP11's window [1.145e11, 2.4e11] on both footings",
      f"timing mass: sharp {TM.get('canonical/sharp')} / {TM.get('alt/sharp')}; ramp {TM.get('canonical/ramp')}; ungated two-body MOND "
      f"{TM.get('canonical/none')}; Newtonian {TM.get('canonical/off')}", g4_ok,
      reading="a pair that must turn around on Newtonian baryons before its MOND switches on is still receding at D0 for baryonic masses",
      load_bearing=False)
OUT["numbers"]["G4"] = dict(branches=G4, timing_mass=TM)
P(f"    {el()}")

# ================================================================================================ G5 the pincer map
banner("G5  THE PINCER MAP (reported): the ramp's width c_w -- KiDS against the LG's R0 (canonical)")
G5 = {}
for rd, conv in (("D1", "B"), ("D2", "B"), ("D2", "A")):
    if True:
        for cw in (1.0, 1.5, 2.0, 3.0, 4.0):
            chi, _ = kids_gated(A0["canonical"], "ramp", rd, conv, z=0.25, cw=cw)
            oLG = flow_batch([LG_MB], A0["canonical"], gate="ramp", read=rd, conv=conv, cw=cw, z_out=(0.0,))[0.0]
            G5[f"{rd}/{conv}/{cw}"] = dict(kids=chi - KB["canonical"], R0=float(oLG["R0"][0]), edge=float(oLG["R0_edge"][0]))
        P(f"    ramp {rd} conv {conv}: " + "; ".join(f"c_w {k_.split('/')[2]}: KiDS {v['kids']:+.1f}, LG R0 {v['R0']:.2f}"
                                                     + (f" (edge {v['edge']:.2f})" if v['R0'] != v['R0'] else "") for k_, v in G5.items()
                                                     if k_.startswith(f"{rd}/{conv}/")))
both = [k_ for k_, v in G5.items() if v["kids"] <= 9.0 and abs((v["R0"] if v["R0"] == v["R0"] else v["edge"]) - R0_T) <= 2 * R0_E]
kids_ok_R0 = [(v["R0"] if v["R0"] == v["R0"] else v["edge"]) for v in G5.values() if v["kids"] <= 9.0]
check("G5 [H4] (reported) THE PINCER MAP: some ramp width passes KiDS (<= +9) AND the LG's R0 (within 2 sigma of 0.93) at once",
      f"cells passing both: {both or 'none'}; LG R0 at the KiDS-passing widths {min(kids_ok_R0) if kids_ok_R0 else float('nan'):.2f}-"
      f"{max(kids_ok_R0) if kids_ok_R0 else float('nan'):.2f} Mpc", len(both) > 0,
      reading="the gate does not open FP18's KiDS-R0 pincer: whatever gives the KiDS lenses their Mpc phantom gives the LG R0 >~ 1.3 Mpc",
      load_bearing=False)
OUT["numbers"]["G5"] = G5
P(f"    {el()}")

# ================================================================================================ G6 MS1
banner("G6  (reported) MS1: the total-matter reading with an outstreaming daughter fraction f_d (1e11 at z = 0.25, convention B)")
G6r = {}
for fd in (0.0, 0.02, 0.05, 0.1, 0.2, 0.5):
    o = flow_batch([1e11], A0["canonical"], gate="sharp", read="D1", conv="B", z_out=(0.25,), fd=fd)[0.25]
    G6r[str(fd)] = dict(r_on=float(o["r_on"][0]), R0=float(o["R0"][0]), r_x=float(o["r_x"][0]))
P("    r_on [Mpc] by f_d: " + ", ".join(f"{k_}: {v['r_on']:.3f}" for k_, v in G6r.items()))
check("G6 [H5] (reported) MS1: reading the total matter flow (daughters outstreaming at 600 km/s, fraction f_d) pulls the switch-on "
      "radius inward toward the multistream core -- the baryon reading is the admissible one",
      ", ".join(f"f_d {k_}: r_on {v['r_on']:.3f}" for k_, v in G6r.items()),
      G6r["0.2"]["r_on"] <= G6r["0.0"]["r_on"], load_bearing=False)
OUT["numbers"]["G6"] = G6r

# ================================================================================================ G7 clusters and splashback
banner("G7  (reported) CLUSTERS AND SPLASHBACK: M_b = 1.5e14 with its carrier kept (5.36 M_b Newtonian, FP16/XR4) and without")
G7 = {}
MB_CL = 1.5e14
rhoc0_ = 3 * LG_H0 ** 2 / (8 * math.pi * G_)
for carr in (0.0, 5.36):
    M200 = MB_CL * (1 + carr) * MS_
    R200 = (3 * M200 / (4 * math.pi * 200 * rhoc0_)) ** (1 / 3) / MPC_
    for gt in ("sharp", "on", "off"):
        o = flow_batch([MB_CL], A0["canonical"], gate=gt, read="D1", conv="B", z_out=(0.0,), carrier=carr, rhi=40.0)[0.0]
        G7[f"{carr}/{gt}"] = dict(R200=R200, r_on=float(o["r_on"][0]), R0=float(o["R0"][0]), r_x=float(o["r_x"][0]))
        P(f"    carrier {carr:4.2f} M_b, gate {gt:5s}: R200 = {R200:.2f} Mpc; gate on to {o['r_on'][0]:.2f} ({o['r_on'][0] / R200:.2f} R200); R0 = "
          f"{o['R0'][0]:.2f} ({o['R0'][0] / R200:.2f} R200); multistream (splashback) region {o['r_x'][0]:.2f} Mpc ({o['r_x'][0] / R200:.2f} R200)")
R500_frac = 0.65
xcop_in = G7["5.36/sharp"]["r_on"] >= R500_frac * G7["5.36/sharp"]["R200"]
check("G7 [H6] (reported) CLUSTERS: with its carrier kept the cluster's gate covers X-COP's radii (R500 ~ 0.65 R200), so X-COP's MOND "
      "share is unchanged by the gate; the multistream (splashback) radius with and without the gate is printed",
      f"carrier kept: gate on to {G7['5.36/sharp']['r_on'] / G7['5.36/sharp']['R200']:.2f} R200, R0 = {G7['5.36/sharp']['R0'] / G7['5.36/sharp']['R200']:.2f} R200, "
      f"splashback {G7['5.36/sharp']['r_x'] / G7['5.36/sharp']['R200']:.2f} (gated) / {G7['5.36/on']['r_x'] / G7['5.36/on']['R200']:.2f} (MOND everywhere) / "
      f"{G7['5.36/off']['r_x'] / G7['5.36/off']['R200']:.2f} (Newton) R200; baryons only: gate on to {G7['0.0/sharp']['r_on'] / G7['0.0/sharp']['R200']:.2f} R200",
      xcop_in, load_bearing=False)
OUT["numbers"]["G7"] = G7
P(f"    {el()}")

# ================================================================================================ G8 flagship and SPARC
banner("G8  (reported gates) THE FLAGSHIP (z = 2.5, y = 0.1) AND SPARC (z = 0, y = 0.01-100): is the galaxy law inside the gate?")
G8 = {"flag": {}, "sparc": {}}
for f in FOOTS:
    o = flow_batch([1e10, 1e11], A0[f], gate="sharp", read="D1", conv="B", z_out=(2.5,))[2.5]
    for j, Mv in enumerate((1e10, 1e11)):
        rF = math.sqrt(G_ * Mv * MS_ / (0.1 * A0[f]))
        W = float(W_on(o, j, np.array([rF]))[0]); nuv = float(nu_p2(np.array([0.1]))[0])
        G8["flag"][f"{f}/{Mv:.0e}"] = dict(r_F_kpc=rF / KPC_, W=W, dev_dex=math.log10((1 + W * (nuv - 1)) / nuv), r_on_kpc=float(o["r_on"][j] * 1e3))
    o0 = flow_batch([1e9, 1e10, 1e11, 1e12], A0[f], gate="sharp", read="D1", conv="B", z_out=(0.0,))[0.0]
    worst = 0.0
    for j, Mv in enumerate((1e9, 1e10, 1e11, 1e12)):
        wm = 0.0
        for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0):
            r_ = math.sqrt(G_ * Mv * MS_ / (yv * A0[f])); W = float(W_on(o0, j, np.array([r_]))[0]); nuv = float(nu_p2(np.array([yv]))[0])
            wm = max(wm, abs(math.log10((1 + W * (nuv - 1)) / nuv)))
        worst = max(worst, wm)
        G8["sparc"][f"{f}/{Mv:.0e}"] = dict(r_on_kpc=float(o0["r_on"][j] * 1e3), r_y001_kpc=math.sqrt(G_ * Mv * MS_ / (0.01 * A0[f])) / KPC_, worst_dex=wm)
    G8["sparc"][f"{f}/worst"] = worst
for kk_, v in G8["flag"].items():
    P(f"    flagship {kk_}: r_F = {v['r_F_kpc']:.1f} kpc, gate on to {v['r_on_kpc']:.1f} kpc, W(r_F) = {v['W']:.2f}: deviation {v['dev_dex']:+.3f} dex")
for kk_, v in G8["sparc"].items():
    if isinstance(v, dict):
        P(f"    SPARC {kk_}: gate on to {v['r_on_kpc']:.0f} kpc; the y = 0.01 radius {v['r_y001_kpc']:.0f} kpc; worst |dev| {v['worst_dex']:.3f} dex")
flag_worst = max(abs(v["dev_dex"]) for v in G8["flag"].values())
sparc_worst = max(G8["sparc"][f"{f}/worst"] for f in FOOTS)
check("G8 [H7] (reported gates) the FLAGSHIP (|dev| <= 0.05 dex at y = 0.1, z = 2.5, 1e10-1e11) and SPARC (|dev| <= 0.01 dex at "
      "y = 0.01-100, 1e9-1e12, z = 0) with the sharp local gate (convention B): the law holds where the gate is on",
      f"flagship worst {flag_worst:.3f} dex; SPARC worst {sparc_worst:.3f} dex", flag_worst <= 0.05 and sparc_worst <= 0.01,
      reading="the galaxy law survives only where the galaxy's own turned-around (and multistream) region covers its test radii",
      load_bearing=False)
OUT["numbers"]["G8"] = G8

# ================================================================================================ G9 the external field in the kernel
banner("G9  WHICH FIELD DOES THE KERNEL SEE? KiDS with the environment's external field (QUMOND monopole, FP20's projector), the web's "
       "field at KiDS lenses (CLASS), and the free-fall-frame reading")
from classy import Class as _Class
_cl = _Class()
_cl.set({"h": 0.6736, "omega_b": 0.02237, "omega_cdm": 0.1200, "A_s": 2.1e-9, "n_s": 0.965, "output": "mPk", "P_k_max_1/Mpc": 60.0,
         "z_max_pk": 1.0})
_cl.compute()
_resc = (0.811 / _cl.sigma8()) ** 2                                               # the chain's sigma_8 (FP6's SIG8)
zK = 0.25; aK = 1 / (1 + zK)
kk9 = np.geomspace(1e-4, 50.0, 6000)                                              # 1/Mpc
Pk9 = np.array([_cl.pk_lin(k_, zK) for k_ in kk9]) * _resc                        # Mpc^3
Om9 = (0.02237 + 0.1200) / 0.6736 ** 2; rhoc9 = 3 * (67.36e3 / MPC_) ** 2 / (8 * math.pi * G_)
pref9 = 4 * math.pi * G_ * Om9 * rhoc9 / aK ** 2                                  # g_k = pref delta_k/k (physical field, comoving k)
kSI = kk9 / MPC_; PSI_ = Pk9 * MPC_ ** 3
LK025_com = L_K(aK) / aK                                                           # H_K1's band-pass length, comoving Mpc
R_l = 1.0                                                                          # comoving Mpc: the lens's own Lagrangian patch (1e12 halo)
W9 = {"full web field": np.ones_like(kk9),
      "H_K1 band-passed": 1 - np.exp(-0.5 * (kk9 * LK025_com) ** 2),
      "exterior of the lens's patch (R_l = 1 Mpc)": np.sinc(kk9 * R_l / math.pi)}
web_e = {}
for lab, w_ in W9.items():
    sg = pref9 * math.sqrt(float(_trap_(PSI_ * w_ ** 2, kSI)) / (2 * math.pi ** 2))
    for f in FOOTS:
        web_e[f"{lab}/{f}/all"] = 0.888 * sg / A0[f]                                  # Maxwell median |g| = 0.888 x rms
        web_e[f"{lab}/{f}/baryons"] = 0.888 * sg * 0.157 / A0[f]                      # reading (b): the baryons' field (f_b)
P("    the web's field at a KiDS lens (z = 0.25, median of the 3-D Maxwell distribution, unconditioned) in units of a0: " + "; ".join(
    f"{k_}: {v:.2e}" for k_, v in web_e.items() if "/canonical/" in k_))
GLQ, WLQ = np.polynomial.legendre.leggauss(96)


def M_efe(Mb_kg, a0, e_a0, W=None):
    """the QUMOND monopole of a point mass in a uniform external field e (units a0): the enclosed phantom is the angle-averaged
    radial flux of (nu(|g|/a0) - 1) g, g = -g_N r^ + e a0 e^ (the uniform part carries no net flux); gated by W(r)."""
    gN = G6 * Mb_kg / RR ** 2 / a0
    g2 = gN[:, None] ** 2 + e_a0 ** 2 - 2 * gN[:, None] * e_a0 * GLQ[None, :]
    rad = -gN[:, None] + e_a0 * GLQ[None, :]
    fl = 0.5 * np.sum((nu_p2(np.sqrt(g2)) - 1.0) * rad * WLQ[None, :], axis=1)
    Mph = -RR ** 2 * fl * a0 / G6
    if W is not None:
        Mph = W * Mph
    return Mb_kg + Mph


E_GRID = [0.0, 1e-4, 2e-4, 3e-4, 5e-4, 1e-3, 3e-3, 1e-2]
G9 = {"base": {}, "gated": {}}
for f in FOOTS:
    for e_ in E_GRID:
        G9["base"][f"{f}/{e_}"] = kids_chi2(lambda Mb_kg, e_=e_, f=f: M_efe(Mb_kg, A0[f], e_)) - KB[f]
    P(f"    {f}: isolated-P2 law with a uniform external field e in the kernel: KiDS d chi^2 by e/a0 " + ", ".join(
        f"{e_:g}: {G9['base'][f'{f}/{e_}']:+.1f}" for e_ in E_GRID))


def e_tol(f):
    xs = E_GRID; ys = [G9["base"][f"{f}/{e_}"] for e_ in xs]
    for (x1, y1), (x2, y2) in zip(zip(xs[:-1], ys[:-1]), zip(xs[1:], ys[1:])):
        if y1 <= 9.0 < y2:
            return x1 + (9.0 - y1) * (x2 - x1) / (y2 - y1)
    return None


ETOL = {f: e_tol(f) for f in FOOTS}
cost = {}
for f in FOOTS:
    for lab in W9:
        for rd in ("all", "baryons"):
            ev = web_e[f"{lab}/{f}/{rd}"]
            cost[f"{lab}/{f}/{rd}"] = kids_chi2(lambda Mb_kg, ev=ev, f=f: M_efe(Mb_kg, A0[f], ev)) - KB[f]
P(f"    KiDS's tolerance on a uniform external field (d chi^2 = +9): e_tol = {ETOL['canonical']} / {ETOL['alt']} a0")
P("    the cost of the web's median field WITHOUT the free-fall-frame reading (isolated P2 + EFE): " + "; ".join(
    f"{k_}: {v:+.1f}" for k_, v in cost.items() if "/canonical/" in k_))
# tidal residual under the free-fall-frame reading: the variation of the environment's field across the lens's region
rho_bar025 = Om9 * rhoc9 / aK ** 3
e_tidal = {r_on_: (4 * math.pi / 3) * G_ * rho_bar025 * 1.0 * r_on_ * MPC_ / A0["canonical"] for r_on_ in (0.1, 0.3, 0.6)}
P("    free-fall-frame reading: the uniform part cancels; the residual is tidal, ~ (4 pi/3) G rho_bar delta_env r_on / a0 (delta_env = 1): "
  + ", ".join(f"r_on = {k_} Mpc: {v:.1e}" for k_, v in e_tidal.items()) + " (its monopole enters at second order)")
check("G9a [H8] (reported gate) KiDS WITH THE WEB'S FIELD IN THE KERNEL (no free-fall-frame reading): within +9 of the isolated "
      "base with the web's median field at a KiDS lens -- the gate alone (no band-pass: the full field, all-matter) and the hybrid "
      "(H_K1's band-passed field, reading (b): baryons only)",
      f"KiDS tolerates e <= {ETOL['canonical']:.1e} / {ETOL['alt']:.1e} a0; the web's median field: full/all-matter "
      f"{web_e['full web field/canonical/all']:.1e}, band-passed/baryons {web_e['H_K1 band-passed/canonical/baryons']:.1e} a0; KiDS cost "
      f"{cost['full web field/canonical/all']:+.0f} / {cost['H_K1 band-passed/canonical/baryons']:+.0f} (canonical), "
      f"{cost['full web field/alt/all']:+.0f} / {cost['H_K1 band-passed/alt/baryons']:+.0f} (alt)",
      max(cost[f"full web field/{f}/all"] for f in FOOTS) <= 9.0 and max(cost[f"H_K1 band-passed/{f}/baryons"] for f in FOOTS) <= 9.0,
      reading="the gate alone puts the web's full field into the kernel: the MOND external-field downturn fails KiDS by hundreds; "
              "H_K1's band-pass (reading b) cuts it to tens -- still over (FP23's AQUAL solver with isolation is the refinement)",
      load_bearing=False)
check("G9b (reported) THE FREE-FALL-FRAME READING: with the kernel reading g - A_Omega (A_Omega the bound region's mean field) a uniform "
      "external field cancels exactly and KiDS's isolated base returns; the residual is tidal, ~(4 pi/3) G rho_bar delta_env r_on/a0, "
      "comparable to e_tol at r_on ~ 0.3 Mpc but entering the monopole only at second order.  The reading does not come out of the "
      "gate's action: it must be POSITED -- a per-region auxiliary vector A_Omega varied in the action (dS/dA_Omega = 0 makes it the "
      "q'-weighted mean field of the region Omega, a connected component of theta <= 0); no new constant, a new nonlocal structure",
      "tidal residual at r_on = 0.1/0.3/0.6 Mpc: " + "/".join(f"{v:.1e}" for v in e_tidal.values()) + f" a0 vs e_tol {ETOL['canonical']:.1e}",
      True, load_bearing=False)
OUT["numbers"]["G9"] = dict(web_e=web_e, kids_vs_e=G9["base"], e_tol=ETOL, cost=cost, e_tidal=e_tidal)
P(f"    {el()}")

# ================================================================================================ G10 how fast the lens outskirts expand
banner("G10 (reported) HOW FAST DO A KiDS LENS'S OUTSKIRTS EXPAND? theta/3H of the baryon flow at 0.3-1.5 Mpc (z = 0.25), the input for "
       "part 3's comparison with the web's matter")
G10 = {}
RQ = (0.3, 0.5, 0.7, 1.0, 1.5)
for f in FOOTS:
    for conv in ("A", "B"):
        o = flow_batch(MB_K, A0[f], gate="sharp", read="D1", conv=conv, z_out=(0.25,))[0.25]
        for j, Mv in enumerate(MB_K):
            ok = ~o["crossed"][j]; rr = o["r"][j][ok]; tk = o["thK"][j][ok]; srt = np.argsort(rr)
            G10[f"{f}/{conv}/{math.log10(Mv):.1f}"] = [float(np.interp(r_, rr[srt], tk[srt])) for r_ in RQ]
    P(f"    {f}: theta/3H at r = " + "/".join(f"{r_}" for r_ in RQ) + " Mpc: " + "; ".join(
        f"{k_.split('/', 1)[1]}: " + "/".join(f"{x:.2f}" for x in v) for k_, v in G10.items() if k_.startswith(f)))
check("G10 (reported) THE LENS OUTSKIRTS EXPAND: at 0.5-1 Mpc around an isolated KiDS lens (z = 0.25, the chain's baryons-only flow) the "
      "matter still expands at the printed fraction of the Hubble rate -- where KiDS needs MOND the flow has NOT turned around",
      "theta/3H at 0.5 / 1.0 Mpc: " + "; ".join(f"{k_}: {v[1]:.2f}/{v[3]:.2f}" for k_, v in G10.items() if "/canonical/" in "/" + k_),
      all(v[3] > 0.5 for v in G10.values()), load_bearing=False)
OUT["numbers"]["G10"] = dict(r_Mpc=RQ, thK=G10)
P(f"    {el()}")

# ================================================================================================ K4 convergence (reported)
banner("K4  (reported) CONVERGENCE: shells x2 and steps x2 on the headline rows")
cv = {}
for (n1, n2, ns_) in ((300, 200, 3000), (600, 400, 3000), (300, 200, 6000)):
    o = flow_batch([1e11, LG_MB], A0["canonical"], gate="sharp", read="D1", conv="B", z_out=(0.25, 0.0), N1=n1, N2=n2, nstep=ns_)
    cv[f"{n1}+{n2}/{ns_}"] = dict(r_on=float(o[0.25]["r_on"][0]), R0=float(o[0.25]["R0"][0]), R0_LG=float(o[0.0]["R0"][1]))
chi_c = {}
for (n1, n2, ns_) in ((300, 200, 3000), (600, 400, 6000)):
    chi, _ = kids_gated(A0["canonical"], "sharp", "D1", "B", z=0.25, N1=n1, N2=n2, nstep=ns_)
    chi_c[f"{n1}+{n2}/{ns_}"] = chi - KB["canonical"]
P("    " + "; ".join(f"N/steps {k_}: r_on {v['r_on']:.3f}, R0 {v['R0']:.3f}, LG R0 {v['R0_LG']:.3f}" for k_, v in cv.items())
  + "; KiDS (sharp D1, B) " + ", ".join(f"{k_}: {v:+.2f}" for k_, v in chi_c.items()))
base = cv["300+200/3000"]
dcv = max(max(abs(v["R0"] / base["R0"] - 1), abs(v["R0_LG"] / base["R0_LG"] - 1)) for v in cv.values())
dchi = abs(chi_c["600+400/6000"] - chi_c["300+200/3000"])
check("K4 (reported) CONVERGENCE: doubling the shells or the steps moves R0 (1e11, z = 0.25; the LG, z = 0) by the printed fraction and "
      "the sharp-D1 KiDS d chi^2 by the printed amount (a fraction of its excess over +9)",
      f"max |R0 change| {dcv:.1e}; KiDS {chi_c}", dcv < 0.03 and dchi < 0.1 * max(abs(chi_c["300+200/3000"]), 1.0), load_bearing=False)
OUT["numbers"]["K4"] = dict(cv=cv, kids=chi_c)

# ================================================================================================ F, W
allnums = [v for v in G2.values()] + [v["R0"][0] for k_, v in G3.items() if "/sharp/" in k_ or "/off/" in k_] + [v["kids"] for v in G5.values()]
fin_ok = all(np.isfinite(allnums))
check("F [load-bearing] every KiDS score, the sharp and Newtonian R0 and every pincer KiDS score is finite", f"{len(allnums)} numbers finite: {fin_ok}", fin_ok)
banner("W  THE LEDGER")
LEDGER = [
    ("XR36-g", "FAILS", "the turnaround gate around isolated KiDS lenses: the turned-around region at z = 0.25 is <= 0.6 Mpc (baryons "
     "only), so KiDS fails for every turnaround-keyed variant", "G1, G2"),
    ("XR36-h", "FAILS", "the LG under the sharp gate: R0 = the Newtonian baryons-only value; the MW-M31 pair must turn around on "
     "Newtonian baryons first", "G3, G4"),
    ("XR36-i", "CONSTRAINT", "the ramp width c_w maps FP18's KiDS-R0 pincer: KiDS passes only where the LG's R0 >~ 1.3 Mpc", "G5"),
    ("XR36-j", "CONSTRAINT", "MS1: the gate must read the baryon flow (a total-matter reading pulls the switch-on inward)", "G6"),
    ("XR36-k", "DERIVED", "clusters that keep their carrier are turned around well beyond R500: X-COP's MOND share is untouched by the "
     "gate", "G7"),
    ("XR36-p", "FAILS", "without a band-pass the kernel reads the web's full field at KiDS lenses (~1e-2 a0 against a tolerance ~1e-4): "
     "the external-field downturn fails KiDS by hundreds", "G9a"),
    ("XR36-q", "POSTULATED", "the free-fall-frame reading (the kernel reads g - A_Omega, A_Omega the bound region's mean field, a per-region "
     "auxiliary varied in the action): removes the uniform external field exactly; not derived from the gate", "G9b"),
]
for row in LEDGER:
    OUT["ledger"].append(dict(zip(("link", "status", "what", "basis"), row)))
    P(f"    {row[0]:8s} {row[1]:10s} {row[2]}  [{row[3]}]")
n_pass = sum(1 for c in CH if c[1]); n_lb_fail = sum(1 for c in CH if (not c[1]) and c[2])
P(f"\n{n_pass}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   {el()}")
OUT["verdict"] = dict(passed=n_pass, total=len(CH), load_bearing_failures=n_lb_fail)
M6["esd_of_M"] = ESD_BUG
with open(JSN, "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
sys.stdout.flush()
sys.exit(1 if n_lb_fail else 0)
