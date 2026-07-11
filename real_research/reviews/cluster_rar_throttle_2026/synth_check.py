import numpy as np
Z=np.sqrt(32*np.pi/3); yc=Z/2
print("Z=%.4f yc=%.4f"%(Z,yc))
a0c=9.36e-11; a0a=1.13e-10
print("break g_bar canonical=%.3e alt=%.3e ratio=%.3f"%(yc*a0c,yc*a0a,(yc*a0a)/(yc*a0c)))

def nu(y): return np.sqrt(1+1/y)
def T(y,n): return np.minimum(1,(yc/y)**n)
# g_obs = [1+(nu-1)*T] g_bar ; fingerprint = log10(g_full_throttle_off?) 
# break fingerprint = difference between plain MOND (T=1) and throttled, in dex of g_obs
def gplain(y): return (1+(nu(y)-1))*1.0   # boost factor = nu
def gthr(y,n): return 1+(nu(y)-1)*T(y,n)
for n in [1,2]:
    ys=np.linspace(yc,50,20000)
    dex=np.log10(gplain(ys))-np.log10(gthr(ys,n))
    imax=np.argmax(dex)
    print("n=%d peak fingerprint=%.4f dex at y=%.2f"%(n,dex[imax],ys[imax]))
    # fractional loss in g_obs
    frac=(gthr(ys,n)-gplain(ys))/gplain(ys)
    imin=np.argmin(frac)
    print("   worst frac g_obs loss=%.4f at y=%.2f"%(frac[imin],ys[imin]))
    for yy in [3,5,10,15,20,50]:
        print("   y=%2d dex=%.4f fracloss=%.4f"%(yy,np.log10(gplain(yy))-np.log10(gthr(yy,n)),(gthr(yy,n)-gplain(yy))/gplain(yy)))
# Tian coverage
print("Tian y_max canonical=%.2f alt=%.2f  (g_bar_max=2.1e-10)"%(2.1e-10/a0c,2.1e-10/a0a))
print("scatter 0.147 lognormal in dex=%.4f"%(np.log10(1.147)))
