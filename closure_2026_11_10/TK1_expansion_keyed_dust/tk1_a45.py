"""TK1 A4 (static-well charge bookkeeping) and A5 (MK1's rows re-read at mu_eff), closed forms. Criteria 98f2ab2b6e.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk1_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
G = 6.67430e-11
GM_SUN = 1.32712440018e20
MSUN = GM_SUN / G
KPC = 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
PD1_CAP = {"canonical": 59.486, "alt": 59.503}
FLD1_ARRIVAL_MAX = 0.051       # FLD1: clock charge inside 10-300 kpc at z 0 is 1.6-5.1 % of the halo's
out = {}

# KA7
c_can = math.sqrt(MSUN * A0["canonical"] / G) * KPC / MSUN
c_alt = math.sqrt(MSUN * A0["alt"] / G) * KPC / MSUN
out["KA7"] = dict(canonical=c_can, alt=c_alt, brief=25914.0, rel=c_can / 25914.0 - 1, pass_=abs(c_can / 25914.0 - 1) < 1e-3)
print("KA7 sqrt(Msun a0/G) per kpc: canonical %.1f (brief 25,914; rel %.1e), alt %.1f Msun/kpc" % (c_can, out["KA7"]["rel"], c_alt))

def law_need(Mb_sun, r_kpc, a0):
    """phantom charge inside r for the action's law (mu(x) = x/(1+x)): M_dyn - M_b."""
    gN = G * Mb_sun * MSUN / (r_kpc * KPC)**2
    g = gN / 2 + math.sqrt(gN**2 / 4 + gN * a0)
    return g * (r_kpc * KPC)**2 / G / MSUN - Mb_sun

out["A4"] = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    rows = []
    for lmb in (9.4, 10.45, 10.7, 10.9):
        Mb = 10**lmb
        for r in (100, 300):
            need = law_need(Mb, r, a0)
            deep = math.sqrt(Mb * MSUN * a0 / G) * r * KPC / MSUN
            x = need / Mb
            rows.append(dict(logMb=lmb, r_kpc=r, need_over_Mb=x, deep_over_Mb=deep / Mb,
                             holds_5p41=x <= 5.41, holds_cap=x <= PD1_CAP[foot],
                             arrival_over_need_max=FLD1_ARRIVAL_MAX, arrival_over_Mb_max=FLD1_ARRIVAL_MAX * x))
            print("[%s] A4 log M_b %.2f r %3d kpc: C_need = %.2f M_b (deep %.2f) | 5.41: %s | cap %.1f: %s | FLD1 arrival <= %.2f M_b" % (
                foot, lmb, r, x, deep / Mb, "HOLDS" if x <= 5.41 else "SHORT x%.2f" % (x / 5.41),
                PD1_CAP[foot], "HOLDS" if x <= PD1_CAP[foot] else "SHORT", FLD1_ARRIVAL_MAX * x))
    out["A4"][foot] = rows
    out["A4"][foot + "_holds_cap_all"] = all(r_["holds_cap"] for r_ in rows)
    out["A4"][foot + "_holds_5p41_all"] = all(r_["holds_5p41"] for r_ in rows)
# the collapsed charge left as dust in a static well (theta = 0): Q - 1 = K n / M_f^2
Mf2 = (1e-3 / L.H0_PER_MPC)**2
for nm, Om in (("200 x mean baryon density", 200 * L.FOOT["canonical"]["Ob"]),
               ("200 x mean clock charge (5.41 x baryons)", 200 * L.FOOT["canonical"]["Od"])):
    q = 1.5 * Om / Mf2
    out.setdefault("A4_dust_in_well", {})[nm] = q
    print("A4 if the clock charge stayed as dust at theta = 0 (%s): Q - 1 = K n / M_f^2 = %.3f" % (nm, q))

# A5: MK1's allowed sets (MK1 RESULT table), per footing, per Mpc
MK1 = {"canonical": {"1 CMB background": (198.25, math.inf), "2 Jeans line": (2.512e4, math.inf), "3 X-COP": None,
                     "4 groups": (0.912, 1.514), "5 SPARC": (0, 7.08), "6 KiDS capped": (0, 1.00), "7 Saturn": (0, 6.22e3)},
       "alt": {"1 CMB background": (198.24, math.inf), "2 Jeans line": (2.512e4, math.inf), "3 X-COP": None,
               "4 groups": (0.759, 1.380), "5 SPARC": (0, 5.62), "6 KiDS capped": (0, 0.765), "7 Saturn": (0, 6.22e3)}}
a3j = json.load(open(os.path.join(HERE, "tk1_a3.json"))) if os.path.exists(os.path.join(HERE, "tk1_a3.json")) else None
out["A5"] = {}
for foot in ("canonical", "alt"):
    a2 = a3j[foot]["A2"]["primary"] if a3j else None
    mu_bg = a2["rows"]["3400"]["mu_eff_perMpc"] if a2 else 3e4
    mu_min = a2["mu_eff_min"]["mu"] if a2 else 3e4
    rows = {}
    for row, rng in MK1[foot].items():
        if row.startswith("1"):
            mu = mu_bg; env = "FRW z 3400"
        elif row.startswith("2"):
            mu = mu_min; env = "FRW, min over z in [0, 3400] (dominance)"
        else:
            mu = 1e-3; env = "static well, theta = 0: mu_eff = M_f"
        ok = rng is not None and rng[0] <= mu <= rng[1]
        rows[row] = dict(mu_eff=mu, env=env, allowed=rng, passes=ok)
        print("[%s] A5 %-17s mu_eff %.4g (%s) allowed %s: %s" % (foot, row, mu, env, rng if rng else "none (MK1)", "PASS" if ok else "FAIL"))
    out["A5"][foot] = rows
json.dump(out, open(os.path.join(HERE, "tk1_a45.json"), "w"), indent=1, default=str)
print("done")
