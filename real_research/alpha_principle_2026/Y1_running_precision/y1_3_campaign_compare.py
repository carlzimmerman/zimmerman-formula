#!/usr/bin/env python3
"""y1_3_campaign_compare.py -- Part 3 (comparison) of Y1_PREREGISTRATION.md: the campaign's one-/two-loop running (lane B `rg_common`, lane U3 `u3_lib` seven variants) against Y1-central,
at 9 scales, for a_Y, a_2, a_3 and a_em = a_Y + a_2, in percent; decomposed into (i) the running above m_t alone and (ii) the boundary/matching difference at m_t.
Run:    python3 y1_3_campaign_compare.py            (exit 0 iff the internal identities and the same-physics check pass)
MUTATE: python3 y1_3_campaign_compare.py MUTATE     (the same-physics check is run with a one-loop Y1 run and must fail: exit 1; exit 3 if not)
Writes y1_3_results.json (numbers only).  Imports lanes B, N1, U3 READ-ONLY (path-relative).  No bytecode.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for sub in ("B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L
import rg_common as RGC
import u3_lib as U3
import n1_lib as N1

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
fails = []


def chk(name, ok, info=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)


print("=" * 130)
print("Y1-3 campaign running versus Y1-central -- mode:", "MUTATE" if MUT else "REAL RUN")
print("=" * 130)

y1 = L.run_central()
XC = L.crossing(y1, "a1", "a2")
XS = U3.XS
SCALES = [("1e3", 1e3), ("1e5", 1e5), ("1e8", 1e8), ("1e10", 1e10), ("X_c(a1=a2)", XC), ("1e16", 1e16), ("X_S", XS), ("X_R", U3.XR), ("X_P", U3.XP)]
print(f"Y1-central: PDG 2024 inputs; boundary at mu = {L.PDG['Mt']} GeV: a_Y {y1.A(L.PDG['Mt'])[0]:.4f} a_2 {y1.A(L.PDG['Mt'])[1]:.4f} a_3 {y1.A(L.PDG['Mt'])[2]:.4f};  X_c = {XC:.4e} GeV")

variants = list(U3.VARIANTS_RUN)
camp = {v: U3.get_traj(v) for v in variants}


def camp_A(v, X):
    return np.array(camp[v].A(X))


def oneloop_B(X):
    return np.array(RGC.run_oneloop(X))


rows = {}
names = ["a_Y", "a_2", "a_3", "a_em"]
print("\nPERCENT DIFFERENCE  100 (campaign / Y1-central - 1)   [Y1-central values in the first block]")
hdr = "scale        " + "".join(f"{n:>26s}" for n in names)
print("Y1-central values:")
print(hdr)
for nm, X in SCALES:
    A = y1.A(X)
    vals = [A[0], A[1], A[2], A[0] + A[1]]
    print(f"{nm:12s} " + "".join(f"{v:26.5f}" for v in vals))
for v in variants + ["rg_common 1-loop"]:
    print(f"\n{v}:")
    print(hdr)
    rows[v] = {}
    for nm, X in SCALES:
        try:
            A_c = camp_A(v, X) if v != "rg_common 1-loop" else oneloop_B(X)
        except ValueError:
            print(f"{nm:12s} (outside the campaign's integrated range)")
            continue
        A = y1.A(X)
        d = [100 * (A_c[0] / A[0] - 1), 100 * (A_c[1] / A[1] - 1), 100 * (A_c[2] / A[2] - 1), 100 * ((A_c[0] + A_c[1]) / (A[0] + A[1]) - 1)]
        rows[v][nm] = d
        print(f"{nm:12s} " + "".join(f"{x:+26.4f}" for x in d))

# ------------------------------------------------------------------------------------------- decomposition for the campaign's central run (2L-T)
print("\nDECOMPOSITION for the campaign's central run 2L-T:  total = (running above m_t, both started from the campaign's own values at m_t) + (boundary / matching difference at m_t)")
Mtc = N1.MT
A0 = np.array(camp["2L-T"].A(Mtc))
u0c = L.u_from_gY_g2_g3(math.sqrt(4 * PI / A0[0]), math.sqrt(4 * PI / A0[1]), math.sqrt(4 * PI / A0[2]), N1.YT_MT, L.YB_MT_SMDR, L.YTAU_MT_SMDR, 0.126)
tr_hand = L.Traj(u0c, Mtc, L.Opts(gauge_loops=4, yuk_loops=3), mu_max=1.3e19)
print("scale        " + "".join(f"{n:>26s}" for n in ["order: a_Y", "a_2", "a_3", "a_em"]) + "".join(f"{n:>26s}" for n in ["bdry: a_Y", "a_2", "a_3", "a_em"]))
dec = {}
ok_id = True
for nm, X in SCALES:
    Ac = camp_A("2L-T", X)
    Ah = tr_hand.A(X)
    Ay = y1.A(X)
    order = [100 * (Ac[0] / Ah[0] - 1), 100 * (Ac[1] / Ah[1] - 1), 100 * (Ac[2] / Ah[2] - 1), 100 * ((Ac[0] + Ac[1]) / (Ah[0] + Ah[1]) - 1)]
    bd = [100 * (Ah[0] / Ay[0] - 1), 100 * (Ah[1] / Ay[1] - 1), 100 * (Ah[2] / Ay[2] - 1), 100 * ((Ah[0] + Ah[1]) / (Ay[0] + Ay[1]) - 1)]
    tot = rows["2L-T"][nm]
    ident = max(abs((1 + order[k] / 100) * (1 + bd[k] / 100) - (1 + tot[k] / 100)) for k in range(4))
    ok_id &= ident < 1e-12
    dec[nm] = dict(order=order, boundary=bd)
    print(f"{nm:12s} " + "".join(f"{x:+26.4f}" for x in order) + "".join(f"{x:+26.4f}" for x in bd))
chk("identity: (1 + order)(1 + boundary) = 1 + total at every scale and coupling (1e-12)", ok_id)

# ------------------------------------------------------------------------------------------- same-physics check: Y1 two-loop from the campaign's boundary reproduces the campaign's two-loop run
print("\nSAME-PHYSICS CHECK: Y1 restricted to two loops, started from the campaign's own 2L-T values at m_t, versus the campaign's 2L-T (the campaign runs the top Yukawa only and no lambda/y_b/y_tau)")
gl = 1 if MUT else 2
tr2 = L.Traj(u0c, Mtc, L.Opts(gauge_loops=gl, yuk_loops=gl), mu_max=1.3e19)
worst = 0
for nm, X in SCALES:
    Ac = camp_A("2L-T", X)
    Ah = tr2.A(X)
    e = max(abs(Ah[k] / Ac[k] - 1) for k in range(3))
    worst = max(worst, e)
    print(f"      {nm:12s} worst |Y1(2 loops)/campaign - 1| over a_Y, a_2, a_3 = {e:.2e}")
chk("Y1 two-loop run reproduces the campaign's two-loop run from the same boundary within 1e-3 at all nine scales", worst < 1e-3, f"worst {worst:.2e}")

# ------------------------------------------------------------------------------------------- route P versus route G at m_t (E9)
print("\nROUTE P (PDG alpha-hat^-1(m_Z) = 127.930, s-hat^2, alpha_s = 0.1180, run to m_t with lane U3's two-loop top-decoupled run) versus ROUTE G (Y1 matching) at mu = 172.57 GeV")
res9 = {}
for lab, s2 in (("campaign's s2 = 0.23122", 0.23122), ("PDG-2024 s2 = 0.23129", 0.23129)):
    trP = U3.Traj("2L-T", inp=dict(alpha_inv=127.930, s2w=s2, alpha_s=0.1180))
    AP = np.array(trP.A(Mtc))
    AG = y1.A(Mtc)
    d = 100 * (AP / AG - 1)
    res9[lab] = list(d)
    print(f"  {lab}:  a_Y(P) {AP[0]:.4f} vs (G) {AG[0]:.4f} -> {d[0]:+.3f}% ;  a_2 {AP[1]:.4f} vs {AG[1]:.4f} -> {d[1]:+.3f}% ;  a_3 {AP[2]:.4f} vs {AG[2]:.4f} -> {d[2]:+.3f}%")
    if s2 == 0.23129:
        for nm, X in SCALES:
            A2 = np.array(trP.A(X)); Ay = y1.A(X)
            print(f"      at {nm:12s}: a_Y {100 * (A2[0] / Ay[0] - 1):+.3f}%  a_2 {100 * (A2[1] / Ay[1] - 1):+.3f}%  a_3 {100 * (A2[2] / Ay[2] - 1):+.3f}%  a_em {100 * ((A2[0] + A2[1]) / (Ay[0] + Ay[1]) - 1):+.3f}%")

# ------------------------------------------------------------------------------------------- campaign running at PUBLISHED starting values (task item 1)
print("\nCAMPAIGN 1- AND 2-LOOP RUNNING STARTED FROM THE PUBLISHED VALUES, compared with the published values at the scales they tabulate (percent difference of a_Y, a_2, a_3)")
B_SM = np.array([41 / 6, -19 / 6, -7.0])


def camp_1loop(a0, mu0, mu):
    return a0 - B_SM / (2 * PI) * math.log(mu / mu0)


def camp_2loop(a0, yt0, mu0, mu):
    from scipy.integrate import solve_ivp
    R = N1.Runner()
    sol = solve_ivp(lambda t, y: R._rhs(t, y), [math.log(mu0), math.log(mu)], list(a0) + [yt0], rtol=1e-11, atol=1e-13)
    return sol.y[:3, -1]


# (P1) Buttazzo et al.: printed couplings at mu = M_t (their inputs) and at the Planck mass
gY0, g20, g30, yt0 = 0.35830, 0.64779, 1.1666, 0.93690
a0 = np.array([4 * PI / gY0 ** 2, 4 * PI / g20 ** 2, 4 * PI / g30 ** 2])
Mt_b = 173.34
pl_print = dict(g1=0.6154, g2=0.5055, g3=0.4873)        # g1 GUT-normalised: a_Y = (5/3) 4 pi / g1^2
aP = np.array([(5.0 / 3.0) * 4 * PI / pl_print["g1"] ** 2, 4 * PI / pl_print["g2"] ** 2, 4 * PI / pl_print["g3"] ** 2])
print("  (P1) Buttazzo et al. arXiv:1307.3536: start = their printed g_Y, g_2, g_3, y_t at mu = M_t = 173.34; end = their printed g_1, g_2, g_3 at 'M_Pl' (1.22089e19 | 1.2e19)")
print("      run                        M_Pl           a_Y diff %    a_2 diff %    a_3 diff %")
p1 = {}
for mpl in (1.220890e19, 1.2e19):
    for lab, A in (("campaign 1-loop", camp_1loop(a0, Mt_b, mpl)), ("campaign 2-loop (N1 runner)", camp_2loop(a0, yt0, Mt_b, mpl))):
        d = 100 * (A / aP - 1)
        p1[f"{lab} @ {mpl:.5e}"] = list(map(float, d))
        print(f"      {lab:28s} {mpl:.5e}   {d[0]:+10.4f}    {d[1]:+10.4f}    {d[2]:+10.4f}")
    tr_b = L.Traj(L.u_from_gY_g2_g3(gY0, g20, g30, yt0, L.YB_MT_SMDR, L.YTAU_MT_SMDR, 0.12604), Mt_b, L.Opts(gauge_loops=3, yuk_loops=3, qcd4=True), mu_max=1.3e19)
    A = np.array(tr_b.A(mpl))
    d = 100 * (A / aP - 1)
    p1[f"Y1 3-loop+QCD4 @ {mpl:.5e}"] = list(map(float, d))
    print(f"      {'Y1 (3-loop + QCD 4-loop)':28s} {mpl:.5e}   {d[0]:+10.4f}    {d[1]:+10.4f}    {d[2]:+10.4f}")
print("      (the printed values have four significant digits: rounding = +-0.5e-4/g, i.e. +-0.01% in a_i)")

# (P2) Antusch-Maurer Table 1: start = their M_Z column, end = their 1, 3, 10 TeV columns
tabAM = {91.1876: (1.2143, 0.65184, 0.461425), 1e3: (1.0560, 0.63935, 0.467774), 3e3: (1.0017, 0.63383, 0.470767), 1e4: (0.9510, 0.62792, 0.474110)}
g3s, g2s, g1s = tabAM[91.1876]
a0m = np.array([(5.0 / 3.0) * 4 * PI / g1s ** 2, 4 * PI / g2s ** 2, 4 * PI / g3s ** 2])
print("  (P2) Antusch-Maurer arXiv:1306.6879 Table 1: start = their printed M_Z column (top NOT decoupled), end = their printed 1, 3, 10 TeV values")
print("      run                        mu(GeV)      a_Y diff %    a_2 diff %    a_3 diff %")
p2 = {}
for mu in (1e3, 3e3, 1e4):
    g3t, g2t, g1t = tabAM[mu]
    aT = np.array([(5.0 / 3.0) * 4 * PI / g1t ** 2, 4 * PI / g2t ** 2, 4 * PI / g3t ** 2])
    for lab, A in (("campaign 1-loop", camp_1loop(a0m, 91.1876, mu)), ("campaign 2-loop (N1 runner)", camp_2loop(a0m, 0.9861, 91.1876, mu))):
        d = 100 * (A / aT - 1)
        p2[f"{lab} @ {mu:.0f}"] = list(map(float, d))
        print(f"      {lab:28s} {mu:8.0f}   {d[0]:+10.4f}    {d[1]:+10.4f}    {d[2]:+10.4f}")

with open(os.path.join(HERE, "y1_3_results_MUTATE.json" if MUT else "y1_3_results.json"), "w") as f:
    json.dump(dict(scales={k: v for k, v in SCALES}, percent_vs_y1=rows, decomposition_2LT=dec, routeP_vs_routeG_at_mt=res9, XC=XC, published_start_P1=p1, published_start_P2=p2), f, indent=1)
print(f"\nY1-3: {len(fails)} failed" + (f": {fails}" if fails else ""))
if MUT:
    print("MUTATE control:", "BITES -> exit 1" if fails else "BROKEN -> exit 3")
    sys.exit(1 if fails else 3)
sys.exit(0 if not fails else 2)
