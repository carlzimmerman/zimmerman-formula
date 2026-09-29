#!/usr/bin/env python3
"""M4 -- red-team of lane C: (i) the C2c 'toy QED emergence' versus the proper SM chain; (ii) self-consistent species cutoff and required extra charged content.
Run:    python3 m4_lane_c_content_and_cutoff.py
MUTATE: python3 m4_lane_c_content_and_cutoff.py MUTATE  (self-consistent identity Lambda^2 (N_SM+4 n_x) = M_red^2 is replaced by the fixed-N cutoff; identity check must fail -> exit 1)
Declared: extra states = n_x unit-hypercharge Dirac fermions at m_x = 1 TeV (one value, not scanned); hypercharge emergence 1/alpha_Y(Lambda) = 0;
inputs as lane B: 1/alpha_em(MZ) = 127.930, sin^2 = 0.23122, MZ = 91.1876, M_red = 2.435e18 GeV, N_SM = 118 (lane C's count).
"""
import sys
import mpmath as mp
from scipy.optimize import brentq
mp.mp.dps = 25
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok: fails.append(n)
Mred = mp.mpf('2.435e18'); MZ = mp.mpf('91.1876'); mx = mp.mpf(1000)
aem, s2 = mp.mpf('127.930'), mp.mpf('0.23122')
aY0, a20 = aem*(1-s2), aem*s2
bY, b2 = mp.mpf(41)/6, -mp.mpf(19)/6
Nsm = 118
def Lam(nx): return Mred/mp.sqrt(Nsm + 4*nx)
# (i) proper SM chain at Lambda(0)
L0 = Lam(0)
aY_L = aY0 - bY/(2*mp.pi)*mp.log(L0/MZ); a2_L = a20 - b2/(2*mp.pi)*mp.log(L0/MZ)
print("(i) Lambda = M_red/sqrt(118) = %.3e GeV: 1/alpha_Y = %.2f, 1/alpha_2 = %.2f, 1/alpha_em = %.2f (emergence would need 0 for the emergent factor)" % (L0, aY_L, a2_L, aY_L+a2_L))
toy = mp.mpf('70.4444')  # lane C c2 output N=118
print("    lane C toy (fermion loops only, no W/Higgs, anchored at 0 not at MZ) gives 1/alpha(0) = %.2f; proper SM leaves %.1f above zero at the cutoff" % (toy, aY_L+a2_L))
chk("proper SM chain leaves 1/alpha_em(Lambda) > 50 (emergence is further away than the toy suggests)", aY_L + a2_L > 50)
chk("hypercharge: 1/alpha_Y(Lambda) > 30 with SM content", aY_L > 30)
# (ii) required extra content
def resid(nx, selfc=True):
    Lm = Lam(nx) if selfc else L0
    inv_at_L = aY0 - bY/(2*mp.pi)*mp.log(Lm/MZ) - (mp.mpf(4)/3*nx)/(2*mp.pi)*mp.log(Lm/mx)
    return float(inv_at_L)
nx_fixed = brentq(lambda n: resid(n, False), 0, 100)
nx_self = brentq(lambda n: resid(n, True), 0, 100)
print("(ii) extra unit-Y Dirac fermions at 1 TeV needed for 1/alpha_Y(Lambda)=0:  fixed Lambda: n_x = %.3f ; self-consistent Lambda: n_x = %.3f  (shift %.2f %%)" % (nx_fixed, nx_self, 100*(nx_self/nx_fixed-1)))
sumY2_sm = 10 + mp.mpf(1)/4   # Weyl sum 10 + Higgs (1/3*2*1/4 -> in units of 3/2 of Weyl) ; used only as a scale for comparison
dW = 2*nx_self       # Weyl sum of extra content = 2 per unit-Y Dirac
print("     extra content = %.2f (sum Y^2 over Weyl units) vs SM fermions 10.0 : ratio %.2f ; species count N: %d -> %.1f ; Lambda %.3e -> %.3e" % (dW, dW/10, Nsm, Nsm+4*nx_self, L0, Lam(nx_self)))
chk("required extra content is not a small integer count of unit-charge Dirac fermions (n_x non-integer)", abs(nx_self - round(nx_self)) > 0.05, "n_x = %.3f" % nx_self)
chk("self-consistent cutoff shifts the requirement by < 10 % (fixed-N assumption of lane C is harmless)", abs(nx_self/nx_fixed - 1) < 0.10)
ident = abs(Lam(nx_self)**2*(Nsm+4*nx_self) - Mred**2)/Mred**2
if MUT:
    ident = abs(L0**2*(Nsm+4*nx_self) - Mred**2)/Mred**2
chk("identity Lambda^2 (N_SM + 4 n_x) = M_red^2 holds at the self-consistent solution", ident < 1e-20, "rel diff %.2e" % ident)
# scan of required content vs the (walled) extra-mass position, REPORT ONLY: the requirement moves continuously with m_x
for mxx in (200, 1e3, 1e5, 1e10):
    def r2(n, mxx=mxx):
        Lm = Lam(n); return float(aY0 - bY/(2*mp.pi)*mp.log(Lm/MZ) - (mp.mpf(4)/3*n)/(2*mp.pi)*mp.log(Lm/mp.mpf(mxx)))
    print("     REPORT (not scored): m_x = %.0e GeV -> n_x = %.2f" % (mxx, brentq(r2, 0, 1e4)))
print("READING: emergence supplies a genuine boundary condition, but the content and its masses are undetermined inputs; the requirement moves continuously with m_x. Lane C's verdict stands.")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
