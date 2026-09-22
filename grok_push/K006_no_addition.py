#!/usr/bin/env python3
"""K006 — does the free-fall branch double-count the disc?

THE QUESTION. K005 put ordinary matter on (F) and a settled medium on (S).
The free-fall branch is cold and clusters. If that mass sits in the disc ON
TOP of the supported mass, the rotation curve is the sum and the RAR is
wrecked. If a static region cannot host (F), the interior mass is (S) only,
and an NFW-like precursor's excess over that demand is not a second halo.

Pre-registered:
  ADDITION killed if (M_b + M_S + M_NFW) / M_dyn > 1.5 at the Sun, either footing.
  CONVERSION survives if (M_b + M_S) / M_dyn is within a factor 1.5 of 1
  at the Sun, and the NFW excess over M_S inside 3 R_d is below M_b
  (L247's spiral ceiling is 0.105 of M_b for the density integral; here the
  enclosed-mass excess is reported, not forced through that ceiling).
A FAIL is a finding. No literal-True conditions.
"""
import json
import math

G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
RHO_CRIT = 8.6e-27
MB = 6.5e10 * MSUN
R0 = 8.2 * KPC
R3 = 7.5 * KPC
V_SUN = 233e3
M200 = 1.0e12 * MSUN
C200 = 10.0

RES, NP, NF = [], 0, 0

def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok:
        NP += 1
    else:
        NF += 1

def m_nfw(u):
    return math.log(1.0 + u) - u / (1.0 + u)

def nfw_mass(r):
    r200 = (3.0 * M200 / (4.0 * math.pi * 200.0 * RHO_CRIT)) ** (1.0 / 3.0)
    rs = r200 / C200
    return M200 * m_nfw(r / rs) / m_nfw(C200)

print(__doc__)
M_dyn = V_SUN ** 2 * R0 / G
print(f"    M_dyn(<8.2 kpc) at 233 km/s = {M_dyn/MSUN:.3e} Msun")
print(f"    NFW(<8.2 kpc), M200=1e12, c=10 = {nfw_mass(R0)/MSUN:.3e} Msun")
print(f"    NFW(<7.5 kpc) = {nfw_mass(R3)/MSUN:.3e} Msun")

rows = {}
for tag, a0 in A0.items():
    rM = math.sqrt(G * MB / a0)
    def MS(r, rM=rM):
        return MB * max(r / rM - 1.0, 0.0)
    ms0 = MS(R0)
    ms3 = MS(R3)
    nfw0 = nfw_mass(R0)
    nfw3 = nfw_mass(R3)
    add = (MB + ms0 + nfw0) / M_dyn
    conv = (MB + ms0) / M_dyn
    excess3 = max(nfw3 - ms3, 0.0) / MB
    rows[tag] = dict(rM_kpc=rM / KPC, MS0=ms0 / MSUN, MS3=ms3 / MSUN,
                     nfw0=nfw0 / MSUN, nfw3=nfw3 / MSUN,
                     add=add, conv=conv, excess3=excess3)
    print(f"    [{tag}] r_M = {rM/KPC:.2f} kpc")
    print(f"           M_S(8.2) = {ms0/MSUN:.3e}   M_S(7.5) = {ms3/MSUN:.3e}")
    print(f"           addition (Mb+MS+NFW)/M_dyn = {add:.2f}")
    print(f"           conversion (Mb+MS)/M_dyn = {conv:.2f}")
    print(f"           NFW excess over M_S inside 7.5 kpc / Mb = {excess3:.2f}")

check(
    "V1 [ADDITION of an NFW halo on top of (S) overshoots the Sun] "
    "(M_b + M_S + M_NFW)/M_dyn at 8.2 kpc, 233 km/s, compared with 1.5, both footings",
    f"canonical {rows['canonical']['add']:.2f}, alt {rows['alt']['add']:.2f}, threshold 1.5",
    rows["canonical"]["add"] > 1.5 and rows["alt"]["add"] > 1.5,
    "the pre-registered kill is a ratio above 1.5. The measured ratio is what it is",
)
check(
    "V2 [CONVERSION: M_b + M_S alone against M_dyn] (M_b + M_S)/M_dyn at 8.2 kpc "
    "compared with the band [1/1.5, 1.5]",
    f"canonical {rows['canonical']['conv']:.2f}, alt {rows['alt']['conv']:.2f}",
    all(1.0 / 1.5 < rows[t]["conv"] < 1.5 for t in A0),
    "deep-branch M_S is zero inside r_M, so this ratio is baryons alone. The band is [0.667, 1.5]",
)
check(
    "V3 [the NFW interior is not a second halo's worth above (S)] "
    "max(M_NFW - M_S, 0)/M_b inside 7.5 kpc, reported against 1",
    f"canonical {rows['canonical']['excess3']:.2f}, alt {rows['alt']['excess3']:.2f}",
    all(rows[t]["excess3"] < 1.0 for t in A0),
    "inside 7.5 kpc, NFW minus the deep-branch M_S (which is 0) over M_b, against 1",
)

def kernel_mass(r, a0):
    """Total mass implied by mu_2 at a0 = s/2. Y = g/s, mu = 1-(1+Y)^{-2}, g_bar = mu*g."""
    s = 2.0 * a0
    g_bar = G * MB / r**2
    # solve mu(g/s)*g = g_bar
    lo, hi = g_bar, g_bar + s
    for _ in range(80):
        if (1.0 - (1.0 + hi / s) ** -2) * hi < g_bar:
            hi *= 2.0
        else:
            break
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        mu = 1.0 - (1.0 + mid / s) ** -2
        if mu * mid < g_bar:
            lo = mid
        else:
            hi = mid
    g = 0.5 * (lo + hi)
    return g * r**2 / G

print("\nPART B — the kernel, not the deep asymptotic, at the Sun")
print("    deep-branch M_S is identically 0 for r < r_M. The Sun is inside r_M.")
kern = {}
for tag, a0 in A0.items():
    Mt = kernel_mass(R0, a0)
    Mph = Mt - MB
    nfw0 = nfw_mass(R0)
    add_k = (Mt + nfw0) / M_dyn
    conv_k = Mt / M_dyn
    kern[tag] = dict(Mtot=Mt / MSUN, Mph=Mph / MSUN, add=add_k, conv=conv_k)
    print(f"    [{tag}] mu_2 M_tot(8.2) = {Mt/MSUN:.3e}, phantom = {Mph/MSUN:.3e}")
    print(f"           conversion M_tot/M_dyn = {conv_k:.2f}; addition (M_tot+NFW)/M_dyn = {add_k:.2f}")

check(
    "V4 [the deep formula is the wrong test at the Sun] r_M > 8.2 kpc on both footings, "
    "so deep-branch M_S(8.2) = 0 by the max(r/r_M-1, 0) clause",
    f"canonical r_M = {rows['canonical']['rM_kpc']:.2f} kpc, alt r_M = {rows['alt']['rM_kpc']:.2f} kpc, R0 = 8.2",
    rows["canonical"]["rM_kpc"] > 8.2 and rows["alt"]["rM_kpc"] > 8.2
    and rows["canonical"]["MS0"] == 0.0 and rows["alt"]["MS0"] == 0.0,
    "V1 and V2 tested a formula outside its domain. They stand as that finding, not as a verdict on the kernel",
)
check(
    "V5 [KERNEL ADDITION still overshoots] (mu_2 mass + NFW)/M_dyn at 8.2 kpc vs 1.5",
    f"canonical {kern['canonical']['add']:.2f}, alt {kern['alt']['add']:.2f}",
    kern["canonical"]["add"] > 1.5 and kern["alt"]["add"] > 1.5,
    "the pre-registered kill is a ratio above 1.5. Below that, addition is not excluded by this gate",
)
check(
    "V6 [KERNEL CONVERSION against 233 km/s] mu_2 M_tot/M_dyn in [1/1.5, 1.5]",
    f"canonical {kern['canonical']['conv']:.2f}, alt {kern['alt']['conv']:.2f}",
    all(1.0 / 1.5 < kern[t]["conv"] < 1.5 for t in A0),
    "the kernel alone, no added halo, is the solar-circle mass to within the pre-registered factor",
)
print()
print("READING")
print(f"""
  The deep-branch formula does not govern the Sun: r_M is {rows['canonical']['rM_kpc']:.2f} / {rows['alt']['rM_kpc']:.2f} kpc,
  so M_S(8.2) = 0. V1's addition kill does not fire on that formula (0.94x, under 1.5).
  V2's conversion band misses (0.63, below 1/1.5) because the formula is outside its domain.

  On mu_2 the kernel mass at 8.2 kpc is {kern['canonical']['conv']:.2f}x / {kern['alt']['conv']:.2f}x M_dyn.
  Adding the 1e12 c=10 halo on top of that kernel mass is {kern['canonical']['add']:.2f}x / {kern['alt']['add']:.2f}x.
  Those two numbers are the result. The reading is whatever the checks say, not this prose if they disagree.
""")
print(f"K006 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES, "rows": rows, "kernel": kern,
           "M_dyn_Msun": M_dyn / MSUN},
          open("grok_push/K006_results.json", "w"), indent=1)
raise SystemExit(0 if NF == 0 else 1)
