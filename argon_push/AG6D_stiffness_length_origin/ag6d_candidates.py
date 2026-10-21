#!/usr/bin/env python3
"""AG6D Part B (candidate formulas for L*, look-elsewhere menu) and Part D (condensate microphysics scope).

FROZEN_CRITERIA.md sections 3 and 6 (b94d6b89b). Every formula is built from dimensioned quantities and must come out
as a length (M^0 L^1 T^0 K^0). Window: canonical [24.0, 1000] pc, alt [24.7, 1000] pc (sensitivity: ceiling 2000 pc).
Flags (frozen): F forced identification of the |grad P|^2 coefficient, R reading/analogy, X operator/regime mismatch.
MUTATE (AG6D_MUTATE=1): a dimensionally wrong formula sqrt(G a0)/c is injected; the checker must reject it -> exit 1.
"""
import json, os, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import brentq

MUT = os.environ.get("AG6D_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
out_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out_lines.append(s)


class Q:
    """value with dimension exponents (M, L, T, K)."""

    def __init__(self, v, d=(0, 0, 0, 0)):
        self.v = float(v)
        self.d = tuple(Fr(x) for x in d)

    def __mul__(self, o):
        o = o if isinstance(o, Q) else Q(o)
        return Q(self.v * o.v, tuple(a + b for a, b in zip(self.d, o.d)))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, Q) else Q(o)
        return Q(self.v / o.v, tuple(a - b for a, b in zip(self.d, o.d)))

    def __rtruediv__(self, o):
        return Q(o) / self

    def __pow__(self, p):
        p = Fr(p).limit_denominator(1000) if not isinstance(p, Fr) else p
        return Q(self.v**float(p), tuple(a * p for a in self.d))

    def __add__(self, o):
        assert self.d == o.d, "dimension mismatch in sum"
        return Q(self.v + o.v, self.d)

    def sqrt(self):
        return self**Fr(1, 2)


LENGTH = (Fr(0), Fr(1), Fr(0), Fr(0))
# constants (CODATA 2018 / IAU)
G = Q(6.67430e-11, (-1, 3, -2, 0))
c = Q(299792458.0, (0, 1, -1, 0))
hbar = Q(1.054571817e-34, (1, 2, -1, 0))
kB = Q(1.380649e-23, (1, 2, -2, -1))
m_e = Q(9.1093837015e-31, (1, 0, 0, 0))
m_p = Q(1.67262192369e-27, (1, 0, 0, 0))
eV = 1.602176634e-19
m_MeV = Q(1e6 * eV / 299792458.0**2, (1, 0, 0, 0))
PC = 3.0856775814913673e16
MSUN = 1.98841e30
MPC = 1e6 * PC
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
WIN = {"canonical": (24.0, 1000.0), "alt": (24.7, 1000.0)}
kappa = 0.5
h = 0.677
H0 = Q(100 * h * 1e3 / MPC, (0, 0, -1, 0))
Om = 0.31
OL = 1 - Om
fc_ratio = 5.364
T1 = Q(1.0, (0, 0, 0, 1))  # 1 kelvin


def as_pc(qv):
    if qv.d != LENGTH:
        raise ValueError(f"NOT A LENGTH: dims {tuple(str(x) for x in qv.d)}")
    return qv.v / PC


def a0q(foot):
    return Q(FOOT[foot], (0, 1, -2, 0))


def lands(Lpc, foot, ceil=None):
    lo, hi = WIN[foot]
    hi = hi if ceil is None else ceil
    return lo <= Lpc <= hi


# ---------------- candidates (frozen table) ------------------------------------------------------------------


def candidates(foot):
    a0 = a0q(foot)
    rho_DE = a0**2 / (Q(kappa**2) * c**2 * G)
    H_inf = H0 * Q(np.sqrt(OL))
    ell_a = c**2 / a0
    out = {}
    out["B1  c^2/a0 ({a0,G,c} theorem)"] = ("R", ell_a, "none")
    out["B2  c/sqrt(2 pi G rho_DE)"] = ("F", c / (Q(2 * np.pi) * G * rho_DE).sqrt(), "none")
    out["B3a sqrt2 hbar/(m_P c), m_P c^2 = hbar a0/c"] = ("F", Q(np.sqrt(2)) * hbar / ((hbar * a0 / c / c**2) * c), "none")
    out["B3b sqrt2 hbar/(m_P c), m_P c^2 = hbar H_inf"] = ("F", Q(np.sqrt(2)) * hbar / ((hbar * H_inf / c**2) * c), "none")
    mDE = (rho_DE * hbar**3 * c**5)**Fr(1, 4) / c**2  # (rho c^2 (hbar c)^3)^(1/4) / c^2
    out["B3c sqrt2 hbar/(m_P c), m_P c^2 = DE scale"] = ("F", Q(np.sqrt(2)) * hbar / (mDE * c), "none")
    out["B3d sqrt2 hbar/(m_h c), m_h = 1 MeV"] = ("F", Q(np.sqrt(2)) * hbar / (m_MeV * c), "none")
    out["B4  sqrt(2 hbar^3/(G m_h^4 c)) [a_s = Compton]"] = ("F", (Q(2) * hbar**3 / (G * m_MeV**4 * c)).sqrt(), "none")
    for cs in (20.0, 220.0):
        out[f"B5  hbar/(sqrt2 m_h c_s), c_s={cs:.0f} m/s"] = ("X", hbar / (Q(np.sqrt(2)) * m_MeV * Q(cs, (0, 1, -1, 0))), "none")
    # B6a baryonic Jeans mass at decoupling
    z = 1090.0
    rho_crit0 = Q(3, ) * H0**2 / (Q(8 * np.pi) * G)
    Ob = Om / (1 + fc_ratio)
    rho_m = rho_crit0 * Q(Om * (1 + z)**3)
    rho_b = rho_crit0 * Q(Ob * (1 + z)**3)
    cs_dec = (kB * Q(3000.0) * T1 / (Q(1.22) * m_p)).sqrt()
    lamJ = cs_dec * (Q(np.pi) / (G * rho_m)).sqrt()
    MJ = Q(4 * np.pi / 3) * rho_b * (lamJ / Q(2))**3
    out["B6a sqrt(2 G M_J,dec/a0)"] = ("R", (Q(2) * G * MJ / a0).sqrt(), f"M_J = {MJ.v/MSUN:.3e} Msun")
    sig2 = kB * Q(1e4) * T1 / (Q(1.22) * m_p)
    out["B6b sqrt2 sigma^2/a0, T=1e4 K, mu=1.22"] = ("R", Q(np.sqrt(2)) * sig2 / a0, f"sigma = {np.sqrt(sig2.v)/1e3:.3f} km/s")
    s753 = Q(7.53e3, (0, 1, -1, 0))
    Mcl = Q(81 / 4) * s753**4 / (G * a0)
    out["B6c sqrt(2 G M_cl/a0), M_cl=81 s^4/(4 G a0) [post hoc]"] = ("R", (Q(2) * G * Mcl / a0).sqrt(), f"M_cl = {Mcl.v/MSUN:.3e} Msun")
    out["B7  sigma^2/a0, T=1e4 K, mu=1.22"] = ("R", sig2 / a0, "none")
    # B8: half-central-density match of CFG870's shape to the n=1 sinc profile
    xh = brentq(lambda x: (x * x + 3) / (x * x + 1)**2 - 1.5, 0.1, 2.0)
    sh = brentq(lambda s: np.sin(np.pi * s) / (np.pi * s) - 0.5, 0.1, 0.99)
    Rcl = Q(xh * 104.0 / sh * PC, (0, 1, 0, 0))
    out["B8  (sqrt2/pi) R_TF, R_TF from CFG870 r_c=104 pc [F + post hoc]"] = ("F+posthoc", Q(np.sqrt(2) / np.pi) * Rcl,
                                                                            f"x_half {xh:.5f}, s_half {sh:.5f}, R {Rcl.v/PC:.2f} pc")
    out["B10 two-field MeV compact object size"] = ("R", Q(1e8, (0, 1, 0, 0)), "none")
    if MUT:
        out["MUTANT sqrt(G a0)/c (dimensionally wrong)"] = ("R", (G * a0).sqrt() / c, "planted")
    return out


res = {"lane": "AG6D", "part": "B+D", "mutate": MUT, "window": WIN, "footings": FOOT}
dim_errors = []
table = {}
for foot in FOOT:
    P(f"\n=== Candidates, {foot} footing (a0 = {FOOT[foot]:.4e}); window {WIN[foot]} pc ===")
    for name, (flag, qv, note) in candidates(foot).items():
        try:
            L = as_pc(qv)
        except ValueError as e:
            dim_errors.append((foot, name, str(e)))
            P(f"  {name:62s} DIMENSION CHECK REJECTED: {e}")
            continue
        land = lands(L, foot)
        land2 = lands(L, foot, ceil=2000.0)
        table.setdefault(name, {"flag": flag})[foot] = {"L_pc": L, "land": land, "land_ceil2kpc": land2, "note": note}
        P(f"  {name:62s} [{flag:9s}] L* = {L:.4e} pc  {'LAND' if land else 'MISS'}" + (f"   ({note})" if note != "none" else ""))

# B11 / B12 families
fam = {"B11": [], "B12": []}
for foot in FOOT:
    a0 = a0q(foot)
    ellP = (hbar * G / c**3).sqrt()
    ell_a = c**2 / a0
    for n in range(2, 13):
        al = Fr(1, n)
        L = as_pc(ellP**al * ell_a**(1 - al))
        fam["B11"].append({"foot": foot, "n": n, "L_pc": L, "land": lands(L, foot)})
    for n in range(1, 61):
        L = as_pc(Q(kappa**n) * ell_a)
        fam["B12"].append({"foot": foot, "n": n, "L_pc": L, "land": lands(L, foot)})
for key, desc in (("B11", "l_P^(1/n) (c^2/a0)^(1-1/n), n=2..12"), ("B12", "kappa^n c^2/a0, n=1..60")):
    P(f"\n{key} family {desc}:")
    for foot in FOOT:
        hits = [(d["n"], round(d["L_pc"], 2)) for d in fam[key] if d["foot"] == foot and d["land"]]
        P(f"  {foot:9s}: landing members (n, L* pc) = {hits}")
both11 = sorted(set(d["n"] for d in fam["B11"] if d["foot"] == "canonical" and d["land"]) &
                set(d["n"] for d in fam["B11"] if d["foot"] == "alt" and d["land"]))
both12 = sorted(set(d["n"] for d in fam["B12"] if d["foot"] == "canonical" and d["land"]) &
                set(d["n"] for d in fam["B12"] if d["foot"] == "alt" and d["land"]))
P(f"  land on both footings: B11 n = {both11}; B12 n = {both12}")
res["families"] = fam

# ---------------- look-elsewhere menu ------------------------------------------------------------------------
fracs = sorted({Fr(p, q) for q in range(2, 9) for p in range(1, q)})
assert len(fracs) == 21
menu = {}
for foot in FOOT:
    a0 = a0q(foot)
    S = {"c2/a0": c**2 / a0, "l_P": (hbar * G / c**3).sqrt(), "lam_e": hbar / (m_e * c), "lam_p": hbar / (m_p * c),
         "lam_1MeV": hbar / (m_MeV * c)}
    keys = list(S)
    rows = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            for al in fracs:
                L = as_pc(S[keys[i]]**(1 - al) * S[keys[j]]**al)
                rows.append({"i": keys[i], "j": keys[j], "alpha": str(al), "L_pc": L, "land": lands(L, foot)})
    nl = sum(r["land"] for r in rows)
    logs = np.log10([r["L_pc"] for r in rows])
    menu[foot] = {"N": len(rows), "N_land": nl, "frac": nl / len(rows), "log10_span_pc": [float(logs.min()), float(logs.max())],
                  "landing": [r for r in rows if r["land"]]}
    P(f"\nLook-elsewhere menu, {foot}: {nl} of {len(rows)} combinations land ({100*nl/len(rows):.1f}%); "
      f"menu spans 10^{logs.min():.1f}..10^{logs.max():.1f} pc; window is {np.log10(WIN[foot][1]/WIN[foot][0]):.2f} dex")
    for r_ in menu[foot]["landing"]:
        P(f"    {r_['i']}^(1-{r_['alpha']}) * {r_['j']}^({r_['alpha']}) = {r_['L_pc']:.1f} pc")
res["menu"] = menu
n_phys = len(table)
n_fam = len(fam["B11"]) // 2 + len(fam["B12"]) // 2
n_menu = menu["canonical"]["N"]
res["count_formulas"] = {"physical_candidates": n_phys, "families": n_fam, "menu": n_menu, "total": n_phys + n_fam + n_menu}
P(f"\nTOTAL dimensionally valid formulas evaluated (per footing): {n_phys} candidates + {n_fam} family members + "
  f"{n_menu} menu = {n_phys + n_fam + n_menu}")

# ---------------- classification (frozen rules) -----------------------------------------------------------------
P("\n=== Classification (frozen) ===")
cls = {}
for name, d in table.items():
    if "canonical" not in d or "alt" not in d:
        continue
    both = d["canonical"]["land"] and d["alt"]["land"]
    flag = d["flag"]
    if flag == "X":
        c_ = "SCOPED NO-GO (operator/regime mismatch)"
    elif flag == "F":
        c_ = "LAND but needs a 2nd prediction" if both else "SCOPED NO-GO (forced, MISS)"
    elif flag == "F+posthoc":
        c_ = "CANDIDATE-eligible (pending its 2nd prediction, Part C2/C1)" if both else "SCOPED NO-GO (MISS)"
    else:
        c_ = "NUMEROLOGY" if both else "MISS"
    cls[name] = c_
    P(f"  {name:62s} -> {c_}")
for key, ns in (("B11", both11), ("B12", both12)):
    cls[key] = f"NUMEROLOGY (members {ns} land)" if ns else "MISS"
    P(f"  {key} family -> {cls[key]}")
res["candidates"] = table
res["classification"] = cls

# planted control K-B1
Lk = as_pc(Q(100 * PC, (0, 1, 0, 0)))
kb1 = lands(Lk, "canonical") and lands(Lk, "alt")
P(f"\nK-B1 planted constant 100 pc classifies LAND on both footings: {kb1}")
res["K-B1"] = kb1

# ---------------- Part D: condensate microphysics scope ---------------------------------------------------------
P("\n=== Part D: dilute-condensate realisation of Kp = pi G L*^2 (a_s/m^3 = G L*^2/(2 hbar^2)) ===")
Gs, hb, cl = 6.67430e-11, 1.054571817e-34, 299792458.0
rho1 = 1.0 * MSUN / PC**3
rho001 = 0.01 * MSUN / PC**3
mgrid_eV = np.logspace(-22, 7, 2901)
m_kg = mgrid_eV * eV / cl**2
partD = {}
for Lpc in (24.0, 1000.0):
    Ls = Lpc * PC
    a_s = Gs * Ls**2 * m_kg**3 / (2 * hb**2)
    dil = (rho1 / m_kg) * a_s**3
    sig_m = 8 * np.pi * a_s**2 / m_kg  # m^2/kg ; 1 cm^2/g = 0.1 m^2/kg
    cs = np.sqrt(2 * np.pi * Gs * Ls**2 * rho001)
    heal = hb / (np.sqrt(2) * m_kg * cs)
    ok = (dil < 1.0) & (sig_m < 0.1) & (heal < 0.1 * Ls)
    band = (float(mgrid_eV[ok].min()), float(mgrid_eV[ok].max())) if ok.any() else None
    iM = np.argmin(abs(mgrid_eV - 1e6))
    partD[f"{Lpc:.0f}pc"] = {"band_eV": band, "at_1MeV": {"a_s_m": float(a_s[iM]), "n_as3": float(dil[iM]),
                                                       "sigma_over_m_cm2_g": float(sig_m[iM] * 10), "heal_over_L": float(heal[iM] / Ls)}}
    P(f"  L* = {Lpc:.0f} pc: allowed band (n a_s^3 < 1, sigma/m < 1 cm^2/g [PROVISIONAL scale], healing < 0.1 L*): "
      f"{band[0]:.2e} .. {band[1]:.2e} eV" if band else f"  L* = {Lpc:.0f} pc: no allowed mass")
    P(f"     at m = 1 MeV: a_s = {a_s[iM]:.2e} m, n a_s^3 = {dil[iM]:.1e}, sigma/m = {sig_m[iM]*10:.1e} cm^2/g -> "
      f"{'inside' if ok[iM] else 'OUTSIDE'} the band (ARGON10 0.4-1.7 MeV: "
      f"{'inside' if ok[np.argmin(abs(mgrid_eV-4e5))] and ok[np.argmin(abs(mgrid_eV-1.7e6))] else 'OUTSIDE'})")
# true-BEC background (NOT the record's mean-subtracted form): interaction = rest energy, and DeltaN_eff
rho_crit0 = 3 * (100 * h * 1e3 / MPC)**2 / (8 * np.pi * Gs)
Oc = Om * fc_ratio / (1 + fc_ratio)
Or = 4.15e-5 / h**2
for Lpc in (24.0, 100.0, 1000.0):
    Ls = Lpc * PC
    rho_s = cl**2 / (np.pi * Gs * Ls**2)
    zs = (rho_s / (Oc * rho_crit0))**(1 / 3) - 1
    ratio = (Oc / Or) / (1 + zs)
    dNeff = (8 / 7) * (11 / 4)**(4 / 3) * 1.6918 * ratio
    partD[f"trueBEC_{Lpc:.0f}pc"] = {"z_s": zs, "rhoX_over_rhor": ratio, "DeltaNeff": dNeff}
    P(f"  true-BEC background, L* = {Lpc:.0f} pc: interaction = rest energy at z = {zs:.2e}; radiation-like completion "
      f"-> rho_X/rho_r ~ {ratio:.2e}, Delta N_eff ~ {dNeff:.2f} (report only; the record's form subtracts the background)")
res["partD"] = partD
# light-field reading (CFG744 branch b): the P-quantum mass the window requires, m_P c^2 = sqrt2 hbar c / L*
for Lpc in (24.0, 1000.0):
    mP = np.sqrt(2) * hb * cl / (Lpc * PC) / eV
    partD[f"lightfield_mPc2_eV_{Lpc:.0f}pc"] = mP
    P(f"  light-field reading: L* = {Lpc:.0f} pc needs m_P c^2 = sqrt2 hbar c/L* = {mP:.3e} eV "
      f"(hbar H_inf = {hb*100*h*1e3/MPC*np.sqrt(OL)/eV:.2e} eV, hbar a0/c = {hb*FOOT['canonical']/cl/eV:.2e} eV)")

ok_all = (not dim_errors) and kb1
res["dimension_errors"] = dim_errors
P(f"\nDimension errors: {len(dim_errors)} {'(planted mutant rejected, as required)' if MUT and dim_errors else ''}")
with open(os.path.join(HERE, f"ag6d_candidates_results{TAG}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(os.path.join(HERE, f"ag6d_candidates{TAG}.out"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
sys.exit(0 if ok_all else 1)
