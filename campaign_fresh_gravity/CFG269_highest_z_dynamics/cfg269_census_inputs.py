# -*- coding: utf-8 -*-
"""
CFG269 census inputs: published numbers only, each with its source (page reads of arXiv abstract / HTML / PDF pages cached by the fetch tool
outside the repository; nothing downloaded into the repository).  Read by cfg269_discriminate.py.  See SCOPING.md for the census table,
the exclusions and how each number was read.

Fields per row
  id, obj, z, cls ('COMPLETE' = stars + gas, 'LOWER-LIMIT' = stars only), role ('headline' / 'sensitivity'), pool_key (None = not pooled),
  branch, flags (AGN / merger / outflow statements in the literature), notes, src
  mstar = (log10 Msun, +err, -err) as published (IMF / code in notes)
  gas   = None or (log10 Msun, +err, -err[, enclosed fraction within r])
  fenc_star = enclosed fraction of M* within r (default 0.5 = half-light = half-mass at r = r_e; other values from the stated profile)
  r     = (kpc, +err, -err): the radius the paper's dynamical estimator uses
  kin   = ("sigma", km/s, +e, -e, K)   M_dyn,tot = K sigma^2 r / G   (enclosed within r = half)
          ("mdyn", log10, +e, -e, kind) the paper's own M_dyn; kind 'total' (enclosed = half) or 'enclosed'
  c8    = optional (K, velocity km/s, r_kpc, log10 M_dyn paper, kind) for the C8 recomputation flag (K applied as printed: M = K v^2 r / G)
"""
import math, os, sys, io, contextlib

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "HZQ_common"))
with contextlib.redirect_stdout(io.StringIO()):
    import hzq_core as _H                                        # kpc per arcsec (H0 67.4, Om 0.315), read-only


def _l(x):
    return math.log10(x)


def _fexp(R, Re):
    """enclosed fraction of a thin exponential (projected) profile with half-light radius Re inside R."""
    x = R / (Re / 1.678)
    return 1.0 - (1.0 + x) * math.exp(-x)


def _arc(z, a, ep, em):
    k = _H.kpc_per_arcsec(z)
    return (a * k, ep * k, em * k)


# ---------------------------------------------------------------- B3: z >= 8
# JADES-GS-z14-0 (Carniani+24 Nature 633, 318, arXiv:2405.18485; Carniani+25 A&A 696, A87, arXiv:2409.20533; Schouws+25 ApJ 988, 19,
# arXiv:2409.20549; Helton+25 Nat Astron 9, 729, arXiv:2405.18462; Heintz+25 arXiv:2502.06016; Scholtz+25 arXiv:2503.10751)
_GAS_H25 = (9.8, 0.3, 0.3, _fexp(0.260, 3 * 0.260))             # Heintz+25 DLA total gas; half-mass radius ~3 x r_UV -> fraction inside 260 pc
_z14 = 14.1796
CENSUS = [
    dict(id="GS-z14-0 [C25 dyn; C25 M*; +H25 gas]", flagged=False, obj="JADES-GS-z14-0 [C25 dyn; C25 M*; +H25 gas]", z=_z14, cls="COMPLETE", role="headline",
         pool_key="JADES-GS-z14-0", branch="C25", mstar=(8.29, math.hypot(0.14, 0.4), math.hypot(0.09, 0.1)), gas=_GAS_H25, r=(0.260, 0.020, 0.020),
         kin=("mdyn", 9.0, math.hypot(0.2, 0.2), math.hypot(0.2, 0.2), "total"), c8=(6.83, 102 / 2.355, 0.260, 9.0, "total"),
         flags="none on the line width (no AGN; Scholtz+25 exclude an outflow for the gradient); gas inside r_e is a geometric assumption (Heintz+25: gas r ~ 3 r_UV)",
         notes="[OIII]88 FWHM 102 +29/-22 (C25 Sect. 3); M_dyn = K(n)K(q) sigma^2 R_e/G, log 9.0 +-0.2 +-0.2 (C25 Sect. 5.2, Eq. 1; n 0.8-2, q 0.3-1); "
               "M* 8.29 +0.14/-0.09 (sys -0.1/+0.4) Prospector, Chabrier 0.1-300 (C25 Table 2), errors combined in quadrature; R_e 260 +- 20 pc UV (C24); "
               "gas 10^9.8 +- 0.3 from the DLA N_HI (H25), enclosed fraction %.3f inside 260 pc for an exponential with R_e,gas = 780 pc" % _GAS_H25[3],
         source="C25 arXiv:2409.20533 (HTML, verified); C24 arXiv:2405.18485; H25 arXiv:2502.06016 (abstract + HTML via helper)"),
    dict(id="GS-z14-0 [S25 sigma; Helton M*; +H25 gas]", flagged=False, obj="JADES-GS-z14-0 [S25 sigma; Helton M*; +H25 gas]", z=_z14, cls="COMPLETE", role="headline",
         pool_key="JADES-GS-z14-0", branch="S25", mstar=(8.7, 0.5, 0.4), gas=_GAS_H25, r=(0.260, 0.020, 0.020),
         kin=("sigma", 136 / 2.355, 31 / 2.355, 31 / 2.355, 5.0), c8=(5.0, 136 / 2.355, 0.260, 9.0, "total"),
         flags="none on the line width; gas inside r_e is a geometric assumption",
         notes="[OIII]88 FWHM 136 +- 31 (S25 Sect. III.1, verified); S25 M_dyn (1.0 +- 0.5)e9 dispersion-dominated at r = 260 pc, coefficient not printed (K = 5 reproduces it); "
               "M* 8.7 +0.5/-0.4 (Helton+25 BAGPIPES, Kroupa, adopted by S25)",
         source="S25 arXiv:2409.20549 (HTML, verified); Helton+25 arXiv:2405.18462 (helper)"),
    dict(id="GS-z14-0 [C25 dyn; C25 M*; stars only]", flagged=False, obj="JADES-GS-z14-0 [C25 dyn; C25 M*; stars only]", z=_z14, cls="LOWER-LIMIT", role="sensitivity",
         pool_key=None, branch="C25", mstar=(8.29, math.hypot(0.14, 0.4), math.hypot(0.09, 0.1)), gas=None, r=(0.260, 0.020, 0.020),
         kin=("mdyn", 9.0, math.hypot(0.2, 0.2), math.hypot(0.2, 0.2), "total"), flags="as above", notes="stars only (dust < 10^6, Schouws+25)", source="as above"),
    dict(id="GS-z14-0 [S25 sigma; Helton M*; stars only]", flagged=False, obj="JADES-GS-z14-0 [S25 sigma; Helton M*; stars only]", z=_z14, cls="LOWER-LIMIT", role="sensitivity",
         pool_key=None, branch="S25", mstar=(8.7, 0.5, 0.4), gas=None, r=(0.260, 0.020, 0.020), kin=("sigma", 136 / 2.355, 31 / 2.355, 31 / 2.355, 5.0),
         flags="as above", notes="stars only", source="as above"),
    dict(id="GS-z14-0 [Scholtz25 KinMS; Helton M*; stars only]", flagged=False, obj="JADES-GS-z14-0 [Scholtz25 KinMS; Helton M*; stars only]", z=_z14, cls="LOWER-LIMIT",
         role="sensitivity", pool_key=None, branch="Sch25", mstar=(8.7, 0.5, 0.4), gas=None, r=(0.260, 0.020, 0.020), kin=("mdyn", 9.4, 0.8, 0.4, "total"),
         flags="3.0-sigma gradient; radius of the KinMS mass not stated (taken as a total mass at R_e = 260 pc)",
         notes="Scholtz+25 log M_dyn 9.4 +0.8/-0.4 (thin exponential disc, R_e fixed 260 pc, inclination-dominated errors)", source="arXiv:2503.10751 (helper, HTML)"),

    # GHZ2 / GLASS-z12 (Zavala+24 ApJL 977, L9, arXiv:2411.03593; Castellano+24 ApJ 972, 143, arXiv:2403.10238; Mitsuhashi+25 arXiv:2501.19384)
    dict(id="GHZ2 [R105; M* C24]", flagged=True, obj="GHZ2 [R 105 pc; M* Castellano+24]", z=12.3327, cls="LOWER-LIMIT", role="headline", pool_key="GHZ2", branch="M*C24",
         mstar=(9.05, 0.10, 0.25), gas=None, r=(0.105, 0.009, 0.009), kin=("sigma", 79.0, 25.0, 25.0, 5.0), c8=(5.0, 79.0, 0.105, _l(8e8), "total"),
         flags="possible AGN (Castellano+26 O III 3133 variability); Zavala+24: line most likely star-formation dominated",
         notes="[OIII]88 FWHM 186 +- 58, sigma 79 +- 25 (Z24 Table 1, verified); M_dyn = 5 sigma^2 R/G (Z24 Eq. 1), 3-8e8; R = 105 +- 9 pc (Yang, delensed, as quoted by C24); "
               "M* 9.05 +0.10/-0.25 BAGPIPES/BPASS, Chabrier, mu = 1.3 corrected (C24 Table 2); dust < 10^5",
         source="Z24 arXiv:2411.03593 (HTML, verified); C24 arXiv:2403.10238 (helper)"),
    dict(id="GHZ2 [R105; M* M25]", flagged=True, obj="GHZ2 [R 105 pc; M* Mitsuhashi+25]", z=12.3327, cls="LOWER-LIMIT", role="headline", pool_key="GHZ2", branch="M*M25",
         mstar=(8.27, 0.23, 0.18), gas=None, r=(0.105, 0.009, 0.009), kin=("sigma", 79.0, 25.0, 25.0, 5.0),
         flags="possible AGN (Castellano+26)", notes="M* 8.27 +0.23/-0.18 Bagpipes non-parametric, mu-corrected (Mitsuhashi+25 Table 1)", source="M25 arXiv:2501.19384 (helper)"),
    dict(id="GHZ2 [R39; M* C24]", flagged=True, obj="GHZ2 [R 39 pc; M* Castellano+24]", z=12.3327, cls="LOWER-LIMIT", role="sensitivity", pool_key=None, branch="M*C24",
         mstar=(9.05, 0.10, 0.25), gas=None, r=(0.039, 0.011, 0.011), kin=("sigma", 79.0, 25.0, 25.0, 5.0), c8=(5.0, 79.0, 0.039, _l(3e8), "total"),
         flags="possible AGN", notes="R = 39 +- 11 pc (Ono, as quoted by Z24; C24 quotes 34 +- 9)", source="Z24"),
    dict(id="GHZ2 [R39; M* M25]", flagged=True, obj="GHZ2 [R 39 pc; M* Mitsuhashi+25]", z=12.3327, cls="LOWER-LIMIT", role="sensitivity", pool_key=None, branch="M*M25",
         mstar=(8.27, 0.23, 0.18), gas=None, r=(0.039, 0.011, 0.011), kin=("sigma", 79.0, 25.0, 25.0, 5.0), flags="possible AGN", notes="", source="Z24; M25"),

    # GN-z11 (Xu+24 ApJ, arXiv:2404.16963; Tacchella+23 ApJ 952, 74, arXiv:2302.07234; Maiolino+24 Nature, arXiv:2305.12492;
    # Alvarez-Marquez+25 A&A 695, A250, arXiv:2412.12826)
    dict(id="GN-z11 [Xu24 <2Re; M* T23]", flagged=True, obj="GN-z11 [Xu+24 M_dyn(<2R_e); M* Tacchella+23]", z=10.60, cls="LOWER-LIMIT", role="headline", pool_key="GN-z11", branch="Xu24",
         mstar=(9.1, 0.3, 0.4), fenc_star=(_fexp(0.418, 0.200) * 10 ** 8.9 + 10 ** 8.4) / 10 ** 9.1, gas=None, r=(0.418, 0.04, 0.04),
         kin=("mdyn", _l(4.6e9), _l(7.3 / 4.6), -_l(1.9 / 4.6), "enclosed"), c8=(1.0, 217.0, 0.418, _l(4.6e9), "enclosed"),
         flags="AGN host (Maiolino+24 assign part of CIII] to the BLR); Xu+24: outflows can also explain the gradient",
         notes="CIII] GalPak3D v_rot 257 +138/-117, sigma 91 +18/-32, i 54 +18/-7, R_e 209 pc; v_c(2R_e) 217 +- 63; M_dyn(<2R_e) 4.6 +- 2.7e9 (Xu+24, verified); "
               "M* 9.1 +0.3/-0.4 (T23 Prospector, Chabrier); stars inside 418 pc = extended component (10^8.9, r_e 200 pc) + point source (10^8.4)",
         source="Xu+24 arXiv:2404.16963 (HTML, verified); T23 arXiv:2302.07234 (helper)"),
    dict(id="GN-z11 [AM25 <64pc; M* T23]", flagged=True, obj="GN-z11 [Alvarez-Marquez+25 M_dyn(<64 pc); M* Tacchella+23]", z=10.60, cls="LOWER-LIMIT", role="headline", pool_key="GN-z11",
         branch="AM25", mstar=(9.1, 0.3, 0.4), fenc_star=(_fexp(0.064, 0.200) * 10 ** 8.9 + 10 ** 8.4) / 10 ** 9.1, gas=None, r=(0.064, 0.020, 0.020),
         kin=("mdyn", _l(1.1e9), _l(1.5 / 1.1), -_l(0.7 / 1.1), "enclosed"), c8=(6.0, 189 / 2.355, 0.064, _l(1.1e9), "enclosed"),
         flags="AGN host; the 64 pc size is the combined point + extended size",
         notes="MIRI/MRS narrow [OIII]5008 FWHM 189 +- 25, Halpha 231 +- 52 (no broad component); M_dyn 1.1 +- 0.4e9 enclosed in 64 +- 20 pc (coefficient not printed; K = 6 gives about half)",
         source="AM25 arXiv:2412.12826 (helper, HTML)"),

    # MACS1149-JD1 (Alvarez-Marquez+24 arXiv:2309.06319; Stiavelli+23 arXiv:2308.14696; Marconcini+24 arXiv:2407.08616; Tokuoka+22 ApJL 933 L19)
    dict(id="MACS1149-JD1 [AM24; M* S23]", flagged=True, obj="MACS1149-JD1 [AM24 K=6; M* Stiavelli+23]", z=9.1096, cls="LOWER-LIMIT", role="headline", pool_key="MACS1149-JD1", branch="M*S23",
         mstar=(_l(1.6e8 * 10 / 11.5), 0.08, 0.08), gas=None, r=(0.332, 0.054, 0.054), kin=("sigma", 69.2, 5.5, 5.5, 6.0), c8=(6.0, 69.2, 0.332, _l(2.4e9), "total"),
         flags="merger favoured by Marconcini+24; clump N outflow or turbulence (AM24)",
         notes="MIRI/MRS Halpha sigma 69.2 +- 5.5 (instrument-corrected); M_dyn = K R_hm sigma^2/G, K = 6, R_hm 332 +- 54 pc at mu = 11.5 -> 2.4 +- 0.5e9 (AM24 Eq. 4); "
               "M* 1.6 +- 0.3e8 (10/mu) gsf (Stiavelli+23) rescaled to mu = 11.5",
         source="AM24 arXiv:2309.06319, S23 arXiv:2308.14696 (helper, HTML)"),
    dict(id="MACS1149-JD1 [AM24; M* M24]", flagged=True, obj="MACS1149-JD1 [AM24 K=6; M* Marconcini+24]", z=9.1096, cls="LOWER-LIMIT", role="headline", pool_key="MACS1149-JD1", branch="M*M24",
         mstar=(7.47 + _l(10 / 11.5), 0.05, 0.05), gas=None, r=(0.332, 0.054, 0.054), kin=("sigma", 69.2, 5.5, 5.5, 6.0),
         flags="merger favoured by Marconcini+24", notes="M* 10^7.47 (10/mu) Prospector integrated (Marconcini+24), rescaled to mu = 11.5", source="M24 arXiv:2407.08616 (helper)"),

    # S04590 (Heintz+23 ApJL 944, L30, arXiv:2212.06877; Fujimoto+22 arXiv:2212.06863)
    dict(id="S04590 [H23]", flagged=True, obj="S04590 [Heintz+23 M_dyn(<r_e,[CII])]", z=8.496, cls="LOWER-LIMIT", role="headline", pool_key="S04590", branch="H23",
         mstar=(7.15, 0.15, 0.15), fenc_star=1.0, gas=None, r=(1.1, 0.7, 0.7), kin=("mdyn", _l(9.0e8), _l(13.5 / 9.0), -_l(4.5 / 9.0), "enclosed"),
         c8=((0.52 * 2.355) ** 2, 114 / 2.355, 1.1, _l(9.0e8), "enclosed"),
         flags="[CII] interpreted as an outflow by Fujimoto+22 (blue-shifted 90 km/s, offset 0.5 arcsec); r_e,[CII] +- 0.7 kpc",
         notes="[CII] FWHM 114 +- 35 intrinsic; M_dyn = 2.33e5 v_circ^2 r_e, v_circ = 0.52 FWHM, r_e,[CII] = 1.1 +- 0.7 kpc -> 9.0 +- 4.5e8 (enclosed); "
               "M* 10^7.15 +- 0.15 Bagpipes, Chabrier, mu = 8.69; stars (r_e,UV 0.11 kpc) all inside 1.1 kpc",
         source="H23 arXiv:2212.06877 (helper, journal HTML)"),

    # MACS0416_Y1 (Bakx+20 MNRAS 493, 4294, arXiv:2001.02812; Harshan+24 ApJL 977, L36, arXiv:2408.12310; Takechi+26 arXiv:2605.14922)
    dict(id="MACS0416_Y1 [B20; M* H24; +T26 gas]", flagged=True, obj="MACS0416_Y1 [Bakx+20 M_dyn; M* Harshan+24; + [CII] gas Takechi+26]", z=8.3113, cls="COMPLETE", role="headline",
         pool_key="MACS0416_Y1", branch="B20", mstar=(9.0, 0.07, 0.07), gas=(_l(5.56e9), _l(6.17 / 5.56), -_l(4.95 / 5.56)), r=(1.15, 0.35, 0.35),
         kin=("mdyn", _l(1.2e10), _l(1.6 / 1.2), -_l(0.8 / 1.2), "total"), c8=(3.4, 191 / 2.355, 1.15, _l(1.2e10), "total"),
         flags="broad-line AGN (Takechi+26, broad Hbeta 1100 km/s); late-stage merger (Harshan+24); Bakx+20 favour a disc; Tamura+23: turbulent",
         notes="[CII] FWHM 191 +- 29; M_dyn = C r sigma^2/G, C = 3.4, r_1/2 = 1.15 +- 0.35 kpc -> 1.2 +- 0.4e10 as printed (Bakx+20 Eq. 3; the printed inputs give about half); "
               "M* 10^9.0 +- 0.07 Dense Basis, Chabrier, mu = 1.6 (Harshan+24); gas 5.56 +- 0.61e9 from [CII] (Zanella+18 relation; Takechi+26)",
         source="B20 arXiv:2001.02812, H24 arXiv:2408.12310, T26 arXiv:2605.14922 (helper)"),
    dict(id="MACS0416_Y1 [B20; M* H24; stars only]", flagged=True, obj="MACS0416_Y1 [Bakx+20 M_dyn; M* Harshan+24; stars only]", z=8.3113, cls="LOWER-LIMIT", role="sensitivity",
         pool_key=None, branch="B20", mstar=(9.0, 0.07, 0.07), gas=None, r=(1.15, 0.35, 0.35), kin=("mdyn", _l(1.2e10), _l(1.6 / 1.2), -_l(0.8 / 1.2), "total"),
         flags="as above", notes="stars only", source="as above"),
]

# ---------------------------------------------------------------- B2: 6 <= z < 8
# de Graaff+24 A&A 684, A87, arXiv:2308.09742 (Table 2 / B.1 read from the PDF page images by the helper): M_dyn = 1.8 r_e v_circ^2(r_e)/G (total),
# v_circ^2 = v^2 + 3.35 sigma0^2; r_e = emission-line half-light radius; M* BEAGLE, Chabrier (capped 100 Msun)
_DG = [("JADES-NS-00047100", 7.43173, (0.130, 0.011, 0.010), 71, 91, (9.85, 0.07, 0.07), (8.53, 0.12, 0.10), "three morphological components (Baker+23): possible merger"),
       ("JADES-NS-20086025", 7.2627, (0.36, 0.14, 0.10), 25, 155, (10.31, 0.20, 0.19), (8.85, 0.18, 0.18), "morphology fit did not converge (weak priors)"),
       ("JADES-NS-19606", 5.88979, (0.117, 0.013, 0.011), 39.1, 5, (9.17, 0.06, 0.06), (7.54, 0.04, 0.04), "dispersion-dominated (v/sigma 0.13)"),
       ("JADES-NS-22251", 5.79912, (0.122, 0.006, 0.006), 39.0, 23, (9.23, 0.03, 0.03), (8.21, 0.05, 0.05), ""),
       ("JADES-NS-16745", 5.56616, (0.32, 0.03, 0.03), 55, 105, (10.23, 0.08, 0.08), (8.80, 0.04, 0.04), ""),
       ("JADES-NS-10016374", 5.50411, (0.084, 0.013, 0.012), 62, 16, (9.45, 0.07, 0.07), (7.86, 0.07, 0.07), "")]
for nm, z, (ra, rp, rm), s0, v, md, ms, fl in _DG:
    r = _arc(z, ra, rp, rm)
    vc = math.sqrt(v ** 2 + 3.35 * s0 ** 2)
    CENSUS.append(dict(id=nm, flagged=("merger" in fl), obj=f"{nm} [de Graaff+24]", z=z, cls="LOWER-LIMIT", role="headline", pool_key=nm, branch="dG24", mstar=ms, gas=None, r=r,
                       kin=("mdyn", md[0], md[1], md[2], "total"), c8=(1.8, vc, r[0], md[0], "total"),
                       flags=fl or "none stated (broad-line outflow objects were excluded by the authors)",
                       notes=f"sigma0 {s0}, v(r_e) {v} km/s, v_circ {vc:.1f}; r_e {ra}'' = {r[0]:.3f} kpc (emission line); gas not tabulated (inverse KS, <M_gas/M*> ~ 10)",
                       source="de Graaff+24 arXiv:2308.09742 (PDF page images read by the helper)"))

# Saldana-Lopez+25 MNRAS, arXiv:2501.17145 v3, Tables A1-A3 (page images read and checked here): M_dyn = K(n)K(q) sigma_gas^2 r_e/G (total);
# M* Bagpipes, BC03, Kroupa; r_e from NIRCam continuum + line light; sigma_gas = total [OIII] width (rotation not removed); resolved (Sersic) rows only
_SL = [("1871-10", 7.5990, (7.96, 0.39), (0.739, 0.262), 65.2, 5.3, (9.54, 0.16), "outflow (broad component; sigma_narrow 49.1)"),
       ("1871-11", 7.6100, (9.07, 0.31), (0.846, 0.037), 60.9, 12.9, (9.77, 0.15), ""),
       ("1871-12", 7.5020, (8.31, 0.09), (0.381, 0.039), 67.3, 2.8, (9.41, 0.05), "outflow (sigma_narrow 59.8); companion at 0.36 pMpc"),
       ("1871-40", 7.0948, (8.47, 0.53), (0.740, 0.045), 60.6, 5.9, (9.73, 0.07), "outflow (sigma_narrow 60.4)"),
       ("1871-70", 7.0302, (8.85, 0.41), (0.659, 0.052), 41.3, 8.0, (9.42, 0.12), ""),
       ("1871-105", 6.5669, (7.81, 0.79), (0.393, 0.041), 49.9, 1.4, (9.34, 0.05), "outflow (sigma_narrow 57.3); model PSF in Fig. 1 vs Sersic in Table A2"),
       ("1871-912", 6.7161, (9.69, 0.20), (0.970, 0.059), 44.4, 1.9, (9.68, 0.04), ""),
       ("1871-1032", 7.0889, (9.07, 0.24), (0.600, 0.037), 37.3, 12.1, (9.41, 0.16), ""),
       ("1871-29", 5.0191, (9.24, 0.22), (0.839, 0.083), 72.0, 2.8, (9.96, 0.04), ""),
       ("1871-451", 4.4615, (7.99, 0.59), (0.556, 0.066), 40.7, 2.5, (9.37, 0.06), ""),
       ("1871-545", 4.0416, (9.41, 0.41), (0.828, 0.088), 96.4, 1.4, (10.11, 0.05), "z and M* close to Danhaive 1086992 (z 4.04, 9.37) but r_e 0.83 vs 3.42 kpc: not treated as a duplicate")]
for nm, z, ms, r, sg, esg, md, fl in _SL:
    CENSUS.append(dict(id=f"GO{nm}", flagged=("outflow" in fl), obj=f"GO{nm} [Saldana-Lopez+25]", z=z, cls="LOWER-LIMIT", role="headline", pool_key=f"GO{nm}", branch="SL25",
                       mstar=(ms[0], ms[1], ms[1]), gas=None, r=(r[0], r[1], r[1]), kin=("mdyn", md[0], md[1], md[1], "total"),
                       flags=fl or "none stated", notes=f"sigma_gas {sg} +- {esg} km/s; r_e {r[0]*1e3:.0f} pc; K(n) not reproducible (n not tabulated)",
                       source="Saldana-Lopez+25 arXiv:2501.17145 v3 Tables A1-A3 (PDF page images, read here)"))

# REBELS-25 (Rowland+24 MNRAS 535, 2068, arXiv:2405.06025; Cescon+26 arXiv:2606.13393): M_dyn,tot = 1.8 r_e V^2/G at r_e = 2.2 kpc ([CII])
_GAS_R25 = (11.0, _l(1.4), -_l(0.6))                            # CO(3-2): M_mol = (1.0 +- 0.4)e11 (alpha_CO/3)^-1 (Cescon+26)
CENSUS += [
    dict(id="REBELS-25 [R24; M* JWST; +CO]", flagged=False, obj="REBELS-25 [Rowland+24 M_dyn; M* 10^9.30; + CO gas Cescon+26]", z=7.3065, cls="COMPLETE", role="headline", pool_key="REBELS-25",
         branch="M*9.30", mstar=(9.30, 0.12, 0.14), gas=_GAS_R25, r=(2.2, 0.3, 0.3), kin=("mdyn", _l(1.2e11), _l(2.2 / 1.2), -_l(0.6 / 1.2), "total"),
         flags="non-circular motions / possible bar (Rowland+24); Cescon+26: the dynamics imply alpha_CO <~ 3.5",
         notes="[CII] V_rot 359 (outer rings), sigma 33, i 25 +- 6; M_dyn,tot (1.2 +1.0/-0.6)e11 (published version); CO(3-2) ~3.5 sigma: M_mol (1.0 +- 0.4)e11 at alpha_CO = 3; "
               "M* 10^9.30 -0.14/+0.12 (Stefanon in prep., adopted by Cescon+26)", source="Rowland+24, Cescon+26 (helper)"),
    dict(id="REBELS-25 [R24; M* BEAGLE; +CO]", flagged=False, obj="REBELS-25 [Rowland+24 M_dyn; M* 8e9 BEAGLE; + CO gas]", z=7.3065, cls="COMPLETE", role="headline", pool_key="REBELS-25",
         branch="M*8e9", mstar=(_l(8e9), _l(12 / 8), -_l(6 / 8)), gas=_GAS_R25, r=(2.2, 0.3, 0.3), kin=("mdyn", _l(1.2e11), _l(2.2 / 1.2), -_l(0.6 / 1.2), "total"),
         flags="as above", notes="M* 8 +4/-2 e9 (BEAGLE, Chabrier; Rowland+24 Table 1)", source="Rowland+24 (helper)"),
]
