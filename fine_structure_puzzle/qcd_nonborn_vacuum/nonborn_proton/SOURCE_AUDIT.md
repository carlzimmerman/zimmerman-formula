# Exact-source and component audit, 2026-10-19

The search covered primary lattice forward-Compton, Cottingham and dynamical
QCD+QED mass sources, including papers indexed through 19 October 2026. This
is a scoped record of what was actually inspected, not a proof that no other
public dataset exists. Source URLs, pinned versions and hashes are in the
receipt JSON files. Cached source archives were inspected without executing
embedded code. Minimal selected equations were extracted; no article text
transcription is used as a new result.

| Source and exact inspected version | Actual content | Why it does not close the full proton non-Born response |
|---|---|---|
| Can et al., [2501.08619v2](https://arxiv.org/abs/2501.08619v2), revised 21 May 2025 | Main source, current-contraction discussion, Appendix A LOPE and Appendix B printed S1 points; source archive has 11 figure PDFs and TeX/Bib files | S1(0,Q²) at unphysical SU(3) pion masses. Only propagator action is differentiated: Type I/II, no determinant two-current same-loop response. It supplies no t2(iQx,Q²), inelastic energy dependence or fixed-MSbar full mass counterterms. Its existing six-point functional was already computed in FSP006 and is not rerun here. |
| Fu et al., [2411.03141v2](https://arxiv.org/abs/2411.03141v2), revised 1 February 2025 | Main text and included supplement, equations 12–20 and Nπ reconstruction section; source archive has ten figure PDFs and TeX/Bib files | Uses a single imaginary-energy line t1(iQ,Q²) and spatial zero-momentum temporal correlator. Includes connected/disconnected diagrams but does not publish the full two-variable tensor. Final optimized proton curve incorporates empirical electric polarizability, radius and anomalous moment through α2, plus variance-minimization weights. Supplement reconstructs Nπ states using a low-momentum extraction extended to a higher momentum band. This is disclosed source modeling/calibration, not a new no-fit QCD tensor input. |
| Crawford et al., [2610.10006v1](https://arxiv.org/abs/2610.10006v1), submitted 7 October 2026 | Exact arXiv abstract page; 15 pages/7 figures advertised | Polarized g1/Bjorken moment. It does not provide the unpolarized t1/t2 tensor needed by the spin-averaged electromagnetic mass. No PDF/data inspection is claimed for this source. |
| Borsanyi et al., [1406.4088v2](https://arxiv.org/abs/1406.4088v2), revised 7 April 2015 | PDF Table 1, dynamical-QED description and supplemental lattice action/parameter discussion | Includes charged sea, four nondegenerate flavors and multiple QED couplings. Published observable is isospin mass splittings, with fitted/interpolated dependence and physical calibration. Splittings leave the common isoscalar proton/neutron response unmeasured; no individual-proton fixed-MSbar response is reconstructed here. A raw individual mass-versus-coupling sequence plus its retuning Jacobian would reopen this route. |
| AHLP, [2005.09518v2](https://arxiv.org/abs/2005.09518v2), revised 9 July 2020 | PDF, TeX source and exact ancillary notebook. Every assignment inventoried in AHLP_ANCILLARY_INVENTORY.json | Ancillary provides static polarizabilities and Q² slopes for πN, πΔ and Δ sectors, including HB expansions. It supplies no full ν,Q² amplitude assignment. Its static πN sector permits the new soft-coefficient computation. Its final proton curve uses a fitted δβ/Baldin anchor, explicitly excluded here. |
| Nevado–Pineda, [0712.1294v2](https://arxiv.org/abs/0712.1294v2), PDF/HTML dated 8 March 2008 | PDF and exact source Pol1loop080308.tex, equations 2.9–2.11,3.16,3.18,3.19,4.26,4.27 | **Does supply complete strict leading HB πN non-Born S1/S2**, including the required seagull. This supports a finite two-dimensional photon-band convolution, beyond a soft Taylor polynomial. It is a specified chiral sector, with higher orders and full mass matching still absent. |

The two lattice source archives contain no raw configuration correlators or
full momentum/energy tensor arrays in their inventories. The active TeX
contains no Zenodo, Figshare, HEPData, GitHub or data-availability link. These
negative observations apply only to the authenticated archives and active
source, not to a claim about unavailable author data. Exact inventories and
hashes are in SOURCE_RECHECK_RECEIPTS.json. No authors were contacted.

Neither an inelastic cross-section fit nor an empirical polarizability was
used as a new numerical input. The exact low-energy source formulas in the
new runs use physically calibrated strong couplings/masses; those imported
inputs are listed as printed decimals. No measured electromagnetic coupling
is used, even though the cached AHLP notebook contains such a constants cell.
