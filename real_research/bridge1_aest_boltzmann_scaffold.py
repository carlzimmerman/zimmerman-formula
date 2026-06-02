#!/usr/bin/env python3
"""
Bridge 1 scaffold: theta-coupled AeST for a modified Boltzmann run -- a STARTING FRAMEWORK.
===========================================================================================

This is the code skeleton for the decisive Bridge-1 calculation (BRIDGE_TO_UNIFICATION.md):
does scaling-MOND (a0 -> a0(z)=cH/Z) keep AeST's CMB fit? It is NOT a finished calculation,
and it does NOT fake one. Discipline:

  [DONE]  runs and is correct: the background H(z)/a0(z), the AQUAL free function with the
          right Newton/deep-MOND limits + the a0(z) substitution, and the C_ell chi^2 harness.
  [TODO]  the AeST-specific perturbation source terms raise NotImplementedError with a precise
          pointer to Skordis-Zlosnik 2021 -- I will not write fake field equations that look
          real but are wrong (the whole point of this repo's audit).
  [TOOL]  the perturbation solve is meant to live inside hi_class/CLASS (it already does the
          photon/neutrino Boltzmann hierarchy + EFT-of-DE); this file specifies what to add.

A cosmologist with the paper + hi_class can finish this. Run: python <thisfile>
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)        # = sqrt(32pi/3) = 5.78881


# ====================================================================================
# SECTION 1 -- background cosmology  [DONE: runs, correct]
# ====================================================================================
@dataclass
class Background:
    """theta-coupled AeST background. At the background level the scalar mimics dust
    (Omega_phi_dust), so H(z) is LCDM-like; a0(z)=cH/Z is derived; the EFE parameter
    g_ext/a0 = Z is constant (bridge1_aest_qsa_scoping.py)."""
    H0_kms: float = 67.4
    Ob: float = 0.0493
    Ophi_dust: float = 0.2657      # the scalar's CDM-mimicking mode (a0-INDEPENDENT)
    OL: float = 0.685
    Or: float = 9.2e-5

    @property
    def H0(self) -> float:
        return self.H0_kms * 1e3 / MPC

    @property
    def Om(self) -> float:
        return self.Ob + self.Ophi_dust

    def E(self, z: float) -> float:
        return math.sqrt(self.Om * (1 + z) ** 3 + self.OL + self.Or * (1 + z) ** 4)

    def H(self, z: float) -> float:
        return self.H0 * self.E(z)

    def a0(self, z: float) -> float:
        """the premise: a0(z) = cH(z)/Z = c*theta/(3Z), theta = div A = 3H."""
        return c * self.H(z) / Z

    def efe_ratio(self, z: float) -> float:
        """g_ext/a0 = cH / (cH/Z) = Z -- exact, epoch-independent."""
        return c * self.H(z) / self.a0(z)

    def rho_phi_dust(self, z: float) -> float:
        """the CMB-fitting mode: ~ (1+z)^3, a0-independent (kg/m^3)."""
        rho_c0 = 3 * self.H0 ** 2 / (8 * math.pi * G)
        return self.Ophi_dust * rho_c0 * (1 + z) ** 3


# ====================================================================================
# SECTION 2 -- the AQUAL free function / interpolation  [DONE: correct limits + a0(z)]
# ====================================================================================
def mu_interp(x: float, kind: str = "simple") -> float:
    """MOND interpolation mu(x), x=|grad phi|/a0. mu->1 (x>>1, Newton), mu->x (x<<1, deep-MOND).
    In AeST this is fixed by the free function K(Y); here are the two standard choices used
    to fit galaxies. The SCALING enters by evaluating x at a0(z), not a constant a0."""
    if kind == "simple":
        return x / (1 + x)
    if kind == "standard":
        return x / math.sqrt(1 + x * x)
    raise ValueError(kind)


def galaxy_force(gN: float, a0z: float, kind: str = "simple") -> float:
    """solve mu(g/a0) g = gN for the MOND acceleration g, given a0(z). [DONE]
    deep-MOND check: gN<<a0 -> g -> sqrt(gN a0)."""
    g = math.sqrt(gN * a0z) if gN < a0z else gN          # seed
    for _ in range(80):                                   # fixed-point
        x = g / a0z
        g = gN / mu_interp(x, kind) if x > 0 else gN
    return g


# ====================================================================================
# SECTION 3 -- linear perturbations  [TODO: AeST terms now SOURCED in bridge1_aest_equations.md]
# ====================================================================================
# The actual AeST equations (action Eq.5, background, perturbations Eqs.11-12, the MOND/dust
# limits, and the theta-coupling a0->a0(theta)=c*theta/(3Z)) are transcribed from arXiv:2007.00082
# in real_research/bridge1_aest_equations.md. KEY (sourced): a0 lives in the F(Y) spatial sector;
# the CMB dust-mode lives in K(Q) temporal sector -> running a0 leaves the dust-mode untouched.
# The stubs below are no longer black boxes -- they point to the specific sourced equations to
# transcribe (verifying exact coefficients vs the PDF) and SOLVE inside hi_class.
@dataclass
class Perturbations:
    """Linear perturbation variables (conformal Newtonian gauge), Fourier mode k.
    The metric (Phi, Psi), the scalar (dphi), the aether (the vector's perturbation V),
    and the matter species couple through the Einstein + scalar + aether equations.
    Photons/neutrinos are the standard Boltzmann hierarchy (provided by CLASS)."""
    k: float
    Phi: float = 0.0
    Psi: float = 0.0
    dphi: float = 0.0          # scalar perturbation -- the CDM-mimicking 'dust mode' lives here
    ddphi: float = 0.0
    V_aether: float = 0.0      # aether (vector) perturbation
    delta_b: float = 0.0       # baryon density contrast
    theta_b: float = 0.0       # baryon velocity divergence
    # photons/neutrinos: handled by the host Boltzmann code (CLASS hierarchy)
    meta: dict = field(default_factory=dict)


def scalar_perturbation_source(p: Perturbations, bg: Background, z: float):
    """RHS of the perturbed scalar EOM delta(box phi) = source.
    [TODO] This is the crux: the source contains the free function's second derivative
    K''(Y_bg) evaluated on the background, which (a) carries the dust-mode that fits the CMB
    and (b) is where a0(z) enters via Y_bg = (d phi_bg/dt)^2-dependence. Needs:
      * Skordis-Zlosnik 2021 (PRL 127,161302) Eqs. for delta-phi (their Sec. on perturbations);
      * the free function K(Y) and its derivatives at the cosmological background;
      * the theta-coupling: a0 -> a0(z), so the MOND-scale parameter in K becomes time-dependent.
    DO NOT fabricate -- transcribe from the paper."""
    raise NotImplementedError(
        "scalar perturbation source: use chi=phi+phidot*alpha, gamma=phidot-phidot*Psi; the EOM "
        "is driven by dK/dQ (Q-sector) with a0 entering only via F's Y-sector terms. See "
        "bridge1_aest_equations.md (arXiv:2007.00082 Eqs. 11-12); promote a0->a0(theta)=c*theta/3Z.")


def aether_perturbation_source(p: Perturbations, bg: Background, z: float):
    """RHS of the perturbed unit-timelike-vector (aether) EOM.
    [TODO] Needs the AeST vector sector (the 'K_B' kinetic term + the unit constraint's
    Lagrange multiplier perturbation). This sector is what keeps c_GW=c and what the
    theta-coupling acts through (theta = div A). Transcribe from the paper; do not invent."""
    raise NotImplementedError(
        "aether perturbation source: AeST Eq. 12  K_B(Edot + H E) = (dK/dQ) chi - (2-K_B)[...]; "
        "see bridge1_aest_equations.md. The vector sector keeps c_GW=c and carries theta=div A.")


def einstein_constraints(p: Perturbations, bg: Background, z: float):
    """Perturbed Einstein 00 and 0i (the modified Poisson + momentum constraints), with the
    scalar and aether stress-energy perturbations on the RHS.
    [TODO] standard structure, but the scalar+aether T^munu perturbations need Sections 3 above."""
    raise NotImplementedError("Einstein constraints: assemble once scalar+aether sources exist.")


def evolve_perturbations(bg: Background, k: float, z_start=1e7, z_end=0.0):
    """Integrate the coupled system (metric + scalar + aether + matter + the CLASS photon/
    neutrino hierarchy) from deep radiation domination to today, for mode k.
    [TODO -> hi_class] This is NOT a from-scratch ODE here: it belongs inside a Boltzmann
    code. The realistic path: patch hi_class -- it already evolves the metric + matter +
    photon/neutrino hierarchy + a general scalar (EFT-of-DE / Horndeski). What must be ADDED:
      1. the unit-timelike VECTOR (aether) sector + its constraint (not in vanilla hi_class);
      2. the AeST free function K(Y) with the MOND-scale parameter promoted to a0(z)=cH/Z;
      3. output the transfer functions -> C_ell.
    Returns the source functions needed for the line-of-sight C_ell integral."""
    raise NotImplementedError(
        "evolve_perturbations: implement in hi_class (add the aether sector + a0(z) K(Y)). "
        "Vanilla CLASS/hi_class lacks the unit-vector field; that is the code work to do.")


# ====================================================================================
# SECTION 4 -- C_ell comparison harness  [DONE: runs; real Planck loader hooked]
# ====================================================================================
def chi2_TT(Cl_model, Cl_planck, sigma):
    """chi^2 of a model TT spectrum against Planck binned TT. [DONE]"""
    return sum(((m - d) / s) ** 2 for m, d, s in zip(Cl_model, Cl_planck, sigma))


def third_peak_ratio(Cl, ells, peak3=(780, 830)):
    """The discriminating observable: 3rd-peak height (the CDM/dust tracer). [DONE]
    Returns mean D_ell over the 3rd acoustic peak window; the dust-mode survival test."""
    band = [Cl[i] for i, l in enumerate(ells) if peak3[0] <= l <= peak3[1]]
    return sum(band) / len(band) if band else float("nan")


def load_planck_TT(path="data/planck_TT_binned.txt"):
    """Load Planck binned TT (ell, D_ell, sigma). [DONE structure -- needs the data file]
    Planck 2018 binned TT is public (PLA / the COM_PowerSpect_CMB-TT-binned product)."""
    try:
        rows = [line.split() for line in open(path) if line.strip() and not line.startswith("#")]
        return ([float(r[0]) for r in rows], [float(r[1]) for r in rows],
                [float(r[2]) for r in rows])
    except FileNotFoundError:
        return None


# ====================================================================================
def main():
    bg = Background()
    print("#" * 84)
    print("# Bridge 1 scaffold -- status of each piece")
    print("#" * 84)

    print("\n[DONE] SECTION 1 background (LCDM-like; scalar mimics dust; a0=cH/Z derived):")
    print(f"   {'z':>7}{'H [1/s]':>12}{'a0(z)':>12}{'g_ext/a0':>10}{'rho_phi_dust':>14}")
    for z in (0, 1, 1100, 3400):
        print(f"   {z:>7}{bg.H(z):>12.3e}{bg.a0(z):>12.3e}{bg.efe_ratio(z):>10.3f}{bg.rho_phi_dust(z):>14.3e}")
    print("   (g_ext/a0 = Z = 5.789 at all z -- the exact invariant; rho_phi_dust ~ (1+z)^3.)")

    print("\n[DONE] SECTION 2 AQUAL free function -- correct limits, evaluated at a0(z):")
    a0_now = bg.a0(0)
    for gN in (1e-12, 1e-10, 1e-8):
        g = galaxy_force(gN, a0_now)
        dm = math.sqrt(gN * a0_now)
        print(f"   gN={gN:.0e}: g={g:.3e}  (deep-MOND sqrt(gN a0)={dm:.3e}, ratio {g/dm:.3f})")

    print("\n[DONE] SECTION 4 C_ell harness self-test (synthetic):")
    ells = list(range(2, 1000, 2))
    model = [5000 * math.exp(-((l - 220) / 200) ** 2) for l in ells]
    data = [m * 1.0 for m in model]
    sig = [max(0.02 * d, 1.0) for d in data]
    print(f"   chi^2(model vs itself) = {chi2_TT(model, data, sig):.3f} (0 expected)")
    print(f"   3rd-peak D_ell (synthetic) = {third_peak_ratio(model, ells):.1f}")
    print(f"   Planck TT loader: {'found' if load_planck_TT() else 'data file not on disk (public, hook it)'}")

    print("\n[TODO] SECTION 3 perturbations -- the decisive, not-yet-done physics:")
    for fn in (scalar_perturbation_source, aether_perturbation_source, evolve_perturbations):
        print(f"   - {fn.__name__}: NotImplementedError (needs Skordis-Zlosnik 2021 + hi_class)")

    print("\n" + "=" * 84)
    print("  NET: the background, the galaxy-force law (with a0(z)), and the C_ell comparison")
    print("  harness are DONE and correct. The decisive step -- the AeST scalar+aether")
    print("  perturbations with a0->a0(z), solved through recombination -- is scoped and stubbed,")
    print("  NOT faked. Finish it by patching hi_class (add the vector sector + a0(z) K(Y)) and")
    print("  checking the 3rd-peak/dust-mode survives. That single run decides Bridge 1.")
    print("=" * 84)


if __name__ == "__main__":
    main()
