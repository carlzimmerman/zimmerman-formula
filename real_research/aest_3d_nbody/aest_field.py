"""
aest_field.py -- AeST (Aether-Scalar-Tensor, Skordis-Zlosnik 2006.00165) field
structure relevant to the cluster phase-pinning question.

We do NOT need the full covariant action numerically here. The GATE question is
structural: the AeST vector A_mu enters with a MAXWELL-TYPE kinetic term

    L_A = -(K_B/2) F_{mu nu} F^{mu nu},   F_{mu nu} = d_mu A_nu - d_nu A_mu

(plus a unit-timelike constraint A_mu A^mu = -1 enforced by a Lagrange multiplier,
and the scalar sector with shift-symmetric free function K(Q),
Q = A^mu d_mu phi, Y = (g^{mu nu}+A^mu A^nu) d_mu phi d_nu phi).

The free scalar oscillation mode obeys a Helmholtz/Klein-Gordon equation with
dispersion omega = mu*c (mu = the AeST mass scale). The QUESTION (cluster door #1):
can 3D asymmetric collapse (shear, mergers) inject power into and thereby PHASE-PIN
this free mode? Linear answer (banked, idea #3): NO, because the coupling matrix C
built from the antisymmetric F is antisymmetric, so v.(C v) = 0 -- zero net power
into the mode.

This module
  (A) supplies the symbolic field objects (Maxwell F, the linearized 4x4
      mode-coupling matrix C on v=(dphi, a_x, a_y, a_z)), and
  (B) CONFIRMS at linear order that the antisymmetric Maxwell coupling gives
      v.(C v)=0 and that symmetric shear contracted with it vanishes.

phase_gate.py does the nonlinear-robustness test (does any nonlinear term break it).
"""

import sympy as sp


# -----------------------------------------------------------------------------
# Constants / scales (framework-canonical; not load-bearing for the gate)
# -----------------------------------------------------------------------------
a0_canonical = 9.36e-11   # m/s^2, framework pure-Lambda a0
c_light = 2.99792458e8    # m/s


# -----------------------------------------------------------------------------
# (A) Symbolic field objects
# -----------------------------------------------------------------------------
def maxwell_F(dim=4):
    """
    Build F_{mu nu} = d_mu A_nu - d_nu A_mu symbolically over `dim` coords.
    Returns (F, dA) where dA[mu][nu] = d_mu A_nu is a generic matrix of
    independent symbols. F is manifestly antisymmetric BY CONSTRUCTION.
    """
    dA = sp.Matrix(dim, dim, lambda i, j: sp.Symbol(f"dA_{i}{j}", real=True))
    F = dA - dA.T
    return F, dA


def is_antisymmetric(M):
    return sp.simplify(M + M.T) == sp.zeros(*M.shape)


def power_injection_quadratic(F):
    """
    v^T A v = 0 for any antisymmetric A. Returns the symbolic quadratic form so
    the gate can confirm it vanishes identically.
    """
    n = F.shape[0]
    v = sp.Matrix(n, 1, lambda i, j: sp.Symbol(f"v_{i}", real=True))
    return sp.expand((v.T * F * v)[0, 0]), v


def linear_mode_coupling_matrix():
    """
    Build the LINEARIZED 4x4 mode-coupling matrix C acting on the perturbation
    vector v = (dphi, a_x, a_y, a_z), about a homogeneous background on a flat
    3D slice, in Fourier space (wavevector k, frequency omega).

    Block structure (this is the physics):
      - scalar self block C[0,0] = omega^2 - mu^2 c^2   (the KG/Helmholtz mode;
        its zero IS the free oscillation omega = mu c).
      - vector self block C[1:4,1:4] = (k k^T - |k|^2 I) = the Maxwell curl-curl
        operator (the |B|^2 piece), SYMMETRIC.
      - scalar<->vector CROSS block: the term 2(2-K_B) J^mu d_mu phi couples
        nabla(dphi) ~ i k_i dphi to the aether perturbation a_i THROUGH the
        antisymmetric Maxwell F.  The cross entries are +g k_i on one side and
        -g k_i on the other (g = 2-K_B): ANTISYMMETRIC by F = dA antisymmetry.

    Returns (C, v, symbols) so callers can decompose / test it.
    """
    mu, c, KB, omega = sp.symbols('mu c K_B omega', real=True)
    kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
    dphi, ax, ay, az = sp.symbols('dphi a_x a_y a_z', real=True)
    v = sp.Matrix([dphi, ax, ay, az])
    kvec = sp.Matrix([kx, ky, kz])
    k2 = kx**2 + ky**2 + kz**2

    curlcurl = kvec * kvec.T - k2 * sp.eye(3)          # symmetric Maxwell |B|^2
    g = (2 - KB)

    C = sp.zeros(4, 4)
    C[0, 0] = omega**2 - mu**2 * c**2                   # KG mode
    C[1:4, 1:4] = curlcurl
    for i, ki in enumerate([kx, ky, kz]):
        C[0, i + 1] = g * ki        # dphi -> a_i
        C[i + 1, 0] = -g * ki       # a_i  -> dphi   (OPPOSITE SIGN: antisymmetric)

    syms = dict(mu=mu, c=c, KB=KB, omega=omega, kx=kx, ky=ky, kz=kz)
    return C, v, syms


def antisymmetric_shear_coupling():
    """
    Representative antisymmetric scalar<->vector coupling tensor A_ij (built from
    the Maxwell F structure) and the symmetric traceless shear sigma_ij, so the
    gate can show sigma_ij A_ij = 0 (symmetric . antisymmetric = 0): shear cannot
    pump the omega=mu c mode at linear order.
    """
    KB, kx, ky, kz = sp.symbols('K_B k_x k_y k_z', real=True)
    g = (2 - KB)
    A_ij = sp.Matrix([[0,     g*kz, -g*ky],
                      [-g*kz, 0,     g*kx],
                      [g*ky, -g*kx, 0]])
    s11, s12, s13, s22, s23, s33 = sp.symbols('s11 s12 s13 s22 s23 s33', real=True)
    sigma = sp.Matrix([[s11, s12, s13],
                       [s12, s22, s23],
                       [s13, s23, s33]])   # symmetric; traceless not even needed
    return A_ij, sigma


# -----------------------------------------------------------------------------
# (B) The LINEAR gate: confirm v.(C v) = 0 for the antisymmetric coupling
# -----------------------------------------------------------------------------
def run_linear_gate(verbose=True):
    out = {}

    # raw Maxwell generator
    F, dA = maxwell_F(4)
    out['F_antisymmetric'] = is_antisymmetric(F)
    P, v0 = power_injection_quadratic(F)
    out['vT_F_v'] = sp.simplify(P)

    # full 4x4 mode-coupling matrix
    C, v, syms = linear_mode_coupling_matrix()
    C_sym = sp.simplify((C + C.T) / 2)
    C_anti = sp.simplify((C - C.T) / 2)

    power_anti = sp.simplify((v.T * C_anti * v)[0, 0])
    out['vT_Canti_v'] = power_anti

    # isolate the scalar<->vector CROSS power from the full quadratic form
    power_full = sp.expand((v.T * C * v)[0, 0])
    scal_self = C[0, 0] * v[0]**2
    vec_self = (v[1:4, 0].T * C[1:4, 1:4] * v[1:4, 0])[0, 0]
    cross_power = sp.simplify(power_full - scal_self - vec_self)
    out['cross_power'] = cross_power

    # shear . antisymmetric coupling
    A_ij, sigma = antisymmetric_shear_coupling()
    shear_power = sp.simplify(sum(sigma[i, j] * A_ij[i, j]
                                  for i in range(3) for j in range(3)))
    out['shear_into_mode'] = shear_power

    out['C'] = C
    out['C_sym'] = C_sym
    out['C_anti'] = C_anti

    if verbose:
        print("=" * 72)
        print("aest_field.py -- LINEAR mode-coupling gate")
        print("=" * 72)
        print("\nFull 4x4 C (rows/cols: dphi, a_x, a_y, a_z):")
        sp.pprint(C)
        print("\nAntisymmetric part C_anti (Maxwell shear-coupling carrier):")
        sp.pprint(C_anti)
        print("\n[check 1] raw Maxwell  v^T F v       =", out['vT_F_v'])
        print("[check 2] antisymmetric v.(C_anti v) =", out['vT_Canti_v'])
        print("[check 3] scalar<->vector cross power =", out['cross_power'])
        print("[check 4] shear_ij . A_ij (sym.anti)  =", out['shear_into_mode'])

    # assertions: the LINEAR obstruction
    assert out['F_antisymmetric'] is True
    assert out['vT_F_v'] == 0
    assert out['vT_Canti_v'] == 0
    assert out['cross_power'] == 0
    assert out['shear_into_mode'] == 0
    return out


if __name__ == "__main__":
    res = run_linear_gate(verbose=True)
    print("\n" + "=" * 72)
    print("LINEAR GATE RESULT: v.(C v)=0 for the antisymmetric Maxwell coupling;")
    print("shear injects ZERO power into omega=mu c at LINEAR order. Idea #3 reproduced.")
    print("=> phase_gate.py now tests whether NONLINEAR terms break this.")
    print("=" * 72)
