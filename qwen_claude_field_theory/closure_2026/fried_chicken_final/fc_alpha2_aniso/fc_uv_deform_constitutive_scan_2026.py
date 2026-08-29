import numpy as np
# UV-deformed field kernel:  J_Y(u) = (1-e^-u) + (lam_inf-1)*(1 - e^{-(u/uc)^n})
# u = sqrt(Y)/a0.  deep-MOND: J_Y~u (mu=u).  UV: J_Y->lam_inf => lam_s=lam_inf, beta0=1/lam_inf.
def JY(u, lam, uc, n):
    return (1-np.exp(-u)) + (lam-1)*(1-np.exp(-(u/uc)**n))
def dJY(u, lam, uc, n):   # dJ_Y/du
    return np.exp(-u) + (lam-1)*np.exp(-(u/uc)**n)*n*(u/uc)**(n-1)/uc
uSS = 1e8   # Solar-System u ~ g_earth-sun/a0 ~ (6e-3)/(9.4e-11) ~ 6e7 ; use 1e8
print(f"{'lam_inf':>8}{'uc':>8}{'n':>3} | {'JY(uSS)':>10}{'ellip?':>8} | {'a2~1/JY(uSS)':>13} | deepMOND JY(0.1)~0.1?  intermediate band")
for lam in [1e6,1e7,1e8]:
    for uc in [1e2,1e4,1e6]:
        for n in [4,6]:
            ug = np.logspace(-4,12,4000)
            jy = JY(ug,lam,uc,n); djy = dJY(ug,lam,uc,n)
            L = jy + ug*djy               # J_Y + 2Y J_YY  (longitudinal ellipticity)
            ellip = np.all(jy>0) and np.all(L>0)
            jy_ss = JY(uSS,lam,uc,n)
            a2 = 1.0/jy_ss + 2.0/(2.5e-5*jy_ss**2)   # alpha_2 with K_B=2.5e-5 (alpha_1 max)
            dm = JY(0.1,lam,uc,n)         # deep-MOND: should be ~0.1 (mu=u)
            # intermediate band: where does J_Y cross, say, 10 and 1e4? (accel = a0*u ~)
            band_lo_u = uc*0.3; band_hi_u = uc*3
            g_lo = 9.4e-11*band_lo_u; g_hi = 9.4e-11*band_hi_u   # m/s^2 of the rise band
            print(f"{lam:8.0e}{uc:8.0e}{n:3d} | {jy_ss:10.3e}{str(ellip):>8} | {a2:13.3e} | JY(0.1)={dm:6.4f}  rise@g~[{g_lo:.1e},{g_hi:.1e}] m/s^2")
print()
print("KEY: alpha_2 PASSES only if JY(uSS)~lam_inf (screened at Solar System) => a2<1e-7.")
print("     deep-MOND intact needs JY(0.1)~0.1.  ellip = no fold from the monotone kernel.")
print("     'rise@g' band = accelerations where J_Y ramps 1->lam_inf; that band's gravity is Newtonianised (J_Y large).")
print("     a0=9.4e-11; wide-binary g~1e-10..1e-8; outer solar system ~1e-6..1e-3; cluster outskirts ~1e-10.")
