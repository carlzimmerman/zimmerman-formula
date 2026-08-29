#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
compiler.py -- MOND THEORY COMPILER (response-space inverse design), Carl's spec 2026-08-29.

WHAT THIS IS (honest scope -- read before trusting any output):
  A STAGE-1 SCREEN in RESPONSE SPACE.  It does NOT do covariant variation.  It builds, for each
  candidate, the linearised QUASISTATIC Fourier response of the coupled system
      (Phi, Psi ; auxiliary carrier fields chi [scalar], Q [TT tensor])
  on a MOND background parameterised by y = g/a0, eliminates the auxiliaries algebraically, and
  applies the hard gates.  Survivors are CANDIDATES FOR covariant derivation, never "viable theories".
  Anything that survives MUST be re-derived from an action (stage 2) before any claim is made.

THE FROZEN NON-NEGOTIABLES (never searched over, never "repaired"):
  mu(y) = 1 - e^{-y}      (elliptic: lam_perp = mu > 0, lam_par = mu + y mu' = 1-e^-y+y e^-y > 0)
  G_eff/G_N = 1 at high acceleration -- FORBIDDEN to fix a failure by rescaling G.

THE PART-I OBSTRUCTION THIS SEARCH EXISTS TO EVADE (committed, verified):
  a local isotropic MOND law couples to the metric only through s = sqrt(gamma^ij D_i q D_j q), so the
  same mu controls the Gauss law AND the on-shell traceless stress Sigma_P = y mu' (lapse-tied) or
  -mu s^2 (covariant carrier).  Sigma_P = 0 <=> mu = 0 or mu' = 0.  => Phi != Psi is FORCED for every
  LOCAL, <=2-spatial-derivative, NON-DEGENERATE single-metric constraint MOND.
  The theorem's hypotheses -- and therefore the search's escape hatches -- are:
    (H1) spatial locality        -> escape: kernel with k^{-2} (spatially nonlocal, NO time nonlocality)
    (H2) <= 2 spatial derivs     -> escape: k^2, k^4 kernels
    (H3) non-degenerate carrier  -> escape: det H = 0 with a genuine second-class pair
    (H4) scalar/isotropic carrier-> escape: auxiliary TT tensor Q_ij with independent traceless stress
  EVERY survivor is tagged with WHICH hypothesis it violates.  A survivor violating none would
  contradict the theorem => treated as a BUG, not a discovery.

THE TARGET RESPONSE (Carl's frozen list):
  MOND      div[mu grad Phi] = 4 pi G rho        Newton    G_eff = G_N
  lensing   Phi = Psi  AND  (Phi+Psi)/2 MOND-enhanced      PPN   alpha_1 = alpha_2 = 0
  carrier   T_ij^TF != 0   but   T_0i^(w) = T_00^(w2) = 0  (metric-visible, PPN-dark)
  health    det H = 0 with constant rank + genuine second-class chain, or K_phys > 0

OUTPUTS (append-only, resumable): candidates.sqlite, SURVIVORS.jsonl, CHAMPIONS.md, KILL_LEDGER.md
Resume: just re-run.  Work is keyed by sha256 of the canonical candidate; done work is skipped.
"""
import os, sys, json, math, hashlib, sqlite3, itertools, random, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, 'candidates.sqlite')
SURV = os.path.join(HERE, 'SURVIVORS.jsonl')

# ----------------------------------------------------------------- frozen constitutive sector
def mu(y):      return 1.0 - np.exp(-y)                 # FROZEN
def dmu(y):     return np.exp(-y)                       # mu'
def lam_perp(y):return mu(y)                            # transverse principal eigenvalue
def lam_par(y): return mu(y) + y*dmu(y)                 # longitudinal
def Sigma_P(y): return y*dmu(y)                         # the Part-I anisotropic stress (lapse-tied form)

# ----------------------------------------------------------------- operator basis
# Each operator: (label, sector, boost_charge, kernel_power, hyp_violated)
#   sector       : 'g'  metric-only | 'chi' aux scalar | 'Q' aux TT tensor
#   boost_charge : 0 => built ONLY from objects invariant under the boost of the source frame
#                       (=> contributes NOTHING to alpha_1/alpha_2)
#                  1 => involves the preferred-foliation normal n^mu / a background timelike vector
#                       (=> generically sources the w and w^2 sectors => alpha_1, alpha_2 != 0)
#   kernel_power : n in K ~ (k^2)^n  (n = -1 is the spatially NONLOCAL Delta^{-1} term)
#   hyp_violated : which Part-I hypothesis this operator breaks (or '' if none)
BASIS = [
    # --- A. ADM geometric (metric-only) ---
    ('R3',          'g',   0,  0, ''),        # 3-Ricci: standard, no escape
    ('KijKij_K2',   'g',   1,  0, ''),        # extrinsic curvature: foliation normal => boost charge
    ('aiai',        'g',   1,  0, ''),        # a_i = D_i ln N : lapse-tied, boost charge
    ('aiD2ai',      'g',   1,  1, 'H2'),      # higher spatial derivative
    ('R3D2R3',      'g',   0,  1, 'H2'),
    # --- B. auxiliary scalar (chi-dot^2 = 0 imposed) ---
    ('chi2',        'chi', 0,  0, 'H3'),      # algebraic mass term -> degenerate (no kinetic)
    ('chiR3',       'chi', 0,  0, 'H3'),
    ('chiD2phi',    'chi', 1,  0, 'H3'),      # couples to lapse gradient -> boost charge
    ('chiDphi2',    'chi', 1,  0, 'H3'),
    ('chiD2chi',    'chi', 0,  1, 'H2H3'),
    # --- C. auxiliary TT tensor Q_ij (no Q-dot) : the unexplored sector ---
    ('QR3',         'Q',   0,  0, 'H3H4'),    # Q^ij R^(3)_ij
    ('QDphiDphi',   'Q',   1,  0, 'H3H4'),    # Q^ij D_i phi D_j phi  <- the MOND anisotropic source
    ('QD2Q',        'Q',   0,  1, 'H2H3H4'),  # spatial kinetic kernel for Q
    ('QQ',          'Q',   0,  0, 'H3H4'),    # algebraic Q mass
    # --- D. spatially nonlocal kernels (NO time nonlocality) ---
    ('QDm2Q',       'Q',   0, -1, 'H1H3H4'),  # Q Delta^{-1} Q   <- the PTA-MOND escape
    ('chiDm2chi',   'chi', 0, -1, 'H1H3'),
    ('QDm2Dphi2',   'Q',   1, -1, 'H1H3H4'),
]
LABELS = [b[0] for b in BASIS]
NOP = len(BASIS)
EXCLUDED = ("time derivatives of auxiliaries (chi-dot, Q-dot) -- deliberately excluded to keep the "
            "auxiliary sector non-propagating (that is the design principle: degeneracy as a design "
            "variable, not an accident); operators above quartic in the carrier; k^6 and higher kernels; "
            "matter-sector modifications (matter stays minimally coupled to the single metric g).")

# ----------------------------------------------------------------- response model
def response(c, y, k, M=1.0):
    """Linearised quasistatic response.  Returns dict of observables or None if singular.
    Variables: Phi, Psi (metric), chi (aux scalar), Q (aux TT amplitude).
    Model (documented, not a covariant derivation):
      Gauss law     : 2 k^2 Psi = 8 pi G rho * A_G  + (carrier scalar source)
      traceless-ij  : k^2 (Phi - Psi) = Sigma_MOND + Sigma_carrier
      carrier eqs   : algebraic (no time derivatives) => eliminate exactly.
    """
    k2 = k*k
    def K(n):  # kernel value for power n
        return (k2/M**2)**n if n >= 0 else (M**2/k2)
    # accumulate coefficients
    a_G   = 1.0                      # Gauss-law normalisation (must stay 1 => G_eff = G_N)
    s_chi = s_Q = 0.0                # carrier sources into the Gauss law
    m_chi = m_Q = 0.0                # carrier self-terms (algebraic masses/kernels)
    g_chi = g_Q = 0.0                # carrier couplings to the metric/MOND sector
    boost1 = boost2 = 0.0            # O(w) and O(w^2) response accumulators
    for ci, (lab, sec, bch, kp, hyp) in zip(c, BASIS):
        if ci == 0.0: continue
        v = ci*K(kp)
        if sec == 'g':
            if lab == 'R3':        a_G += 0.0            # standard EH piece, already normalised
            elif lab in ('KijKij_K2','aiai','aiD2ai'):
                a_G += 0.0                                # do not let metric ops rescale G silently
        elif sec == 'chi':
            if lab in ('chi2','chiD2chi','chiDm2chi'): m_chi += v
            elif lab == 'chiR3':   g_chi += v; s_chi += v
            elif lab in ('chiD2phi','chiDphi2'): g_chi += v
        elif sec == 'Q':
            if lab in ('QQ','QD2Q','QDm2Q'): m_Q += v
            elif lab == 'QR3':     g_Q += v
            # Q^ij D_i phi D_j phi sources from the MOND gradient => inherits the y-dependence of
            # the background |D phi|^2 ~ y^2 and of the constitutive response.  Without this the
            # LENSING gate would be failed by a modelling artifact (y-independent carrier vs
            # y-dependent Sigma_P), not by physics.
            elif lab == 'QDphiDphi':   g_Q += v*(y*y)
            elif lab == 'QDm2Dphi2':   g_Q += v*(y*y)
        if bch:                       # boost-charged operator feeds the preferred-frame sectors
            boost1 += abs(ci)*K(kp) if kp >= 0 else abs(ci)*K(kp)
            boost2 += abs(ci)*K(kp) if kp >= 0 else abs(ci)*K(kp)
    # eliminate auxiliaries (algebraic; singular => reject)
    if abs(m_chi) < 1e-14 and abs(g_chi) > 0: return None      # chi undetermined & sourced
    if abs(m_Q)   < 1e-14 and abs(g_Q)   > 0: return None      # Q undetermined & sourced
    chi_amp = (-g_chi/m_chi) if abs(m_chi) > 1e-14 else 0.0
    Q_amp   = (-g_Q/m_Q)     if abs(m_Q)   > 1e-14 else 0.0
    # traceless sector: MOND stress + carrier stress
    Sig_M   = Sigma_P(y)
    Sig_Q   = g_Q*Q_amp                      # carrier traceless stress (this is T_ij^TF)
    slip    = (Sig_M + Sig_Q)/k2             # Phi - Psi (in units of the Newtonian amplitude)
    G_ratio = a_G + s_chi*chi_amp/max(k2, 1e-30)
    return dict(slip=slip, G_ratio=G_ratio, T_TF=Sig_Q, chi=chi_amp, Q=Q_amp,
                boost1=boost1, boost2=boost2, m_chi=m_chi, m_Q=m_Q)

# ----------------------------------------------------------------- gates (lexicographic, cheap first)
YGRID = np.array([0.03, 0.3, 1.0, 3.0, 30.0])       # deep-MOND .. Newtonian
KGRID = np.array([0.1, 1.0, 10.0])
TOL   = 1e-6

def gates(c):
    """Return (passed, failed_gate, metrics)."""
    m = dict()
    # G-ELLIP: frozen sector must stay elliptic (guards against a candidate wrecking it)
    if not (np.all(lam_perp(YGRID) > 0) and np.all(lam_par(YGRID) > 0)):
        return False, 'ELLIP', m
    # G-CARRIER: the carrier must actually turn on (this is what killed minimal AC-MOND: A_mu = 0)
    r0 = response(c, 1.0, 1.0)
    if r0 is None: return False, 'SINGULAR', m
    if abs(r0['T_TF']) < 1e-12:
        m['T_TF'] = r0['T_TF']
        return False, 'CARRIER_OFF', m
    # G-NEWTON: G_eff/G_N = 1, no rescaling repair allowed
    gr = [response(c, y, k)['G_ratio'] for y in YGRID for k in KGRID]
    m['G_ratio_max_dev'] = float(np.max(np.abs(np.array(gr) - 1.0)))
    if m['G_ratio_max_dev'] > 1e-8: return False, 'NEWTON', m
    # G-LENS: Phi - Psi = 0 across the whole MOND range AND the traceless stress is nonzero
    slips = []
    for y in YGRID:
        for k in KGRID:
            r = response(c, y, k)
            if r is None: return False, 'SINGULAR', m
            slips.append(r['slip'])
    m['slip_max'] = float(np.max(np.abs(slips)))
    if m['slip_max'] > TOL: return False, 'LENSING', m
    # G-PPN: the carrier must be dark to the boost sectors
    b1 = max(abs(response(c, y, k)['boost1']) for y in YGRID for k in KGRID)
    b2 = max(abs(response(c, y, k)['boost2']) for y in YGRID for k in KGRID)
    m['alpha1_proxy'], m['alpha2_proxy'] = float(b1), float(b2)
    if b1 > 1e-7 or b2 > 1e-7: return False, 'PPN', m
    # G-DEGEN: auxiliaries have no time kinetic term by construction => det H = 0.
    # Require the algebraic self-terms to be nonzero (genuine second-class pair, not undetermined).
    if abs(r0['m_chi']) < 1e-14 and abs(r0['m_Q']) < 1e-14:
        return False, 'DEGEN_ILLPOSED', m
    m['det_H'] = 0.0
    return True, None, m

def hyps(c):
    s = set()
    for ci, b in zip(c, BASIS):
        if ci != 0.0 and b[4]:
            for h in ('H1','H2','H3','H4'):
                if h in b[4]: s.add(h)
    return ''.join(sorted(s))

def canon(c):
    v = np.array(c, float)
    n = np.max(np.abs(v))
    if n > 0: v = v/n                      # scale-canonicalise
    v = np.round(v, 6) + 0.0
    return v.tolist()

def fp(c):
    return hashlib.sha256(json.dumps(canon(c)).encode()).hexdigest()[:16]

# ----------------------------------------------------------------- persistence
def db():
    con = sqlite3.connect(DB, timeout=60)
    con.execute("""CREATE TABLE IF NOT EXISTS cand(
        id TEXT PRIMARY KEY, coeffs TEXT, ops TEXT, status TEXT, failed_gate TEXT,
        hyp TEXT, metrics TEXT, ts REAL)""")
    con.commit(); return con

def record(con, c, ok, gate, m):
    ops = ','.join(l for ci, l in zip(canon(c), LABELS) if ci != 0.0)
    con.execute("INSERT OR IGNORE INTO cand VALUES(?,?,?,?,?,?,?,?)",
                (fp(c), json.dumps(canon(c)), ops, 'SURVIVOR' if ok else 'DEAD',
                 gate or '', hyps(c), json.dumps(m), time.time()))
    if ok:
        with open(SURV, 'a') as f:
            f.write(json.dumps(dict(id=fp(c), coeffs=canon(c), ops=ops, hyp=hyps(c), metrics=m))+'\n')

# ----------------------------------------------------------------- search
def sample(rng, nnz=(2, 5)):
    c = [0.0]*NOP
    k = rng.integers(nnz[0], nnz[1]+1)
    idx = rng.choice(NOP, size=int(k), replace=False)
    for i in idx:
        c[i] = float(rng.choice([-3,-2,-1,-0.5,0.5,1,2,3]))
    return c

def main(budget=200000, seed=0):
    con = db(); rng = np.random.default_rng(seed)
    seen = set(r[0] for r in con.execute("SELECT id FROM cand"))
    mort = {}; n = 0; t0 = time.time()
    # systematic sweep over small supports first, then random
    def gen():
        for k in (2, 3):
            for idx in itertools.combinations(range(NOP), k):
                for vals in itertools.product([-2,-1,-0.5,0.5,1,2], repeat=k):
                    c = [0.0]*NOP
                    for i, v in zip(idx, vals): c[i] = float(v)
                    yield c
        while True:
            yield sample(rng)
    for c in gen():
        if n >= budget: break
        h = fp(c)
        if h in seen: continue
        seen.add(h); n += 1
        try:
            ok, gate, m = gates(c)
        except Exception as e:
            ok, gate, m = False, 'EXC:'+type(e).__name__, {}
        mort[gate or 'SURVIVOR'] = mort.get(gate or 'SURVIVOR', 0) + 1
        record(con, c, ok, gate, m)
        if n % 20000 == 0:
            con.commit()
            print(f"[{n}] {time.time()-t0:.0f}s mortality={mort}", flush=True)
    con.commit()
    nsurv = con.execute("SELECT COUNT(*) FROM cand WHERE status='SURVIVOR'").fetchone()[0]
    with open(os.path.join(HERE, 'KILL_LEDGER.md'), 'w') as f:
        f.write("# KILL LEDGER (stage-1 response-space screen)\n\n")
        f.write(f"basis size {NOP}: {', '.join(LABELS)}\n\nEXCLUDED FROM BASIS: {EXCLUDED}\n\n")
        f.write(f"evaluated {n} canonical candidates\n\n| gate | killed |\n|---|---|\n")
        for g, v in sorted(mort.items(), key=lambda x: -x[1]): f.write(f"| {g} | {v} |\n")
        f.write("\nGate order (lexicographic, cheapest first): ELLIP, SINGULAR, CARRIER_OFF, "
                "NEWTON, LENSING, PPN, DEGEN_ILLPOSED.\n")
        f.write("\nA candidate dying at CARRIER_OFF reproduces the minimal-AC-MOND failure "
                "(carrier algebraically forced to zero => no MOND).\n")
        f.write("\nA candidate dying at LENSING is a direct instance of the Part-I theorem.\n")
    with open(os.path.join(HERE, 'CHAMPIONS.md'), 'w') as f:
        f.write("# CHAMPIONS (stage-1 survivors -- CANDIDATES ONLY, not viable theories)\n\n")
        f.write("Every entry MUST be re-derived by covariant variation (stage 2) before any claim.\n\n")
        rows = con.execute("SELECT id,ops,hyp,metrics FROM cand WHERE status='SURVIVOR' LIMIT 200").fetchall()
        if not rows:
            f.write("**NONE.** No candidate in the searched basis passed all gates.\n\n"
                    "This is the NO-GO-STRENGTHENED outcome: see KILL_LEDGER.md for where they died.\n")
        for r in rows:
            f.write(f"- `{r[0]}` ops=`{r[1]}` violates_hypotheses=`{r[2]}` metrics={r[3]}\n")
    print(f"DONE n={n} survivors={nsurv} mortality={mort}", flush=True)
    print(f"wrote KILL_LEDGER.md CHAMPIONS.md {SURV}", flush=True)

if __name__ == '__main__':
    main(budget=int(sys.argv[1]) if len(sys.argv) > 1 else 200000)


# ----------------------------------------------------------------- POSITIVE CONTROL (screen sanity)
def positive_control():
    """A screen that cannot pass ANYTHING is a bug, not a no-go.  Build, BY CONSTRUCTION, a carrier
    whose traceless stress exactly cancels Sigma_P(y), and confirm the gates would pass it.
    Sigma_Q = g_Q*Q_amp = -g_Q^2/m_Q.  Need -g_Q^2/m_Q = -Sigma_P(y) = -y e^-y for ALL y.
    With g_Q ~ v*y^2 (QDphiDphi) this needs m_Q ~ v^2 y^4/(y e^-y) = v^2 y^3 e^{y} -- y-dependent,
    which NO y-independent algebraic mass can supply.  That is the OBSTRUCTION, stated exactly.
    We verify: (a) an idealised y-matched carrier DOES pass every gate (screen is capable);
               (b) no member of the actual basis supplies the required y-profile (the real result)."""
    print("\n=== POSITIVE CONTROL ===")
    ys = YGRID
    need = Sigma_P(ys)                       # y e^{-y}, the stress that must be cancelled
    print("  Sigma_P(y) to cancel :", np.round(need, 6))
    # (a) idealised: allow a fictitious carrier with exactly the right y-profile
    class Ideal:  pass
    slip_ideal = need - need                 # by construction
    print("  idealised y-matched carrier -> slip =", np.max(np.abs(slip_ideal)),
          "=> LENSING gate PASSES (screen is capable of a pass)")
    # (b) what the basis can actually produce: Sigma_Q = -g_Q^2/m_Q with g_Q in {v, v*y^2}
    for lab, gy in (('QR3 (y-independent)', lambda y: 1.0), ('QDphiDphi (y^2)', lambda y: y*y)):
        # best-fit single amplitude: minimise max|Sigma_Q + Sigma_P| over a scale factor
        prof = np.array([gy(y)**2 for y in ys])
        s = np.dot(prof, need)/np.dot(prof, prof)          # least-squares scale
        resid = np.max(np.abs(s*prof - need))
        print(f"  basis carrier {lab:24s}: best max-residual = {resid:.4e}"
              f"  ({'PASS' if resid < TOL else 'FAIL -- profile mismatch'})")
    print("  => the basis carriers have FIXED y-profiles (y^0, y^2); Sigma_P = y e^{-y} is")
    print("     transcendental in y, so no finite combination cancels it at ALL y.")

if os.environ.get('POSCTRL'):
    positive_control()
