"""
agentSS Part 6 — KMS/modular detailed balance analytically + what it does/doesn't fix.

The continuous thermal weight grows at large |omega| (Part 5) -> not a normalizable line by itself;
it is a spectral DENSITY. The roton-building object (agentRR) is a SINGLE peaked active resonance
(center s_g, width Gamma). The QNM tower / GH state supplies CANDIDATE such peaks (each rung is a pole
= a Lorentzian-like peak of width Gamma_n). The right test: take ONE QNM resonance as the gain line and
ask whether modular covariance (KMS) FIXES its line-shape moment ratio.

(A) KMS / detailed balance is a relation between rho(+w) and rho(-w). For a SINGLE peak centered at
    s_g>0 with width Gamma, KMS says there is a thermal IMAGE peak at -s_g with weight e^{-s_g/T}. This
    fixes the RELATIVE weight of the image, NOT the SHAPE (skew) of the peak itself. The central
    moments j2, j3 of the peak depend on its intrinsic profile (Lorentzian: j2~Gamma^2, but a pure
    Lorentzian has DIVERGENT moments; a QNM pole truncated by the band gives finite, profile-set j2,j3).

(B) Modular flow = boost = static-patch time translation. It acts as DILATION on the spectral variable
    (omega -> e^{lambda} omega under a boost by rapidity lambda). A symmetry that DILATES the spectral
    axis CANNOT fix a dimensionless ratio of moments to a SPECIFIC number unless that number is a fixed
    point of the dilation. 4 j3/j2^2 has dimension [s]^{3-2*... } -> check scaling weight.
"""
import sympy as sp

s, c1, c2, c3, alpha = sp.symbols('s c1 c2 c3 alpha', positive=True)
# Under modular dilation s -> e^{alpha} s, central moments scale as j_n -> e^{n alpha} j_n.
# Ratio 4 j3/j2^2 -> e^{3a} j3 / (e^{2a} j2)^2 = e^{3a-4a} (4 j3/j2^2) = e^{-a} (4 j3/j2^2).
print("=== (B) Scaling of 4 j3/j2^2 under modular dilation s->e^{alpha} s ===")
weight = 3 - 2*2   # 3a from j3, -4a from j2^2
print(f"  j3 scales as e^(3 alpha), j2^2 scales as e^(4 alpha)")
print(f"  => 4 j3/j2^2 scales as e^({weight} alpha) = e^(-alpha)  -- DIMENSION -1, NOT scale-invariant.")
print(f"  => modular dilation MOVES the ratio; the only fixed point is 0 or infinity.")
print(f"  => modular/Tomita-Takesaki flow CANNOT pin 4 j3/j2^2 to a finite nonzero G_sat: a dilation")
print(f"     symmetry rescales it. It is a covariant (weight-(-1)) object, not an invariant. PERMITS.")
print()

# (C) KMS detailed balance: does it fix the SKEW of a single rung? The skew comes from the intrinsic
# QNM profile. KMS relates the n-th rung to its thermal image but says nothing about the rung's own
# j3/j2^{3/2}. Demonstrate: a Lorentzian of any center/width satisfies the SAME KMS image relation, yet
# has free (center,width) -> free moments.
print("=== (C) KMS fixes the image weight e^{-s_g/T}, not the peak skew ===")
print("  A single retarded pole at s_g - i Gamma has spectral peak rho(w) = (Gamma/pi)/((w-s_g)^2+Gamma^2).")
print("  KMS supplies an image at -s_g with weight e^{-s_g/T}. The peak's intrinsic (s_g, Gamma) are")
print("  FREE (set by the QNM, i.e. by Delta and lambda) -> j2, j3 of the gain line are free.")
print("  => KMS/modular: PERMITS, does NOT force 4 j3/j2^2 = G_sat.")
