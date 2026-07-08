#!/usr/bin/env python3
"""
ADVERSARIAL REFUTATION -- LENS = acausality / secular growth.

The compute's SETUP A tested UHP-analyticity of the SYMBOL D(w)=w*K(-(w/a0)^2) via Titchmarsh and
declared CAUSAL. But the LENS demands more than a symbol-analyticity assertion:

  (1) ACTUALLY CONSTRUCT the time-domain retarded kernel G_R(t) = FT^{-1}[1/D_ret(w)] (and of the
      RESPONSE operator D_ret(w) itself), and CHECK its support: G_R(t)=0 for t<0 to numerical
      precision. A symbol "analytic in the UHP" is NECESSARY but the compute never did the inverse
      transform to exhibit a vanishing advanced tail. Branch points sitting ON the real axis
      (w=0, w=+-a0/2) are precisely where a Titchmarsh argument is DELICATE: a cut that touches the
      real axis can leak an advanced piece or a non-decaying tail.

  (2) SECULAR GROWTH: nonlocal-in-time operators famously produce t*sin, t*cos runaways (resonant
      response) or algebraically-growing tails. Check the late-time behavior of G_R(t) as t->+inf:
      does it DECAY (bounded response) or GROW (secular)? The w=0 branch point (K~1/(2 sqrt z) ~
      a0/(2|w|)) is a genuine IR concern: 1/|w| in a symbol FTs to a log/constant tail.

We test the framework's OWN operator. Two objects:
  A) the KINETIC/RESPONSE symbol  D(w) = w * K(-(w/a0)^2)   (the inertia operator eigenvalue)
  B) the PROPAGATOR symbol        P(w) = 1 / D(w)           (the retarded Green's function)
Retarded prescription: w -> w + i*eta, eta->0+, then inverse FT with a t>0 vs t<0 split.

We do the inverse transform NUMERICALLY at finite eta and watch:
  - support: |G_R(t<0)| vs |G_R(t>0)|  (advanced tail?)
  - late time: |G_R(t)| envelope as t grows (secular growth?)
Both a0 footings. Units a0=1 (dimensionless; a0 only sets the real-axis gap scale, checked separately).
"""
import numpy as np

np.seterr(all='ignore')
print("="*100)
print(" ADVERSARIAL REFUTATION -- acausality / secular growth: TIME-DOMAIN retarded kernel + support")
print("="*100)

# ---------------------------------------------------------------------------------------------------
# The framework operator, a0=1 units.  K(z)=(sqrt(1+4z)-1)/(2 sqrt z), z=-(w)^2  (proper freq w=u.k).
# For the RETARDED response we need the analytic continuation w -> w + i*eta of both sqrt's.
# ---------------------------------------------------------------------------------------------------
def K_ret(w, eta):
    """K(z) with z = -(w+i eta)^2, principal branches of both sqrt (retarded, UHP-analytic side)."""
    wc = w + 1j*eta
    z = -(wc**2)
    inner = np.sqrt(1.0 + 4.0*z)     # branch pt z=-1/4
    return (inner - 1.0) / (2.0*np.sqrt(z))   # branch pt z=0

def D_ret(w, eta):
    """Kinetic/response symbol D(w) = w*K(z). This is the INERTIA operator eigenvalue."""
    wc = w + 1j*eta
    return wc * K_ret(w, eta)

# ---------------------------------------------------------------------------------------------------
# STEP 1: exhibit the large-w structure D(w)/w = 1 + i a0/(2w) + ...  (the |u.k| pseudo-diff term).
#   The compute claimed D(w)/w = 1 + i a0/(2w). VERIFY numerically, and note: the +i/(2w) piece is
#   the retarded continuation of the -(a0/2)|w| symbol. Its inverse FT is the danger for causality.
# ---------------------------------------------------------------------------------------------------
print("\n[1] Large-w structure of D(w)/w (the pseudo-differential |u.k| term, retarded continuation)")
for w in [10.0, 50.0, 200.0, 1000.0]:
    d = D_ret(w, 1e-9)/w
    approx = 1.0 + 1j/(2.0*w)   # a0=1
    print(f"   w={w:7.1f}:  D/w = {d.real:+.6f}{d.imag:+.6e}i   vs 1+i/(2w)={approx.real:+.6f}{approx.imag:+.6e}i")

# ---------------------------------------------------------------------------------------------------
# STEP 2: CONSTRUCT the retarded kernel in TIME. G_R(t) = (1/2pi) INT dw e^{-i w t} f(w+i eta).
#   Do it for BOTH the response symbol D and the propagator 1/D. Use a dense grid + small eta.
#   CAUSALITY TEST: G_R(t) must vanish for t<0 (advanced tail = FAIL). Do the honest FFT.
# ---------------------------------------------------------------------------------------------------
print("\n[2] TIME-DOMAIN retarded kernels via inverse FT (the construction the compute did NOT do)")

def retarded_kernel(symbol_fn, eta, Wmax, N, subtract=None):
    """Inverse FT of symbol_fn(w,eta) -> g(t). Returns (t, g). subtract: a function of w removed before
       transform (to kill a non-decaying constant/linear part that is a contact/local term, not a tail)."""
    w = np.linspace(-Wmax, Wmax, N, endpoint=False)
    dw = w[1]-w[0]
    F = symbol_fn(w, eta)
    if subtract is not None:
        F = F - subtract(w)
    F = np.nan_to_num(F, nan=0.0, posinf=0.0, neginf=0.0)
    # g(t) = (1/2pi) INT dw e^{-i w t} F(w).  Build t-grid conjugate to w.
    t = np.fft.fftshift(np.fft.fftfreq(N, d=dw)) * 2*np.pi
    # e^{-i w t}: use ifft convention. F is on w-grid symmetric about 0; shift for fft.
    g = np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(F))) * (N*dw) / (2*np.pi)
    return t, g

# --- PROPAGATOR 1/D : the physical retarded Green's function of the inertia operator ---
# D(w)=w*K -> near w=0, K ~ 1/(2|w|)*... actually K(z=-w^2): as w->0, z->0-, K~1/(2 sqrt z). Let's just
# transform 1/D numerically with a regulator and inspect support + late-time envelope.
def prop_symbol(w, eta):
    d = D_ret(w, eta)
    return 1.0/d

eta = 1e-3
Wmax = 2000.0
N = 2**20
t, gP = retarded_kernel(prop_symbol, eta, Wmax, N)

# support test: energy in t<0 vs t>0 (exclude a tiny |t|<t0 core around origin where FFT ringing lives)
dt = t[1]-t[0]
core = np.abs(t) < 5*dt
neg = (t < 0) & ~core
pos = (t > 0) & ~core
E_neg = np.trapz(np.abs(gP[neg])**2, t[neg])
E_pos = np.trapz(np.abs(gP[pos])**2, t[pos])
print(f"   PROPAGATOR 1/D:  energy(t<0)={E_neg:.3e}   energy(t>0)={E_pos:.3e}   ratio neg/pos={E_neg/max(E_pos,1e-300):.3e}")
causal_prop = E_neg/max(E_pos,1e-30) < 1e-2
print(f"   -> advanced tail {'ABSENT (causal)' if causal_prop else 'PRESENT (ACAUSAL!)'} for propagator")

# --- RESPONSE D itself, minus its local part (w*1 = local d/dt piece) to expose the NONLOCAL tail ---
# D = w + w*(K-1). The w term is a local (contact) operator; the NONLOCAL memory is w*(K-1).
def nonlocal_response(w, eta):
    wc = w + 1j*eta
    return wc*(K_ret(w,eta) - 1.0)
t2, gNL = retarded_kernel(nonlocal_response, eta, Wmax, N)
neg2 = (t2 < 0) & (np.abs(t2) >= 5*dt)
pos2 = (t2 > 0) & (np.abs(t2) >= 5*dt)
E_neg2 = np.trapz(np.abs(gNL[neg2])**2, t2[neg2])
E_pos2 = np.trapz(np.abs(gNL[pos2])**2, t2[pos2])
print(f"   NONLOCAL memory w*(K-1):  energy(t<0)={E_neg2:.3e}   energy(t>0)={E_pos2:.3e}   ratio={E_neg2/max(E_pos2,1e-300):.3e}")
causal_resp = E_neg2/max(E_pos2,1e-30) < 1e-2
print(f"   -> advanced tail {'ABSENT (causal)' if causal_resp else 'PRESENT (ACAUSAL!)'} for nonlocal memory")

# ---------------------------------------------------------------------------------------------------
# STEP 3: SECULAR GROWTH -- late-time envelope of the retarded memory kernel w*(K-1) and 1/D.
#   Fit |g(t)| ~ t^p on t>0 for large t. p<0 = decays (bounded); p>=0 = secular/non-decaying.
# ---------------------------------------------------------------------------------------------------
print("\n[3] SECULAR GROWTH: late-time power law of the retarded kernels (t>0)")
def late_power(t, g, tlo, thi):
    m = (t>tlo)&(t<thi)&np.isfinite(np.abs(g))
    tt = t[m]; gg = np.abs(g[m])
    gg = np.maximum(gg, 1e-300)
    # robust: bin-average |g| in log-t to suppress oscillation, then fit slope
    lt = np.log(tt); lg = np.log(gg)
    # coarse binning
    nb = 40
    edges = np.linspace(lt.min(), lt.max(), nb+1)
    bx=[]; by=[]
    for i in range(nb):
        sel=(lt>=edges[i])&(lt<edges[i+1])
        if sel.sum()>3:
            bx.append(lt[sel].mean()); by.append(np.log(np.mean(np.exp(lg[sel]))))
    bx=np.array(bx); by=np.array(by)
    if len(bx)<5: return np.nan
    p=np.polyfit(bx,by,1)[0]
    return p

tmax = t.max()
p_prop = late_power(t, gP, 0.05*tmax, 0.9*tmax)
p_nl   = late_power(t2, gNL, 0.05*tmax, 0.9*tmax)
print(f"   propagator 1/D late-time envelope |g|~t^p :  p = {p_prop:+.3f}   ({'DECAYS' if p_prop< -0.05 else 'NON-DECAYING/SECULAR' if p_prop>-0.05 else '?'})")
print(f"   nonlocal memory w*(K-1) envelope |g|~t^p  :  p = {p_nl:+.3f}   ({'DECAYS' if p_nl< -0.05 else 'NON-DECAYING/SECULAR' if p_nl>-0.05 else '?'})")

# ---------------------------------------------------------------------------------------------------
# STEP 4: CONTROL -- a KNOWN acausal symbol to prove the pipeline can DETECT acausality.
#   Advanced propagator uses w -> w - i eta (LHP-analytic) -> support must flip to t<0.
# ---------------------------------------------------------------------------------------------------
print("\n[4] CONTROL: advanced prescription w->w-i eta must produce a t<0 (advanced) kernel -> pipeline works")
def prop_adv(w, eta):
    wc = w - 1j*eta
    z = -(wc**2)
    inner=np.sqrt(1.0+4.0*z)
    K=(inner-1.0)/(2.0*np.sqrt(z))
    return 1.0/(wc*K)
tA,gA = retarded_kernel(prop_adv, eta, Wmax, N)
negA=(tA<0)&(np.abs(tA)>=5*dt); posA=(tA>0)&(np.abs(tA)>=5*dt)
EnA=np.trapz(np.abs(gA[negA])**2,tA[negA]); EpA=np.trapz(np.abs(gA[posA])**2,tA[posA])
print(f"   ADVANCED 1/D:  energy(t<0)={EnA:.3e}  energy(t>0)={EpA:.3e}  ratio neg/pos={EnA/max(EpA,1e-300):.3e}")
control_ok = EnA/max(EpA,1e-30) > 10   # advanced kernel lives in t<0: neg >> pos
print(f"   -> advanced kernel correctly lives at t<0: {'YES (pipeline discriminates causal vs acausal)' if control_ok else 'NO -- pipeline blind!'}")

# ---------------------------------------------------------------------------------------------------
# STEP 5: BOTH FOOTINGS -- redo the support test with a0=9.36e-11 and 1.13e-10 (rescale w by a0).
# ---------------------------------------------------------------------------------------------------
print("\n[5] Both a0 footings: support of retarded 1/D (rescale w-grid by a0)")
for label,a0 in [("canonical 9.36e-11",9.36e-11),("alt 1.13e-10",1.13e-10)]:
    def prop_a0(w,eta,a0=a0):
        wc=w+1j*eta
        z=-(wc**2)/a0**2
        inner=np.sqrt(1.0+4.0*z)
        K=(inner-1.0)/(2.0*np.sqrt(z))
        return 1.0/(wc*K)
    Wm=2000.0*a0; et=1e-3*a0
    tf,gf=retarded_kernel(prop_a0,et,Wm,N)
    dtf=tf[1]-tf[0]; cf=np.abs(tf)<5*dtf
    En=np.trapz(np.abs(gf[(tf<0)&~cf])**2, tf[(tf<0)&~cf])
    Ep=np.trapz(np.abs(gf[(tf>0)&~cf])**2, tf[(tf>0)&~cf])
    print(f"   {label}: neg/pos energy ratio = {En/max(Ep,1e-300):.3e}  -> {'causal' if En/max(Ep,1e-30)<1e-2 else 'ACAUSAL'}")

# ---------------------------------------------------------------------------------------------------
print("\n"+"="*100)
print(" REFUTATION SUMMARY")
print("="*100)
print(f"   causal (propagator support t>=0):     {causal_prop}")
print(f"   causal (nonlocal memory support t>=0): {causal_resp}")
print(f"   no secular growth (prop p<0):          {p_prop < -0.02}")
print(f"   no secular growth (memory p<0):        {p_nl < -0.02}")
print(f"   control detects acausality:            {control_ok}")
allgood = causal_prop and causal_resp and (p_prop< -0.02) and (p_nl< -0.02) and control_ok
if allgood:
    print("\n   -> The retarded kernel WAS constructible in time, support IS t>=0 (no advanced tail),")
    print("      and late-time envelope DECAYS (no secular runaway). CAUSAL leg SURVIVES refutation.")
else:
    print("\n   -> A time-domain check FAILED: either an advanced tail or a secular tail is present.")
    print("      The compute's symbol-only Titchmarsh assertion would be INCOMPLETE / REFUTED.")
import sys; sys.exit(0)
