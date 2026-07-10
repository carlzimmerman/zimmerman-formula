import numpy as np
ceil=5.2e-27
def w(beta,kt): return 1.0/(1.0+4.0*beta/kt)
def bcrit(Q2,kt): return kt*(Q2/ceil-1.0)/4.0

Q2={'canon':(2.0e-26,2.25e-26,2.5e-26),'alt':(2.7e-26,3.0e-26,3.3e-26)}
print("=== beta_crit(kappa_t) ===")
for foot,(lo,mid,hi) in Q2.items():
    for kt in (0.5,1.0):
        print(f"{foot} kt={kt}: bcrit central={bcrit(mid,kt):.3f}  band[{bcrit(lo,kt):.3f},{bcrit(hi,kt):.3f}]")

print("\n=== natural beta=2/7=0.286 verdict (Q2_med / ceiling) ===")
b=2/7
for foot,(lo,mid,hi) in Q2.items():
    for kt in (0.5,1.0):
        qm=w(b,kt)*mid
        print(f"{foot} kt={kt}: Q2_med={qm:.2e}  ratio={qm/ceil:.2f}x {'PASS' if qm<=ceil else 'FAIL'}")

print("\n=== most-favorable admissible corner (natural-high beta=0.333, kt=0.5, canon Q2_low) ===")
qm=w(0.333,0.5)*2.0e-26
print(f"Q2_med={qm:.2e} ratio={qm/ceil:.2f}x")
print("\n=== least-favorable (natural-low beta=0.182, kt=1.0, alt Q2_hi) ===")
qm=w(0.182,1.0)*3.3e-26
print(f"Q2_med={qm:.2e} ratio={qm/ceil:.2f}x")

print("\n=== beta needed to PASS (=beta_crit) vs natural window [0.18,0.33] ===")
for foot,(lo,mid,hi) in Q2.items():
    for kt in (0.5,1.0):
        print(f"{foot} kt={kt}: need beta>={bcrit(mid,kt):.3f}; saturated beta=2 gives Q2_med={w(2,kt)*mid:.2e} ({'PASS' if w(2,kt)*mid<=ceil else 'FAIL'})")
