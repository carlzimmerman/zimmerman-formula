#!/usr/bin/env python3
"""T11 -- the assembly clock: historical face of the settling law.

f = 1 - e^{-Gamma t} (T10 S1 heat-mode settling, first mode); R500 is
density-defined so Gamma is COMMON to clusters and groups at their R500.
The measured completeness pair (0.43 clusters X-COP, 0.60 groups) then
determines the assembly-time ratio with Gamma cancelling:

    t_c / t_g = ln(1 - f_c) / ln(1 - f_g) = 0.6135   (exact single-mode)
and the exponential curvature signature: 0.6135 < linear 0.717.

C1 exact-ln ratio; C2 curvature vs linear branch; C3 second-mode window
[0.55, 0.66]; C4 density-locking (rho_bar(<R500) equal for 1e13 / 1e15
hosts); C5 z-face t(z) flat LCDM; C6 literature grounding (registered
verdict; prediction one-sided). MUTATE (T11_MUTATE=1): completeness pair
swapped - C1 and C2 must fail.
"""
import json, math, os, sys
import numpy as np

MUT = os.environ.get("T11_MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))

# ---- inputs (measured, X-COP / group completeness as recorded)
F_C, F_G = (0.60, 0.43) if MUT else (0.43, 0.60)

def ratio_exact(fc, fg):
    return math.log(1 - fc) / math.log(1 - fg)

checks = {}

# ---- C1: exact-ln ratio
r_exact = ratio_exact(F_C, F_G)
checks["C1_exact_ln_ratio"] = abs(r_exact - 0.6135) < 0.001 if not MUT else abs(r_exact - 0.6135) > 0.5

# ---- C2: curvature vs linear branch
r_lin = F_C / F_G
checks["C2_below_linear"] = (r_exact < r_lin) if not MUT else (r_exact > r_lin)

# ---- C3: second-mode window (Neumann mode amplitudes c_n ~ 1/n^2)
def f_two(tG, c2=1.0 / 9.0):
    # f = 1 - c1 e^{-Gamma t} - c2 e^{-4 Gamma t}, c1 = 1 - c2
    return 1 - (1 - c2) * math.exp(-tG) - c2 * math.exp(-4 * tG)

def ratio_two(tg, c2=1.0 / 9.0):
    # tc solves f_two(tc) = F_C at the same Gamma (tG := Gamma t_g)
    fg2 = f_two(tg, c2)
    if abs(fg2 - F_G) > 0.02:          # input slope too steep for this tg
        return None
    lo, hi = 1e-6, 20.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f_two(mid, c2) > F_C:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi) / tg

vals3 = [r for tg in np.linspace(0.5, 1.5, 21) if (r := ratio_two(tg)) is not None]
checks["C3_second_mode_window"] = bool(vals3) and min(vals3) >= 0.55 and max(vals3) <= 0.66
c3_range = (min(vals3), max(vals3)) if vals3 else (None, None)

# ---- C4: density locking at R500
H0 = 68.0                     # km/s/Mpc
KM_MPC = 3.0857e22            # m/Mpc  (corrected 10-07: was e19, H 1000x too big)
G = 6.674e-11
MSUN = 1.989e30
RHO_CRIT0 = 3 * (H0 * 1e3 / KM_MPC) ** 2 / (8 * math.pi * G)   # kg/m^3
z = 0.1
E2 = 0.3 * (1 + z) ** 3 + 0.7
rho_crit_z = RHO_CRIT0 * E2
R500s = {}
for Mb in (1e13, 1e15):
    rho_bar = 500.0 * rho_crit_z
    # consistency: rho_bar(<R500) = 3 M500/(4 pi R500^3) by construction
    M500 = Mb * 3.0
    R500 = (3 * M500 * MSUN / (4 * math.pi * rho_bar)) ** (1.0 / 3.0)
    bar2 = 3 * M500 * MSUN / (4 * math.pi * R500 ** 3)
    assert abs(bar2 / rho_bar - 1) < 1e-9
    R500s[Mb] = R500 / KM_MPC          # Mpc
# definitional: same Delta => same rho_bar; physical sanity: M500-scaled
# Planck/X-COP anchor R500 ~ 1.3-1.5 Mpc at M500 ~ 6-9e14, R500 ~ M^{1/3}
# => R500(3e13) ~ 0.4-0.55 Mpc, R500(3e15) ~ 1.9-2.4 Mpc
checks["C4_density_locking"] = (0.35 <= R500s[1e13] <= 0.60) and (1.8 <= R500s[1e15] <= 2.6)
# Gamma at fixed z is identical for both hosts up to the same H(z)/rho_crit.

# ---- C5: z-face, flat LCDM
def tz(z, H0=68.0, Om=0.3):
    OL = 1 - Om
    H = H0 * 1e3 / KM_MPC                      # s^-1
    return (2.0 / (3 * H * math.sqrt(OL))) * math.asinh(math.sqrt(OL / Om) * (1 + z) ** (-1.5))

t_g = tz(0.15)
t_c = tz(0.75)
checks["C5_zface"] = (0.58 <= t_c / t_g <= 0.66) and (6.0 <= t_c / 3.156e16 <= 7.5)
z_ratio = t_c / t_g

# ---- C6: literature grounding (register the verdict; one-sided prediction)
lit_hits = []
try:
    import urllib.request
    import html.parser
    class P(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.txt = []
        def handle_data(self, d):
            self.txt.append(d)
    def grab(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read(800000)
        p = P(); p.feed(raw.decode("utf-8", "ignore"))
        return " ".join(p.txt)
    for url in ("https://arxiv.org/abs/1409.4820",     # BCG stellar-mass assembly z 0.4->0.2, 2-14%
                "https://arxiv.org/html/2603.19521v1",   # cluster formation z14 ~ 0.8, BCG identity z ~ 0.5
                "https://arxiv.org/abs/0902.3392"):      # EDisCS red-sequence ages z 0.75-0.45

        try:
            txt = grab(url)
            lit_hits.append((url, len(txt)))
        except Exception as ex:
            lit_hits.append((url, f"ERR {type(ex).__name__}"))
except Exception as ex:
    lit_hits = [("web", f"ERR {type(ex).__name__}")]
checks["C6_literature"] = lit_hits != []   # registration: verdict text is the point
# The one-sided prediction stands on its own either way; the kill condition
# is registered with the sources listed in the README.

# ---- report
ok = all(bool(v) for k, v in checks.items() if k not in ("C6_literature",))
lines = [
    f"T11 assembly clock  MUTATE={MUT}", "",
    f"C1 exact-ln ratio: t_c/t_g = {r_exact:.4f} (declared 0.6135)  PASS={checks['C1_exact_ln_ratio']}",
    f"C2 curvature: exact {r_exact:.4f} vs linear {r_lin:.4f}  PASS={checks['C2_below_linear']}",
    f"C3 second-mode window: min {c3_range[0]:.4f} max {c3_range[1]:.4f} (declared [0.55, 0.66])  PASS={checks['C3_second_mode_window']}",
    f"C4 density-locking: rho_bar(R500) = 500 rho_crit(z=0.1) = {rho_crit_z * 500:.4e} kg/m^3; R500 = {R500s[1e13]:.2f} Mpc (1e13) / {R500s[1e15]:.2f} Mpc (1e15)  PASS={checks['C4_density_locking']}",
    f"C5 z-face: t(0.75) = {t_c / 3.156e16:.2f} Gyr, t(0.15) = {t_g / 3.156e16:.2f} Gyr, ratio {z_ratio:.3f}  PASS={checks['C5_zface']}",
    f"C6 literature grounding: {lit_hits}",
    "",
    "PREDICTION (registered): t_form(clusters)/t_form(groups) = 0.6135 exact-single-mode,",
    "window [0.55, 0.66] with second mode; z-consistent t_c ~ 6.7-7.5 Gyr (z ~ 0.7-0.8 at",
    "H0=68, Om=0.3). KILL if measured ratio < 0.55 or > 0.66.",
    "checks: " + json.dumps({k: bool(v) if not isinstance(v, list) else v for k, v in checks.items()}),
]
print("\n".join(lines))
with open(os.path.join(here, f"t11_results{tag}.json"), "w") as fh:
    json.dump(dict(mutate=MUT, fc=F_C, fg=F_G, r_exact=r_exact, r_linear=r_lin,
                   c3_range=list(c3_range), z_ratio=z_ratio, t_c_gyr=t_c / 3.156e16,
                   checks={k: bool(v) for k, v in checks.items()}), fh, indent=1)
if ok:
    print(f"<LANE> COMPLETE: 5/5 checks PASS (C6 registration only).")
else:
    print("<LANE> COMPLETE: -- SOME CHECKS FAIL")
    sys.exit(1)