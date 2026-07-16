#!/usr/bin/env python3
"""
gext_estimator.py -- environmental Newtonian field vector estimator, re-implementing
Chae 2021 (ApJ 921, 104; arXiv:2109.04745) Sec. 3.1 (2M++ + MCXC all-sky sum).

Every load-bearing constant is cited in src/METHOD_NOTES.md (quotes from Chae Sec. 2-3)
or flagged [OURS] there.

Returns, for an arbitrary (RA, Dec, D/Mpc) test point:
    |e_N| = |g_Ne,env| / a0   with a0 = 1.2e-10 m/s^2  (Chae Sec. 2)
    unit vector (ICRS Cartesian + supergalactic Cartesian)
    per-contributor breakdown (top contributors by |g| share)

Modes:
    completeness=False  -> "noclu" analog: raw visible-catalogue sum
    completeness=True   -> "maxclu" analog: 1/f(D) LF up-weighting; multiply the FIELD by 8
                           (cosmological missing baryons, Chae Sec. 3.2.4) OUTSIDE this module.

No hard-coded validation results anywhere.
"""
import numpy as np
from scipy.special import gammainc, gamma as gammafn  # lower regularized

# ---------- constants ----------
G_SI    = 6.674e-11          # m^3 kg^-1 s^-2
MSUN_KG = 1.989e30
MPC_M   = 3.0857e22
A0      = 1.2e-10            # m/s^2 (Chae Sec. 2)
H0      = 73.0               # km/s/Mpc (Chae Sec. 3.1, "as assumed in SPARC")
C_KMS   = 299792.458
MSUN_KS = 3.28               # Vega Ks solar absolute magnitude [OURS - global constant]
ML_KS   = 0.64               # Chae Sec. 3.1
KS_LIM  = 11.5               # Chae Sec. 3.1
D_MAX   = 200.0              # Mpc, Chae Sec. 3.1
EXCL_KPC = 0.010             # 10 kpc exclusion, Chae Sec. 3.1.2 (in Mpc)
# Kochanek et al. 2001 2MASS Ks Schechter LF [OURS, for the completeness weight only]
LF_MSTAR = -23.39 + 5*np.log10(0.73)   # = -24.072 for h=0.73
LF_ALPHA = -1.09

def radec_to_cart(ra_deg, dec_deg):
    ra = np.radians(np.asarray(ra_deg, float)); dec = np.radians(np.asarray(dec_deg, float))
    return np.stack([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)], axis=-1)

# ICRS -> supergalactic (SGX,SGY,SGZ) rotation. Built from the standard definition:
# supergalactic north pole at (l,b)=(47.37, +6.32) galactic; SG longitude zero at l=137.37.
# We construct it via the galactic rotation (IAU 1958 / J2000 values).
def _icrs_to_gal_matrix():
    # J2000: alpha_NGP=192.85948, delta_NGP=27.12825, l_NCP=122.93192
    aN = np.radians(192.85948); dN = np.radians(27.12825); lN = np.radians(122.93192)
    # rotation matrix (standard, e.g. Murray 1989)
    R = np.array([
        [-np.sin(aN)*np.sin(lN) - np.cos(aN)*np.sin(dN)*np.cos(lN),
          np.cos(aN)*np.sin(lN) - np.sin(aN)*np.sin(dN)*np.cos(lN),
          np.cos(dN)*np.cos(lN)],
        [ np.sin(aN)*np.cos(lN) - np.cos(aN)*np.sin(dN)*np.sin(lN),
         -np.cos(aN)*np.cos(lN) - np.sin(aN)*np.sin(dN)*np.sin(lN),
          np.cos(dN)*np.sin(lN)],
        [ np.cos(aN)*np.cos(dN), np.sin(aN)*np.cos(dN), np.sin(dN)]])
    return R

def _gal_to_sgal_matrix():
    # supergalactic pole (l,b) = (47.37, +6.32); zero longitude at l=137.37 (de Vaucouleurs)
    lp = np.radians(47.37); bp = np.radians(6.32)
    zsg = np.array([np.cos(bp)*np.cos(lp), np.cos(bp)*np.sin(lp), np.sin(bp)])
    l0 = np.radians(137.37)
    x0 = np.array([np.cos(l0), np.sin(l0), 0.0])
    x0 = x0 - zsg*np.dot(zsg, x0); x0 /= np.linalg.norm(x0)
    ysg = np.cross(zsg, x0)
    return np.stack([x0, ysg, zsg])

_R_ICRS2GAL = _icrs_to_gal_matrix()
_R_GAL2SG   = _gal_to_sgal_matrix()
R_ICRS2SG   = _R_GAL2SG @ _R_ICRS2GAL

def lf_visible_fraction(D_mpc, z=None, ks_lim=KS_LIM):
    """Fraction of the K-band LUMINOSITY density visible above ks_lim at distance D.
    f = Gamma(alpha+2, x)/Gamma(alpha+2), x = L_lim/L*  [OURS -- see METHOD_NOTES 6].
    ks_lim may be an array (region-dependent 2M++ depth: 11.5 all-sky, 12.5 in 6dF/SDSS)."""
    D = np.maximum(np.asarray(D_mpc, float), 0.1)
    if z is None:
        z = D*H0/C_KMS
    dm = 5*np.log10(D*(1.0+z)) + 25.0
    Mlim = np.asarray(ks_lim, float) - dm + 2.1*z - 0.8*z  # LH11 k,e corrections on the limit too
    x = 10.0**(-0.4*(Mlim - LF_MSTAR))
    a = LF_ALPHA + 2.0
    f = 1.0 - gammainc(a, x)             # upper incomplete / complete (regularized)
    return np.clip(f, 1e-3, 1.0)

# ---------- catalogue loaders ----------
def load_2mpp(path, apply_c115_weight=False, catalog_mode='full'):
    """Returns dict of arrays: ra, dec, D (Mpc), Mstar, Mgas (Msun), name, kslim.

    catalog_mode:
      'ks115' -- Ks<=11.5 & D<=200 (Chae Sec 3.1 as WRITTEN; ~27.6k sources)
      'full'  -- D<=200 only (reproduces Chae's own quoted count of 54,483; the
                 Ks<=12.5 deep 6dF/SDSS sources are kept, with region-dependent
                 completeness limits from the M1/M2 flags). See METHOD_NOTES 2b.
    Columns expected: Name Ksmag Vcmb c11.5 c12.5 M1 M2 Ref _RA _DE
    """
    names=[]; ks=[]; vcmb=[]; ra=[]; dec=[]; c115=[]; deep=[]
    with open(path) as fh:
        for ln in fh:
            if ln.startswith('#') or not ln.strip(): continue
            p = ln.rstrip('\n').split('\t')
            if len(p) < 10: continue
            try:
                k = float(p[1]); v = float(p[2]); r = float(p[8]); d = float(p[9])
            except ValueError:
                continue
            try: c = float(p[3])
            except ValueError: c = 1.0
            m1 = p[5].strip(); m2 = p[6].strip()
            deep.append(1 if (m1 == '1' or m2 == '1') else 0)
            names.append(p[0].strip()); ks.append(k); vcmb.append(v)
            ra.append(r); dec.append(d); c115.append(c)
    ks = np.array(ks); vcmb = np.array(vcmb); ra = np.array(ra); dec = np.array(dec)
    c115 = np.array(c115); names = np.array(names); deep = np.array(deep)
    D = vcmb / H0
    if catalog_mode == 'ks115':
        sel = (ks <= KS_LIM) & (D > 0) & (D <= D_MAX)      # Chae Sec 3.1 as written
    elif catalog_mode == 'full':
        sel = (D > 0) & (D <= D_MAX)                       # reproduces his N=54,483
    else:
        raise ValueError(catalog_mode)
    ks, D, ra, dec, c115, names, deep = (ks[sel], D[sel], ra[sel], dec[sel], c115[sel],
                                         names[sel], deep[sel])
    z = vcmb[sel]/C_KMS
    kslim = np.where((deep == 1) & (catalog_mode == 'full'), 12.5, 11.5)
    # LH11 Eq 1: M = m - k(z) + e(z) - DM ; k=-2.1z, e=0.8z ; DM with D_L = D(1+z)
    dm = 5*np.log10(D*(1+z)) + 25.0
    Mabs = ks + 2.1*z - 0.8*z - dm       # NOTE: -k(z) = +2.1z ; +e(z) = +0.8z... see METHOD_NOTES 2
    LK = 10.0**(-0.4*(Mabs - MSUN_KS))
    Mstar = ML_KS * LK
    if apply_c115_weight:
        Mstar = Mstar / np.clip(c115, 0.2, 1.0)
    # gas (METHOD_NOTES 3): deterministic expectation of Chae Eqs 7/8
    lgM = np.log10(np.maximum(Mstar, 1.0))
    f_early = np.clip(0.28*lgM - 2.12, 0.0, 1.0)
    Mg_cold = 11500.0*np.maximum(Mstar,1.0)**0.54 + 0.07*Mstar
    Mg_hot  = 10.0**(1.47*lgM - 5.414)
    Mgas = (1-f_early)*Mg_cold + f_early*Mg_hot
    return dict(name=names, ra=ra, dec=dec, D=D, z=z, Mstar=Mstar, Mgas=Mgas,
                kslim=kslim, kind=np.full(len(D),'gal2mpp'))

def load_mcxc(path, ez_sqrt=False):
    """Returns dict: name, ra, dec, D, M_MOND (Msun), R500 (Mpc)."""
    names=[]; ra=[]; dec=[]; zz=[]; L=[]; R5=[]
    with open(path) as fh:
        for ln in fh:
            if ln.startswith('#') or not ln.strip(): continue
            p = ln.rstrip('\n').split('\t')
            if len(p) < 8: continue
            try:
                z = float(p[4]); L500 = float(p[5]); r500 = float(p[7])
            except ValueError:
                continue
            # sexagesimal coords
            try:
                h,m,s = p[2].split(); rd = (float(h)+float(m)/60+float(s)/3600)*15.0
                dgs = p[3].split(); sgn = -1.0 if dgs[0].strip().startswith('-') else 1.0
                dd = sgn*(abs(float(dgs[0]))+float(dgs[1])/60+float(dgs[2])/3600)
            except Exception:
                continue
            nm = (p[1].strip() or p[0].strip())
            names.append(nm); ra.append(rd); dec.append(dd); zz.append(z); L.append(L500); R5.append(r500)
    ra=np.array(ra); dec=np.array(dec); z=np.array(zz); L500=np.array(L); R500=np.array(R5)
    names=np.array(names)
    Ez = 0.3*(1+z)**3 + 0.7
    if ez_sqrt: Ez = np.sqrt(Ez)
    logL = np.log10(L500*1e44)           # erg/s
    MX = (1e14/Ez) * 10.0**((np.log10(10**logL/Ez) - 44.44)/1.11)   # Chae Eq 3
    # equivalently ((logL - log Ez) - 44.44)/1.11
    Mmond = 10.0**(3.814 + 0.728*np.log10(MX))                       # Chae Eq 4
    D = C_KMS*z/H0
    sel = (D > 0) & (D <= D_MAX)
    return dict(name=names[sel], ra=ra[sel], dec=dec[sel], D=D[sel], z=z[sel],
                Mmond=Mmond[sel], R500=R500[sel], kind=np.full(sel.sum(),'cluster'))

# ---------- the estimator ----------
class GextEstimator:
    def __init__(self, twompp_path, mcxc_path, gas=True, ez_sqrt=False, c115_weight=False,
                 catalog_mode='full'):
        g = load_2mpp(twompp_path, apply_c115_weight=c115_weight, catalog_mode=catalog_mode)
        c = load_mcxc(mcxc_path, ez_sqrt=ez_sqrt)
        self.gal = g; self.clu = c
        self.gal_mass = g['Mstar'] + (g['Mgas'] if gas else 0.0)
        self.gal_pos = radec_to_cart(g['ra'], g['dec']) * g['D'][:,None]     # Mpc, ICRS cart
        self.clu_pos = radec_to_cart(c['ra'], c['dec']) * c['D'][:,None]
        self.n_gal = len(g['D']); self.n_clu = len(c['D'])

    def field_at(self, ra, dec, D, completeness=False, exclude_self=True, n_top=3):
        """Newtonian field vector (m/s^2, ICRS cartesian) at test point.
        completeness=True applies the 1/f(D) LF up-weight to 2M++ galaxy masses
        (the x8 cosmological-baryon factor is NOT applied here)."""
        tp = radec_to_cart(ra, dec) * D
        # galaxies
        dvec = self.gal_pos - tp                     # Mpc
        r = np.linalg.norm(dvec, axis=1)
        m = self.gal_mass.copy()
        if completeness:
            m = m / lf_visible_fraction(self.gal['D'], self.gal['z'], self.gal['kslim'])
        keep = r > EXCL_KPC                          # 10 kpc exclusion (Chae 3.1.2)
        if exclude_self:
            # 0.1 deg + distance match (METHOD_NOTES 5)
            dots = (self.gal_pos * tp[None, :]).sum(axis=1)
            cosang = dots / (np.linalg.norm(self.gal_pos, axis=1)*D + 1e-30)
            ang = np.degrees(np.arccos(np.clip(cosang,-1,1)))
            selfmask = (ang < 0.1) & (np.abs(self.gal['D']-D) < np.maximum(3.0, 0.2*D))
            keep &= ~selfmask
        gmag = G_SI * m[keep]*MSUN_KG / (r[keep]*MPC_M)**2     # m/s^2
        gvec = (dvec[keep]/r[keep,None]) * gmag[:,None]
        # clusters: point mass outside R500, (d/R500)^3 interior scaling (METHOD_NOTES 4)
        dvc = self.clu_pos - tp
        rc = np.linalg.norm(dvc, axis=1)
        mc = self.clu['Mmond'].copy()
        inner = rc < self.clu['R500']
        mc_eff = np.where(inner, mc*(rc/np.maximum(self.clu['R500'],1e-6))**3, mc)
        keepc = rc > EXCL_KPC
        gmagc = G_SI * mc_eff[keepc]*MSUN_KG / (rc[keepc]*MPC_M)**2
        gvecc = (dvc[keepc]/rc[keepc,None]) * gmagc[:,None]
        total = gvec.sum(axis=0) + gvecc.sum(axis=0)
        # contributor breakdown: share of each source's |g| in the sum of |g| is not
        # direction-meaningful; instead rank by |g_i| and report share of |total|
        mags = np.concatenate([gmag, gmagc])
        names = np.concatenate([self.gal['name'][keep], self.clu['name'][keepc]])
        kinds = np.concatenate([self.gal['kind'][keep], self.clu['kind'][keepc]])
        order = np.argsort(mags)[::-1][:n_top]
        tot_mag = np.linalg.norm(total)
        top = [(str(names[i]), str(kinds[i]), float(mags[i]), float(mags[i]/max(tot_mag,1e-30)))
               for i in order]
        return total, top

    def eN_at(self, ra, dec, D, completeness=False, missing_baryons_x8=False, **kw):
        gvec, top = self.field_at(ra, dec, D, completeness=completeness, **kw)
        if missing_baryons_x8:
            gvec = gvec * 8.0                        # Chae Sec 3.2.4 max-clustering
        mag = np.linalg.norm(gvec)
        unit = gvec/max(mag, 1e-30)
        return dict(eN=mag/A0, unit_icrs=unit, unit_sg=R_ICRS2SG @ unit, top=top, gvec=gvec)

# ---------- unit test: synthetic point mass ----------
def _unit_test():
    """One point mass at a known position -> known |g| and direction, machine precision."""
    est = object.__new__(GextEstimator)
    M = 1e12  # Msun
    est.gal = dict(name=np.array(['PT']), ra=np.array([90.0]), dec=np.array([0.0]),
                   D=np.array([10.0]), z=np.array([10.0*H0/C_KMS]),
                   kslim=np.array([11.5]), kind=np.array(['gal2mpp']))
    est.gal_mass = np.array([M])
    est.gal_pos = radec_to_cart([90.0],[0.0]) * 10.0
    est.clu = dict(name=np.array([]), ra=np.array([]), dec=np.array([]), D=np.array([]),
                   z=np.array([]), Mmond=np.array([]), R500=np.array([]), kind=np.array([]))
    est.clu_pos = np.zeros((0,3))
    # test point at origin-direction RA=90,Dec=0, distance 5 Mpc -> source is 5 Mpc further out, same LOS
    res = est.eN_at(90.0, 0.0, 5.0, exclude_self=False)
    g_expect = G_SI * M * MSUN_KG / (5.0*MPC_M)**2
    dir_expect = np.array([0.0, 1.0, 0.0])   # RA=90 -> +y
    assert abs(res['eN']*A0/g_expect - 1) < 1e-12, res['eN']*A0/g_expect
    assert np.allclose(res['unit_icrs'], dir_expect, atol=1e-12), res['unit_icrs']
    # off-axis: test point at RA=0,Dec=0,D=5 ; source at RA=90 D=10 -> direction (0,10,0)-(5,0,0)
    res2 = est.eN_at(0.0, 0.0, 5.0, exclude_self=False)
    dv = np.array([0.0,10.0,0.0]) - np.array([5.0,0.0,0.0])
    g2 = G_SI*M*MSUN_KG/(np.linalg.norm(dv)*MPC_M)**2
    assert abs(res2['eN']*A0/g2 - 1) < 1e-12
    assert np.allclose(res2['unit_icrs'], dv/np.linalg.norm(dv), atol=1e-12)
    # supergalactic rotation is orthonormal
    assert np.allclose(R_ICRS2SG @ R_ICRS2SG.T, np.eye(3), atol=1e-12)
    print("unit test PASSED: point-mass magnitude+direction at machine precision; SG rotation orthonormal")

if __name__ == '__main__':
    _unit_test()
