#!/usr/bin/env python3
"""
ATTACK Piece 3: is the evolving-a0 signal real, or a systematics/LCDM artifact?
===============================================================================

Piece 3 of THE_SURVIVING_THEORY.md is the empirical leg: a0(z)=a0(0)E(z)^p fits
p=0.80+/-0.17, with constant-a0 (p=0) rejected at 5sigma. Every other piece rests on
this. So before building more, try to KILL it. Three adversarial tests:

  [A] JACKKNIFE       -- is the 5sigma carried by one point? (leave-one-out)
  [B] INTER-METHOD    -- the two LOCAL points (same z) disagree, proving an unmodeled
       SYSTEMATIC        systematic. Fold it in: how much does the 5sigma degrade?
  [C] LCDM MIMIC      -- can standard halo evolution + sample selection fake the trend?

DISCIPLINE: this is an attack. I look for reasons the signal is NOT real and report them
straight. Same data as a0_powerlaw_confrontation.py. Run: python <thisfile>   (needs numpy)
"""
import numpy as np

OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)

# data: (z, a0 [1e-10], err, method/sample)
Z   = np.array([0.00, 0.05, 0.90])
A0  = np.array([1.20, 1.69, 2.38])
ERR = np.array([0.26, 0.13, 0.11])
SRC = ["SPARC rot.curves (local disks)", "Varasteanu z<0.08", "MUSE-DARK z~0.9 (IFU, 79 gal)"]


def fit(z, a, err):
    """Return (p_best, chi2_best, chi2_const, sigma_evolution)."""
    Ez = E(z)
    def A_best(p):
        Ep = Ez ** p
        return np.sum(a * Ep / err ** 2) / np.sum(Ep ** 2 / err ** 2)
    def chi2(p):
        return np.sum(((a - A_best(p) * Ez ** p) / err) ** 2)
    ps = np.linspace(-2, 4, 60001)
    cs = np.array([chi2(p) for p in ps])
    i = np.argmin(cs)
    dchi2 = chi2(0.0) - cs[i]                 # evidence for evolution vs constant (1 dof)
    return ps[i], cs[i], chi2(0.0), np.sqrt(max(dchi2, 0.0))


def attack_A():
    print("=" * 78)
    print("[A] JACKKNIFE -- leave each point out; does the evolution evidence survive?")
    print("=" * 78)
    p0, c0b, c0c, s0 = fit(Z, A0, ERR)
    print(f"   ALL 3 points:        p={p0:+.2f}   constant-a0 rejected at {s0:.1f}sigma")
    for k in range(3):
        m = np.array([j for j in range(3) if j != k])
        p, cb, cc, s = fit(Z[m], A0[m], ERR[m])
        note = ""
        if 0 in m and 1 in m and 2 not in m:
            note = "  <- only the two near-z=0 points remain: NO lever arm in z"
        print(f"   drop {SRC[k][:22]:22}: p={p:+6.2f}   constant rejected at {s:.1f}sigma{note}")
    print("   READ: dropping the single z~0.9 point collapses the evidence -- the lever arm")
    print("   (hence the whole 'evolution') is carried by ONE measurement, MUSE-DARK.\n")


def attack_B():
    print("=" * 78)
    print("[B] INTER-METHOD SYSTEMATIC -- the local pair proves the quoted errors are too small")
    print("=" * 78)
    # the two lowest-z points are at essentially the SAME z, so a0 cannot physically differ:
    d = A0[1] - A0[0]
    sd = np.hypot(ERR[0], ERR[1])
    print(f"   z=0.00 a0=1.20+/-0.26  and  z=0.05 a0=1.69+/-0.13 are at ~the same epoch")
    print(f"   (E=1.000 vs 1.025) yet differ by {d:.2f} ({d/sd:.1f}sigma). a0 CANNOT evolve in")
    print(f"   dz=0.05, so this gap is a pure INTER-METHOD SYSTEMATIC. Quoted errors miss it.")
    # the sigma_sys per point that reconciles the local pair (makes them ~1 sigma apart):
    s_recon = np.sqrt(max((d**2 - ERR[0]**2 - ERR[1]**2) / 2.0, 0.0))
    print(f"   sigma_sys needed to reconcile the local pair ~ {s_recon:.2f}e-10.\n")
    print("   Fold a common sigma_sys (added in quadrature to every point) and refit:")
    print(f"     {'sigma_sys':>10}{'p_best':>9}{'constant-a0 rejected at':>26}")
    for ss in (0.0, 0.10, 0.20, s_recon, 0.35, 0.50):
        err2 = np.hypot(ERR, ss)
        p, cb, cc, s = fit(Z, A0, err2)
        tag = "  <- reconciles local pair" if abs(ss - s_recon) < 1e-9 else ""
        print(f"     {ss:>10.2f}{p:>9.2f}{s:>22.1f}sigma{tag}")
    print("   READ: the sigma_sys the LOCAL pair already demands drops the constant-a0")
    print("   rejection from ~5sigma to ~2sigma. The '5sigma' assumed three heterogeneous")
    print("   measurements are commensurate to their tiny quoted errors -- the local pair")
    print("   falsifies that assumption directly.\n")


def attack_C():
    print("=" * 78)
    print("[C] LCDM MIMIC + selection -- can the trend be faked without fundamental a0(z)?")
    print("=" * 78)
    print("   The three a0's are DIFFERENT methods on DIFFERENT samples:")
    for z, s in zip(Z, SRC):
        print(f"     z={z:.2f}: {s}")
    print("   Two model-independent ways to fake a rising apparent-a0 with z, both real:")
    print("    1. LCDM RAR evolution: at higher z, halos are denser (rho~(1+z)^3 at fixed M)")
    print("       and galaxies more compact -> the acceleration scale where the RAR bends can")
    print("       shift upward. Simulations show the RAR is ~invariant but NOT exactly; tens-of-")
    print("       percent drift to z~1 is not excluded. That is the SAME sign as the signal.")
    print("    2. Selection: z~0.9 IFU samples pick massive, compact, dispersion-supported")
    print("       galaxies; local SPARC is rotation-supported disks. a0 inferred from")
    print("       dispersions vs rotation can differ systematically (interpolation-function and")
    print("       anisotropy dependence). A population offset mimics an epoch trend.")
    print("   Neither is computed here (both need sims / a homogeneous pipeline). The point is")
    print("   that 3 heterogeneous points CANNOT separate fundamental a0(z) from (1)+(2).\n")


def verdict():
    print("=" * 78)
    print("VERDICT -- Piece 3, downgraded honestly")
    print("=" * 78)
    print("   * The DIRECTION is real: a0 at z~0.9 sits above the local value in the data.")
    print("   * The '5sigma' is INFLATED: it rests on a single lever-arm point [A], and folding")
    print("     in the inter-method systematic the local pair already proves drops it to ~2sigma [B].")
    print("   * It is DEGENERATE with LCDM RAR-evolution + sample selection [C]; 3 heterogeneous")
    print("     points cannot tell fundamental a0(z) from a measurement/astrophysics trend.")
    print("   => HONEST STATUS: a ~2sigma HINT in the right direction, single-point-driven and")
    print("      LCDM-degenerate -- NOT a 5sigma detection. The premise is not yet empirically")
    print("      established. What would fix it: (i) a homogeneous a0(z) pipeline across z,")
    print("      (ii) a clean deep-MOND a0 at z>2, (iii) the JWST cross-channel COHERENCE test")
    print("      (M_dyn/M*~sqrt(E) AND BTFR~-logE AND sigma~E^1/4 together) -- which selection")
    print("      and halo evolution do NOT forge coherently. Piece 3 is a hint; Piece 8 is the test.")
    print("=" * 78)


def main():
    attack_A()
    attack_B()
    attack_C()
    verdict()


if __name__ == "__main__":
    main()
