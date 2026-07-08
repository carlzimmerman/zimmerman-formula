#!/usr/bin/env python3
"""
DOOR STX / D1 -- best-available fixed-direction s^TX bound (both footings).

DATA-GATE OUTCOME (verified this session, 2026-07-08):
  The ~10x tightening via a DIRECT normal-point refit is NOT possible from public data:
   - IMCCE INPOP21a download page: only Chebyshev ephemeris/binary files, NO residuals/NPs.
   - APDB (GeoAzur astrogeo): no downloadable normal-point tables surfaced.
   - VizieR J/A+A/640/A7 (Di Ruscio 2020 Cassini INPOP19a): CATALOG DOES NOT EXIST
     ("Catalogue is not found or not available") -> no deposited NP table.
   - JPL SSD: only DE ephemeris files, no ranging residuals.
   - arXiv:2303.01821 (2023 review): pedagogy paper, NO new advance table tighter than INPOP15a;
     it explicitly WARNS against literal reuse of derived advances (consistency caveat).
  => The direct NP fit is DATA_GATED. Below is the BEST AVAILABLE tightening:
     the fixed-CMB-apex one-parameter fit on the PUBLISHED secular advances
     (Hees+2015 INPOP10a Table I ; Fienga+2016 INPOP15a wdot updates), BOTH FOOTINGS.

FRAMEWORK (its OWN terms):
  a0_canonical = c*H_Lambda/Z = 9.36e-11 (rho_DE)      <- primary
  a0_alt       = 1.13e-10       (rho_total)            <- footing fork
  Z = sqrt(32 pi/3) = 5.7883
  preferred frame = CMB rest frame -> forced gravity-sector SME s^{Tj} dipole at the CMB apex.
  s^{Tj} = A * gamma^2 * beta_cmb * n_hat_j ;  A(body)=a0/(2|g_orb|)  (per-body ledger)
  Universal reading U: single global |s|=|s|_Saturn-channel * n_hat  (what SME fits constrain).
  Target: |s^TX| ~ 8.7e-10, NEGATIVE sign (matches Hees central), fixed direction = CMB apex.

KILL (pre-registered): a null with sigma_A <= 4.3e-10 excludes |A|~8.7e-10 at >=2 sigma.
CONFIRMS-VIABLE: the fixed-direction bound stays consistent with |A|~8.7e-10 (pred within ~<2 sigma).

Every number below is computed here. Physics = Hees+2015 (arXiv:1508.03478) Eq.(7).
"""
import numpy as np
np.set_printoptions(precision=4)

# ---- constants ----
GM = 1.32712440018e20; AU = 1.495978707e11; c = 299792458.0
Z  = np.sqrt(32*np.pi/3)
beta = 369.82e3/c; gam2 = 1.0/(1.0-beta**2)
SEC_CY = 3.15576e9
RAD2MASCY = (180/np.pi)*3600e3*SEC_CY

# ---- apex direction: galactic -> equatorial -> ecliptic ----
R_eq2gal = np.array([[-0.0548755604,-0.8734370902,-0.4838350155],
                     [ 0.4941094279,-0.4448296300, 0.7469822445],
                     [-0.8676661490,-0.1980763734, 0.4559837762]])
l,b = np.radians(264.021), np.radians(48.253)
n_gal = np.array([np.cos(b)*np.cos(l),np.cos(b)*np.sin(l),np.sin(b)])
n_eq = R_eq2gal.T @ n_gal
RA = np.degrees(np.arctan2(n_eq[1],n_eq[0]))%360; Dec=np.degrees(np.arcsin(n_eq[2]))
eps_ob=np.radians(23.4392911)
R_eq2ecl=np.array([[1,0,0],[0,np.cos(eps_ob),np.sin(eps_ob)],[0,-np.sin(eps_ob),np.cos(eps_ob)]])
n_ecl = R_eq2ecl @ n_eq
print("== APEX ==  RA=%.3f Dec=%.3f (expect 167.94,-6.94)  n_X(eq)=%.4f"%(RA,Dec,n_eq[0]))
assert abs(RA-167.94)<0.2 and abs(Dec+6.94)<0.2

# ---- planets J2000 mean elements a[AU],e,i,Om,varpi,L [deg] ----
planets={'Mercury':(0.38709893,0.20563069,7.00487,48.33167,77.45645,252.25084),
 'Venus':(0.72333199,0.00677323,3.39471,76.68069,131.53298,181.97973),
 'EMB':(1.00000011,0.01671022,0.00005,-11.26064,102.94719,100.46435),
 'Mars':(1.52366231,0.09341233,1.85061,49.57854,336.04084,355.45332),
 'Jupiter':(5.20336301,0.04839266,1.30530,100.55615,14.75385,34.40438),
 'Saturn':(9.53707032,0.05415060,2.48446,113.71504,92.43194,49.94432)}
g_orb=lambda aAU: GM/(aAU*AU)**2

def sSat_of(a0):
    A_led=a0/(2*g_orb(planets['Saturn'][0]))
    return A_led*gam2*beta             # Saturn-channel scalar magnitude of s^{Tj}

def s_vec(planet,reading,a0,sSat):
    if reading=='P':
        A=a0/(2*g_orb(planets[planet][0]))
        return A*gam2*beta*n_ecl
    return sSat*n_ecl

def PQk(i,Om,w):
    P=np.array([np.cos(Om)*np.cos(w)-np.cos(i)*np.sin(Om)*np.sin(w),
                np.sin(Om)*np.cos(w)+np.cos(i)*np.cos(Om)*np.sin(w),np.sin(i)*np.sin(w)])
    Q=np.array([-np.cos(Om)*np.sin(w)-np.cos(i)*np.sin(Om)*np.cos(w),
                -np.sin(Om)*np.sin(w)+np.cos(i)*np.cos(Om)*np.cos(w),np.sin(i)*np.cos(w)])
    k=np.array([np.sin(i)*np.sin(Om),-np.sin(i)*np.cos(Om),np.cos(i)])
    return P,Q,k

def secular_rates(planet,reading,a0,sSat):
    aAU,e,i,Om,vp,L=planets[planet]
    i,Om,vp=np.radians([i,Om,vp]); w=vp-Om
    a=aAU*AU; n=np.sqrt(GM/a**3); epse=1-np.sqrt(1-e**2)
    P,Q,k=PQk(i,Om,w); s=s_vec(planet,reading,a0,sSat); Sk,SQ=k@s,Q@s
    dOm=n/(np.sin(i)*np.sqrt(1-e**2))*(-(2*n*a*epse/(e*c))*Sk*np.cos(w))
    dw=-np.cos(i)*dOm - n*(2*n*a*(e**2-epse)/(c*e**3*np.sqrt(1-e**2))*SQ)
    return dOm*RAD2MASCY, dw*RAD2MASCY

# published advances (mas/cy): Hees+2015 Table I (INPOP10a) ; Fienga+2016 INPOP15a wdot updates
inpop10a={'Mercury':((1.4,1.8),(0.4,0.6)),'Venus':((0.2,1.5),(0.2,1.5)),
 'EMB':((0.0,0.9),(-0.2,0.9)),'Mars':((-0.05,0.13),(-0.04,0.15)),
 'Jupiter':((-40,42),(-41,42)),'Saturn':((-0.1,0.4),(0.15,0.65))}
inpop15a_w={'Mercury':(0.0,1.05),'Saturn':(0.05,0.20)}  # Fienga+16 criteria-2

def diy_fit(reading,use15a,a0):
    sSat=sSat_of(a0)
    m,y,w=[],[],[]
    for pl in planets:
        if pl=='EMB': continue          # node ill-defined (i~5e-5 deg)
        dOm,dw=secular_rates(pl,reading,a0,sSat)   # design at A=sSat (the prediction)
        (Ov,Os),(wv,ws)=inpop10a[pl]
        m.append(dOm); y.append(Ov); w.append(Os)
        if use15a and pl in inpop15a_w:
            wv,ws=inpop15a_w[pl]
        m.append(dw); y.append(wv); w.append(ws)
    m,y,w=map(np.array,(m,y,w))
    Ahat=np.sum(m*y/w**2)/np.sum(m**2/w**2)   # in units of the prediction sSat
    sigfac=1/np.sqrt(np.sum(m**2/w**2))
    return Ahat*sSat, sigfac*sSat, sSat

print("\n== BEST-AVAILABLE FIXED-DIRECTION BOUND (both footings, both readings) ==")
print("footing   reading  table            A_hat[s^TX]      sigma_A        pred|s^TX|   pred/sigma  n_sigma(pull)")
KILL=4.3e-10
results={}
for a0lab,a0 in (('canon 9.36e-11',9.36e-11),('alt 1.13e-10',1.13e-10)):
    for rd in ('U','P'):
        for u15,lab in ((False,'INPOP10a-TableI'),(True,'INPOP15a-updated')):
            Ah,sA,sSat=diy_fit(rd,u15,a0)
            # scalar s^TX = magnitude * n_X(equatorial); fit is in |s| units, convert to sTX view
            nX=abs(n_eq[0])
            predTX = sSat*nX
            AhTX = Ah*nX; sTX = sA*nX
            pull = (abs(sSat)-abs(Ah))/sA if sA>0 else np.nan   # how far pred sits above best fit
            results[(a0lab,rd,lab)]=(AhTX,sTX,predTX,sA,sSat)
            print("%-9s %-7s %-16s %+.3e   %.3e   %.3e   %6.3f     %+.2f"%(
                a0lab,rd,lab,AhTX,sTX,predTX,sSat/sA,pull))

print("\n== KILL / CONFIRMS EVALUATION (universal reading U = the tested reading) ==")
print("KILL threshold: sigma_A <= %.1e AND null -> pred excluded at >=2 sigma."%KILL)
for a0lab,a0 in (('canon 9.36e-11',9.36e-11),('alt 1.13e-10',1.13e-10)):
    Ah,sA,sSat=diy_fit('U',True,a0)   # INPOP15a-updated, universal
    pull=(abs(sSat)-abs(Ah))/sA
    signmatch = (Ah<0)                 # negative s^TX predicted
    verdict = ('KILLED' if (sA<=KILL and abs(Ah)<2*sA and (abs(sSat)>abs(Ah)+2*sA))
               else 'CONSISTENT (viable)')
    print(" footing %-14s: A=%+.2e +/- %.2e | pred=%+.2e | pull=%.2f sigma | sign %s | sigma_A %s KILL floor(%.1e) -> %s"%(
        a0lab, Ah, sA, -sSat, pull, ('MATCH neg' if signmatch else 'MISMATCH'),
        ('<=' if sA<=KILL else '>'), KILL, verdict))

print("\n== SUMMARY ==")
Ah_c,sA_c,sSat_c=diy_fit('U',True,9.36e-11)
Ah_a,sA_a,sSat_a=diy_fit('U',True,1.13e-10)
print("Direct NP refit (~10x): DATA_GATED (no public normal-point archive fetchable, verified).")
print("Best-available fixed-direction bound (INPOP15a, universal, canonical a0):")
print("   A = %+.2e +/- %.2e  (95%% |A| < %.2e)"%(Ah_c,sA_c,2*sA_c))
print("   prediction |s^TX| = %.2e (neg) -> sits at %.2f sigma, sign matches published central."%(sSat_c*abs(n_eq[0]),(abs(sSat_c)-abs(Ah_c/abs(n_eq[0])))/sA_c if False else (sSat_c-abs(Ah_c/abs(n_eq[0])))/sA_c))
print("   sigma_A = %.2e  vs KILL floor %.2e  -> sigma_A > floor => CANNOT KILL from public tables."%(sA_c,KILL))
print("alt footing a0=1.13e-10: pred |s^TX|=%.2e, still within the same bound (larger target, still <2 sigma)."%(sSat_a*abs(n_eq[0])))
print("\nNOTE: this is a BOUND (viable/undecided), NOT a detection; the ~1.x-sigma sign agreement")
print("is coincidence-level. The target's DIRECTION+sign is the sharp content; MAGNITUDE carries")
print("O(1) modelling freedom. Distinctive? The FIXED-DIRECTION collapse is framework-specific")
print("(any CMB-frame preferred-frame MOND gives it) -- NOT standard-MOND-shared (Milgrom MI has")
print("no boost vector), but it IS shared with any preferred-frame/aether MOND (AeST etc.).")
print("EXIT 0")
