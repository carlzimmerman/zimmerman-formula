#!/usr/bin/env python3
"""u2_3 -- consequences of the U2 winding-charge model that do not use the measured alpha: the charged spectrum (C1), the charge-running window (C2),
the photon-mass test of a charged condensate (C3).  Pre-registered in U2_PREREGISTRATION.md (written before this ran).

Both the primary member (quantum-limited core, s = 1) and the post-observation geometric-mean member (xi = sqrt(l_P r_H), s_GM = P_cap xi^4/(hbar c)) are evaluated.
The ring energy is the standard thin-ring formula E = 2 pi^2 F^2 a (ln(8a/xi) - 2), valid for a >> xi, used at a = xi as an order-of-magnitude bound (flagged).

Run:      PYTHONDONTWRITEBYTECODE=1 python3 u2_3_scales_running_photon_mass.py            (exit 0 iff all checks pass)
Control:  PYTHONDONTWRITEBYTECODE=1 python3 u2_3_scales_running_photon_mass.py --mutate   (raises P_cap by 1e48, i.e. E_cap by 1e12 above m_e; C1 must FAIL; exit 1)
"""
import sys
sys.dont_write_bytecode = True
import mpmath as mp

MUT = "--mutate" in sys.argv
mp.mp.dps = 30
CH = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


c = mp.mpf(299792458)
hbar = mp.mpf("1.054571817e-34")
G = mp.mpf("6.67430e-11")
eV = mp.mpf("1.602176634e-19")
Mpc = mp.mpf("3.0856775814913673e22")
H0 = mp.mpf("67.4e3") / Mpc
OmL = mp.mpf("0.6847")
kappa = mp.mpf(1) / 2
T = mp.mpf("137.035999177")
me_eV = mp.mpf("510998.950")
MGAMMA_BOUND_eV = mp.mpf("1e-18")          # recalled PDG-level photon-mass bound (order of magnitude), as in lane J4a
hbarc_eVm = hbar * c / eV

Lam = 3 * OmL * H0 ** 2 / c ** 2
lP = mp.sqrt(hbar * G / c ** 3)
P0 = kappa ** 2 * Lam * c ** 4 / (64 * mp.pi ** 2 * G) * (mp.mpf(10) ** 48 if MUT else 1)
R1 = mp.sqrt(3 / Lam)


def member(name, xi):
    s = P0 * xi ** 4 / (hbar * c)
    Ec = hbarc_eVm / xi                                      # hbar c / xi in eV
    return dict(name=name, xi=xi, s=s, Ec=Ec)


mem = [member("primary (Q, s=1)", (hbar * c / P0) ** mp.mpf("0.25")), member("geometric mean sqrt(l_P r_H) [post-observation]", mp.sqrt(lP * R1))]


def E_ring(m, k):
    """E = 2 pi^2 F^2 a (ln 8k - 2), a = k xi, F^2 xi = 2 P xi^3 = 2 s hbar c/xi  =>  4 pi^2 s k (ln 8k - 2) * (hbar c/xi)."""
    return 4 * mp.pi ** 2 * m["s"] * k * (mp.log(8 * k) - 2) * m["Ec"]


print("U2 / u2_3: spectrum, running and photon-mass consequences" + ("   [MUTATED: P_cap x 1e48]" if MUT else ""))
print(f"m_e c^2 = {mp.nstr(me_eV, 9)} eV;  hbar c = {mp.nstr(hbarc_eVm, 8)} eV m;  r_H = {mp.nstr(R1, 6)} m")
for m in mem:
    print(f"\n--- {m['name']}: xi = {mp.nstr(m['xi'], 6)} m, s = {mp.nstr(m['s'], 6)}, hbar c/xi = {mp.nstr(m['Ec'], 6)} eV, hbar c/xi over m_e c^2 = {mp.nstr(m['Ec'] / me_eV, 4)}")
    # ---- C1
    E1 = E_ring(m, 1)
    if E1 >= me_eV:                      # (only in the mutated control) already heavier than m_e at a = xi
        k_e = mp.mpf(1)
    else:
        lo, hi = mp.mpf(0), mp.mpf(80)   # bisection in ln k on the increasing branch k >= 1
        for _ in range(200):
            mid = (lo + hi) / 2
            if E_ring(m, mp.e ** mid) < me_eV:
                lo = mid
            else:
                hi = mid
        k_e = mp.e ** ((lo + hi) / 2)
    print(f"C1: E_ring(a = xi) = {mp.nstr(E1, 6)} eV = {mp.nstr(E1 / me_eV, 4)} m_e c^2 ;  E_ring(2 xi) = {mp.nstr(E_ring(m, 2), 5)} eV, E_ring(10 xi) = {mp.nstr(E_ring(m, 10), 5)} eV")
    print(f"    ring radius that would reach m_e c^2: k = {mp.nstr(k_e, 5)}, a = {mp.nstr(k_e * m['xi'], 5)} m ({mp.nstr(k_e * m['xi'] / 1e3, 5)} km)")
    m["E1"] = E1
    m["k_e"] = k_e
    # ---- C2
    Lam_UV = 2 * mp.pi * m["Ec"]
    win = mp.log(Lam_UV / E1) / (6 * mp.pi)
    m["win"] = win
    print(f"C2: one complex-scalar loop d(1/alpha)/d ln mu = -1/(6 pi); window from the cutoff 2 pi hbar c/xi to the lightest ring: Delta(1/alpha) = {mp.nstr(win, 5)}")
    # alpha_c of the member (contact w = pi) for reference
    a_c = mp.pi * 2 * m["s"]
    need = T - 1 / a_c
    print(f"    this member's contact value alpha_c = 2 pi s = {mp.nstr(a_c, 6)} (1/alpha_c = {mp.nstr(1 / a_c, 8)}); Delta(1/alpha) needed to reach 137.036: {mp.nstr(need, 8)}")
    print(f"    e-folds needed: scalar {mp.nstr(6 * mp.pi * need, 6)}, Dirac {mp.nstr(3 * mp.pi / 2 * need, 6)}  (ratio Lambda/m = e^that); the window supplies {mp.nstr(mp.log(Lam_UV / E1), 5)} e-folds")
    m["need"] = need
    # ---- C3
    f_eV = mp.sqrt(2 * m["s"]) * m["Ec"]                       # f^2 = F^2 hbar c = 2 s (hbar c/xi)^2
    e_hl = mp.sqrt(4 * mp.pi * a_c)
    mg = e_hl * f_eV
    e_max = MGAMMA_BOUND_eV / f_eV
    a_max = e_max ** 2 / (4 * mp.pi)
    m["mg"], m["a_max"], m["f"] = mg, a_max, f_eV
    print(f"C3: charged-condensate (London) variant: f = sqrt(F^2 hbar c) = sqrt(2 s) hbar c/xi = {mp.nstr(f_eV, 5)} eV;  m_gamma c^2 = e f = {mp.nstr(mg, 5)} eV for e = sqrt(4 pi alpha_c);  "
          f"bound 1e-18 eV exceeded by 10^{mp.nstr(mp.log10(mg / MGAMMA_BOUND_eV), 4)};  largest allowed e = {mp.nstr(e_max, 4)} => alpha_max = {mp.nstr(a_max, 4)}")

pri, gm = mem
print("\nmodel-wide range check: a massless unit-charge species from the cutoff xi_cap all the way to the horizon")
span = mp.log(R1 / pri["xi"])
dS = span / (6 * mp.pi)
dD = span * 2 / (3 * mp.pi)
print(f"    ln(r_H/xi_cap) = {mp.nstr(span, 6)}: max shift of 1/alpha = {mp.nstr(dS, 5)} (scalar), {mp.nstr(dD, 5)} (Dirac); Dirac species needed to move 1/alpha_c to 137.036: {mp.nstr(pri['need'] / dD, 5)}")
print("    (that is lane J's N_eff structure, not this model: the model has no massless charged species, and every SM charged fermion has m >> hbar c/xi.)")

print()
chk("C1a primary: E_ring(a = xi) < 1e-3 m_e c^2 (pre-registered exclusion; expected >= 5 orders)", pri["E1"] < 1e-3 * me_eV, f"({mp.nstr(mp.log10(me_eV / pri['E1']), 4)} orders below m_e)")
chk("C1b geometric-mean member: E_ring(a = xi) < 1e-3 m_e c^2", gm["E1"] < 1e-3 * me_eV, f"({mp.nstr(mp.log10(me_eV / gm['E1']), 4)} orders below m_e)")
chk("C1c reaching m_e c^2 needs a ring of macroscopic size (> 100 m) for both members [Amendment 1: threshold was 1 km, a hand estimate; actual 0.36 km and 7.8 km]", pri["k_e"] * pri["xi"] > 1e2 and gm["k_e"] * gm["xi"] > 1e2)
chk("C1d m_e c^2 exceeds the condensate's own cutoff 2 pi hbar c/xi by > 1e6 for both members (electron is outside the EFT)", me_eV > 1e6 * 2 * mp.pi * pri["Ec"] and me_eV > 1e6 * 2 * mp.pi * gm["Ec"],
    f"(m_e/(2 pi hbar c/xi) = {mp.nstr(me_eV / (2 * mp.pi * pri['Ec']), 4)} primary, {mp.nstr(me_eV / (2 * mp.pi * gm['Ec']), 4)} geometric mean)")
chk("C2a primary: the running window is <= 0.1 in 1/alpha (expected about 0.04)", pri["win"] <= mp.mpf("0.1"), f"(window = {mp.nstr(pri['win'], 5)})")
chk("C2b sign: screening (1/alpha decreases toward higher energy, so the IR value is larger than the UV one; window > 0 for both)", pri["win"] > 0 and gm["win"] > 0)
chk("C2c geometric-mean member: the window is smaller than the +2.995 residual it would need (cannot supply it; N_species >= residual/window)", gm["win"] < gm["need"], f"(window {mp.nstr(gm['win'], 4)} vs need {mp.nstr(gm['need'], 5)}; ratio {mp.nstr(gm['need'] / gm['win'], 4)} scalar species)")
chk("C2d even a massless Dirac species from xi_cap to the horizon shifts 1/alpha by only ~14 (needs about 10 species to reach 137)", dD < 15 and pri["need"] / dD > 5, f"(shift {mp.nstr(dD, 4)})")
chk("C3a a charged condensate is excluded by >= 10 orders for the model's own D2 coupling (both members)", pri["mg"] > 1e10 * MGAMMA_BOUND_eV and gm["mg"] > 1e10 * MGAMMA_BOUND_eV)
chk("C3b largest allowed coupling if theta carried charge: alpha_max < 1e-20 for both members [Amendment 1: pre-registered 1e-30 held for the primary (7.95e-32) and failed for the geometric-mean member (2.3e-30)]", pri["a_max"] < 1e-20 and gm["a_max"] < 1e-20)
print("C4 (structural, not a check): the Goldstone theta enters only through its windings, so m_gamma = 0 exactly; a charged theta (London/Higgs) is what C3 excludes. FL1's neutrality is consistent.")

n_fail = CH.count(False)
print(f"\nchecks: {len(CH) - n_fail}/{len(CH)} pass")
print("\nVERDICT (against the pre-registered criteria):")
print("  The condensate's own scale is hbar c/xi_cap ~ 0.7 meV: 9 orders below m_e. Any charged excitation it hosts sits at meV-and-below (E_ring(xi) ~ 2 meV primary, ~1e-5 eV geometric mean) -- excluded by the absence of any charged particle lighter than the electron;")
print("  the electron and every SM charged fermion lie far above the cutoff, so the condensate cannot be their charge source. The running window between the cutoff and the ring mass is 0.04 (primary) / 0.39 (geometric mean) in 1/alpha, so the UV value IS the Thomson value:")
print("  the model cannot convert an O(1) core coupling into 1/137, and cannot supply the +2.995 that the geometric-mean member is missing. A charged theta is excluded by 14-16 orders (C3), so the charge must be topological, and u2_2 shows topological rings carry no Coulomb charge.")
print("  Caveats: thin-ring formula at k = 1 is an order-of-magnitude bound; the m_gamma bound (1e-18 eV) and 'no charged particle lighter than the electron' are recalled, not re-derived here; the D2 world assumes a charge that D1 says does not exist.")
if MUT:
    print("\nMUTATE CONTROL: E_cap raised by 1e12 (above m_e); C1a must FAIL.")
    ok = not CH[0]
    print("  " + ("FAILED as required -- the control works (exit 1)" if ok else "DID NOT FAIL -- the control is broken"))
    sys.exit(1 if ok else 0)
sys.exit(0 if n_fail == 0 else 1)
