"""AKD1 evaluation (criteria d88d310eb1): the g_c rule (KA6), the FRW background (KA3, A2), the sign of K4's A_z over
k_phys in [H/c, 1/pc] at z = 3400, 1100, 10, 2, 0 on the three readings of the law sector (R0: P held at 0; R1: law on,
unscreened, label-setting; R2: law on, screened), c_s^2 and growth rates from K4's closed forms, z_x (R = 1), brackets
(p 1, p 4, floor off), MUTATE MU1 (p -> -2) and MU2 (g_c x 100), the G-ratio, A4's weight W(r), A6(ii).
Units: lengths in Mpc, c = 1 (an acceleration g becomes g * Mpc / c^2 per Mpc). One thread.
Env AKD1_ARM = MU1 | MU2 writes separately named outputs. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math
import mpmath as mp
import sympy as sp
mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
ARM = os.environ.get("AKD1_ARM", "")
TAG = ("_MUTATE_" + ARM) if ARM else ""
out = {"arm": ARM}
lines = []
def say(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True); lines.append(s)

MPC = mp.mpf("3.0856775814913673e22"); KPC = MPC / 1000; PC = MPC / 1e6
C = mp.mpf(299792458); G = mp.mpf("6.6743e-11"); MSUN = mp.mpf("1.98841e30")
A0 = {"canonical": mp.mpf("9.3603e-11"), "alt": mp.mpf("1.1312e-10")}
XS = {"canonical": mp.mpf("59.486"), "alt": mp.mpf("59.503")}            # PD1's cap share (ONE1)
MU_KIDS = {"canonical": mp.mpf("1.00"), "alt": mp.mpf("0.765")}           # MK1 row 6, per Mpc
LSTAR = {"canonical": mp.mpf("21.7") * PC / MPC, "alt": mp.mpf("22.9") * PC / MPC}
MU_J = mp.mpf("2.512e4")
H0 = mp.mpf("67.4") / mp.mpf("299792.458")                                  # per Mpc
KD1 = json.load(open(os.path.join(HERE, "../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json")))["footings"]
FOOT = {}
for f in ("canonical", "alt"):
    s_ = KD1[f]["setting"]
    I0 = mp.mpf(s_["I0_Mpc-2"]); Od = I0 / (3 * H0**2); Ob = mp.mpf(s_["omega_b"]) / mp.mpf("0.674")**2
    Or = mp.mpf(KD1[f]["B1"]["Omega_r"])
    FOOT[f] = dict(I0=I0, Od=Od, Ob=Ob, Or=Or, OL=1 - Od - Ob - Or, mu_B1a=mp.mpf(KD1[f]["B1"]["mu_B1a"]))
MASSES = [mp.mpf("9.4"), mp.mpf("10.45"), mp.mpf("10.7"), mp.mpf("10.9")]
MID_EDGE_KPC = [190, 637, 849, 1069]     # FLD1 RESULT table, ONE1's middle KiDS window edge (canonical table)
ZS = [3400, 1100, 10, 2, 0]

def acc_to_Mpc(g):            # m/s^2 -> per Mpc (c = 1)
    return g * MPC / C**2

def law_g(gN, a0):
    return gN / 2 + mp.sqrt(gN**2 / 4 + gN * a0)

def law_g_root(gN, a0):
    return mp.findroot(lambda g: g**2 / (g + a0) - gN, law_g(gN, a0) * mp.mpf("1.3"))

PRIMARY = dict(mu0=mp.mpf(3e4), p=2, Mf=mp.mpf("1e-3"))
BRACKETS = {"p1": dict(mu0=mp.mpf(3e4), p=1, Mf=mp.mpf("1e-3")),
            "p4": dict(mu0=mp.mpf(3e4), p=4, Mf=mp.mpf("1e-3")),
            "floor_off": dict(mu0=mp.mpf(3e4), p=2, Mf=mp.mpf(0))}

def gc_rule(prm, foot, gmin):
    """largest g_c with M_2(g_min^2) <= mu_KiDS^2 (M_2 decreasing in Y): closed form."""
    ratio = prm["mu0"]**2 / (MU_KIDS[foot]**2 - prm["Mf"]**2)
    return gmin / mp.sqrt(ratio**(mp.mpf(1) / prm["p"]) - 1)

class Key:
    def __init__(self, mu0, p, Mf, gc):
        self.mu0, self.p, self.Mf, self.gc = mu0, p, Mf, gc          # per Mpc
    def M2(self, Y):
        return self.mu0**2 / (1 + Y / self.gc**2)**self.p + self.Mf**2
    def M2p(self, Y):
        return -self.p * self.mu0**2 / (self.gc**2 * (1 + Y / self.gc**2)**(self.p + 1))

# ------------------------------------------------------------------ g_min, g_c (KA6)
say("== g_min (the law's g at ONE1's middle KiDS window edge) and g_c (frozen rule)")
GMIN = {}; KA6 = []
for f in ("canonical", "alt"):
    gs = []
    for lm, rk in zip(MASSES, MID_EDGE_KPC):
        M = mp.mpf(10)**lm * MSUN; r = rk * KPC
        gN = G * M / r**2
        g1 = law_g(gN, A0[f]); g2 = law_g_root(gN, A0[f])
        KA6.append(float(abs(g1 / g2 - 1)))
        gs.append(g1)
        say("  %-9s log M_b %5s  r %4d kpc  g_N %.3e  g %.4e m/s^2 = %.4e a0" % (f, lm, rk, gN, g1, g1 / A0[f]))
    GMIN[f] = min(gs)
    say("  %-9s g_min = %.4e m/s^2 = %.4e a0" % (f, GMIN[f], GMIN[f] / A0[f]))
out["KA6_max_rel"] = max(KA6); out["KA6_pass"] = max(KA6) < 1e-12
say("  KA6 law g closed form vs root solve: max rel %.1e -> %s" % (max(KA6), "PASS" if out["KA6_pass"] else "FAIL"))

def make_key(prm, f, gc_scale=1, arm_p=None):
    gmin = acc_to_Mpc(GMIN[f])
    if arm_p is not None and arm_p < 0:
        gc = gc_rule(PRIMARY, f, gmin)            # MU1: the rule cannot be met for an increasing M_2; primary g_c kept
        k = Key(prm["mu0"], arm_p, prm["Mf"], gc)
    else:
        gc = gc_rule(prm, f, gmin) * gc_scale
        k = Key(prm["mu0"], prm["p"], prm["Mf"], gc)
    return k

# ------------------------------------------------------------------ background (KA3, A2)
def bg(f, z, M20):
    F = FOOT[f]; a = 1 / mp.mpf(1 + z)
    q0 = F["I0"] / (2 * M20 * a**3)
    On = F["Od"] / a**3
    H = H0 * mp.sqrt(F["Or"] / a**4 + (F["Ob"]) / a**3 + On + mp.mpf("0.75") * On**2 * H0**2 / M20 + F["OL"])
    return q0, H

say("== KA3 / A2: FRW limit (A = 0, so M_2 = M_2(0) = mu_0^2 + M_f^2 exactly)")
for f in ("canonical", "alt"):
    F = FOOT[f]; a = 1 / mp.mpf(3401)
    mu_b1a = mp.sqrt(99 * F["I0"] / (4 * a**3))
    rel = mu_b1a / F["mu_B1a"] - 1
    M20 = PRIMARY["mu0"]**2 + PRIMARY["Mf"]**2
    w0 = F["I0"] / (4 * M20); w3400 = w0 / (w0 + a**3)
    out.setdefault("KA3", {})[f] = dict(mu_B1a=float(mu_b1a), rel=float(rel))
    out.setdefault("A2", {})[f] = dict(w_z3400=float(w3400), mu_eff=float(mp.sqrt(M20)), mu_J=float(MU_J),
                                       ratio=float(mp.sqrt(M20) / MU_J), pass_=bool(w3400 <= 0.01 and mp.sqrt(M20) >= MU_J))
    say("  %-9s KA3 mu_B1a %.4f vs KD1 %.4f (rel %.1e);  A2 w(3400) %.3e (line 0.01), mu_eff %.4e vs mu_J %.4e (ratio %.4f): %s"
        % (f, mu_b1a, F["mu_B1a"], rel, w3400, mp.sqrt(M20), MU_J, mp.sqrt(M20) / MU_J,
           "PASS" if out["A2"][f]["pass_"] else "FAIL"))
out["KA3_pass"] = all(abs(v["rel"]) < 1e-4 for v in out["KA3"].values())

# ------------------------------------------------------------------ A1 K4 evaluation
K4J = json.load(open(os.path.join(HERE, "akd1_k4.json")))
EXPR = {nm: eval(K4J["K4_sym_" + nm], {**sp.__dict__}) for nm in ("Az", "grad")}
SY = {}
for e in EXPR.values():
    for s_ in e.free_symbols:
        SY[str(s_)] = s_
FUN = {nm: sp.lambdify([SY[n] for n in sorted(SY)], e, "mpmath") for nm, e in EXPR.items()}
ORDER = sorted(SY)

def c_law(reading, kphys, f):
    if reading == "R0":
        return mp.mpf(0)
    if reading == "R1":
        return mp.mpf(1)
    return 1 / (1 + LSTAR[f]**2 * kphys**2 / 2)

def S_of_k(key, q0, kphys, reading, f):
    """K * (FQQ Q0^2 + 2 FY k_phys^2) = M_2(0) Q0^2 + k^2 [M_2'(0) q0^2 + c_law]; sign(A_z) = sign(S)."""
    Q0 = 1 + q0
    return key.M2(0) * Q0**2 + kphys**2 * (key.M2p(0) * q0**2 + c_law(reading, kphys, f))

def k4_rates(key, f, z, kphys_list, reading):
    """growth / oscillation rates from K4's closed forms on the K4-consistent background (gravity + clock + Lambda;
    baryons folded into the clock charge, as TK1's KA5). Units H0 = 1, K = 1.5. Returns per k: (A_z, grad, rate/H)."""
    F = FOOT[f]; OL = F["OL"]; Oc = 1 - OL
    Kc = mp.mpf(1.5)
    m2 = key.M2(0) / H0**2; m2p = key.M2p(0)              # M_2'(0) is dimensionless in c = 1 per-Mpc units (mu^2/g^2)
    def bgf(a):
        On = Oc / a**3
        q = mp.mpf(1.5) * On / m2
        H = mp.sqrt(OL + On + mp.mpf(0.75) * On**2 / m2)
        return q, H
    a = 1 / mp.mpf(1 + z)
    def N0f(a_):
        q, H = bgf(a_); return 1 / (1 + q)
    def adotf(a_):
        q, H = bgf(a_); return a_ * H / (1 + q)
    q, H = bgf(a); N0 = 1 / (1 + q)
    ad = adotf(a)
    dda = lambda fn: mp.diff(fn, a)
    vals = dict(a=a, a_d=ad, a_dd=ad * dda(adotf), N0=N0, N0_d=ad * dda(N0f), K=Kc, Lambda=3 * OL)
    F0f = lambda a_: m2 * bgf(a_)[0]**2 / (2 * Kc)
    FQf = lambda a_: m2 * bgf(a_)[0] / Kc
    vals.update(F0=F0f(a), F0_d=ad * dda(F0f), FQ=FQf(a), FQ_d=ad * dda(FQf), FQQ=m2 / Kc)
    res = []
    for kp in kphys_list:
        kH0 = kp / H0                                       # physical k in H0/c units
        kc = kH0 * a                                        # comoving
        cl = c_law(reading, kp, f)
        vals["FY"] = (m2p * q**2 + cl) / (2 * Kc)
        vals["k"] = kc
        args = [vals.get(n, 0) for n in ORDER]
        Az = FUN["Az"](*args); gr = FUN["grad"](*args)
        r2 = gr / (Az * N0**2)                              # proper-time rate^2 (H0 units); < 0 means growth
        res.append((Az, gr, r2, H))
    return res

def analyse(key, f, label, z_list=ZS, verbose=True):
    rows = {}
    for z in z_list:
        q0, H = bg(f, z, key.M2(0))
        R = -key.M2p(0) * q0**2
        kmin, kmax = H, 1 / (PC / MPC)                      # [H/c, 1/pc] per Mpc
        grid = [kmin * (kmax / kmin)**(mp.mpf(i) / 399) for i in range(400)]
        per = {}
        for rd in ("R0", "R1", "R2"):
            S = [S_of_k(key, q0, kp, rd, f) for kp in grid]
            neg = [kp for kp, s_ in zip(grid, S) if s_ < 0]
            # threshold (first sign change on the grid), refined by bisection in log k
            kth = None
            for i in range(1, len(grid)):
                if (S[i - 1] > 0) != (S[i] > 0):
                    lo, hi = grid[i - 1], grid[i]
                    for _ in range(80):
                        mid = mp.sqrt(lo * hi)
                        if (S_of_k(key, q0, mid, rd, f) > 0) == (S[i - 1] > 0):
                            lo = mid
                        else:
                            hi = mid
                    kth = mp.sqrt(lo * hi); break
            if S[0] < 0:
                kth = "below H/c"
            per[rd] = dict(frac_ghost=len(neg) / len(grid), ghost=len(neg) > 0,
                           k_threshold_perMpc=(None if kth is None else (kth if isinstance(kth, str) else float(kth))),
                           k_threshold_over_H=(None if kth is None or isinstance(kth, str) else float(kth / H)),
                           eta_eff=float(2 * (c_law(rd, grid[-1], f) - R)) if rd != "R2" else None)
        rows[z] = dict(q0=float(q0), R=float(R), H_perMpc=float(H), readings=per)
        if verbose:
            say("  %-9s %-10s z %-5s q0 %.3e  R = p(mu0 q0/g_c)^2 %.3e  H %.3e/Mpc" % (f, label, z, q0, R, H))
            for rd in ("R0", "R1", "R2"):
                p_ = per[rd]
                say("      %s: ghost on %5.1f %% of [H, 1/pc]; A_z = 0 at k_phys %s per Mpc (%s x H)%s" % (
                    rd, 100 * p_["frac_ghost"],
                    ("%.3e" % p_["k_threshold_perMpc"]) if isinstance(p_["k_threshold_perMpc"], float) else p_["k_threshold_perMpc"],
                    ("%.3e" % p_["k_threshold_over_H"]) if p_["k_threshold_over_H"] is not None else "-",
                    ("; eta_eff %.3e" % p_["eta_eff"]) if p_["eta_eff"] is not None else ""))
    return rows

def z_cross(key, f):
    """z where R = 1 (R1's ghost switches off below it): R propto (1+z)^6."""
    q0_today, _ = bg(f, 0, key.M2(0))
    R0_ = -key.M2p(0) * q0_today**2
    if R0_ <= 0:
        return None
    return float((1 / R0_)**(mp.mpf(1) / 6) - 1)

def a1_label(rows):
    bad = [(z, "R1") for z, r in rows.items() if r["readings"]["R1"]["ghost"]]
    return ("WELL-POSED AROUND FRW" if not bad else "NOT WELL-POSED AROUND FRW"), bad


if os.environ.get("AKD1_EXTRA") == "1":
    # POST-FREEZE REPORTED READINGS (disclosed in RESULT.md; label-setting nothing):
    # (a) K4 growth rates on R1 just above z_x, where the zero of A_z is inside the horizon;
    # (b) the g_c rule with the law's g in the PD1-capped well (the frozen rule used the uncapped law g).
    ex = {}
    for f in ("canonical", "alt"):
        key = make_key(PRIMARY, f)
        zx = z_cross(key, f)
        zl = [(1 + zx) * mp.mpf(1.5)**(mp.mpf(i) / 14) - 1 for i in range(1, 29)]   # 1+z from 1.03 to 2.25 x (1+z_x)
        rowsx = []
        for z in zl:
            q0, H = bg(f, z, key.M2(0)); R = -key.M2p(0) * q0**2
            kth = mp.sqrt(key.M2(0) * (1 + q0)**2 / (R - 1))
            # K4's own background (gravity + clock + Lambda, all matter in the clock): its q and its zero of A_z
            aa = 1 / mp.mpf(1 + z); qK = mp.mpf(1.5) * H0**2 * (1 - FOOT[f]["OL"]) / aa**3 / key.M2(0)
            RK = -key.M2p(0) * qK**2
            kth = mp.sqrt(key.M2(0) * (1 + qK)**2 / (RK - 1))
            ks = [kth * mp.mpf(fc) for fc in ("1.0001", "1.01", "1.1", "2", "10", "1e3")]
            ks = [kp for kp in ks if kp <= 1 / (PC / MPC)]
            res = k4_rates(key, f, z, ks, "R1")
            rates = [float(mp.sqrt(-r2) / Hh) for (Az, gr, r2, Hh) in res if r2 < 0]
            rowsx.append(dict(z=float(z), R=float(R), kth_over_H=float(kth / H), kth_pc=float(1 / kth * MPC / PC),
                              growth_rate_over_H=rates))
            say("  extra(a) %-9s z %7.3f R %.3e  (K4 background: zero of A_z at k_th = %.3e H (1/k_th = %.3g pc); growth/H at k/k_th 1.0001, 1.01, 1.1, 2, 10, 1e3 (<= 1/pc): %s"
                % (f, z, R, kth / H, 1 / kth * MPC / PC, ["%.2e" % v for v in rates]))
        ex.setdefault("a_rates_above_zx", {})[f] = rowsx
        # (b) capped g_min
        gs = []
        for lm, rk in zip(MASSES, MID_EDGE_KPC):
            M = mp.mpf(10)**lm * MSUN; r = rk * KPC
            rM = mp.sqrt(G * M / A0[f]); Rcap = mp.sqrt(XS[f] * (XS[f] + 1)) * rM
            gs.append(law_g(G * M / r**2, A0[f]) if r < Rcap else G * M * (1 + XS[f]) / r**2)
        gmc = min(gs)
        gcc = gc_rule(PRIMARY, f, acc_to_Mpc(gmc))
        kb = Key(PRIMARY["mu0"], PRIMARY["p"], PRIMARY["Mf"], gcc)
        rows = analyse(kb, f, "capped_gmin", verbose=False)
        lab, bad = a1_label(rows)
        ex.setdefault("b_capped_gmin", {})[f] = dict(g_min_capped=float(gmc), g_c_ms2=float(gcc * C**2 / MPC),
                                                     g_c_over_a0=float(gcc * C**2 / MPC / A0[f]), label=lab,
                                                     ghost_on_R1_at=[z for z, _ in bad], z_x=z_cross(kb, f))
        say("  extra(b) %-9s capped g_min %.4e m/s^2 -> g_c %.4e a0: %s, ghost on R1 at z %s, z_x %.2f" % (
            f, gmc, gcc * C**2 / MPC / A0[f], lab, [z for z, _ in bad], z_cross(kb, f)))
        # W inside the windows with the capped g_c
        for lm, redge in zip(MASSES, MID_EDGE_KPC):
            M = mp.mpf(10)**lm * MSUN; a0 = A0[f]; xs = XS[f]
            rM = mp.sqrt(G * M / a0); Rcap = mp.sqrt(xs * (xs + 1)) * rM
            def g_of(r):
                return law_g(G * M / r**2, a0) if r < Rcap else G * M * (1 + xs) / r**2
            def Phi(r):
                return -G * M * (1 + xs) / r if r >= Rcap else -G * M * (1 + xs) / Rcap - mp.quad(g_of, [r, Rcap])
            rs = [10 * KPC * (mp.mpf(redge) / 10)**(mp.mpf(i) / 80) for i in range(81)]
            Wv = [abs(kb.M2p(acc_to_Mpc(g_of(r))**2)) * (abs(Phi(r)) / C**2)**2 * (1 + g_of(r) / a0) for r in rs]
            first = next((r for r, w in zip(rs, Wv) if w > 1), None)
            ex["b_capped_gmin"][f]["W_max_inside_%s" % lm] = float(max(Wv))
            say("  extra(b) %-9s log M_b %5s: max W inside the middle window %.3e%s" % (
                f, lm, max(Wv), ("; W > 1 from %.0f kpc" % (first / KPC)) if first is not None else ""))
    json.dump(dict(extra=ex, lines=lines), open(os.path.join(HERE, "akd1_extra.json"), "w"), indent=1, default=str)
    sys.exit(0)

ARMS = {"": ("primary", PRIMARY, None, 1)}
if ARM == "MU1":
    ARMS = {"MU1": ("MU1_p_minus2", PRIMARY, -2, 1)}
elif ARM == "MU2":
    ARMS = {"MU2": ("MU2_gc_x100", PRIMARY, None, 100)}

say("== A1: sign of A_z over k_phys in [H/c, 1/pc] (A_z propto M_2(0) Q0^2 + k^2 [M_2'(0) q0^2 + c_law])")
for arm, (label, prm, arm_p, gscale) in ARMS.items():
    for f in ("canonical", "alt"):
        key = make_key(prm, f, gc_scale=gscale, arm_p=arm_p)
        gc_ms2 = key.gc * C**2 / MPC
        say("  %-9s %s: g_c = %.4e m/s^2 = %.4e a0 ;  M_2(g_min^2)^(1/2) = %.4f per Mpc (line %.3f);  M_2'(0) = %.4e"
            % (f, label, gc_ms2, gc_ms2 / A0[f], mp.sqrt(key.M2(acc_to_Mpc(GMIN[f])**2)), MU_KIDS[f], key.M2p(0)))
        rows = analyse(key, f, label)
        lab, bad = a1_label(rows)
        zx = z_cross(key, f)
        out.setdefault("A1", {}).setdefault(label, {})[f] = dict(g_c_ms2=float(gc_ms2), g_c_over_a0=float(gc_ms2 / A0[f]),
                                                               rows={str(z): r for z, r in rows.items()}, label=lab,
                                                               ghost_on_R1_at=[z for z, _ in bad], z_x_R_equals_1=zx)
        say("  %-9s %s: A1 reading on R1 = %s (ghost at z %s); R = 1 at z_x = %s" % (f, label, lab, [z for z, _ in bad],
                                                                                  ("%.2f" % zx) if zx is not None else "never"))
        # fine z grid: where is R1 ghost-free?
        zg = [mp.mpf(3401)**(mp.mpf(i) / 139) - 1 for i in range(140)]
        fine = analyse(key, f, label, z_list=zg, verbose=False)
        gh = [float(z) for z, r in fine.items() if r["readings"]["R1"]["ghost"]]
        out["A1"][label][f]["R1_ghost_z_range_fine_grid"] = [min(gh), max(gh)] if gh else None
        out["A1"][label][f]["R0_ghost_all_fine_z"] = all(r["readings"]["R0"]["ghost"] for r in fine.values())
        say("  %-9s %s: 140-point z grid: R1 ghost for z in %s; R0 ghost at every z: %s" % (
            f, label, out["A1"][label][f]["R1_ghost_z_range_fine_grid"], out["A1"][label][f]["R0_ghost_all_fine_z"]))
        # rates from K4's closed forms (K4-consistent background), R1 and R0, three k per z
        if arm == "":
            rt = {}
            for z in ZS:
                q0, H = bg(f, z, key.M2(0))
                R = -key.M2p(0) * q0**2
                ks = [10 * H, 1e3 * H, 1 / (PC / MPC)]
                for rd in ("R1", "R0"):
                    res = k4_rates(key, f, z, ks, rd)
                    txt = []
                    for kp, (Az, gr, r2, Hh) in zip(ks, res):
                        rate_over_H = mp.sqrt(abs(r2)) / Hh
                        cs2 = r2 / (kp / H0)**2
                        txt.append(dict(k_over_H=float(kp / H), Az_sign=int(mp.sign(Az)), grad_sign=int(mp.sign(gr)),
                                        omega2_sign=int(mp.sign(r2)), rate_over_H=float(rate_over_H), cs2=float(cs2)))
                    rt["z%s_%s" % (z, rd)] = txt
                    say("      rates z %-5s %s: " % (z, rd) + "; ".join(
                        "k %.0e H: A_z %+d grad %+d omega^2 %+d |rate|/H %.2e c_s^2 %+.2e" % (
                            t_["k_over_H"], t_["Az_sign"], t_["grad_sign"], t_["omega2_sign"], t_["rate_over_H"], t_["cs2"])
                        for t_ in txt))
            out["A1"][label][f]["rates_K4"] = rt
            # closed-form growth near the threshold (R1, z 1100): rate^2 = B k^2/|I(k)| diverges as I -> 0
            q0, H = bg(f, 1100, key.M2(0)); R = -key.M2p(0) * q0**2
            kth = mp.sqrt(key.M2(0) * (1 + q0)**2 / (R - 1))
            Bk = key.M2(0) * q0 * (1 + q0)                 # K*(2B) = M_2 q0 Q0 -> rate^2 = K Q n ... in decoupling form
            near = []
            for fac in ("1.1", "1.01", "1.0001"):
                kp = kth * mp.mpf(fac)
                I = key.M2(0) * (1 + q0)**2 + kp**2 * (key.M2p(0) * q0**2 + 1)
                near.append(float(mp.sqrt(Bk * kp**2 / abs(I)) / H))
            out["A1"][label][f]["decoupling_rate_over_H_near_threshold_z1100_R1"] = dict(k_over_kth=["1.1", "1.01", "1.0001"], rate_over_H=near)
            say("      decoupling rate/H just above the z 1100 threshold (R1), k/k_th 1.1 / 1.01 / 1.0001: %s" % ["%.2e" % v for v in near])

if ARM == "":
    say("== brackets (reported): p 1, p 4, floor off; g_c re-fixed by the rule")
    for nm, prm in BRACKETS.items():
        for f in ("canonical", "alt"):
            key = make_key(prm, f)
            rows = analyse(key, f, nm, verbose=False)
            lab, bad = a1_label(rows)
            out.setdefault("brackets", {}).setdefault(nm, {})[f] = dict(
                g_c_over_a0=float(key.gc * C**2 / MPC / A0[f]), label=lab, ghost_on_R1_at=[z for z, _ in bad],
                R={str(z): r["R"] for z, r in rows.items()}, z_x=z_cross(key, f),
                R1_kth_over_H={str(z): r["readings"]["R1"]["k_threshold_over_H"] for z, r in rows.items()})
            say("  %-9s %-9s g_c %.3e a0: %s, ghost on R1 at z %s, z_x %s; R(3400) %.2e R(0) %.2e" % (
                f, nm, key.gc * C**2 / MPC / A0[f], lab, [z for z, _ in bad],
                ("%.2f" % z_cross(key, f)) if z_cross(key, f) is not None else "never", rows[3400]["R"], rows[0]["R"]))

    # ---------------------------------------------------------------- G ratio (closed form) and A6(ii)
    out["G_ratio"] = ("G_cosmo / G_N = 1 exactly at linear order: on FRW A = 0, so rho_K at fixed charge is MK1's "
                      "(no H dependence); around Q = 1 the Y-term's coefficient M_2'(Y) (Q-1)^2 vanishes at linear order. "
                      "The Horava-like coefficient eta_eff = 4 K F_Y,tot = 2 (c_law - R) is printed per reading above.")
    say("== G-ratio:", out["G_ratio"])
    say("== A6(ii): leaving the stiff branch, A = K |grad n| / M_2(0) > g_c")
    for f in ("canonical", "alt"):
        key = make_key(PRIMARY, f)
        Kn0 = FOOT[f]["I0"] / 2                            # K * mean clock charge today, per Mpc^2
        L3 = 3 * KPC / MPC
        delta = key.M2(0) * key.gc * L3 / Kn0
        out.setdefault("A6ii", {})[f] = dict(overdensity_over_3kpc=float(delta))
        say("  %-9s needed |grad n| = M_2(0) g_c / K: an overdensity of %.3e x today's mean clock charge over 3 kpc" % (f, delta))

    # ---------------------------------------------------------------- A4 weight W(r) (reported)
    say("== A4 / A6(i): weight W = |M_2'(g^2)| q^2 (1+u) around MK1's four masses (PD1-capped potential, zero at infinity)")
    for f in ("canonical", "alt"):
        key = make_key(PRIMARY, f)
        a0 = A0[f]; xs = XS[f]
        for lm, redge in zip(MASSES, MID_EDGE_KPC):
            M = mp.mpf(10)**lm * MSUN
            rM = mp.sqrt(G * M / a0); Rcap = mp.sqrt(xs * (xs + 1)) * rM
            def g_of(r):
                return law_g(G * M / r**2, a0) if r < Rcap else G * M * (1 + xs) / r**2
            Phi_cap = -G * M * (1 + xs) / Rcap
            def Phi(r):
                if r >= Rcap:
                    return -G * M * (1 + xs) / r
                return Phi_cap - mp.quad(g_of, [r, Rcap])
            def W(r):
                g = g_of(r); q = abs(Phi(r)) / C**2; gl = acc_to_Mpc(g)
                return abs(key.M2p(gl**2)) * q**2 * (1 + g / a0)
            rs = [10 * KPC * (mp.mpf(30) * redge / 10)**(mp.mpf(i) / 120) for i in range(121)]   # 10 kpc to 30 x edge
            Ws = [W(r) for r in rs]
            first = next((r for r, w in zip(rs, Ws) if w > 1), None)
            Wedge = W(redge * KPC)
            Wmax_in = max(w for r, w in zip(rs, Ws) if r <= redge * KPC)
            out.setdefault("A4_W", {}).setdefault(f, {})[str(lm)] = dict(
                R_cap_kpc=float(Rcap / KPC), W_at_middle_edge=float(Wedge), W_max_inside_window=float(Wmax_in),
                r_W_gt_1_kpc=(float(first / KPC) if first is not None else None), middle_edge_kpc=redge,
                W_max_to_30x_edge=float(max(Ws)))
            say("  %-9s log M_b %5s: R_cap %.0f kpc; W at middle edge (%d kpc) %.3e; max W inside the window %.3e; "
                "W > 1 first at %s; max W out to 30x edge %.3e" % (
                    f, lm, Rcap / KPC, redge, Wedge, Wmax_in,
                    ("%.0f kpc" % (first / KPC)) if first is not None else "nowhere to 30x edge", max(Ws)))
        # Saturn line
        gS = G * MSUN / (mp.mpf("9.5826") * mp.mpf("1.495978707e11"))**2
        mS = mp.sqrt(key.M2(acc_to_Mpc(gS)**2))
        out.setdefault("A4_saturn", {})[f] = dict(mu_eff=float(mS), line=6.22e3, pass_=bool(mS <= 6.22e3))
        say("  %-9s Saturn: mu_eff %.3e per Mpc vs 6.22e3: %s" % (f, mS, "PASS" if mS <= 6.22e3 else "FAIL"))
    # class bound (any decreasing M_2 meeting both lines; Newtonian outskirts q^2 propto sqrt(Y))
    for f in ("canonical", "alt"):
        lm, redge = MASSES[2], MID_EDGE_KPC[2]
        M = mp.mpf(10)**lm * MSUN; a0 = A0[f]; xs = XS[f]
        q_edge = G * M * (1 + xs) / (redge * KPC) / C**2
        gmin = acc_to_Mpc(GMIN[f])
        bound = (MU_J**2 - MU_KIDS[f]**2) * q_edge**2 / (2 * gmin**2)
        out.setdefault("class_bound", {})[f] = float(bound)
        say("  %-9s class bound: any M_2 falling from mu_J^2 at Y = 0 to mu_KiDS^2 at g_min^2 has W >= %.3e somewhere at or "
            "beyond the middle edge (log M_b 10.7, Newtonian outskirts, q^2 propto sqrt(Y))" % (f, bound))

out["lines"] = lines
json.dump(out, open(os.path.join(HERE, "akd1_eval%s.json" % TAG), "w"), indent=1, default=str)
