# Independent review of the four-dimensional S4 pion packet

**Primary verdict: proved as written for the specified determinant.** The round-S4, positive-mass, minimally coupled LO real-pion determinant has heat coefficients
\[
(a_0,a_1,a_2,a_3)=(1,2,29/15,74/63).
\]
After the stated local \(H^0,H^2,H^4\) action-density subtractions,
\[
f_{\rm real,res}=-{a_3H^6\over32\pi^2M^2}+O(H^8/M^4),\qquad
\rho_{\rm real,res}=+{a_3H^6\over64\pi^2M^2}+O(H^8/M^4).
\]
The coefficient of a linear \(H\) term is zero in this defined massive determinant, at fixed positive \(M\) before \(H\to0\). This is not a full-QCD statement.

The raw harmonic/Hurwitz derivation was saved in INDEPENDENT_DERIVATION.md before the coordinator's packet was read. A fresh child received the scalar problem without the proposed coefficient list and derived the same answer by hand. The QCD-E parent independently checked the residue arithmetic, stress factor and multiplicity. No new numerical or symbolic experiment was executed.

## Checks of the supplied packet

The reviewed files are coordinator/curved_pion/DERIVATION.md, check_pion.py, contract.json, SOURCES.json and run_001/manifest.json at the hashes in INPUT_PROVENANCE.json. The later wrapper REPORT.md was also read for final claim calibration.

1. The scalar spectrum follows from degree-\(\ell\) harmonic polynomials in \(\mathbb R^5\); trace subtraction gives the stated degeneracy. The \(\ell=0\) eigenvalue is \(M^2>0\). Removing it as a zero mode would change the determinant.
2. Shifting \(\ell\) to \(\ell+3/2\), the extra half-integer \(1/2\) term vanishes. The Hurwitz residues give the stated four heat coefficients. This independently confirms the table-based normalization.
3. The real scalar factor is \(+\frac12\log\det\), whose proper-time representation has the minus sign used in the packet. The first unsubtracted heat term is \(a_3H^6s^3\), and its massive integral is \(1/M^2\).
4. Constant metric rescaling gives \(V\mapsto e^{4\sigma}V\), \(H\mapsto e^{-\sigma}H\), hence \(\rho=f-Hf_H/4\) at fixed \(M\). The \(H^6\) factor is \(-1/2\), reversing the sign of the leading residual.
5. A charged complex pion contains two real modes, not four. Thus, for shifted-minus-unshifted mass squared,
\[
\delta\rho_{\pi^\pm}
={a_3H^6\over32\pi^2}
\left[{1\over M^2+\Delta}-{1\over M^2}\right]+O(H^8).
\]
It is negative for \(\Delta>0\). At \(\Delta=2e^2F^2Z\), its zero-charge derivative is
\[
\left.\partial_{e^2}\delta\rho_{\pi^\pm}\right|_0
=-{a_3F^2Z H^6\over16\pi^2M^4}+O(H^8).
\]
6. The proper-time remainder argument is sufficient for zero linear-\(H\) coefficient. For fixed positive \(M\), the large-\(u\) part is exponentially suppressed and the bounded small-\(u\) remainder gives \(O(H^8/M^4)\). No mere finite-grid fit or mass-derivative integration constant is being used to infer the zero coefficient.
7. The third mass derivative of the formal full real-scalar determinant is \((1/V)\sum_\ell d_\ell/\lambda_\ell^3\). Its sign and factor are correct. The paired polygamma identity for the convergent sum is correct by differentiating the positive partial fractions. The code's lower-term subtraction in its \(H^6\) estimator is consistent with that identity.

The installed manifest validator accepts the coordinator's run_001 evidence record against the reviewed files. This review did not rerun the numerical suite or independently certify its numerical tolerances. The independent hand derivation supplies a separate check of the load-bearing coefficients and signs.

## One notation qualification

The resolvent paragraph writes \(\partial_{(M^2)}^3 f=(1/V)\sum d_\ell/\lambda_\ell^3\). Here \(f\) means the full determinant modulo its UV-polynomial definition, not the specifically defined \(f_{\rm res}\) with mass-dependent \(H^0,H^2,H^4\) heat pieces removed. Those removed pieces have nonzero third mass derivatives. The displayed numerical expansion and estimator correctly contain and subtract the lower terms, so no result or code correction follows. This clarification is recorded here instead of mutating the frozen derivation run input.

## Curved-space chiral operators and the exact scope

The LO minimally coupled pion operator is the correct normalized target. Full curved chiral EFT also permits independent higher-order couplings. An exact source check of [Megías–Ruiz Arriola–Salcedo, arXiv:hep-ph/0504271v2, equation (71)](https://arxiv.org/abs/hep-ph/0504271v2) confirms the operator structures
\[
L_{11}R\langle\nabla U^\dagger\nabla U\rangle,\quad
L_{12}R_{\mu\nu}\langle\nabla^\mu U^\dagger\nabla^\nu U\rangle,\quad
L_{13}R\langle\chi^\dagger U+U^\dagger\chi\rangle,
\]
plus curvature-squared contacts. The source uses its own curvature signs and quark-model estimates; only the allowed structures are used here, with no model values imported.

A concrete illustration shows why the full fixed-mass \(H^6\) coefficient is not determined by the minimal loop. A scalar shift \(\xi R\), \(R=12H^2\), multiplies the heat kernel by \(e^{-12\xi H^2s}\), giving
\[
a_3(\xi)={74\over63}-{116\over5}\xi+144\xi^2-288\xi^3.
\]
An \(R\chi\) chiral insertion can induce \(\xi\) proportional to \(M^2/F^2\). It therefore changes a fixed-mass \(H^6\) coefficient through terms of order \(H^6/F^2\), while the LO \(H^6/M^2\) infrared singularity remains the leading small-mass pion contribution in regular chiral counting. This example is a matching qualification, not a replacement of the stipulated LO action by an arbitrary nonminimal scalar.

Further curvature contacts and interacting pion/photon loops also need matching. A pure mass-independent \(cR^3\) term cancels if an artificial shifted-minus-unshifted comparison holds exactly the same \(c\) fixed. It must not be claimed that every \(R^3\) term necessarily contaminates that particular difference. Charge/mass-dependent curvature matching, additional operators, and the physical comparison path remain separate obligations.

Local curvature polynomials do not generate a linear \(H\) term on a closed round sphere. That observation and the computed pion determinant do not settle any proposed nonlocal/topological contribution in the full QCD generating functional, its state, metric stress or subtraction. The calculation has the hierarchy \(H\ll M\ll\Lambda_\chi\); taking \(M\to0\) at fixed \(H\) invalidates this expansion. Its charged mass-shift function is not a complete electromagnetic calculation and uses no target alpha.

## Restricted Einstein-branch check

The wrapper's additional algebra is correct. For three equal-mass zero-charge pion modes the retained loop stress gives
\[
H^2={8\pi G\over3}{3a_3H^6\over64\pi^2M^2},
\qquad
H^4={8\pi M^2\over Ga_3}
\]
on a putative nonzero branch. With \(M_{\rm Pl}=G^{-1/2}\),
\[
{H\over M}=\left({8\pi\over a_3}\right)^{1/4}
\left({M_{\rm Pl}\over M}\right)^{1/2}.
\]
It is large for a hadronic \(M\ll M_{\rm Pl}\), contradicting the required \(H/M\ll1\). Thus the algebraic nonzero root cannot be claimed within this approximation; the wrapper correctly treats it as outside the domain. The check does not solve modified gravitational equations with additional curvature matching or establish absence of a full-theory branch.

## Remaining obligation and provenance

For the specified minimal positive-mass determinant, no missing coefficient/sign implication remains. For the physical proposal, the missing implication is the independently specified full curved QCD state and matched stress response, including the sectors omitted from the pion determinant.

The child and parent derivations are separate within the same program, not an external referee report. The child did not read coordinator material before returning its raw result. The parent read the supplied packet only after saving that independent derivation. Source authentication and exact hashes are in SOURCES.json; mathematical proofreading self-review covered the raw equations and this review. No parent/coordinator input was changed.
