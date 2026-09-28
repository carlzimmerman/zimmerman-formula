#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG24 -- THE COLD BUDGET WITH TURNED-AROUND ASSOCIATIONS AS THE TOP-LEVEL SYSTEMS (FG001 applied at T3's own level).

WHY.  CFG23's diagnostics (V4): against KiDS's own best edge (x_e ~ 0.62, CFG21), the cold budget's edge (CFG17: 0.348 canonical
P2) costs 40.9-62.0 in chi^2 (6.4-7.9 sigma).  The budget's FG001 grouping (CFG11) used Kourkchi & Tully 2017's groups, whose
members lie inside the group's SECOND-turnaround radius.  But T3 switches the law ON inside top-level systems that have TURNED
AROUND (Delta >= Delta_ta), and FG001 gives the phantom to the outermost such system -- so the owning system is the turned-around
association, one level above KT2017's groups (CFG12's standing named this the untested next step).  The phantom is sublinear in
the baryons (~M_b^3/4), so owning at the association level can only lower the phantom sum.

THE ASSOCIATIONS (no new constant).  In CFG11's volume-limited D <= 15 Mpc sample (the one CFG17 uses), KT2017's groups -- their
sample members' baryons summed with CFG17's xGASS gas -- are linked friends-of-friends in redshift space: two systems join when
        s_proj^2 + (dV / 75 km/s/Mpc)^2  <  r_link(M_1 + M_2)^2 ,
s_proj their projected separation at the pair's mean distance (the catalogue's V/75 convention, CFG11), dV their heliocentric
velocity difference, and r_link the self-consistent turnaround radius of the combined system at the edge being tested: the law's
profile cut at x r_ta (CFG4's density edge, enclosed mass constant beyond), where its mean density falls to Delta_ta(0) rho_m
(CFG16's r_bound convention, at z = 0).  Merged systems take the baryon-weighted mean direction and velocity; linking repeats until
nothing joins.  Redshift space compresses infalling pairs, so every turned-around pair inside r_link in projection is linked; a
Hubble-flow pair at a true separation < r_link that has not turned around may be linked too, and the law's turnaround radius is
itself larger than the LG's observed zero-velocity radius (CFG20).  Both make the linking GENEROUS to the budget: a closure here
is robust, an opening is not.

THE BUDGET is CFG17's exact machinery (exec'd read-only): the GAMA SMF with xGASS gas (non-detections at their limits), CFG12's
share at the budget's own scale, the FG001 reduction applied only above the sample's mass limit -- with CFG11's grouping ratio
replaced by the associations' R(x), recomputed at every x (the linking depends on x).  THE KiDS COST is CFG23_diagnostics' V4:
KiDS's chi^2 at the new edge (CFG16's self-consistent caps) against KiDS's own best (CFG21).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG17's committed edge_A (four rows) reproduced exactly by the exec'd machinery; with the linking switched off, this
      lane's R equals CFG17's R (x = 0.31, 0.40) to 1e-12 and its edge function reproduces edge_A to 1e-12; the tabulated linking
      radius matches the direct computation to 1e-4.
  C2  CONTROL  the finder conserves the sample: every KT2017 group lies in exactly one association, and the associations' baryons
      sum to the sample's.
  H0  [MUTATE must fail] association ownership lowers the phantom sum below the group level at x = 0.35 (canonical P2).
  H1  [HEADLINE] with turned-around associations, the canonical budget edge moves far enough that KiDS's cost against its own best
      is <= 9, both kernels.  Declared EXPECTATION: FAIL (it needs R ~ 0.6 against the groups' 0.89).
  R1  (reported) R(x) for groups and associations; the association statistics; all four rows' edges and KiDS costs; the most
      generous variant (linking at the law's untruncated r_ta); the largest association removed.
MUTATE=1: the linking is switched off (associations = KT2017 groups) -- H0 must FAIL (rc = 1).

REVISION (after the first -- MUTATE -- run, before any main run; disclosed).  That run showed that the D <= 15 Mpc sample (CFG11's,
inherited by CFG12 and CFG17) contains the Milky Way's own group (KT2017 group 5064336: the MW, the LMC, the SMC, Sgr dSph) at a
V/75 distance of 0.12 Mpc, where the MW's integrated K magnitude seen from inside (Ks = -8.4) becomes L_K = 7e12 Lsun and M_b =
4.4e12 Msun -- 47% of the sample's baryons.  The V/75 convention fails inside the Local Group.  The OPERATIVE sample drops galaxies
whose group V/75 distance is < 1 Mpc (exactly those 4 members).  On the committed group-level budget this is an erratum for
CFG11/12/17: R(0.31) 0.889 -> 0.870 and the canonical P2 edge 0.3483 -> 0.3542 (alt 0.2998 -> 0.3049) -- small.  In the association
finder the bogus entry would link every system within a few hundred km/s of the MW's velocity into one spurious association, so
H0 and H1 are scored on the operative sample; the first-written versions (CFG11's sample) are still computed, reported, and marked
as contaminated.  C1 still reproduces CFG17 on CFG11's sample.  Added (reported): the group-level edge and KiDS cost on the
operative sample (the erratum's size), and a 2-Mpc cut.
Run: python3 campaign_fresh_gravity/CFG24_budget_associations.py   (MUTATE=1 for the control; ~2-4 min)
"""
import os, sys, math, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG24_budget_associations", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the linking switched off -- H0 must FAIL ***")
np.seterr(all="ignore")
t0 = time.time()


class _Q:
    def banner(self, *a, **k):
        pass

    def num(self, *a, **k):
        pass


C17J = json.load(open(os.path.join(HERE, "CFG17_budget_xgass_results.json")))["numbers"]["RES"]
C21 = json.load(open(os.path.join(HERE, "CFG21_kids_lg_joint_results.json")))["numbers"]["RES"]

# ================================================================================================ CFG17's budget machinery (exec'd read-only)
C17P = os.path.join(HERE, "CFG17_budget_xgass.py")
s17 = open(C17P).read()
g17 = {"__file__": C17P, "__name__": "cfg17_slices", "np": np, "math": math, "os": os, "json": json, "sys": sys, "C7": C7, "C": C,
       "HERE": HERE, "MUTATE": False, "P": lambda *a, **k: None, "check": lambda *a, **k: None, "R": _Q(), "_Q": _Q}
a_ = s17.index("C11P = os.path.join(")
b_ = s17.index('R.banner("C1  CONTROL: SPARC')
exec(compile("\n" * s17[:a_].count("\n") + s17[a_:b_], C17P, "exec"), g17)
ns = g17["ns"]                                                                         # CFG11's namespace, as CFG17 holds it
KERN, A0, OC0, C12, XS, MLIM, UPSK, m15 = (g17[k] for k in ("KERN", "A0", "OC0", "C12", "XS", "MLIM", "UPSK", "m15"))
omega_x, edge17, R_at17 = g17["omega_x"], g17["edge"], g17["R_at"]
BARY_A = g17["xgass_baryons_factory"](g17["GAS_A"])
GID0 = ns["gid"].copy()
RHOM0 = ns["OM0"] * ns["RHOC0"]                                                        # kg/m^3, z = 0
DTA0 = ns["DTA"][0.0]
MPC = C.MPC

# the sample's galaxies: directions, velocities, baryons (CFG17's xGASS baryons, exactly as its R_at sets them)
ig = ns["ig"]
RA = np.array([ns["fnum"](r_[ig["RAJ2000"]]) for r_ in ns["rg_"]])
DE = np.array([ns["fnum"](r_[ig["DEJ2000"]]) for r_ in ns["rg_"]])
DV_ALL = ns["MODE"]["V/75"]


def sample_arrays(mask):
    """a sample's baryons (CFG17's xGASS baryons, exactly as its R_at sets them), velocities, directions and KT2017 groups."""
    ns["baryons"] = BARY_A
    return dict(MB=BARY_A(ns["lum"](DV_ALL)[mask], UPSK)[0], V=ns["HRV"][mask], G=GID0[mask],
                VEC=np.stack([np.cos(np.radians(DE[mask])) * np.cos(np.radians(RA[mask])),
                              np.cos(np.radians(DE[mask])) * np.sin(np.radians(RA[mask])), np.sin(np.radians(DE[mask]))], 1))


S_FW = sample_arrays(m15)                                                              # CFG11's sample (first-written)
M_OP = m15 & (DV_ALL >= 1.0)
S_OP = sample_arrays(M_OP)                                                             # operative: the MW's own group dropped
S_2 = sample_arrays(m15 & (DV_ALL >= 2.0))                                             # reported: a 2-Mpc cut
for lab_, S_ in (("CFG11's D <= 15 sample", S_FW), ("operative (group V/75 >= 1 Mpc)", S_OP)):
    ug_, inv_ = np.unique(S_["G"], return_inverse=True); Mg_ = np.bincount(inv_, weights=S_["MB"])
    P(f"\n    {lab_}: {len(S_['MB'])} galaxies in {len(ug_)} KT2017 groups; baryons {S_['MB'].sum():.3e} Msun; largest group "
      f"{ug_[np.argmax(Mg_)]} with {Mg_.max():.2e} ({Mg_.max() / S_['MB'].sum():.2f}); finite: "
      f"{bool(np.all(np.isfinite(S_['VEC'])) and np.all(np.isfinite(S_['V'])))}")
P(f"    log M_* limit {MLIM:.2f}")


# ================================================================================================ the linking radius
def rta_sc_direct(Mb_msun, kfun, a0, x, mode="sc"):
    """[Mpc] the turnaround radius of the law's profile cut at x r_ta (mode 'sc'), or the law's own r_ta (mode 'law'), z = 0."""
    Mb = np.atleast_1d(np.asarray(Mb_msun, float)) * C.MSUN
    rl = ns["rta_of"](Mb, kfun, a0, 0.0)
    if mode == "law":
        return rl / MPC
    re = x * rl
    Me = Mb * kfun(C.G_SI * Mb / re ** 2 / a0)
    rsc = (Me / (4 / 3 * math.pi * DTA0 * RHOM0)) ** (1 / 3)
    return np.where(rsc > re, rsc, rl) / MPC


LMT = np.linspace(7.0, 15.5, 341)
_RT = {}


def r_link(M_msun, kfun, a0, x, mode):
    key = (id(kfun), a0, x, mode)
    if key not in _RT:
        _RT[key] = np.log(rta_sc_direct(10 ** LMT, kfun, a0, x, mode))
    return np.exp(np.interp(np.log10(M_msun), LMT, _RT[key]))


# ================================================================================================ the association finder
def associate(S, kfun, a0, x, link=True, mode="sc"):
    """KT2017 groups (sample members only) linked in redshift space at r_link(M1 + M2); returns the association label per galaxy."""
    MB_GAL, V_GAL, VEC_GAL = S["MB"], S["V"], S["VEC"]
    ug, g_of = np.unique(S["G"], return_inverse=True)
    lab = np.arange(len(ug))                                                            # group -> association
    if not link:
        return lab[g_of]
    while True:
        ua, a_of = np.unique(lab[g_of], return_inverse=True)
        M = np.bincount(a_of, weights=MB_GAL)
        V = np.bincount(a_of, weights=MB_GAL * V_GAL) / M
        X = np.stack([np.bincount(a_of, weights=MB_GAL * VEC_GAL[:, k]) for k in range(3)], 1)
        X /= np.linalg.norm(X, axis=1)[:, None]
        n = len(M)
        iu, ju = np.triu_indices(n, 1)
        ang = np.arccos(np.clip(np.sum(X[iu] * X[ju], 1), -1.0, 1.0))
        Dp = 0.5 * (V[iu] + V[ju]) / 75.0
        s2 = (Dp * ang) ** 2 + ((V[iu] - V[ju]) / 75.0) ** 2
        ok = s2 < r_link(M[iu] + M[ju], kfun, a0, x, mode) ** 2
        if not ok.any():
            break
        par = np.arange(n)

        def find(i):
            while par[i] != i:
                par[i] = par[par[i]]
                i = par[i]
            return i
        for i, j in zip(iu[ok], ju[ok]):
            ri, rj = find(i), find(j)
            if ri != rj:
                par[max(ri, rj)] = min(ri, rj)
        root = np.array([find(i) for i in range(n)])
        lab = root[np.searchsorted(ua, lab)]
    return lab[g_of]


def R_of(S, labels, kfun, a0, x):
    """the phantom sum over associations / over galaxies (CFG11's ratio's arithmetic, CFG4's per-system phantom)."""
    MB_GAL = S["MB"]
    ua, inv = np.unique(labels, return_inverse=True)
    Mg = np.bincount(inv, weights=MB_GAL) * C.MSUN
    Mb = MB_GAL * C.MSUN
    rt_g, rt_G = ns["rta_of"](Mb, kfun, a0, 0.0), ns["rta_of"](Mg, kfun, a0, 0.0)
    mph = lambda M_, rt: M_ * (kfun(C.G_SI * M_ / (x * rt) ** 2 / a0) - 1.0) / C.MSUN
    return float(np.sum(mph(Mg, rt_G)) / np.sum(mph(Mb, rt_g)))


def edge_with(f, kn, Rfun):
    """CFG17's edge condition with any R(x); the first crossing of the limit (om need not be monotone once R depends on x)."""
    lim = OC0 * C12["D1"][f"{f}|{kn}"]["f_ta"]
    om = np.array([omega_x(f, kn, float(x), 7.0, "A") - (1.0 - Rfun(float(x))) * omega_x(f, kn, float(x), MLIM, "A") for x in XS])
    above = np.where(om > lim)[0]
    if len(above) == 0:
        return float(XS[-1])
    j = int(above[0])
    if j == 0:
        return 0.0
    return float(XS[j - 1] + (lim - om[j - 1]) * (XS[j] - XS[j - 1]) / (om[j] - om[j - 1]))


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG17 reproduced; the lane's R and edge with the linking off; the tabulated linking radius")
dev_e17, dev_r, dev_e = 0.0, 0.0, 0.0
for f in C.FOOTS:
    for kn in KERN:
        e17, r31, r40 = edge17(f, kn, "A")
        dev_e17 = max(dev_e17, abs(e17 - C17J[f"{f}|{kn}"]["edge_A"]))
        ns["baryons"] = BARY_A
        lab0 = associate(S_FW, KERN[kn], A0[f], 0.31, link=False)
        q31, q40 = R_of(S_FW, lab0, KERN[kn], A0[f], 0.31), R_of(S_FW, lab0, KERN[kn], A0[f], 0.40)
        dev_r = max(dev_r, abs(q31 - r31), abs(q40 - r40))
        e_mine = edge_with(f, kn, lambda x, _a=q31, _b=q40: float(np.interp(x, [0.31, 0.40], [_a, _b])))
        dev_e = max(dev_e, abs(e_mine - e17))
ns["baryons"] = BARY_A
dlink = 0.0
for kn in KERN:
    for mode in ("sc", "law"):
        for Mt in (3.3e8, 7.7e10, 2.2e12, 5.5e13):
            d_ = float(rta_sc_direct(Mt, KERN[kn], A0["canonical"], 0.43, mode)[0])
            dlink = max(dlink, abs(float(r_link(np.array([Mt]), KERN[kn], A0["canonical"], 0.43, mode)[0]) / d_ - 1))
c1 = dev_e17 <= 1e-12 and dev_r <= 1e-12 and dev_e <= 1e-12 and dlink <= 1e-4
check("C1 CONTROL: CFG17's edge_A reproduced; with the linking off the lane's R equals CFG17's and its edge function reproduces "
      "edge_A; the tabulated linking radius matches the direct one",
      f"|d edge_A| {dev_e17:.1e}; |d R| {dev_r:.1e}; |d edge| {dev_e:.1e}; link table {dlink:.1e}", c1)

# ================================================================================================ the associations and R(x)
R.banner("THE ASSOCIATIONS: R(x) at the turned-around level")
XR = np.round(np.arange(0.25, 0.8001, 0.025), 3)
CURVES, STAT = {}, {}
cons = True


def curves(S, f, kn, tag, stats=False):
    """R(x) on XR for the groups, the associations (r_link at the tested edge) and the generous variant (the law's r_ta)."""
    global cons
    kf, a0 = KERN[kn], A0[f]
    lab0 = associate(S, kf, a0, 0.3, link=False)
    rg, ra, rl = [], [], []
    for x in XR:
        lab = associate(S, kf, a0, float(x), link=not MUTATE, mode="sc")
        labL = associate(S, kf, a0, float(x), link=not MUTATE, mode="law")
        ua, inv = np.unique(lab, return_inverse=True)
        Ma = np.bincount(inv, weights=S["MB"])
        for g_ in np.unique(S["G"]):
            if len(np.unique(lab[S["G"] == g_])) != 1:
                cons = False
        cons &= abs(Ma.sum() / S["MB"].sum() - 1) < 1e-12
        rg.append(R_of(S, lab0, kf, a0, float(x))); ra.append(R_of(S, lab, kf, a0, float(x))); rl.append(R_of(S, labL, kf, a0, float(x)))
        if stats and (abs(x - 0.35) < 1e-9 or abs(x - 0.625) < 1e-9):
            ng = np.bincount(inv, weights=np.ones_like(S["MB"]))
            gpa = np.array([len(np.unique(S["G"][inv == k])) for k in range(len(ua))])
            big = int(np.argmax(Ma))
            # the largest association removed (reported): its galaxies dropped from both sums
            keep = inv != big
            Sk = dict(MB=S["MB"][keep], V=S["V"][keep], G=S["G"][keep], VEC=S["VEC"][keep])
            r_nobig = R_of(Sk, lab[keep], kf, a0, float(x))
            STAT[(tag, f, kn, float(x))] = dict(n_assoc=int(len(ua)), n_groups=int(len(np.unique(S["G"]))), multi=int(np.sum(gpa > 1)),
                                                frac_baryons_multi=float(Ma[gpa > 1].sum() / Ma.sum()), largest_Mb=float(Ma[big]),
                                                largest_ngal=int(ng[big]), largest_ngroups=int(gpa[big]),
                                                largest_frac=float(Ma[big] / Ma.sum()), R_without_largest=r_nobig)
    CURVES[(tag, f, kn)] = dict(groups=np.array(rg), associations=np.array(ra), generous=np.array(rl))


for f in C.FOOTS:
    for kn in KERN:
        curves(S_OP, f, kn, "op", stats=True)
        v = CURVES[("op", f, kn)]
        P(f"    {f:9s} {kn:8s} [operative]: R_groups(0.35) {np.interp(0.35, XR, v['groups']):.4f}; R_assoc x = 0.30 / 0.35 / 0.45 / "
          f"0.625: " + " / ".join(f"{np.interp(q, XR, v['associations']):.4f}" for q in (0.30, 0.35, 0.45, 0.625)) +
          "; generous (law's r_ta): " + " / ".join(f"{np.interp(q, XR, v['generous']):.4f}" for q in (0.30, 0.35, 0.45, 0.625)))
curves(S_FW, "canonical", "P2", "fw")
curves(S_2, "canonical", "P2", "d2")
for tag, lab_ in (("fw", "CFG11's sample (contaminated)"), ("d2", "2-Mpc cut")):
    v = CURVES[(tag, "canonical", "P2")]
    P(f"    canonical P2 [{lab_}]: R_groups(0.35) {np.interp(0.35, XR, v['groups']):.4f}; R_assoc 0.35 / 0.625: "
      f"{np.interp(0.35, XR, v['associations']):.4f} / {np.interp(0.625, XR, v['associations']):.4f}")
for k, v in STAT.items():
    P(f"    {k[1][:3]}/{k[2]} x {k[3]}: {v['n_groups']} groups -> {v['n_assoc']} associations ({v['multi']} multi-group, holding "
      f"{v['frac_baryons_multi']:.2f} of the baryons); largest: {v['largest_ngroups']} groups, {v['largest_ngal']} galaxies, "
      f"M_b {v['largest_Mb']:.2e} ({v['largest_frac']:.2f} of the sample); R without it {v['R_without_largest']:.4f}")
check("C2 CONTROL: the finder conserves the sample (every group in one association; baryons summed exactly)",
      f"conserved: {cons}", cons)
j35 = int(np.argmin(np.abs(XR - 0.35)))
vop = CURVES[("op", "canonical", "P2")]; vfw = CURVES[("fw", "canonical", "P2")]
h0 = vop["associations"][j35] < vop["groups"][j35] - 1e-9
check("H0 association ownership lowers the phantom sum below the group level at x = 0.35 (canonical P2, operative sample)" +
      ("  [MUTATE: linking off]" if MUTATE else ""),
      f"R_assoc {vop['associations'][j35]:.4f} vs R_groups {vop['groups'][j35]:.4f}", h0)
check("H0 (first-written, CFG11's sample -- CONTAMINATED by the MW entry, see REVISION; not a result)",
      f"R_assoc {vfw['associations'][j35]:.4f} vs R_groups {vfw['groups'][j35]:.4f}",
      vfw["associations"][j35] < vfw["groups"][j35] - 1e-9, load_bearing=False)

# ================================================================================================ the edges and the KiDS cost
R.banner("THE BUDGET EDGE WITH ASSOCIATIONS, AND KiDS's COST THERE AGAINST ITS OWN BEST (CFG23_diagnostics V4)")
C16P = os.path.join(HERE, "CFG16_selfconsistent_floor.py")
s16 = open(C16P).read()
g16 = {"__file__": C16P, "__name__": "cfg16_slices", "json": json, "os": os, "sys": sys, "math": math, "time": time, "np": np,
       "C7": C7, "C": C, "HERE": HERE, "MUTATE": False, "P": lambda *a, **k: None, "check": lambda *a, **k: None, "R": _Q()}
a_ = s16.index("SWJ = json.load(")
b_ = s16.index("# ================================================================================================ C1\n")
exec(compile("\n" * s16[:a_].count("\n") + s16[a_:b_], C16P, "exec"), g16)
_KC = {}


def kids_cost(f, kn, x):
    key = (f, kn, round(x, 10))
    if key not in _KC:
        T = g16["table"](g16["M_trunc_xta"](g16["KERN"][kn], x), f)
        v = g16["kfit_caps"](T, g16["caps_at"](f, kn, x))
        v = v[0] if isinstance(v, tuple) else v
        best = g16["BASE"][(f, kn)] + C21[f"{f}|{kn}|1.145e+11"]["kids_min"]
        _KC[key] = (float(v - best), float(v), float(best))
    return _KC[key]


EDG = {}
for (tag, f, kn), cv in CURVES.items():
    out = {}
    for lab, arr in (("groups", cv["groups"]), ("associations", cv["associations"]), ("generous", cv["generous"])):
        e = edge_with(f, kn, lambda x, _arr=arr: float(np.interp(x, XR, _arr)))
        cost, chi, best = kids_cost(f, kn, e)
        out[lab] = dict(edge=e, kids_cost=cost, chi2=chi, best=best)
    out["edge_A_CFG17"] = C17J[f"{f}|{kn}"]["edge_A"]
    EDG[(tag, f, kn)] = out
    P(f"    [{tag}] {f:9s} {kn:8s}: budget edge groups {out['groups']['edge']:.4f} (CFG17 committed: {out['edge_A_CFG17']:.4f}) -> KiDS "
      f"cost {out['groups']['kids_cost']:.1f}; associations {out['associations']['edge']:.4f} -> {out['associations']['kids_cost']:.1f}; "
      f"generous {out['generous']['edge']:.4f} -> {out['generous']['kids_cost']:.1f}  (KiDS best {out['groups']['best']:.2f})")
h1 = all(EDG[("op", "canonical", kn)]["associations"]["kids_cost"] <= 9.0 for kn in KERN)
check("H1 [HEADLINE] with turned-around associations the canonical budget edge moves far enough that KiDS's cost against its own "
      "best is <= 9, both kernels (operative sample) [declared expectation: FAIL]",
      "; ".join(f"{kn}: edge {EDG[('op', 'canonical', kn)]['associations']['edge']:.4f}, cost "
                f"{EDG[('op', 'canonical', kn)]['associations']['kids_cost']:.1f}" for kn in KERN), h1)
check("H1 (first-written, CFG11's sample -- CONTAMINATED by the MW entry, see REVISION; not a result)",
      f"P2: edge {EDG[('fw', 'canonical', 'P2')]['associations']['edge']:.4f}, cost {EDG[('fw', 'canonical', 'P2')]['associations']['kids_cost']:.1f}",
      EDG[("fw", "canonical", "P2")]["associations"]["kids_cost"] <= 9.0, load_bearing=False)
check("R1 (reported) every row's edges and KiDS costs (groups = the CFG11/12/17 erratum on the operative sample); the generous variant",
      "; ".join(f"[{k[0]}] {k[1][:3]}/{k[2]}: groups {v['groups']['edge']:.4f} ({v['groups']['kids_cost']:.1f}), assoc "
                f"{v['associations']['edge']:.4f} ({v['associations']['kids_cost']:.1f}), generous {v['generous']['edge']:.4f} "
                f"({v['generous']['kids_cost']:.1f})" for k, v in EDG.items()), True, load_bearing=False)
R.num("R", {f"{k[0]}|{k[1]}|{k[2]}": dict(x=XR.tolist(), **{q: v[q].tolist() for q in v}) for k, v in CURVES.items()})
R.num("stats", {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": v for k, v in STAT.items()})
R.num("edges", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in EDG.items()})
P(f"    ({time.time() - t0:.0f} s)")
nf = R.write()
sys.exit(1 if nf else 0)
