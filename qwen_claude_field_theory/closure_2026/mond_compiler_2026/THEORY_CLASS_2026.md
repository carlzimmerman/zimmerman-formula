# OUR THEORY CLASS — derived from the session's no-gos + passes (2026-08-29)

Not a literature remix.  Assembled from what we PROVED works and forbidden by what we PROVED fails.

## Design rules (each grounded in a committed result)
R1  carrier couples LINEARLY to the metric, not quadratically through the MOND flux
      [T3, dirac_Phi_Q_sf42: Sigma^TF, J both ~ dL/dX => Sigma_P=0 <=> J=0; elim of quadratic carrier
       gives stress ~ f^2 vs obstruction ~ f]
R2  no preferred timelike direction (no vector / lapse-khronon / phi_dot_c)   [AeST 1/K_B; disformal alpha_2]
R3  carrier = auxiliary spatial TRACE-FREE tensor Q_ij, second-class removable [det KK!=0, verified 2x;
       Q supplies a spatial DIRECTION (lensing needs it) with no FRAME (alpha_2 safe)]
R4  MOND sector must not weight the lapse; keep H_perp FIRST class   [lapse-tied + sf42 both -> 3 DOF]
R5  FREEZE mu(y)=1-e^{-y} (elliptic); realized by aux-Legendre chi (V'=-[ln(1-chi)]^2) or nonlocal F+
R6  if locality fails R1-R4, SPATIAL (never temporal) nonlocality is licensed [DEFW/F+], but must not
      reintroduce a mode (banked warning omega^2=(1/2)c^2 k^2)

## The class
Single metric g (matter minimal) + aux trace-free Q_ij (no Q-dot) + aux-Legendre chi.
The forced structural move (R1 x R3): couple Q to TWO objects --
    S_Q = int Q^ij [ f(chi) A_ij + lambda R_ij ] - (1/2) Q^ij KK_ijkl Q^kl
  A_ij = [D_i Phi D_j Phi]^TF (MOND source), R_ij = a LINEAR curvature object (3-Ricci / K_ij), KK = kernel.
Eliminate Q =>  physical stress ~ f(chi) A . KK^{-1} . R   (LINEAR in A, LINEAR in R separately)
  => the lensing stress is CURVATURE-sourced, MODULATED by the MOND flux -- NOT the flux squared.
  This is the escape from T3 that no chassis tried.

## Status: DESIGN.  Nothing here is verified viable.
  Inherited PASS: Q_ij second-class removal (proven); mu=1-e^{-y} (frozen, elliptic).
  UNTESTED (in order): (1) does the cross-term f A KK^{-1} R actually CANCEL Sigma_P on-shell so Phi=Psi
    (profile-match is NECESSARY not sufficient -- T3 lesson); (2) does R_ij coupling keep H_perp first
    class (R^(3)_ij has no lapse -- promising, but K_ij does => choose carefully); (3) DOF/Dirac rank;
    (4) alpha_1, alpha_2 (Q is boost-scalar-coupled + spatial TF => hope PPN-dark, must COMPUTE);
    (5) KK^{-1} nonlocality health; (6) c_T; (7) cosmology.
  Two variants to test: R_ij = R^(3)_ij (spatial Ricci, no lapse -- R4 safe) vs R_ij = K_ij (extrinsic).

## Decisive first test (cheapest, singular):
  weak-field static: does eliminating Q with source [f A + lambda R^(3)] produce a traceless metric
  stress that cancels Sigma_P = -mu s^2 (covariant) or y mu' (lapse) EXACTLY, for some (lambda, KK)?
  If NO for all lambda,KK -> the class is dead, and Part-I/T3 upgrade to "+ linear-curvature TT carriers".
  If YES -> run DOF + alpha_2.
