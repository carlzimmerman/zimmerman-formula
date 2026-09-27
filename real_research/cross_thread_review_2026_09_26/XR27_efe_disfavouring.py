#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR27_efe_disfavouring.py -- THE EFE SAMPLES THAT DISFAVOUR AN EXTERNAL-FIELD EFFECT, re-scored in the derivation chain's
band-passed static law: the cluster-infall BTFR (N = 314), the Local Volume dwarfs (N = 92, statistic C) and the eleven
Coma UDGs, as a function of the band-pass length L (0.5-5 Mpc), with H_Y's and H_S's own L marked, both a0 footings.
Independent cross-thread review (2026-09-27).  Read-only on every other file: XR6's definitions (and through them the
committed loaders of hunt_2026/k_contrarian_clusterbtfr.py, k_contrarian_dwarfefe.py and L23's Coma pipeline) and FP11's
definitions (and through them FP6's band-pass machinery) are exec'd in private namespaces; no main block is run.

WHY.  M* (the construction model) fails all three (XR9 at the converged cell: cluster slope 2.2-6.3 sigma, dwarfs 3.9-4.5,
UDGs 4.2-4.3).  FP10 says its dark sector (S = 0) cannot move them: "they stay the separator's".  Nobody has scored them in
the chain's own law.  The chain's separator band-passes the kernel's argument, so a uniform external field is removed
(FP11 F11j) while a host closer than ~L partly survives.  That could flip these samples either way.

THE LAW (FP11's statement of the chain's static law, QUMOND form; nothing added):
    g = g_N + P (1 - S_L) X(g_bp),   g_bp = (1 - S_L) g_N,   X(g) = a0 x_P2(|g|/a0 - y_th) g/|g|,   x_P2(D) = sqrt(D^2+D) - D,
  S_L the Gaussian heat filter (sigma = L), xi -> 0, the kernel P2 (FP1 L4d; nu_P2 = sqrt(1 + 1/y) at y_th = 0), g_N sourced by
  the BARYONS only (FP10's L353 pair: the dark field is kernel-invisible).  FP11 F11a: the two-body field is Newton + each body's
  isolated band-passed phantom + the interaction field P(1 - S_L) W, W = X(g1 + g2) - X(g1) - X(g2).
  DERIVED HERE (the reduction used for every sample).  A satellite s (size r_s) at distance D from a host h, with r_s << D and
  r_s << L: near s, (1 - S_L) g_s = g_s Efac(r/L) ~ g_s, and (1 - S_L) g_h = e_bp + O(r_s/D) tides, where
      e_bp(D) = G [M_h(<D) - (S_L M_h)(<D)]/D^2      (point host: G M_h Efac(D/L)/D^2, Efac(u) = 1 - gfrac(u), FP11's Efac)
  is the band-passed host field AT the satellite.  The satellite's own phantom plus FP11's interaction field is then
  X(g_s + e_bp) - X(e_bp) (the output filter's S_L part varies on the scale L: a tidal-order term).  So the internal dynamics
  is the ordinary QUMOND external-field effect with (i) the kernel P2 and (ii) the external Newtonian field e_N REPLACED by
  e_bp.  A uniform field has e_bp = 0 (h(k = 0) = 0); a host at D >> L is removed; a host at D << L survives.  For an
  EXTENDED host the smoothed part S_L M_h includes its outer mass: the outer profile matters (carried as a systematic).
THE STATISTICS (the record's, unchanged; only the prediction changes):
  clusters  XR4/XR6/XR9: the partial slope d Delta/d log g_e (Delta = log V - (1/4) log G M_b a0; regressors 1, log M_b, log M_HI,
            log g_e with g_e the committed TRUE NFW field) and the zero point (members - field), bootstrap errors of the
            observed; the scalar-sum form nu((g_N + e)/a0) and the 1-D QUMOND subtract form; variants f_b(R500) 0.10/0.13/0.157
            x r = R_proj / 1.3 R_proj x baryons extended / truncated at r200 x both footings.  Pass (XR9's gate): every variant
            <= 2 sigma.  Here e = e_bp of the host's BARYONS (XR6's e_in = G M_b,cl(<r)/r^2 times the band-pass fraction).
  dwarfs    k_contrarian_dwarfefe's statistic C (quadratic design, the committed regressor held fixed), host baryons x1/x1.5/x2
            (XR4's CGM variants), both footings; the larger host field, each host band-passed as a point mass.  Pass: every
            variant <= 2 sigma.
  UDGs      L23's pipeline as XR6 rebuilt it (the 'sphere' coupling nu(y)(1 + f_ext L/3), the systematic floor recomputed on the
            arm with L23's entries, the f_b(R500) template spread added as XR6 did); e = Coma's band-passed baryonic field.
            Pass (XR9's gate): the central arm (beta-model, Einasto 3-D, f_b 0.13) < 2 sigma on both footings, here for both
            baryon extents (extended as XR6, and truncated at each mass model's own r200: the band-pass reads the outer
            profile, a new systematic of this law).
  A third form, the FLUX form (reported, never pooled): the angle-averaged internal field at the kinematic radius from Gauss's
  law applied to FP11's own decomposition, gbar(s) = G m/s^2 + <-n.[X(g_s,bp + g_h,bp) - X(g_h,bp)]>_sphere with the host's
  ACTUAL non-uniform band-passed field over the sphere (FP11's Xfield and Efac, read-only).  Its quasi-Newtonian limit is
  L23's 'sphere' coupling nu(1 + L/3) (check F1); it drops the host's own tidal phantom density, as the record's forms do.
THE SCAN.  L = 0.5-5 Mpc applied at each system's epoch (all at z <= 0.065), y_th = 0; plus L = infinity; plus the two
  separators' own cells at each system's redshift: H_Y (FP9/FP11: L = 2.4615 Omega_L(z) Mpc = 1.690 Mpc at z = 0, its running
  yield y_th(z) included) and H_S (FP13's committed headline, NL, s = delta_c: L(0) = 2.879 Mpc, L(0.25) = 1.914, interpolated
  log-linearly in z; its yield is off at z < 0.635).  H_S as written is linearly ill-posed at z <= 0.635 (XR18) and is being
  repaired in FP19: its cell is FP13's committed length, labelled pending.
The footings: the chain's FP0 values 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt) for every chain cell; the controls use
  the record's own (9.36e-11 / 1.13e-10 for clusters and dwarfs, L23's 9.3619e-11 / 1.1279e-10 for Coma).

CHECKS (controls first; load-bearing unless marked 'reported')
  C1 CONTROL (clusters): with the band-pass removed (L -> oo), the record's kernel and footings, this lane's predictor
     reproduces XR6's committed S0 (XR4's, nu_RAR) and S1 (MOND-sector switch, no cap, nu_mono) rows -- 24 variants x 8 numbers
     -- and XR9's committed uncapped range, to <= 1e-9.  M*'s own kappa-form range (XR9 p1_x2.5, operator A, 2.23-6.28) is NOT
     the L -> oo limit of the chain: M* screens the members beyond its kappa cap (a region rule the chain does not have);
     the difference is printed, not hidden.
  C2 CONTROL (dwarfs): L -> oo with KD's kernel (nu_RAR) reproduces XR4's committed statistic C (observed +0.0800 +- 0.0467,
     predicted -0.1006 / -0.1026, the six CGM x screen variants) and M*'s XR9 p1_x2.5 rows (3.87-4.48 sigma) to <= 1e-9.
  C3 CONTROL (UDGs): L -> oo with L23's kernel reproduces XR6's committed candidate arm (+0.982 / +0.949 dex, floor 0.2175,
     4.35 / 4.20 sigma, range 4.05-4.45) = M*'s XR9 p1_x2.5 UDG rows, to <= 1e-9.
  C4 CONTROL (FP11): FP11's committed two-body numbers (K3: the band-passed dipole kernel against FP6's phantom, momentum,
     Milgrom's deep limit, the test-particle limit) are reproduced EXACTLY from FP11's own exec'd definitions.
  K1 the band-pass of a spherical host: (a) a point mass gives FP11's Efac to 1e-12; (b) an extended (Hernquist) profile's
     shell-sum (FP6's shell_frac) matches a direct quadrature of the Gaussian-smoothed enclosed mass to 1e-4; (c) the grid is
     converged: doubling it moves every member's band-pass fraction by < 1e-3; (d) the smoothing conserves a truncated host's
     total mass (f_bp -> 0 far outside) to 1e-4.
  K2 the reduction's neglected term: the output filter's smoothed phantom (S_L X) varies on the scale L, so its field across a
     satellite is bounded by (r_s/L) of the host phantom -- < 1e-2 of the internal field for every scored object (reported
     worst case).
  K2b, K2c (reported, POST-HOC; see HISTORY) the neglected term's monopole: a loose bound (K2b) and the actual smoothed density (K2c).
  F1 the flux form: no host -> nu_P2(y) (1e-10); a uniform host field in the quasi-Newtonian limit -> nu(e)(1 + L(e)/3) (1e-3);
     64 vs 128 Gauss nodes agree to 1e-6.
  B1 [load-bearing; MUTATE must fail] THE BAND-PASS REMOVES A FAR HOST: a point host at D = 3L keeps Efac(3) = 0.029 of its
     field, and across the cluster members at L = 0.5 Mpc the median e_bp/e_N is < 0.5 (both f_b extents).
  S  the scan tables (reported), the marked H_Y and H_S cells (reported), the flips against M* (reported).
PRE-DECLARED HYPOTHESES (written before any scan cell ran; reported as they fall, never re-worded after the run):
  H1 THE LV DWARFS DO NOT FLIP: statistic C stays >= 3 sigma at every L in [0.5, 5] Mpc on both footings -- the satellites that
     carry it sit within ~0.3 Mpc of the MW/M31, where (1 - S_L) keeps >= 90% of the host field even at L = 0.5 Mpc.
  H2 THE CLUSTER SLOPE FLIPS ONLY AT SHORT L: every variant <= 2 sigma needs L <~ 1 Mpc; at H_Y's (1.69) and H_S's (2.88) L at
     least one variant still fails (> 2 sigma).  At intermediate L the band-pass may steepen the slope (M*'s step, smoothed).
  H3 THE COMA UDGs DO NOT FLIP at any L >= 0.5 Mpc (the isolated floor is ~2.0-2.25 sigma, XR13; P2 raises the offset).
  H4 THE KERNEL: at L -> oo, P2 moves each sample's worst sigma by < 0.5 sigma from the record's kernel.
MUTATE=1: the band-pass WRONGLY PASSES the external field (the host's field enters un-band-passed while the satellite's own field
  is still filtered -- FP11's counterfactual phantom_efe): B1 must FAIL (rc = 1); outputs *_MUTATE.out / *_results_MUTATE.json.
HISTORY (disclosed; three development runs before the committed MUTATE and main runs, all overwritten by them).
  Run 1 (the docstring above as written, checks and hypotheses unchanged since): every control passed; K2 (pre-declared) FAILED --
  its bound |X_host| r_s/L compares the whole variation of S_L X across a satellite with the internal field, while every statistic
  here is a sphere average that feels only the divergence of S_L X.  K2b was then added POST-HOC as a monopole bound; run 2 FAILED
  it too (it put the host's whole phantom mass inside D + 5L into one Gaussian of width L, which overstates the smoothed density by
  orders of magnitude).  K2c was then added POST-HOC: the actual Gaussian-smoothed host phantom density at each object (FP6's shell
  smoothing), beside plain QUMOND's unsmoothed background that the record's forms drop for M* and the chain alike.  K2 and K2b are
  kept as run (reported FAILs, loose bounds, not physics).  Also after run 1: the flux form was extended from five cells to every
  cell, and per-form pass sets were added to section S; run 2 then crashed in S's print loop (a KeyError on the new per-form keys);
  fixed in run 3.  No scan number changed between runs 1 and 3 (the same deterministic code paths).

SCOPE.  Spherical hosts, 1-D kinematic forms (the record's) plus the flux form; member 3-D radii from projected radii (x1, x1.3);
XR4's f_b template; the Coma mass models as XR6 carries them (the beta-model's isothermal tail is extrapolated; the r200
truncation brackets it); hosts' tidal fields and the members' neighbours are not modelled (as in the record); no particle-mesh
run; AQUAL-vs-QUMOND (the chain's root is AQUAL-type; FP11 uses the QUMOND form, <= 0.035 dex on discs, FP7 A3).
Runtime ~5-10 min, single-threaded.  Run from the repository root:
    python3 real_research/cross_thread_review_2026_09_26/XR27_efe_disfavouring.py        (MUTATE=1 for the control)
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR27_efe_disfavouring"
T0 = time.time()


class _Tee:
    def __init__(self, fh): self.fh = fh; self.so = sys.__stdout__
    def write(self, s): self.so.write(s); self.fh.write(s)
    def flush(self): self.so.flush(); self.fh.flush()


if __name__ == "__main__":
    _OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")
    sys.stdout = _Tee(_OUTF)
P = lambda *a: print(*a, flush=True)
CH = []
OUT = {"lane": "XR27 part 1 (EFE-disfavouring samples)", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, load_bearing=True, reading=""):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


# ================================================================================================= read-only loaders
def load_chunks(path, cuts, name):
    """exec the definitions of a committed script (its MUTATE forced off, stdout swallowed); cuts = [(start, end)] markers."""
    ns = {"__name__": name, "__file__": path}
    src = open(path).read().replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    with contextlib.redirect_stdout(io.StringIO()):
        for a_, b_ in cuts:
            chunk = src if a_ is None else src.split(a_)[1]
            chunk = chunk if b_ is None else chunk.split(b_)[0]
            exec(chunk, ns)
    return ns


def exec_ro(path, name):
    """exec a committed chain script whole with __name__ != '__main__' (its main() is not run), MUTATE forced to 0."""
    src = open(path).read(); ns = {"__file__": path, "__name__": name}
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, "exec"), ns)
    finally:
        if old is None: os.environ.pop("MUTATE", None)
        else: os.environ["MUTATE"] = old
    return ns


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the external (host) field enters UN-band-passed; B1 must FAIL (rc = 1) ***")
    MK = "# ============================================================================================ "
    EF = load_chunks(os.path.join(HERE, "XR6_efe_udg_under_candidate.py"),
                     [(None, MK + "PART A clusters"), (MK + "PART A clusters", "F500S = (0.10, 0.13, FCOS)"),
                      (MK + "PART C Coma UDGs", "arm_L23 = lambda")], "xr6_ro")
    F11 = exec_ro(os.path.join(CHAIN, "FP11_local_group_flyby.py"), "fp11_ro")
    M6 = F11["M6"]
    XR4J = json.load(open(os.path.join(HERE, "XR4_efe_under_region_kernel_results.json")))["numbers"]
    XR6J = json.load(open(os.path.join(HERE, "XR6_efe_udg_under_candidate_results.json")))["numbers"]
    XR9J = json.load(open(os.path.join(HERE, "XR9_environment_results.json")))["numbers"]
    F11J = json.load(open(os.path.join(CHAIN, "FP11_local_group_flyby_results.json")))["numbers"]
    F13J = json.load(open(os.path.join(CHAIN, "FP13_separator_from_state_results.json")))["numbers"]
    P(f"\n  XR6's definitions (clusters, dwarfs, L23's Coma pipeline) and FP11's (FP6's band-pass) loaded read-only   {el()}")

    # --------------------------------------------------------------------------------------------- the chain's pieces
    A0C = dict(F11["A0"])                                   # FP0: 9.3603e-11 / 1.1312e-10
    A0R = dict(EF["A0"])                                    # hunt_lib: 9.36e-11 / 1.13e-10 (clusters, dwarfs: the record)
    A0U = dict(EF["A0L"])                                   # L23: 9.3619e-11 / 1.1279e-10 (Coma: the record)
    FOOTS = ("canonical", "alt")
    x_P2, Xfield, Efac_f11, gfrac_f11 = F11["x_P2"], F11["Xfield"], F11["Efac"], F11["gfrac"]
    SHELL, GFR = M6["shell_frac"], M6["gfrac_smooth"]
    LG_OmL = F11["LG_OmL"]; L_LAMBDA = F11["L_LAMBDA"]; HEAD = F11["HEAD"]

    def nu_chain(y, yth=0.0):
        """the chain's kernel: 1 + x_P2(y - y_th)/y (P2 with FP9's yield; y_th = 0 gives sqrt(1 + 1/y) exactly in value)."""
        y = np.maximum(np.asarray(y, float), 1e-300)
        return 1.0 + x_P2(y - (yth or 0.0)) / y

    def Efac(u):
        """(1 - S_L) of a point mass at r/L = u (FP11's Efac); u = 0 (L -> oo) gives exactly 1."""
        u = np.asarray(u, float)
        return np.where(u > 0, 1.0 - gfrac_f11(u), 1.0)

    def L_HY(z):
        return L_LAMBDA * LG_OmL(1.0 / (1.0 + z)) ** (HEAD["n"] / 2.0)             # Mpc (FP11's L_of_a)

    def yth_HY(z):
        return F11["yth_of_a"](1.0 / (1.0 + z))

    _hs = F13J["A2"]["L_kpc"]["NL_1.686"]
    _hz = np.array(sorted(float(k) for k in _hs)); _hl = np.array([math.log(_hs[str(k) if str(k) in _hs else f"{k}"]) for k in _hz])

    def L_HS(z):
        return math.exp(float(np.interp(z, _hz, _hl))) / 1e3                        # Mpc, FP13 NL s = delta_c (log-linear in z)

    P(f"  H_Y: L(z = 0) = {L_HY(0.0):.4f} Mpc, y_th(0) = {yth_HY(0.0):.3e};  H_S (FP13 headline, pending FP19): L(0) = {L_HS(0.0):.4f} Mpc, "
      f"L(0.023) = {L_HS(0.0231):.4f}, L(0.25) = {L_HS(0.25):.4f};  footings (FP0) {A0C['canonical']:.5e} / {A0C['alt']:.5e}")
    LSCAN = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.5, 5.0)

    # --------------------------------------------------------------------------------------------- the band-pass of a host
    def bp_fraction(r, M, L_len):
        """(1 - S_L) of a spherical mass profile M(<r) [any units] on the grid r: returns f_bp = [M - S_L M](<r)/M(<r);
        the innermost mass is a point (FP6's phantom() convention); L_len in r's units; None -> 1."""
        if L_len is None:
            return np.ones_like(r)
        rm = np.sqrt(r[1:] * r[:-1]); dM = np.diff(M)
        Ms = SHELL(r[:, None], rm[None, :], L_len) @ dM + M[0] * GFR(r / L_len)
        return (M - Ms) / np.maximum(M, 1e-300)

    def bp_fraction_many(r, Mcols, L_len):
        """the same for several profiles (columns) sharing one grid: one smoothing matrix per L."""
        if L_len is None:
            return np.ones_like(Mcols)
        rm = np.sqrt(r[1:] * r[:-1]); dM = np.diff(Mcols, axis=0)
        K = SHELL(r[:, None], rm[None, :], L_len)
        Ms = K @ dM + Mcols[0][None, :] * GFR(r / L_len)[:, None]
        return (Mcols - Ms) / np.maximum(Mcols, 1e-300)

    MUG, MUW = np.polynomial.legendre.leggauss(64)

    def nu_flux(m_eff, s, D, ehost, L_len, a0, yth, mu=MUG, w=MUW, eunif=None):
        """FLUX form: <-n.[X(g_s,bp + g_h,bp) - X(g_h,bp)]>_sphere at radius s about the satellite, host at distance D along -z;
        ehost(r) -> band-passed host field magnitude at distance r from the host (vectorised over objects: arrays (n, K)).
        eunif: a uniform field of this magnitude along -z instead (the check F1).  Returns gbar/(G m/s^2) [with G folded in m_eff]."""
        m_eff, s, D = (np.asarray(v, float)[:, None] for v in (m_eff, s, D))
        MU = mu[None, :]; SA = np.sqrt(1.0 - MU ** 2)
        gs = m_eff / s ** 2                                                          # G m/s^2 (m_eff carries G)
        ls = None if L_len is None else L_len
        gsb = gs * (1.0 if ls is None else Efac(s / ls))
        sx, sz = -gsb * SA, -gsb * MU
        if eunif is not None:
            hx = np.zeros_like(sx); hz = -np.asarray(eunif, float)[:, None] * np.ones_like(MU)
        else:
            px, pz = s * SA, s * MU + D                                              # the point relative to the host
            rh = np.sqrt(px ** 2 + pz ** 2); eh = ehost(rh)
            hx, hz = -eh * px / rh, -eh * pz / rh
        Vx, Vz = Xfield(sx + hx, sz + hz, a0, yth); Hx, Hz = Xfield(hx, hz, a0, yth)
        Wn = (Vx - Hx) * SA + (Vz - Hz) * MU
        gbar = gs - 0.5 * (Wn * w[None, :]).sum(axis=1)[:, None]
        return (gbar / gs)[:, 0]

    # ============================================================================================= C4: FP11 reproduced
    banner("C4  FP11's COMMITTED TWO-BODY NUMBERS FROM ITS OWN DEFINITIONS (read-only)")
    dg_body, g_iso, nu_p2f, G11, MS11, MPC11, FMW = (F11[k] for k in ("dg_body", "g_iso", "nu_p2", "G", "MSUN", "MPC", "FMW"))
    a0c = A0C["canonical"]; kern = []
    for (mB, d, Lz, yt) in ((1.2e11, 0.78, None, None), (1.2e11, 0.78, 1.69, 3.5e-7), (1.2e11, 0.3, 0.183, 2.5e-3), (6e10, 0.1, 0.5, None)):
        Lm = None if Lz is None else Lz * MPC11
        gz = dg_body(6e10 * MS11, mB * MS11, d * MPC11, a0c, Lm, yt, ns=500, control_W="Biso")
        ref = g_iso(mB * MS11, a0c, Lm, yt, np.array([d * MPC11]))[0]
        kern.append(abs(-gz / ref - 1))
    mom, mil = [], []
    for (mA, mB, d) in ((0.37 * 1.75e11, 0.63 * 1.75e11, 0.78), (1e11, 1e11, 0.78), (0.37 * 1.75e11, 0.63 * 1.75e11, 3.0), (0.37 * 1.75e11, 0.63 * 1.75e11, 0.2)):
        dA = dg_body(mA * MS11, mB * MS11, d * MPC11, a0c, None, None); dB = dg_body(mB * MS11, mA * MS11, d * MPC11, a0c, None, None)
        gNB, gNA = G11 * mB * MS11 / (d * MPC11) ** 2, G11 * mA * MS11 / (d * MPC11) ** 2
        aA = float(nu_p2f(gNB / a0c)) * gNB - dA; aB = float(nu_p2f(gNA / a0c)) * gNA - dB
        mom.append(abs(mA * aA / (mB * aB) - 1))
        M = (mA + mB) * MS11; Fm = (2 / 3) * math.sqrt(G11 * a0c) * (M ** 1.5 - (mA * MS11) ** 1.5 - (mB * MS11) ** 1.5) / (d * MPC11)
        mil.append([d, aA / (Fm / (mA * MS11) + gNB)])
    tp = []
    for q in (1e-4, 1e-2):
        mA, mB, d = 1.2e11, 1.2e11 * q, 0.5
        dB = dg_body(mB * MS11, mA * MS11, d * MPC11, a0c, None, None, smin_fac=1e-7, ns=900)
        gA = float(nu_p2f(G11 * mA * MS11 / (d * MPC11) ** 2 / a0c)) * G11 * mA * MS11 / (d * MPC11) ** 2
        tp.append([q, (gA - dB) / gA, (2 / 3) * ((1 + q) ** 1.5 - 1 - q ** 1.5) / q])
    ref3 = F11J["K3"]
    dk3 = max([abs(a - b) for a, b in zip(kern, ref3["kernel"])] + [abs(a - b) for a, b in zip(mom, ref3["momentum"])]
              + [abs(a[1] - b[1]) for a, b in zip(mil, ref3["milgrom"])] + [abs(a[1] - b[1]) + abs(a[2] - b[2]) for a, b in zip(tp, ref3["test_particle"])])
    check("C4 CONTROL (FP11): FP11's committed K3 numbers -- the band-passed dipole kernel against FP6's phantom (4 cells), momentum "
          "(4), Milgrom's deep two-body limit (4), the test-particle limit (2) -- reproduced exactly from FP11's exec'd definitions",
          f"max |diff| vs FP11's JSON {dk3:.1e}; kernel devs {', '.join(f'{v:.1e}' for v in kern)}; test-particle (q = 1e-2) "
          f"{tp[1][1]:.6f} (exact {tp[1][2]:.6f})", dk3 == 0.0 or dk3 < 1e-12)
    OUT["numbers"]["C4_FP11_K3"] = dict(kernel=kern, momentum=mom, milgrom=mil, test_particle=tp, max_diff=dk3)

    # ============================================================================================= K1 band-pass machinery
    banner("K1  THE BAND-PASS OF A SPHERICAL HOST (FP6's shell smoothing, read-only) AND F1 THE FLUX FORM")
    rg = np.geomspace(1e-4, 80.0, 1400)                                               # Mpc
    kpt = float(np.max(np.abs(bp_fraction(rg, np.full_like(rg, 1.0), 0.7) - (1.0 - GFR(rg / 0.7)))))
    kpt2 = float(np.max(np.abs(Efac(rg / 0.7) - (1.0 - GFR(rg / 0.7)))))
    # (b) a Hernquist host against a direct quadrature of the Gaussian-smoothed enclosed mass
    aH = 0.3; MH = lambda r: r ** 2 / (r + aH) ** 2                                   # unit mass, a = 0.3 Mpc
    rhoH = lambda r: aH / (2 * math.pi * r * (r + aH) ** 3)

    def smoothed_M(r, L_):
        def rho_s(x):                                                                # Gaussian-smoothed density at radius x
            f = lambda rp: rhoH(rp) * 4 * math.pi * rp ** 2 * (L_ ** 2 / (2 * x * rp)) * (math.exp(-(x - rp) ** 2 / (2 * L_ ** 2))
                                                                                       - math.exp(-(x + rp) ** 2 / (2 * L_ ** 2))) / (2 * math.pi * L_ ** 2) ** 1.5
            return quad(f, 1e-9, max(x + 12 * L_, 50.0), limit=400, points=[x])[0]
        return quad(lambda x: 4 * math.pi * x ** 2 * rho_s(x), 1e-6, r, limit=200)[0]
    kq = []
    for L_ in (0.5, 1.7):
        fg = bp_fraction(rg, MH(rg), L_)
        for rr in (0.2, 0.8, 2.0):
            fq = (MH(rr) - smoothed_M(rr, L_)) / MH(rr)
            kq.append(abs(float(np.interp(math.log(rr), np.log(rg), fg)) - fq))
    check("K1a/b THE BAND-PASS OF A SPHERICAL HOST: a point mass gives FP11's Efac (1 - gfrac(r/L)) to 1e-12; a Hernquist host's "
          "shell-sum (FP6's shell_frac) matches a direct quadrature of the Gaussian-smoothed enclosed mass (L = 0.5, 1.7 Mpc; r = 0.2, "
          "0.8, 2 Mpc) to 1e-4", f"point mass {max(kpt, kpt2):.1e}; Hernquist max |d f_bp| {max(kq):.1e}", max(kpt, kpt2) < 1e-12 and max(kq) < 1e-4)
    # F1 the flux form's limits
    ys = np.array([1e-3, 1e-2, 0.1, 1.0, 10.0])
    f_no = nu_flux(ys * a0c, np.ones(5), np.full(5, 1e9), lambda r: 0.0 * r, None, a0c, 0.0, eunif=np.zeros(5))
    d_no = float(np.max(np.abs(f_no / nu_chain(ys) - 1)))
    ye = np.array([1e-3, 1e-2, 0.1, 1.0]); yi = ye * 1e-4
    f_qn = nu_flux(yi * a0c, np.ones(4), np.full(4, 1e9), None, None, a0c, 0.0, eunif=ye * a0c)
    Lsl = np.array([(math.log(nu_chain(y * (1 + 1e-5))) - math.log(nu_chain(y * (1 - 1e-5)))) / 2e-5 for y in ye])
    d_qn = float(np.max(np.abs(f_qn / (nu_chain(ye) * (1 + Lsl / 3)) - 1)))
    MUG2, MUW2 = np.polynomial.legendre.leggauss(128)
    yq = np.array([0.01, 0.1, 1.0]); eq = np.array([0.05, 0.02, 0.3])
    f64 = nu_flux(yq * a0c, np.full(3, 1.0), np.full(3, 30.0), lambda r: eq[:, None] * a0c * (30.0 / r) ** 2, None, a0c, 0.0)
    f128 = nu_flux(yq * a0c, np.full(3, 1.0), np.full(3, 30.0), lambda r: eq[:, None] * a0c * (30.0 / r) ** 2, None, a0c, 0.0, mu=MUG2, w=MUW2)
    d_gl = float(np.max(np.abs(f64 / f128 - 1)))
    check("F1 THE FLUX FORM: with no host it returns nu_P2(y) (1e-10); in a uniform host field in the quasi-Newtonian limit it returns "
          "nu(e)(1 + L(e)/3), L23's 'sphere' coupling (1e-3); 64 vs 128 Gauss nodes agree (1e-6)",
          f"no host {d_no:.1e}; quasi-Newtonian {d_qn:.1e}; nodes {d_gl:.1e}", d_no < 1e-10 and d_qn < 1e-3 and d_gl < 1e-6)
    OUT["numbers"]["K1"] = dict(point=max(kpt, kpt2), hernquist=kq, flux_no_host=d_no, flux_quasi_newtonian=d_qn, flux_nodes=d_gl)
    P(f"    {el()}")

    # ============================================================================================= PART A clusters
    banner("PART A -- THE CLUSTER-INFALL BTFR (N = 314) in the band-passed law")
    KC, KD = EF["KC"], EF["KD"]
    G, MSUN, MPC = EF["G"], EF["MSUN"], EF["MPC"]; KPC = MPC / 1e3
    gal, cls, idx, memb, Vv, Mbg, lHIall, RHI, gNint, used = (EF[k] for k in ("gal", "cls", "idx", "memb", "V", "Mb", "lHIall", "RHI", "gN", "used"))
    Rp = EF["Rp"]; cluster_Mb, fb_profile, regress, boot_err, zero_point, nu_mono = (EF[k] for k in (
        "cluster_Mb", "fb_profile", "regress", "boot_err", "zero_point", "nu_mono"))
    F500S = (0.10, 0.13, EF["FCOS"]); GEOS = (("R_proj", 1.0), ("1.3 R_proj", 1.3)); EXTS = ("extended", "r200")
    mi = np.where(memb)[0]

    # member geometry (per geometry), the committed regressor, e_in (XR6's in-region baryonic field), e0 (XR4's)
    GEO = {}
    for geo, dp in GEOS:
        r_m = np.zeros(len(gal)); x_m = np.zeros(len(gal)); ge = np.zeros(len(gal)); zc = np.zeros(len(gal))
        for i in mi:
            c = cls[idx[i]]; r = max(Rp[i] * dp, 0.05 * c["r500"])
            r_m[i] = r; x_m[i] = r / c["r500"]; zc[i] = c["z"]
            ge[i] = G * KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN / r ** 2
        e_in = {}
        for f500 in F500S:
            for ext in EXTS:
                e = np.zeros(len(gal))
                for i in mi:
                    c = cls[idx[i]]; r = r_m[i]
                    e[i] = G * float(cluster_Mb(c, f500, ext, np.array([r]))[0]) / r ** 2
                e_in[(f500, ext)] = e
        GEO[geo] = dict(r_m=r_m, x_m=x_m, ge=ge, zc=zc, e_in=e_in)

    # the cluster baryon profiles on one shared grid, band-pass fractions per L (one smoothing matrix per L)
    RGc = np.geomspace(1e-3, 60.0, 1400) * MPC
    PROF_KEYS = [(j, f500, ext) for j in used for f500 in F500S for ext in EXTS]
    MCOL = np.column_stack([cluster_Mb(cls[j], f500, ext, RGc) for (j, f500, ext) in PROF_KEYS])
    lRGc = np.log(RGc)

    def fbp_members(L_mpc, geo, f500, ext, grid=None, mcols=None):
        """band-pass fraction e_bp/e_N at every member's 3-D radius for one (f500, ext); L_mpc None -> 1 (L -> oo)."""
        out = np.ones(len(gal))
        if L_mpc is None:
            return out
        key = (L_mpc, grid is None)
        if key not in _FB_CACHE:
            rr = RGc if grid is None else grid
            mc = MCOL if mcols is None else mcols
            _FB_CACHE[key] = bp_fraction_many(rr, mc, L_mpc * MPC)
        FB = _FB_CACHE[key]; lr = lRGc if grid is None else np.log(grid)
        r_m = GEO[geo]["r_m"]
        for i in mi:
            k = PROF_KEYS.index((int(idx[i]), f500, ext))
            out[i] = float(np.interp(math.log(r_m[i]), lr, FB[:, k]))
        return out
    _FB_CACHE = {}

    def predict_forms(e, a0, knu, fint=None):
        """the record's two forms with the chain's internal band-pass: V^2 = [g_N + (nu - 1) g_N,bp] R_HI (scalar sum) and
        g = g_N + (nu_t - 1)(g_N,bp + e) - (nu_e - 1) e (1-D subtract; = nu_t (g_N + e) - nu_e e at fint = 1)."""
        gNb = gNint if fint is None else gNint * fint
        y = (gNb + e) / a0
        if fint is None:
            Dp = np.log10(np.sqrt(knu(y) * G * Mbg / RHI)) - 0.25 * np.log10(G * Mbg * a0)
            gi = knu(y) * (gNb + e) - np.where(e > 0, knu(np.maximum(e, 1e-30) / a0) * e, 0.0)
        else:
            Dp = np.log10(np.sqrt((1.0 + (knu(y) - 1.0) * fint) * G * Mbg / RHI)) - 0.25 * np.log10(G * Mbg * a0)
            gi = gNint + (knu(y) - 1.0) * (gNb + e) - np.where(e > 0, (knu(np.maximum(e, 1e-30) / a0) - 1.0) * e, 0.0)
        Dq = np.log10(np.sqrt(np.maximum(gi, 1e-30) * RHI)) - 0.25 * np.log10(G * Mbg * a0)
        return Dp, Dq

    BOOT = {}

    def score_clusters(A0set, knu_of_z, L_of_z, tag, flux=False, e_mode="bp"):
        """every variant: slopes (scalar, subtract[, flux]) and sigma from the observed; the zero point.  L_of_z(z) -> L [Mpc] or
        None; knu_of_z(z) -> the kernel at the member's epoch.  e_mode 'bp' (the chain), 'raw' (MUTATE: host un-band-passed)."""
        res = {}
        for foot in FOOTS:
            a0 = A0set[foot]
            Dobs = np.log10(Vv * 1e3) - 0.25 * np.log10(G * Mbg * a0)
            for geo, _ in GEOS:
                ge = GEO[geo]["ge"]; lge = np.log10(ge[memb] / a0); zc = GEO[geo]["zc"]
                bk = (tag.split("|")[0], foot, geo)
                if bk not in BOOT: BOOT[bk] = boot_err(Dobs, memb, lge)
                sobs, eobs = BOOT[bk]
                Lz = np.array([L_of_z(zc[i]) if L_of_z(zc[i]) is not None else np.inf for i in range(len(gal))])
                for f500 in F500S:
                    for ext in EXTS:
                        e = GEO[geo]["e_in"][(f500, ext)].copy()
                        fint = None
                        if np.isfinite(Lz[mi]).any():
                            fb = np.ones(len(gal))
                            for Lv in sorted(set(Lz[mi][np.isfinite(Lz[mi])])):
                                sel = mi[Lz[mi] == Lv]
                                fbL = fbp_members(float(Lv), geo, f500, ext)
                                fb[sel] = fbL[sel]
                            fint = np.ones(len(gal)); fin = np.isfinite(Lz)
                            fint[fin] = Efac(RHI[fin] / (Lz[fin] * MPC))
                            if e_mode == "bp":
                                e = e * fb
                        knu = knu_of_z(float(np.median(zc[mi])))
                        Dp, Dq = predict_forms(e, a0, knu, fint)
                        sp, _ = regress(Dp, memb, lge); sq, _ = regress(Dq, memb, lge)
                        co, cp, sej = zero_point(Dobs, Dp, f"{tag.split('|')[0]}/{foot}/{geo}")
                        row = dict(slope_scalar=float(sp), sigma_scalar=float(abs(sobs - sp) / eobs), slope_subtract=float(sq),
                                   sigma_subtract=float(abs(sobs - sq) / eobs), zp_obs=float(co), zp_pred=float(cp), zp_err=float(sej),
                                   zp_sigma=float(abs(co - cp) / sej), obs=float(sobs), err=float(eobs))
                        if flux:
                            # host field magnitude at distance r from the cluster centre: e_N(r) f_bp(r), per member's cluster and L
                            nf = np.ones(len(gal)); yth = float(flux) if not isinstance(flux, bool) else 0.0
                            for j in used:
                                sel = mi[idx[mi] == j]
                                if not sel.size: continue
                                Lf = float(Lz[sel[0]]); Lm = None if not np.isfinite(Lf) else Lf * MPC
                                if Lm is not None:
                                    fbp_members(Lf, geo, f500, ext)                    # fills the cache for this L
                                k = PROF_KEYS.index((j, f500, ext))
                                col = MCOL[:, k]
                                fcol = np.ones_like(col) if (Lm is None or e_mode != "bp") else _FB_CACHE[(Lf, True)][:, k]
                                eprof = G * col * fcol / RGc ** 2
                                eh = lambda rr, ep=eprof: np.interp(np.log(rr), lRGc, ep)
                                nf[sel] = nu_flux(G * Mbg[sel], RHI[sel], GEO[geo]["r_m"][sel], eh, Lm, a0, yth)
                            Df = np.log10(np.sqrt(nf * G * Mbg / RHI)) - 0.25 * np.log10(G * Mbg * a0)
                            sf, _ = regress(Df, memb, lge)
                            row.update(slope_flux=float(sf), sigma_flux=float(abs(sobs - sf) / eobs))
                        res[f"{foot}/{geo}/{f500}/{ext}"] = row
        return res

    # ---- C1 the controls: L -> oo, the record's kernels and footings
    kc_nu, EFnu = KC.nu, nu_mono
    C1S0 = score_clusters(A0R, lambda z: kc_nu, lambda z: None, "rec|S0")
    C1S1 = score_clusters(A0R, lambda z: EFnu, lambda z: None, "rec|S1")
    dS0 = dS1 = 0.0
    for key, ref in XR6J["clusters"].items():
        for k_ in ("slope_scalar", "sigma_scalar", "slope_subtract", "sigma_subtract", "zp_obs", "zp_pred", "zp_err", "zp_sigma"):
            dS1 = max(dS1, abs(C1S1[key][k_] - ref["rows"]["S1 MOND-sector switch, no cap"][k_]))
        dS1 = max(dS1, abs(C1S1[key]["obs"] - ref["obs"]), abs(C1S1[key]["err"] - ref["err"]))
    # S0 = XR4's switch uses e0 = fb_profile(x) g_e on the 'extended' keys: rebuild it exactly as XR6 did
    S0rows = {}
    for foot in FOOTS:
        a0 = A0R[foot]; Dobs = np.log10(Vv * 1e3) - 0.25 * np.log10(G * Mbg * a0)
        for geo, _ in GEOS:
            ge, x_m = GEO[geo]["ge"], GEO[geo]["x_m"]; lge = np.log10(ge[memb] / a0); sobs, eobs = BOOT[("rec", foot, geo)]
            for f500 in F500S:
                e0 = np.zeros(len(gal)); e0[memb] = fb_profile(x_m[memb], f500) * ge[memb]
                Dp, Dq = predict_forms(e0, a0, kc_nu)
                sp, _ = regress(Dp, memb, lge); sq, _ = regress(Dq, memb, lge)
                co, cp, sej = zero_point(Dobs, Dp, f"rec/{foot}/{geo}")
                ref = XR6J["clusters"][f"{foot}/{geo}/{f500}/extended"]["rows"]["S0 XR4 switch, no cap (nu_RAR)"]
                mine = dict(slope_scalar=sp, sigma_scalar=abs(sobs - sp) / eobs, slope_subtract=sq, sigma_subtract=abs(sobs - sq) / eobs,
                            zp_obs=co, zp_pred=cp, zp_err=sej, zp_sigma=abs(co - cp) / sej)
                dS0 = max(dS0, max(abs(mine[k_] - ref[k_]) for k_ in ref))
                S0rows[f"{foot}/{geo}/{f500}"] = mine
    sig_unc = [C1S1[k][f] for k in C1S1 for f in ("sigma_scalar", "sigma_subtract")]
    x9 = XR9J["clusters"]["p1_x2.5"]
    d9u = max(abs(min(sig_unc) - x9["sigma_uncapped"][0]), abs(max(sig_unc) - x9["sigma_uncapped"][1]))
    check("C1 CONTROL (clusters): with the band-pass removed (L -> oo) and the record's kernels and footings, this lane's predictor "
          "reproduces XR6's committed S0 (XR4's, nu_RAR) and S1 (MOND-sector switch, no cap, nu_mono) rows -- 24 variants x 8 numbers -- "
          "and XR9's committed uncapped sigma range", f"S0 max |diff| {dS0:.1e}; S1 max |diff| {dS1:.1e}; uncapped range "
          f"{min(sig_unc):.4f}-{max(sig_unc):.4f} vs XR9 {x9['sigma_uncapped'][0]:.4f}-{x9['sigma_uncapped'][1]:.4f} ({d9u:.1e})",
          dS0 < 1e-9 and dS1 < 1e-9 and d9u < 1e-9,
          reading=f"M*'s own number is XR9's kappa-form operator A, {x9['sigma_range'][0]:.2f}-{x9['sigma_range'][1]:.2f} sigma: NOT the chain's "
                  f"L -> oo limit, because M* screens members beyond its kappa cap (a region rule the chain does not have; XR9 puts "
                  f"{100 * (1 - x9['fraction_inside']['canonical']['galaxy']):.0f}% ('galaxy') / {100 * (1 - x9['fraction_inside']['canonical']['twofield']):.0f}% "
                  f"('two-field') of the members outside the host region at that cell).  The chain's L -> oo limit is XR6's S1 row.")
    OUT["numbers"]["C1"] = dict(dS0=dS0, dS1=dS1, uncapped_range=[min(sig_unc), max(sig_unc)], Mstar_kappa_range=x9["sigma_range"],
                                Mstar_fraction_inside=x9["fraction_inside"])
    P(f"    {el()}")

    # ---- the chain's scan
    def summarize_clusters(R):
        sg = [R[k][f] for k in R for f in ("sigma_scalar", "sigma_subtract")]
        cen = [R[k][f] for k in R if k.split("/")[1:] == ["R_proj", "0.13", "extended"] for f in ("sigma_scalar", "sigma_subtract")]
        zp = [R[k]["zp_sigma"] for k in R]
        byf = {f: [min(R[k][f] for k in R), max(R[k][f] for k in R)] for f in ("sigma_scalar", "sigma_subtract")}
        byext = {x: [min(R[k][f] for k in R if k.endswith("/" + x) for f in ("sigma_scalar", "sigma_subtract")),
                     max(R[k][f] for k in R if k.endswith("/" + x) for f in ("sigma_scalar", "sigma_subtract"))] for x in EXTS}
        sl = {f: [min(R[k][s] for k in R), max(R[k][s] for k in R)] for f, s in (("scalar", "slope_scalar"), ("subtract", "slope_subtract"))}
        out = dict(sigma_range=[min(sg), max(sg)], sigma_central=[min(cen), max(cen)], zp_range=[min(zp), max(zp)], by_form=byf,
                   by_extent=byext, slopes=sl, pass_=max(sg) <= 2.0, below3=max(sg) < 3.0,
                   pass_scalar=byf["sigma_scalar"][1] <= 2.0, pass_subtract=byf["sigma_subtract"][1] <= 2.0, zp_pass=max(zp) <= 2.0)
        if "sigma_flux" in next(iter(R.values())):
            fl = [R[k]["sigma_flux"] for k in R]; out["flux_range"] = [min(fl), max(fl)]; out["pass_flux"] = max(fl) <= 2.0
        return out

    e_mode = "raw" if MUTATE else "bp"
    knuP2 = lambda z: (lambda y: nu_chain(y, 0.0))
    CL = {}
    for Lv in (None,) + LSCAN:
        R = score_clusters(A0C, knuP2, (lambda z, Lv=Lv: Lv), "chain", flux=True, e_mode=e_mode)
        CL["inf" if Lv is None else f"{Lv:g}"] = dict(summary=summarize_clusters(R), rows=R if Lv in (None, 0.5, 1.0, 1.6, 2.8) else None)
        s = CL["inf" if Lv is None else f"{Lv:g}"]["summary"]
        P(f"  L = {'oo' if Lv is None else f'{Lv:4.2f}':>4s} Mpc: slope sigma all variants {s['sigma_range'][0]:.2f}-{s['sigma_range'][1]:.2f} "
          f"(scalar {s['by_form']['sigma_scalar'][0]:.2f}-{s['by_form']['sigma_scalar'][1]:.2f}, subtract {s['by_form']['sigma_subtract'][0]:.2f}-"
          f"{s['by_form']['sigma_subtract'][1]:.2f}; extended {s['by_extent']['extended'][1]:.2f} / r200 {s['by_extent']['r200'][1]:.2f} worst); "
          f"central {s['sigma_central'][0]:.2f}-{s['sigma_central'][1]:.2f}; zero point {s['zp_range'][0]:.2f}-{s['zp_range'][1]:.2f}"
          + (f"; flux form {s['flux_range'][0]:.2f}-{s['flux_range'][1]:.2f}" if "flux_range" in s else "")
          + f" -> {'PASS' if s['pass_'] else 'fail'}   {el()}")
    # the two separators' own cells, at each cluster's redshift
    RHY = score_clusters(A0C, lambda z: (lambda y, yt=yth_HY(z): nu_chain(y, yt)), L_HY, "chain|HY", flux=yth_HY(0.04), e_mode=e_mode)
    RHS = score_clusters(A0C, knuP2, L_HS, "chain|HS", flux=True, e_mode=e_mode)
    CL["H_Y"] = dict(summary=summarize_clusters(RHY), rows=RHY); CL["H_S"] = dict(summary=summarize_clusters(RHS), rows=RHS)
    zcs = sorted(set(float(cls[j]["z"]) for j in used))
    for nm in ("H_Y", "H_S"):
        s = CL[nm]["summary"]; Lr = (L_HY if nm == "H_Y" else L_HS)
        P(f"  {nm} (L = {Lr(zcs[0]):.3f}-{Lr(zcs[-1]):.3f} Mpc at z = {zcs[0]:.3f}-{zcs[-1]:.3f}): slope sigma {s['sigma_range'][0]:.2f}-{s['sigma_range'][1]:.2f} "
          f"(scalar {s['by_form']['sigma_scalar'][0]:.2f}-{s['by_form']['sigma_scalar'][1]:.2f}, subtract {s['by_form']['sigma_subtract'][0]:.2f}-"
          f"{s['by_form']['sigma_subtract'][1]:.2f}; flux form {s['flux_range'][0]:.2f}-{s['flux_range'][1]:.2f}); zero point {s['zp_range'][0]:.2f}-"
          f"{s['zp_range'][1]:.2f} -> {'PASS' if s['pass_'] else 'fail'}")
    OUT["numbers"]["clusters"] = CL
    # the kernel alone at L -> oo (the record's nu_mono at FP0's footings) for H4
    Rk = score_clusters(A0C, lambda z: EFnu, lambda z: None, "chainkern|mono")
    OUT["numbers"]["clusters_kernel_mono_Loo"] = summarize_clusters(Rk)
    P(f"  kernel check at L -> oo: nu_mono at FP0 footings {OUT['numbers']['clusters_kernel_mono_Loo']['sigma_range'][0]:.2f}-"
      f"{OUT['numbers']['clusters_kernel_mono_Loo']['sigma_range'][1]:.2f} vs P2 {CL['inf']['summary']['sigma_range'][0]:.2f}-{CL['inf']['summary']['sigma_range'][1]:.2f}")

    # K1c grid convergence and K1d mass conservation (clusters)
    RGc2 = np.geomspace(1e-3, 60.0, 2800) * MPC
    MCOL2 = np.column_stack([cluster_Mb(cls[j], f500, ext, RGc2) for (j, f500, ext) in PROF_KEYS])
    dconv = 0.0
    for Lv in (0.5, 1.7, 5.0):
        F1_ = bp_fraction_many(RGc, MCOL, Lv * MPC); F2_ = bp_fraction_many(RGc2, MCOL2, Lv * MPC)
        for geo, _ in GEOS:
            r_m = GEO[geo]["r_m"]
            for i in mi[::3]:
                for f500 in F500S:
                    for ext in EXTS:
                        k = PROF_KEYS.index((int(idx[i]), f500, ext))
                        a = float(np.interp(math.log(r_m[i]), lRGc, F1_[:, k])); b = float(np.interp(math.log(r_m[i]), np.log(RGc2), F2_[:, k]))
                        dconv = max(dconv, abs(a - b))
    tr = [k for k, (j, f500, ext) in enumerate(PROF_KEYS) if ext == "r200"]
    Ftr = bp_fraction_many(RGc, MCOL[:, tr], 1.0 * MPC)
    far = RGc > 30.0 * MPC
    dcons = float(np.max(np.abs(Ftr[far])))
    check("K1c/d THE GRID: doubling the shared cluster grid moves every member's band-pass fraction by < 1e-3 (L = 0.5, 1.7, 5 Mpc), and "
          "the smoothing conserves a truncated host's mass (f_bp -> 0 beyond 30 Mpc at L = 1 Mpc) to 1e-4",
          f"max |d f_bp| {dconv:.1e}; max |f_bp| beyond 30 Mpc {dcons:.1e}", dconv < 1e-3 and dcons < 1e-4)

    # B1 the band-pass removes a far host
    fb05 = [np.median(fbp_members(0.5, "R_proj", 0.13, ext)[mi]) for ext in EXTS]
    e3 = float(Efac(3.0))
    fb05_eff = fb05 if not MUTATE else [1.0, 1.0]
    e3_eff = e3 if not MUTATE else 1.0
    s05 = CL["0.5"]["summary"]["sigma_range"][1]; sinf = CL["inf"]["summary"]["sigma_range"][1]
    check("B1 THE BAND-PASS REMOVES A FAR HOST (MUTATE must fail): a point host at D = 3L keeps Efac(3) = 0.029 of its field, and across "
          "the members at L = 0.5 Mpc the median e_bp/e_N is < 0.5 (both extents); the scored slope responds (worst sigma at 0.5 Mpc vs L -> oo)",
          f"Efac(3) as scored {e3_eff:.4f}; median e_bp/e_N at L = 0.5 Mpc as scored: extended {fb05_eff[0]:.3f}, r200 {fb05_eff[1]:.3f}; worst sigma "
          f"{s05:.2f} (0.5 Mpc) vs {sinf:.2f} (oo)", e3_eff < 0.05 and max(fb05_eff) < 0.5 and abs(s05 - sinf) > 0.5)
    OUT["numbers"]["B1"] = dict(Efac3=e3, median_fbp_05=fb05, scored=dict(Efac3=e3_eff, median=fb05_eff))
    P(f"    {el()}")

    # ============================================================================================= PART B dwarfs
    banner("PART B -- THE LOCAL VOLUME DWARFS (N = 92): statistic C in the band-passed law")
    d = KD.load(ups_v=2.0)
    lsig = np.log10(np.array([g_["sig"] for g_ in d])); lM = np.log10(np.array([g_["Mb"] for g_ in d]))
    lrh = np.log10(np.array([g_["rh"] / KD.PC for g_ in d]))
    dmw = np.array([g_["dmw"] for g_ in d]); dm31 = np.array([g_["dm31"] for g_ in d]); gNe0 = np.array([g_["gNe"] for g_ in d])
    Mbd = np.array([g_["Mb"] for g_ in d]) * KD.MSUN; rhd = np.array([g_["rh"] for g_ in d])
    okmw = np.isfinite(dmw) & (dmw > 0); ok31 = np.isfinite(dm31) & (dm31 > 0)
    DW_OBS = {}

    def dwarf_obs(A0set, tag):
        for foot in FOOTS:
            a0 = A0set[foot]; lge = np.log10(KD.true_external_field(gNe0, a0) / a0)
            q = [lM, lrh, lM * lM, lrh * lrh, lM * lrh, lge]
            cobs, _ = KD.partial_slope(lsig, q); eobs = KD.boot_slope(lsig, q)
            DW_OBS[(tag, foot)] = (q, float(cobs), float(eobs))

    def sigma_pred(a0, knu, gNe, fint=None):
        """KD.predict_sigma's formula (beta = 2/9) with the chain's internal band-pass (fint = Efac(r_h/L))."""
        gNi = KD.G * Mbd / rhd ** 2
        if fint is None:
            return np.sqrt((2.0 / 9.0) * knu((gNi + gNe) / a0) * KD.G * Mbd / rhd) / 1e3
        y = (gNi * fint + gNe) / a0
        return np.sqrt((2.0 / 9.0) * (1.0 + (knu(y) - 1.0) * fint) * KD.G * Mbd / rhd) / 1e3

    def host_field(cgm, L_mpc, mode="bp"):
        """the larger of the two hosts' (band-passed, point-mass) Newtonian fields; KD's convention."""
        uM = 1.0 if L_mpc is None else 1.0 / (L_mpc * 1e3)                            # dmw, dm31 in kpc
        fmw = np.where(okmw, KD.G * KD.M_MW_BAR * cgm * KD.MSUN / (np.where(okmw, dmw, 1.0) * KD.KPC) ** 2, 0.0)
        f31 = np.where(ok31, KD.G * KD.M_M31_BAR * cgm * KD.MSUN / (np.where(ok31, dm31, 1.0) * KD.KPC) ** 2, 0.0)
        if L_mpc is not None and mode == "bp":
            fmw = fmw * Efac(np.where(okmw, dmw, 0.0) * uM); f31 = f31 * Efac(np.where(ok31, dm31, 0.0) * uM)
        return np.maximum(fmw, f31), fmw >= f31

    dwarf_obs(A0R, "rec"); dwarf_obs(A0C, "chain")
    # C2 controls
    dC2 = 0.0
    for foot in FOOTS:
        q, cobs, eobs = DW_OBS[("rec", foot)]; ref = XR4J["dwarfs"][foot]
        dC2 = max(dC2, abs(cobs - ref["obs"]), abs(eobs - ref["err"]))
        dC2 = max(dC2, abs(KD.partial_slope(np.log10(sigma_pred(A0R[foot], KD.nu, gNe0)), q)[0] - ref["committed"]))
        for cgm in (1.0, 1.5, 2.0):
            for scr in (None, 1.2):
                g_new = gNe0 * cgm
                if scr is not None:
                    farr = np.fmin(np.where(np.isfinite(dmw), dmw, np.inf), np.where(np.isfinite(dm31), dm31, np.inf)) > 1e3 * scr
                    g_new = np.where(farr, 1e-30, g_new)
                sp = KD.partial_slope(np.log10(sigma_pred(A0R[foot], KD.nu, g_new)), q)[0]
                rv = ref["variants"][f"cgm{cgm}_screen{scr}"]
                dC2 = max(dC2, abs(sp - rv["slope"]), abs(abs(cobs - sp) / eobs - rv["sigma"]))
            sp = KD.partial_slope(np.log10(sigma_pred(A0R[foot], KD.nu, gNe0 * cgm)), q)[0]
            r9 = XR9J["dwarfs"]["p1_x2.5"]["rows"][f"{foot}/{cgm}"]
            dC2 = max(dC2, abs(sp - r9["slope"]), abs(abs(cobs - sp) / eobs - r9["sigma"]))
    # KD's own predict_sigma equals this lane's at L -> oo
    dd_ = [dict(g_, gNe=gg) for g_, gg in zip(d, gNe0)]
    dKD = float(np.max(np.abs(KD.predict_sigma(dd_, A0R["canonical"]) - sigma_pred(A0R["canonical"], KD.nu, gNe0))))
    s9 = XR9J["dwarfs"]["p1_x2.5"]["sigma_range"]
    check("C2 CONTROL (dwarfs): L -> oo with KD's kernel reproduces XR4's committed statistic C (observed, the committed prediction, "
          "six CGM x screen variants, both footings) and M*'s XR9 p1_x2.5 rows (host baryons x1/x1.5/x2)",
          f"max |diff| {dC2:.1e}; KD.predict_sigma vs this lane {dKD:.1e}; M* range {s9[0]:.2f}-{s9[1]:.2f} sigma", dC2 < 1e-9 and dKD < 1e-12)

    def score_dwarfs(A0set, knu, L_mpc, tag, mode="bp", flux=False):
        out = {}
        for foot in FOOTS:
            a0 = A0set[foot]; q, cobs, eobs = DW_OBS[(tag, foot)]
            for cgm in (1.0, 1.5, 2.0):
                gNe, host_mw = host_field(cgm, L_mpc, mode)
                fint = None if L_mpc is None else Efac(rhd / (L_mpc * 1e3 * KD.KPC))
                sp = KD.partial_slope(np.log10(sigma_pred(a0, knu, gNe, fint)), q)[0]
                row = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs), obs=cobs, err=eobs,
                           host_frac_median_inner=float(np.median((gNe / (host_field(cgm, None)[0]))[np.fmin(np.where(okmw, dmw, np.inf), np.where(ok31, dm31, np.inf)) < 300.0])))
                if flux:
                    Lm = None if L_mpc is None else L_mpc * 1e3 * KD.KPC
                    Mh = np.where(host_mw, KD.M_MW_BAR, KD.M_M31_BAR) * cgm * KD.MSUN
                    Dh = np.where(host_mw, np.where(okmw, dmw, np.nan), np.where(ok31, dm31, np.nan)) * KD.KPC
                    Mhc = Mh[:, None]

                    def eh(rr, Mhc=Mhc):
                        e_ = KD.G * Mhc / rr ** 2
                        return e_ * (Efac(rr / Lm) if (Lm is not None and mode == "bp") else 1.0)
                    nf = nu_flux(KD.G * Mbd, rhd, Dh, eh, Lm, a0, 0.0)
                    sf = KD.partial_slope(np.log10(np.sqrt((2.0 / 9.0) * nf * KD.G * Mbd / rhd) / 1e3), q)[0]
                    row.update(slope_flux=float(sf), sigma_flux=float(abs(cobs - sf) / eobs))
                out[f"{foot}/{cgm}"] = row
        return out

    DWT = {}
    for Lv in (None,) + LSCAN:
        rows = score_dwarfs(A0C, lambda y: nu_chain(y, 0.0), Lv, "chain", mode=("raw" if MUTATE else "bp"), flux=True)
        sg = [v["sigma"] for v in rows.values()]
        DWT["inf" if Lv is None else f"{Lv:g}"] = dict(rows=rows, sigma_range=[min(sg), max(sg)], pass_=max(sg) <= 2.0, below3=max(sg) < 3.0,
                                                        flux_range=([min(v["sigma_flux"] for v in rows.values()), max(v["sigma_flux"] for v in rows.values())]
                                                                    if "sigma_flux" in next(iter(rows.values())) else None))
        r1 = rows["canonical/1.0"]; t = DWT["inf" if Lv is None else f"{Lv:g}"]
        P(f"  L = {'oo' if Lv is None else f'{Lv:4.2f}':>4s} Mpc: statistic C predicted {r1['slope']:+.4f} (x1, canonical) vs observed {r1['obs']:+.4f} +- "
          f"{r1['err']:.4f}; sigma over x1-x2 and footings {t['sigma_range'][0]:.2f}-{t['sigma_range'][1]:.2f}; median host-field fraction kept "
          f"(dwarfs within 0.3 Mpc) {r1['host_frac_median_inner']:.3f}" + (f"; flux form {t['flux_range'][0]:.2f}-{t['flux_range'][1]:.2f}" if t["flux_range"] else "")
          + f" -> {'PASS' if t['pass_'] else 'fail'}")
    for nm, Lf, kn in (("H_Y", L_HY(0.0), lambda y: nu_chain(y, yth_HY(0.0))), ("H_S", L_HS(0.0), lambda y: nu_chain(y, 0.0))):
        rows = score_dwarfs(A0C, kn, Lf, "chain", mode=("raw" if MUTATE else "bp"))
        sg = [v["sigma"] for v in rows.values()]
        DWT[nm] = dict(rows=rows, sigma_range=[min(sg), max(sg)], pass_=max(sg) <= 2.0, below3=max(sg) < 3.0, L=Lf)
        P(f"  {nm} (L = {Lf:.3f} Mpc at z = 0): statistic C sigma {min(sg):.2f}-{max(sg):.2f} -> {'PASS' if max(sg) <= 2.0 else 'fail'}")
    rk = score_dwarfs(A0C, KD.nu, None, "chain"); sgk = [v["sigma"] for v in rk.values()]
    OUT["numbers"]["dwarfs"] = DWT; OUT["numbers"]["dwarfs_kernel_rar_Loo"] = [min(sgk), max(sgk)]
    P(f"  kernel check at L -> oo: nu_RAR at FP0 footings {min(sgk):.2f}-{max(sgk):.2f} vs P2 {DWT['inf']['sigma_range'][0]:.2f}-{DWT['inf']['sigma_range'][1]:.2f}   {el()}")

    # ============================================================================================= PART C Coma UDGs
    banner("PART C -- THE COMA UDGs (L23's pipeline, XR6's rebuild) in the band-passed law")
    UDG, MODELS, BETA, ZCOMA, R500C, kpc23, G23, wmean = (EF[k] for k in ("UDG", "MODELS", "BETA", "ZCOMA", "R500C", "kpc23", "G23", "wmean"))
    nus, Lslope, run_xr6, budget_xr6 = EF["nus"], EF["Lslope"], EF["run"], EF["budget"]
    rho_cL = EF["rho_cL"]
    Mpc23 = kpc23 * 1e3
    # each mass model's own r200 (200 rho_c(z_Coma), the cluster pipeline's definition)
    R200M = {}
    for mname, gfn in MODELS.items():
        Mt = lambda rk: gfn(rk) * (rk * kpc23) ** 2 / G23
        R200M[mname] = brentq(lambda rk: Mt(rk) / (4 / 3 * math.pi * (rk * kpc23) ** 3) - 200 * rho_cL, 200.0, 8000.0)
    P("  mass-model r200 (200 rho_c at z = 0.0231): " + "; ".join(f"{k}: {v:.0f} kpc" for k, v in R200M.items()))
    RGu = np.geomspace(1.0, 60000.0, 1400)                                           # kpc
    UPROF = {}
    for mname, gfn in MODELS.items():
        Mt = np.array([gfn(x_) for x_ in RGu]) * (RGu * kpc23) ** 2 / G23
        for f500 in F500S:
            Mb_ = fb_profile(RGu / R500C, f500) * Mt
            UPROF[(mname, f500, "extended")] = Mb_
            i2 = RGu > R200M[mname]
            Mt2 = float(gfn(R200M[mname])) * (R200M[mname] * kpc23) ** 2 / G23
            UPROF[(mname, f500, "r200")] = np.where(i2, float(fb_profile(np.array(R200M[mname] / R500C), f500)) * Mt2, Mb_)
    UKEYS = list(UPROF); UCOL = np.column_stack([UPROF[k] for k in UKEYS]); lRGu = np.log(RGu)
    _UFB = {}

    def ufbp(L_mpc, mname, f500, ext, rk):
        if L_mpc is None:
            return 1.0
        if L_mpc not in _UFB:
            _UFB[L_mpc] = bp_fraction_many(RGu, UCOL, L_mpc * 1e3)
        return float(np.interp(math.log(rk), lRGu, _UFB[L_mpc][:, UKEYS.index((mname, f500, ext))]))

    def udg_run(a0, mname, rkey, f500, ext, L_mpc, knu, kL, mode="bp", ml_scale=1.0, sig_scale=1.0, dist_scale=1.0, flux=False, yth=0.0):
        """XR6's run(..., 'baryonic'/'given', 'sphere') with the chain's band-pass (L_mpc None -> the record's arm exactly when
        knu is L23's kernel) and an optional flux form."""
        gfn = MODELS[mname]; oi, oe, er, xs = [], [], [], []
        Lk = None if L_mpc is None else L_mpc * 1e3
        for i, u in enumerate(UDG):
            r = u[rkey]
            gobs = u["gobs"] * sig_scale ** 2 / dist_scale; gbar = u["gbar"] * ml_scale
            xobs = gfn(r) / a0
            fbp = 1.0 if (L_mpc is None or mode != "bp") else ufbp(L_mpc, mname, f500, ext, r)
            if ext == "r200" and r > R200M[mname]:
                xobs = xobs * (float(np.interp(math.log(r), lRGu, UPROF[(mname, f500, "r200")])) /
                               float(np.interp(math.log(r), lRGu, UPROF[(mname, f500, "extended")])))
            ya = float(fb_profile(np.array(r / R500C), f500)) * xobs
            if fbp != 1.0:
                ya = ya * fbp
            fint = 1.0 if Lk is None else float(Efac(u["r12"] / kpc23 / Lk))
            if flux:
                eprof = G23 * UPROF[(mname, f500, ext)] * (1.0 if (L_mpc is None or mode != "bp") else _UFB[L_mpc][:, UKEYS.index((mname, f500, ext))]) / (RGu * kpc23) ** 2
                eh = lambda rr, ep=eprof: np.interp(np.log(rr / kpc23), lRGu, ep)
                cpl = float(nu_flux(np.array([G23 * u["Mst"] / 2.0 * ml_scale]), np.array([u["r12"]]), np.array([r * kpc23]), eh,
                                    None if Lk is None else Lk * kpc23, a0, yth)[0])
            else:
                yi = gbar / a0 if fint == 1.0 else gbar / a0 * fint
                ytot = yi + ya; fext = ya / ytot
                cpl = knu(ytot) * (1 + fext * kL(ytot) / 3)
                if fint != 1.0:
                    cpl = 1.0 + (cpl - 1.0) * fint
            oi.append(math.log10(gobs) - math.log10(knu(gbar / a0) * gbar))
            oe.append(math.log10(gobs) - math.log10(cpl * gbar))
            er.append(u["err"]); xs.append(ya)
        mi_, si_ = wmean(oi, er); me_, se_ = wmean(oe, er)
        return dict(mi=mi_, si=si_, me=me_, se=se_, oi=np.array(oi), oe=np.array(oe), err=np.array(er), ya=np.array(xs))

    def udg_budget(A0set, arm, knu, extra=None):
        """XR6's budget (L23's entries, every EFE-dependent entry recomputed on the arm), with the kernel in the estimator entry."""
        a0c_ = A0set["canonical"]
        base = arm(a0c_, BETA, "dmean")["me"]
        S = {}
        S["stellar M/L and IMF"] = abs(arm(a0c_, BETA, "dmean", ml_scale=1.41)["me"] - base)
        rr_ = [2 * math.log10(math.sqrt(knu(u["gbar"] / a0c_) * u["gbar"] * u["r12"] / 3.0) / (((4 / 81.) * G23 * u["Mst"] * a0c_) ** 0.25)) for u in UDG]
        S["sigma -> acceleration estimator"] = float(np.std(rr_) + abs(np.mean(rr_)))
        S["aperture + orbital anisotropy"] = 0.12
        sig_inst = 2.99792458e5 / (4800 * 2.3548)
        prop = [(sig_inst / u["sig"]) ** 2 * 0.05 for u in UDG if u["name"] not in ("DF44", "DFX1")]
        S["instrumental (9 of 11)"] = float(2 * np.median(prop) / math.log(10)) * (9 / 11.)
        spread = [arm(a0c_, m_, k_)["me"] for m_ in MODELS for k_ in ("dproj", "dmean")]
        S["Coma mass model + 3-D position"] = float((max(spread) - min(spread)) / 2)
        S["distance to Coma (+-5%)"] = abs(arm(a0c_, BETA, "dmean", dist_scale=1.05)["me"] - base)
        S["a0 footing"] = abs(arm(A0set["alt"], BETA, "dmean")["me"] - base)
        if extra: S.update(extra)
        return S, math.sqrt(sum(v_ ** 2 for v_ in S.values()))

    def udg_cell(A0set, L_mpc, knu, kL, ext="extended", mode="bp", flux=False, yth=0.0):
        """the central arm (beta-model, Einasto 3-D) at f_b 0.13 with its floor recomputed (f_b template spread added, as XR6)."""
        arm = lambda a0, m_, k_, f500=0.13, **kw: udg_run(a0, m_, k_, f500, ext, L_mpc, knu, kL, mode=mode, flux=flux, yth=yth, **kw)
        cand = {f"{f}/{f5}": arm(A0set[f], BETA, "dmean", f500=f5) for f in FOOTS for f5 in F500S}
        fbs = (max(cand[f"canonical/{f5}"]["me"] for f5 in F500S) - min(cand[f"canonical/{f5}"]["me"] for f5 in F500S)) / 2
        S, floor = udg_budget(A0set, arm, knu, extra={"f_b(R500) template 0.10-0.157 (new)": fbs})
        sig = {f: cand[f"{f}/0.13"]["me"] / math.sqrt(cand[f"{f}/0.13"]["se"] ** 2 + floor ** 2) for f in FOOTS}
        allf = [cand[k]["me"] / math.sqrt(cand[k]["se"] ** 2 + floor ** 2) for k in cand]
        fbu = [ufbp(L_mpc, BETA, 0.13, ext, u["dmean"]) for u in UDG] if (L_mpc is not None and mode == "bp") else [1.0] * len(UDG)
        return dict(me={k: v["me"] for k, v in cand.items()}, mi={k: v["mi"] for k, v in cand.items()}, floor=floor, budget=S, sigma=sig,
                    sigma_range=[min(allf), max(allf)], fbp_udg=[min(fbu), max(fbu)])

    # C3 control: L -> oo with L23's kernel reproduces XR6's candidate (= M*'s XR9 rows)
    ctl = udg_cell(A0U, None, nus, Lslope)
    refU = XR6J["udg"]["candidate"]
    dC3 = max(max(abs(ctl["me"][k] - v) for k, v in refU["me"].items()), abs(ctl["floor"] - refU["floor"]),
              abs(ctl["sigma"]["canonical"] - refU["sigma"][0]), abs(ctl["sigma"]["alt"] - refU["sigma"][1]),
              abs(ctl["sigma_range"][0] - refU["sigma_range"][0]), abs(ctl["sigma_range"][1] - refU["sigma_range"][1]))
    # and XR6's own run() equals this lane's udg_run on the 'baryonic' arm
    dRun = max(abs(run_xr6(A0U[f], MODELS[BETA], "dmean", "baryonic", "sphere", f500=f5)["me"]
                   - udg_run(A0U[f], BETA, "dmean", f5, "extended", None, nus, Lslope)["me"]) for f in FOOTS for f5 in F500S)
    x9u = XR9J["udg"]["p1_x2.5"]
    check("C3 CONTROL (UDGs): L -> oo with L23's kernel reproduces XR6's committed candidate arm (offsets x 6, floor, two sigmas, the f_b "
          "range) = M*'s XR9 p1_x2.5 UDG rows; XR6's own run() equals this lane's on the baryonic arm",
          f"max |diff| {dC3:.1e}; run() vs this lane {dRun:.1e}; offsets {ctl['me']['canonical/0.13']:+.3f} / {ctl['me']['alt/0.13']:+.3f} dex, "
          f"floor {ctl['floor']:.4f}, {ctl['sigma']['canonical']:.2f} / {ctl['sigma']['alt']:.2f} sigma (M* XR9: {x9u['sigma_range'][0]:.2f}-"
          f"{x9u['sigma_range'][1]:.2f})", dC3 < 1e-9 and dRun < 1e-12)
    OUT["numbers"]["C3"] = dict(max_diff=dC3, run_diff=dRun, control=ctl)
    P(f"    {el()}")

    def Lsl_chain(yth):
        return lambda y: (math.log(float(nu_chain(y * (1 + 1e-5), yth))) - math.log(float(nu_chain(y * (1 - 1e-5), yth)))) / 2e-5

    kP2 = lambda y: float(nu_chain(y, 0.0)); kLP2 = Lsl_chain(0.0)
    UD = {}
    for Lv in (None,) + LSCAN:
        cell = {}
        for ext in EXTS:
            cell[ext] = udg_cell(A0C, Lv, kP2, kLP2, ext=ext, mode=("raw" if MUTATE else "bp"))
        cell["flux_extended"] = udg_cell(A0C, Lv, kP2, kLP2, ext="extended", mode=("raw" if MUTATE else "bp"), flux=True)
        worst = max(max(cell[x]["sigma"].values()) for x in EXTS)
        cell["pass_"] = worst < 2.0; cell["worst_central"] = worst; cell["below3"] = worst < 3.0
        UD["inf" if Lv is None else f"{Lv:g}"] = cell
        ce = cell["extended"]; cr = cell["r200"]
        P(f"  L = {'oo' if Lv is None else f'{Lv:4.2f}':>4s} Mpc: offset (extended) {ce['me']['canonical/0.13']:+.3f} / {ce['me']['alt/0.13']:+.3f} dex, floor "
          f"{ce['floor']:.3f} -> {ce['sigma']['canonical']:.2f} / {ce['sigma']['alt']:.2f} sigma; r200-truncated {cr['me']['canonical/0.13']:+.3f} -> "
          f"{cr['sigma']['canonical']:.2f} / {cr['sigma']['alt']:.2f}; Coma field kept at the UDGs {ce['fbp_udg'][0]:.2f}-{ce['fbp_udg'][1]:.2f}"
          + (f"; flux form {cell['flux_extended']['sigma']['canonical']:.2f} / {cell['flux_extended']['sigma']['alt']:.2f}" if "flux_extended" in cell else "")
          + f" -> {'PASS' if cell['pass_'] else 'fail'}   {el()}")
    for nm, Lf, yt in (("H_Y", L_HY(ZCOMA), yth_HY(ZCOMA)), ("H_S", L_HS(ZCOMA), 0.0)):
        kn = lambda y, yt=yt: float(nu_chain(y, yt)); kl = Lsl_chain(yt)
        cell = {ext: udg_cell(A0C, Lf, kn, kl, ext=ext, mode=("raw" if MUTATE else "bp")) for ext in EXTS}
        worst = max(max(cell[x]["sigma"].values()) for x in EXTS)
        cell["pass_"] = worst < 2.0; cell["worst_central"] = worst; cell["L"] = Lf; cell["below3"] = worst < 3.0
        UD[nm] = cell
        P(f"  {nm} (L = {Lf:.3f} Mpc at z = {ZCOMA}): offset {cell['extended']['me']['canonical/0.13']:+.3f} dex -> {cell['extended']['sigma']['canonical']:.2f} / "
          f"{cell['extended']['sigma']['alt']:.2f} sigma (r200 {cell['r200']['sigma']['canonical']:.2f} / {cell['r200']['sigma']['alt']:.2f}) -> {'PASS' if cell['pass_'] else 'fail'}")
    ck_ = udg_cell(A0C, None, nus, Lslope)
    OUT["numbers"]["udg"] = UD; OUT["numbers"]["udg_kernel_L23_Loo"] = ck_["sigma"]
    P(f"  kernel check at L -> oo: L23's kernel at FP0 footings {ck_['sigma']['canonical']:.2f} / {ck_['sigma']['alt']:.2f} vs P2 "
      f"{UD['inf']['extended']['sigma']['canonical']:.2f} / {UD['inf']['extended']['sigma']['alt']:.2f}")

    # ============================================================================================= K2 the neglected term
    banner("K2  THE REDUCTION'S NEGLECTED TERM: the output filter's smoothed phantom across a satellite (a tidal-order bound)")
    # |grad S_L X| <= |X_host|/L; across r_s the field changes by <= |X_host(D)| r_s/L; compare with the internal field at r_s
    wk = []
    for foot in FOOTS:
        a0 = A0C[foot]
        # dwarfs at L = 0.5 Mpc (the shortest scanned), MW/M31 hosts x2
        gNe, hmw = host_field(2.0, 0.5)
        Xh = a0 * x_P2(gNe / a0); gin = KD.G * Mbd / rhd ** 2 * nu_chain((KD.G * Mbd / rhd ** 2 + gNe) / a0)
        wk.append(("dwarfs", float(np.max(Xh * rhd / (0.5 * MPC) / gin))))
        # cluster members (extended baryons, f_b 0.157)
        e = GEO["R_proj"]["e_in"][(EF["FCOS"], "extended")]
        Xh = a0 * x_P2(e[mi] / a0); gin = gNint[mi] * nu_chain((gNint[mi] + e[mi]) / a0)
        wk.append(("clusters", float(np.max(Xh * RHI[mi] / (0.5 * MPC) / gin))))
        # UDGs
        vals = []
        for u in UDG:
            ya = float(fb_profile(np.array(u["dmean"] / R500C), EF["FCOS"])) * MODELS[BETA](u["dmean"]) / a0
            yi = u["gbar"] / a0
            vals.append(x_P2(ya) * u["r12"] / (0.5 * Mpc23) / (yi * nu_chain(yi + ya)))
        wk.append(("UDGs", float(max(vals))))
    worst = max(v for _, v in wk)
    check("K2 (reported) THE NEGLECTED TERM IS SMALL: the output filter's S_L X varies on the scale L, so across a satellite it changes by "
          "<= |X_host| r_s/L; at the shortest L scanned (0.5 Mpc) that is < 1e-2 of every object's internal field",
          "; ".join(f"{k}: {v:.1e}" for k, v in wk), worst < 1e-2, load_bearing=False)
    OUT["numbers"]["K2"] = wk
    # K2b (POST-HOC, written after K2 failed in the first debug run): K2's bound compares the whole variation of S_L X across the
    # satellite with the internal field, but every statistic here is a sphere-averaged (monopole) quantity, to which only the
    # DIVERGENCE of S_L X contributes (Gauss): div S_L X = S_L div X = the Gaussian-smoothed host phantom density.  Its traceless
    # (tidal) part is smaller than the host's own tidal field by ~D/L, which the record's forms and this lane both neglect.
    # Bound: M_ph,host(< D + 5L)/(2 pi L^2)^(3/2) x (4 pi/3) r_s^3, against the satellite's dynamical mass nu m inside r_s.
    wk2 = []
    for foot in FOOTS:
        a0 = A0C[foot]; Lm = 0.5 * MPC
        # dwarfs (hosts x2, the MW or M31 as the larger field), the host's phantom inside D + 5L
        Mh = np.where(host_field(2.0, None)[1], KD.M_MW_BAR, KD.M_M31_BAR) * 2.0 * KD.MSUN
        Dh = np.where(host_field(2.0, None)[1], np.where(okmw, dmw, 1.0), np.where(ok31, dm31, 1.0)) * KD.KPC
        Rb = Dh + 5 * Lm; yb = KD.G * Mh / Rb ** 2 / a0; Mph = (nu_chain(yb) - 1.0) * Mh
        rho = Mph / (2 * math.pi * Lm ** 2) ** 1.5
        gNe, _ = host_field(2.0, 0.5); gi = KD.G * Mbd / rhd ** 2
        Mdyn = nu_chain((gi + gNe) / a0) * Mbd
        wk2.append(("dwarfs", float(np.max(rho * (4 * math.pi / 3) * rhd ** 3 / Mdyn))))
        # cluster members (extended baryons, f_b 0.157): the cluster's phantom inside r + 5L
        vals = []
        for i in mi:
            c = cls[idx[i]]; r = GEO["R_proj"]["r_m"][i]; Rb = r + 5 * Lm
            Mbr = float(cluster_Mb(c, EF["FCOS"], "extended", np.array([Rb]))[0]); yb = G * Mbr / Rb ** 2 / a0
            rho = (nu_chain(yb) - 1.0) * Mbr / (2 * math.pi * Lm ** 2) ** 1.5
            e = GEO["R_proj"]["e_in"][(EF["FCOS"], "extended")][i]
            vals.append(rho * (4 * math.pi / 3) * RHI[i] ** 3 / (nu_chain((gNint[i] + e) / a0) * Mbg[i]))
        wk2.append(("clusters", float(max(vals))))
        vals = []
        for u in UDG:
            rk = u["dmean"] + 5 * 500.0; Mbr = float(fb_profile(np.array(rk / R500C), EF["FCOS"])) * MODELS[BETA](rk) * (rk * kpc23) ** 2 / G23
            yb = G23 * Mbr / (rk * kpc23) ** 2 / a0; rho = (nu_chain(yb) - 1.0) * Mbr / (2 * math.pi * (500.0 * kpc23) ** 2) ** 1.5
            ya = float(fb_profile(np.array(u["dmean"] / R500C), EF["FCOS"])) * MODELS[BETA](u["dmean"]) / a0; yi = u["gbar"] / a0
            vals.append(rho * (4 * math.pi / 3) * u["r12"] ** 3 / (nu_chain(yi + ya) * u["Mst"] / 2.0))       # u["Mst"] is in kg (XR6)
        wk2.append(("UDGs", float(max(vals))))
    worst2 = max(v for _, v in wk2)
    check("K2b (reported, POST-HOC: written after K2 failed in the first debug run) THE NEGLECTED TERM'S MONOPOLE: the Gaussian-smoothed "
          "host phantom mass inside the kinematic radius (an upper bound) is < 1e-2 of the object's dynamical mass at L = 0.5 Mpc, for every "
          "scored object; the traceless part is below the host's own (neglected) tidal field by ~D/L",
          "; ".join(f"{k}: {v:.1e}" for k, v in wk2), worst2 < 1e-2, load_bearing=False)
    OUT["numbers"]["K2b"] = wk2
    # K2c (POST-HOC, written after K2b failed in the second debug run; K2b's bound puts the host's WHOLE phantom mass into one
    # Gaussian ball).  The quantity itself: the host's phantom density AT the satellite, unsmoothed (plain QUMOND's background, which
    # the record's forms -- and this lane's -- neglect for M* and the chain alike) and Gaussian-smoothed over L (the part the chain's
    # output filter removes from that background), each as a fraction of the object's dynamical mass inside its kinematic radius.
    def bg_fracs(r_grid, Mb_grid, D, r_s, Mdyn, a0, L_len):
        y = G * Mb_grid / r_grid ** 2 / a0; Mph = (nu_chain(y) - 1.0) * Mb_grid
        rho = np.gradient(Mph, r_grid) / (4 * math.pi * r_grid ** 2)
        Ms = Mph * (1.0 - bp_fraction(r_grid, Mph, L_len))
        rhos = np.gradient(Ms, r_grid) / (4 * math.pi * r_grid ** 2)
        lr = np.log(r_grid)
        rD = float(np.interp(math.log(D), lr, rho)); sD = float(np.interp(math.log(D), lr, rhos))
        v = (4 * math.pi / 3) * r_s ** 3 / Mdyn
        return rD * v, sD * v
    wk3 = {}
    a0 = A0C["canonical"]
    for Lv in (0.5, L_HY(0.0), L_HS(0.0)):
        # cluster members (extended baryons, f_b 0.157; R_proj)
        fb_, fs_ = [], []
        for i in mi:
            k = PROF_KEYS.index((int(idx[i]), EF["FCOS"], "extended")); col = MCOL[:, k]
            e = GEO["R_proj"]["e_in"][(EF["FCOS"], "extended")][i]
            b, sm = bg_fracs(RGc, col, GEO["R_proj"]["r_m"][i], RHI[i], nu_chain((gNint[i] + e) / a0) * Mbg[i], a0, Lv * MPC)
            fb_.append(b); fs_.append(sm)
        # dwarfs (the larger-field host as a point mass, x1)
        db_, ds_ = [], []
        gNe1, hmw1 = host_field(1.0, None)
        rgd = np.geomspace(1e-3, 60.0, 1400) * MPC
        for j in range(len(d)):
            Mh = (KD.M_MW_BAR if hmw1[j] else KD.M_M31_BAR) * KD.MSUN
            Dj = (dmw[j] if hmw1[j] else dm31[j]) * KD.KPC
            if not np.isfinite(Dj) or Dj <= 0: continue
            b, sm = bg_fracs(rgd, np.full_like(rgd, Mh), Dj, rhd[j], nu_chain((KD.G * Mbd[j] / rhd[j] ** 2 + gNe1[j]) / a0) * Mbd[j], a0, Lv * MPC)
            db_.append(b); ds_.append(sm)
        # Coma UDGs (beta-model, f_b 0.157, Einasto 3-D)
        ub_, us_ = [], []
        Mt = np.array([MODELS[BETA](x_) for x_ in RGu]) * (RGu * kpc23) ** 2 / G23; Mbu = fb_profile(RGu / R500C, EF["FCOS"]) * Mt
        for u in UDG:
            ya = float(fb_profile(np.array(u["dmean"] / R500C), EF["FCOS"])) * MODELS[BETA](u["dmean"]) / a0; yi = u["gbar"] / a0
            b, sm = bg_fracs(RGu * kpc23, Mbu, u["dmean"] * kpc23, u["r12"], nu_chain(yi + ya) * u["Mst"] / 2.0, a0, Lv * 1e3 * kpc23)
            ub_.append(b); us_.append(sm)
        wk3[f"{Lv:.3f}"] = {nm: dict(background_median=float(np.median(b_)), background_max=float(np.max(b_)),
                                     smoothed_median=float(np.median(s_)), smoothed_max=float(np.max(s_)))
                            for nm, b_, s_ in (("clusters", fb_, fs_), ("dwarfs", db_, ds_), ("UDGs", ub_, us_))}
    w05 = wk3["0.500"]
    check("K2c (reported, POST-HOC: written after K2b failed in the second debug run) THE BACKGROUND THE FORMS NEGLECT: the host's phantom "
          "density at the object (plain QUMOND's tidal-monopole background, dropped by the record's forms for M* and by this lane for the chain) "
          "and its Gaussian-smoothed part (what the chain's output filter removes), as fractions of the dynamical mass inside the kinematic "
          "radius; pass if the smoothed part (the chain-specific term) is < 0.1 for the median object of every sample at every L shown",
          "; ".join(f"L = {Lk} Mpc: " + ", ".join(f"{nm} background {v['background_median']:.1e} (max {v['background_max']:.1e}), smoothed "
                                                     f"{v['smoothed_median']:.1e} (max {v['smoothed_max']:.1e})" for nm, v in wv.items()) for Lk, wv in wk3.items()),
          all(v["smoothed_median"] < 0.1 for wv in wk3.values() for v in wv.values()), load_bearing=False)
    OUT["numbers"]["K2c"] = wk3

    # ============================================================================================= flips and hypotheses
    banner("S  THE FLIPS AGAINST M* AND THE PRE-DECLARED HYPOTHESES")
    keysL = [f"{v:g}" for v in LSCAN]
    passL = {"clusters": [float(k) for k in keysL if CL[k]["summary"]["pass_"]],
             "dwarfs": [float(k) for k in keysL if DWT[k]["pass_"]],
             "udg": [float(k) for k in keysL if UD[k]["pass_"]]}
    below3 = {"clusters": [float(k) for k in keysL if CL[k]["summary"]["below3"]],
              "dwarfs": [float(k) for k in keysL if DWT[k]["below3"]],
              "udg": [float(k) for k in keysL if UD[k]["below3"]]}
    passL["clusters_scalar"] = [float(k) for k in keysL if CL[k]["summary"]["pass_scalar"]]
    passL["clusters_subtract"] = [float(k) for k in keysL if CL[k]["summary"]["pass_subtract"]]
    passL["clusters_flux"] = [float(k) for k in keysL if CL[k]["summary"].get("pass_flux")]
    passL["clusters_zero_point"] = [float(k) for k in keysL if CL[k]["summary"]["zp_pass"]]
    passL["udg_flux"] = [float(k) for k in keysL if "flux_extended" in UD[k] and max(UD[k]["flux_extended"]["sigma"].values()) < 2.0]
    OUT["numbers"]["pass_L"] = passL; OUT["numbers"]["below3_L"] = below3
    for s_ in ("clusters", "dwarfs", "udg"):
        v = passL[s_]
        P(f"    {s_:8s}: passes (XR9's 2-sigma gate) at L = {v if v else 'none of the scanned values'}; below 3 sigma at L = {below3[s_] if below3[s_] else 'none'}")
    for s_ in ("clusters_scalar", "clusters_subtract", "clusters_flux", "clusters_zero_point", "udg_flux"):
        P(f"    {s_:20s}: every variant <= 2 sigma at L = {passL[s_] if passL[s_] else 'none of the scanned values'}")
    P(f"    H_Y cell: clusters {'PASS' if CL['H_Y']['summary']['pass_'] else 'fail'} ({CL['H_Y']['summary']['sigma_range'][0]:.2f}-{CL['H_Y']['summary']['sigma_range'][1]:.2f}), "
      f"dwarfs {'PASS' if DWT['H_Y']['pass_'] else 'fail'} ({DWT['H_Y']['sigma_range'][0]:.2f}-{DWT['H_Y']['sigma_range'][1]:.2f}), UDGs "
      f"{'PASS' if UD['H_Y']['pass_'] else 'fail'} (worst central {UD['H_Y']['worst_central']:.2f})")
    P(f"    H_S cell: clusters {'PASS' if CL['H_S']['summary']['pass_'] else 'fail'} ({CL['H_S']['summary']['sigma_range'][0]:.2f}-{CL['H_S']['summary']['sigma_range'][1]:.2f}), "
      f"dwarfs {'PASS' if DWT['H_S']['pass_'] else 'fail'} ({DWT['H_S']['sigma_range'][0]:.2f}-{DWT['H_S']['sigma_range'][1]:.2f}), UDGs "
      f"{'PASS' if UD['H_S']['pass_'] else 'fail'} (worst central {UD['H_S']['worst_central']:.2f})")
    h1 = all(DWT[k]["sigma_range"][0] >= 3.0 for k in keysL)
    check("H1 (reported, pre-declared) THE LV DWARFS DO NOT FLIP: statistic C >= 3 sigma at every scanned L, both footings",
          f"min sigma over the scan {min(DWT[k]['sigma_range'][0] for k in keysL):.2f}", h1, load_bearing=False)
    Lc = passL["clusters"]
    h2 = (len(Lc) > 0 and max(Lc) <= 1.0) and (not CL["H_Y"]["summary"]["pass_"]) and (not CL["H_S"]["summary"]["pass_"])
    check("H2 (reported, pre-declared) THE CLUSTER SLOPE FLIPS ONLY AT SHORT L: every variant <= 2 sigma only for L <~ 1 Mpc, and both "
          "separators' cells still fail", f"passing L {Lc if Lc else 'none'}; H_Y worst {CL['H_Y']['summary']['sigma_range'][1]:.2f}, H_S worst "
          f"{CL['H_S']['summary']['sigma_range'][1]:.2f}", h2, load_bearing=False)
    check("H3 (reported, pre-declared) THE COMA UDGs DO NOT FLIP at any scanned L >= 0.5 Mpc (central arm < 2 sigma on both footings, both extents)",
          f"passing L {passL['udg'] if passL['udg'] else 'none'}; best worst-central sigma {min(UD[k]['worst_central'] for k in keysL):.2f} at L = "
          f"{keysL[int(np.argmin([UD[k]['worst_central'] for k in keysL]))]} Mpc", len(passL["udg"]) == 0, load_bearing=False)
    dk = [abs(CL["inf"]["summary"]["sigma_range"][1] - OUT["numbers"]["clusters_kernel_mono_Loo"]["sigma_range"][1]),
          abs(DWT["inf"]["sigma_range"][1] - max(OUT["numbers"]["dwarfs_kernel_rar_Loo"])),
          abs(UD["inf"]["extended"]["sigma"]["canonical"] - ck_["sigma"]["canonical"])]
    check("H4 (reported, pre-declared) THE KERNEL: at L -> oo, P2 moves each sample's worst sigma by < 0.5 sigma from the record's kernel",
          f"clusters {dk[0]:.2f}, dwarfs {dk[1]:.2f}, UDGs (canonical central) {dk[2]:.2f}", max(dk) < 0.5, load_bearing=False)

    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    OUT["L_scan"] = list(LSCAN); OUT["L_HY_z0"] = L_HY(0.0); OUT["L_HS_z0"] = L_HS(0.0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   {el()}")
    sys.exit(1 if nlb else 0)
