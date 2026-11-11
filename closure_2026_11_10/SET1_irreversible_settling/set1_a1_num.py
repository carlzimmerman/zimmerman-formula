#!/usr/bin/env python3
"""SET1 A1b / A1c: the P = J(g) static state for extended spherical baryons, against the law; known answers; MUTATE.

    python3 set1_a1_num.py                  -> set1_a1_num.out / .json
    SET1_MUTATE=M1 python3 set1_a1_num.py   -> *_MUTATE_M1.*  (target spread doubled, P = 2J)
    SET1_MUTATE=M3 python3 set1_a1_num.py   -> *_MUTATE_M3.*  (no target pressure, J = 0)

The P = c J(g) state solves  g' = (K rho_b - 2 g / r) / (1 + c/(1 + u))  (Jeans + Poisson, A1a).  For c = 1 it is solved
exactly as Y(r) = r^2 mu(u) g / G = Int_0^r mu(u) dM_b (A1a (i), (iv)), with a0 u^2/(1 + u) = G Y / r^2.
Units kpc, km/s, Msun. TEST lane (FROZEN_CRITERIA.md section 3). Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp, quad
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get('SET1_MUTATE', '')
G = 4.30091e-6
K = 4 * math.pi * G
A0 = {'canonical': 9.3603e-11 * 3.0857e19 / 1e6, 'alt': 1.1312e-10 * 3.0857e19 / 1e6}
LINE = {'canonical': 0.0660, 'alt': 0.0658}
LOGM = [9.4, 10.45, 10.7, 10.9]
CJ = {'': 1.0, 'M1': 2.0, 'M3': 0.0}[MUT]
lines, RES = [], {'mutate': MUT, 'c_J': CJ}


def out(s):
    print(s); lines.append(s)


def R50(M): return 0.10 * M ** 0.14 * (1 + M / 3.98e10) ** 0.25


class Plummer:
    name = 'Plummer'
    def __init__(self, M, R): self.M, self.b = M, R / 1.3048
    def Menc(self, r): return self.M * r ** 3 / (r * r + self.b ** 2) ** 1.5
    def rho(self, r): return 3 * self.M / (4 * math.pi * self.b ** 3) * (1 + (r / self.b) ** 2) ** -2.5
    def col(self, r):                                   # Int_r^inf rho dr'
        s = r / self.b
        return 3 * self.M / (4 * math.pi * self.b ** 2) * (2 / 3 - s * (2 * s * s + 3) / (3 * (1 + s * s) ** 1.5))


class Hernquist:
    name = 'Hernquist'
    def __init__(self, M, R): self.M, self.a = M, R / (1 + math.sqrt(2))
    def Menc(self, r): return self.M * r * r / (r + self.a) ** 2
    def rho(self, r): return self.M * self.a / (2 * math.pi * r * (r + self.a) ** 3)
    def col(self, r): return quad(self.rho, r, np.inf, limit=200)[0]


def u_of_s(s): return 0.5 * (s + np.sqrt(s * s + 4 * s))          # u^2/(1+u) = s


def glaw(gN, a0): return 0.5 * (gN + np.sqrt(gN * gN + 4 * a0 * gN))


def law_state(p, r, a0):
    """g_law and rho_ph (analytic derivative)."""
    Mr = p.Menc(r); gN = G * Mr / r ** 2
    gl = glaw(gN, a0)
    dgN = K * p.rho(r) - 2 * gN / r                                  # g_N' (Poisson for the baryons)
    dgl = 0.5 * (1 + (gN + 2 * a0) / np.sqrt(gN * gN + 4 * a0 * gN)) * dgN
    rho_ph = ((2 * gl / r + dgl) - (2 * gN / r + dgN)) / K
    return gl, rho_ph


def jstate_Y(p, a0, rmin, rmax):
    """P = J state (c = 1) by the Y integral; returns callables g(r), rho_c(r) (Jeans form) and rho_c (Poisson form)."""
    r0 = rmin; Mb0 = p.Menc(r0); mu0 = 0.5
    for _ in range(200):
        u0 = u_of_s(G * mu0 * Mb0 / (a0 * r0 * r0)); mu0n = u0 / (1 + u0)
        if abs(mu0n - mu0) < 1e-15: break
        mu0 = mu0n

    def rhs(t, Y):
        r = math.exp(t); u = u_of_s(G * Y[0] / (a0 * r * r))
        return [u / (1 + u) * 4 * math.pi * r ** 3 * p.rho(r)]
    sol = solve_ivp(rhs, (math.log(rmin), math.log(rmax)), [mu0 * Mb0], method='DOP853', rtol=1e-11, atol=1e-30 + 0 * Mb0,
                    dense_output=True)

    def fields(r):
        r = np.asarray(r, float); Y = sol.sol(np.log(r))[0]
        s = G * Y / (a0 * r * r); u = u_of_s(s); mu = u / (1 + u)
        ds = G * mu * 4 * math.pi * r * r * np.vectorize(p.rho)(r) / (a0 * r * r) - 2 * s / r
        du = (1 + u) ** 2 / (u * (2 + u)) * ds
        g = a0 * u; dg = a0 * du
        rho_c_jeans = -dg / (K * (1 + u))
        rho_c_pois = (2 * g / r + dg) / K - np.vectorize(p.rho)(r)
        return g, rho_c_jeans, rho_c_pois, Y
    return fields, sol


def cstate_ode(p, a0, c, rmin, rmax, r_eval):
    """P = c J state by the direct ODE (used for MUTATE and as a cross-check of the Y form)."""
    g0 = glaw(G * p.Menc(rmin) / rmin ** 2, a0) if c > 0 else G * p.Menc(rmin) / rmin ** 2

    def rhs(t, y):
        r = math.exp(t); g = y[0]; u = g / a0
        return [r * (K * p.rho(r) - 2 * g / r) / (1 + c / (1 + u))]
    sol = solve_ivp(rhs, (math.log(rmin), math.log(rmax)), [g0], method='LSODA', rtol=1e-10, atol=1e-12,
                    t_eval=np.log(r_eval))
    return sol.y[0]


class Point:
    """softened-free point mass via a very compact Plummer (KA4) is used instead; this class serves M1/M3 only."""
    name = 'point'
    def __init__(self, M): self.M = M
    def Menc(self, r): return self.M
    def rho(self, r): return 0.0


# ---------------------------------------------------------------- known answers
KA = {}
for foot in ('canonical', 'alt'):
    a0 = A0[foot]; M = 10 ** 10.45; rM = math.sqrt(G * M / a0)
    # KA1 point-mass M_ph closed form against the numeric integral of the law's rho_ph (compact Plummer as the point)
    pc = Plummer(M, 1e-5 * rM * 1.3048)
    xs = np.array([0.1, 0.3, 1.0, 3.0, 10.0])
    errs = []
    for xv in xs:
        rr = np.logspace(math.log10(1e-3 * rM), math.log10(xv * rM), 4001)
        _, rp = law_state(pc, rr, a0)
        num = TRAPZ(4 * math.pi * rr ** 2 * rp, rr)
        r1 = 1e-3 * rM; g1, _ = law_state(pc, np.array([r1]), a0)
        num += r1 * r1 * (g1[0] - G * pc.Menc(r1) / r1 ** 2) / G     # phantom inside 1e-3 r_M by Gauss
        closed = M * (math.sqrt(1 + 4 * xv * xv) - 1) / 2
        errs.append(abs(num / closed - 1))
    KA[f'KA1_{foot}'] = dict(max_rel=float(max(errs)), line=1e-6, pass_=bool(max(errs) < 1e-6))
    # KA2 Newtonian limit (a0 x 1e-6), Plummer at log M 10.45
    p = Plummer(M, R50(M)); a0n = a0 * 1e-6
    f, _ = jstate_Y(p, a0n, 1e-7 * R50(M), 1e3 * R50(M))
    rw = R50(M) * np.logspace(math.log10(0.3), math.log10(6), 60)
    g, *_ = f(rw); gN = G * np.vectorize(p.Menc)(rw) / rw ** 2
    e2 = float(np.max(np.abs(g / gN - 1)))
    KA[f'KA2_{foot}'] = dict(max_rel=e2, line=1e-4, pass_=bool(e2 < 1e-4))
    # KA3 deep limit (a0 x 1e8): closed forms
    a0d = a0 * 1e8
    f, _ = jstate_Y(p, a0d, 1e-7 * R50(M), 1e3 * R50(M)); g, *_ = f(rw)
    gP = G * M / (2 * rw * p.b) * (1 - (1 + (rw / p.b) ** 2) ** -1.5)
    h = Hernquist(M, R50(M)); fh, _ = jstate_Y(h, a0d, 1e-7 * R50(M), 1e3 * R50(M)); gh, *_ = fh(rw)
    gH = G * M * (rw + 2 * h.a) / (2 * h.a * (rw + h.a) ** 2)
    e3 = float(max(np.max(np.abs(g / gP - 1)), np.max(np.abs(gh / gH - 1))))
    KA[f'KA3_{foot}'] = dict(max_rel=e3, line=1e-4, pass_=bool(e3 < 1e-4))
    # KA4 compact Plummer b = 1e-4 r_M: the P = J state is the law at r >= 0.1 r_M
    pc = Plummer(M, 1e-4 * rM * 1.3048)
    f, _ = jstate_Y(pc, a0, 1e-7 * rM, 1e4 * rM)
    rr = rM * np.logspace(-1, 2, 60); g, *_ = f(rr); gl, _ = law_state(pc, rr, a0)
    e4 = float(np.max(np.abs(np.log10(g / gl))))
    KA[f'KA4_{foot}'] = dict(max_dex=e4, line=1e-3, pass_=bool(e4 < 1e-3))
RES['known_answers'] = KA
ka_ok = all(v['pass_'] for v in KA.values())
out('Known answers (FROZEN_CRITERIA A1):')
for k, v in KA.items():
    out(f'  {k}: ' + ', '.join(f'{kk} {vv:.3g}' if isinstance(vv, float) else f'{kk} {vv}' for kk, vv in v.items()))
out(f'  ALL KNOWN ANSWERS {"PASS" if ka_ok else "FAIL"}')

# ---------------------------------------------------------------- MUTATE arms (point mass, c = 2 or 0)
if MUT:
    bite = {}
    for foot in ('canonical', 'alt'):
        a0 = A0[foot]; M = 10 ** 10.45; rM = math.sqrt(G * M / a0); pt = Point(M)
        rr = rM * np.logspace(math.log10(0.3), math.log10(30), 60)
        g = cstate_ode(pt, a0, CJ, 1e-4 * rM, 31 * rM, rr)
        gl = glaw(G * M / rr ** 2, a0)
        d = float(np.max(np.abs(np.log10(g / gl))))
        bite[foot] = dict(max_dex_off_law=d, line=LINE[foot], bites=bool(d > LINE[foot]))
        out(f'MUTATE {MUT} ({foot}): point-mass P = {CJ:g} J state, max |dex| from the law over [0.3, 30] r_M = {d:.3f}'
            f' (line {LINE[foot]}): {"BITES" if d > LINE[foot] else "DOES NOT BITE"}')
    RES['mutate_bite'] = bite
    stem = f'set1_a1_num_MUTATE_{MUT}'
    open(os.path.join(HERE, stem + '.out'), 'w').write('\n'.join(lines) + '\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n')
    json.dump(RES, open(os.path.join(HERE, stem + '.json'), 'w'), indent=1)
    sys.exit(1 if all(b['bites'] for b in bite.values()) else 0)

# cross-check of the c = 1 point-mass ODE against the law (the direct form of A1a (iii))
xc = {}
for foot in ('canonical', 'alt'):
    a0 = A0[foot]; M = 10 ** 10.45; rM = math.sqrt(G * M / a0)
    rr = rM * np.logspace(math.log10(0.3), math.log10(30), 60)
    g = cstate_ode(Point(M), a0, 1.0, 1e-4 * rM, 31 * rM, rr)
    xc[foot] = float(np.max(np.abs(np.log10(g / glaw(G * M / rr ** 2, a0)))))
RES['point_mass_ode_c1_max_dex'] = xc
out(f'Point mass, direct ODE with P = J: max |dex| from the law over [0.3, 30] r_M = {xc["canonical"]:.2e} / {xc["alt"]:.2e}')

# ---------------------------------------------------------------- A1b rows
out('\nA1b: P = J(g) static state for extended spherical baryons (window r in [0.3, 6] R_50; dex in g):')
out('footing   logM  profile    R50   r_M   rms_dex  max_dex  asym_dex  min rho_c/peak rho_ph  neg range (R50)  '
    'M_neg/M_b   rho_c(0)/rho_b(0)  D: a0 col/J at R50  Jeans-Poisson check')
ROWS = []
for foot in ('canonical', 'alt'):
    a0 = A0[foot]
    for lm in LOGM:
        M = 10 ** lm; R = R50(M); rM = math.sqrt(G * M / a0)
        for P in (Plummer, Hernquist):
            p = P(M, R)
            f, sol = jstate_Y(p, a0, 1e-7 * R, 1e4 * R)
            rw = R * np.logspace(math.log10(0.3), math.log10(6), 60)
            g, rcj, rcp, _ = f(rw); gl, rph = law_state(p, rw, a0)
            dex = np.log10(g / gl)
            rms = float(np.sqrt(np.mean(dex ** 2))); mx = float(np.max(np.abs(dex)))
            Meff = float(sol.sol(math.log(1e4 * R))[0] / p.Menc(1e4 * R))
            asym = 0.5 * math.log10(Meff)
            rf = R * np.logspace(-5, 2, 4001)
            gf_, rcf, rcpf, _ = f(rf)
            peak = float(np.max(rph))
            neg = rcf < 0
            if neg.any():
                rlo, rhi = float(rf[neg].min() / R), float(rf[neg].max() / R)
                Mneg = float(TRAPZ(np.where(neg, 4 * math.pi * rf ** 2 * rcf, 0.0), rf) / M)
            else:
                rlo = rhi = float('nan'); Mneg = 0.0
            minrel = float(rcf.min() / peak)
            resolved_neg = bool(minrel < -1e-6 and neg.any() and (rhi - rlo) > 0.01)
            rc0 = float(rcf[0] / p.rho(rf[0]))
            jcheck = float(np.max(np.abs(rcf - rcpf) / np.maximum(np.abs(rcpf), 1e-300)))
            # reading D: P_eq = J(g_law) + a0 Int_r^inf rho_b ; nonlocal piece / J at R_50
            glR, _ = law_state(p, np.array([R]), a0); uR = glR[0] / a0
            JR = a0 ** 2 / K * (uR - math.log1p(uR))
            Dratio = a0 * p.col(R) / JR
            fail_rms = rms > LINE[foot]
            row = dict(footing=foot, logM=lm, profile=p.name, R50_kpc=R, rM_kpc=rM, rms_dex=rms, max_dex=mx,
                       asym_dex=asym, M_eff_over_Mb=Meff, min_rho_c_over_peak_rho_ph=minrel,
                       neg_range_R50=[rlo, rhi], M_neg_over_Mb=Mneg, rho_c0_over_rho_b0=rc0,
                       D_nonlocal_over_J_at_R50=Dratio, jeans_poisson_maxrel=jcheck,
                       fails_negative=resolved_neg, fails_rms=bool(fail_rms), line=LINE[foot])
            ROWS.append(row)
            out(f'{foot:9s} {lm:5.2f} {p.name:9s} {R:5.2f} {rM:5.2f}  {rms:7.4f}  {mx:7.4f}  {asym:+8.4f}  '
                f'{minrel:+12.4e}          {rlo:7.4f}-{rhi:7.4f}  {Mneg:+.3e}   {rc0:+8.4f}           {Dratio:8.3f}'
                f'           {jcheck:.1e}')
RES['A1b_rows'] = ROWS

# ---------------------------------------------------------------- A1c (reported): point-mass spread and Knudsen number
out('\nA1c (reported): point mass, sigma^2 = J/rho_ph (units sqrt(G M a0)), d ln sigma^2/d ln r, Knudsen sigma tau/r')
A1c = []
for x in (0.3, 1.0, 3.0, 10.0):
    def s2(xx):
        u = 0.5 * (1 / xx ** 2 + math.sqrt(1 / xx ** 4 + 4 / xx ** 2))
        return 0.5 * xx * math.sqrt(1 + 4 * xx * xx) * (u - math.log1p(u)), u
    v, u = s2(x); e = 1e-5
    slope = (math.log(s2(x * (1 + e))[0]) - math.log(s2(x * (1 - e))[0])) / (math.log(1 + e) - math.log(1 - e))
    vc2 = u * x                     # g r in units sqrt(G M a0): g = a0 u, r = x r_M -> a0 u x r_M = u x sqrt(G M a0)
    kn = {eta: 2 * math.pi * eta * math.sqrt(v / vc2) for eta in (0.3, 1.0, 3.0)}
    A1c.append(dict(x=x, sigma2=v, dlnsig2_dlnr=slope, sigma2_over_vc2=v / vc2, knudsen=kn))
    out(f'  x = {x:5.1f}: sigma^2 = {v:.4f}, slope {slope:+.3f}, sigma^2/v_c^2 = {v / vc2:.3f}, Kn (eta 0.3/1/3) = '
        + ' / '.join(f'{kn[k]:.2f}' for k in (0.3, 1.0, 3.0)))
RES['A1c'] = A1c

# ---------------------------------------------------------------- A1 rule
lab = {}
for foot in ('canonical', 'alt'):
    rr_ = [r_ for r_ in ROWS if r_['footing'] == foot]
    reasons = []
    if xc[foot] > 1e-3: reasons.append('point mass not the law')
    for r_ in rr_:
        if r_['fails_negative']: reasons.append(f"{r_['profile']} {r_['logM']}: rho_c < 0")
        if r_['fails_rms']: reasons.append(f"{r_['profile']} {r_['logM']}: rms {r_['rms_dex']:.3f} > {r_['line']}")
    lab[foot] = dict(label=('STRUCTURE FAILS AT A1' if reasons else 'A1 HOLDS') if ka_ok else 'NO VERDICT (known answer)',
                     reasons=reasons)
RES['A1_label'] = lab
out('\nA1 label (reading L, as frozen):')
for foot in ('canonical', 'alt'):
    out(f'  {foot}: {lab[foot]["label"]}; ' + '; '.join(lab[foot]['reasons']))
out('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
open(os.path.join(HERE, 'set1_a1_num.out'), 'w').write('\n'.join(lines) + '\n')
json.dump(RES, open(os.path.join(HERE, 'set1_a1_num.json'), 'w'), indent=1)
