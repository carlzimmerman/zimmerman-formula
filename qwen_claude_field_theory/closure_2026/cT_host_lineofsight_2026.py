#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cT_host_lineofsight_2026.py
===========================
WHAT IS THE FIELD ALONG THE ACTUAL GW170817 LINE OF SIGHT?

cT_gradient_coupling_2026.py closed the intergalactic leg (required power p >= 1.21, framework
supplies 3/2) and then FAILED on the host-galaxy crossing -- but it failed while assuming the
host contributes at FULL disformal strength. That assumption is wrong, and wrong in the
programme's own recurring way: it evaluates a deep-MOND quantity at a location that is not
deep-MOND.

GW170817's progenitor sat at a projected ~2 kpc from the centre of NGC 4993, an EARLY-TYPE
galaxy. That is a HIGH-acceleration environment. The disformal amplitude must be suppressed
there for exactly the same reason it is suppressed in the solar system -- otherwise general
relativity is not recovered locally at all.

This file computes the field along the actual line of sight and integrates the arrival-time
difference properly, instead of multiplying a path fraction by a deep-MOND value.
"""
import sys
import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
G, MSUN, KPC, MPC, C = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22, 2.99792458e8
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
GW_BOUND = 7e-16
# NGC 4993: early-type, stellar mass ~ 1.0e11 Msun, effective radius ~ 3.2 kpc,
# merger at projected ~2.0 kpc.  Distance 40 Mpc.
M_HOST, R_EFF, R_MERGE, D_HOST = 1.0e11 * MSUN, 3.2 * KPC, 2.0 * KPC, 40.0 * MPC

head("PART A -- the field at the merger site is NOT deep-MOND")
# Hernquist enclosed mass, a = R_eff/1.8153
a_H = R_EFF / 1.8153
def M_enc(r):
    return M_HOST * r**2 / (r + a_H) ** 2
def g_bar(r):
    return G * M_enc(r) / r**2
g_merge = g_bar(R_MERGE)
for nm, a0 in A0.items():
    info(f"A1  {nm:9s}", f"g_bar(2 kpc) = {g_merge:.3e} m/s^2 = {g_merge/a0:.1f} a_0")
y_merge_can = g_merge / A0["canonical"]
check(y_merge_can > 5,
      f"A1b *** THE MERGER SITE IS AT {y_merge_can:.0f} a_0 -- DEEP IN THE NEWTONIAN REGIME, "
      "not deep-MOND. The previous file's host term evaluated a deep-MOND coupling strength "
      "at a location where the field is more than an order of magnitude above a_0 ***",
      "the programme's recurring error mode, sprung again and caught here")

head("PART B -- the coupling strength along the line of sight")
# B(r) ~ (v_c^2/c^2) * f(y), f -> 1 deep-MOND, f -> 1/(2y) Newtonian  [the a0-line's own nu-1]
def f_supp(y):
    return np.sqrt(1 + 1 / y) - 1.0          # nu(y) - 1, the a0-line's anomaly fraction
vc2 = np.sqrt(G * M_HOST * A0["canonical"])
B_deep = vc2 / C**2
info("B0  deep-MOND reference", f"v_c^2 = sqrt(G M a_0) = {vc2:.3e} m^2/s^2, "
     f"B_deep = v_c^2/c^2 = {B_deep:.3e}")
for nm, a0 in A0.items():
    info(f"B1  {nm:9s} suppression at the merger site",
         f"f(y={g_merge/a0:.1f}) = {f_supp(g_merge/a0):.4f}  =>  B ~ {B_deep*f_supp(g_merge/a0):.3e}")

head("PART C -- integrate the arrival-time difference along the real path")
def dt_over_t(a0, p_grad):
    """Path integral of B/2 from the merger site outward, then intergalactic.
    B(r) = B_deep * f(y) * (Y/Y_a0)^p with Y ~ (g/c^2)^2 giving the gradient suppression
    only BELOW a0 (the escape); above a0 the f(y) factor does the suppressing."""
    rs = np.geomspace(R_MERGE, 300 * KPC, 20000)
    y = g_bar(rs) / a0
    grad_sup = np.where(y < 1.0, y ** (2 * p_grad), 1.0)     # Y^p suppression in deep MOND
    Br = B_deep * f_supp(y) * grad_sup
    host = np.trapz(Br / 2, rs)                              # metres of B/2
    # intergalactic remainder
    g_igm = 300e3 / (13.8 * 3.156e16)
    B_igm = B_deep * (g_igm / a0) ** (2 * p_grad)
    path = (D_HOST - rs[-1]) * B_igm / 2
    return (host + path) / D_HOST, host / D_HOST, path / D_HOST
for nm, a0 in A0.items():
    tot, h, pth = dt_over_t(a0, 1.5)
    info(f"C1  {nm:9s} at p = 3/2",
         f"host {h:.3e} + path {pth:.3e} = {tot:.3e}  ({tot/GW_BOUND:.2e}x the bound)")
tot_can, h_can, p_can = dt_over_t(A0["canonical"], 1.5)
prev = 9.81e-11
check(tot_can < prev,
      f"C2  *** INTEGRATING PROPERLY GIVES Delta t/t = {tot_can:.3e}, against the previous "
      f"file's {prev:.2e} from multiplying a path fraction by the deep-MOND value. The correct "
      f"treatment is {prev/tot_can:.1f}x SMALLER -- the assumption, not the physics, was "
      "carrying the failure ***",
      f"direction: the earlier number MANUFACTURED A DEFICIT by {prev/tot_can:.1f}x")
check(tot_can > GW_BOUND,
      f"C3  BUT IT STILL FAILS: {tot_can:.3e} against {GW_BOUND:.1e}, over by "
      f"{tot_can/GW_BOUND:.2e}x = {np.log10(tot_can/GW_BOUND):.2f} orders",
      "the gate does not close; the gap is smaller and better characterised, not gone")
info("C4  where it now comes from", f"host {h_can/tot_can*100:.1f}% / intergalactic "
     f"{p_can/tot_can*100:.1f}% -- so the binding contribution is still the host, and inside "
     "the host it is the OUTER galaxy (deep-MOND, unsuppressed by f) rather than the merger site")

head("PART D -- what actually decides it")
for nm, a0 in A0.items():
    best = min(dt_over_t(a0, p)[0] for p in (1.5, 2.0, 3.0, 5.0))
    info(f"D1  {nm:9s} best over p in [1.5, 5]", f"{best:.3e} = {best/GW_BOUND:.2e}x bound")
check(min(dt_over_t(A0["canonical"], p)[0] for p in (1.5, 2.0, 3.0, 5.0)) > GW_BOUND,
      "D2  and raising the gradient power does NOT help further, because the residual is "
      "generated in the host's deep-MOND outskirts where the gradient suppression is by "
      "construction absent -- that is exactly where lensing needs B at full strength",
      "*** SO THE TWO REQUIREMENTS COLLIDE IN THE SAME PLACE: the deep-MOND outskirts of any "
      "galaxy a GW crosses. That is the irreducible statement of the welding ***")
for s_ in [
    "THE HONEST RESULT: integrating along the real line of sight, with the merger site's true "
    f"{y_merge_can:.0f} a_0 environment and the a_0-line's own anomaly fraction, reduces the "
    f"gap by {prev/tot_can:.1f}x relative to the previous file. It does NOT close it: the "
    f"residual is {tot_can/GW_BOUND:.1e}x the GW170817 bound.",
    "AND IT LOCATES THE OBSTRUCTION EXACTLY, which the earlier files did not: not the "
    "intergalactic path (closed by the gradient power), not the merger site (Newtonian, "
    "suppressed), but THE DEEP-MOND OUTSKIRTS OF THE HOST -- the one region where lensing "
    "requires the coupling at full strength and no suppression mechanism is available, "
    "because suppressing it there is the same as switching off MOND.",
    "THAT IS THE IRREDUCIBLE FORM OF THE WELDING, and it is a cleaner statement than 'c_T "
    "fails': any galaxy a gravitational wave crosses has a deep-MOND region, and in that "
    "region lensing and c_T make incompatible demands on the same function.",
    "NOT RULED OUT, and stated as an open door rather than a closed one: a coupling whose "
    "disformal piece is orthogonal to the propagation direction, or one built on a NULL "
    "rather than timelike vector, would evade the null-cone argument entirely. Neither was "
    "computed here.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"LINE-OF-SIGHT CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
