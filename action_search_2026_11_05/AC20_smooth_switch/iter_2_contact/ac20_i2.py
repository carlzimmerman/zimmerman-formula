#!/usr/bin/env python3
"""AC20 iter_2: contact form F = (gamma/2) Pi_+^4/(Pi_+ + a)^2, a = s^2 (criteria iter_2_contact/FROZEN_CRITERIA.md).
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC20_smooth_switch/iter_2_contact/ac20_i2.py
MUTATE (AC20_MUTATE=1): v3s's F (exponent 2, a = 0) through C-c; it must FAIL. Outputs ac20_i2[_MUTATE].json/.out.
kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, itertools
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from harness import ladder

MUT = os.environ.get("AC20_MUTATE") == "1"
tag = "ac20_i2_MUTATE" if MUT else "ac20_i2"
ok, res = {}, {}

# ---------------- C-a, C-b: sympy ----------------
Q, a, g, u = sp.symbols("Pi a gamma u", positive=True)
F = g / 2 * Q ** 4 / (Q + a) ** 2
Fp = sp.simplify(sp.diff(F, Q)); Fpp = sp.simplify(sp.diff(F, Q, 2))
ok["Ca_Fp"] = sp.simplify(Fp - g * Q ** 3 * (Q + 2 * a) / (Q + a) ** 3) == 0
fprime_u = u ** 2 * (u ** 2 + 4 * u + 6) / (u + 1) ** 4
ok["Ca_Fpp"] = sp.simplify(Fpp - g * fprime_u.subs(u, Q / a)) == 0
ok["Ca_Fpp_limit"] = sp.limit(Fpp, Q, sp.oo) == g
ok["Ca_c2_nonneg"] = all(t >= 0 for t in sp.Poly(sp.expand(u ** 2 * (u ** 2 + 4 * u + 6)), u).coeffs())
dev = sp.factor(sp.simplify(g * Q - Fp))
ok["Cb_dev_form"] = sp.simplify(dev - g * a * Q * (Q ** 2 + 3 * a * Q + a ** 2) / (Q + a) ** 3) == 0
ok["Cb_dev_le_ga"] = all(t >= 0 for t in sp.Poly(sp.expand((Q + a) ** 3 - Q * (Q ** 2 + 3 * a * Q + a ** 2)), Q, a).coeffs())
res["C_ab"] = dict(Fp=str(Fp), Fpp=str(Fpp), deviation=str(dev))
# C-c analytic: near 0, w ~ Pi^(3/2)
w_near = sp.integrate(sp.sqrt(sp.series(Fpp / Q, Q, 0, 2).removeO()), (Q, 0, Q))
res["w_near_zero_leading"] = str(sp.simplify(w_near))

# ---------------- C-c: numerics ----------------
pred_dvx_n3 = -2 * 0.05 / (1 - 2 * 0.05 ** 2)          # iter_1's n = 3 kink size, the yardstick
avals = (0.4, 0.1, 0.025)
if MUT:
    hps = {"v3s_a0": (lambda P: P)}
else:
    hps = {f"a{aa}": (lambda P, aa=aa: P ** 3 * (P + 2 * aa) / (P + aa) ** 3) for aa in avals}
num = {k: ladder(h) for k, h in hps.items()}
res["numerics"] = num
cc = {}
for k, L in num.items():
    dv = [r["Dvx"] for r in L]; ti = [r["t_inv"] for r in L]
    rt = (ti[-2] / ti[-1]) if (ti[-2] and ti[-1]) else None
    cc[k] = dict(smooth=abs(dv[-1]) <= 0.1 * abs(pred_dvx_n3) and abs(dv[-1]) < abs(dv[-2]),
                 tconv=rt is not None and 0.9 <= rt <= 1.1, t_ratio=rt)
p_fit = None
if not MUT:
    T = [num[f"a{aa}"][-1]["t_inv"] for aa in avals]
    p_fit = float(np.polyfit(np.log(avals), np.log(T), 1)[0])
    ok["Cc_p_in_band"] = 0.35 <= p_fit <= 0.65
res["Cc"] = cc; res["Cc_p_fit"] = p_fit
ok["Cc_all_smooth"] = all(v["smooth"] for v in cc.values())
ok["Cc_all_tconv"] = all(v["tconv"] for v in cc.values())

# ---------------- C-d: statics bounds (both footings) ----------------
G, c, Msun, pc = 6.67430e-11, 2.99792458e8, 1.98892e30, 3.0856775814913673e16
dens_unit = Msun / pc ** 3
foot = {"canonical": dict(a0=9.3603e-11, cass=0.0055, Lstar=21.7), "alt": dict(a0=1.1312e-10, cass=0.0062, Lstar=22.9)}
Cd = {}
for fn, f_ in foot.items():
    rho_de = 4 * f_["a0"] ** 2 / (c ** 2 * G)                 # a0 = kappa c sqrt(G rho_DE), kappa = 1/2
    a_phys = 2 * rho_de / dens_unit                            # Msun/pc^3
    M, r = 1e9 * Msun, 30e3 * pc
    rho_ph = np.sqrt(G * M * f_["a0"]) / (4 * np.pi * G * r ** 2) / dens_unit
    row = dict(rho_DE_kgm3=rho_de, a_Msun_pc3=a_phys,
               cassini=a_phys / f_["cass"], globular_inside_Lstar=a_phys / 0.084,
               floor_shift_pct=(a_phys / 1.5e-4) * 0.042,
               sparc=(f_["Lstar"] / 1e3) ** 2 * a_phys / rho_ph, rho_ph_30kpc_1e9=rho_ph)
    row["pass"] = row["cassini"] <= 1e-3 and row["globular_inside_Lstar"] <= 1e-3 and row["floor_shift_pct"] <= 0.01 and row["sparc"] <= 1e-4
    Cd[fn] = row
ok["Cd_statics"] = all(r["pass"] for r in Cd.values())
res["Cd"] = Cd

# ---------------- C-e: AC2q FRW, AC7 Q1 method ----------------
X, D, s = sp.symbols("X D s", positive=True)
Fq = lambda q, aa: g / 2 * q ** 4 / (q + aa) ** 2
Fp_q = lambda q, aa: g * q ** 3 * (q + 2 * aa) / (q + aa) ** 3
g1 = sp.simplify(sp.diff(Fq(D + 2 * X, 2 * X), D, 2).subs(D, 0))
g2 = sp.simplify(sp.diff(sp.diff(Fq(D + 2 * X, 2 * X) - Fq(2 * X, 2 * X), D).subs(D, 0), X))
k, K, al, P = sp.symbols("k K alpha P", positive=True)
PA = k * P * al / 2; W = K * P ** 2 / 4; DD = k ** 2 * P ** 2 / 2; XD = (-s ** 2 * al) * (-k * P) / 2
L_new = PA - W - g1 / 2 * DD - g2 * XD
L_old = PA - W - g / 2 * DD                                  # AC2 at stiffness gamma (AC7's baseline)
integ = lambda L: sp.simplify(L.subs(P, sp.solve(sp.diff(L, P), P)[0]))
factor = sp.factor(sp.simplify(integ(L_new) / integ(L_old)))
f_s0 = sp.simplify(factor.subs(s, 0))
# crash fix (post-first-run, before any graded number printed): relative to AC2 at stiffness gamma the factor depends on
# k and K (the FRW stiffness is g1 = 11 gamma/16, not gamma), so AC7's fixture loop needs the factor relative to AC2 at
# stiffness g1 (AC2's block at a rescaled Lstar; the ell grid spans 1e-3..1e2). The frozen '= 1 at s = 0' line is
# still graded on the gamma-relative factor below.
L_old_g1 = PA - W - g1 / 2 * DD
factor_g1 = sp.factor(sp.simplify(integ(L_new) / integ(L_old_g1)))
res["Ce"] = dict(g1=str(g1), g2=str(g2), factor=str(factor), factor_at_s0=str(f_s0), factor_rel_AC2_at_g1=str(factor_g1))
rows, healthy = [], True
for gs2 in (0.0, 1e-11):
    fval = float(sp.N(factor_g1.subs({s: 1, g: gs2}))) if gs2 else float(sp.N(factor_g1.subs({s: 0})))
    for E, ell, xx in itertools.product((0.01, 0.5, 2.0), (0.001, 1.0, 100.0), (0.1, 1.0, 10.0, 1000.0)):
        with mp.workdps(40):
            E_, l_, x_, f_ = map(mp.mpf, (E, ell, xx, fval))
            kin = E_ + f_ * x_ ** 2 / (1 + l_ ** 2 * x_ ** 2)
            w2 = lambda y: E_ * y ** 2 / (E_ + f_ * y ** 2 / (1 + l_ ** 2 * y ** 2))
            cph = mp.sqrt(w2(x_)) / x_; cgr = mp.diff(lambda y: mp.sqrt(w2(y)), x_)
            good = kin > 0 and 0 < cph <= 1 + mp.mpf("1e-30") and 0 < cgr <= 1 + mp.mpf("1e-30")
            healthy &= bool(good); rows.append(dict(gamma_s2=gs2, E=E, ell=ell, x=xx, f=fval, healthy=bool(good)))
ok["Ce_factor_positive"] = bool(factor_g1.subs({s: 1, g: sp.Rational(1, 10 ** 11)}) > 0)
ok["Ce_factor_is_1_at_s0"] = sp.simplify(f_s0 - 1) == 0
ok["Ce_fixtures_healthy"] = healthy
res["Ce_rows_healthy"] = sum(r["healthy"] for r in rows)

# ---------------- C-f: soft side identical ----------------
ok["Cf_soft_side_zero"] = all(sp.simplify(sp.diff(Fq(0 * Q, a), Q, j)) == 0 for j in range(3))

c_ab = all(ok[k] for k in ok if k.startswith("Ca") or k.startswith("Cb"))
c_c = ok["Cc_all_smooth"] and ok["Cc_all_tconv"] and ok.get("Cc_p_in_band", False)
c_e = ok["Ce_factor_positive"] and ok["Ce_factor_is_1_at_s0"] and ok["Ce_fixtures_healthy"]
if MUT:
    label = "MUTATE: v3s F through C-c: " + ("C-c PASS (control does NOT bite)" if (ok["Cc_all_smooth"] and ok["Cc_all_tconv"]) else "C-c FAIL (bites)")
else:
    label = dict(v3s=("REPAIR (1D)" if (c_ab and c_c and ok["Cd_statics"]) else "NOT A REPAIR") + " [C-e is AC2q-only]",
                 AC2q="REPAIR (1D)" if (c_ab and c_c and ok["Cd_statics"] and c_e) else "NOT A REPAIR",
                 parts=dict(Cab=c_ab, Cc=c_c, Cd=ok["Cd_statics"], Ce=c_e))
out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, results=res, note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k_}: {'ok' if v else 'FAIL'}" for k_, v in ok.items())
for k_, L in num.items():
    txt += f"\n{k_}: " + "; ".join(f"N{r['N']} dvx {r['Dvx']:.5f} t_inv {r['t_inv']}" for r in L)
txt += f"\np_fit {p_fit}\nCd {json.dumps(Cd, default=float)}\nCe g1 {g1}, g2 {g2}, factor {factor}, at s=0 {f_s0}; rel AC2@g1 {factor_g1}\nLABEL: {label}\n"
open(os.path.join(HERE, tag + ".out"), "w").write(txt)
print(txt)
sys.exit(1 if (MUT and not (ok["Cc_all_smooth"] and ok["Cc_all_tconv"])) else 0)
