# TP01 follow-up discriminators (before execution)

The completed 729-case fixed-coupling threshold scan finds a repeated
pressure boundary. Test its scaling origin and the validity of interpreting
the local radial branch, without promoting it to the unknown full quantum
vacuum.

1. Symbolically derive STr M^2 and STr M^4 by traces of the representation
   matrices, and compare the latter with
   6 f^2 h^2 lambda^2(29 lambda^2-200g^2)/(30h^2+lambda^2)^2.
2. At critical g, derive mass-squared units c=f h lambda^2/(30h^2+lambda^2)
   and coordinate z=hX/sqrt(c). Verify universal scaling and absence of log c
   in the one-loop CW shape; the singlet sector cancels identically.
3. On h=lambda=0.6, locate minimum, compressibility boundary and W_ss=0
   with direct mpmath differentiation (distinct from finite-difference
   derivative extraction), comparing the .005/.0025 scan roots. Compute
   actual positive tree scalar gaps and canonical radial masses on radial
   branch samples X/Xmin={1.05,1.12,1.2,1.3,1.5}. No claim that the massless
   R phase, Goldstino or unbroken gauge sector has been integrated out.
4. Quantify rather than suppress the old leading-log two-loop curvature
   relative to the newly computed finite one-loop curvature. For h=lambda
   in {0.03,0.1,0.3,0.6,1}, report this diagnostic; the smallest two are
   weak-coupling controls of this same model, not new fitted models.
5. Reconstruct total P=U_s/3-U and density rho proportional to
   [U_s exp(2s)/2]^(3/5) on each positive-source sample; directly differentiate
   to verify dP/dlnrho. Signs are accepted only well away from zero after
   the independent derivative comparison. Uniform higher-loop bounds are
   not established by this finite check.

50-digit/80-digit mpmath and exact rational SymPy, one thread, 180 seconds
wall and 170 CPU seconds. macOS does not support CPU affinity and rejected
the requested address-space cap; retain failed manifest and report measured
RSS instead. No generated output is substituted into an earlier manifest.
