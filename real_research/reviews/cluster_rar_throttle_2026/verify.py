import numpy as np

# Framework constants
Z = np.sqrt(32*np.pi/3)
y_c = Z/2
a0_canon = 9.36e-11
a0_alt   = 1.13e-10
print(f"Z={Z:.4f}  y_c=Z/2={y_c:.4f}")

def nu(y):            # framework's OWN interpolation: g_obs=sqrt(g_bar^2+g_bar a0)
    return np.sqrt(1+1/y)   # = g_obs/g_bar

def T(y,n=1):
    return np.minimum(1,(y_c/y)**n)

def break_dex(y,n=1):
    plain = nu(y)                      # g_obs/g_bar plain framework MOND
    thr   = 1+(nu(y)-1)*T(y,n)         # throttled
    return np.log10(plain/thr)

# Break at requested y
for y in [3,4,5,5.5,6,7,8,10,20]:
    print(f"y={y:5.1f}  nu={nu(y):.5f}  T={T(y):.4f}  break={break_dex(y):.5f} dex")

# Peak
yy=np.linspace(y_c,50,100000)
b=break_dex(yy)
print(f"PEAK break={b.max():.5f} dex at y={yy[np.argmax(b)]:.3f}")

# Tian y-range
gbar_max=2.1e-10; gbar_min=1.3e-11
print(f"\nTian gbar_max={gbar_max:.2e} -> y_max canon={gbar_max/a0_canon:.3f} alt={gbar_max/a0_alt:.3f}")
print(f"Tian gbar_min={gbar_min:.2e} -> y_min canon={gbar_min/a0_canon:.3f} alt={gbar_min/a0_alt:.3f}")
print(f"break location gbar=y_c*a0: canon={y_c*a0_canon:.3e}  alt={y_c*a0_alt:.3e}")
print(f"y_c/y_max canon={y_c/(gbar_max/a0_canon):.3f}  alt={y_c/(gbar_max/a0_alt):.3f}")

# Cluster deficit: g_dagger=2.02e-9 vs a0
gd=2.02e-9
print(f"\ng_dagger/a0_canon={gd/a0_canon:.2f}  sqrt={np.sqrt(gd/a0_canon):.2f} (deep under-pred factor)")
print(f"g_dagger/galaxy1.2e-10={gd/1.2e-10:.2f}")

# throttle cost within Tian range: is T<1 anywhere?
print(f"\nWithin Tian range y<=2.24: throttle active? T(2.24)={T(2.24):.3f} (=1 means inactive)")

print("\n=== ROBUSTNESS: what if g_bar_max were underestimated? ===")
for gbar in [2.1e-10, 3.0e-10, 5.0e-10, 8.0e-10]:
    y=gbar/a0_canon
    print(f"gbar={gbar:.1e} -> y={y:.2f}  T={T(y):.3f}  break={break_dex(y):.5f} dex (vs 0.059 scatter)")

print("\n=== Cluster DEFICIT vs THROTTLE worsening (where throttle active) ===")
gd=2.02e-9
def g_data(gbar): return np.sqrt(gd*gbar)                    # cluster deep-MOND fit
def g_fw(gbar):   return np.sqrt(gbar**2+gbar*a0_canon)       # framework MOND
for gbar in [1.3e-11,2.1e-10]:
    defc=np.log10(g_data(gbar)/g_fw(gbar))
    print(f"gbar={gbar:.1e}: cluster deficit={defc:.3f} dex")
# throttle worsening at active y vs deficit magnitude
print("throttle max depletion 0.017 dex on ~0.4-0.67 dex deficit = %.1f%% relative"%(0.017/0.5*100))
