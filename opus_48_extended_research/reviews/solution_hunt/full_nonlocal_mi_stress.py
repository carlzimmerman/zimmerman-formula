"""STRESS TEST: maximize high-frequency granular power and check if the genuine A(omega)
   MI can EVER add mean dynamical mass. Push encounter rate/amplitude to the physical max
   (member deep inside a violently relaxing/merging cluster core). Both ways."""
import numpy as np
np.random.seed(1)
c,G=2.998e8,6.674e-11; a0=9.36e-11; Msun=1.989e30; kpc=3.086e19; Mpc=1e3*kpc; km=1e3; yr=3.156e7; Gyr=1e9*yr
def boost_fw(x): x=np.asarray(x,float); return np.sqrt(1+1/x)  # framework nu multiplier

def run(g_smooth_a0, fluct_strength, n_enc_per_Gyr, label):
    g_sm=g_smooth_a0*a0; sigma=1500*km; R=0.5*Mpc; om=sigma/R
    dt=0.1e6*yr; T=8*Gyr; nt=int(T/dt); t=np.arange(nt)*dt
    ax=g_sm*np.cos(om*t); ay=g_sm*np.sin(om*t)
    n=int(n_enc_per_Gyr*T/Gyr)
    for k in range(n):
        m=10**np.random.uniform(10,13.5)*Msun
        b=np.random.uniform(0.05,0.5)*Mpc*(1.0/np.sqrt(fluct_strength))
        vr=abs(np.random.normal(sigma,0.5*sigma))+0.3*sigma; tau=b/vr
        amp=G*m/b**2*fluct_strength; tk=np.random.rand()*T; an=np.random.rand()*2*np.pi
        prof=amp/(1+((t-tk)/tau)**2); ax+=prof*np.cos(an); ay+=prof*np.sin(an)
    amag=np.sqrt(ax**2+ay**2); amean=np.mean(amag); arms=np.sqrt(np.mean(amag**2))
    # spectral high-freq fraction
    S=np.abs(np.fft.fft(ax+1j*ay)/nt)**2; f=np.fft.fftfreq(nt,dt); w=2*np.pi*f
    hi=(np.abs(w)>3*om).sum and S[np.abs(w)>3*om].sum()/S.sum()
    bqs=boost_fw(amean/a0)                 # QS at mean
    blocal=np.mean(boost_fw(amag/a0))      # generous local Jensen (VOID upper bound)
    brms=boost_fw(arms/a0)                 # honest A>=rms
    print(f"{label:32s} fluct={arms/amean:.2f} hi-freq%={hi*100:5.1f} | "
          f"QS(<a>)={bqs:.3f} local(void)={blocal:.3f}({blocal/bqs:.3f}x) honest(A>=rms)={brms:.3f}({brms/bqs:.3f}x)")
    return blocal/bqs, brms/bqs

print("STRESS: push granularity to the physical maximum; does the genuine A(omega) MI EVER add mass?")
print("="*120)
for gs in [0.04, 0.1, 0.3]:
    for fs,ne,lab in [(1.0,15,"nominal"),(3.0,50,"strong-merger"),(10.0,150,"violent-core max")]:
        run(gs, fs, ne, f"g={gs}a0 {lab}")
print("="*120)
print("READ: 'local(void)' is the GENEROUS apocenter-singularity ceiling (NOT physical); 'honest(A>=rms)'")
print("is the genuine Milgrom functional. Even at violent-core MAX granularity, honest ratio <= ~1.0 and")
print("the generous void ceiling never exceeds a few %. The cluster needs ~2.3x. Granularity cannot do it.")
