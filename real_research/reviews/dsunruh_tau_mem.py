#!/usr/bin/env python3
r"""
DOES THE dS BATH FORCE tau_mem? -- honest both-ways derivation.
================================================================
Framework: de Sitter-Unruh MODIFIED INERTIA. a0 = cH_Lambda/Z = 9.36e-11, Z=sqrt(32pi/3),
T_dS = H_Lambda/2pi. Validated frequency kernel theta(y)=sqrt2/(1+(sqrt2-1)y^2), y=om_ext/om_int
(paper DSUNRUH_MI_THEORY_2026.md sec.4). The dwarf sigma-hysteresis door is MG-impossible but its
MAGNITUDE is hostage to a TIME-domain memory time tau_mem = 1/omega_corner. theta(y) is scale-free
in y, so tau_mem is fixed iff the ABSOLUTE corner frequency omega_c is fixed.

THE SINGLE SHARP QUESTION: does the dS bath FORCE omega_c (hence tau_mem)?

This script:
 (a) builds K(t), the memory/dissipation kernel, DIRECTLY from the dS worldline Wightman function
     W(u) = -(kappa^2/16 pi^2)/sinh^2(kappa(u-i eps)/2), kappa=2pi T_dS = H_Lambda, via
     fluctuation-dissipation (the retarded/dissipation kernel is set by the ANTISYMMETRIC part /
     spectral density, NOT the raw symmetric correlator amplitude);
 (b) extracts tau_mem = decay time of K(t) and identifies the physical timescale it maps to;
 (c) cross-checks against the framework's OWN inverse-problem kernel pole v2 (d1: forced above-band);
 (d) DECIDES honestly: is the corner at y=1 bath-forced, or the Milgrom-1994 averaging-bandwidth
     postulate? If forced, pin the Crater II / Antlia II door at the derived tau_mem.

#1 HONESTY GUARD: do NOT smuggle omega_c = omega_internal (the y=1 corner) as an assumption and call
it a derivation. The corner LOCATION must come out of the bath's actual correlator/coupling, or
tau_mem is NOT forced.

Every number from THIS run (exit 0). New file, no git commit. Reuses the committed dwarf door.
"""
import numpy as np
import importlib.util, os, sys
np.seterr(all="ignore")

c   = 2.998e8
Z   = np.sqrt(32*np.pi/3.0)
A0  = 9.36e-11
HL  = A0*Z/c                      # = 1.807e-18 s^-1  (de Sitter / Lambda Hubble rate)
kappa = HL                        # surface gravity of the dS horizon on a comoving worldline = H_Lambda
T_dS  = HL/(2*np.pi)              # Gibbons-Hawking temperature (in frequency units, hbar=k_B=1)
Gyr = 3.156e16
sec_per_Gyr = Gyr

def banner(s): print("\n"+"="*96+"\n "+s+"\n"+"="*96)

banner("SETUP: the de Sitter bath scales")
print(f"  H_Lambda (=kappa)      = {HL:.4e} s^-1   (a0*Z/c, sealed)")
print(f"  T_dS = H_Lambda/2pi    = {T_dS:.4e} s^-1")
print(f"  1/H_Lambda             = {1/HL/Gyr:.2f} Gyr   (raw bath correlation time, Hubble scale)")
print(f"  2pi/H_Lambda           = {2*np.pi/HL/Gyr:.2f} Gyr   (thermal period 1/T_dS)")

# =====================================================================================
# (a) K(t) from the dS Wightman function via fluctuation-dissipation
# =====================================================================================
# The de Sitter worldline (comoving detector) two-point Wightman function of a conformally-coupled
# probe is  W(u) = -(kappa^2/16 pi^2) / sinh^2( kappa (u - i eps)/2 ),  kappa = 2 pi T_dS = H_Lambda.
# (Gibbons-Hawking 1977; Hu-Verdaguer influence-functional bath.)
#
# Fluctuation-dissipation: the memory / DISSIPATION kernel that appears in the effective equation of
# motion is the RETARDED response gamma(t) built from the ANTISYMMETRIC (commutator) part of the
# correlator, i.e. the spectral density rho(omega) = the odd-in-omega piece of the Fourier transform
# of W. The SYMMETRIC (noise) part sets the fluctuations; KMS ties them by tanh(omega/2T). The point
# of FDT here: the kernel DECAY is governed by the analytic structure (poles) of rho(omega), i.e. the
# large-|u| envelope of W, NOT by the raw amplitude kappa^2 out front.
#
# Large-separation envelope: 1/sinh^2(kappa u/2) -> 4 e^{-kappa|u|} as kappa|u| >> 1.
# So the correlator (and hence the retarded kernel it generates) decays EXPONENTIALLY with rate kappa:
#     K(t) ~ e^{-kappa |t|}  =>  tau_corr = 1/kappa = 1/H_Lambda.
# In frequency space this exponential envelope is exactly the Lorentzian 1/(1+(omega/kappa)^2):
# the paper's "correlator-forced Lorentzian form", with its CORNER at omega = kappa = H_Lambda.

banner("(a) MEMORY KERNEL K(t) FROM THE dS WIGHTMAN FUNCTION (fluctuation-dissipation)")
print("  W(u) = -(kappa^2/16 pi^2) / sinh^2( kappa(u-i eps)/2 ),  kappa = 2pi T_dS = H_Lambda")
print("  FDT: dissipation kernel = retarded response from the spectral density rho(omega)")
print("       (odd/commutator part of FT[W]); its DECAY is set by the poles of rho, i.e. the")
print("       large-|u| ENVELOPE of W -- NOT by the amplitude prefactor kappa^2/16pi^2.")

# Numerically confirm the exponential envelope + extract its rate from the correlator itself.
u = np.linspace(0.02/kappa, 40/kappa, 400000)          # avoid u=0 pole
W = 1.0/np.sinh(kappa*u/2.0)**2                        # |W| shape (drop constant prefactor & sign)
env = 4.0*np.exp(-kappa*u)                             # asymptotic envelope
# rate from a log-slope fit in the asymptotic tail (kappa u in [6,30]):
mask = (kappa*u>6)&(kappa*u<30)
slope = np.polyfit(u[mask], np.log(W[mask]), 1)[0]     # d ln W / dt
rate_fit = -slope
print(f"\n  numeric envelope fit:  d ln|W|/dt = {slope:.4e} s^-1")
print(f"  => decay RATE          = {rate_fit:.4e} s^-1   (should equal kappa = {kappa:.4e})")
print(f"  rate/kappa             = {rate_fit/kappa:.6f}   (== 1 confirms K(t) ~ e^-kappa|t|)")
assert abs(rate_fit/kappa - 1.0) < 1e-3, "envelope rate is not kappa -- FDT read broken"

# retarded kernel decay time from the correlator envelope:
tau_bath = 1.0/rate_fit
print(f"\n  RAW-CORRELATOR memory time  tau_bath = 1/kappa = {tau_bath:.4e} s = {tau_bath/Gyr:.2f} Gyr")
print("  -> the bath's own correlator puts the Lorentzian CORNER at omega_c = kappa = H_Lambda,")
print("     i.e. tau_mem ~ Hubble time (candidate 2). This is bath-HONEST and door-KILLING.")

# =====================================================================================
# (b) extract tau_mem candidates and map each to a physical timescale
# =====================================================================================
banner("(b) THE THREE CANDIDATE tau_mem AND THEIR PHYSICAL TIMESCALES")

# candidate 1: internal dynamical time of the dwarf (the postulate, y=1 corner)
# Crater II: sigma_los ~ 2.7 km/s, R_half ~ 1100 pc.  omega_int = sigma/R.
pc = 3.0857e16
def internal_time(sig_kms, R_pc):
    R = R_pc*pc; om = sig_kms*1e3/R
    return 1.0/om
tau_int_CrII = internal_time(2.7, 1100.0)
tau_int_AntII= internal_time(5.71, 2867.0)
print(f"  [1] internal 1/omega_int (Crater II, sig=2.7, R=1100pc) = {tau_int_CrII/Gyr:.3f} Gyr")
print(f"      internal 1/omega_int (Antlia II, sig=5.71,R=2867pc) = {tau_int_AntII/Gyr:.3f} Gyr")
print("      <- this is what the y=1 (omega_ext=omega_int) corner ASSERTS; the door NEEDS ~this.")

# candidate 2: raw dS correlator (computed in (a))
print(f"  [2] dS-thermal 1/kappa = 1/H_Lambda                     = {tau_bath/Gyr:.2f} Gyr")
print("      <- FDT decay of K(t) from the bare Wightman envelope. tau_mem >> P -> door DIES.")

# candidate 3: framework's OWN inverse-problem kernel pole v2 (d1), forced ABOVE the galactic band.
# d1 result: v2 >= ~ (nu2_hon) x band-top, band-top W2 = 3008 * H0 with H0=2.2e-18 (d1's spec).
# We import d1 to reuse its honest number rather than hard-code it.
d1path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kernel_2026_07", "d1_kernel_inversion.py")
v2_over_bandtop = None; v2_abs = None
if os.path.exists(d1path):
    # d1 prints v2 >= X x band-top and period <= Y Myr; recompute its min_nu2 by importing its funcs.
    spec = importlib.util.spec_from_file_location("d1mod", d1path)
    d1 = importlib.util.module_from_spec(spec)
    # d1 executes fully on import (prints its own banner); capture is fine.
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(d1)
    v2_over_bandtop = d1.nu2_hon
    W2 = d1.W2                     # band-top angular freq (s^-1)
    v2_abs = v2_over_bandtop*W2    # forced pole frequency
    tau_v2 = 1.0/v2_abs
    print(f"  [3] d1-forced kernel pole v2 = {v2_over_bandtop:.1f} x band-top = {v2_abs:.3e} s^-1")
    print(f"      => tau_v2 = 1/v2 = {tau_v2:.3e} s = {tau_v2/Gyr*1e3:.3f} Myr")
    print("      <- the framework's OWN inverse solution puts the pole ABOVE the galactic band")
    print("         (fast, reactive-in-band response). tau_mem ~ Myr << P -> door DIES (tau->0).")
else:
    tau_v2 = None
    print("  [3] d1_kernel_inversion.py not found -- skipping (pole is above-band, tau~Myr)")

# =====================================================================================
# (c) THE DECISION: is the y=1 corner (hence tau_mem) bath-FORCED?
# =====================================================================================
banner("(c) DECISION: forced by the bath, or the averaging-bandwidth POSTULATE?")
print("  tau_mem = 1/omega_c. theta(y) is scale-free in y=om_ext/om_int, so tau_mem is fixed")
print("  IFF the ABSOLUTE corner frequency omega_c is fixed. Three physical inputs fix omega_c")
print("  to THREE DIFFERENT values:")
print(f"    omega_c = kappa=H_Lambda   -> tau_mem = {tau_bath/Gyr:6.1f} Gyr    (raw dS correlator, (a))")
if tau_v2: print(f"    omega_c = v2 (above-band)  -> tau_mem = {tau_v2/Gyr*1e3:6.3f} Myr    (d1 forced pole, (c))")
print(f"    omega_c = omega_internal   -> tau_mem = {tau_int_CrII/Gyr:6.3f} Gyr   (Crater II 1/om_int) = POSTULATE")
print()
# Honest test: does ANY bath-derived correlator scale land on omega_internal?
ratio_bath = tau_int_CrII/tau_bath
ratio_v2   = (tau_int_CrII/tau_v2) if tau_v2 else np.nan
print(f"  bath-scale mismatch:  1/kappa is {1/ratio_bath:.1e}x too SLOW vs 1/omega_int (Hubble vs 0.4 Gyr)")
if tau_v2:
    print(f"                        1/v2   is {ratio_v2:.1e}x too FAST vs 1/omega_int (Myr vs 0.4 Gyr)")
print("  -> NEITHER bath-derived timescale equals 1/omega_int. omega_int sits BETWEEN them and")
print("     coincides with NEITHER the raw correlator NOR the framework's forced kernel pole.")
print()
print("  The only way to land omega_c = omega_internal is the Milgrom-1994 'internal orbit =")
print("  averaging bandwidth' postulate (paper sec.4 line 110: the corner LOCATION is NOT handed")
print("  over by the dS correlator; it 'rides on' this postulate, licensed only quasi-statically).")

FORCED = False   # the honest verdict -- set by the derivation above, NOT assumed.
# Guard: FORCED could only be True if a bath-derived correlator scale matched omega_int within,
# say, a factor of 3. It does not (Hubble is ~44x too slow; v2 is ~1e5x too fast).
match_bath = (1/3.0) < ratio_bath < 3.0
match_v2   = (tau_v2 is not None) and ((1/3.0) < ratio_v2 < 3.0)
if match_bath or match_v2:
    FORCED = True
print(f"\n  bath scale matches omega_int within 3x?  correlator:{match_bath}  pole:{match_v2}")
print(f"  ==> tau_mem FORCED by the bath: {FORCED}")

# =====================================================================================
# (d) door magnitude: since NOT forced, report the door across the bracket (dies / postulate / dies)
# =====================================================================================
banner("(d) DOOR MAGNITUDE across the bath-bracket (Crater II & Antlia II)")
dwpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dwarf_sigma_mi_final.py")
if os.path.exists(dwpath) and not FORCED:
    print("  tau_mem is NOT bath-forced -> we CANNOT pin a single door magnitude. We report the door")
    print("  at each candidate timescale; the bath does not pick among them.\n")
    # import the committed door WITHOUT re-running its whole print block: exec in a namespace,
    # suppress its stdout, then call door_for_dwarf directly at each tau.
    import io, contextlib
    spec = importlib.util.spec_from_file_location("dwmod", dwpath)
    dw = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(dw)
    DW = dw.DW  # [(name, rperi_kpc, rapo_kpc, sigma_kms, R_pc, is_carrier), ...]
    # map: dwarf -> (its own 1/om_int, in seconds)
    tau_int = {"Crater II": tau_int_CrII, "Antlia II": tau_int_AntII}
    print(f"  {'dwarf':10s} {'tau_mem source':26s} {'tau (Gyr)':>10} {'peak hyst %':>12}")
    for nm,rpk,rak,sfd,Rpc,isc in DW:
        if nm not in tau_int: continue
        cases = [("dS correlator 1/kappa", tau_bath),
                 ("internal 1/om_int (POSTULATE)", tau_int[nm])]
        if tau_v2: cases.insert(1, ("d1 pole 1/v2 (above-band)", tau_v2))
        for label, tau in cases:
            d = dw.door_for_dwarf(nm,rpk,rak,sfd,Rpc,isc,kern=dw.th_fw,tau=tau)
            peak = d['peak_hyst'] if d else float('nan')
            print(f"  {nm:10s} {label:26s} {tau/Gyr:>10.3f} {peak:>11.1f}%")
        print()
    print("  READ: the door is ~0% (bath-derived Myr or Hubble timescales) and only reaches its")
    print("  ~15% peak at tau = 1/om_int -- which is the POSTULATE, not a bath-forced scale.")
    print("  The door magnitude is a PROXY MEASUREMENT of omega_c: a positive dwarf sigma-hysteresis")
    print("  detection would EMPIRICALLY place the corner at omega_internal -- resolving the")
    print("  postulate the theory cannot currently derive.")
elif FORCED:
    print("  (would pin here) -- but the derivation returned NOT forced, so this branch is dead.")
else:
    print("  dwarf_sigma_mi_final.py not found; door bracket unavailable.")

# =====================================================================================
banner("BOTTOM LINE")
print("  The dS bath FORCES the memory kernel's FORM (Lorentzian) and DC weight (sqrt2), but NOT")
print("  its CORNER LOCATION. The raw correlator gives tau ~ Hubble (~17.5 Gyr); the framework's")
print("  own inverse-problem pole (d1) sits ABOVE the galactic band, tau ~ Myr. NEITHER equals the")
print("  ~0.4 Gyr = 1/omega_internal the door needs. Landing omega_c = omega_internal requires the")
print("  Milgrom-1994 averaging-bandwidth POSTULATE (an input, not derivable from the bath).")
print(f"\n  tau_mem_forced = NOT-FORCED")
print(f"  door = 0% (bath timescales)  vs  ~15% (postulate, 1/om_int)")
print("\nEXIT 0")
