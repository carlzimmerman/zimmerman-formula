# PDG kinematics source check

- Source question: verify the ordinary positive-energy relativistic two-body kinematic formulas used to translate a daughter recoil velocity into a mass gap.
- Bibliographic record: D. Miller and D. R. Tovey, reviewed August 2021; written by J. D. Jackson, January 2000, *Kinematics*, in S. Navas et al. (Particle Data Group), *Phys. Rev. D* **110**, 030001 (2024) and 2025 update.
- Exact version checked: official `rpp2025-rev-kinematics.pdf`, dated 1 December 2025, section 49.4.2, page 3, equations (49.16)-(49.17); definition of `beta=p/E` and `E^2-p^2=m^2` on page 1.
- Stable locator: [PDG official review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).
- Date checked: 2026-09-12.
- Acquisition: project-local clock-response reports were searched for `PDG` and `rpp.*kinematics`; no cached record was found in that bounded scope. The official PDF was opened through the web tool. The relevant extracted text was read directly. No PDF or copyrighted text was copied to local files; local cache hash is therefore not applicable.
- Authentication: official `pdg.lbl.gov` source, identifiable review authors, version footer, and exact numbered equations.
- Source status: states the standard two-body decay energy and momentum formulas; the local audit separately derives the formulas from the supplied shell and conservation premises.
- Required hypotheses: parent rest frame, decay into two on-shell particles with real nonnegative masses, physical positive-energy branch, and ordinary Lorentzian energy-momentum relation. Units are `c=1`.
- Notation dictionary: PDG `M,m_1,m_2,E_1,|p_1|` correspond to local `M,m,mu,E_d,p`. PDG Kallen function factors into the four factors shown in `RECOIL_AUDIT.md`.
- Application: exact match under these hypotheses. The PDG formula does not justify a dispersion law in a Lorentz-breaking clock medium, the proposed decay amplitude, repeated transitions, or the halo trigger.
- Overlap classification: known after translation of notation for ordinary two-body kinematics. No novelty claim, broad literature search, or source claim about the C003 theory is made.
- Unresolved source issues: none for this narrow formula match. Existence of a suitable dynamical clock realization remains outside the source's claim.
