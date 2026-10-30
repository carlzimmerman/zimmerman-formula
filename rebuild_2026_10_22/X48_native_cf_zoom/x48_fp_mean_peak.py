"""X48 first-principles diagnostic FP1 (reported, not graded): radial spherical collapse of the MEAN Hoffman-Ribak peak on the native
spectrum (continuum k). Each shell ends at ~1/2 its turnaround radius, so r_-2 sits at the Lagrangian q where d ln dbar(<q)/d ln q = -2
and c_f = (qM/q_-2) dbar(q_-2)/dbar(qM) (the 1/2 cancels; in EdS r(qM) = r_vir at 18 pi^2 exactly)."""
import sys, math, json, numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ["x"]
import x48_zoom as Z
from scipy.special import erf
from scipy.optimize import brentq
C = Z.cosmology()
K, PK = C["K"], C["PK"]
k = np.geomspace(1e-4, K[-1], 20000); P = np.exp(np.interp(np.log(k), np.log(K), np.log(PK)))
def tophat(x): return np.where(x < 1e-3, 1 - x**2/10, 3*(np.sin(x) - x*np.cos(x))/np.maximum(x,1e-30)**3)
def I(f): return float(np.trapz(f * k**2, k) / (2*math.pi**2))
def fB(x): return ((x**3-3*x)/2*(erf(math.sqrt(2.5)*x)+erf(math.sqrt(2.5)*x/2)) + math.sqrt(2/(5*math.pi))*((31*x**2/4+1.6)*np.exp(-5*x**2/8)+(x**2/2-1.6)*np.exp(-5*x**2/2)))
xs = np.linspace(1e-4, 30, 30001)
out = {}
for M in (1e12, 1e13, 1e14):
    zf, Df = Z.lacey_cole_zf(C, M); Mf = M/2; rho = C["rhom"]
    qM = (3*Mf/(4*math.pi*rho))**(1/3); RG = (Mf/((2*math.pi)**1.5*rho))**(1/3)
    W = np.exp(-(k*RG)**2/2)
    s0, s1, s2 = (math.sqrt(I(P*W**2*k**(2*j))) for j in (0,1,2)); gam = s1**2/(s0*s2)
    CCi = np.linalg.inv(np.array([[s0**2, -s1**2], [-s1**2, s2**2]]))
    def xmean(nu):
        w = fB(xs)*np.exp(-(xs-gam*nu)**2/(2*(1-gam**2))); return float(np.trapz(xs*w, xs)/np.trapz(w, xs))
    def dbar(q, nu):          # enclosed mean linear contrast of the HR mean field at z=0
        x = xmean(nu); w = CCi @ np.array([nu*s0, -x*s2]); th = tophat(k*q)
        return w[0]*I(P*W*th) + w[1]*I(-k**2*P*W*th)
    nu = brentq(lambda n: dbar(qM, n) - 1.686/Df, 0.05, 50, xtol=1e-10)
    q = qM*np.geomspace(0.02, 1.5, 400); d = np.array([dbar(x, nu) for x in q])
    s = np.gradient(np.log(d), np.log(q))
    i = np.where((s[:-1] > -2) & (s[1:] <= -2))[0]
    q2 = float(np.exp(np.interp(-2, [s[i[0]+1], s[i[0]]], [np.log(q[i[0]+1]), np.log(q[i[0]])]))) if len(i) else None
    cf = (qM/q2)*float(np.interp(np.log(q2), np.log(q), d))/(1.686/Df) if q2 else None
    out[f"{M:.0e}"] = dict(zf=zf, nu=nu, xbar=xmean(nu), gamma=gam, q2_over_qM=q2/qM if q2 else None, cf=cf,
                           slope_at=[(round(float(a),3), round(float(b),3)) for a, b in zip(q[::40]/qM, s[::40])])
    print(M, json.dumps(out[f"{M:.0e}"]))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "x48_fp_mean_peak.json"),"w"), indent=1)
