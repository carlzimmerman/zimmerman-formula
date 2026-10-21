"""WT-03 - the vacuum clock (criteria c9ea722b6, FROZEN_CRITERIA.md in this folder).

Which way and how fast does a0 = kappa c sqrt(G X) run in cosmic time under the three dark-energy readings on the record
(eps, -p, V), and what does that demand of dark energy? Input: CFG689's committed primary band (cfg689.json, result commit
6c064b83a; read only). Posterior samples are not stored, so node draws use the declared APPROX-G (Gaussian per node from the
stored posterior mean/std; adjacent-node correlation bracket rho_adj in {-0.5, 0, +0.5}, primary 0).
kappa = 1/2 is FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; nothing here says the data favour the framework.
Env WT03_MUTATE=1: X -> H^2(z) per draw (the rival a0 ~ H(z)); outputs carry the _MUTATE tag.
Run: OMP_NUM_THREADS=1 nice -n 10 /usr/bin/time -l python3 wt03.py
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CFG689 = os.path.join(ROOT, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689.json")
MUT = os.environ.get("WT03_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"wt03{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"criteria": "c9ea722b6", "mode": "MUTATE" if MUT else "main", "input": "cfg689.json @ 6c064b83a (BAO+SN, primary)"}
CHECKS = {}
def check(name, ok, detail):
    CHECKS[name] = dict(ok=bool(ok), detail=detail); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

# ---- constants (CFG689's own, fb8d4bba4 line 90/128) ----
G, CMS, RHO100, OMG = 6.67430e-11, 2.99792458e8, 1.87847e-26, 2.4728e-5
OMR = OMG*(1 + 0.2271*3.044)                       # m_nu = 0 in the primary mode
HBAR, MSUN, AU = 1.054571817e-34, 1.98847e30, 1.495978707e11
YR = 3.15576e7; GYR = 1e9*YR; MPC_KM = 3.0856775814913673e19
KMSMPC_TO_GYR = GYR/MPC_KM                          # 1 km/s/Mpc in 1/Gyr (= 1/977.792)
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
ZVAL = math.sqrt(32*math.pi/3)
T68, T95 = 0.8413, 0.9750
LEVELS = {"68": T68, "95": T95}
TOL = 1e-12
RHOS = (-0.5, 0.0, 0.5)
NDRAW, SEED = 400_000, 3031
READ = ("eps", "-p", "V")

P(f"WT-03 vacuum clock  mode={'MUTATE (X -> H^2, rival a0 ~ H)' if MUT else 'main'}  criteria c9ea722b6")
P("kappa = 1/2 FITTED; Z = sqrt(32 pi/3) = %.4f; footings %.4e / %.4e (never pooled)" % (ZVAL, FOOT["canonical"], FOOT["alt"]))

# =====================================================================================================================
# S. sympy theory (criteria section 5)
# =====================================================================================================================
P("\n=== S. Theory (sympy) ===")
t, z = sp.symbols("t z", real=True)
Hs, kap, c_, G_ = sp.symbols("H kappa c G", positive=True)
w_ = sp.symbols("w", real=True)
rho_t = sp.Function("rho")(t)
# S1: eps reading, fluid continuity
rdot = -3*Hs*(rho_t + w_*rho_t)
dlna0_dt = sp.diff(sp.log(kap*c_*sp.sqrt(G_*rho_t)), t).subs(sp.Derivative(rho_t, t), rdot)
S1 = sp.simplify(dlna0_dt + sp.Rational(3, 2)*Hs*(1 + w_))
P("S1 eps: d ln a0/dt =", sp.simplify(dlna0_dt), " ; minus [-(3/2)H(1+w)] simplifies to", S1)
K17 = sp.simplify(dlna0_dt/Hs + sp.Rational(3, 2)*(1 + w_))
P("    CFG911 K17 form d ln a0/d ln a = -(3/2)(1+w): residual", K17)
# z form: rho(z), p from continuity in z
rz = sp.Function("rho")(z)
r1, r2 = sp.diff(rz, z), sp.diff(rz, z, 2)
p_z = (1 + z)*r1/3 - rz
cont_chk = sp.simplify(-(1 + z)*Hs*r1 - (-3*Hs*(rz + p_z)))       # d rho/dt = -(1+z) H rho' must equal -3H(rho+p)
eps_z = sp.simplify(-(1 + z)*Hs*sp.diff(sp.log(sp.sqrt(rz)), z) - (-sp.Rational(3, 2)*Hs*(1 + p_z/rz)))
P("    z-form: p = (1+z) rho'/3 - rho satisfies continuity (residual %s); -1/2 (1+z) H rho'/rho = -(3/2)H(1+w) (residual %s)"
  % (cont_chk, eps_z))
# S2: -p reading
mp = sp.expand(-p_z)
dmp = sp.expand(sp.diff(mp, z))
S2a = sp.simplify(dmp - (sp.Rational(2, 3)*r1 - (1 + z)*r2/3))
P("S2 -p: -p =", mp, "; d(-p)/dz =", dmp, "; residual vs (2/3)rho' - (1+z)rho''/3:", S2a)
ca2, Hh = sp.symbols("c_a2 H_", real=True)
rho_s, p_s = sp.symbols("rho_s p_s", real=True)
pdot = ca2*(-3*Hs*(rho_s + p_s))
S2b = sp.simplify(pdot/p_s - 3*Hs*ca2*(1 + p_s/rho_s)/(-p_s/rho_s))
P("    fluid: d ln(-p)/dt = p_dot/p = 3H c_a^2 (1+w)/(-w): residual", S2b,
  "=> for -p > 0, rising <=> c_a^2 (1+w) > 0; with NEC (1+w>0) rising <=> c_a^2 > 0, falling <=> c_a^2 < 0")
rise_mp = sp.expand(-3*dmp)       # rising in time <=> d(-p)/dz < 0 <=> (1+z) rho'' - 2 rho' > 0
P("    rising -p in time <=> d(-p)/dz < 0 <=> (1+z) rho'' - 2 rho' > 0 :", rise_mp, "> 0")
phi = sp.Function("phi")(t); Vf = sp.Function("V")
phid = sp.diff(phi, t); phidd_kg = -3*Hs*phid - sp.diff(Vf(phi), phi)
Kin = phid**2/2
mp_scalar = Vf(phi) - Kin
dmp_s = sp.diff(mp_scalar, t).subs(sp.Derivative(phi, (t, 2)), phidd_kg)
S2c = sp.simplify(dmp_s - (2*sp.diff(Vf(phi), phi)*phid + 3*Hs*phid**2))
P("    canonical scalar: d(-p)/dt = 2 V' phi_dot + 3 H phi_dot^2: residual", S2c)
Vp = sp.symbols("Vp", real=True); pd = sp.symbols("pd", real=True)
slow = sp.simplify((2*Vp*pd + 3*Hs*pd**2).subs(Vp, -3*Hs*pd))
P("      slow-roll attractor (V' = -3H phi_dot):", slow, " (< 0: -p falls);  flat potential V' = 0:", 3*Hs*pd**2, "(> 0: -p rises, NEC holds)")
rho_dot_s = sp.simplify(sp.diff(Kin + Vf(phi), t).subs(sp.Derivative(phi, (t, 2)), phidd_kg))
P("      scalar rho_dot =", rho_dot_s, "(= -3H phi_dot^2 <= 0 always: a canonical scalar's density never grows)")
# S3: V reading
Vdot = sp.diff(Vf(phi), t)
ddphi2 = sp.simplify(sp.diff(phid**2, t).subs(sp.Derivative(phi, (t, 2)), phidd_kg))
P("S3 V: V_dot =", Vdot, "; d(phi_dot^2)/dt =", ddphi2,
  "=> V rises only while the field climbs (V' phi_dot > 0), and then phi_dot^2 must fall: transient, decelerating")
K_z = sp.simplify((rz + p_z)/2); V_z = sp.simplify((rz - p_z)/2)
S3a = sp.simplify(K_z - (1 + z)*r1/6); S3b = sp.simplify(V_z - (rz - (1 + z)*r1/6))
dV = sp.expand(sp.diff(V_z, z)); S3c = sp.simplify(dV - (sp.Rational(5, 6)*r1 - (1 + z)*r2/6))
P("    z-form: K = (1+z) rho'/6 (res %s), V = rho - (1+z) rho'/6 (res %s), V' = (5/6) rho' - (1+z) rho''/6 (res %s)" % (S3a, S3b, S3c))
P("    no ghost <=> K >= 0 <=> rho' >= 0 ; rising V in time <=> (1+z) rho'' - 5 rho' > 0")
# S4: piecewise-linear identity
a_, m_ = sp.symbols("a m", real=True)
lin = a_ + m_*z
S4 = [sp.simplify(sp.diff(e.subs(rz, lin).doit(), z)) for e in (rz, mp, V_z)]
P("S4 (TRUE BY CONSTRUCTION) inside a CFG689 segment rho = a + m z: d/dz of (eps, -p, V) =", S4, "-> all sign(m)")
# S5: IDENTITY
a0s, hb = sp.symbols("a0 hbar", positive=True)
S_H = sp.pi*c_**5/(G_*hb*Hs**2)
S5 = sp.simplify(S_H.subs(Hs, sp.sqrt(sp.Rational(32, 3)*sp.pi)*a0s/c_) - 3*c_**7/(32*G_*hb*a0s**2))
P("S5 IDENTITY (no verdict weight): S_dS/k_B = pi c^5/(G hbar H_L^2), H_L = Z a0/c, Z^2 = 32 pi/3 -> 3 c^7/(32 G hbar a0^2): residual", S5,
  "; d ln S/dt = -2 d ln a0/dt")
k4 = all(sp.simplify(x) == 0 for x in [S1, K17, cont_chk, eps_z, S2a, S2b, S2c, S3a, S3b, S3c, S5]) and slow == -3*Hs*pd**2 \
     and S4[0] == m_ and sp.simplify(S4[1] - 2*m_/3) == 0 and sp.simplify(S4[2] - 5*m_/6) == 0
check("K4 sympy S1-S5 + CFG911 K17", k4, "all residuals zero" if k4 else "a residual is non-zero")
RES["theory"] = {
    "S1_eps": "d ln a0/dt = -(3/2) H (1+w) = -1/2 (1+z) H rho'/rho. Rising <=> w < -1 (NEC violated). Falling <=> w > -1.",
    "S2_-p": "-p = rho - (1+z) rho'/3; d(-p)/dz = (2/3) rho' - (1+z) rho''/3; d ln(-p)/dt = 3H c_a^2 (1+w)/(-w). Rising with NEC <=> "
             "c_a^2 > 0 <=> rho'' > 2 rho'/(1+z) (convex). Canonical scalar: d(-p)/dt = 2V' phi_dot + 3H phi_dot^2: rises if the field "
             "is faster than its slow-roll speed (|V'| < 1.5 H |phi_dot|) or climbs; falls on the slow-roll attractor.",
    "S3_V": "V_dot = V' phi_dot: rises only while the field climbs; then phi_dot^2 falls (transient). rho_dot = -3H phi_dot^2 <= 0. "
            "K = (1+z) rho'/6 >= 0 <=> no ghost; V' = (5/6) rho' - (1+z) rho''/6; rising V with no ghost <=> rho' >= 0 and "
            "rho'' > 5 rho'/(1+z). rho' < 0 needs K < 0 (a ghost) for a canonical-form scalar.",
    "S4": "TRUE BY CONSTRUCTION: inside a CFG689 linear segment rho'' = 0, so all three readings drift with sign(-rho').",
    "S5": "IDENTITY: S_dS = 3 k_B c^7/(32 G hbar a0^2) at kappa = 1/2; d ln S/dt = -2 d ln a0/dt. No verdict weight.",
    "falling": "eps falls <=> w > -1; -p falls (NEC) <=> c_a^2 < 0 (e.g. slow-roll thawing); V falls <=> field rolls down (V' phi_dot < 0)."}

# =====================================================================================================================
# A. the band (criteria section 3; exact keys)
# =====================================================================================================================
P("\n=== A. CFG689 primary band (cfg689.json @ 6c064b83a, keys BAO+SN.*) ===")
D = json.load(open(CFG689)); B = D["BAO+SN"]
assert D["mode"] == "primary" and D["cfg"]["mnu"] == 0.0 and D["cfg"]["f"] == 0.0
NODES = np.array(D["cfg"]["nodes"], float); NN = len(NODES); ZS = ("1.0", "1.2", "1.5", "2.33")
QP = [2.5, 16, 50, 84, 97.5]
post = B["posterior"]; MU = np.array(post["node_mean"]); SD = np.array(post["node_std"])
OB, OC, OK_ = post["omega_b"], post["omega_c"], post["omega_k"]
P("cfg.nodes =", NODES.tolist(), "; percentiles Q =", QP)
for zk in ZS:
    P(f"  P1[{zk}].sqrtX_q = {np.round(B['P1'][zk]['sqrtX_q'], 4).tolist()}   E_q[2] = {B['P1'][zk]['E_q'][2]:.5f}   "
      f"P3.P_w_le0 = {B['P3']['P_w_le0'][zk]:.4f}")
for i, zk in enumerate(["0.0", "0.4", "0.7", "1.0", "1.5", "2.33"]):
    P(f"  P3.a0_node_q[{zk}] = {np.round(np.array(B['P3']['a0_node_q'][zk])/1e-11, 3).tolist()} e-11   "
      f"posterior node {zk}: mean {MU[i]:.4f} std {SD[i]:.4f}")
P(f"  posterior omega_b {OB}, omega_c {OC}, omega_k {OK_}; P3.H0_q = {np.round(B['P3']['H0_q'], 3).tolist()}")
P(f"  P2 (context): dchi2 {B['P2']['dchi2']:.3f}/{B['P2']['dof']}, {B['P2']['sigma_equiv']:.3f} sigma, {B['P2']['P2_class']}")
RES["band"] = {"keys": ["cfg.nodes", "BAO+SN.P1.<z>.sqrtX_q", "BAO+SN.P1.<z>.E_q", "BAO+SN.P3.a0_node_q.<z>", "BAO+SN.P3.H0_q",
                        "BAO+SN.P3.P_w_le0", "BAO+SN.posterior.node_mean/node_std/omega_b/omega_c/omega_k", "BAO+SN.P2 (context)"],
               "percentiles": QP, "sqrtX_q": {zk: B["P1"][zk]["sqrtX_q"] for zk in ZS},
               "a0_node_q": B["P3"]["a0_node_q"], "node_mean": MU.tolist(), "node_std": SD.tolist()}

# ---- mean background (criteria section 4) ----
OM = OB[0] + OC[0]; WK = OK_[0]
def E2raw(zz, wn):  # h^2 E^2 for node vector(s) wn, CFG689 bg() form
    return OM*(1 + zz)**3 + OMR*(1 + zz)**4 + WK*(1 + zz)**2 + np.interp(zz, NODES, wn)
H2BAR = E2raw(0.0, MU); HBAR0 = 100*math.sqrt(H2BAR); H0G = HBAR0*KMSMPC_TO_GYR
def Hgyr(zz): return 100*np.sqrt(E2raw(zz, MU))*KMSMPC_TO_GYR
def lookback(zz): return quad(lambda x: 1.0/((1 + x)*Hgyr(x)), 0, zz, limit=200, points=[n for n in NODES if 0 < n < zz])[0] if zz > 0 else 0.0
AGE = quad(lambda a: 1.0/(a*Hgyr(1/a - 1)), 1e-12, 1, limit=400, points=[1/(1 + n) for n in NODES[1:]])[0]
TLB = {float(n): lookback(n) for n in NODES}

P("\n=== K1 / K5. Reproduction and integrator ===")
a0_0 = 0.5*CMS*math.sqrt(G*RHO100*MU[0])
k1a = abs(HBAR0 - B["P3"]["H0_q"][2]) <= 0.05
k1b = abs(a0_0/B["P3"]["a0_node_q"]["0.0"][2] - 1) <= 0.005
ek = {zk: math.sqrt(E2raw(float(zk), MU)/H2BAR) for zk in ZS}
k1c = all(abs(ek[zk]/B["P1"][zk]["E_q"][2] - 1) <= 0.005 for zk in ZS)
check("K1(a) H0 from posterior means", k1a, f"{HBAR0:.4f} vs P3.H0_q[2] {B['P3']['H0_q'][2]:.4f} (tol 0.05)")
check("K1(b) a0(z=0) at kappa=1/2", k1b, f"{a0_0:.5e} vs P3.a0_node_q[0.0][2] {B['P3']['a0_node_q']['0.0'][2]:.5e} (tol 0.5%)")
check("K1(c) E(z) mean background", k1c, "; ".join(f"z {zk}: {ek[zk]:.5f} vs {B['P1'][zk]['E_q'][2]:.5f}" for zk in ZS))
om_t, H0t = 0.3, 70.0
num = quad(lambda a: 1.0/(a*H0t*KMSMPC_TO_GYR*math.sqrt(om_t/a**3 + 1 - om_t)), 0, 1, limit=200)[0]
ana = 2/(3*H0t*KMSMPC_TO_GYR*math.sqrt(1 - om_t))*math.asinh(math.sqrt((1 - om_t)/om_t))
check("K5 flat matter+Lambda age", abs(num/ana - 1) <= 1e-6, f"numeric {num:.8f} Gyr vs closed form {ana:.8f} Gyr")
P(f"  native mean background: H0 = {HBAR0:.3f} km/s/Mpc = {H0G:.5f} /Gyr; age {AGE:.3f} Gyr; lookback to nodes "
  + ", ".join(f"z {n:g}: {TLB[float(n)]:.3f}" for n in NODES) + " Gyr")
RES["background"] = dict(H0=HBAR0, H0_per_Gyr=H0G, age_Gyr=AGE, lookback_Gyr={str(k): v for k, v in TLB.items()},
                         omega_m=OM, omega_k=WK, omega_r=OMR, h2=H2BAR)

# =====================================================================================================================
# draws (APPROX-G) and the classifier
# =====================================================================================================================
def draw(rho_adj, n=NDRAW, mu=MU, sd=SD, seed=SEED):
    C = np.diag(sd**2)
    for i in range(NN - 1):
        C[i, i + 1] = C[i + 1, i] = rho_adj*sd[i]*sd[i + 1]
    L = np.linalg.cholesky(C)
    rng = np.random.default_rng(seed)
    return mu + rng.standard_normal((n, NN))@L.T

def mutate(W):   # X -> h^2 E^2(z_k) per draw (rival a0 ~ H)
    return np.stack([OM*(1 + zk)**3 + OMR*(1 + zk)**4 + WK*(1 + zk)**2 + W[:, i] for i, zk in enumerate(NODES)], axis=1)

def seg_F(W, R, recon, cs=None):
    """F_R at both ends of each segment: arrays (n, 5) Fa (z_k), Fb (z_{k+1})."""
    if recon == "literal":
        dz = np.diff(NODES); m = np.diff(W, axis=1)/dz
        fac = {"eps": 0.0, "-p": 1/3, "V": 1/6}[R]
        Fa = W[:, :-1] - (1 + NODES[:-1])*m*fac; Fb = W[:, 1:] - (1 + NODES[1:])*m*fac
        return Fa, Fb
    rho, d1 = cs
    fac = {"eps": 0.0, "-p": 1/3, "V": 1/6}[R]
    F = rho - (1 + NODES)[None, :]*d1*fac
    return F[:, :-1], F[:, 1:]

def spline_nodes(W):
    cs = CubicSpline(NODES, W.T, axis=0)    # not-a-knot (scipy default)
    return cs(NODES).T, cs(NODES, 1).T, cs(NODES, 2).T

def q5(x):
    x = x[np.isfinite(x)]
    return np.percentile(x, QP).tolist() if x.size else [float("nan")]*5

def net_from_draws(W, mut=False):
    out = {}
    for zk in ZS:
        zz = float(zk)
        wz = W@np.array([np.interp(zz, NODES, np.eye(NN)[i]) for i in range(NN)])
        if mut:
            X = (OM*(1 + zz)**3 + OMR*(1 + zz)**4 + WK*(1 + zz)**2 + wz)/(OM + OMR + WK + W[:, 0])
        else:
            X = np.where(W[:, 0] > 0, wz/np.where(W[:, 0] > 0, W[:, 0], 1.0), -1.0)
        out[zk] = dict(sqrtX_q=np.percentile(np.sqrt(np.clip(X, 0, None)), QP).tolist(), P_w_le0=float(np.mean(wz <= 0)))
    return out

def net_flags(netq):
    fl = {}
    for zk, q in netq.items():
        fl[zk] = {"68": "RISE" if q[3] < 1 else ("FALL" if q[1] > 1 else "FLAT"),
                  "95": "RISE" if q[4] < 1 else ("FALL" if q[0] > 1 else "FLAT")}
    return fl

def classify(W, netq, mut=False):
    """Everything per reading for one set of draws. W: (n, 6) X node values (w, or h^2E^2 under MUTATE)."""
    res = {"segments": [f"{NODES[k]:g}-{NODES[k+1]:g}" for k in range(NN - 1)]}
    dW = np.diff(W, axis=1)
    fnec = np.mean(dW < 0, axis=0)
    res["f_NEC"] = fnec.tolist()
    rho_s, d1_s, d2_s = spline_nodes(W)
    nf = net_flags(netq); res["net"] = {"sqrtX_q": netq, "flags": nf}
    for recon in ("literal", "spline"):
        res[recon] = {}
        for R in READ:
            Fa, Fb = seg_F(W, R, recon, (rho_s, d1_s))
            dfd = (Fa > 0) & (Fb > 0)
            rise = dfd & (Fb < Fa - TOL*np.abs(Fa)); fall = dfd & (Fb > Fa + TOL*np.abs(Fa))
            nd = dfd.sum(axis=0)
            pr = np.where(nd > 0, rise.sum(axis=0)/np.maximum(nd, 1), np.nan); pf = np.where(nd > 0, fall.sum(axis=0)/np.maximum(nd, 1), np.nan)
            # segment-average a0 drift in time per Gyr: 1/2 ln(Fa/Fb) / (t_lb(z_b) - t_lb(z_a))
            dt = np.array([TLB[float(NODES[k + 1])] - TLB[float(NODES[k])] for k in range(NN - 1)])
            with np.errstate(divide="ignore", invalid="ignore"):
                rate = np.where(dfd, 0.5*np.log(np.where(dfd, Fa, 1)/np.where(dfd, Fb, 1))/dt, np.nan)
            row = dict(p_rise=pr.tolist(), p_fall=pf.tolist(), undefined=(1 - nd/W.shape[0]).tolist(),
                       seg_rate_per_Gyr_q=[q5(rate[:, k]) for k in range(NN - 1)], flags={}, cls={}, arrow={})
            for L, tl in LEVELS.items():
                RISE = pr >= tl; FALL = pf >= tl; Dn = fnec >= tl
                fl = ["RISE" if RISE[k] else ("FALL" if FALL[k] else "FLAT") for k in range(NN - 1)]
                row["flags"][L] = fl
                netr = R == "eps" and recon == "literal" and any(nf[zk][L] == "RISE" for zk in ZS)
                netf = R == "eps" and recon == "literal" and any(nf[zk][L] == "FALL" for zk in ZS)
                if np.any(RISE & Dn) or netr: c = "PHANTOM-REQUIRED"
                elif np.any(RISE & ~Dn): c = "HEALTHY"
                elif np.any(FALL) or netf: c = "FALLING"
                else: c = "NOT DIAGNOSTIC"
                row["cls"][L] = c
                # arrow / turnaround
                definite = [(NODES[k], NODES[k + 1], +1 if RISE[k] else -1) for k in range(NN - 1) if RISE[k] or FALL[k]]
                if R == "eps" and recon == "literal":
                    definite += [(0.0, float(zk), +1 if nf[zk][L] == "RISE" else -1) for zk in ZS if nf[zk][L] != "FLAT"]
                pairs = [(a, b) for a in range(NN - 1) for b in range(NN - 1) if (RISE[a] and FALL[b]) or (FALL[a] and RISE[b])]
                pairs = [(a, b) for a, b in pairs if NODES[a] >= NODES[b + 1]]      # a at higher z than b
                if pairs:
                    a, b = min(pairs, key=lambda ab: NODES[ab[0]] - NODES[ab[1] + 1])
                    kind = "PEAK (a0 rose, then fell)" if RISE[a] else "TROUGH (a0 fell, then rose)"
                    loc = [float(n) for n in NODES if NODES[b + 1] - 1e-9 <= n <= NODES[a] + 1e-9]
                    ar = dict(cls="TURNAROUND", kind=kind, nodes_z=loc, lookback_Gyr=[TLB[x] for x in loc],
                              verdict="NO GLOBAL VACUUM ARROW (a0 not monotone; its direction flips where w crosses -1 under eps)")
                elif not definite:
                    ar = dict(cls="FLAT", verdict="NO VACUUM CLOCK MEASURED at this level")
                elif len({s for *_, s in definite}) == 1:
                    sg = definite[0][2]
                    ar = dict(cls="RISING-ONLY" if sg > 0 else "FALLING-ONLY", definite=[[float(x), float(y), s] for x, y, s in definite],
                              verdict="DIRECTION SEEN, MONOTONICITY NOT ESTABLISHED")
                else:
                    ar = dict(cls="MIXED (not classified by the frozen rule)", definite=[[float(x), float(y), s] for x, y, s in definite],
                              verdict="not classified")
                row["arrow"][L] = ar
            res[recon][R] = row
    # descriptive
    am = np.argmax(W, axis=1)
    res["P_max_at_node"] = {f"{NODES[k]:g}": float(np.mean(am == k)) for k in range(NN)}
    res["P_monotone_rising_in_t"] = float(np.mean(np.all(dW < 0, axis=1)))
    res["P_monotone_falling_in_t"] = float(np.mean(np.all(dW > 0, axis=1)))
    zm = 0.5*(NODES[1:] + NODES[:-1]); m = dW/np.diff(NODES); rmid = 0.5*(W[:, 1:] + W[:, :-1])
    with np.errstate(divide="ignore", invalid="ignore"):
        weff = np.where(rmid > 0, -1 + (1 + zm)*m/(3*rmid), np.nan)
    res["w_eff_secant_q"] = [q5(weff[:, k]) for k in range(NN - 1)]
    # a0 ratio at the unstored nodes 0.4, 0.7 (eps, literal) - descriptive
    with np.errstate(divide="ignore", invalid="ignore"):
        res["sqrtX_nodes_q"] = {f"{NODES[k]:g}": q5(np.where((W[:, 0] > 0) & (W[:, k] > 0), np.sqrt(W[:, k]/W[:, 0]), np.nan)) for k in range(1, NN)}
    # rates today
    m1 = (W[:, 1] - W[:, 0])/(NODES[1] - NODES[0]); w0 = W[:, 0]
    rt = {}
    with np.errstate(divide="ignore", invalid="ignore"):
        lit = {"eps": np.where(w0 > 0, -0.5*H0G*m1/w0, np.nan),
               "-p": np.where(w0 - m1/3 > 0, -0.5*H0G*(2/3)*m1/(w0 - m1/3), np.nan),
               "V": np.where(w0 - m1/6 > 0, -0.5*H0G*(5/6)*m1/(w0 - m1/6), np.nan)}
        r0, a1, a2 = rho_s[:, 0], d1_s[:, 0], d2_s[:, 0]
        spl = {"eps": np.where(r0 > 0, -0.5*H0G*a1/r0, np.nan),
               "-p": np.where(r0 - a1/3 > 0, -0.5*H0G*((2/3)*a1 - a2/3)/(r0 - a1/3), np.nan),
               "V": np.where(r0 - a1/6 > 0, -0.5*H0G*((5/6)*a1 - a2/6)/(r0 - a1/6), np.nan)}
    for R in READ:
        rt[("literal", R)] = lit[R]; rt[("spline", R)] = spl[R]
    Ep0 = (3*OM + 4*OMR + 2*WK + m1)/(2*H2BAR)
    rt[("rival", "H")] = -H0G*Ep0
    res["rates_today"] = {}
    for (recon, R), arr in rt.items():
        q = q5(arr); a68 = max(abs(q[1]), abs(q[3]))
        res["rates_today"][f"{recon}:{R}"] = dict(q_per_Gyr=q, q_per_yr=[x/1e9 for x in q], q_H0=[x/H0G for x in q],
                                                 abs68_per_yr=a68/1e9, undefined=float(np.mean(~np.isfinite(arr))))
    res["_raw_rates"] = rt
    return res

def strip(res):
    return {k: v for k, v in res.items() if not k.startswith("_")}

# =====================================================================================================================
# main computation
# =====================================================================================================================
STORED_NET = {zk: B["P1"][zk]["sqrtX_q"] for zk in ZS}
RUNS = {}
for rho_adj in RHOS:
    W = draw(rho_adj)
    if MUT:
        X = mutate(W); netq = {zk: v["sqrtX_q"] for zk, v in net_from_draws(W, mut=True).items()}
        RUNS[rho_adj] = classify(X, netq, mut=True)
        RUNS[rho_adj]["_W"] = W
    else:
        RUNS[rho_adj] = classify(W, STORED_NET)
        if rho_adj == 0.0:
            NETD = net_from_draws(W); W0KEEP = W
    P(f"  draws rho_adj = {rho_adj:+.1f}: done")

# ---- K1b approximation diagnostic (main only) ----
if not MUT:
    P("\n=== K1b. APPROX-G (rho_adj = 0) vs stored joint quantities (diagnostic; flags only) ===")
    k1b_flags = {}
    for zk in ZS:
        s, d = STORED_NET[zk], NETD[zk]["sqrtX_q"]
        dev = max(abs(s[i] - d[i]) for i in (1, 2, 3)); dp = abs(NETD[zk]["P_w_le0"] - B["P3"]["P_w_le0"][zk])
        ok = dev <= 0.03 and dp <= 0.01; k1b_flags[zk] = dict(ok=ok, max_dev_16_50_84=dev, dP_w_le0=dp, approx=d, stored=s)
        P(f"  z {zk}: approx sqrtX 16/50/84 {np.round(d[1:4], 4).tolist()} vs stored {np.round(s[1:4], 4).tolist()} (max dev {dev:.4f}); "
          f"P_w_le0 {NETD[zk]['P_w_le0']:.4f} vs {B['P3']['P_w_le0'][zk]:.4f}  -> {'OK' if ok else 'APPROXIMATION OFF at z ' + zk}")
    RES["K1b"] = k1b_flags

# ---- K2 constant DE (identity) ----
P("\n=== K2. constant dark energy => flat (TRUE BY CONSTRUCTION) ===")
Wc = (W0KEEP if not MUT else RUNS[0.0]["_W"])[:50_000, :1].repeat(NN, axis=1)
rc = classify(Wc, {zk: [1.0]*5 for zk in ZS})
k2 = True
for recon in ("literal", "spline"):
    for R in READ:
        r = rc[recon][R]; flat = all(x == 0 for x in r["p_rise"]) and all(x == 0 for x in r["p_fall"])
        k2 &= flat
for key, arr in rc["_raw_rates"].items():
    if key[0] in ("literal", "spline"):
        k2 &= bool(np.nanmax(np.abs(arr)) <= 1e-12*H0G)
check("K2 constant DE -> every reading flat, rate 0", k2, "all segments flat in every draw; |r| <= 1e-12 H0 (literal and spline)")

# ---- K3 logic plants ----
P("\n=== K3. noiseless plants (w = -1.2 phantom, w = -0.8 quintessence) ===")
k3 = True
for wpl, want_flag, want_cls in ((-1.2, "RISE", "PHANTOM-REQUIRED"), (-0.8, "FALL", "FALLING")):
    mu_p = 0.31*(1 + NODES)**(3*(1 + wpl))
    Wp = draw(0.0, n=20_000, mu=mu_p, sd=SD*1e-9, seed=SEED + 7)
    netp = {zk: v["sqrtX_q"] for zk, v in net_from_draws(Wp).items()}
    rp = classify(Wp, netp)
    lit = rp["literal"]["eps"]
    okf = all(f == want_flag for f in lit["flags"]["95"]); okc = lit["cls"]["68"] == want_cls and lit["cls"]["95"] == want_cls
    exact = classify(mu_p[None, :].repeat(2, axis=0), netp)["_raw_rates"][("literal", "eps")][0]
    sec = -0.5*H0G*((1.4)**(3*(1 + wpl)) - 1)/0.4; inst = -1.5*(1 + wpl)*H0G
    oks = abs(exact/sec - 1) <= 1e-10 and np.sign(exact) == np.sign(inst)
    k3 &= okf and okc and oks
    P(f"  w = {wpl}: flags95 {lit['flags']['95']} cls68/95 {lit['cls']['68']}/{lit['cls']['95']}; rate {exact:+.6e}/Gyr vs secant "
      f"{sec:+.6e} (rel {abs(exact/sec - 1):.1e}); secant/instantaneous = {sec/inst:.4f} (reported, not graded)")
check("K3 plants recovered", k3, "phantom -> RISE_95 x5 + PHANTOM-REQUIRED; quintessence -> FALL_95 x5 + FALLING; secant rate to 1e-10")

# =====================================================================================================================
# report
# =====================================================================================================================
P("\n=== B/C. Per-segment drift of a0 in cosmic time (literal = CFG689's own linear w(z); PRIMARY) ===")
P("segment z: " + "  ".join(RUNS[0.0]["segments"]) + "   (lookback Gyr at nodes: "
  + ", ".join(f"{TLB[float(n)]:.2f}" for n in NODES) + ")")
for rho_adj in RHOS:
    r = RUNS[rho_adj]
    P(f"\n-- rho_adj = {rho_adj:+.1f} --")
    P("  f_NEC (P(dw<0): band needs NEC violation somewhere in the segment; reading-independent; under V = ghost needed): "
      + "  ".join(f"{x:.3f}" for x in r["f_NEC"]))
    for recon in ("literal", "spline"):
        for R in READ:
            row = r[recon][R]
            P(f"  {recon:7s} {R:3s} p_rise " + " ".join(f"{x:.3f}" for x in row["p_rise"]) + " | p_fall "
              + " ".join(f"{x:.3f}" for x in row["p_fall"]) + f" | undef max {max(row['undefined']):.3f}"
              + f" | 68% {row['flags']['68']} -> {row['cls']['68']} | 95% {row['flags']['95']} -> {row['cls']['95']}")
    P("  w_eff (secant, median [16, 84]) per segment: " + "; ".join(f"{q[2]:+.3f} [{q[1]:+.3f}, {q[3]:+.3f}]" for q in r["w_eff_secant_q"]))
    P("  literal eps segment-average d ln a0/dt per Gyr, median [16, 84]: "
      + "; ".join(f"{q[2]:+.4f} [{q[1]:+.4f}, {q[3]:+.4f}]" for q in r["literal"]["eps"]["seg_rate_per_Gyr_q"]))
    P("  a0(z_k)/a0(0) (eps) at nodes, median [16, 84]: " + "; ".join(f"z {k}: {q[2]:.3f} [{q[1]:.3f}, {q[3]:.3f}]" for k, q in r["sqrtX_nodes_q"].items()))
    P("  P(a0 maximum at node): " + ", ".join(f"z {k}: {v:.3f}" for k, v in r["P_max_at_node"].items())
      + f"; P(monotone rising in t) {r['P_monotone_rising_in_t']:.4f}; P(monotone falling in t) {r['P_monotone_falling_in_t']:.4f}")
P("\nnet intervals [0, z] (eps, stored sqrtX_q; interpolation-free): "
  + "; ".join(f"z {zk}: 68% {f['68']}, 95% {f['95']}" for zk, f in RUNS[0.0]["net"]["flags"].items()))
if not MUT:
    for zk in ZS:   # descriptive: probability level where the stored band crosses 1 (linear in normal score)
        q = np.array(STORED_NET[zk]); sc = norm.ppf(np.array(QP)/100)
        P(f"  z {zk}: P(net rise from z to now) ~ {norm.cdf(np.interp(1.0, q, sc)):.3f} (interpolated from the stored quantiles; descriptive)")

# ---- verdict per reading ----
P("\n=== VERDICT per reading (literal reconstruction; class at rho_adj = 0, suffix if the bracket changes it) ===")
VERD = {}
for R in READ:
    VERD[R] = {}
    for L in LEVELS:
        cl = {ra: RUNS[ra]["literal"][R]["cls"][L] for ra in RHOS}
        s = cl[0.0] + ("" if len(set(cl.values())) == 1 else " (CORRELATION-SENSITIVE: " + ", ".join(f"{ra:+.1f}: {c}" for ra, c in cl.items()) + ")")
        VERD[R][L] = s
    P(f"  {R:3s}: 68% {VERD[R]['68']}\n       95% {VERD[R]['95']}")
VERD_SPL = {R: {L: {f"{ra:+.1f}": RUNS[ra]["spline"][R]["cls"][L] for ra in RHOS} for L in LEVELS} for R in READ}
P("  spline (sensitivity, no verdict weight): " + "; ".join(f"{R} 68% {VERD_SPL[R]['68']['+0.0']}/95% {VERD_SPL[R]['95']['+0.0']}" for R in READ))
THEO = {"eps": "NO: a rising a0 IS NEC violation (S1).",
        "-p": "YES in principle: with NEC, if rho'' > 2 rho'/(1+z) (c_a^2 > 0; e.g. a scalar faster than slow roll on a shallow potential).",
        "V": "YES in principle, transient: the scalar must climb (V' phi_dot > 0), needs rho' >= 0 and rho'' > 5 rho'/(1+z)."}
P("  THEOREM-LEVEL (can a rising a0 come from healthy minimal DE at all?): " + " | ".join(f"{R}: {v}" for R, v in THEO.items()))
P("  Does the CFG689 band measure the rho'' that -p and V need? NO: nodes 0.3-0.83 apart, rho'' = 0 inside segments (S4); "
  "the spline rows show what a smooth choice does.")
ARW = {L: {f"{ra:+.1f}": RUNS[ra]["literal"]["eps"]["arrow"][L] for ra in RHOS} for L in LEVELS}
P("\n=== D. Arrow / turnaround (literal, eps; -p and V identical inside segments by S4) ===")
for L in LEVELS:
    for ra in RHOS:
        a = ARW[L][f"{ra:+.1f}"]
        P(f"  {L}% rho_adj {ra:+.1f}: {a['cls']}" + (f" {a.get('kind', '')} at z {a.get('nodes_z')} (lookback {np.round(a.get('lookback_Gyr', []), 2).tolist()} Gyr)" if a["cls"] == "TURNAROUND" else "")
          + f" -> {a['verdict']}")
P("  by construction: a0 depends on t only through rho_DE(a(t)); any direction it has is the expansion's, read through dark energy.")

# ---- E. rates today ----
P("\n=== E. Rate today d ln a0/dt at z = 0 (H0 = %.3f km/s/Mpc = %.5f /Gyr, mean background) ===" % (HBAR0, H0G))
RT = RUNS[0.0]["rates_today"]
for key, v in RT.items():
    q = v["q_per_Gyr"]
    P(f"  {key:12s} median {q[2]:+.3e}/Gyr = {q[2]/1e9:+.3e}/yr ({q[2]/H0G:+.3f} H0); 68% [{q[1]:+.3e}, {q[3]:+.3e}]/Gyr; "
      f"95% [{q[0]:+.3e}, {q[4]:+.3e}]/Gyr; undefined {v['undefined']:.4f}")
for ra in (-0.5, 0.5):
    P(f"  bracket rho_adj {ra:+.1f}: literal eps 68% [{RUNS[ra]['rates_today']['literal:eps']['q_per_Gyr'][1]:+.3e}, "
      f"{RUNS[ra]['rates_today']['literal:eps']['q_per_Gyr'][3]:+.3e}]/Gyr; rival median {RUNS[ra]['rates_today']['rival:H']['q_per_Gyr'][2]:+.3e}/Gyr")
a0q = B["P3"]["a0_node_q"]["0.0"]; DREC = (a0q[3] - a0q[1])/(2*a0q[2])
P(f"\n  reachability: delta_rec = (q84 - q16)/(2 q50) of P3.a0_node_q[0.0] = {DREC:.4f}; baseline 100 yr; stress delta 1e-6 (hypothetical)")
REACH = {}
for key, v in RT.items():
    a68 = v["abs68_per_yr"]; Treq = DREC/a68 if a68 > 0 else float("inf"); Ts = 1e-6/a68 if a68 > 0 else float("inf")
    REACH[key] = dict(abs68_per_yr=a68, T_req_yr=Treq, T_req_stress_yr=Ts, cls="REACHABLE" if Treq <= 100 else "NOT REACHABLE",
                      drift_100yr=a68*100)
    P(f"  {key:12s} |r|_68 = {a68:.3e}/yr -> 100-yr drift {a68*100:.2e}; T_req {Treq:.2e} yr (stress 1e-6: {Ts:.2e} yr) -> {REACH[key]['cls']}")
# observables
MB = 6e10*MSUN
OBS = {}
P("\n  observables (deep-MOND flat curve, M_b = 6e10 Msun, outer orbit at r = 3 r_M); per footing; 100-yr changes")
for fname, a0f in FOOT.items():
    v = (G*MB*a0f)**0.25; rM = math.sqrt(G*MB/a0f); rorb = 3*rM; Per = 2*math.pi*rorb/v
    OBS[fname] = dict(a0=a0f, v_flat_kms=v/1e3, r_M_kpc=rM/3.0856775814913673e19, P_orbit_Myr=Per/(1e6*YR), rows={})
    P(f"  [{fname}] a0 {a0f:.4e}: v_flat {v/1e3:.2f} km/s, r_M {rM/3.0856775814913673e19:.2f} kpc, P(3 r_M) {Per/(1e6*YR):.1f} Myr")
    for key in ("literal:eps", "literal:-p", "literal:V", "spline:eps", "rival:H"):
        for lab, rv in (("median", RT[key]["q_per_yr"][2]), ("|68|", RT[key]["abs68_per_yr"])):
            row = dict(adot0_m_s2_per_yr=a0f*rv, dv_100yr_m_s=v*rv/4*100, drM_100yr_AU=-rM*rv/2*100/AU,
                       dP_fixed_r_100yr_s=-Per*rv/4*100, dP_adiabatic_100yr_s=-Per*rv/2*100, efold_time_Gyr=(1/abs(rv)/1e9 if rv != 0 else float("inf")))
            OBS[fname]["rows"][f"{key}:{lab}"] = row
            P(f"    {key:12s} {lab:6s} rate {rv:+.2e}/yr: a0_dot {row['adot0_m_s2_per_yr']:+.2e} m/s^2/yr; dv {row['dv_100yr_m_s']:+.2e} m/s; "
              f"dr_M {row['drM_100yr_AU']:+.2e} AU; dP {row['dP_fixed_r_100yr_s']:+.2e} s (fixed r) / {row['dP_adiabatic_100yr_s']:+.2e} s (adiabatic); "
              f"e-fold {row['efold_time_Gyr']:.3g} Gyr")
# F. identity
P("\n=== F. IDENTITY (no verdict weight): de Sitter horizon entropy through a0 ===")
SID = {}
for fname, a0f in FOOT.items():
    S = 3*CMS**7/(32*G*HBAR*a0f**2); Hl = ZVAL*a0f/CMS; S2 = math.pi*CMS**5/(G*HBAR*Hl**2)
    SID[fname] = dict(S_over_kB=S, H_L_per_s=Hl, check_rel=abs(S/S2 - 1))
    P(f"  [{fname}] S/k_B = 3c^7/(32 G hbar a0^2) = {S:.4e} (= pi c^5/(G hbar H^2) with H = Z a0/c = {Hl:.4e}/s; rel {abs(S/S2-1):.1e}); "
      f"d ln S/dt = -2 d ln a0/dt -> today (literal eps median) {-2*RT['literal:eps']['q_per_yr'][2]:+.2e}/yr")

# ---- MUTATE grading ----
if MUT:
    P("\n=== MUTATE grading (X -> H^2: the rival a0 ~ H(z)) ===")
    r0 = RUNS[0.0]["literal"]["eps"]
    i_ = all(f == "FALL" for f in r0["flags"]["95"]); ii = r0["cls"]["68"] == "FALLING" and r0["cls"]["95"] == "FALLING"
    iii = ARW["68"]["+0.0"]["cls"] == "FALLING-ONLY" and ARW["95"]["+0.0"]["cls"] == "FALLING-ONLY"
    Wm = RUNS[0.0]["_W"][:1000]; Xm = mutate(Wm)
    rm = -0.5*H0G*(Xm[:, 1] - Xm[:, 0])/(0.4*Xm[:, 0]); E2 = Xm[:, 1]/Xm[:, 0]; rsec = -0.5*H0G*(E2 - 1)/0.4
    iv = bool(np.max(np.abs(rm/rsec - 1)) <= 1e-10)
    main_cls = None
    try:
        main_cls = json.load(open(os.path.join(HERE, "wt03_results.json")))["verdict"]["eps"]["68"].split(" (")[0]
    except Exception:
        pass
    bite = (main_cls is not None) and (main_cls != r0["cls"]["68"])
    P(f"  (i) all five FALL_95: {i_}; (ii) class FALLING at 68/95: {ii} ({r0['cls']['68']}/{r0['cls']['95']}); (iii) arrow FALLING-ONLY: {iii}; "
      f"(iv) rate == rival secant: {iv}")
    P(f"  bite: unmutated eps 68% class = {main_cls}; mutated = {r0['cls']['68']} -> {'BITES (class flips)' if bite else 'NO BITE'}")
    RES["MUTATE"] = dict(i=i_, ii=ii, iii=iii, iv=iv, PASS=bool(i_ and ii and iii and iv), unmutated_eps68=main_cls, bite=bool(bite))
    P(f"  MUTATE {'PASS' if RES['MUTATE']['PASS'] else 'FAIL'}")

RES["runs"] = {f"{ra:+.1f}": strip(RUNS[ra]) for ra in RHOS}
RES["verdict"] = VERD; RES["verdict_spline_sensitivity"] = VERD_SPL; RES["theorem_level"] = THEO; RES["arrow"] = ARW
RES["reachability"] = dict(delta_rec=DREC, baseline_yr=100, stress_delta=1e-6, rows=REACH)
RES["observables"] = OBS; RES["identity_entropy"] = SID; RES["checks"] = CHECKS
def jdef(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
for ra in RHOS:
    RES["runs"][f"{ra:+.1f}"].pop("_W", None)
json.dump(RES, open(os.path.join(HERE, f"wt03_results{TAG}.json"), "w"), indent=1, default=jdef)
hard = all(CHECKS[k]["ok"] for k in CHECKS)
P(f"\nChecks: {sum(c['ok'] for c in CHECKS.values())}/{len(CHECKS)} pass" + ("" if hard else " -> exit 1"))
OUTF.close()
sys.exit(0 if hard else 1)
