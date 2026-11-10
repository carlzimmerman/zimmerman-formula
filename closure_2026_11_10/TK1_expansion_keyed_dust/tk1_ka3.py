"""TK1 KA3 numeric part: with M_2 constant at KD1's mu_B1a the code's w(z 3400) must be 0.01 (MK1/KD1's B1a line).
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk1_lib as L
import tk1_a3 as A3
out = {}
for foot in ("canonical", "alt"):
    mu = L.FOOT[foot]["mu_B1a"]
    r = A3.a2(foot, dict(mu0=mu, th0=0.1, p=0, Mf=0.0), {})
    w = r["rows"]["3400"]["w"]
    # closed form w0/(w0 + a^3), w0 = I0/(4 mu^2)
    a = 1 / 3401.0
    w0 = L.FOOT[foot]["I0"] / (4 * mu**2)
    out[foot] = dict(mu_B1a=mu, w_code=w, w_closed=w0 / (w0 + a**3), rel=w / 0.01 - 1, pass_=abs(w / 0.01 - 1) < 1e-4)
    print("[%s] KA3: mu_B1a %.6f -> w(3400) code %.8f, closed form %.8f, rel to 0.01 %.1e" % (foot, mu, w, w0 / (w0 + a**3), w / 0.01 - 1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tk1_ka3.json"), "w"), indent=1)
