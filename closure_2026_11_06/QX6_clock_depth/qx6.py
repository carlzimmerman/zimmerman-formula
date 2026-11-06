#!/usr/bin/env python3
"""QX6 (criteria 3edba4879f): derive QX5's clock-depth boost F(Q-1) from the action, no cluster input.
    python3 qx6.py            # graded: qx6.json / qx6.out
    python3 qx6.py --mutate   # power controls of iter 1-3: qx6_MUTATE.json / .out
QX5's samples and key-a construction are reused by executing qx5.py's own source up to its class loop.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; TAG = "qx6_MUTATE" if MUT else "qx6"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

# ---- reuse QX5 machinery (samples, key a, tables, stats) ----
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
exec(compile(src[:cut], Q5, "exec"), NS); sys.argv = argv0
G, MS, KPC, C, A0, glaw, XC, SP, tables, phi_from = (NS[k] for k in ("G", "MS", "KPC", "C", "A0", "glaw", "XC", "SP", "tables", "phi_from"))
MPC = 1e3 * KPC
LSTAR = {"canonical": 21.7 * KPC / 1e3, "alt": 22.9 * KPC / 1e3}
R5J = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))
_Q5J = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.json")))
FREQ_MED = {f: _Q5J["a"][f]["XCOP_F_required"]["median"] for f in ("canonical", "alt")}
FREQ_MIN = {f: _Q5J["a"][f]["XCOP_F_required"]["min"] for f in ("canonical", "alt")}
RES = dict(tag=TAG, criteria="3edba4879f", note="kappa = 1/2 FITTED; not theory closed")

def gx(d): return bool(abs(d.mean()) <= 0.05 and np.sqrt((d ** 2).mean()) <= 0.10)
def mr(d): return float(d.mean()), float(np.sqrt((d ** 2).mean()))

# ================= iter 1: K(Q) sector on its own static equation =================
def psi_profile(z, name, zero_mult):
    r = np.asarray(z["hr"], float); M = np.asarray(z["hM"], float)
    R200 = 1e3 * R5J[name]["R200"] if name in R5J else 1.5 * 1e3 * 0.7  # all X-COP clusters are in R5J (checked below)
    rr = np.geomspace(1.0, zero_mult * R200, 4000)
    lr, lm = np.log10(r), np.log10(M); sl = (lm[-1] - lm[-6]) / (lr[-1] - lr[-6])
    Mr = np.where(rr <= r[-1], 10 ** np.interp(np.log10(rr), lr, lm), M[-1] * (rr / r[-1]) ** sl)
    Mr = np.where(rr < r[0], M[0] * (rr / r[0]) ** 3, Mr)
    gacc = G * Mr * MS / (rr * KPC) ** 2
    seg = 0.5 * (gacc[1:] + gacc[:-1]) * np.diff(rr * KPC)
    psi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (np.abs(psi[1:]) * (rr[1:] * KPC) ** 2 + np.abs(psi[:-1]) * (rr[:-1] * KPC) ** 2) * np.diff(rr * KPC))])
    return rr, integ, psi

assert all(z["name"] in R5J for z in XC), "R200 missing for an X-COP cluster"
IK = {zm: [psi_profile(z, z["name"], zm) for z in XC] for zm in (3, 10)}
def MK_x(i, mu_mpc, zm):
    rr, integ, _ = IK[zm][i]; mu = mu_mpc / MPC
    return mu ** 2 / G * float(np.interp(XC[i]["r_kpc"], rr, integ)) / MS
def mlaw(Mb, r_kpc, a0):
    rm = r_kpc * KPC; return glaw(G * Mb * MS / rm ** 2, a0) * rm ** 2 / G / MS
MOBS_PLANT = {}
def xcop_d(a0, mu, zm, f):
    out = []
    for i, z in enumerate(XC):
        Mo = MOBS_PLANT[f][i] if MUT else z["M_obs"]
        out.append(math.log10(Mo / (mlaw(z["M_b"], z["r_kpc"], a0) + MK_x(i, mu, zm))))
    return np.array(out)

def sparc_d(a0, mu):  # g_model = g_law + G M_K(<r)/r^2, psi from key a (QX5 construction, cosmic-clock zero)
    out = []; mu_ = mu / MPC
    for g in SP:
        r, V = g["R"], g["V"]; gobs = V ** 2 / r; gbar = g["vb2"] / r; gl = glaw(gbar, a0); Mb_last = g["vb2"][-1] * r[-1] / G
        psi = np.array([phi_from(r, gobs, i, Mb_last, a0) for i in range(len(r))])
        f_ = psi * r ** 2; cum = np.concatenate([[psi[0] * r[0] ** 3 / 3], psi[0] * r[0] ** 3 / 3 + np.cumsum(0.5 * (f_[1:] + f_[:-1]) * np.diff(r))])
        gK = mu_ ** 2 * cum / r ** 2
        out += list(np.log10(gobs / (gl + gK)))
    return np.array(out)

MU_GRID = 10 ** np.arange(-3, 4.0001, 0.01)
R1 = {}
for f, a0 in A0.items():
    if MUT: MOBS_PLANT[f] = [mlaw(z["M_b"], z["r_kpc"], a0) + MK_x(i, 1.0, 3) for i, z in enumerate(XC)]
    R1[f] = {}
    for zm in (3, 10):
        stats = [(mu, *mr(dd), gx(dd)) for mu in MU_GRID for dd in [xcop_d(a0, mu, zm, f)]]
        passing = [s[0] for s in stats if s[3]]
        best_rms = min(stats, key=lambda s: s[2]); best_mean = min(stats, key=lambda s: abs(s[1]))
        R1[f][f"zero_{zm}R200"] = dict(pass_interval=[min(passing), max(passing)] if passing else None, n_pass=len(passing),
                                     min_rms=dict(mu=best_rms[0], mean=best_rms[1], rms=best_rms[2]),
                                     mean0=dict(mu=best_mean[0], mean=best_mean[1], rms=best_mean[2]),
                                     at_S4_0p1=dict(zip(("mean", "rms"), mr(xcop_d(a0, 0.1, zm, f)))))
        s = R1[f][f"zero_{zm}R200"]
        P(f"[iter1 {f} psi=0 at {zm} R200] passing mu_K interval: {s['pass_interval']} ({s['n_pass']} grid pts); "
          f"min rms {s['min_rms']['rms']:.3f} at mu {s['min_rms']['mu']:.3g} (mean {s['min_rms']['mean']:+.3f}); "
          f"mean 0 at mu {s['mean0']['mu']:.3g} (rms {s['mean0']['rms']:.3f}); at S4 0.1: {s['at_S4_0p1']['mean']:+.3f}/{s['at_S4_0p1']['rms']:.3f}")
    # SPARC at the cluster-favoured mu (mean-0 point, graded footing zero 3 R200) and at the S4 bound
    base = sparc_d(a0, 0.0)
    for tag, mu in (("S4_0.1", 0.1), ("cluster_mean0", R1[f]["zero_3R200"]["mean0"]["mu"])):
        d = sparc_d(a0, mu); R1[f][f"SPARC_{tag}"] = dict(mu=mu, d_mean=float(d.mean() - base.mean()), d_rms=float(np.sqrt((d ** 2).mean()) - np.sqrt((base ** 2).mean())))
        P(f"[iter1 {f}] SPARC at mu {mu:.3g}: mean shift {R1[f][f'SPARC_{tag}']['d_mean']:+.4f}, rms shift {R1[f][f'SPARC_{tag}']['d_rms']:+.4f} (lines 0.02 / 0.01)")
    # Sun at 1 AU, largest mu in any passing interval (or the mean-0 mu if none)
    pi_ = R1[f]["zero_3R200"]["pass_interval"]; mu_s = (pi_[1] if pi_ else R1[f]["zero_3R200"]["mean0"]["mu"]) / MPC
    psi_s = (1e-6 + 1e-8) * C ** 2; AU = 1.496e11; gK = mu_s ** 2 * psi_s * AU / 3; gN = 5.93e-3
    R1[f]["Sun"] = dict(mu=mu_s * MPC, gK_1AU=gK, ratio_gN=gK / gN); P(f"[iter1 {f}] Sun: g_K(1 AU) = {gK:.3e} m/s^2 = {gK / gN:.3e} g_N at mu {mu_s * MPC:.3g}")
    # window vs record bounds
    ok_any = any(R1[f][k]["pass_interval"] for k in ("zero_3R200",))
    if ok_any:
        lo, hi = R1[f]["zero_3R200"]["pass_interval"]
        R1[f]["E2"] = dict(S4=bool(lo <= 0.1), QX3_mu_max=bool(lo <= 79.0), CMB=bool(hi >= 3.98e4))
    lab = "DEAD (no mu_K passes G-X)" if not ok_any else ("DERIVED-PASS candidate" if R1[f]["E2"]["S4"] and R1[f]["E2"]["QX3_mu_max"] else "FAIL (passing mu_K violates the galaxy bound)")
    if ok_any and R1[f]["E2"]["S4"] and not R1[f]["E2"]["CMB"]: lab += "; CMB-CONFLICT"
    R1[f]["label"] = lab; P(f"[iter1 {f}] LABEL: {lab}")
RES["iter1"] = R1

# ================= iter 2: a0 tied to khronon-frame rho_DE =================
R2 = {}
for f, a0 in A0.items():
    T = tables("a", a0, False); amp = 2.1e4 if MUT else 2.1
    d0 = np.array([math.log10(z["M_obs"] / mlaw(z["M_b"], z["r_kpc"], a0)) for z in XC])
    d = np.array([math.log10(z["M_obs"] / mlaw(z["M_b"], z["r_kpc"], a0 * (1 + amp * x["k"]))) for z, x in zip(XC, T["X"])])
    kmax = max(x["k"] for x in T["X"]); Fm1 = amp * kmax
    R2[f] = dict(mean=mr(d)[0], rms=mr(d)[1], shift=float(d.mean() - d0.mean()), max_F_minus_1=Fm1, factor_short=(FREQ_MIN[f] - 1) / Fm1,
                 label="DEAD" if not gx(d) else "passes G-X")
    P(f"[iter2 {f}] a0 -> a0(1+{amp:g} k): X-COP mean {R2[f]['mean']:+.4f} rms {R2[f]['rms']:.4f} (shift {R2[f]['shift']:+.2e}); "
      f"max F-1 {Fm1:.2e} vs needed >= {FREQ_MIN[f] - 1:.2f} (short x{R2[f]['factor_short']:.2e}) -> {R2[f]['label']}")
RES["iter2"] = R2

# ================= iter 3: native-threshold window =================
COMA = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "iter_a2_member_galaxies", "qx5_a2.json")))
def coma_z(f, F):
    c = COMA[f]; sig = c["F1"]["meanE"] / c["F1"]["z"]
    m = float(np.mean([p["E_v3"] - math.log(p["rN"] + F * (1 - p["rN"])) for p in c["per"]])); return m / sig
R3 = {}
for f, a0 in A0.items():
    T = tables("a", a0, False)
    kg = max([c["k"] for c in T["C"]] + [e["k"] for e in T["E"]] + [l["k"] for l in T["L"]]); kx = min(x["k"] for x in T["X"])
    Ls = LSTAR[f]; grp = {"G1 a0 Lstar/c^2": a0 * Ls / C ** 2}
    for mu in (0.1, 79.0, 3.98e4):
        grp[f"G2 a0/(c^2 mu_K) mu={mu:g}"] = a0 / (C ** 2 * mu / MPC); grp[f"G3 mu_K Lstar mu={mu:g}"] = mu / MPC * Ls
    for nm, v in (("kappa", 0.5), ("2pi", 2 * math.pi), ("Z", 5.7888)):
        grp[nm] = v; grp["1/" + nm] = 1 / v
    hits, trials = [], 0
    for nm, v in grp.items():
        for p in (1, 0.5, 1 / 3, 0.25, 2):
            kt = v ** p; trials += 1
            if kg < kt < kx: hits.append(dict(group=nm, p=p, k_t=kt))
    def step_eval(kt, A):
        F = lambda k: np.where(np.asarray(k) >= kt, A, 1.0)
        xd = np.array([math.log10(x["M_obs"] / (x["M_b"] + F(x["k"]) * (x["M_law"] - x["M_b"]))) for x in T["X"]])
        gm = {}
        for fst in (0.0, 1.0):
            v_ = np.array([math.log10(g["M_obs"] / (g["M_b"] + F(g["k"]) * (g["M_law"] - g["M_b"]))) for g in T["G"] if g["fst"] == fst]); gm[fst] = float(v_.mean())
        lo, hi = sorted(gm.values()); kmax_cal = kg
        return dict(X_mean=mr(xd)[0], X_rms=mr(xd)[1], GX=gx(xd), groups=[gm[0.0], gm[1.0]], groups_pass=bool(lo <= 0.05 and hi >= -0.05),
                    galaxies_untouched=bool(kmax_cal < kt), coma_z=coma_z(f, A))
    if MUT:
        kt = math.sqrt(kg * kx); R3[f] = dict(mutate_A=step_eval(kt, FREQ_MED[f]), mutate_A1=step_eval(kt, 1.0), k_t=kt)
        P(f"[iter3 MUTATE {f}] step at sqrt(kg kx) = {kt:.3e}: A={FREQ_MED[f]:.2f} G-X {R3[f]['mutate_A']['GX']} "
          f"({R3[f]['mutate_A']['X_mean']:+.3f}/{R3[f]['mutate_A']['X_rms']:.3f}); A=1 G-X {R3[f]['mutate_A1']['GX']}")
        continue
    for h in hits: h.update(step_eval(h["k_t"], FREQ_MED[f]))
    R3[f] = dict(k_g=kg, k_x=kx, trials=trials, hits=hits, n_hits=len(hits),
                 label="DEAD (action on the table: no Q-step; see README occurrence list)" + (f"; {len(hits)} COINCIDENCE(s), CLUSTER-SET amplitude" if hits else ""))
    P(f"[iter3 {f}] window W = ({kg:.3e}, {kx:.3e}); trials {trials}; hits {len(hits)}")
    for h in hits:
        P(f"   COINCIDENCE {h['group']} ^{h['p']:.3g} = {h['k_t']:.3e}: step A={FREQ_MED[f]:.2f} (CLUSTER-SET) X-COP {h['X_mean']:+.3f}/{h['X_rms']:.3f} "
          f"G-X {h['GX']}; groups {h['groups'][0]:+.3f}/{h['groups'][1]:+.3f} pass {h['groups_pass']}; galaxies untouched {h['galaxies_untouched']}; Coma UDG z {h['coma_z']:.2f}")
RES["iter3"] = R3

if MUT:
    bite1 = all(R1[f]["zero_3R200"]["pass_interval"] is not None and R1[f]["zero_3R200"]["pass_interval"][0] <= 1.0 <= R1[f]["zero_3R200"]["pass_interval"][1] for f in A0)
    bite2 = all(R2[f]["shift"] <= -0.2 for f in A0)
    bite3 = all(R3[f]["mutate_A"]["GX"] and not R3[f]["mutate_A1"]["GX"] for f in A0)
    RES["bites"] = dict(iter1=bite1, iter2=bite2, iter3=bite3); P(f"MUTATE bites: iter1 {bite1}, iter2 {bite2}, iter3 {bite3}")
else:
    derived = any("DERIVED-PASS" in R1[f]["label"] for f in A0)
    RES["door"] = "Clusters FAIL: no route derives F(Q-1) from the action" if not derived else "a derived candidate: later gates owed"
    P(f"DOOR: {RES['door']}")
json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
