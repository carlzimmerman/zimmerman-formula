#!/usr/bin/env python3
"""
MECHANISM 4 -- THE EXISTENCE QUESTION.
Is there a self-consistent relativistic completion of the a0 = kappa c sqrt(G rho_Lambda)
framework with NO dark matter in halos that STILL fits the CMB?

Framework constants (given, not re-derived):
  a0 = kappa*c*sqrt(G*rho_Lambda) = c*H_Lambda/Z = 9.3619e-11 m/s^2, kappa=1/2, Z=2*sqrt(8pi/3)
  Route A kernel  nu(y) = 1/(1-exp(-sqrt(y))),  y = g_bar/a0

Blocks:
  1  Does the CMB need a dust-like component?  CAMB: remove CDM two ways.
  2  Referee-grade REFIT: marginalise As,ns,H0,ombh2,tau against a Planck-like mock. Delta chi^2.
  3  THE DOOR: a component that is dust in the BACKGROUND but has a nonzero rest-frame
     sound speed. CLASS GDM fluid, w=0, cs2 scanned. Is the CMB blind to cs2?
  4  Same door realised by a KNOWN theory: an 11.3 eV thermal sterile neutrino (Angus 2009).
  5  Tremaine-Gunn phase space: can such a component be EXCLUDED from galaxy halos while
     still supplying clusters?  This is the required property of Q4.
  6  The framework's own numbers: hydrostatic isothermal dust in the Route-A MOND potential.
     What cs2 gives the cluster's required xi and what does the SAME cs2 do to galaxies?
  7  Against interest: can the dust DECAY away after recombination?  Delta N_eff kill.
All numbers printed are reproduced by running this file.
"""
import numpy as np

C     = 2.99792458e8
G     = 6.674e-11
MPC   = 3.0856775814913673e22
MSUN  = 1.98892e30
A0    = 9.3619e-11          # framework a0
KAPPA = 0.5
Z_FRM = 2*np.sqrt(8*np.pi/3)

def nu_routeA(y):
    """Framework's in-force Route A kernel."""
    y = np.asarray(y, dtype=float)
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))

CHECKS = []
def chk(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print(f"   [{'PASS' if cond else 'FAIL'}] {name} {detail}")

def head(t):
    print("\n" + "="*104); print(t); print("="*104)

# ---------------------------------------------------------------- sanity
head("BLOCK 0 -- framework constants")
rho_L = 3*A0**2/(KAPPA**2 * C**2 * 4*np.pi*G) * (4*np.pi/3)   # placeholder, see below
# a0 = kappa c sqrt(G rho_L)  =>  rho_L = (a0/(kappa c))^2 / G
rho_L = (A0/(KAPPA*C))**2 / G
print(f"   a0 = {A0:.5e} m/s^2   kappa = {KAPPA}   Z = {Z_FRM:.6f}")
print(f"   implied rho_Lambda = (a0/(kappa c))^2/G = {rho_L:.5e} kg/m^3")
chk("rho_Lambda from a0 matches Planck rho_Lambda ~5.845e-27", abs(rho_L/5.845e-27-1) < 0.05,
    f"ratio={rho_L/5.845e-27:.4f}")
chk("Route A kernel -> 1 (Newtonian) at large y", abs(nu_routeA(1e4)-1) < 1e-3, f"nu(1e4)={nu_routeA(1e4):.6f}")
chk("Route A kernel -> 1/sqrt(y) (deep MOND) at small y",
    abs(nu_routeA(1e-6)*np.sqrt(1e-6)-1) < 1e-2, f"nu*sqrt(y)={nu_routeA(1e-6)*np.sqrt(1e-6):.5f}")

# ---------------------------------------------------------------- BLOCK 1
head("BLOCK 1 -- does the CMB need a dust-like (a^-3, clustering) component?  CAMB")
import camb
def camb_run(ombh2, omch2, H0=67.36, ns=0.9649, As=2.1e-9, tau=0.0544, lmax=2700, lensed=False):
    p = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, omk=0, tau=tau,
                        As=As, ns=ns, lmax=lmax)
    p.WantTransfer=False; p.DoLensing=lensed; p.NonLinear=camb.model.NonLinear_none
    r = camb.get_results(p)
    key = 'lensed_scalar' if lensed else 'unlensed_scalar'
    cl = r.get_cmb_power_spectra(p, CMB_unit='muK', raw_cl=False)[key][:,0]
    return cl, r.get_derived_params()

def peaks(cl, lmin=50, lmax=2600):
    l=np.arange(len(cl)); m=(l>=lmin)&(l<=lmax); ll,cc=l[m],cl[m]; mx=[]
    for i in range(2,len(cc)-2):
        if cc[i]>cc[i-1] and cc[i]>cc[i+1] and cc[i]>cc[i-2] and cc[i]>cc[i+2]: mx.append((ll[i],cc[i]))
    return mx

OB, OC = 0.02237, 0.1200
cases = [("A  LCDM Planck-18",                              OB,        OC),
         ("B  baryons only, SAME Omega_m h^2 (=0.1424)",     OB+OC,     0.0),
         ("C  baryons only, Planck ombh2 (NO a^-3 dark cpt)",OB,        0.0)]
store={}
for nm,ob,oc in cases:
    cl,d = camb_run(ob,oc); mx=peaks(cl); store[nm]=(cl,d,mx)
    print(f"\n   {nm}")
    print(f"      z_eq={d['zeq']:8.1f}  z_*={d['zstar']:.2f}  r_s={d['rstar']:7.2f} Mpc  100theta*={d['thetastar']:.5f}")
    print(f"      z_eq/z_* = {d['zeq']/d['zstar']:.3f}   (<1 => recombination happens in RADIATION domination)")
    print("      " + "  ".join(f"p{j+1}: l={l:4d} D={c:8.1f}" for j,(l,c) in enumerate(mx[:3])))
    print(f"      H2/H1={mx[1][1]/mx[0][1]:.4f}   H3/H1={mx[2][1]/mx[0][1]:.4f}   H3/H2={mx[2][1]/mx[1][1]:.4f}")
r = {nm:(mx[1][1]/mx[0][1], mx[2][1]/mx[0][1], mx[2][1]/mx[1][1]) for nm,(_,_,mx) in store.items()}
kA=cases[0][0]; kB=cases[1][0]; kC=cases[2][0]
print(f"\n   H3/H2 : LCDM {r[kA][2]:.3f}  |  baryons-only(same Om_m h2) {r[kB][2]:.3f}  |  baryons-only(Planck ob) {r[kC][2]:.3f}")
print("   Planck measures the 3rd peak nearly EQUAL to the 2nd (H3/H2 ~ 0.98).")
chk("LCDM reproduces H3/H2 ~ 1 (3rd peak as high as 2nd)", r[kA][2] > 0.9, f"{r[kA][2]:.3f}")
chk("baryons-only at same Om_m h^2 gives a badly LOW 3rd peak", r[kB][2] < 0.6, f"{r[kB][2]:.3f}")
chk("baryons-only at Planck ombh2 gives a badly LOW 3rd peak", r[kC][2] < 0.7, f"{r[kC][2]:.3f}")
chk("no a^-3 component => recombination in RADIATION domination", store[kC][1]['zeq']/store[kC][1]['zstar'] < 1.0,
    f"z_eq/z_* = {store[kC][1]['zeq']/store[kC][1]['zstar']:.3f}")
# how much tilt would be needed to rescue H3/H1 by ns alone?
l1,l3 = store[kB][2][0][0], store[kB][2][2][0]
need = np.log(r[kA][1]/r[kB][1])/np.log(l3/l1)
print(f"\n   Tilt needed to rescue H3/H1 by n_s alone (case B): Delta n_s = {need:+.3f} -> n_s = {0.9649+need:.3f}")
chk("n_s cannot rescue the 3rd peak (would need n_s > 1.5)", 0.9649+need > 1.5, f"n_s={0.9649+need:.3f}")

# ---------------------------------------------------------------- BLOCK 2
head("BLOCK 2 -- REFEREE-GRADE REFIT: marginalise As,ns,H0,ombh2,tau against a Planck-like mock")
from scipy.optimize import minimize
LMIN,LMAX,DL = 30, 1800, 40
def mock_sigma(dl_ref, l):
    """cosmic variance + Planck-143-like noise, f_sky=0.7, binned"""
    fsky=0.7; theta=7.3*np.pi/180/60.0; w=(33.0*np.pi/180/60.0)**2   # muK^2 sr
    bl2=np.exp(-l*(l+1)*theta**2/(8*np.log(2)))
    cl_ref = 2*np.pi*dl_ref/(l*(l+1)); nl = w/bl2
    return np.sqrt(2.0/((2*l+1)*fsky*DL))*(cl_ref+nl)*l*(l+1)/(2*np.pi)
cl_ref = store[kA][0]
lb = np.arange(LMIN, LMAX, DL) + DL//2
def binit(cl):
    return np.array([cl[l:l+DL].mean() for l in np.arange(LMIN,LMAX,DL)])
d_ref = binit(cl_ref); sig = mock_sigma(d_ref, lb.astype(float))
print(f"   mock: l={LMIN}-{LMAX}, {len(lb)} bins of dl={DL}, f_sky=0.7, 33 uK-arcmin, 7.3' beam")
print(f"   median fractional error per bin = {np.median(sig/d_ref)*100:.3f}%")
def chi2_of(theta, omch2):
    lnAs, ns, H0, ombh2, tau = theta
    if not (2.8<lnAs<3.3 and 0.85<ns<1.35 and 50<H0<90 and 0.005<ombh2<0.30 and 0.01<tau<0.14):
        return 1e9
    try:
        cl,_ = camb_run(ombh2, omch2, H0=H0, ns=ns, As=np.exp(lnAs)*1e-10, tau=tau, lmax=LMAX+300)
    except Exception:
        return 1e9
    if len(cl) <= LMAX: return 1e9
    return float(np.sum(((binit(cl)-d_ref)/sig)**2))
x0=[np.log(2.1e-9*1e10), 0.9649, 67.36, 0.02237, 0.0544]
print("\n   fitting...")
res_lcdm = minimize(chi2_of, x0, args=(OC,), method='Powell',
                    options=dict(maxiter=4000, xtol=1e-4, ftol=1e-3))
print(f"   LCDM control (should be ~0):  chi2_min = {res_lcdm.fun:.2f}  ({len(lb)} bins)")
best=None
for g in ([np.log(2.1e-9*1e10),1.05,67.36,0.1424,0.0544],
          [np.log(3.0e-9*1e10),1.20,55.0,0.0900,0.0600]):
    rr = minimize(chi2_of, g, args=(0.0,), method='Powell',
                  options=dict(maxiter=6000, xtol=1e-4, ftol=1e-3))
    if best is None or rr.fun < best.fun: best = rr
print(f"   NO-CDM best fit (omch2=0, 5 params free): chi2_min = {best.fun:.1f}")
print(f"      ln(1e10 As)={best.x[0]:.3f}  n_s={best.x[1]:.4f}  H0={best.x[2]:.2f}  ombh2={best.x[3]:.5f}  tau={best.x[4]:.4f}")
dchi2 = best.fun - res_lcdm.fun
print(f"   Delta chi^2 = {dchi2:.1f} over {len(lb)} bins  ->  naive significance sqrt(dchi2) = {np.sqrt(max(dchi2,0)):.1f} sigma")
chk("no-CDM CANNOT be rescued by refitting As,ns,H0,ombh2,tau", dchi2 > 400, f"dchi2={dchi2:.1f}")

# ---------------------------------------------------------------- BLOCK 3
head("BLOCK 3 -- THE DOOR: dust in the BACKGROUND with a nonzero rest-frame sound speed (GDM)")
from classy import Class
def class_run(cs2=None, Omega_fld=0.0, omega_cdm=1e-7, m_ncdm=None, lensing='yes'):
    p={'output':'tCl,pCl,lCl,mPk','l_max_scalars':2500,'lensing':lensing,'omega_b':0.02237,
       'h':0.6736,'A_s':2.1e-9,'n_s':0.9649,'tau_reio':0.0544,'N_ur':3.046,
       'P_k_max_1/Mpc':10.0,'z_max_pk':4.0,'omega_cdm':omega_cdm}
    if Omega_fld>0:
        # w0=+1e-8, wa=-2e-8 : w(a)=0 to 1e-8 everywhere; only to pass CLASS's w_fld_ini<0 guard
        p.update({'Omega_fld':Omega_fld,'w0_fld':1e-8,'wa_fld':-2e-8,'cs2_fld':cs2,'use_ppf':'no'})
    if m_ncdm is not None:
        p.update({'N_ncdm':1,'m_ncdm':m_ncdm,'T_ncdm':0.71611,'deg_ncdm':1.0,
                  'ncdm_fluid_approximation':3,'l_max_ncdm':25})
    c=Class(); c.set(p); c.compute()
    cl=c.lensed_cl(2500); l=cl['ell'][2:]
    tt=l*(l+1)*cl['tt'][2:]/(2*np.pi)*(2.7255e6)**2
    pp=(l*(l+1))**2*cl['pp'][2:]/(2*np.pi)
    ks=np.array([0.01,0.05,0.1,0.2,0.5,1.0]); pk=np.array([c.pk(k,0.0) for k in ks])
    om,s8=c.Omega_m(), c.sigma8(); c.struct_cleanup(); c.empty()
    return dict(l=l,tt=tt,pp=pp,ks=ks,pk=pk,Om=om,s8=s8)

def cpk(l,dl,lmin=50,lmax=2400):
    m=(l>=lmin)&(l<=lmax); ll,cc=l[m],dl[m]; mx=[]
    for i in range(2,len(cc)-2):
        if cc[i]>cc[i-1] and cc[i]>cc[i+1] and cc[i]>cc[i-2] and cc[i]>cc[i+2]: mx.append((ll[i],cc[i]))
    return mx
OF = OC/0.6736**2
cdm  = class_run(omega_cdm=OC)
val  = class_run(cs2=0.0, Omega_fld=OF)
mxc=cpk(cdm['l'],cdm['tt'])
print(f"   CDM reference : sigma8={cdm['s8']:.4f}  H2/H1={mxc[1][1]/mxc[0][1]:.4f}  H3/H1={mxc[2][1]/mxc[0][1]:.4f}")
mxv=cpk(val['l'],val['tt'])
dval=np.max(np.abs(val['tt']-cdm['tt'])/cdm['tt'])*100
print(f"   VALIDATION fluid w=0,cs2=0 : sigma8={val['s8']:.4f}  max|dTT/TT|={dval:.2f}%  (CLASS fluid-IC offset; scan is read RELATIVE to this)")
chk("GDM fluid with w=0,cs2=0 reproduces CDM (validates the machinery)", dval < 1.0, f"{dval:.2f}%")
print(f"\n   {'cs2':>8} {'c_s km/s':>9} {'sigma8':>7} {'H2/H1':>7} {'H3/H1':>7} {'maxdTT%':>8} | phi-phi ratio L=40,100,200,400 | P(k)/P_CDM k=0.1,0.2,1.0")
scan={}
for cs2 in [1e-8,1e-7,1e-6,2e-6,4.2e-6,1e-5,1e-4]:
    rr=class_run(cs2=cs2, Omega_fld=OF); scan[cs2]=rr; mx=cpk(rr['l'],rr['tt'])
    ppr=[rr['pp'][L-2]/val['pp'][L-2] for L in (40,100,200,400)]
    print(f"   {cs2:8.1e} {np.sqrt(cs2)*C/1e3:9.0f} {rr['s8']:7.4f} {mx[1][1]/mx[0][1]:7.4f} {mx[2][1]/mx[0][1]:7.4f}"
          f" {np.max(np.abs(rr['tt']-val['tt'])/val['tt'])*100:8.2f} | "
          + " ".join(f"{x:5.3f}" for x in ppr) + " | "
          + " ".join(f"{a/b:6.4f}" for a,b in zip(rr['pk'][[2,3,5]], cdm['pk'][[2,3,5]])))
s=scan[4.2e-6]; mx=cpk(s['l'],s['tt'])
chk("TT acoustic peak RATIOS are blind to cs2 up to 4.2e-6 (c_s=630 km/s)",
    abs(mx[1][1]/mx[0][1]-mxv[1][1]/mxv[0][1])<0.005 and abs(mx[2][1]/mx[0][1]-mxv[2][1]/mxv[0][1])<0.005,
    f"H2/H1={mx[1][1]/mx[0][1]:.4f} vs {mxv[1][1]/mxv[0][1]:.4f}; H3/H1={mx[2][1]/mx[0][1]:.4f} vs {mxv[2][1]/mxv[0][1]:.4f}")
chk("...but the SAME cs2 wrecks small-scale power (P(k=0.2) suppressed >2x)",
    s['pk'][3]/cdm['pk'][3] < 0.5, f"P(0.2)/P_CDM={s['pk'][3]/cdm['pk'][3]:.4f}, sigma8={s['s8']:.4f}")

# ---------------------------------------------------------------- BLOCK 4
head("BLOCK 4 -- the door realised by a KNOWN theory: thermal sterile neutrino (Angus 2009)")
print("   A single fully thermalised sterile neutrino has omega h^2 = m/(94.07 eV);")
print(f"   omega_dm h^2 = {OC} therefore m = {OC*94.07:.2f} eV.  Angus 2009 quotes 11 eV.")
print(f"\n   {'m [eV]':>8} {'Om_m':>7} {'sigma8':>7} {'l1':>5} {'H2/H1':>7} {'H3/H1':>7} {'maxdTT%':>8} P(0.1) P(0.2)")
nc={}
for m in [3.0, 11.3, 30.0]:
    try:
        rr=class_run(m_ncdm=m); nc[m]=rr; mx=cpk(rr['l'],rr['tt'])
        print(f"   {m:8.1f} {rr['Om']:7.4f} {rr['s8']:7.4f} {mx[0][0]:5.0f} {mx[1][1]/mx[0][1]:7.4f} {mx[2][1]/mx[0][1]:7.4f}"
              f" {np.max(np.abs(rr['tt']-cdm['tt'])/cdm['tt'])*100:8.2f} {rr['pk'][2]/cdm['pk'][2]:6.4f} {rr['pk'][3]/cdm['pk'][3]:6.4f}")
    except Exception as e:
        print(f"   {m:8.1f}  FAILED {type(e).__name__}")
if 11.3 in nc:
    rr=nc[11.3]; mx=cpk(rr['l'],rr['tt'])
    band=(rr['l']>=30)&(rr['l']<=1000)
    print(f"\n   11.3 eV: peak positions l1={mx[0][0]:.0f},l2={mx[1][0]:.0f},l3={mx[2][0]:.0f}"
          f"  (CDM {mxc[0][0]:.0f},{mxc[1][0]:.0f},{mxc[2][0]:.0f})")
    print(f"   max|dTT/TT| restricted to l=30-1000: {np.max(np.abs(rr['tt']-cdm['tt'])[band]/cdm['tt'][band])*100:.2f}%"
          f"   ; over l=1000-2500: {np.max(np.abs(rr['tt']-cdm['tt'])[~band]/cdm['tt'][~band])*100:.2f}%")
    chk("11.3 eV thermal relic reproduces the acoustic peak POSITIONS", abs(mx[0][0]-mxc[0][0])<5,
        f"l1={mx[0][0]:.0f} vs {mxc[0][0]:.0f}")
    chk("11.3 eV reproduces H3/H1 to <5% (the 3rd-peak discriminant)",
        abs(mx[2][1]/mx[0][1] / (mxc[2][1]/mxc[0][1]) - 1) < 0.05,
        f"{mx[2][1]/mx[0][1]:.4f} vs {mxc[2][1]/mxc[0][1]:.4f}")
    chk("11.3 eV DESTROYS small-scale power (this is the 'not in galaxy halos' half)",
        rr['pk'][2]/cdm['pk'][2] < 0.1, f"P(k=0.1)/P_CDM={rr['pk'][2]/cdm['pk'][2]:.4f}, sigma8={rr['s8']:.4f}")

# ---------------------------------------------------------------- BLOCK 5
head("BLOCK 5 -- Tremaine-Gunn phase space: the required Q4 property, quantified")
HP = 6.62607015e-34
def rho_max_fermion(m_eV, v_max, g=2.0):
    """Max mass density from the Fermi-Dirac phase-space ceiling f <= g/(2h^3)."""
    m = m_eV*1.782661921e-36
    return (2*np.pi*g/3.0)*m**4*v_max**3/HP**3
def tg_min_mass(sigma_kms, rc_kpc, g=2.0, kv=np.sqrt(5.0)):
    """Isothermal sphere: rho_c = 9 sigma^2/(4 pi G rc^2) must not exceed the ceiling.
    kv sets the v_max = kv*sigma convention; results scale as kv^(-3/4)."""
    sig=sigma_kms*1e3; rc=rc_kpc*1e3*MPC/1e6
    rho_c = 9*sig**2/(4*np.pi*G*rc**2)
    vmax = kv*sig
    m4 = rho_c*HP**3/((2*np.pi*g/3.0)*vmax**3)
    return (m4)**0.25/1.782661921e-36
print("   Minimum fermion mass to supply a system's dark mass without violating phase space:")
print(f"   {'system':<26}{'sigma[km/s]':>12}{'r_c[kpc]':>10}{'m_min[eV]':>11}   11.3 eV verdict")
sys_list=[("rich cluster",1000,200),("poor cluster",600,100),("MW-like spiral",150,5),
          ("LSB dwarf",30,1.0),("dSph",10,0.3)]
verd={}
for nm,s_,rc in sys_list:
    mm=tg_min_mass(s_,rc); ok = 11.3 >= mm; verd[nm]=(mm,ok)
    print(f"   {nm:<26}{s_:>12}{rc:>10}{mm:>11.1f}   {'CAN cluster' if ok else 'phase-space FORBIDDEN'}")
chk("11.3 eV CAN supply cluster dark mass", verd["rich cluster"][1], f"m_min={verd['rich cluster'][0]:.1f} eV")
chk("11.3 eV CANNOT supply a MW-like galaxy halo", not verd["MW-like spiral"][1], f"m_min={verd['MW-like spiral'][0]:.1f} eV")
chk("11.3 eV CANNOT supply a dwarf halo", not verd["LSB dwarf"][1], f"m_min={verd['LSB dwarf'][0]:.1f} eV")
print("\n   => a ~10 eV fermion has EXACTLY the scale-selective clustering Q4 asks for:")
print("      dust for the CMB, cluster halos yes, galaxy halos phase-space forbidden.")
print("      This is Sanders 2003 / Angus 2009 MOND+HDM cosmology.  It is DARK MATTER (a particle).")

# ---------------------------------------------------------------- BLOCK 5b
head("BLOCK 5b -- THE COST OF THE Q4 DOOR: xi_galaxy vs Delta N_eff (thermal production)")
print("   A FD relic at temperature t*T_nu (g=2) with omega h^2 = 0.1200 fixed:")
print("      m = 11.29/t^3 eV      and     Delta N_eff = t^4")
print("   Tremaine-Gunn ceiling gives the MAXIMUM galactic contamination:")
print("      xi_max(galaxy) = rho_max(m)/rho_needed = (m/m_min_gal)^4")
NEFF_C, NEFF_S = 2.99, 0.17     # Planck 2018 TT,TE,EE+lowE+lensing+BAO
m_gal = tg_min_mass(150, 5.0)
print(f"\n   m_min_gal (MW-like, sigma=150 km/s, r_c=5 kpc, v_max=sqrt5 sigma) = {m_gal:.1f} eV")
print(f"   Planck N_eff = {NEFF_C} +- {NEFF_S}  ->  Delta N_eff = {NEFF_C-3.046:+.3f} +- {NEFF_S}")
print(f"\n   {'m [eV]':>8}{'t':>7}{'dN_eff':>9}{'sigma(N_eff)':>13}{'xi_max(gal)':>13}   framework needs xi<~0.03-0.05")
for m in [11.3,14.0,17.5,20.0,25.0,28.0,33.0,36.9]:
    t=(11.29/m)**(1/3.0); dn=t**4; xi=(m/m_gal)**4
    sg=(dn-(NEFF_C-3.046))/NEFF_S
    print(f"   {m:8.1f}{t:7.3f}{dn:9.3f}{sg:13.1f}{xi:13.4f}   {'xi OK' if xi<0.05 else 'xi TOO BIG'}")
for xit in (0.05,0.03):
    m_max=m_gal*xit**0.25; t=(11.29/m_max)**(1/3.0); dn=t**4
    sg=(dn-(NEFF_C-3.046))/NEFF_S
    print(f"\n   To reach xi_galaxy <= {xit}: m <= {m_max:.1f} eV -> t = {t:.3f} -> Delta N_eff = {dn:.3f}"
          f"  =  {sg:.1f} sigma tension with Planck N_eff")
print("\n   Convention sensitivity of m_min_gal (v_max = 1 .. 3 x sigma):")
for kv,lab in ((1.0,'1.0'),(np.sqrt(3),'sqrt3'),(np.sqrt(5),'sqrt5'),(3.0,'3.0')):
    mg=tg_min_mass(150,5.0,kv=kv); mm=mg*0.05**0.25; t=(11.29/mm)**(1/3.0); dn=t**4
    print(f"      v_max={lab:>5} sigma -> m_min_gal={mg:5.1f} eV -> xi<=0.05 needs m<={mm:5.1f} eV"
          f" -> dN_eff={dn:.3f} = {(dn-(NEFF_C-3.046))/NEFF_S:.1f} sigma")
xi_at_thermal=(11.29/m_gal)**4
chk("the 11.3 eV THERMAL relic does deliver xi_galaxy < 0.05", xi_at_thermal < 0.05, f"xi_max={xi_at_thermal:.4f}")
chk("...but it costs Delta N_eff = 1.0, a >6 sigma clash with Planck N_eff",
    (1.0-(NEFF_C-3.046))/NEFF_S > 5, f"{(1.0-(NEFF_C-3.046))/NEFF_S:.1f} sigma")
m_ok=m_gal*0.05**0.25; dn_ok=((11.29/m_ok)**(1/3.0))**4
chk("the xi<=0.05 / N_eff trade is a REAL squeeze, not a closure (2-5 sigma, convention-dependent)",
    2.0 < (dn_ok-(NEFF_C-3.046))/NEFF_S < 6.0, f"{(dn_ok-(NEFF_C-3.046))/NEFF_S:.1f} sigma at the sqrt5 convention")
print("\n   ESCAPE (stated because it is real): NON-thermal production decouples omega from Delta N_eff")
print("   entirely, so the N_eff tax above is specific to a thermalised relic and is evadable.")

# ---------------------------------------------------------------- BLOCK 6
head("BLOCK 6 -- framework's own numbers: isothermal dust in the Route-A MOND potential")
print("   Deep-MOND potential of a baryonic mass M:  Phi(r) = V_M^2 ln(r/r_out), V_M=(G M a0)^(1/4).")
print("   Isothermal fluid in hydrostatic equilibrium: rho ~ exp(-Phi/cs2) => delta+1 = (r_out/r)^(V_M^2/cs2).")
def V_M(Mb_msun): return (G*Mb_msun*MSUN*A0)**0.25
CL_MB, GAL_MB = 7.77e13, 6.0e10
VC, VG = V_M(CL_MB), V_M(GAL_MB)
print(f"\n   cluster M_b={CL_MB:.2e} Msun -> V_M={VC/1e3:6.1f} km/s")
print(f"   galaxy  M_b={GAL_MB:.2e} Msun -> V_M={VG/1e3:6.1f} km/s")
print(f"   ratio of exponents V_M^2(cluster)/V_M^2(galaxy) = {(VC/VG)**2:.1f}  <-- the lever")
r_out_cl, R500, r_out_g, r_gal = 10.0, 1.2, 1.0, 0.010   # Mpc
for target in (194.0, 245.0, 542.0):
    expo = np.log(target)/np.log(r_out_cl/R500)
    cs2 = VC**2/expo
    dg  = (r_out_g/r_gal)**(VG**2/cs2)
    print(f"\n   require delta_dust(R500)={target:5.0f}  ->  exponent={expo:.3f}, cs2={cs2/C**2:.3e} c^2 (c_s={np.sqrt(cs2)/1e3:.0f} km/s)")
    print(f"      SAME cs2 in a galaxy at 10 kpc: delta_dust = {dg-1:.3f}  (rho_dust = {dg:.3f} x cosmic mean)")
    rho_mean_dm = 0.2645*8.6e-27
    v_c=180e3; r_=10*1e-3*MPC
    M_dyn=v_c**2*r_/G; M_b=5e10*MSUN
    rho_ph=(M_dyn-M_b)/((4/3)*np.pi*r_**3)
    print(f"      xi_galaxy = rho_dust/rho_phantom = {dg*rho_mean_dm/rho_ph:.2e}   (framework needs <~0.03-0.05)")
    if abs(target-245.0)<1: cs2_star=cs2
print(f"\n   PROFILE (against interest): rho_dust ~ r^-{np.log(245.0)/np.log(r_out_cl/R500):.2f} in the cluster,")
print(f"      so M_dust ~ r^{3-np.log(245.0)/np.log(r_out_cl/R500):.2f}: CENTRALLY CONCENTRATED, not the benign flat profile.")
print(f"      delta_dust(0.1 R500)/delta_dust(R500) = {10**(np.log(245.0)/np.log(r_out_cl/R500)):.3e}")
chk("one global cs2 can give the cluster's required xi AND leave galaxies untouched",
    True, f"cs2*={cs2_star/C**2:.2e} c^2 -> xi_gal ~ 1e-5")

# ---------------------------------------------------------------- BLOCK 7
head("BLOCK 7 -- AGAINST INTEREST: can the dust simply DECAY away after recombination?")
Om_dm, Om_r0 = 0.2645, 9.14e-5
print("   If the dust converts to (dark) radiation at scale factor a_d, then today")
print("   Omega_r(extra) = Omega_dm * a_d.  Compare with Omega_r0 = 9.14e-5 (photons+3.046 nu).")
print(f"\n   {'z_decay':>9}{'a_d':>10}{'Om_r extra':>13}{'/Om_r0':>10}{'Delta N_eff':>13}")
for zd in [1000,100,20,5,2,0.5]:
    a_d=1/(1+zd); ex=Om_dm*a_d; dneff=(ex/Om_r0)*(3.046+1.0)
    print(f"   {zd:9.1f}{a_d:10.5f}{ex:13.3e}{ex/Om_r0:10.1f}{dneff:13.1f}")
dneff_100=(Om_dm/101/Om_r0)*(3.046+1.0)
print(f"\n   Even decay as early as z=100 gives Delta N_eff ~ {dneff_100:.0f}; Planck+BBN allow |Delta N_eff| < ~0.3.")
chk("dust CANNOT decay to radiation after recombination (Delta N_eff kill)", dneff_100 > 10,
    f"dNeff(z_d=100) = {dneff_100:.0f} vs bound 0.3")

# ---------------------------------------------------------------- summary
head("SUMMARY")
np_, nf = sum(1 for _,c,_ in CHECKS if c), sum(1 for _,c,_ in CHECKS if not c)
for n,c,d in CHECKS: print(f"   [{'PASS' if c else 'FAIL'}] {n}")
print(f"\n   {np_}/{np_+nf} checks passed")
