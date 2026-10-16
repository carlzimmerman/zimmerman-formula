#!/usr/bin/env python3
"""PARAMRED lane C (LSTAR): what is the stiffness length L*?  Criteria: FROZEN_CRITERIA.md (written before this script ran).

Part 1: every constraint on L* on the record, read from the recorded JSONs (read only), plus ONE new compute: the SPARC upper
edge of the window (CFG691's own statistic copied, scanned from 1 kpc to 30 kpc).  Part 2: the P-sector branch conditions.
kappa = 1/2 FITTED; both footings (never pooled); no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 19 python3 lstar_constraints.py        (LSTAR_MUTATE=1: S = 1 negative control; exit 1 iff it bites)
Inputs: small JSON / text only (CFG4_common reads the SPARC rotmod text files).  Writes only next to itself.
"""
import os, sys, json, math, time

sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import solve_bvp
import resource

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(os.path.dirname(HERE))          # campaign_fresh_gravity
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("LSTAR_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"lstar_constraints{TAG}.out"), "w")
RES = {"lane": "PARAMRED_C_LSTAR", "mutate": MUT, "checks": {}, "R": {}}
T0 = time.time()
G, MSUN, AU, PC, KPC_S = 6.6743e-11, 1.98847e30, 1.495978707e11, 3.0856775814913673e16, 3.0857e19
GM_SUN = 1.32712440018e20
SUN_BOUND, M_SAT_BOUND, R_SAT = 3.66e-14, 6.7e-11, 9.54 * AU       # the record's CFG3 gates (as in CFG691)
Q2_CEIL = 5.2e-27                                                   # CFG770 (Park+2026 2-sigma ceiling), s^-2
C_LIGHT = 299792458.0
FOOT = C4.FOOTS


def P(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


def MEM(tag, cap=285.0):
    """RSS guard (compute gate: <= 300 MB): record max RSS so far (macOS reports bytes) and stop before the cap is exceeded."""
    mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    RES.setdefault("maxrss_MB_by_stage", {})[tag] = mb
    if mb > cap:
        P(f"MEMORY GUARD: max RSS {mb:.0f} MB > {cap:.0f} MB at stage '{tag}': stopping (compute gate)")
        OUT.close()
        sys.exit(3)


def bisect_root(fn, lo, hi, n=80):
    """root of a decreasing-through-zero function on [lo, hi] (log-space arguments), plain bisection."""
    flo = fn(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = fn(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def J(rel):
    return json.load(open(os.path.join(LANES, rel)))


def js(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


P(__doc__.strip())

# ============================================================================ the universal profile (CFG691, copied)
def solve_profile(smin=1e-4, smax=1e4):
    """-[q'' + 2q'/s - 2q/s^2] + q|q| = 1/s^2 in t = ln s: y1 = q, y2 = dq/dt."""
    def f(t, y):
        s = np.exp(t)
        return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])

    def bc(ya, yb):
        return np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1 / smax - 1 / smax ** 2)])

    t = np.linspace(math.log(smin), math.log(smax), 4001)
    s = np.exp(t)
    y0 = np.vstack([1 / (s + 2), -s / (s + 2) ** 2])
    return solve_bvp(f, bc, t, y0, tol=1e-8, max_nodes=200000)


sol = solve_profile()
MEM('profile solved')


def S_of(s):
    s = np.asarray(s, float)
    out = np.empty_like(s)
    lo, hi = s < 1e-4, s > 1e4
    mid = ~(lo | hi)
    out[lo] = s[lo] * 0.5
    out[hi] = 1 - 1 / s[hi]
    out[mid] = s[mid] * sol.sol(np.log(s[mid]))[0]
    return out


def g_an(r, M, Lstar, a0):
    rM = math.sqrt(G * M / a0)
    ell = Lstar ** 2 / (2 * rM)
    return math.sqrt(G * M * a0) / r * float(S_of(np.array([r / ell]))[0])


c691 = J("CFG691_stiffness_window/cfg691_results.json")["numbers"]
P("\nK1  profile table vs CFG691 JSON")
k1 = max(abs(sv * float(sol.sol(math.log(sv))[0]) / c691["profile"]["S_table"][str(sv)] - 1) for sv in (0.01, 0.1, 0.3, 1, 3, 10, 100))
check("K1 S(s) table reproduces CFG691 JSON (1e-6 relative)", sol.status == 0 and k1 <= 1e-6, f"status {sol.status}, max rel diff {k1:.2e}")

# ============================================================================ SPARC statistic (CFG691 G-GAL, copied)
GAL = C4.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL]); eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL]); Vd = np.concatenate([g["Vdisk"] for g in GAL]); Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WPT = 1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2
WW = np.where(OK, WPT[:, None], 0.0)
last = np.array([np.where(GI == i)[0][-1] for i in range(NG)])
MB_LAST = np.clip(VB2[last] * 1e6 * Rm[last, None] / G, 1e30, None)          # [NG, U]  (CFG691: total baryon mass at the last point)
RM_LAST = np.sqrt(G * MB_LAST)[GI]                                            # [Npts, U]; r_M = RM / sqrt(a0)
MB_PT = np.clip(VB2 * 1e6 * Rm[:, None] / G, 1e30, None)                      # variant: enclosed mass at each point
RM_PT = np.sqrt(G * MB_PT)
MEM('SPARC arrays built')


def fit(a0, Lstar, mode="last", nblk=7):
    """rms (dex) and Upsilon_disk of the screened simple-nu fit; Lstar in metres; MUT: S = 1 (no stiffness).
    Upsilon columns are processed in blocks (identical arithmetic, smaller temporaries: compute gate <= 300 MB)."""
    RMx = RM_LAST if mode == "last" else RM_PT
    mse_parts = []
    for sl in np.array_split(np.arange(len(UPS)), nblk):
        with np.errstate(all="ignore"):
            ok = OK[:, sl]
            gb = np.where(ok, GB[:, sl], 1.0)
            boost = np.sqrt(a0 / gb)
            if Lstar > 0 and not MUT:
                ell = Lstar ** 2 / (2 * RMx[:, sl] / math.sqrt(a0))
                boost = boost * S_of((Rm[:, None] / ell).ravel()).reshape(ell.shape)
            r_ = np.log10(np.where(ok, GO[:, sl], 1.0)) - np.log10(np.where(ok, (1 + boost) * gb, 1.0))
        ww = WW[:, sl]
        mse_parts.append((ww * r_ ** 2).sum(0) / ww.sum(0))
    mse = np.concatenate(mse_parts)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


if not MUT:
    P("\nK2  SPARC statistic vs CFG691 JSON (316.2 pc, 1000 pc), and K3 vs CFG760 JSON (7585 pc alt, 9549 pc canonical)")
    k2 = True; k3 = True; det2 = []; det3 = []
    for f in FOOT:
        lad = c691["G_GAL"][f]["ladder"]
        for key, Lpc in (("316", 10 ** 2.5), ("1e+03", 1e3)):
            r_, u_ = fit(C4.A0[f], Lpc * PC)
            k2 &= abs(r_ - lad[key]["rms"]) <= 1e-6 and abs(u_ - lad[key]["U"]) < 1e-9
            det2.append(f"{f} {key}: {r_:.8f}@{u_:.2f} vs {lad[key]['rms']:.8f}@{lad[key]['U']:.2f}")
    c760 = J("CFG760_p_wave_gap/cfg760_results.json")["numbers"]["G3"]
    for f in FOOT:
        r_, u_ = fit(C4.A0[f], c760[f]["L_all_pc"] * PC)
        k3 &= abs(r_ - c760[f]["rms"]) <= 1e-6 and abs(u_ - c760[f]["U"]) < 1e-9
        det3.append(f"{f} {c760[f]['L_all_pc']:.0f} pc: {r_:.8f}@{u_:.2f} vs {c760[f]['rms']:.8f}@{c760[f]['U']:.2f}")
    check("K2 rms/Upsilon at 316 and 1000 pc reproduce CFG691 JSON (1e-6)", k2, "; ".join(det2))
    check("K3 rms/Upsilon at L*_all reproduce CFG760 JSON (1e-6)", k3, "; ".join(det3))

# ============================================================================ R7 SPARC upper edge (NEW compute)
P("\nR7  SPARC upper edge of the window: CFG691 statistic, L* 1 kpc .. 30 kpc on a 0.01-dex grid, Upsilon_disk profiled 0.30-1.20"
  + ("   [MUTATE: S = 1, no stiffness]" if MUT else ""))
LS = 10 ** np.round(np.arange(3.0, 4.4772, 0.01), 2)                    # pc, 1 kpc .. 30 kpc
R7 = {}
for f in FOOT:
    R7[f] = {}
    for mode in (("last",) if MUT else ("last", "pt")):
        rows = []
        for k_, L in enumerate(LS):
            rows.append(fit(C4.A0[f], L * PC, mode))
            if k_ % 20 == 0:
                MEM(f'R7 scan {f} {mode} {k_}')
        rms = np.array([x[0] for x in rows]); ups = np.array([x[1] for x in rows])
        ent = dict(rms_at_1kpc=float(rms[0]), U_at_1kpc=float(ups[0]), rms_at_30kpc=float(rms[-1]),
                   nonmonotone_steps=int((np.diff(rms) < -1e-9).sum()), edges={})
        for line in (0.105, 0.110, 0.115):
            okg = rms <= line
            if not okg[0]:
                ent["edges"][str(line)] = dict(Lmax_pc=None, note="already failing at 1 kpc")
                continue
            nf = int(np.argmin(okg)) if not okg.all() else None            # first failing index of the contiguous run
            if nf is None:
                ent["edges"][str(line)] = dict(Lmax_pc=None, note="no edge up to 30 kpc")
            else:
                ent["edges"][str(line)] = dict(Lmax_pc=float(LS[nf - 1]), first_fail_pc=float(LS[nf]), rms_at_edge=float(rms[nf - 1]),
                                               rms_first_fail=float(rms[nf]), U_at_edge=float(ups[nf - 1]),
                                               passes_again_later=bool(okg[nf:].any()))
        ent["ladder"] = {f"{LS[k]:.5g}": dict(rms=float(rms[k]), U=float(ups[k])) for k in range(0, len(LS), 10)}
        R7[f][mode] = ent
        e = ent["edges"]["0.11"]
        P(f"    {f:9s} [{mode:4s}] rms(1 kpc) {rms[0]:.5f}  rms(30 kpc) {rms[-1]:.5f}  non-monotone steps {ent['nonmonotone_steps']}  "
          + "edges (0.105/0.110/0.115): " + " / ".join((f"{ent['edges'][str(l)]['Lmax_pc']:.0f} pc" if ent['edges'][str(l)].get('Lmax_pc') else "none") for l in (0.105, 0.11, 0.115)))
RES["R"]["R7_sparc_edge"] = R7
MEM('R7 done')

if MUT:
    bite = all(R7[f]["last"]["edges"]["0.11"].get("Lmax_pc") is None and R7[f]["last"]["edges"]["0.11"].get("note") == "no edge up to 30 kpc" for f in FOOT)
    P(f"\nMUTATE (S = 1): edge found on either footing? {'NO -> the edge is caused by the stiffness; tooth bites' if bite else 'YES -> negative control FAILED to bite'}")
    RES["verdict"] = dict(mutate_bites=bool(bite))
    json.dump(RES, open(os.path.join(HERE, f"lstar_constraints_results{TAG}.json"), "w"), indent=1, default=js, sort_keys=True)
    OUT.close()
    sys.exit(0 if bite else 1)

EDGE = {f: R7[f]["last"]["edges"]["0.11"].get("Lmax_pc") for f in FOOT}

# ============================================================================ R1-R4 lower-edge gates
P("\nR1/R2  Solar-System gates (CFG691): ratio(L*) = ratio(L*_grid) (L*_grid/L*)^2 exactly (inner pull GM/L*^2)")
LOW = {}
for f in FOOT:
    gs = c691["G_SS"][f]
    Lg = gs["Lmin_pc"]
    LOW[f] = dict(L_grid_pc=Lg, L_Saturn_pc=Lg * math.sqrt(gs["ratio_Sat_at_Lmin"]), L_1AU_pc=Lg * math.sqrt(gs["ratio_1AU_at_Lmin"]))
    # K4: root of the full-profile ratio
    a0 = C4.A0[f]
    fr = lambda lnL: g_an(R_SAT, MSUN, math.exp(lnL) * PC, a0) * R_SAT ** 2 / G / MSUN / M_SAT_BOUND - 1.0
    root = math.exp(bisect_root(fr, math.log(1.0), math.log(20.0)))
    LOW[f]["L_Saturn_fullprofile_root_pc"] = root
    P(f"    {f:9s}: grid L*_min {Lg:.4f} pc;  Saturn edge {LOW[f]['L_Saturn_pc']:.4f} pc (full-profile root {root:.4f});  1-AU edge {LOW[f]['L_1AU_pc']:.4f} pc")
check("K4 Saturn edge: scaling vs full-profile root (1e-3)", all(abs(LOW[f]["L_Saturn_pc"] / LOW[f]["L_Saturn_fullprofile_root_pc"] - 1) <= 1e-3 for f in FOOT),
      "; ".join(f"{f} {LOW[f]['L_Saturn_pc']:.4f} vs {LOW[f]['L_Saturn_fullprofile_root_pc']:.4f}" for f in FOOT))

c770 = J("CFG770_cassini_stiff_action/cfg770_results.json")["numbers"]
worst_q2 = max(abs(v) for v in c770["T1_Q2"].values())
t2 = c770["T2"]
k6 = abs((abs(t2["5.75"]) / abs(t2["30"])) / (30 / 5.75) ** 3 - 1)
check("K6 Q2 ~ L*^-3 on CFG770's own ladder (1e-2 relative at 5.75 vs 30 pc)", k6 <= 1e-2, f"ratio/(30/5.75)^3 - 1 = {k6:.2e}")
L_Q2 = 5.75 * (worst_q2 / Q2_CEIL) ** (1 / 3)
P(f"R3  Cassini Q2: worst |Q2| {worst_q2:.4e} s^-2 over 3 g_e x 2 footings at 5.75 pc = {worst_q2 / Q2_CEIL:.3e} of the ceiling -> L* >= {L_Q2:.4f} pc")

c658 = J("CFG658_one_action_untested_gates/cfg658_efe_results.json")
fr_sat = max(v["frac_sat"] for v in c658["E3"]["rows"].values())
L_E3 = c691["G_SS"]["canonical"]["Lmin_pc"] * math.sqrt(fr_sat / 0.155)
P(f"R4  star halos (CFG694 G3 / CFG658 E3): worst M_ph/M {fr_sat:.5f} at L* {c691['G_SS']['canonical']['Lmin_pc']:.4f} pc, r_b 1.08 pc; allowance 0.155 -> L* >= {L_E3:.4f} pc  (pure scaling 1.08/sqrt(0.155) = {1.08 / math.sqrt(0.155):.4f})")
RES["R"]["R1_R4_lower"] = dict(per_footing=LOW, Q2=dict(worst_abs_Q2=worst_q2, ceiling=Q2_CEIL, ratio=worst_q2 / Q2_CEIL, L_Q2_pc=L_Q2),
                               E3=dict(worst_frac_sat=fr_sat, allowance=0.155, L_E3_pc=L_E3))
L_LOWER = {f: max(LOW[f]["L_Saturn_pc"], LOW[f]["L_1AU_pc"], L_E3, L_Q2) for f in FOOT}
P(f"    lower edge = max(R1..R4) = {L_LOWER['canonical']:.4f} pc (canonical) / {L_LOWER['alt']:.4f} pc (alt); set by the Saturn gate")

P("\n     sensitivity of the lower edge to the Saturn-orbit enclosed-mass bound B (L*_min = r/sqrt(B), r = 9.54 AU): improvement needed to probe L*")
IMPR = {}
for Lt in (5.754, 10, 30, 100, 300, 1000):
    need_B = (9.54 * AU / (Lt * PC)) ** 2
    IMPR[str(Lt)] = dict(B_needed_Msun=need_B, improvement_factor_vs_6p7e_11=M_SAT_BOUND / need_B)
    P(f"        to reach L* = {Lt:7.1f} pc the bound must fall to {need_B:.2e} Msun  ({M_SAT_BOUND / need_B:.2e} x tighter than 6.7e-11)")
RES["R"]["R1_sensitivity"] = IMPR

# ============================================================================ R5 wide binaries
P("\nR5  wide binaries (CFG740 formula gamma_v - 1 = (1/2)(s/L*)^2; CFG816 error model)")
c740 = J("CFG740_sealed_wb_slope2/cfg740_predictions.json")
S50 = 50000 * AU / PC
S236 = 236000 * AU / PC
L0 = c740["Lstar_pc"]
env50 = 0.5 * (S50 / L0) ** 2
env236 = 0.5 * (S236 / L0) ** 2
k7 = max(abs(env50 / c740["footings"][f]["bins_kAU"]["50"]["inner_limit"] - 1) for f in c740["footings"])
check("K7 CFG740 envelope at 50 kAU, L* 5.7544 pc (1e-3 vs JSON inner limit)", k7 <= 1e-3, f"formula {env50:.6e}, rel diff {k7:.2e}")
sig = lambda N: math.sqrt((0.019 * math.sqrt(30000 / N)) ** 2 + 0.02 ** 2)
Ns = (1421, 5000, 10000, 30000, 100000)
rec = (0.090, 0.051, 0.039, 0.028, 0.023)
check("K5 CFG816 sigma_tot values (6e-4)", all(abs(sig(N) - r) <= 6e-4 for N, r in zip(Ns, rec)), ", ".join(f"{sig(N):.4f}" for N in Ns))
L_sat = LOW["canonical"]["L_Saturn_pc"]
env50_sat = 0.5 * (S50 / L_sat) ** 2
WB = dict(s50_pc=S50, s236_pc=S236, envelope_50kAU_at_Lmin=env50, envelope_236kAU_at_Lmin=env236, envelope_50kAU_at_Saturn_edge=env50_sat, null=[], detect=[])
P(f"    s = 50 kAU = {S50:.5f} pc.  Envelope (1/2)(s/L*)^2 at L*=5.7544: {env50:.4e} at 50 kAU, {env236:.4e} at 236 kAU; at the exact Saturn edge {L_sat:.3f} pc: {env50_sat:.4e} at 50 kAU")
P("    NULL (DR4 R-statistic error model): 2-sigma upper limit beta = 2 sigma_tot on gamma_v - 1 at 50 kAU  ->  L* >= s / sqrt(2 beta)")
for N in Ns:
    sg = sig(N); beta = 2 * sg
    Lb = S50 / math.sqrt(2 * beta)
    Lb236 = S236 / math.sqrt(2 * beta)
    WB["null"].append(dict(N=N, sigma_tot=sg, beta_2sigma=beta, L_bound_50kAU_pc=Lb, L_bound_236kAU_extrapolated_pc=Lb236, exceeds_Saturn_edge=bool(Lb > L_sat)))
    P(f"        N = {N:6d}: sigma_tot {sg:.4f}, 2-sigma beta {beta:.4f} -> L* >= {Lb:.3f} pc at 50 kAU ({Lb236:.2f} pc if the 236 kAU bin were usable at the same error); exceeds Saturn edge {L_sat:.2f}? {Lb > L_sat}")
sig_req = env50_sat / 2
WB["sigma_required_to_exceed_Saturn_at_50kAU"] = sig_req
WB["floor_over_required"] = 0.02 / sig_req
P(f"    to move the lower edge ABOVE the Saturn edge a null needs 2 sigma < {env50_sat:.3e}, i.e. sigma < {sig_req:.2e}; the irreducible floor is 0.02 -> {0.02 / sig_req:.0f} x short, at any N")
P("    DETECTION b = R - 1 at 50 kAU (maps to L* = s / sqrt(2 b); the framework needs L* >= the Saturn edge):")
for b in (env50_sat, 0.003, 0.01, 0.05, 0.10, 0.15, 0.20):
    Lb = S50 / math.sqrt(2 * b)
    WB["detect"].append(dict(b=b, L_pc=Lb, contradicts_Saturn=bool(Lb < L_sat)))
    P(f"        b = {b:.4e}: L* = {Lb:7.3f} pc  {'< Saturn edge: no L* in the stiffened action reproduces it' if Lb < L_sat else '(>= Saturn edge)'}")
WB["kill_rule_b"] = 0.01
WB["L_at_kill_rule_pc"] = S50 / math.sqrt(2 * 0.01)
WB["resolvable_b_at_3sigma"] = {str(N): 3 * sig(N) for N in Ns}
WB["untestable_zone_b"] = [env50_sat, 3 * sig(100000)]
P(f"    kill rule b >= 0.01 (3 sigma) maps to L* <= {WB['L_at_kill_rule_pc']:.3f} pc ({L_sat / WB['L_at_kill_rule_pc']:.1f} x below the Saturn edge).  Untestable zone: b between {env50_sat:.2e} and {3 * sig(100000):.3f} (3 sigma at N = 1e5)")
dr3 = c658["E1"]["rows"]
WB["DR3"] = dict({f"{f}|basin_only(L*->0)": dict(median=dr3[f"{f}|basin_only"]["median"], z_builder=dr3[f"{f}|basin_only"]["z_builder"]) for f in FOOT},
                 **{f"{f}|Cstar(L*=5.754)": dict(median=dr3[f"{f}|Cstar"]["median"], z_builder=dr3[f"{f}|Cstar"]["z_builder"]) for f in FOOT})
P(f"    DR3 (CFG658 E1, record as given): L* -> 0 gives gamma-hat 1.500, excluded at +{dr3['canonical|basin_only']['z_builder']:.2f} / +{dr3['alt|basin_only']['z_builder']:.2f} sigma; L* = 5.754 pc gives "
  f"{dr3['canonical|Cstar']['median']:.4f} / {dr3['alt|Cstar']['median']:.4f}, {dr3['canonical|Cstar']['z_builder']:+.2f} / {dr3['alt|Cstar']['z_builder']:+.2f} sigma (CONSISTENT). No injection at 0 < L* < 5.754 pc is on the record: DR3 gives NO L* bound beyond that.")
RES["R"]["R5_wide_binaries"] = WB

# ============================================================================ R6 fixed-L* sealed predictions
c774 = J("CFG774_sealed_deep_space/cfg774_results.json")["table"]
a5, a30 = abs(c774["canonical_Lstar_5.75"]["10"]), abs(c774["canonical_Lstar_30"]["10"])
k_a = abs((a5 / a30) / (30 / 5.75) ** 2 - 1)
check("K8 CFG774 pull ~ L*^-2 (1e-3)", k_a <= 1e-3, f"{k_a:.2e}")
L_kill774 = 5.75 * math.sqrt(a5 / 1e-13)
R6 = dict(pull_5p75=a5, kill_line=1e-13, L_at_kill_pc=L_kill774, table={str(Lt): a5 * (5.75 / Lt) ** 2 for Lt in (5.75, 10, 30, 100, 300, 1000)})
P(f"\nR6  CFG774 probe pull a(L*) = {a5:.4e} (5.75/L*)^2 m/s^2:  " + ", ".join(f"{Lt} pc: {v:.2e}" for Lt, v in ((k, v) for k, v in R6['table'].items())))
P(f"    kill line 1e-13 beyond 1000 AU maps to L* <= {L_kill774:.3f} pc (below the Saturn edge -> a detection kills the stiffened action, it does not select an L*).")
P("    CFG771 saddle stress ~ L*^-2 (null at 5.75 pc; larger L* is smaller); CFG772 lab prediction is L*-independent (F1: 0): neither bounds L*.")
RES["R"]["R6_fixed"] = R6

# ============================================================================ R8 P-sector branch conditions
P("\nR8  P-sector branch conditions vs the SPARC edge (R7, primary 'last' mass, line 0.110)")
c760 = J("CFG760_p_wave_gap/cfg760_results.json")["numbers"]["G3"]
c744 = J("CFG744_radiative_damping_scale/cfg744_results.json")["N2"]
R8 = {}
for f in FOOT:
    lo = c760[f]["L_open"]
    n_inside = sum(1 for v in lo.values() if v <= 1000.0)
    cases = {k: v for k, v in c744.items() if k.startswith(f + "|")}
    Lopen_law = {k: 5.754 * math.sqrt(v["t_medium_Gyr"] / 4.6) for k, v in cases.items()}
    s0_new = {k: cases[k]["s0"] * (5.754 / Lopen_law[k]) ** 2 for k in cases}
    Lopen_len = {k: 5.754 * v["t_medium_one_crossing_Gyr"] / 13.8 for k, v in cases.items()}
    R8[f] = dict(
        pwave_export=dict(L_all_pc=c760[f]["L_all_pc"], L_open=lo, n_cases_open_by_1kpc=n_inside, closed_by_SPARC_edge=bool(EDGE[f] is not None and c760[f]["L_all_pc"] > EDGE[f])),
        ident_law=dict(L_open_pc=Lopen_law, L_all_pc=max(Lopen_law.values()), L_min_case_pc=min(Lopen_law.values()), s0_at_open=s0_new,
                       closed_by_SPARC_edge=bool(EDGE[f] is not None and max(Lopen_law.values()) > EDGE[f])),
        ident_lenient=dict(L_open_pc=Lopen_len, L_all_pc=max(Lopen_len.values()), closed_by_SPARC_edge=bool(EDGE[f] is not None and max(Lopen_len.values()) > EDGE[f])))
    P(f"    {f:9s}: SPARC edge {EDGE[f]:.0f} pc")
    P(f"        (a) P-wave export (CFG760 G3): L*_all {c760[f]['L_all_pc']:.0f} pc; {n_inside}/8 cases already open by 1 kpc;  closed over the window: {R8[f]['pwave_export']['closed_by_SPARC_edge']}")
    P(f"        (b) identification, CFG744 law t ~ L*^-2, 4.6 Gyr: L*_open per case {min(Lopen_law.values()):.0f} .. {max(Lopen_law.values()):.0f} pc; min s0 at L*_open "
      f"{min(s0_new.values()):.2f} (law fitted on s0 10-80); closed over the window: {R8[f]['ident_law']['closed_by_SPARC_edge']}")
    P(f"        (c) identification, exponent-free one-crossing bound t ~ L*^-1, 13.8 Gyr (necessary only): L*_open {min(Lopen_len.values()):.0f} .. {max(Lopen_len.values()):.0f} pc; closed over the window: {R8[f]['ident_lenient']['closed_by_SPARC_edge']}")
RES["R"]["R8_branches"] = R8

# ============================================================================ R9 UFD (reported only)
P("\nR9  screening factor S(r_h / ell_gamma) for a generic dwarf (r_h = 30 pc), canonical a0 -- generic, NOT scored")
R9 = {}
a0c = C4.A0["canonical"]
for M in (1e3, 1e4, 1e5, 1e7):
    row = {}
    rM = math.sqrt(G * M * MSUN / a0c)
    for Lt in (5.754, 30, 100, 300, 1000):
        ell = (Lt * PC) ** 2 / (2 * rM)
        row[str(Lt)] = dict(ell_gamma_pc=ell / PC, S=float(S_of(np.array([30 * PC / ell]))[0]))
    R9[str(M)] = row
    P(f"    M_b {M:8.0e} Msun: " + "  ".join(f"L*={Lt}: S={row[str(Lt)]['S']:.3g}" for Lt in (5.754, 30, 100, 300, 1000)))
RES["R"]["R9_generic_dwarf"] = R9

# ============================================================================ Part 2 numbers
P("\nPart 2  scale argument (D-B), numbers frozen before the comparison")
c2a = {f: C_LIGHT ** 2 / C4.A0[f] for f in FOOT}
D = {f: dict(c2_over_a0_m=c2a[f], c2_over_a0_pc=c2a[f] / PC, ratio_to_SPARC_edge=(c2a[f] / PC) / EDGE[f]) for f in FOOT}
for f in FOOT:
    P(f"    {f:9s}: c^2/a0 = {c2a[f]:.4e} m = {c2a[f] / PC:.4e} pc;  / SPARC edge {EDGE[f]:.0f} pc = {D[f]['ratio_to_SPARC_edge']:.2e};  / lower edge {L_LOWER[f]:.2f} pc = {c2a[f] / PC / L_LOWER[f]:.2e}")
RES["R"]["D_B_scale"] = D

# ============================================================================ interval + verdict
INT = {f: dict(lower_pc=L_LOWER[f], lower_set_by="Saturn enclosed-mass gate (CFG691 G-SS, Pitjev & Pitjeva bound)", upper_pc=EDGE[f], upper_set_by="SPARC rms 0.110 line (CFG691 statistic, point-mass screening of extended systems)",
            width_decades=(math.log10(EDGE[f] / L_LOWER[f]) if EDGE[f] else None)) for f in FOOT}
P("\nALLOWED INTERVAL (each footing alone; the lower edge is a-priori footing-free):")
for f in FOOT:
    P(f"    {f:9s}: L* in [{INT[f]['lower_pc']:.3f} pc, {INT[f]['upper_pc']:.0f} pc]  ({INT[f]['width_decades']:.2f} decades)")
soft = {}
for f in FOOT:
    ee = [R7[f][m]["edges"][str(l)].get("Lmax_pc") for m in R7[f] for l in (0.105, 0.11, 0.115)]
    ee = [e for e in ee if e]
    soft[f] = dict(n_edges=len(ee), spread=(max(ee) / min(ee) if ee else None), soft=bool(ee and (max(ee) / min(ee)) > 3.0), all_found=len(ee) == 6)
P("    softness (6 edges: 3 lines x 2 mass rules): " + "; ".join(f"{f} spread x{soft[f]['spread']:.2f} ({'SOFT' if soft[f]['soft'] else 'firm'}; all 6 found: {soft[f]['all_found']})" for f in FOOT))
tight = all(EDGE[f] is not None and EDGE[f] < 30000 for f in FOOT)
nontrivial = all(EDGE[f] is not None and EDGE[f] < min(c760[f2]["L_all_pc"] for f2 in FOOT) for f in FOOT)
verdict = dict(part1="CONSTRAINT TIGHTENED (upper edge located; approximation-conditional)" if tight else "NO NEW BOUND",
               part2="NO REDUCTION (no derived relation fixes L*)", intervals=INT, softness=soft, edge_below_CFG760_hatch=bool(nontrivial))
RES["verdict"] = verdict
RES["elapsed_s"] = time.time() - T0
MEM('end')
RES['maxrss_MB'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
P(f"\nVERDICT: Part 1: {verdict['part1']};  Part 2: {verdict['part2']}.  elapsed {RES['elapsed_s']:.1f} s")
fails = [k for k, v in RES["checks"].items() if not v["ok"]]
P(f"controls: {len(RES['checks']) - len(fails)}/{len(RES['checks'])} pass" + (f"; FAILED: {fails}" if fails else ""))
json.dump(RES, open(os.path.join(HERE, "lstar_constraints_results.json"), "w"), indent=1, default=js, sort_keys=True)
OUT.close()
sys.exit(1 if fails else 0)
