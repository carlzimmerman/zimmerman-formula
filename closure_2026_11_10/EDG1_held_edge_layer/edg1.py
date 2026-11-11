"""EDG1 (criteria f57da1f35c): held edge layer of real cold dark energy charge. E0-E4, KA1-KA4.
EDG1_MUTATE=MU1|MU2|MU3|MU4 writes edg1_MUTATE_<id>.json/.out. Inputs copied (read-only) from LFS1 lfs1_num.py
(constants, gS, Claw, Rcap, FLD1 table, FOOT X) and checked against LFS1 lfs1_num.json (KA2).
Run single-thread: OMP_NUM_THREADS=1 nice -n 19 python3 edg1.py"""
import os, json, math
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("EDG1_MUTATE", "")
tag = f"_MUTATE_{MUT}" if MUT else ""
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

# ---- copied from LFS1 lfs1_num.py (lines 20-58) ----
G = 6.674e-11; MSUN = 1.98847e30; KPC = 3.085677581e19; GYR = 3.15576e16
FOOT = {"canonical": dict(a0=9.3603e-11, X=59.486), "alt": dict(a0=1.1312e-10, X=59.503)}
FLD1 = {9.4: dict(Rta=120, inner=81), 10.45: dict(Rta=268, inner=272),
        10.7: dict(Rta=325, inner=362), 10.9: dict(Rta=378, inner=456)}
def gS(M, r, a0):
    gN = G * M / r**2
    return gN / 2 + math.sqrt(gN**2 / 4 + gN * a0)
def Claw(M, r, a0): return r**2 * (gS(M, r, a0) - G * M / r**2) / G
def Rcap(M, a0, X): return math.sqrt(G * M * X * (X + 1) / a0)
T0 = 13.8 * GYR
R = {"mutate": MUT}

# ================= KA1 (SMF1 S0b, Gauss) =================
r, Rs, w, M, Q, CR, K = sp.symbols("r R_s w M_b Q C_R K", positive=True)
Y = sp.Function("Y")                       # Y = r^2 P (opaque), regular centre Y(0) = 0
net = sp.integrate(sp.diff(Y(r), r), (r, 0, Rs))      # 4 pi Int rho_pol r^2 dr / (4 pi) with rho_pol = r^-2 d(r^2 P)/dr
net = net.subs(Y(0), 0)
boundary = 0 if MUT != "MU1" else sp.Symbol("Y_R", positive=True)   # MU1: P continued past the edge, P(R_s) != 0
ka1_res = sp.simplify(net.subs(Y(Rs), boundary))
R["KA1"] = dict(net_charge=str(ka1_res), pass_=bool(ka1_res == 0))
say(f"KA1 net polarization charge of a ball with P(R_s) = 0: {ka1_res}  -> {'PASS' if ka1_res == 0 else 'FAIL'}")

# ================= E0 books (exact) =================
Cf = sp.Function("C")                      # law's enclosed polarization charge C(r), C(R_s) = C_R
rhoQ, rhoP = Q / (4 * sp.pi * Rs**2 * w), -CR / (4 * sp.pi * Rs**2 * w)    # thin-layer densities (uniform in the layer)
if MUT == "MU4":
    Qval = sp.Rational(9, 10) * CR
else:
    Qval = Q
M_in = M + Cf(r)                           # r < R_s - w: shell theorem, the layer pulls nothing
M_out = M + CR - CR + Qval                 # r > R_s: baryons + halo + polarization layer + real layer
layer_net = sp.simplify(Qval - CR)
rho_layer = sp.simplify(rhoQ.subs(Q, Qval) + rhoP)
cond = sp.solve(sp.Ge(rho_layer, 0), Q) if MUT != "MU4" else None
g_in_edge = G * (M + CR) / Rs**2           # law's g at R_s (layer net zero when Q = C_R)
g_out_edge = G * M_out.subs(Q, CR) / Rs**2 if MUT != "MU4" else G * M_out / Rs**2
e0 = dict(M_inside=str(M_in), M_outside=str(sp.simplify(M_out)), layer_net=str(layer_net),
          layer_density=str(rho_layer), positivity_condition=str(cond),
          g_jump_at_Q_eq_C=str(sp.simplify(g_out_edge - g_in_edge)))
pos_ok = (MUT != "MU4") and sp.simplify(rho_layer.subs(Q, CR)) == 0
inside_indep = sp.diff(M_in, Q) == 0
outside_ok = sp.simplify(M_out - (M + Qval)) == 0
e0["PASS"] = bool(pos_ok and inside_indep and outside_ok)
if MUT == "MU4":
    e0["layer_density_sign_at_Q_0p9C"] = "negative (-C_R/10 per layer volume)"
R["E0"] = e0
say(f"E0 inside M_enc = {M_in} (independent of Q: {inside_indep}); outside = {sp.simplify(M_out)}; layer net = {layer_net};"
    f" layer density = {rho_layer}; >= 0 iff {cond}; g jump at R_s for Q = C_R: {e0['g_jump_at_Q_eq_C']}  -> {'PASS' if e0['PASS'] else 'FAIL'}")

# ================= E2(a) frame dust, exact sign relation =================
Phi = sp.Function("Phi"); rho = sp.Function("rho"); cs2 = sp.Function("c2")
# hydrostatics with p = p(rho): c_s^2 rho' = -rho Phi'; depth D = Phi(R_s) - Phi(r), dD/dr = -Phi'
rho_p = -rho(r) * sp.diff(Phi(r), r) / cs2(r)
dlnrho_dD = sp.simplify((rho_p / rho(r)) / (-sp.diff(Phi(r), r)))
R["E2a_sym"] = dict(dlnrho_dD=str(dlnrho_dD), residual=str(sp.simplify(dlnrho_dD - 1 / cs2(r))))
say(f"E2(a) hydrostatics: d ln rho / dD = {dlnrho_dD} (residual vs 1/c_s^2: {R['E2a_sym']['residual']}): a layer thinning with depth needs c_s^2 < 0")
k, rh, c2 = sp.symbols("k rho c2", real=True)
om2 = c2 * k**2 - 4 * sp.pi * G * rh
# C5 continued to chi < 0: omega^2 = -K n K chi/(K chi + k^2), chi = -q/K
n_, q_ = sp.symbols("n q", positive=True)
om2_c5 = sp.simplify(-K * n_ * (-q_) / (-q_ + k**2))
R["E2a_sym"]["C5_continued"] = str(om2_c5)
say(f"E2(a) plain fluid omega^2 = {om2}: negative at every k for c_s^2 < 0 (rate |c_s| k, unbounded). C5 continued to chi = -q/K: omega^2 = {om2_c5} -> -inf as k^2 -> q from below")

# ================= KA3 / E2(b) empty core =================
rng = np.random.default_rng(1)
ka3_ok = True
for trial in range(200):
    n = 50
    rr = rng.uniform(0, 1, n); gg = rng.uniform(0, 1, n); dd = rng.uniform(0, 1, n)
    if MUT == "MU2":
        gg = -gg                            # outward g (negative enclosed mass)
    p = np.concatenate([[0.0], -np.cumsum(rr * gg * dd)])
    if np.any(p > 0):
        ka3_ok = False
i_ = sp.symbols("i", integer=True); nn = sp.symbols("n", integer=True, positive=True)
a_ = sp.IndexedBase("a")                    # a_i = rho_i g_i dr_i >= 0
pn = -sp.Sum(a_[i_], (i_, 0, nn - 1))
R["KA3"] = dict(p_n=str(pn), random_trials_all_nonpositive=ka3_ok, pass_=ka3_ok)
say(f"KA3 empty core: p_n = {pn} with a_i = rho g dr >= 0 -> p_n <= 0; 200 random trials all p <= 0: {ka3_ok} -> {'PASS' if ka3_ok else 'FAIL'}")
R["E2b"] = dict(equilibrium=("NONE" if ka3_ok else "EXISTS (mutated)"),
                statement="dp/dr = -rho g, g = G M_enc/r^2 > 0 (M_enc >= M_b > 0 everywhere in the layer), p(R_s - w) = 0 -> p <= 0 -> rho = 0")

# ================= KA4 spin =================
lam_req = 1 / math.sqrt(2)
R["KA4"] = dict(lam_req=lam_req, ratio=lam_req / 0.035, pass_=(round(lam_req, 2) == 0.71 and round(lam_req / 0.035) == 20))
say(f"KA4 rotation-held shell at R_vir: lambda' = j/(sqrt2 R V) with j = R V -> {lam_req:.4f}; / 0.035 = {lam_req/0.035:.1f} -> {'PASS' if R['KA4']['pass_'] else 'FAIL'}")

# ================= E2(d) net rotation, exact =================
th, Om = sp.symbols("theta Omega", positive=True)
gsym = sp.symbols("g", positive=True)
sol = sp.solve(sp.Eq(Om**2 * Rs * sp.sin(th)**2, gsym), Om)
at_pole = sp.limit(Om**2 * Rs * sp.sin(th)**2, th, 0)
R["E2d"] = dict(radial_support=str(Om**2 * Rs * sp.sin(th)**2), support_at_pole=str(at_pole),
                Omega_needed=str(sol), equilibrium="NONE (no Omega supports theta = 0; Omega(theta) varies, so no rigid rotation)")
say(f"E2(d) radial centrifugal support on a sphere = {R['E2d']['radial_support']}; at the pole = {at_pole}; Omega needed {sol} depends on theta -> no rotation-held spherical shell")

# ================= numbers per footing =================
def vc(Mb, rr, a0): return math.sqrt(gS(Mb, rr, a0) * rr)
def fmin(Mb, Ra, Rp, a0):
    dPhi = quad(lambda x: gS(Mb, x, a0), Rp, Ra, limit=200, epsrel=1e-12)[0]
    j = math.sqrt(2 * dPhi / (1 / Rp**2 - 1 / Ra**2))
    return j / (Ra * vc(Mb, Ra, a0))
def kappa2(Mb, rr, a0):
    e = 1e-4
    f = lambda x: x**3 * gS(Mb, x, a0)
    return (f(rr * (1 + e)) - f(rr * (1 - e))) / (2 * e * rr) / rr**3
def rc_of_j(Mb, j, a0):
    return brentq(lambda x: x**3 * gS(Mb, x, a0) - j**2, 1e-3 * KPC, 1e5 * KPC)

LFS1J = json.load(open(os.path.join(HERE, "..", "LFS1_leafwise_flux_supply", "lfs1_num.json")))
printed = {"canonical": [-61.5, -40.9, -37.1, -34.3], "alt": [-67.7, -45.0, -40.9, -37.7]}
ka2_ok = True
R["F"] = {}
for foot, F in FOOT.items():
    a0, X = F["a0"], F["X"]
    say(f"\n===== {foot}: a0 = {a0}, X = {X} =====")
    rows = {}
    for idx, lm in enumerate(FLD1):
        Mb = 10**lm * MSUN
        Rta = FLD1[lm]["Rta"] * KPC; Rc = Rcap(Mb, a0, X)
        # KA2
        q_ta = -Claw(Mb, Rta, a0) / Mb; q_cap = -Claw(Mb, Rc, a0) / Mb
        ref = LFS1J["A"][foot][str(lm)]["edge"]["R_ta"]["q_edge_over_Mb"]
        ok2 = (round(q_ta, 1) == printed[foot][idx]) and abs(q_ta / ref - 1) < 1e-9 and round(q_cap, 1) == round(-X, 1)
        ka2_ok &= ok2
        row = dict(Rta_kpc=Rta / KPC, Rcap_kpc=Rc / KPC, KA2_q_ta=q_ta, KA2_q_cap=q_cap, KA2_lfs1_json=ref, KA2_ok=ok2)
        for rd, Rsv in (("R5", min(Rta, Rc)), ("U", Rta)):
            C = Claw(Mb, Rsv, a0); v = vc(Mb, Rsv, a0); wv = 0.1 * Rsv
            d = dict(R_s_kpc=Rsv / KPC, Qmin_over_Mb=C / Mb, f_of_share=C / (X * Mb), E1_pass=C / Mb <= X + 1e-12,
                     over_5p41=C / Mb / 5.41)
            # E2(a): needed c_s^2 = -g w; the C5 pole scale k* = sqrt(K|chi|), |chi| = rho_layer/(g w)
            gl = gS(Mb, Rsv, a0)
            rho_l = C / (4 * math.pi * Rsv**2 * wv)
            kstar = math.sqrt(4 * math.pi * G * rho_l / (gl * wv))
            d["E2a"] = dict(cs2_needed_kms2=-gl * wv / 1e6, kstar_Rs=kstar * Rsv,
                            growth_rate_at_k_10_over_Rs_perGyr=math.sqrt(gl * wv * (10 / Rsv)**2 + 4 * math.pi * G * rho_l) * GYR)
            # E2(c)
            sig2 = v**2 / 2; Sig = C / (4 * math.pi * Rsv**2)
            s = 2 * math.pi * G * Sig * Rsv / sig2
            lmax = [l for l in range(1, 50) if l * (l + 1) < s**2]
            k2 = kappa2(Mb, Rsv, a0); Om2 = gl / Rsv
            fm = fmin(Mb, Rsv, Rsv - wv, a0)
            Torb = 2 * math.pi * Rsv / v
            # fixed-j circular orbit as M_b grows 10 %: d ln r_c / d ln M
            j0 = Rsv * v
            dlnr = math.log(rc_of_j(1.1 * Mb, j0, a0) / Rsv) / math.log(1.1)
            d["E2c"] = dict(vc_kms=v / 1e3, inshell_s=s, s2=s**2, unstable_l=lmax, kappa2_over_Omega2=k2 / Om2,
                            fmin_peri_in_layer=fm, Torb_Gyr=Torb / GYR, Torb_over_t0=Torb / T0, dlnrc_dlnM_fixed_j=dlnr,
                            equilibrium=True, radial_stable=k2 > 0, nonradial_stable=(not [l for l in lmax if l >= 2]))
            d["E2c"]["pass"] = d["E2c"]["radial_stable"] and d["E2c"]["nonradial_stable"]
            # E3
            Rv2 = Rta / 2
            brack = {}
            for Fg in (1, 3):
                for lam in (0.035, 0.1):
                    a_s = Fg * lam * math.sqrt(2)                                    # R_vir = R_s
                    a_t = Fg * lam * math.sqrt(2) * Rv2 * vc(Mb, Rv2, a0) / (Rsv * v)  # R_vir = R_ta/2
                    if MUT == "MU3":
                        a_s = a_t = 1.0
                    brack[f"F{Fg}_lam{lam}"] = dict(avail_Rvir_Rs=a_s, avail_Rvir_Rta2=a_t,
                                                    short_Rvir_Rs=fm / a_s, short_Rvir_Rta2=fm / a_t)
            d["E3"] = dict(fmin=fm, brackets=brack, pass_=brack["F3_lam0.1"]["avail_Rvir_Rs"] >= fm,
                           lam_needed_Rvir_Rs=fm / math.sqrt(2), lam_needed_Rvir_Rta2=fm * Rsv * v / (math.sqrt(2) * Rv2 * vc(Mb, Rv2, a0)))
            # E4: R_s against KiDS inner edge; 3D mass ratio there (configuration / untruncated law)
            Rk = FLD1[lm]["inner"] * KPC
            mcfg = (Mb + Claw(Mb, Rk, a0)) if Rk <= Rsv else (Mb + C)
            d["E4"] = dict(R_s_over_kids_inner=Rsv / Rk, M3D_cfg_over_law_at_inner=mcfg / (Mb + Claw(Mb, Rk, a0)))
            row[rd] = d
        rows[str(lm)] = row
        a, b = row["R5"], row["U"]
        say(f"log M_b {lm}: R_ta {Rta/KPC:.0f}, R_cap {Rc/KPC:.1f} kpc; KA2 q(R_ta) {q_ta:.2f} (LFS1 {ref:.2f}, printed {printed[foot][idx]}), q(R_cap) {q_cap:.2f} -> {'ok' if ok2 else 'FAIL'}")
        for rd, d in (("R5", a), ("U", b)):
            c = d["E2c"]; e3 = d["E3"]
            say(f"  [{rd}] R_s {d['R_s_kpc']:.1f} kpc: E1 Q_min {d['Qmin_over_Mb']:.2f} M_b vs X {X} (f {d['f_of_share']:.3f}; {d['over_5p41']:.1f} x 5.41) -> {'pass' if d['E1_pass'] else 'FAIL'}")
            say(f"       E2(a) needs c_s^2 = {d['E2a']['cs2_needed_kms2']:.0f} (km/s)^2; C5 pole at k R_s = {d['E2a']['kstar_Rs']:.1f}; plain-fluid growth at k = 10/R_s: {d['E2a']['growth_rate_at_k_10_over_Rs_perGyr']:.2f} /Gyr")
            say(f"       E2(c) v_c {c['vc_kms']:.1f} km/s; in-shell s^2 = {c['s2']:.3f} (unstable l: {c['unstable_l']}); kappa^2/Omega^2 = {c['kappa2_over_Omega2']:.3f};"
                f" f_min = {c['fmin_peri_in_layer']:.4f}; T_orb {c['Torb_Gyr']:.1f} Gyr = {c['Torb_over_t0']:.2f} t0; fixed-j r_c ~ M^{c['dlnrc_dlnM_fixed_j']:.3f}")
            br = e3["brackets"]
            say(f"       E3 lambda' needed {e3['lam_needed_Rvir_Rs']:.3f} (R_vir = R_s) / {e3['lam_needed_Rvir_Rta2']:.3f} (R_vir = R_ta/2);"
                f" short x: F1 0.035 {br['F1_lam0.035']['short_Rvir_Rs']:.1f}/{br['F1_lam0.035']['short_Rvir_Rta2']:.1f},"
                f" F3 0.1 {br['F3_lam0.1']['short_Rvir_Rs']:.2f}/{br['F3_lam0.1']['short_Rvir_Rta2']:.2f} -> {'pass' if e3['pass_'] else 'FAIL'}")
            say(f"       E4 R_s / KiDS inner {d['E4']['R_s_over_kids_inner']:.2f}; 3D mass at the inner edge / law {d['E4']['M3D_cfg_over_law_at_inner']:.3f}")
    R["F"][foot] = rows
R["KA2"] = dict(pass_=bool(ka2_ok))
say(f"\nKA2 LFS1 A2 edge charges reproduced on both footings: {'PASS' if ka2_ok else 'FAIL'}")

json.dump(R, open(os.path.join(HERE, f"edg1{tag}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"edg1{tag}.out"), "w").write("\n".join(OUT) + "\n")
