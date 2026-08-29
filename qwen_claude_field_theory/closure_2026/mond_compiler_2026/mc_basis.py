"""
mc_basis.py -- the FINITE covariant operator basis for the carrier multiplet.

Carrier multiplet  Xi_A  =  { phi , chi , A_mu , S_mn , lam }
    phi    shift-symmetric scalar (enters only through nabla_mu phi)  -- the MOND potential slot
    chi    ordinary scalar        -- the "constitutive"/algebraic slot (the archetype's chi)
    A_mu   vector                 -- aether / Palatini-distortion slot
    S_mn   symmetric traceless    -- higher-irrep slot (independent traceless stress)
    lam    Lagrange multiplier    -- constrained-multiplier sector

Rules (the anti-hiding discipline):
    * <= 2 derivatives per operator
    * <= quartic in the carrier (nabla_mu phi counts as ONE power of carrier)
    * NO free functions.  chi's potential is a POLYNOMIAL of degree <= 4.  Any nonlinear
      mu(y) must be an OUTPUT of eliminating an algebraic carrier, never an input.
    * gravity sector is FIXED: (1/16 pi G) R(g) with coefficient exactly 1.  Rescaling G
      is forbidden by G3, so R(g) is not a searchable operator.
    * the matter frame is a FINITE 4-parameter conformal+disformal map (see MFRAME below),
      not a free function.

Everything the Palatini/distortion archetype produces after integrating out an algebraic
distortion is a LINEAR COMBINATION of operators already in this basis (see
`PALATINI_ARCHETYPE` and mc_selftest.py, which verifies
    R(Gamma) = R(g) - 3 div A + 3 A^2
for C^a_mn = d^a_m A_n + d^a_n A_m by direct component computation).
"""
import sympy as sp

# --------------------------------------------------------------------------------------
# operator table.  each entry: (id, group, label, callable(ctx) -> sympy scalar)
# --------------------------------------------------------------------------------------

OPS = []


def _op(oid, group, label, fn):
    OPS.append(dict(id=oid, group=group, label=label, fn=fn))


# ---- group P : phi-sector (the MOND kinetic core).  X = (grad phi)^2 -------------------
_op("P1",  "P", "X = (grad phi)^2",                        lambda c: c.X)
_op("P2",  "P", "chi * X",                                 lambda c: c.chi * c.X)
_op("P3",  "P", "chi^2 * X",                               lambda c: c.chi**2 * c.X)
_op("P4",  "P", "X^2",                                     lambda c: c.X**2)
_op("P5",  "P", "A^2 * X",                                 lambda c: c.A2 * c.X)
_op("P6",  "P", "(A^mu d_mu phi)^2  [aether projector]",   lambda c: c.Adphi**2)
_op("P7",  "P", "S^mn d_m phi d_n phi",                    lambda c: c.Sdphidphi())
_op("P8",  "P", "chi * (A^mu d_mu phi)^2",                 lambda c: c.chi * c.Adphi**2)
_op("P9",  "P", "(A^mu d_mu phi) * div A",                 lambda c: c.Adphi * c.divA)
_op("P10", "P", "A^mu d_mu phi",                           lambda c: c.Adphi)
_op("P11", "P", "chi * A^mu d_mu phi",                     lambda c: c.chi * c.Adphi)

# ---- group V : algebraic / potential sector ------------------------------------------
_op("V1",  "V", "chi",                                     lambda c: c.chi)
_op("V2",  "V", "chi^2",                                   lambda c: c.chi**2)
_op("V3",  "V", "chi^3",                                   lambda c: c.chi**3)
_op("V4",  "V", "chi^4",                                   lambda c: c.chi**4)
_op("V6",  "V", "A^2",                                     lambda c: c.A2)
_op("V7",  "V", "chi * A^2",                               lambda c: c.chi * c.A2)
_op("V8",  "V", "chi^2 * A^2",                             lambda c: c.chi**2 * c.A2)
_op("V9",  "V", "(A^2)^2",                                 lambda c: c.A2**2)
_op("V10", "V", "S^mn S_mn",                               lambda c: c.S2)
_op("V11", "V", "chi * S^mn S_mn",                         lambda c: c.chi * c.S2)
_op("V12", "V", "S^mn A_m A_n",                            lambda c: c.SAA())
_op("V13", "V", "S^m_n S^n_p S^p_m",                       lambda c: c.S3())
_op("V14", "V", "(S^mn S_mn)^2",                           lambda c: c.S2**2)
_op("V15", "V", "lam (A^2 + 1)   [unit-timelike multiplier]", lambda c: c.lam * (c.A2 + 1))
_op("V16", "V", "lam * chi        [multiplier-frozen chi]",   lambda c: c.lam * c.chi)
_op("V17", "V", "S^mn A_m d_n phi",                        lambda c: c.SAdphi())
_op("V18", "V", "lam * (S^mn S_mn - 1)  [tensor-norm multiplier]",
    lambda c: c.lam * (c.S2 - 1))

# ---- group D : one covariant derivative ------------------------------------------------
_op("D1",  "D", "chi * div A",                             lambda c: c.chi * c.divA)
_op("D2",  "D", "chi^2 * div A",                           lambda c: c.chi**2 * c.divA)
_op("D3",  "D", "A^2 * div A",                             lambda c: c.A2 * c.divA)
_op("D4",  "D", "S^mn nabla_m A_n",                        lambda c: c.SdA())
_op("D5",  "D", "A_m nabla_n S^mn",                        lambda c: c.AdivS())
_op("D6",  "D", "chi * S^mn nabla_m A_n",                  lambda c: c.chi * c.SdA())
_op("D7",  "D", "S^mn A_m d_n chi",                        lambda c: c.SAdchi())
_op("D8",  "D", "lam * div A",                             lambda c: c.lam * c.divA)

# ---- group K : two derivatives (carrier kinetic) --------------------------------------
_op("K1",  "K", "(grad chi)^2",                            lambda c: c.dchi2)
_op("K2",  "K", "chi (grad chi)^2",                        lambda c: c.chi * c.dchi2)
_op("K3",  "K", "(div A)^2",                               lambda c: c.divA**2)
_op("K4",  "K", "F_mn F^mn",                               lambda c: c.F2())
_op("K5",  "K", "nabla_m A_n nabla^m A^n",                 lambda c: c.DAsq())
_op("K6",  "K", "chi (div A)^2",                           lambda c: c.chi * c.divA**2)
_op("K7",  "K", "chi F_mn F^mn",                           lambda c: c.chi * c.F2())
_op("K8",  "K", "nabla_m S_np nabla^m S^np",               lambda c: c.DSsq())
_op("K9",  "K", "nabla_m S^mn nabla^p S_pn",               lambda c: c.divSdivS())
_op("K10", "K", "nabla_m S^mn d_n chi",                    lambda c: c.divSdchi())
_op("K12", "K", "A^2 (grad chi)^2",                        lambda c: c.A2 * c.dchi2)
_op("K13", "K", "(A^mu d_mu chi)^2",                       lambda c: c.Adchi**2)
_op("K14", "K", "S^mn d_m chi d_n chi",                    lambda c: c.Sdchidchi())

# ---- group C : curvature couplings -----------------------------------------------------
_op("C1",  "C", "chi R",                                   lambda c: c.chi * c.Rs)
_op("C2",  "C", "chi^2 R",                                 lambda c: c.chi**2 * c.Rs)
_op("C3",  "C", "A^2 R",                                   lambda c: c.A2 * c.Rs)
_op("C4",  "C", "A^m A^n R_mn",                            lambda c: c.AAR())
_op("C5",  "C", "S^mn R_mn",                               lambda c: c.SR())
_op("C6",  "C", "chi S^mn R_mn",                           lambda c: c.chi * c.SR())
_op("C7",  "C", "d^m phi d^n phi R_mn",                    lambda c: c.dphidphiR())
_op("C8",  "C", "X R",                                     lambda c: c.X * c.Rs)

OP_IDS = [o["id"] for o in OPS]
OP_INDEX = {o["id"]: i for i, o in enumerate(OPS)}
N_OPS = len(OPS)

# --------------------------------------------------------------------------------------
# matter frame: a FINITE conformal + disformal map.  Matter and light couple to
#
#   g~_mn = e^{2(M1 phi + M2 chi)} [ g_mn + (M3 + M5 phi) A_m A_n
#                                        + (M4 + M6 phi) S_mn
#                                        + (M7 + M8 phi) d_m phi d_n phi ]
#
# The phi-DEPENDENCE of the disformal coefficients is essential and is not optional
# padding: it is exactly the TeVeS/AeST lensing mechanism.  With a conformal factor alone
# one gets Phi~ = Phi_E + c phi and Psi~ = Psi_E - c phi, so the lensing potential
# (Phi~+Psi~)/2 is UNCHANGED while the dynamical potential is MOND-enhanced -- the classic
# "conformal scalars do not lens" failure.  Bekenstein's disformal term
#     g~ = e^{-2 phi} g - 2 sinh(2 phi) A_m A_n
# is the point (M1, M5) = (-1, -4) of this family and gives Phi~ = Psi~ = Phi_N + phi.
# Without M5/M6/M8 the search would be structurally incapable of expressing the only
# construction known to pass G2, so the screen would be a rigged empty result.
# The coefficients are polynomials of degree <= 1 in the carrier: still a finite basis.
# --------------------------------------------------------------------------------------
MFRAME = ["M1_conf_phi", "M2_conf_chi", "M3_disf_AA", "M4_disf_S",
          "M5_disf_AA_phi", "M6_disf_S_phi", "M7_disf_dphidphi", "M8_disf_dphidphi_phi"]
N_MF = len(MFRAME)
N_PARAM = N_OPS + N_MF
PARAM_IDS = OP_IDS + MFRAME


# --------------------------------------------------------------------------------------
# named constructions -- coefficient vectors used to VALIDATE the pipeline
# --------------------------------------------------------------------------------------

def _vec(d):
    import numpy as np
    v = np.zeros(N_PARAM)
    for k, val in d.items():
        if k in OP_INDEX:
            v[OP_INDEX[k]] = val
        else:
            v[N_OPS + MFRAME.index(k)] = val
    return v


NAMED = {
    # AQUAL-like: chi(grad phi)^2 + polynomial V(chi), conformal matter coupling.
    # eliminating chi gives a genuinely nonlinear mu(y) with NO free function.
    # L = -chi X/2 - V(chi) with V(chi) = -chi^3/3 :  eliminating the ALGEBRAIC chi gives
    # a genuine MOND interpolation with NO free function (validated in mc_validate.py):
    #     mu(y) = (1/y) [ (sqrt(k^2 + 4y) - k)/2 ]^2 ,   k = sqrt(8/sqrt(2))
    # mu -> 1 (Newtonian, no rescaling of G) and mu -> y/k^2 (deep MOND).
    "AQUAL_chi_cubic":     dict(P2=-0.5, V3=1.0 / 3.0, M1_conf_phi=1.0),
    "AQUAL_chi_quadratic": dict(P2=-0.5, V2=0.5, M1_conf_phi=1.0),
    "AQUAL_chi_quartic":   dict(P2=-0.5, V4=0.25, M1_conf_phi=1.0),
    # TeVeS/AeST-like: the aether projector h^{mn} = g^{mn} + A^m A^n contracted with dphi
    # is exactly  X + (A.dphi)^2  = P1 + P6 ; with the unit-timelike multiplier V15
    # and a Maxwell kinetic term K4 for the aether.
    "AeST_projector":      dict(P2=-0.5, P8=-0.5, V3=1.0 / 3.0, V15=1.0, K4=-0.25,
                                M1_conf_phi=1.0),
    # Palatini vector distortion  C^a_mn = d^a_m A_n + d^a_n A_m :
    #   R(Gamma) = R(g) - 3 div A + 3 A^2 .  With 16 pi G = 1 the 3 A^2 lands on V6 with
    #   coefficient 3; the div A piece is a boundary term at constant coefficient.
    #   The algebraic constitutive field chi couples through W^2 = 25 A^2 -> V7.
    #   The A-equation is [3 + 25 chi] A_mu = 0 ; the DEGENERATE branch is chi = -3/25.
    # Bekenstein/TeVeS disformal frame on top of the AQUAL cubic core: the known G2 pass
    "TeVeS_disformal":     dict(P2=-0.5, V3=1.0 / 3.0, V15=1.0, K4=-0.25,
                                M1_conf_phi=-1.0, M5_disf_AA_phi=-4.0),
    # the same trick attempted with the symmetric-traceless carrier instead of a vector
    "TeVeS_S_disformal":   dict(P2=-0.5, V3=1.0 / 3.0, V18=1.0, K8=-0.5, K9=1.0,
                                M1_conf_phi=-1.0, M6_disf_S_phi=-4.0),
    # purely scalar disformal partner (Lorentz-invariant vacuum by construction)
    "Disformal_scalar":    dict(P2=-0.5, V3=1.0 / 3.0,
                                M1_conf_phi=-1.0, M7_disf_dphidphi=1.0),
    "PALATINI_ARCHETYPE":  dict(V6=3.0, V7=25.0, V2=-0.5, V1=0.0),
    "PALATINI_DEGENERATE": dict(V6=3.0, V7=25.0, V1=-3.0 / 25.0 * 2, V2=-0.5),
    # a pure ghost, for gate calibration
    "GHOST_probe":         dict(P1=+0.5),
}


def basis_json():
    out = dict(
        n_operators=N_OPS,
        n_matter_frame=N_MF,
        n_parameters=N_PARAM,
        gravity_sector="FIXED: (1/16 pi G) R(g), coefficient exactly 1 (G3 forbids rescaling G)",
        carrier_multiplet=dict(
            phi="shift-symmetric scalar (enters only via nabla_mu phi)",
            chi="scalar (algebraic/constitutive slot)",
            A_mu="vector",
            S_mn="symmetric traceless rank-2",
            lam="Lagrange multiplier (constrained-multiplier sector)"),
        operators=[dict(id=o["id"], group=o["group"], label=o["label"]) for o in OPS],
        matter_frame=dict(
            form="g~_mn = e^{2(M1 phi + M2 chi)} ( g_mn + M3 A_m A_n + M4 S_mn )",
            parameters=MFRAME),
        named_constructions={k: v for k, v in NAMED.items()},
        excluded=EXCLUDED,
    )
    return out


EXCLUDED = [
    "torsion / antisymmetric connection distortion (needs an independent 3-form; new field content)",
    "operators with >2 derivatives (Horndeski/Galileon box-phi terms, f(R), Gauss-Bonnet)",
    "operators of degree >4 in the carrier",
    "Riemann/Weyl couplings C_mnrs S^mn S^rs, R_mnrs A^m A^r ... (generically ghostly at 2 derivatives; deferred)",
    "parity-odd operators built with the Levi-Civita tensor (epsilon A F F~, Chern-Simons)",
    "nonlocal operators (box^{-1}) -- locality is an explicit premise of the Part-I no-go; leaving it is a SEPARATE programme, not this basis",
    "second copies of an irrep (two vectors, a third scalar)",
    "free functions of the carrier -- chi's potential is capped at quartic (V1..V4) by the anti-hiding discipline",
    "explicit extra mass scales -- all coefficients are dimensionless in units a0 = c = 1, 16 pi G = 1",
    "matter couplings beyond the 4-parameter conformal+disformal frame map (no pressure- or shear-couplings)",
    "S_0z (time-space) component in the STATIC reduction (parity/time-reversal odd); retained in full in the Hessian reduction",
]
