#!/usr/bin/env python3
"""
pdg_constants.py — the machine-readable particle-physics constants dataset, WITH UNCERTAINTIES.

WHY UNCERTAINTIES ARE THE POINT (Carl's #1 emphasis this run):
    A 6-digit match to a 2-digit-known constant is meaningless. The engine must only ever score
    "matches WITHIN the measurement error", and the FDR gate must weight by precision — n-sigma
    agreement, surplus bits relative to the tolerance, not raw digit-count. So EVERY target here
    carries an ABSOLUTE sigma, a RELATIVE sigma, and a derived `n_digits_known` (the number of
    significant figures the measurement actually pins). A formula that lands inside [val-sigma,
    val+sigma] is a *candidate hit*; one that lands 6 digits deep on a 2-digit target is fitting
    noise, and `rel_precision` is exactly the knob that tells the gate which is which.

PROVENANCE / SOURCE TAGS:
    PDG  = Particle Data Group (Review of Particle Physics, 2024-class central values).
    CODATA = CODATA 2018/2022 recommended values (leptons, alpha, G_F-derived).
    NuFIT = NuFIT 5.2-class global fit of the neutrino oscillation data (PMNS, Dm^2).
    DERIVED = computed here from other entries with PROPAGATED uncertainty (ratios, Koide Q, ...).
    All values are PDG-2024-class from model knowledge (assistant cutoff Jan 2026); a few [L]
    entries (light-quark masses, Sum m_nu, delta_CP, ordering) are deliberately flagged LOW so the
    search never fits a tight formula to a loosely-measured number and calls it a discovery.

CONFIDENCE TAGS (the width of the target gates the strength of any claim):
    H = high   (well-measured, scheme-stable; GOOD search target)
    M = medium (scheme/scale-dependent or moderate error; usable, weight by sigma)
    L = low    (poorly known / scheme-fragile; WEAK target — quark masses, abs nu scale, phases)

DESIGN:
    - One flat registry of `Target` records, each with (value, sigma_abs, sigma_rel, units,
      source, conf, sector, note).
    - Asymmetric PDG errors (+a/-b) are stored as a symmetrized sigma (the conservative max) plus
      the raw (plus,minus) kept in `note` — honest about the asymmetry without pretending it away.
    - A `get(key) -> TargetView` accessor returns exactly the tuple the brief asks for:
        (value, sigma, rel_precision, n_digits_known)  via .value/.sigma/.rel_precision/.n_digits.
    - DERIVED dimensionless ratios (m_mu/m_e, m_tau/m_mu, m_p/m_e, m_t/m_b, Dm21^2/|Dm31^2|, the
      Koide invariants, ...) are computed with FULL error propagation (independent-Gaussian add in
      quadrature on the relative errors for products/quotients) so the ratio's own sigma is honest.
    - `precise_targets()` / `weak_targets()` partition by rel_precision so the engine can aim at the
      sharp ones (leptons, alpha, sin^2 theta_13) and quarantine the blunt ones (light quarks).

Pure-stdlib + mpmath if available (graceful float fallback). No network. Run as a script to print
the loaded table and the precise/weak partition.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---- mpmath if present (SM ratios want > double precision for honest FDR tolerances) ----------
try:
    import mpmath as mp
    mp.mp.dps = 40
    def _F(x):
        return mp.mpf(str(x))
    def _sqrt(x):
        return mp.sqrt(x)
    _HAVE_MP = True
except Exception:  # pragma: no cover - fallback
    def _F(x):
        return float(x)
    def _sqrt(x):
        return math.sqrt(float(x))
    _HAVE_MP = False


# =============================================================================
# CORE RECORD
# =============================================================================

@dataclass
class Target:
    """One measured (or derived) particle-physics observable, with its uncertainty.

    value       : central value (mpmath mpf if available, else float)
    sigma       : SYMMETRIC 1-sigma absolute uncertainty (conservative if PDG error asymmetric)
    units       : physical units, '' for dimensionless
    source      : PDG | CODATA | NuFIT | DERIVED
    conf        : 'H' | 'M' | 'L'
    sector      : grouping key ('lepton_mass', 'quark_mass', 'gauge', 'higgs', 'ckm', 'pmns', ...)
    note        : free text (scheme/scale, asymmetric raw error, ordering caveat, ...)
    sigma_plus  : raw + error if PDG asymmetric (else == sigma)
    sigma_minus : raw - error if PDG asymmetric (else == sigma)
    is_bound    : True if the value is an upper bound, not a measurement (theta_QCD, Sum m_nu)
    """
    key: str
    value: object
    sigma: object
    units: str
    source: str
    conf: str
    sector: str
    note: str = ""
    sigma_plus: object = None
    sigma_minus: object = None
    is_bound: bool = False

    def __post_init__(self):
        self.value = _F(self.value)
        self.sigma = _F(self.sigma)
        self.sigma_plus = self.sigma if self.sigma_plus is None else _F(self.sigma_plus)
        self.sigma_minus = self.sigma if self.sigma_minus is None else _F(self.sigma_minus)

    # ---- the four numbers the brief asks every target to expose ----
    @property
    def rel_precision(self) -> float:
        """Relative 1-sigma = sigma/|value|. The load-bearing 'how well is this known' number.
        For a bound, this is sigma/value where sigma is set to the bound itself (rel ~ 1)."""
        v = abs(float(self.value))
        if v == 0.0:
            return float("inf")
        return float(self.sigma) / v

    @property
    def n_digits(self) -> float:
        """Significant figures actually pinned = -log10(rel_precision). A rel error of 1e-5 ->
        5 digits known; 0.1 -> 1 digit. This is the cap on how deep a 'match' can mean anything."""
        rp = self.rel_precision
        if rp <= 0 or not math.isfinite(rp):
            return 0.0
        return -math.log10(rp)

    @property
    def n_sigma_of(self):
        """Return a function val -> n-sigma deviation of a candidate `val` from this target."""
        v = float(self.value)
        s = float(self.sigma) if float(self.sigma) > 0 else float("inf")
        def _f(candidate):
            return abs(float(candidate) - v) / s
        return _f

    def within(self, candidate, k: float = 1.0) -> bool:
        """Does `candidate` fall within k sigma of this target? (the engine's hit predicate)."""
        return self.n_sigma_of(candidate) <= k

    def as_tuple(self) -> Tuple[float, float, float, float]:
        """(value, sigma, rel_precision, n_digits_known) — the exact accessor the brief specifies."""
        return (float(self.value), float(self.sigma), self.rel_precision, self.n_digits)


# =============================================================================
# UNCERTAINTY PROPAGATION (for DERIVED ratios — honest sigma on every ratio)
# =============================================================================

def _quad(*xs) -> float:
    return math.sqrt(sum(float(x) ** 2 for x in xs))


def ratio(a: Target, b: Target, key: str, note: str = "", conf: Optional[str] = None) -> Target:
    """a/b with relative errors added in quadrature (independent-Gaussian assumption).
    Conf defaults to the WORSE of the two inputs (a ratio is no better-known than its blunter leg).
    """
    val = float(a.value) / float(b.value)
    rel = _quad(a.rel_precision, b.rel_precision)
    sig = val * rel
    if conf is None:
        conf = _worse(a.conf, b.conf)
    return Target(key, val, sig, "", "DERIVED", conf, "ratio",
                  note or f"{a.key}/{b.key}, rel err quadrature {rel:.2e}")


def _worse(c1: str, c2: str) -> str:
    order = {"H": 0, "M": 1, "L": 2}
    return c1 if order.get(c1, 2) >= order.get(c2, 2) else c2


def koide_Q(m1: Target, m2: Target, m3: Target, key: str, note: str = "") -> Target:
    """Koide Q = (m1+m2+m3)/(sqrt(m1)+sqrt(m2)+sqrt(m3))^2, with a Monte-Carlo-free linearized
    error propagation. Q is dimensionless and scale-invariant in the masses' common units, so the
    OVERALL mass scale cancels — only the within-sector errors matter. We propagate by the partials
    numerically (central differences) over the three masses' sigmas added in quadrature.
    """
    ms = [float(m1.value), float(m2.value), float(m3.value)]
    ss = [float(m1.sigma), float(m2.sigma), float(m3.sigma)]

    def Q_of(vals):
        num = sum(vals)
        den = (math.sqrt(vals[0]) + math.sqrt(vals[1]) + math.sqrt(vals[2])) ** 2
        return num / den

    Q0 = Q_of(ms)
    var = 0.0
    for i in range(3):
        h = ms[i] * 1e-6 if ms[i] != 0 else 1e-9
        up = list(ms); up[i] += h
        dn = list(ms); dn[i] -= h
        dQ = (Q_of(up) - Q_of(dn)) / (2 * h)
        var += (dQ * ss[i]) ** 2
    sig = math.sqrt(var)
    conf = _worse(_worse(m1.conf, m2.conf), m3.conf)
    return Target(key, Q0, sig, "", "DERIVED", conf, "koide",
                  note or "Koide Q = Sum m / (Sum sqrt m)^2; scale-invariant")


def sqrt_mass_angle(m1: Target, m2: Target, m3: Target, key: str) -> Target:
    """The geometric Koide angle theta where cos^2 theta = (Sum sqrt m)^2 / (3 Sum m) = 1/(3Q).
    Koide leptons => Q=2/3 => cos^2 = 1/2 => theta = 45 deg. Returned in DEGREES with propagated
    sigma from Q. (theta = arccos(sqrt(1/(3Q))).)"""
    Qt = koide_Q(m1, m2, m3, key + "_Q")
    Q = float(Qt.value)
    cos2 = 1.0 / (3.0 * Q)
    cos2 = min(max(cos2, 0.0), 1.0)
    theta = math.degrees(math.acos(math.sqrt(cos2)))
    # dtheta/dQ propagation
    dQ = float(Qt.sigma)
    eps = Q * 1e-6
    def th_of(q):
        c2 = min(max(1.0 / (3.0 * q), 0.0), 1.0)
        return math.degrees(math.acos(math.sqrt(c2)))
    dtheta = (th_of(Q + eps) - th_of(Q - eps)) / (2 * eps)
    sig = abs(dtheta * dQ)
    return Target(key, theta, sig, "deg", "DERIVED", Qt.conf, "koide",
                  "sqrt-mass vector angle to (1,1,1); leptons -> 45 deg (Q=2/3)")


# =============================================================================
# THE DATASET
# =============================================================================

def _build_measured() -> List[Target]:
    """All directly-measured SM/particle observables with PDG-class central + uncertainty."""
    T = []  # noqa

    # ---------------------------------------------------------------------
    # 1. CHARGED-LEPTON POLE MASSES (CODATA/PDG; the sharpest masses in the SM)
    # ---------------------------------------------------------------------
    T += [
        Target("m_e", 0.51099895000, 1.5e-10, "MeV", "CODATA", "H", "lepton_mass",
               "electron pole mass; rel err ~3e-10"),
        Target("m_mu", 105.6583755, 2.3e-6, "MeV", "CODATA", "H", "lepton_mass",
               "muon pole mass; rel err ~2e-8"),
        Target("m_tau", 1776.86, 0.12, "MeV", "PDG", "H", "lepton_mass",
               "tau pole mass; rel err ~7e-5 (the blunt one among leptons)"),
    ]

    # ---------------------------------------------------------------------
    # 2. QUARK MASSES — scheme/scale dependent. MS-bar at the noted scale; t is a pole.
    #    Light quarks (u,d) are LOW confidence: fractional errors ~10-20%.
    # ---------------------------------------------------------------------
    T += [
        Target("m_u", 2.16, 0.49, "MeV", "PDG", "L", "quark_mass",
               "MS-bar(2 GeV); PDG +0.49/-0.26 -> sym sigma=0.49 (conservative)",
               sigma_plus=0.49, sigma_minus=0.26),
        Target("m_d", 4.70, 0.48, "MeV", "PDG", "L", "quark_mass",
               "MS-bar(2 GeV); PDG +0.48/-0.17 -> sym sigma=0.48 (conservative)",
               sigma_plus=0.48, sigma_minus=0.17),
        Target("m_s", 93.5, 0.8, "MeV", "PDG", "M", "quark_mass",
               "MS-bar(2 GeV) strange"),
        Target("m_c", 1270.0, 20.0, "MeV", "PDG", "M", "quark_mass",
               "MS-bar(m_c) charm running mass = 1.27 GeV"),
        Target("m_b", 4180.0, 30.0, "MeV", "PDG", "M", "quark_mass",
               "MS-bar(m_b) bottom running mass = 4.18 GeV; PDG +0.03/-0.02 GeV",
               sigma_plus=30.0, sigma_minus=20.0),
        Target("m_t", 172570.0, 290.0, "MeV", "PDG", "H", "quark_mass",
               "top pole mass = 172.57 GeV; Yukawa ~ 1"),
    ]

    # ---------------------------------------------------------------------
    # 3. BARYON MASSES (proton, neutron) — NOT Yukawa, QCD-dominated; useful for m_p/m_e
    # ---------------------------------------------------------------------
    T += [
        Target("m_p", 938.27208816, 2.9e-7, "MeV", "CODATA", "H", "baryon_mass",
               "proton mass; rel err ~3e-10"),
        Target("m_n", 939.56542052, 5.4e-7, "MeV", "CODATA", "H", "baryon_mass",
               "neutron mass; rel err ~6e-10"),
    ]

    # ---------------------------------------------------------------------
    # 4. GAUGE COUPLINGS
    # ---------------------------------------------------------------------
    T += [
        Target("alpha_em_inv_0", 137.035999177, 2.1e-8, "", "CODATA", "H", "gauge",
               "1/alpha_em at q^2=0 (Thomson limit); rel err ~1.5e-10 (sharpest in the SM)"),
        Target("alpha_em_inv_MZ", 127.951, 0.009, "", "PDG", "M", "gauge",
               "1/alpha_em(M_Z), MS-bar; rel err ~7e-5"),
        Target("alpha_s_MZ", 0.1180, 0.0009, "", "PDG", "M", "gauge",
               "alpha_s(M_Z); THE loosest gauge input, rel err ~8e-3"),
        Target("sin2_thetaW_MZ", 0.23122, 0.00003, "", "PDG", "H", "gauge",
               "sin^2 theta_W(M_Z) MS-bar (scheme-dependent); SU(5) tree value is 3/8"),
        Target("G_F", 1.1663788e-5, 6.0e-12, "GeV^-2", "PDG", "H", "ew_scale",
               "Fermi constant; rel err ~5e-7"),
    ]

    # ---------------------------------------------------------------------
    # 5. EW / HIGGS SCALES
    # ---------------------------------------------------------------------
    T += [
        Target("v_higgs", 246.21965, 0.00060, "GeV", "PDG", "H", "ew_scale",
               "Higgs vev = (sqrt2 G_F)^-1/2; sets overall mass scale (not ratios)"),
        Target("m_H", 125.20, 0.11, "GeV", "PDG", "H", "higgs",
               "Higgs boson mass; -> lambda = m_H^2/2v^2 ~ 0.129"),
        Target("m_W", 80.3692, 0.0133, "GeV", "PDG", "H", "ew_scale",
               "W boson mass (PDG world avg)"),
        Target("m_Z", 91.1880, 0.0020, "GeV", "PDG", "H", "ew_scale",
               "Z boson mass; rel err ~2e-5"),
    ]

    # ---------------------------------------------------------------------
    # 6. STRONG CP
    # ---------------------------------------------------------------------
    T += [
        Target("theta_QCD", 1.0e-10, 1.0e-10, "", "PDG", "H", "strong_cp",
               "theta-bar_QCD < ~1e-10 (nEDM bound); a BOUND not a measurement ('strong CP problem')",
               is_bound=True),
    ]

    # ---------------------------------------------------------------------
    # 7. CKM (Wolfenstein params + Jarlskog) — quark mixing
    # ---------------------------------------------------------------------
    T += [
        Target("ckm_lambda", 0.22501, 0.00068, "", "PDG", "H", "ckm",
               "Wolfenstein lambda = sin(theta_C) = |V_us|; Cabibbo angle"),
        Target("ckm_A", 0.826, 0.016, "", "PDG", "M", "ckm",
               "Wolfenstein A; PDG +0.016/-0.015", sigma_plus=0.016, sigma_minus=0.015),
        Target("ckm_rhobar", 0.1591, 0.0094, "", "PDG", "M", "ckm",
               "Wolfenstein rho-bar"),
        Target("ckm_etabar", 0.3523, 0.0073, "", "PDG", "M", "ckm",
               "Wolfenstein eta-bar (CP phase); PDG +0.0073/-0.0071",
               sigma_plus=0.0073, sigma_minus=0.0071),
        Target("ckm_J", 3.08e-5, 0.13e-5, "", "PDG", "M", "ckm",
               "Jarlskog invariant (CP violation measure)"),
        # standard-angle form (degrees) for cross-sector / complementarity tests
        Target("ckm_theta12", 13.00, 0.04, "deg", "PDG", "H", "ckm",
               "Cabibbo angle theta_12^CKM ~ asin(lambda)"),
        Target("ckm_theta23", 2.41, 0.06, "deg", "PDG", "M", "ckm",
               "theta_23^CKM ~ asin(A lambda^2)"),
        Target("ckm_theta13", 0.201, 0.011, "deg", "PDG", "M", "ckm",
               "theta_13^CKM (the small CKM angle)"),
        Target("ckm_deltaCP", 65.5, 3.0, "deg", "PDG", "M", "ckm",
               "CKM CP phase delta ~ atan2(etabar, rhobar) ~ 66 deg"),
    ]

    # ---------------------------------------------------------------------
    # 8. PMNS + neutrino mass-squared splittings (NuFIT 5.2-class, NORMAL ordering)
    #    Stored as sin^2(theta) (the fit's natural variable) AND theta in degrees.
    #    The NO/IO ambiguity is carried explicitly: |Dm^2_31| is the NO atmospheric splitting.
    # ---------------------------------------------------------------------
    T += [
        Target("Dm2_21", 7.42e-5, 0.21e-5, "eV^2", "NuFIT", "H", "nu_mass",
               "solar mass-squared splitting; PDG/NuFIT +0.21/-0.20 e-5",
               sigma_plus=0.21e-5, sigma_minus=0.20e-5),
        Target("Dm2_31_NO", 2.510e-3, 0.027e-3, "eV^2", "NuFIT", "M", "nu_mass",
               "|Dm^2_31| atmospheric splitting, NORMAL ordering (sign=ordering unknown)"),
        Target("Dm2_32_IO", -2.490e-3, 0.028e-3, "eV^2", "NuFIT", "L", "nu_mass",
               "|Dm^2_32| INVERTED ordering branch (negative); NO favored ~2-3 sigma"),
        Target("Sum_m_nu", 0.06, 0.06, "eV", "PDG", "L", "nu_mass",
               "Sum m_nu: cosmo bound < ~0.12 eV; abs scale UNKNOWN (BOUND, weak target)",
               is_bound=True),

        Target("pmns_sin2_12", 0.303, 0.012, "", "NuFIT", "H", "pmns",
               "sin^2 theta_12 (solar); TBM value is 1/3 = 0.3333"),
        Target("pmns_sin2_23", 0.572, 0.018, "", "NuFIT", "M", "pmns",
               "sin^2 theta_23 (atm); near-maximal, octant open; TBM value 1/2"),
        Target("pmns_sin2_13", 0.02203, 0.00056, "", "NuFIT", "H", "pmns",
               "sin^2 theta_13 (reactor); TBM value 0 -> this is the TBM-breaking angle"),
        Target("pmns_deltaCP", 197.0, 27.0, "deg", "NuFIT", "L", "pmns",
               "Dirac CP phase ~ 1.2 pi; poorly constrained, ~consistent with pi at 1-2 sigma"),
        Target("pmns_theta12", 33.41, 0.75, "deg", "NuFIT", "H", "pmns",
               "theta_12 = asin(sqrt(0.303)); solar ~ 33.4 deg (TBM 35.26 deg)"),
        Target("pmns_theta23", 49.1, 1.0, "deg", "NuFIT", "M", "pmns",
               "theta_23 = asin(sqrt(0.572)); atm ~ 49 deg (near-maximal 45 deg)"),
        Target("pmns_theta13", 8.54, 0.11, "deg", "NuFIT", "H", "pmns",
               "theta_13 = asin(sqrt(0.02203)); reactor ~ 8.5 deg (was 0 in exact TBM)"),
        # Majorana phases: unknown (only if Majorana). Logged as fully-unknown placeholders.
        Target("pmns_alpha21", 0.0, 180.0, "deg", "NuFIT", "L", "pmns",
               "Majorana phase alpha_21: UNKNOWN (only if Majorana); sigma=full range",
               is_bound=True),
        Target("pmns_alpha31", 0.0, 180.0, "deg", "NuFIT", "L", "pmns",
               "Majorana phase alpha_31: UNKNOWN (only if Majorana); sigma=full range",
               is_bound=True),
    ]

    # ---------------------------------------------------------------------
    # 9. ANOMALOUS MAGNETIC MOMENTS (g-2) — a_l = (g-2)/2
    # ---------------------------------------------------------------------
    T += [
        Target("a_e", 1.15965218059e-3, 0.00000000013e-3, "", "CODATA", "H", "moment",
               "electron anomalous moment a_e=(g-2)/2; rel err ~1e-10 (a precision test, not free)"),
        Target("a_mu", 1.16592059e-3, 0.00000022e-3, "", "PDG", "H", "moment",
               "muon anomalous moment a_mu (2023 world avg); rel err ~1.9e-7"),
    ]

    # ---------------------------------------------------------------------
    # 10. WIDTHS / LIFETIMES (where measured) — a few representative ones
    # ---------------------------------------------------------------------
    T += [
        Target("Gamma_Z", 2.4955, 0.0023, "GeV", "PDG", "H", "width",
               "Z total width"),
        Target("Gamma_W", 2.085, 0.042, "GeV", "PDG", "M", "width",
               "W total width"),
        Target("Gamma_H", 3.7e-3, 1.4e-3, "GeV", "PDG", "L", "width",
               "Higgs total width (poorly measured directly); SM ~4.1 MeV"),
        Target("tau_mu", 2.1969811e-6, 2.2e-12, "s", "PDG", "H", "lifetime",
               "muon lifetime; rel err ~1e-6"),
        Target("tau_tau", 2.903e-13, 0.005e-13, "s", "PDG", "H", "lifetime",
               "tau lifetime"),
        Target("tau_n", 878.4, 0.5, "s", "PDG", "M", "lifetime",
               "free neutron lifetime (beam/bottle tension ~ a few sigma)"),
    ]

    return T


def _build_derived(reg: Dict[str, Target]) -> List[Target]:
    """DERIVED dimensionless ratios + Koide invariants, with PROPAGATED uncertainty."""
    g = reg.__getitem__
    D = []  # noqa

    # --- charged-lepton ratios (sharp; the prime search targets) ---
    D += [
        ratio(g("m_mu"), g("m_e"), "r_mu_e", "m_mu/m_e ~ 206.768; SHARP target", conf="H"),
        ratio(g("m_tau"), g("m_mu"), "r_tau_mu", "m_tau/m_mu ~ 16.817"),
        ratio(g("m_tau"), g("m_e"), "r_tau_e", "m_tau/m_e ~ 3477.2"),
        ratio(g("m_p"), g("m_e"), "r_p_e", "m_p/m_e ~ 1836.15; the famous one (QCD, not Yukawa)", conf="H"),
        ratio(g("m_n"), g("m_p"), "r_n_p", "m_n/m_p ~ 1.00138"),
    ]

    # --- quark ratios (blunt: light-quark errors dominate -> mostly LOW conf) ---
    D += [
        ratio(g("m_c"), g("m_u"), "r_c_u", "m_c/m_u ~ 588 (light-quark error dominated)"),
        ratio(g("m_t"), g("m_c"), "r_t_c", "m_t/m_c ~ 136"),
        ratio(g("m_s"), g("m_d"), "r_s_d", "m_s/m_d ~ 19.9"),
        ratio(g("m_b"), g("m_s"), "r_b_s", "m_b/m_s ~ 44.7"),
        ratio(g("m_t"), g("m_b"), "r_t_b", "m_t/m_b ~ 41.3 (SHARP-ish: both H/M)"),
        ratio(g("m_b"), g("m_tau"), "r_b_tau", "m_b/m_tau ~ 2.35 (GUT b-tau unification target)"),
    ]

    # --- GST mass-mixing target: sqrt(m_d/m_s) vs Cabibbo lambda ---
    md, ms = float(g("m_d").value), float(g("m_s").value)
    val = math.sqrt(md / ms)
    rel = 0.5 * _quad(g("m_d").rel_precision, g("m_s").rel_precision)
    D.append(Target("sqrt_md_ms", val, val * rel, "", "DERIVED", "L", "ckm",
                    "sqrt(m_d/m_s); Gatto-Sartori-Tonin ~ |V_us| (mass-mixing interlock test)"))

    # --- Koide invariants (the live interlock) ---
    D.append(koide_Q(g("m_e"), g("m_mu"), g("m_tau"), "koide_Q_lep",
                     "Koide Q charged leptons ~ 0.66666 (the 2/3 interlock; ~ -9e-6 from 2/3)"))
    D.append(sqrt_mass_angle(g("m_e"), g("m_mu"), g("m_tau"), "koide_theta_lep"))
    D.append(koide_Q(g("m_u"), g("m_c"), g("m_t"), "koide_Q_up",
                     "Koide Q up-quarks ~ 0.85 (!= 2/3 -> cross-fermion FALSIFIES naive cube-Koide)"))
    D.append(koide_Q(g("m_d"), g("m_s"), g("m_b"), "koide_Q_down",
                     "Koide Q down-quarks ~ 0.73 (!= 2/3)"))

    # --- neutrino mass-squared splitting ratio (NO) ---
    D.append(ratio(g("Dm2_31_NO"), g("Dm2_21"), "r_Dm2_atm_sol",
                   "|Dm^2_31|/Dm^2_21 ~ 33.8 (NO); the nu mass-splitting hierarchy ratio"))

    # --- cross-sector complementarity numbers (computed, with naive propagation) ---
    # quark-lepton complementarity: theta_C + theta_12^PMNS (should be ~45 deg if real)
    tc = g("ckm_theta12"); t12 = g("pmns_theta12")
    qlc = float(tc.value) + float(t12.value)
    qlc_sig = _quad(tc.sigma, t12.sigma)
    D.append(Target("qlc_sum", qlc, qlc_sig, "deg", "DERIVED", "H", "cross_sector",
                    "theta_C + theta_12^PMNS (quark-lepton complementarity; ~45 deg if real)"))
    # theta_13^PMNS vs lambda/sqrt2 (charged-lepton correction to TBM)
    lam = g("ckm_lambda")
    lam_over_root2 = float(lam.value) / math.sqrt(2.0)
    sin_t13 = math.sin(math.radians(float(g("pmns_theta13").value)))
    D.append(Target("pmns_sin_t13", sin_t13,
                     math.cos(math.radians(float(g("pmns_theta13").value)))
                     * math.radians(float(g("pmns_theta13").sigma)),
                     "", "DERIVED", "H", "pmns",
                     f"sin(theta_13^PMNS) ~ {sin_t13:.4f}; compare lambda/sqrt2 = {lam_over_root2:.4f}"))

    # --- Higgs quartic lambda = m_H^2/(2 v^2) ---
    mH, vh = g("m_H"), g("v_higgs")
    lam_h = float(mH.value) ** 2 / (2 * float(vh.value) ** 2)
    lam_h_rel = _quad(2 * mH.rel_precision, 2 * vh.rel_precision)
    D.append(Target("higgs_lambda", lam_h, lam_h * lam_h_rel, "", "DERIVED", "H", "higgs",
                    "Higgs self-coupling lambda = m_H^2/2v^2 ~ 0.129"))

    return D


# =============================================================================
# THE LOADER
# =============================================================================

class PDGDataset:
    """The loaded dataset. Construct once; query by key or sector; partition by precision."""

    def __init__(self):
        self._reg: Dict[str, Target] = {}
        for t in _build_measured():
            self._reg[t.key] = t
        for t in _build_derived(self._reg):
            self._reg[t.key] = t

    # ---- accessors ----
    def __getitem__(self, key: str) -> Target:
        return self._reg[key]

    def __contains__(self, key: str) -> bool:
        return key in self._reg

    def __iter__(self):
        return iter(self._reg.values())

    def __len__(self):
        return len(self._reg)

    def keys(self) -> List[str]:
        return list(self._reg.keys())

    def get(self, key: str) -> Tuple[float, float, float, float]:
        """(value, sigma, rel_precision, n_digits_known) — the brief's required accessor."""
        return self._reg[key].as_tuple()

    def target(self, key: str) -> Target:
        return self._reg[key]

    def sector(self, name: str) -> List[Target]:
        return [t for t in self._reg.values() if t.sector == name]

    def sectors(self) -> List[str]:
        seen = []
        for t in self._reg.values():
            if t.sector not in seen:
                seen.append(t.sector)
        return seen

    # ---- precision partitions (good vs weak search targets) ----
    def precise_targets(self, rel_thresh: float = 1e-3, include_bounds: bool = False) -> List[Target]:
        """Well-measured targets (rel error < thresh): the GOOD search targets."""
        out = []
        for t in self._reg.values():
            if t.is_bound and not include_bounds:
                continue
            if t.rel_precision < rel_thresh:
                out.append(t)
        return sorted(out, key=lambda x: x.rel_precision)

    def weak_targets(self, rel_thresh: float = 1e-3, include_bounds: bool = True) -> List[Target]:
        """Poorly-measured targets (rel error >= thresh): WEAK; quarantine from tight-fit claims."""
        out = []
        for t in self._reg.values():
            if t.is_bound:
                if include_bounds:
                    out.append(t)
                continue
            if t.rel_precision >= rel_thresh:
                out.append(t)
        return sorted(out, key=lambda x: -x.rel_precision)

    def dimensionless(self, include_holdout: bool = False) -> List[Target]:
        """Targets with units == '' (ratios, couplings, sin^2, Q) — the anonymizable search pool.

        HOLDOUT IS EXCLUDED BY DEFAULT (see HOLDOUT_KEYS below). Pass include_holdout=True only to
        SCORE a survivor's prediction, never to search.
        """
        return [t for t in self._reg.values()
                if t.units == "" and (include_holdout or t.key not in HOLDOUT_KEYS)]

    # ---- held-back validation set (added 2026-07-27) ------------------------------------------
    # WHY. GATE_POWER_ANALYSIS.py showed a single-target match is statistically empty beyond depth
    # ~10-13, because the expression count 30^(D-4) outruns any fixed measurement precision. So
    # essentially all of the gate's discriminating power lives in Gate C's cross-sector interlock.
    # But an interlock that FITS every target it touches is still a fit: k targets used, k fitted,
    # nothing predicted -- and a JACKPOT would then be UNFALSIFIABLE, hence unpublishable.
    # The fix is out-of-sample prediction. Two targets are held back and MUST NOT be searched:
    #   koide_Q_lep  -- TIGHT (rel ~1e-5), the charged-lepton Koide invariant
    #   r_tau_mu     -- LOOSE (rel ~1e-4), m_tau/m_mu
    # Both are flavour-sector, so a survivor fitted elsewhere must REACH them rather than be shown
    # them. One tight and one loose on purpose: the tight one tests whether the relation is sharp,
    # the loose one whether it is even in the right place.
    # A survivor is a RESULT only if it predicts BOTH inside error without having used either.
    #
    # CAVEAT ON THE TIGHT ONE, recorded so it is not over-credited: koide_Q_lep is measured at
    # 0.666660511 +/- 6.8e-6, and the exact value 2/3 sits only 0.91 sigma away. So a survivor that
    # lands on 2/3 PASSES this holdout -- but 2/3 has been the known answer since Koide (1981), so
    # hitting it is not a novel prediction, only a consistency check. r_tau_mu = 16.8170 +/- 0.0011 has
    # no famous closed form, which makes it the STRONGER of the two tests despite being the looser.
    # Read a JACKPOT accordingly: r_tau_mu is the one that carries information.
    def holdout(self) -> List[Target]:
        """The held-back validation targets. For SCORING a prediction only -- never for searching."""
        return [self._reg[k] for k in HOLDOUT_KEYS if k in self._reg]

    def is_holdout(self, key: str) -> bool:
        return key in HOLDOUT_KEYS

    def fittable(self, rel_thresh: float = 1e-2) -> List[Target]:
        """Dimensionless targets a search MAY fit: precise enough, and not held back."""
        return [t for t in self.precise_targets(rel_thresh=rel_thresh)
                if t.units == "" and t.key not in HOLDOUT_KEYS]

    def score_holdout(self, key: str, predicted: float) -> Tuple[float, float, bool]:
        """Score a survivor's PREDICTION for a held-back target.

        Returns (sigma_offset, rel_offset, passes_2sigma). The only legitimate use of the holdout:
        `predicted` must come from an expression fixed on the OTHER targets.
        """
        t = self._reg[key]
        # cast through float: this dataset carries mpmath values, and returning mpf breaks caller
        # f-string formatting and JSON serialisation downstream.
        val, sg = float(t.value), float(t.sigma)
        pred = float(predicted)
        sig = abs(pred - val)/sg if sg > 0 else float("inf")
        return sig, abs(pred - val)/abs(val), bool(sig <= 2.0)


# ---------------------------------------------------------------------------------------------
# THE HELD-BACK VALIDATION SET. Do not add to a search pool. See PDGDataset.holdout() for why.
HOLDOUT_KEYS: frozenset = frozenset({"koide_Q_lep", "r_tau_mu"})


# module-level singleton + convenience function (mirrors hali_flow's load pattern)
_DATASET: Optional[PDGDataset] = None


def load() -> PDGDataset:
    global _DATASET
    if _DATASET is None:
        _DATASET = PDGDataset()
    return _DATASET


def get(key: str) -> Tuple[float, float, float, float]:
    """Top-level convenience: (value, sigma, rel_precision, n_digits_known) for a target key."""
    return load().get(key)


# =============================================================================
# SCRIPT ENTRY — print the loaded table
# =============================================================================

def _fmt(x, width=16):
    try:
        return f"{float(x):.10g}".ljust(width)
    except Exception:
        return str(x).ljust(width)


def _print_table():
    ds = load()
    print("=" * 118)
    print(f"PDG_CONSTANTS — project_atomos particle-physics target dataset"
          f"   (mpmath={'on' if _HAVE_MP else 'OFF (float fallback)'})")
    print("=" * 118)
    hdr = (f"{'key':22} {'value':>17} {'sigma':>14} {'rel_err':>11} "
           f"{'n_dig':>6} {'conf':>4} {'src':>7}  {'sector':<13} units")
    measured = [t for t in ds if t.source != "DERIVED"]
    derived = [t for t in ds if t.source == "DERIVED"]

    print("\n--- MEASURED OBSERVABLES ---------------------------------------------------"
          "-----------------------------------------")
    print(hdr)
    print("-" * 118)
    for t in measured:
        bound = " (BOUND)" if t.is_bound else ""
        print(f"{t.key:22} {_fmt(t.value,17)[:17]:>17} {_fmt(t.sigma,14)[:14]:>14} "
              f"{t.rel_precision:>11.2e} {t.n_digits:>6.1f} {t.conf:>4} {t.source:>7}  "
              f"{t.sector:<13} {t.units}{bound}")

    print("\n--- DERIVED (ratios, Koide, cross-sector; propagated uncertainty) ----------"
          "-----------------------------------------")
    print(hdr)
    print("-" * 118)
    for t in derived:
        print(f"{t.key:22} {_fmt(t.value,17)[:17]:>17} {_fmt(t.sigma,14)[:14]:>14} "
              f"{t.rel_precision:>11.2e} {t.n_digits:>6.1f} {t.conf:>4} {t.source:>7}  "
              f"{t.sector:<13} {t.units}")

    # precision partition
    precise = ds.precise_targets(1e-3)
    weak = ds.weak_targets(1e-3)
    print("\n" + "=" * 118)
    print(f"PRECISION PARTITION (threshold rel_err < 1e-3 = 'good search target')")
    print("=" * 118)
    print(f"PRECISE (good) targets [{len(precise)}]:  "
          + ", ".join(t.key for t in precise[:30]) + (" ..." if len(precise) > 30 else ""))
    print(f"WEAK   targets [{len(weak)}]:  "
          + ", ".join(f"{t.key}({t.rel_precision:.1e})" for t in weak[:30])
          + (" ..." if len(weak) > 30 else ""))

    # sanity-check the live Koide interlock + 2/3
    Q = ds.target("koide_Q_lep")
    th = ds.target("koide_theta_lep")
    print("\n" + "=" * 118)
    print("LIVE-INTERLOCK SANITY CHECK")
    print("=" * 118)
    print(f"  Koide Q (leptons)     = {float(Q.value):.8f}  +/- {float(Q.sigma):.2e}   "
          f"(2/3 = {2/3:.8f}; dev = {float(Q.value)-2/3:+.2e} = "
          f"{abs(float(Q.value)-2/3)/float(Q.sigma):.1f} sigma)")
    print(f"  Koide angle (leptons) = {float(th.value):.5f} deg +/- {float(th.sigma):.2e}  "
          f"(45 deg if Q=2/3)")
    print(f"  Koide Q (up quarks)   = {float(ds.target('koide_Q_up').value):.5f}   (!= 2/3)")
    print(f"  Koide Q (down quarks) = {float(ds.target('koide_Q_down').value):.5f}   (!= 2/3)")
    qlc = ds.target("qlc_sum")
    print(f"  theta_C + theta12_PMNS= {float(qlc.value):.2f} deg +/- {float(qlc.sigma):.2f}  "
          f"(quark-lepton complementarity; 45 deg if real)")

    # counts
    n_total = len(ds)
    n_meas = len(measured)
    n_der = len(derived)
    n_dimless = len(ds.dimensionless())
    print("\n" + "=" * 118)
    print(f"COUNT: {n_total} targets total  ({n_meas} measured + {n_der} derived); "
          f"{n_dimless} dimensionless (anonymizable search pool); "
          f"{len(precise)} precise / {len(weak)} weak; sectors: {', '.join(ds.sectors())}")
    print("=" * 118)
    return ds


if __name__ == "__main__":
    _print_table()
