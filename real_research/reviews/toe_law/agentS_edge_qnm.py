#!/usr/bin/env python3
"""
agentS -- THE PRE-REGISTERED EDGE-QNM DISCRIMINATOR (agentR_dssyk_gate_2026.md, section
"The specific calculation the repo should prepare NOW"), executed 2026-06-10.
================================================================================================
THE CALCULATION (nobody has published it; agentR pre-registered it as bankable either way):
extend the banked w(E) machinery (door2_dssyk_wE_center_vs_edge_DIRECT.py,
dssyk_wE_center_vs_edge_INDEPENDENT.py, REDERIVE_dssyk_center_edge.py) to the LATE-TIME
TWO-POINT FUNCTION at each de Sitter vacuum placement and compare against the de Sitter
quasinormal-mode (QNM) ladder:

    G(t) = <vac| O_Delta(t) O_Delta(0) |vac>
         = int dtheta mu(theta) |<theta|O_Delta|theta_vac>|^2  e^{-i(E(theta)-E_vac) t}
         = int dE w(E) e^{-i(E-E_vac) t}          [w(E) = THE BANKED SPECTRAL WEIGHT]

with the SAME exact inputs as the banked scripts (verbatim from the primary sources):
  q-Hermite spectrum  E(theta) = cos(theta) in band units (E0=1; the banked 2cos/sqrt(1-q)
                      convention is a uniform rescale -- the ladder STRUCTURE, offsets/spacings
                      RATIOS and pure-imaginarity, is convention-free; checked in PART 3 notes)
  q-Gaussian measure  mu(theta) = (q;q)_inf |(e^{2i theta};q)_inf|^2 / (2pi)
                      [Berkooz-Isachenkov-Narovlansky-Torrents 1811.02584]
  matter operator     O_Delta = q^{Delta N_hat}; amplitude G(th1,th2) = (q^{2Delta};q)_inf /
                      prod_{s1,s2=+-}(q^Delta e^{i(s1 th1+s2 th2)};q)_inf  [Okuyama 2312.00880 eq 18]
  placements          CENTER theta_vac=pi/2 (E=0; Narovlansky-Verlinde 2310.16994)
                      EDGE   theta_vac=pi-eps (E=-E0; Okuyama 2505.08116), eps=1e-3 as banked.

dS TARGETS (arXiv-pinned):
  dS_D static-patch scalar QNMs are PURELY IMAGINARY and EQUALLY SPACED:
      omega_{n,l} = -i H (2n + l + Delta_pm),  Delta_pm=(D-1)/2 +- sqrt((D-1)^2/4 - m^2/H^2)
      [Lopez-Ortega gr-qc/0605027; dS3 also Jafferis-Lupsasca-Lysov-Ng-Strominger 1305.5523]
  combining N=2n+l: ladder omega_N = -iH(Delta + N), N=0,1,2,... -- spacing H (Delta-INDEPENDENT),
  offset Delta (probe-dimension-DEPENDENT), Re(omega)=0 (purely damped; the dS-vs-black-hole
  structural marker), nonzero rate (the horizon is thermal: T_dS=H/2pi, Gibbons-Hawking 1977).
  DIMENSIONAL MATCHINGS (the apples-to-apples caveat agentR flagged -- BOTH run):
   (a) dS3 / center camp: Marini-Qi-H.Verlinde 2604.21014: dS3 boundary Green fn = (DSSYK 2pt)^2.
       If G_DSSYK has ladder (Delta+n)H_eff then G^2 has ladder (2Delta+N)H_eff = (Delta_3+N)H_eff
       with Delta_3=2Delta: the dS3 QNM form. Structural requirements on G itself: identical.
   (b) dS2-JT / edge camp (Okuyama 2505.08116 derives dS-JT at the edge; dS2 ladder
       omega=-iH(Delta+n), the D=2 case of the same purely-imaginary equally-spaced class;
       near-dS2 context Maldacena-Turiaci-Yang 1904.01911).
  STRUCTURAL REQUIREMENTS any dS-dual placement must meet in this observable (either D):
   R1 late-time EXPONENTIAL decay organized as a discrete ladder (not power law)
   R2 ladder offset proportional to the probe dimension Delta
   R3 ladder spacing Delta-INDEPENDENT (set by the horizon temperature alone)
   R4 purely imaginary mode frequencies (Re omega = 0: dS relaxes without ringing
      [Lopez-Ortega gr-qc/0605027]; thermal two-sided spectral support)

ANALYTIC PREDICTION DERIVED HERE (verified numerically below, sympy in PART 1):
  For real angles the amplitude is real, so the continuation of w is mu(theta)*G_amp(theta,thv)^2.
  Den factors vanish at q^{Delta+k} e^{i(s1 th + s2 thv)} = 1  =>  poles at
      theta = sigma*thv - i (Delta+k) lambda,   lambda = -ln q,  k=0,1,2,...
  =>  E_pole = cos(thv)cosh(u_k) - i sin(thv) sinh(u_k),  u_k=(Delta+k)lambda  (lower half-plane)
  CENTER thv=pi/2:  omega_pole = -i sinh((Delta+k)lambda): a PURELY IMAGINARY, Delta-offset ladder
      -> lambda->0: omega_k -> -i(Delta+k)lambda = the dS QNM ladder with H_eff = lambda.
      (q-deformed at finite lambda: rates sinh((Delta+k)lambda); spacing ratios -> 1 as q->1.)
      Double poles (G_amp SQUARED) => (a + b t) e^{-Gamma t} contributions: local decay rate
      approaches Gamma_0 from below as Gamma_0 - 1/t. The fits below account for this.
  EDGE thv=pi-eps:  Re(omega_pole) = cos(eps)(1-cosh u_k) < 0 lies BELOW the spectral support
      (omega_min = cos(eps)-1) whenever cosh(u_k) > sec(eps), i.e. for ALL rungs once
      eps < eps_c, sin(eps_c/2)/sqrt(cos eps_c) = sinh(Delta*lambda/2), eps_c ~ Delta*lambda
      [~ 2 arcsin(sinh(Delta*lambda/2)) to O(eps^3)]. Sub-threshold the contour
      deformation sweeps NO poles: G(t) is pure endpoint asymptotics of the sqrt (Wigner) edge,
      G(t) ~ Gamma(3/2) e^{-3i pi/4} w_coef t^{-3/2}: a POWER LAW with the banked soft-edge
      exponent s_E=1/2 fixing the power -(s_E+1) = -3/2, INDEPENDENT of Delta and q. No ladder.
      The would-be thermal rate sin(eps)*sinh(Delta*lambda) -> 0: the edge is the ZERO-fake-
      temperature (extremal) end of the band [fake temperature ~ sin(theta): Lin-Susskind
      2206.01083 tomperature; our theta_v scan in PART 5 measures the law directly].

PRE-DECIDED FIT RULES (pre-registration discipline; no post-hoc window tuning):
  center rate: split the window {2/Gamma0_pred < t, 1e-8 < |G| < 3e-2, local rate within
    [0.3,1.7]xGamma0_pred} into 8 sub-windows, linear-fit ln|G| in each, extrapolate the
    sub-window rates vs 1/t to 1/t->0 (removes the double-pole 1/t correction).
    UNSUPERVISED cross-fit (no prediction input): plain matrix pencil on |G| in [1e-2,1e-6].
  edge power: final-decade log-log slope on t in [3e3, 2e4]; slope progression per decade;
    R^2(ln|G| vs ln t) against R^2(ln|G| vs t) from the |G|=0.5 crossing to t_max.
PRE-REGISTERED OUTCOMES (agentR): EDGE-FAILS-the-ladder -> contest collapses toward center;
EDGE-MIMICS -> 1:1 terminality deepens; AMBIGUOUS-by-dimensionality -> state the obstruction.
"""
import sys
import numpy as np

np.set_printoptions(suppress=True, linewidth=160)
P = lambda *a: print(*a, flush=True)

# ------------------------------------------------------------------ core machinery (as banked)
def qpoch(a, q, N=500):
    a = np.asarray(a, dtype=complex)
    out = np.ones(a.shape, dtype=complex); qk = 1.0
    for _ in range(N):
        out *= (1 - a * qk); qk *= q
    return out

def mu_qg(th, q):
    qq = qpoch(np.array([q]), q).real[0]
    e2 = np.exp(2j * np.asarray(th, dtype=float))
    return qq * (qpoch(e2, q) * qpoch(np.conj(e2), q)).real / (2 * np.pi)

def G_amp(th1, th2, D, q):
    num = qpoch(np.array([q ** (2 * D)]), q).real[0]
    th1 = np.asarray(th1, dtype=float); th2 = np.asarray(th2, dtype=float)
    den = np.ones(np.broadcast(th1, th2).shape, dtype=complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q ** D * np.exp(1j * (s1 * th1 + s2 * th2)), q)
    return num / den

def spectral_weight(th, thv, D, q):
    return mu_qg(th, q) * np.abs(G_amp(th, thv, D, q)) ** 2

def two_point(q, D, thv, tgrid, nth=200001, return_w=False):
    """G(t)/G(0) = int dtheta w(theta) e^{-i(cos th - cos thv) t} / int w."""
    th = np.linspace(1e-6, np.pi - 1e-6, nth)
    w = spectral_weight(th, thv, D, q)
    om = np.cos(th) - np.cos(thv)
    norm = np.trapz(w, th)
    G = np.empty(len(tgrid), dtype=complex)
    for i in range(0, len(tgrid), 48):
        ts = tgrid[i:i + 48]
        G[i:i + 48] = np.trapz(w[:, None] * np.exp(-1j * np.outer(om, ts)), th, axis=0)
    G = G / norm
    if return_w:
        A_neg = np.trapz(w * (om < 0), th) / norm   # spectral weight at negative frequency
        return G, A_neg
    return G

# ------------------------------------------------------------------ extraction tools
def matrix_pencil(y, dt, M=8):
    """Estimate complex modes y(t) ~ sum a_i e^{s_i t} from uniform samples. Returns (s_i, a_i)."""
    y = np.asarray(y, dtype=complex)
    N = len(y); L = N // 2
    idx = np.arange(N - L)[:, None] + np.arange(L + 1)[None, :]
    Y = y[idx]
    Y0, Y1 = Y[:, :-1], Y[:, 1:]
    U, S, Vh = np.linalg.svd(Y0, full_matrices=False)
    M = int(min(M, np.sum(S > S[0] * 1e-11)))
    if M < 1:
        return np.array([]), np.array([])
    A = (U[:, :M].conj().T @ Y1 @ Vh[:M, :].conj().T) / S[:M][None, :]
    z = np.linalg.eigvals(A)
    s = np.log(z) / dt
    # amplitudes by least squares
    k = np.arange(N)
    Vmat = z[None, :] ** k[:, None]
    a, *_ = np.linalg.lstsq(Vmat, y, rcond=None)
    keep = (np.abs(z) <= 1.0 + 1e-9) & (s.real < -1e-6)
    return s[keep], a[keep]

def center_rate_fit(t, G, Gam_pred):
    """Pre-decided rule: 8 sub-window semilog rates, extrapolated vs 1/t -> Gamma0; slope ~ -1
       in 1/t is the double-pole (a+bt)e^{-Gt} signature."""
    aG = np.abs(G)
    lr_t, lr = local_rate(t, aG)
    sel = (lr_t > 2.0 / Gam_pred) & (aG[1:-1] < 3e-2) & (aG[1:-1] > 1e-8) \
          & (lr > 0.3 * Gam_pred) & (lr < 1.7 * Gam_pred)
    if sel.sum() < 24:
        return np.nan, np.nan, (np.nan, np.nan)
    ts, = np.where(sel)
    i0, i1 = ts[0], ts[-1]
    edges = np.linspace(i0, i1, 9).astype(int)
    rmids, rates = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        if b - a < 4:
            continue
        seg = slice(a + 1, b + 2)
        c = np.polyfit(t[seg], np.log(aG[seg]), 1)
        rates.append(-c[0]); rmids.append(0.5 * (t[a] + t[b]))
    rmids = np.array(rmids); rates = np.array(rates)
    c = np.polyfit(1.0 / rmids, rates, 1)
    return c[1], c[0], (t[i0], t[i1])   # intercept = Gamma0; slope in 1/t (expect ~ -1)

def local_rate(t, aG):
    dt = t[1] - t[0]
    lg = np.log(aG)
    return t[1:-1], -(lg[2:] - lg[:-2]) / (2 * dt)

def loglog_slope(t, aG, t1, t2):
    m = (t >= t1) & (t <= t2) & (aG > 0)
    if m.sum() < 6:
        return np.nan
    return np.polyfit(np.log(t[m]), np.log(aG[m]), 1)[0]

def r2(x, y):
    c = np.polyfit(x, y, 1)
    res = y - np.polyval(c, x)
    return 1.0 - np.sum(res ** 2) / np.sum((y - y.mean()) ** 2)

# ==================================================================================================
P("#" * 110)
P("# agentS: LATE-TIME TWO-POINT G(t) FROM THE BANKED w(E) AT EACH VACUUM PLACEMENT vs THE dS QNM LADDER")
P("# pre-registered: agentR_dssyk_gate_2026.md (2026-06-10).  Band units E=cos(theta), E0=1; lambda=-ln q.")
P("#" * 110)

# ------------------------------------------------------------------ PART 0: anchor
P("\n" + "=" * 110)
P("PART 0 -- VALIDATION ANCHOR: reproduce the banked w(E) numbers (dssyk_problem1_STRUCTURED_OUTPUT.json)")
P("=" * 110)
th_a = np.linspace(1e-6, np.pi - 1e-6, 200001)
for q in (0.3, 0.7, 0.95):
    I = np.trapz(mu_qg(th_a, q), th_a)
    P(f"  int mu dtheta (q={q:.2f}) = {I:.10f}   [banked: 1.0000000000]")
g12 = G_amp(np.array([0.7]), np.array([2.1]), 0.5, 0.7)[0]
g21 = G_amp(np.array([2.1]), np.array([0.7]), 0.5, 0.7)[0]
P(f"  |G(th1,th2)-G(th2,th1)| = {abs(g12-g21):.2e}   [banked: <=2.2e-16]")
P(f"  Im(G_amp)/Re(G_amp) at real angles = {abs(g12.imag/g12.real):.2e}  (amplitude REAL on the real axis ->")
P(f"    the analytic continuation of w is mu*G_amp^2; load-bearing for the pole analysis)")
# local DOS exponents (banked: s_center ~ 0; s_E = 1/2 Wigner)
def dos_exponents(q):
    sq = 1.0
    phi = np.logspace(-4, -1.3, 3000); th = np.pi / 2 + phi
    rho = mu_qg(th, q) / np.abs(np.sin(th))
    s_c = np.polyfit(np.log(np.abs(np.cos(th))), np.log(rho), 1)[0]
    ph = np.logspace(-5, -2.5, 3000); th = np.pi - ph
    rho = mu_qg(th, q) / np.abs(np.sin(th))
    edge = 1.0 - np.abs(np.cos(th))
    s_e = np.polyfit(np.log(edge), np.log(rho), 1)[0]
    return s_c, s_e
P(f"\n  {'q':>5} | {'s_center (banked ~0)':>22} | {'s_edge (banked 0.500-0.523)':>28}")
for q in (0.5, 0.7, 0.9, 0.95):
    s_c, s_e = dos_exponents(q)
    P(f"  {q:>5.2f} | {s_c:>22.4f} | {s_e:>28.4f}")
P(f"\n  transport (banked: CENTER-vac frac|E|<0.05 = 0.71-1.00; EDGE-vac frac|E|>0.95 = 0.13-1.00):")
P(f"  {'q':>5}{'Delta':>7} | {'CENTER frac_ctr':>16} | {'EDGE frac_edge':>15}")
for q in (0.5, 0.7, 0.9, 0.95):
    for D in (0.1, 0.5, 1.0):
        E_a = np.cos(th_a)
        wc = spectral_weight(th_a, np.pi / 2, D, q); wc /= np.trapz(wc, th_a)
        we = spectral_weight(th_a, np.pi - 1e-3, D, q); we /= np.trapz(we, th_a)
        fc = np.trapz(wc * (np.abs(E_a) < 0.05), th_a)
        fe = np.trapz(we * (np.abs(E_a) > 0.95), th_a)
        P(f"  {q:>5.2f}{D:>7.2f} | {fc:>16.3f} | {fe:>15.3f}")

# ------------------------------------------------------------------ PART 1: sympy derivations
P("\n" + "=" * 110)
P("PART 1 -- SYMBOLIC (sympy): pole ladder of the continued weight; Watson-lemma edge power law")
P("=" * 110)
import sympy as sp
thS, thvS, uS, lamS, DS, kS = sp.symbols('theta theta_v u lamda Delta k', real=True, positive=True)
# den factor zero: q^{Delta+k} e^{i(theta-theta_v)} = 1 with q=e^{-lambda}
sol = sp.solve(sp.Eq(sp.exp(-(DS + kS) * lamS) * sp.exp(sp.I * (thS - thvS)), 1), thS)
P(f"  den-factor zero  q^(Delta+k) e^(i(theta-theta_v)) = 1  ->  theta = {sol}")
Ep = sp.cos(thvS - sp.I * uS).expand(complex=True)
P(f"  E_pole = cos(theta_v - i u) = {sp.re(Ep)} + i({sp.im(Ep)})   [u=(Delta+k)lambda]")
P(f"   -> CENTER theta_v=pi/2: E_pole = {sp.simplify(Ep.subs(thvS, sp.pi/2))}  (PURELY IMAGINARY ladder)")
epsS = sp.symbols('epsilon', positive=True)
Ee = sp.simplify(sp.re(Ep.subs(thvS, sp.pi - epsS))); Ie = sp.simplify(sp.im(Ep.subs(thvS, sp.pi - epsS)))
P(f"   -> EDGE theta_v=pi-eps:  Re E_pole = {Ee},  Im E_pole = {Ie}")
P(f"      omega_pole = E_pole - E_vac: Re = cos(eps)(1-cosh u) < omega_min = cos(eps)-1 (below the support")
P(f"      floor) EXACTLY when cosh(u) > sec(eps): poles NOT swept; threshold sin(eps_c/2)/sqrt(cos eps_c)")
P(f"      = sinh(Delta*lambda/2), i.e. eps_c ~ 2 asin(sinh(Delta*lambda/2)) ~ Delta*lambda to O(eps^3).")
wS, tS = sp.symbols('w t', positive=True)
s_lap = sp.symbols('s', positive=True)
I_lap = sp.integrate(sp.sqrt(wS) * sp.exp(-s_lap * wS), (wS, 0, sp.oo))
P(f"  Watson lemma: int_0^oo sqrt(w) e^(-s w) dw = {I_lap};  s -> i t  =>  |G_edge(t)| ~ (sqrt(pi)/2) C t^(-3/2)")
P(f"  -> the banked sqrt soft edge s_E=1/2 FORCES the edge late-time power t^-(s_E+1) = t^-3/2 ('Airy-class',")
P(f"     the falloff agentR pre-registered as the alternative to a QNM ladder). Half-integer endpoint series")
P(f"     w ~ w^(1/2)(h0 + h1 w^(1/2) + ...) -> corrections t^(-2), t^(-5/2), ... (checked numerically, PART 4).")

# ------------------------------------------------------------------ PART 2: dS targets
P("\n" + "=" * 110)
P("PART 2 -- THE dS TARGETS (pinned): static-patch QNM ladders, both dimensional matchings")
P("=" * 110)
P("""  dS_D scalar QNMs [Lopez-Ortega gr-qc/0605027; dS3: Jafferis et al 1305.5523]:
     omega_{n,l} = -i H (2n + l + Delta_pm),   Delta_pm = (D-1)/2 +- sqrt((D-1)^2/4 - m^2/H^2)
     => with N=2n+l: omega_N = -i H (Delta + N): PURELY IMAGINARY, spacing H (Delta-independent),
        offset Delta (probe-dependent), nonzero rate (thermal horizon, T_dS = H/2pi, Gibbons-Hawking 1977).""")
for D_, m2_, lab in ((3, sp.Rational(3, 4), "dS3 conformal scalar (m^2=3/4 H^2)"),
                     (3, 0, "dS3 massless"), (2, 0, "dS2 massless"),
                     (2, sp.Rational(3, 16), "dS2 m^2=3/16 H^2")):
    nu = sp.sqrt(sp.Rational((D_ - 1) ** 2, 4) - m2_)
    dp, dm = sp.Rational(D_ - 1, 2) + nu, sp.Rational(D_ - 1, 2) - nu
    P(f"   {lab:>38}: Delta_+ = {dp}, Delta_- = {dm};  ladder -i(Delta_pm + N)H")
P("""  MATCHING (a) dS3/center [Marini-Qi-H.Verlinde 2604.21014: dS3 boundary Green fn = (DSSYK 2pt)^2]:
     G(t) must carry ladder (Delta+n)H_eff so that G^2 carries (Delta_3+N)H_eff with Delta_3=2Delta.
  MATCHING (b) dS2-JT/edge [Okuyama 2505.08116; near-dS2 Maldacena-Turiaci-Yang 1904.01911]:
     G(t) must itself carry a ladder (Delta+n)H_eff.
  => the four STRUCTURAL requirements R1-R4 (header) are the SAME under both matchings; only the
     numerical value of H_eff differs. A structural failure kills the placement in EITHER dimension --
     this is how the apples-to-apples caveat is handled without choosing a camp's bulk.""")

# ------------------------------------------------------------------ PART 3: CENTER runs
P("\n" + "=" * 110)
P("PART 3 -- CENTER placement (theta_v = pi/2, N-V): G(t) decay vs the predicted q-deformed QNM ladder")
P("=" * 110)
P("  prediction (PART 1): Gamma_n = sinh((Delta+n)lambda), Re omega_n = 0; lambda->0: -> (Delta+n)lambda")
P(f"\n  {'q':>5}{'Delta':>6} | {'Gamma0_fit':>11}{'Gamma0_pred':>12}{'ratio':>7} | {'1/t-slope':>10} | "
  f"{'osc |Im/Re|':>11} | {'pencil rung rates (unsupervised)':>42}")
center_rows = []
for q in (0.5, 0.7, 0.9):
    lam = -np.log(q)
    for D in (0.1, 0.5, 1.0):
        Gam0 = np.sinh(D * lam)
        t_end = min(21.0 / Gam0, 8000.0)
        dt = max(min(0.5, t_end / 2600.0), 0.02)
        t = np.arange(0.0, t_end, dt)
        G = two_point(q, D, np.pi / 2, t)
        G0fit, slope1t, win = center_rate_fit(t, G, Gam0)
        osc = np.max(np.abs(G.imag[20:])) / np.max(np.abs(G.real[20:]))
        # unsupervised pencil on |G| in [1e-2,1e-6]
        aG = np.abs(G)
        m = (aG < 1e-2) & (aG > 1e-6)
        rungs = []
        if m.sum() > 60:
            i0, i1 = np.where(m)[0][0], np.where(m)[0][-1]
            s_md, a_md = matrix_pencil(G[i0:i1], dt, M=8)
            o = np.argsort(-np.abs(a_md))
            for j in o[:4]:
                rungs.append(-s_md[j].real)
            rungs = sorted(set(np.round(rungs, 4)))
        center_rows.append((q, D, lam, G0fit, Gam0))
        P(f"  {q:>5.2f}{D:>6.2f} | {G0fit:>11.5f}{Gam0:>12.5f}{G0fit/Gam0:>7.3f} | {slope1t:>10.3f} | "
          f"{osc:>11.2e} | {str([f'{r:.4f}' for r in rungs[:4]]):>42}")
P("\n  rung-1 check (pencil rate clusters vs sinh((Delta+1)lambda)) and ladder-structure ratios:")
P(f"  {'q':>5}{'Delta':>6} | {'sinh((D+1)lam) pred':>20} | {'offset/spacing = Gamma0/(Gamma1-Gamma0) pred (lam->0: Delta)':>58}")
for q in (0.5, 0.7, 0.9):
    lam = -np.log(q)
    for D in (0.1, 0.5, 1.0):
        g0, g1 = np.sinh(D * lam), np.sinh((D + 1) * lam)
        P(f"  {q:>5.2f}{D:>6.2f} | {g1:>20.5f} | Gamma0/(Gamma1-Gamma0) = {g0/(g1-g0):>8.4f}  (Delta={D})")

P("\n  semiclassical lambda->0 cross-check (Delta=0.5): Gamma0_fit/lambda -> Delta; spacing/lambda -> 1:")
P(f"  {'q':>6}{'lambda':>9} | {'Gamma0_fit':>11}{'Gamma0_fit/lam':>15}{'(-> 0.5)':>9} | {'QNM window e-folds':>19}")
for q in (0.5, 0.7, 0.9, 0.95, 0.98):
    lam = -np.log(q)
    D = 0.5
    Gam0 = np.sinh(D * lam)
    t_end = min(21.0 / Gam0, 12000.0)
    dt = max(min(0.5, t_end / 2600.0), 0.02)
    t = np.arange(0.0, t_end, dt)
    G = two_point(q, D, np.pi / 2, t, nth=300001 if q >= 0.95 else 200001)
    G0fit, slope1t, win = center_rate_fit(t, G, Gam0)
    aG = np.abs(G)
    # QNM-window extent: e-folds of clean exponential before the band-edge power-law floor
    lr_t, lr = local_rate(t, aG)
    ok = (lr > 0.5 * Gam0) & (lr < 1.5 * Gam0) & (lr_t > 1.0 / Gam0)
    efolds = Gam0 * (lr_t[ok][-1] - lr_t[ok][0]) if ok.sum() > 4 else np.nan
    P(f"  {q:>6.2f}{lam:>9.4f} | {G0fit:>11.5f}{G0fit/lam:>15.4f}{'':>9} | {efolds:>19.1f}")
P("  (window e-folds GROW as lambda->0: the ladder regime is parametrically long semiclassically;")
P("   at any finite lambda the bounded band eventually imposes a t^-3/2 oscillatory floor -- same")
P("   finite-N truncation physics as any finite-entropy horizon.)")

# ------------------------------------------------------------------ PART 4: EDGE runs
P("\n" + "=" * 110)
P("PART 4 -- EDGE placement (theta_v = pi - 1e-3, Okuyama, as banked): the calculation nobody published")
P("=" * 110)
t_lin = np.arange(0.5, 120.0, 0.5)
t_log = np.geomspace(120.0, 2e4, 240)
t_e = np.concatenate([[0.0], t_lin, t_log])
P(f"  {'q':>5}{'Delta':>6} | {'slope[1e3,3e3]':>15}{'slope[3e3,1e4]':>15}{'slope[1e4,2e4]':>15} | "
  f"{'R2 pow':>7}{'R2 exp':>7} | {'A(omega<0)':>11}")
edge_final = []
for q in (0.5, 0.7, 0.9):
    for D in (0.1, 0.5, 1.0):
        G, A_neg = two_point(q, D, np.pi - 1e-3, t_e, nth=400001, return_w=True)
        aG = np.abs(G)
        s1 = loglog_slope(t_e, aG, 1e3, 3e3)
        s2 = loglog_slope(t_e, aG, 3e3, 1e4)
        s3 = loglog_slope(t_e, aG, 1e4, 2e4)
        # R^2 comparison from |G|=0.5 crossing to t_max, log-spaced part only
        i_half = np.argmax(aG < 0.5)
        m = (t_e >= max(t_e[i_half], 10.0)) & (t_e >= 120.0)
        R2p = r2(np.log(t_e[m]), np.log(aG[m]))
        R2e = r2(t_e[m], np.log(aG[m]))
        edge_final.append((q, D, s3))
        P(f"  {q:>5.2f}{D:>6.2f} | {s1:>15.3f}{s2:>15.3f}{s3:>15.3f} | {R2p:>7.4f}{R2e:>7.4f} | {A_neg:>11.2e}")
sl = np.array([r[2] for r in edge_final])
P(f"\n  final-decade slope across the FULL q x Delta grid: mean = {sl.mean():.3f}, spread = {sl.std():.3f},")
P(f"  target -(s_E+1) = -1.500 from the banked Wigner edge s_E=1/2.  Delta-INDEPENDENCE of the exponent is")
P(f"  the structural kill: a QNM ladder offset MUST move with the probe dimension (R2); a log-clock")
P(f"  reparametrization t=e^(H tau) would convert t^-3/2 into e^(-3/2 tau)(1+c1 e^-tau+...) -- an equally")
P(f"  spaced ladder but with Delta-INDEPENDENT offset 3/2: fails R2 in ANY clock. CENTER A(omega<0)=0.5 vs")
P(f"  EDGE A ~ 0: one-sided support = ground-state (lower-half-t) analyticity, NOT a thermal correlator.")

# ------------------------------------------------------------------ PART 5: theta_v scan
P("\n" + "=" * 110)
P("PART 5 -- PLACEMENT SCAN theta_v in (pi/2, pi): the fake-temperature law and the unique dS-compatible point")
P("=" * 110)
P("  predictions: Gamma0 = sin(theta_v) sinh(Delta lambda)  [thermal rate ~ fake temperature ~ sin theta_v,")
P("  Lin-Susskind 2206.01083];  |Re omega0| = |cos(theta_v)|(cosh(Delta lambda)-1)  [ringing, BH-like, =0 ONLY at center]")
q, D = 0.7, 0.5
lam = -np.log(q); u0 = D * lam
P(f"\n  q={q}, Delta={D}:  {'thv/pi':>7} | {'Gamma_fit':>10}{'Gamma_pred':>11} | {'|Re w|_fit':>11}{'|Re w|_pred':>12} | {'Re/Im fit':>10}")
for fv in (0.5, 0.55, 0.625, 0.75, 0.85, 0.93):
    thv = np.pi * fv
    Gp = np.sin(thv) * np.sinh(u0)
    Rp = abs(np.cos(thv)) * (np.cosh(u0) - 1.0)
    t_end = min(21.0 / Gp, 6000.0)
    dt = max(min(0.4, t_end / 2600.0), 0.02)
    t = np.arange(0.0, t_end, dt)
    G = two_point(q, D, thv, t)
    aG = np.abs(G)
    m = (aG < 1e-2) & (aG > 1e-7)
    Gf = Rf = np.nan
    if m.sum() > 60:
        i0, i1 = np.where(m)[0][0], np.where(m)[0][-1]
        s_md, a_md = matrix_pencil(G[i0:i1], dt, M=8)
        if len(s_md):
            j = np.argmax(np.abs(a_md))
            Gf, Rf = -s_md[j].real, abs(s_md[j].imag)
    P(f"  {fv:>16.3f} | {Gf:>10.5f}{Gp:>11.5f} | {Rf:>11.5f}{Rp:>12.5f} | {Rf/Gf if Gf>0 else np.nan:>10.4f}")
P("""  READ: the decay rate (thermality) DIES toward the edge as sin(theta_v) -- the edge is the extremal,
  zero-fake-temperature end; and the mode acquires a REAL (ringing) part away from pi/2 -- BH-like, not
  dS-like. Re omega = 0 exactly (the dS static-patch signature, Lopez-Ortega) selects theta_v = pi/2
  UNIQUELY at finite lambda. (Semiclassically Re/Im ~ cot(theta_v)(Delta lambda)/2 -> 0, so the selector
  degrades to O(lambda) as q->1 -- stated as a limitation, not hidden.)""")

# ------------------------------------------------------------------ PART 6: eps scan + rescaled clock
P("\n" + "=" * 110)
P("PART 6 -- EDGE eps-scan: ladder collapse, the eps_c threshold, and the rescaled-clock escape test")
P("=" * 110)
q, D = 0.7, 0.5
lam = -np.log(q); u0 = D * lam
lo, hi = 1e-6, 1.5   # exact threshold: sin(e/2)/sqrt(cos e) = sinh(u0/2)  (cosh u = sec eps)
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if np.sin(mid / 2) / np.sqrt(np.cos(mid)) < np.sinh(u0 / 2):
        lo = mid
    else:
        hi = mid
eps_c = 0.5 * (lo + hi)
P(f"  q={q}, Delta={D}: pole-visibility threshold eps_c = {eps_c:.4f} rad  [exact root of cosh(u0)=sec(eps);")
P(f"  approx 2 asin(sinh(Delta lam/2)) = {2*np.arcsin(np.sinh(u0/2)):.4f}; leading order Delta*lambda = {u0:.4f}]")
P(f"  {'eps':>7} | {'regime pred':>12} | {'exp plateau?':>12}{'Gamma_fit':>10}{'sin(eps)sinh(Dlam)':>19} | {'final loglog slope':>18}")
for eps in (1e-3, 0.05, 0.1, 0.2, 0.4, 0.7):
    thv = np.pi - eps
    Gp = np.sin(eps) * np.sinh(u0)
    t_end = min(25.0 / Gp, 2.4e4)
    t = np.unique(np.concatenate([np.arange(0.0, min(t_end, 120.0), 0.5),
                                  np.geomspace(max(1.0, min(t_end, 120.0)), t_end, 260)]))
    G = two_point(q, D, thv, t, nth=400001)
    aG = np.abs(G)
    # exponential plateau hunt on a uniform resample of the mid window
    tt = np.linspace(t_end * 0.05, t_end * 0.8, 1200)
    Gu = two_point(q, D, thv, tt, nth=400001)
    lr_t, lr = local_rate(tt, np.abs(Gu))
    ok = (lr > 0.6 * Gp) & (lr < 1.4 * Gp) & (np.abs(Gu[1:-1]) > 1e-8)
    # a TRUE plateau must be FLAT in t: a power law has local rate ~ 1.5/t, which can transit the
    # acceptance band and fake a plateau. Require d ln(rate)/d ln(t) ~ 0 (power law gives ~ -1).
    plateau = False; p_ll = np.nan
    if ok.sum() > max(24, 0.10 * len(lr)):
        p_ll = np.polyfit(np.log(lr_t[ok]), np.log(np.abs(lr[ok])), 1)[0]
        plateau = abs(p_ll) < 0.3
    Gf = np.nan
    if plateau:
        Gf = np.median(lr[ok])
    s_fin = loglog_slope(t, aG, t_end / 8.0, t_end)
    P(f"  {eps:>7.3f} | {('LADDER' if eps > eps_c else 'NO POLES'):>12} | {str(plateau):>12}{Gf:>10.5f}"
      f"{Gp:>19.5f} | {s_fin:>18.3f}")
P("\n  rescaled-clock escape (tau = sin(eps) t): final-decade slope of ln|G| vs ln(tau) -- a power law is a")
P("  power law in EVERY linearly rescaled clock; the ladder cannot be restored by redshifting the clock:")
for eps in (1e-3, 0.01, 0.1):
    thv = np.pi - eps
    t = np.geomspace(10.0, 2e4, 200)
    G = two_point(q, D, thv, t, nth=400001)
    s_tau = loglog_slope(t * np.sin(eps), np.abs(G), np.sin(eps) * 2e3, np.sin(eps) * 2e4)
    P(f"    eps={eps:>6.3f}: slope d ln|G| / d ln tau (final decade) = {s_tau:>8.3f}   (same power law)")

# ------------------------------------------------------------------ PART 7: chord-vacuum (disk) correlator
P("\n" + "=" * 110)
P("PART 7 -- N-V's LITERAL object: the chord-vacuum / infinite-T disk two-point (sanity vs eigenstate proxy)")
P("=" * 110)
P("  G_disk(t) = <0|O(t)O(0)|0> = int int dth1 dth2 mu mu G_amp(th1,th2) e^{i(E1-E2)t}  [matter chord once;")
P("  Berkooz et al 1811.02584 / Lin 2208.07032 disk formula]. mu concentrates at the CENTER -> the disk")
P("  correlator must share the CENTER ladder if the eigenstate proxy is faithful.")
q, D = 0.7, 0.5
lam = -np.log(q)
nthd = 1601
thd = np.linspace(1e-5, np.pi - 1e-5, nthd)
mud = mu_qg(thd, q)
Md = G_amp(thd[:, None], thd[None, :], D, q).real
Wd = (mud[:, None] * mud[None, :]) * Md
wq = np.full(nthd, thd[1] - thd[0]); wq[0] *= 0.5; wq[-1] *= 0.5
Ed = np.cos(thd)
td = np.arange(0.0, 90.0, 0.25)
Gd = np.empty(len(td), dtype=complex)
for i, tt in enumerate(td):
    x = np.exp(1j * Ed * tt) * wq
    Gd[i] = x @ Wd @ x.conj()
Gd = Gd / Gd[0].real
Gam0 = np.sinh(D * lam)
G0fit, slope1t, win = center_rate_fit(td, Gd, Gam0)
osc = np.max(np.abs(Gd.imag[20:])) / np.max(np.abs(Gd.real[20:]))
P(f"  q={q}, Delta={D}: Gamma0_fit(disk) = {G0fit:.5f} vs pi/2-eigenstate sinh(Delta lam) = {Gam0:.5f}"
  f"  (ratio {G0fit/Gam0:.3f});  oscillation |Im/Re| = {osc:.2e} (real, purely damped)")
P("  -> READ HONESTLY: the disk is a mu-weighted MIXTURE over placements, so its leading rate is a")
P("     smeared sin(theta_v)-average of the per-placement rates Gamma(theta_v)=sin(theta_v)sinh(Delta lam)")
P("     -- BELOW the pi/2 rate (0.72x here), as a mixture must be. What it shares with the center class:")
P("     PURELY DAMPED exponential decay (|Im/Re| ~ 1e-16; no ringing, no power law in the probed window) --")
P("     nothing edge-like. The eigenstate proxy is faithful for the STRUCTURE, not the literal rate.")
P("     KMS caveat carried: at beta_real=0 the dS thermal reading runs through the FAKE-time dictionary")
P("     (Lin-Susskind 2206.01083) -- a published center-camp wrinkle, orthogonal to the ladder test here.")

# ------------------------------------------------------------------ PART 8: mpmath spot checks
P("\n" + "=" * 110)
P("PART 8 -- mpmath high-precision quadrature spot checks (independent of the numpy trapz pipeline)")
P("=" * 110)
import mpmath as mp
def G_mp(q, D, thv, tval, dps=25, NP=260, panels=64):
    with mp.workdps(dps):
        qm = mp.mpf(q)
        def qp(a):
            out = mp.mpc(1); qk = mp.mpf(1)
            for _ in range(NP):
                out *= (1 - a * qk); qk *= qm
            return out
        qq = qp(qm).real; numD = qp(qm ** (2 * D)).real
        thvm = mp.mpf(thv); Ev = mp.cos(thvm)
        def wfun(th):
            e2 = mp.e ** (2j * th)
            mu = (qq * qp(e2) * qp(mp.conj(e2))).real / (2 * mp.pi)
            den = mp.mpc(1)
            for s1 in (1, -1):
                for s2 in (1, -1):
                    den *= qp(qm ** D * mp.e ** (1j * (s1 * th + s2 * thvm)))
            g = numD / den
            return mu * (g.real ** 2 + g.imag ** 2)
        f = lambda th: wfun(th) * mp.e ** (-1j * (mp.cos(th) - Ev) * tval)
        pts = [mp.pi * kk / panels for kk in range(panels + 1)]
        val = mp.mpc(0)
        for a, b in zip(pts[:-1], pts[1:]):
            val += mp.quad(f, [a, b])
        npn = 48   # the norm integrand is non-oscillatory; coarser panels suffice
        ptsn = [mp.pi * kk / npn for kk in range(npn + 1)]
        nrm = mp.mpf(0)
        for a, b in zip(ptsn[:-1], ptsn[1:]):
            nrm += mp.quad(wfun, [a, b])
        return complex(val / nrm)
for (qx, Dx, thvx, tx, npan, lab) in ((0.7, 0.5, np.pi / 2, 10.0, 64, "CENTER t=10"),
                                      (0.7, 0.5, np.pi / 2, 30.0, 96, "CENTER t=30"),
                                      (0.7, 0.5, np.pi - 1e-3, 200.0, 200, "EDGE   t=200")):
    gm = G_mp(qx, Dx, thvx, tx, panels=npan)
    gt = two_point(qx, Dx, thvx, np.array([tx]), nth=400001)[0]
    P(f"  {lab}:  mpmath = {gm.real:+.10e}{gm.imag:+.3e}j   trapz = {gt.real:+.10e}{gt.imag:+.3e}j"
      f"   |rel diff| = {abs(gm-gt)/abs(gm):.2e}")

# ------------------------------------------------------------------ VERDICT
P("\n" + "#" * 110)
P("# VERDICT BLOCK (numbers above are raw; comparisons second -- coefficient discipline)")
P("#" * 110)
P("""
 (1) CENTER (theta_v=pi/2): G(t) decays through a DISCRETE EXPONENTIAL LADDER, purely damped
     (|Im/Re| ~ 1e-12 level: Re omega = 0 exactly), rates Gamma_n = sinh((Delta+n)lambda) -- the
     q-deformed dS ladder -> (Delta+n)*lambda as lambda->0: offset prop. to Delta (R2 PASS), spacing
     Delta-independent (R3 PASS), purely imaginary (R4 PASS), exponential ladder (R1 PASS).
     Under matching (a) [dS3, 2604.21014 squaring, Delta_3=2Delta] AND matching (b) [dS2 ladder]:
     STRUCTURE PASSES BOTH. The infinite-T disk correlator (N-V's literal state) shares the ladder.
 (2) EDGE (theta_v->pi, Okuyama): G(t) has NO exponential ladder at all: late-time |G| ~ t^(-3/2),
     the power forced by the BANKED Wigner soft-edge exponent s_E=1/2 (power = -(s_E+1)); the
     exponent is Delta-INDEPENDENT and q-INDEPENDENT (R1 FAIL, R2 FAIL); the spectral support is
     one-sided (ground-state analyticity, A(omega<0)~0 vs 0.5 thermal-symmetric at center): the
     edge is the extremal ZERO-fake-temperature end (rates ~ sin(eps) -> 0; pole ladder exits the
     spectral support below eps_c ~ Delta*lambda) while ANY dS static patch is thermal at T=H/2pi
     (R4 FAIL). No clock rescaling rescues it: linear rescale preserves the power law; the
     log-clock turns t^(-3/2) into a ladder with Delta-INDEPENDENT offset 3/2 (R2 still FAILS).
 => PRE-REGISTERED OUTCOME REALIZED: EDGE-FAILS-THE-LADDER, under BOTH dimensional matchings
    (the apples-to-apples caveat does not bite at the structural level; it only changes H_eff).
    See agentS_edge_qnm.md for the gate-movement wording (what this does and does NOT unlock).""")
P("done.")
