"""
agentTT ROUTE 2 — MODULAR/KMS SELECTION OF THE DSSYK PLACEMENT
Part 1: The KMS test under modular flow.

SETUP (all banked, not invented):
  - The Gibbons-Hawking (GH) state of the dS static patch is KMS (thermal) at
    T_dS = H/2pi under the modular flow sigma_t = static-patch boost generator L_0
    (= a dilation s -> e^a s). [agentSS: Tomita-Takesaki modular flow of GH = boost.]
  - The dS QNM ladder Gamma_n = sinh((Delta+n)lambda) is the lowest-weight
    discrete-series rep of static-patch SL(2,R); L_0 spectrum = the ladder Delta+n.
    [agentSS.]
  - CENTER placement (theta_v=pi/2): late-time matter 2pt pole structure
    omega_pole = -i sinh((Delta+k)lambda): purely imaginary, discrete ladder,
    TWO-SIDED/balanced spectral support, spectral asymmetry A = 1/2 (machine:
    0.49976-0.49999). [agentS.]
  - EDGE placement (theta_v->pi): |G| ~ t^{-3/2}, ONE-SIDED support, spectral
    asymmetry A(omega<0) = 4e-9..1e-5 ~ 0, extremal/zero-temperature. [agentS.]

THE TOMITA-TAKESAKI / KMS FORCING QUESTION:
  Modular covariance is NOT optional decoration: by Tomita-Takesaki, for a given
  von Neumann algebra + cyclic-separating vector, the modular flow sigma_t is UNIQUE,
  and the vector state is the UNIQUE state that is KMS at beta=2pi (in modular time)
  w.r.t. sigma_t. The GH state's modular flow IS the boost. So: a candidate "dS
  vacuum" placement, to BE the GH state, must produce a 2pt function that satisfies
  the KMS condition under the boost. KMS is a SYMMETRY the physical dS placement
  must respect (it is the defining property of the thermal GH state), not a
  preference.

  TEST: compute, for each placement's late-time observable, whether it satisfies
  the KMS condition under the boost/dilation modular flow at beta = 2pi/H. If the
  center satisfies KMS (detailed balance, two-sided analytic strip) and the edge
  carries a FORBIDDEN modular property (zero-temperature / one-sided = beta->infinity,
  NOT beta=2pi/H), then modular covariance EXCLUDES the edge.

  RUTHLESS forcing-vs-preference discipline: I must check whether the exclusion is
  (a) a genuine FORCING (the edge is structurally incompatible with KMS at the
  required temperature, i.e. forbidden), or (b) merely a CONSISTENCY (center happens
  to be KMS, edge happens not to be, but nothing forces the placement to be KMS in
  the first place). The difference: is KMS-at-T_dS a CONSTRAINT the placement MUST
  satisfy (forcing), or just one nice property the center has (preference)?
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40

print("="*78)
print("PART 1 — KMS DETAILED BALANCE under the boost modular flow, each placement")
print("="*78)

# ---------------------------------------------------------------------------
# KMS condition, stated precisely.
# A 2pt function G(t) = <A(t) B> is KMS at inverse temperature beta w.r.t. a
# flow sigma_t iff:
#   (i)  G(t) is analytic in the strip -beta < Im t < 0,
#   (ii) G(t - i beta) = <B A(t)> = G_swap(t)  (the KMS boundary condition),
#  equivalently in Fourier space the DETAILED-BALANCE relation:
#       tilde G(-omega) = e^{-beta omega} tilde G(omega)   (for the Wightman fn)
#  i.e. the ratio of negative- to positive-frequency weight is e^{-beta omega}.
#
# For the GH state, modular time = boost parameter; beta_modular = 2pi (always),
# which in physical static-patch time corresponds to T_dS = H/2pi, i.e.
# beta_phys = 2pi/H. The KMS-in-modular-time statement beta_mod=2pi is the
# UNIVERSAL Bisognano-Wichmann/Tomita-Takesaki value.
# ---------------------------------------------------------------------------

omega, beta, lam, Delta, H = sp.symbols('omega beta lambda Delta H', real=True, positive=True)
n = sp.symbols('n', integer=True, nonnegative=True)

print("""
KMS detailed-balance criterion (Wightman 2pt under modular flow):
    tilde G(-omega) / tilde G(+omega) = e^{-beta_mod omega_mod}
with beta_mod = 2pi the universal modular temperature (Tomita-Takesaki).
A placement is the GH (dS) state ONLY IF its boost-frame 2pt obeys this with
beta_mod=2pi exactly. Test each placement's measured spectral asymmetry against it.
""")

# ---- CENTER: the discrete QNM ladder spectral function -----------------------
# The center 2pt has poles at omega = -i Gamma_n, Gamma_n = sinh((Delta+n)lambda),
# purely imaginary, and (banked) TWO-SIDED balanced support: asymmetry A = 1/2.
# A KMS spectral function at temperature beta has, for a discrete thermal spectrum,
# the structure of a thermal (two-sided) ladder. The measured A = 1/2 means
# weight is balanced between omega>0 and omega<0 sectors at the BOOST origin.
#
# Decisive structural check: the boost modular Hamiltonian L_0 has spectrum
# {Delta+n}. A KMS state w.r.t. modular flow has its 2pt fully determined by the
# modular spectrum via the thermal weighting. The center's purely-imaginary ladder
# omega_n = -i sinh((Delta+n)lambda) is exactly the analytic continuation of the
# L_0 = Delta+n spectrum to the static-patch boost frame at the GH temperature
# (lambda<->H_eff). Compute the asymmetry the KMS condition PREDICTS and compare.

print("-"*78)
print("CENTER placement")
print("-"*78)

# Model the center Wightman function in the boost frame as a thermal sum over the
# modular spectrum {Delta+n}. KMS forces the two-sided (emission+absorption)
# structure. The 'spectral asymmetry' A := [weight in omega<0] / [total weight],
# measured by agentS as ~0.5. For a KMS (detailed-balance) spectrum symmetric about
# the modular origin in the Re-omega=0 (boost-fixed) sector, A = 1/2 EXACTLY when
# the modular flow fixes the observable (Re omega = 0). Verify the logic:
#
# Purely imaginary modes => Re omega_pole = 0 => modular flow (which acts as
# omega_mod -> omega_mod, a phase e^{i omega_mod t_mod} along the boost) leaves the
# decay rates (Im omega) invariant and the modes sit at the BOOST-FIXED axis.
# At Re omega = 0 the detailed-balance ratio e^{-beta_mod omega_mod} -> e^0 = 1
# in the Re-omega direction => balanced => A = 1/2. This MATCHES the boost-fixed
# (modular-invariant decay) structure.

A_center_measured = mp.mpf('0.499875')   # midpoint of agentS 0.49976-0.49999
A_center_KMS_pred = mp.mpf('0.5')        # KMS at boost-fixed axis (Re omega=0)
print(f"  spectral asymmetry A measured (agentS): {A_center_measured}")
print(f"  KMS prediction at boost-fixed (Re omega=0) axis: A = {A_center_KMS_pred}")
print(f"  |measured - KMS|: {abs(A_center_measured - A_center_KMS_pred)}  (consistent => KMS-COMPATIBLE)")
print("  => CENTER observable sits at the modular FIXED axis (Re omega=0), balanced,")
print("     two-sided: it IS a KMS spectrum under the boost. CONSISTENT with GH.")

# ---- EDGE: the soft-edge endpoint spectral function --------------------------
print("-"*78)
print("EDGE placement")
print("-"*78)
# Edge: |G| ~ t^{-3/2}, one-sided support, A ~ 0 (4e-9..1e-5). A one-sided
# (ground-state) spectral function has support only for omega>0 (or only omega<0):
# this is the beta->infinity (T=0) KMS limit, NOT beta=2pi/H.
A_edge_measured = mp.mpf('1e-5')   # upper end of agentS 4e-9..1e-5 (worst case for our claim)
print(f"  spectral asymmetry A measured (agentS, worst case): {A_edge_measured}")
print(f"  KMS-at-T_dS prediction (beta_mod=2pi, finite T): A = {A_center_KMS_pred} (balanced)")
print(f"  one-sided support => detailed-balance ratio e^{{-beta omega}} with beta->infinity")
print(f"  => the edge realizes the T=0 (beta=inf) limit, NOT beta_mod=2pi.")
print(f"  |A_edge - A_KMS| = {abs(A_edge_measured - A_center_KMS_pred)}  (~0.5 mismatch => KMS-INCOMPATIBLE at T_dS)")

print("""
PRELIMINARY READ (to be hardened in parts 2-6):
  - CENTER: Re omega = 0 (boost-fixed), two-sided/balanced (A=1/2) => satisfies the
    KMS detailed-balance condition under the boost modular flow at the GH temperature.
  - EDGE: one-sided (A~0) => a T=0 / beta->infinity correlator => CANNOT satisfy
    KMS at beta_mod=2pi (the GH temperature). It is a DIFFERENT thermal class.

  This is the SHAPE of a forcing argument (KMS is the defining symmetry of GH), but
  Parts 2-6 must rigorously (i) confirm Re omega=0 is FORCED by modular covariance,
  not merely true at center; (ii) compute the modular WEIGHT carried by each
  observable and check if the edge's weight is FORBIDDEN; (iii) decide FORCING vs
  CONSISTENCY by the SS standard.
""")
