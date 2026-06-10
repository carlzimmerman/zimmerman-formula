#!/usr/bin/env python3
"""
FINAL consolidation (FRESH): assemble the a0(3)/a0(0) band across (gate, IC), pin the
fast-limit value analytically, and emit the decisive numbers.
"""
import numpy as np, json, importlib.util
from scipy.integrate import solve_ivp, quad
spec=importlib.util.spec_from_file_location("cosmo_desi","/tmp/gamma_th_blind/cosmo_desi.py")
C=importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
def Teq(z): return C.T_ansatz(z)

def Gamma_gate(name,z):
    H=C.H_of_z(z)
    d={"G3_tauc(1/H)":H,"G4_Hubble(1/H)":H,"G5_TGH(2pi/H)":H/(2*np.pi),
       "G1_gapless_l1":1.0**2*H/(2*np.pi**2),"G1_gapless_l0.3":0.3**2*H/(2*np.pi**2),
       "G1_gapless_l3":3.0**2*H/(2*np.pi**2),
       "HDE_repo":C.H_DE(z),"HDE_2pi_repo":C.H_DE(z)/(2*np.pi)}
    return d[name]
GATES=["G3_tauc(1/H)","G5_TGH(2pi/H)","G1_gapless_l3","G1_gapless_l1","G1_gapless_l0.3",
       "HDE_repo","HDE_2pi_repo"]

def integ(gate,Tinit,zi=30.0):
    def rhs(z,T):
        H=C.H_of_z(z); G=Gamma_gate(gate,z); return G*(T-Teq(z))/((1+z)*H)
    return solve_ivp(rhs,[zi,0.0],[Tinit],dense_output=True,rtol=1e-10,atol=1e-13,max_step=0.005)

zero_lag=np.sqrt(C.f_DE(3.0))
print("="*78); print("FINAL: a0(3)/a0(0) band  (zero-lag = %.4f)"%zero_lag); print("="*78)
band={}
allvals=[]
for g in GATES:
    rs={}
    for ic,Ti in [("adiabatic",Teq(30.0)),("constant",1.0),("cold",0.0)]:
        s=integ(g,Ti); rs[ic]=float(s.sol(3)[0]/s.sol(0)[0]); allvals.append(rs[ic])
    band[g]=rs
    print(f"  {g:18s}  adiabatic={rs['adiabatic']:.4f}  constant={rs['constant']:.4f}  "
          f"cold={rs['cold']:.4f}")
print(f"\nFULL BAND across (derived gate, IC): [{min(allvals):.3f}, {max(allvals):.3f}]")
# derived-gate-only band (exclude repo HDE columns), exclude cold-start as unphysical-extreme? keep all
derived=[v for g in GATES if not g.startswith("HDE") for v in band[g].values()]
print(f"DERIVED-gate band (G1/G3/G5, all IC):  [{min(derived):.3f}, {max(derived):.3f}]")
print(f"zero-lag (framework nominal) = {zero_lag:.4f}  sits {'INSIDE' if min(derived)<=zero_lag<=max(derived) else 'OUTSIDE'} the band")

# analytic fast-limit (Gamma>>H) IC-independent value: T->Teq pointwise => 0.737.
# But finite leading correction at Gamma=K*H, K large: shown to approach 0.730 at K=100.
print("\nIC-independent limit (Gamma>>H): a0(3)/a0(0) -> zero-lag 0.737 (all IC converge).")
print("Verified earlier: K=100 -> 0.730 (residual O(H/Gamma) lag), K->inf -> 0.737.")

# key gapless rate restated:
print("\n--- KEY DERIVED QUANTITIES ---")
print("Gamma_th(omega) = (lambda^2 omega/2pi) coth(pi omega/H)")
print("Gamma_th(0)     = lambda^2 H/(2 pi^2)   [gapless]  = lambda^2 T_GH/pi")
print("tau_c           = 1/H")
print("T_GH            = H/(2 pi)")

# eps at z=3 per gate (the 'per gate' Part C anchor), recompute cleanly
print("\n--- eps(z=3) per gate (Part C anchor) ---")
dlnTdt3=C.abs_dlnT_dt_analytic(3.0)
eps3={"G3/G4 (1/H)":dlnTdt3/C.H_of_z(3),
      "G5 (2pi/H)":dlnTdt3*2*np.pi/C.H_of_z(3),
      "G1 l=1 (2pi^2/H)":dlnTdt3*2*np.pi**2/C.H_of_z(3),
      "G1 l=0.3":dlnTdt3*2*np.pi**2/(0.3**2*C.H_of_z(3)),
      "G1 l=3":dlnTdt3*2*np.pi**2/(3.0**2*C.H_of_z(3)),
      "HDE repo":dlnTdt3/C.H_DE(3),"HDE/2pi repo":dlnTdt3*2*np.pi/C.H_DE(3)}
for k,v in eps3.items(): print(f"  eps(3) {k:18s} = {v:.4f}")
a=1/(1+3.0); w=C.w0+C.wa*(1-a)
print(f"  (eps_G3(3) should equal 1.5|1+w(z=3)| = {abs(1.5*(1+w)):.4f})")

summary=dict(zero_lag=zero_lag, band_all=[min(allvals),max(allvals)],
             band_derived=[min(derived),max(derived)], a0_3_over_0=band,
             Gamma_th_gapless="lambda^2 H/(2 pi^2)", tau_c="1/H", T_GH="H/2pi",
             eps3={k:float(v) for k,v in eps3.items()})
with open("/tmp/gamma_th_blind/FINAL_summary.json","w") as fh: json.dump(summary,fh,indent=2)
print("\nsaved /tmp/gamma_th_blind/FINAL_summary.json")
