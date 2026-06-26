#!/usr/bin/env python3
"""
INDEPENDENT lambda RECOMPUTATION #2  (agentT4b)
================================================
Crux equation (2311.05525, verbatim, l.617-619):

    lambda = -(1/16) gamma^{IJ} gamma_{KL} [ d_{omega_mu^{IJ}} , omega_mu^{KL} ]  = 3

with (l.615-616) the operator being the Weyl-ordered spin-connection term
    (1/4) gamma^{IJ} d_{omega_mu^{IJ}} omega_mu^{KL} gamma_{KL}  (commutator-vee product)
and  gamma^{IJ} vee Psi := (1/2)[gamma^{IJ}, Psi].

PHYSICS OF THE BRACKET (the only honest reading):
  [ d_{omega_mu^{IJ}} , omega_nu^{KL} ] = delta_mu^nu * (antisym pair delta)^{IJ}_{KL}
  i.e. the field-space derivative hitting its OWN conjugate field is a c-number.
  Contracting KL->IJ via that delta and summing the spacetime index mu (-> factor
  delta_mu^mu = d = 4) leaves the *matrix* object
        S := sum_{I,J} gamma^{IJ} gamma_{IJ}      (a multiple of the identity)
  and  lambda = -(1/16) * (mu-sum=4) * (1/4 from the 1/2-vee twice? -> see note) * <S>
  where <S> is the scalar coefficient of S = c * 1.

  We compute <S> = (1/dim) Tr( sum_{IJ} gamma^{IJ} gamma_{IJ} )  INDEPENDENTLY in
  multiple bases/signatures.  THE QUESTION: is <S> (hence lambda) the SAME number
  across a Dirac basis (+---), a Majorana/real basis, and signature (-+++)?
     SAME  -> lambda ROBUST (a real prediction)
     DIFF  -> lambda CONVENTION-DEPENDENT (ordering ambiguity; explains 3-vs-42)

We do NOT pre-assume gamma^{IJ}gamma_{IJ} = -12.  We compute it from the explicit
matrices in each basis and each signature, and we also scan the index-bookkeeping
choices (all-16 vs ordered-6 pairs; flat-Kronecker vs metric-lowered contraction).
"""
import sympy as sp
import itertools

I = sp.I

# ----------------------------------------------------------------------
# Helper: build explicit 4x4 gamma matrices for a given signature & basis,
# verify the Clifford relation {g^I,g^J} = 2 eta^{IJ} 1, return (gammas, eta).
# ----------------------------------------------------------------------

def dirac_basis(signature):
    """Standard Dirac rep. signature in {'+---','-+++'}.
    We build g^0..g^3 satisfying {g^I,g^J}=2 eta^{IJ}."""
    # Pauli
    s1 = sp.Matrix([[0,1],[1,0]])
    s2 = sp.Matrix([[0,-I],[I,0]])
    s3 = sp.Matrix([[1,0],[0,-1]])
    Z  = sp.zeros(2)
    Id = sp.eye(2)
    def blk(A,B,C,D):
        return sp.Matrix(sp.BlockMatrix([[A,B],[C,D]]))
    # Dirac basis: g0 = diag(1,-1) blocks; gk = [[0,sk],[-sk,0]]
    g0 = blk(Id,Z,Z,-Id)
    g1 = blk(Z,s1,-s1,Z)
    g2 = blk(Z,s2,-s2,Z)
    g3 = blk(Z,s3,-s3,Z)
    if signature == '+---':
        gammas = [g0,g1,g2,g3]
        eta = sp.diag(1,-1,-1,-1)
    elif signature == '-+++':
        # to flip signature, multiply each matrix by I so squares flip sign
        # g'^I = I * g^I gives {g',g'} = -{g,g}; pick consistent set:
        # We want g0^2=-1, gk^2=+1. Multiply ALL by I: g0^2 -> -1, gk^2 -> +1?
        # (I g0)^2 = -g0^2 = -1 OK; (I gk)^2 = -gk^2 = -(-1)=+1 OK.
        gammas = [I*g0, I*g1, I*g2, I*g3]
        eta = sp.diag(-1,1,1,1)
    else:
        raise ValueError(signature)
    return [sp.Matrix(g) for g in gammas], eta


def majorana_basis():
    """Real (Majorana) representation of Cl(1,3), signature +---.
    All gamma matrices purely real (times i in a couple of entries become real).
    Standard Majorana rep (e.g. Peskin App / itzykson-zuber):
      g0 =  s2 (x) s1 ... we use a known explicit real set.
    Known Majorana set (signature +---, {g,g}=2 eta):
      g0 = [[0, s2],[s2,0]]
      g1 = [[i s3,0],[0,i s3]]
      g2 = [[0,-s2],[s2,0]]
      g3 = [[-i s1,0],[0,-i s1]]
    Check: these are the standard Majorana matrices; g0^2=+1, gk^2=-1.
    They are purely imaginary*real -> the *representation* is real in the sense
    that i*gamma are real; what matters for us is it is a DIFFERENT similarity
    class realization. We verify Clifford explicitly regardless."""
    s1 = sp.Matrix([[0,1],[1,0]])
    s2 = sp.Matrix([[0,-I],[I,0]])
    s3 = sp.Matrix([[1,0],[0,-1]])
    Z  = sp.zeros(2)
    def blk(A,B,C,D):
        return sp.Matrix(sp.BlockMatrix([[A,B],[C,D]]))
    g0 = blk(Z, s2, s2, Z)
    g1 = blk(I*s3, Z, Z, I*s3)
    g2 = blk(Z, -s2, s2, Z)
    g3 = blk(-I*s1, Z, Z, -I*s1)
    eta = sp.diag(1,-1,-1,-1)
    return [sp.Matrix(g) for g in (g0,g1,g2,g3)], eta


def verify_clifford(gammas, eta):
    ok = True
    for a in range(4):
        for b in range(4):
            anti = gammas[a]*gammas[b] + gammas[b]*gammas[a]
            target = 2*eta[a,b]*sp.eye(4)
            if sp.simplify(anti - target) != sp.zeros(4):
                ok = False
    return ok


def gamma_IJ(gammas, eta, I_, J_, normalization='half_comm'):
    """gamma^{IJ} with UPPER indices. Upper index = raise with eta.
       half_comm:  gamma^{IJ} = (1/2)[gamma^I, gamma^J]   (paper's choice, 2511 eq6)
    """
    gI = sum((eta[I_,k]*gammas[k] for k in range(4)), sp.zeros(4))  # gamma^I (raised)
    gJ = sum((eta[J_,k]*gammas[k] for k in range(4)), sp.zeros(4))
    comm = gI*gJ - gJ*gI
    if normalization == 'half_comm':
        return comm/2
    elif normalization == 'quarter_comm':   # sigma normalization
        return comm/4
    elif normalization == 'product':        # gamma^I gamma^J (I!=J equals comm/... no)
        return gI*gJ
    raise ValueError


def scalar_of_identity(M):
    """If M = c * 1, return c (= Tr/dim). Else return Tr/dim and a flag."""
    dim = M.shape[0]
    c = sp.simplify(M.trace()/dim)
    is_scalar = sp.simplify(M - c*sp.eye(dim)) == sp.zeros(dim)
    return c, is_scalar


def compute_S(gammas, eta, sum_range='all16', contraction='metric',
              normalization='half_comm'):
    """Compute  S = sum_{I,J} gamma^{IJ} gamma_{IJ}   (matrix), return (coeff, is_scalar).
       sum_range: 'all16' = all I,J in 0..3 ; 'ord6' = I<J only.
       contraction: how gamma_{IJ} (lower) relates to gamma^{IJ} (upper).
          'metric' : gamma_{IJ} = eta_{IK} eta_{JL} gamma^{KL}  (genuine contraction)
          'flat'   : gamma_{IJ} := gamma^{IJ} literally (Kronecker pairing, the
                     literal reading of the [d_omega^{IJ}, omega^{KL}] = delta^{IJ}_{KL})
    """
    S = sp.zeros(4)
    if sum_range == 'all16':
        pairs = [(i,j) for i in range(4) for j in range(4)]
    elif sum_range == 'ord6':
        pairs = [(i,j) for i in range(4) for j in range(4) if i<j]
    else:
        raise ValueError
    for (i,j) in pairs:
        up = gamma_IJ(gammas, eta, i, j, normalization)
        if contraction == 'flat':
            low = up
        elif contraction == 'metric':
            low = eta[i,i]*eta[j,j]*up   # diagonal eta so this is the lowered one
        else:
            raise ValueError
        S += up*low
    c, isc = scalar_of_identity(S)
    return c, isc


# ----------------------------------------------------------------------
# RUN: compute the crux Clifford scalar  gamma^{IJ}gamma_{IJ}  in each basis,
# under the metric-contracted / all-16 reading (the paper's stated lambda=3 reading).
# Then map  S -> lambda via the paper's bookkeeping and check robustness.
# ----------------------------------------------------------------------

print("="*78)
print("INDEPENDENT RECOMPUTATION #2 of Kanatchikov ordering constant lambda")
print("Crux: lambda = -(1/16) gamma^{IJ} gamma_{KL} [d_omega^{IJ}, omega^{KL}]")
print("="*78)

bases = {
    'Dirac (+---)'    : dirac_basis('+---'),
    'Dirac (-+++)'    : dirac_basis('-+++'),
    'Majorana (+---)' : majorana_basis(),
}

results = {}
for name,(gammas,eta) in bases.items():
    ok = verify_clifford(gammas, eta)
    print(f"\n--- basis: {name} ---  Clifford {{g,g}}=2eta verified: {ok}")
    if not ok:
        print("   !! Clifford FAILED -- skipping")
        continue
    # the paper's stated reading: metric contraction, all-16 sum, half-comm norm
    c_metric_all, isc1 = compute_S(gammas, eta, 'all16', 'metric', 'half_comm')
    c_flat_all,   isc2 = compute_S(gammas, eta, 'all16', 'flat',   'half_comm')
    c_metric_ord, _    = compute_S(gammas, eta, 'ord6',  'metric', 'half_comm')
    c_flat_ord,   _    = compute_S(gammas, eta, 'ord6',  'flat',   'half_comm')
    print(f"  gamma^IJ gamma_IJ  [metric, all-16] = {c_metric_all} * 1   (scalar? {isc1})")
    print(f"  gamma^IJ gamma^IJ  [flat,   all-16] = {c_flat_all} * 1   (scalar? {isc2})")
    print(f"  gamma^IJ gamma_IJ  [metric, ord-6 ] = {c_metric_ord} * 1")
    print(f"  gamma^IJ gamma^IJ  [flat,   ord-6 ] = {c_flat_ord} * 1")
    results[name] = dict(metric_all=c_metric_all, flat_all=c_flat_all,
                         metric_ord=c_metric_ord, flat_ord=c_flat_ord)

# ----------------------------------------------------------------------
# Robustness verdict on the Clifford scalar itself (the basis-invariant core)
# ----------------------------------------------------------------------
print("\n" + "="*78)
print("ROBUSTNESS ACROSS BASES (fixed bookkeeping = metric, all-16, half-comm):")
vals = [results[n]['metric_all'] for n in results]
print("   values:", vals)
print("   all equal? ", len(set(map(sp.nsimplify,vals)))==1)

print("\nROBUSTNESS ACROSS BASES (literal flat-Kronecker, all-16):")
valsf = [results[n]['flat_all'] for n in results]
print("   values:", valsf)
print("   all equal? ", len(set(map(sp.nsimplify,valsf)))==1)

# ----------------------------------------------------------------------
# Map the Clifford scalar to lambda under the paper's literal -1/16 + mu-sum=4,
# for EACH bookkeeping cell, and tabulate the implied lambda + Z_eff.
#   lambda = -(1/16) * (mu-sum = 4) * <gamma^IJ gamma_IJ>    [one common reading]
#   (the -1/16 and the factor 4 from delta_mu^mu are the paper's; the Clifford
#    scalar is what we computed)
#   NOTE: paper's stated chain lands lambda=3 from <S>=-12 via -(1/16)*(-12)*4=3.
# ----------------------------------------------------------------------
print("\n" + "="*78)
print("IMPLIED lambda  (lambda = -(1/16) * mu_sum * <gamma^IJ gamma_IJ>):")
print("="*78)
Z_zim = sp.sqrt(sp.Rational(32,3)*sp.pi)
print(f"Z_zimmerman = sqrt(32 pi/3) = {sp.N(Z_zim,8)}")
print()
mu_sum = 4
table = []
# use Dirac(+---) as the reference basis for the bookkeeping scan
ref = 'Dirac (+---)'
gammas, eta = bases[ref]
cells = [
    ('metric, all-16, half-comm', compute_S(gammas,eta,'all16','metric','half_comm')[0]),
    ('flat,   all-16, half-comm', compute_S(gammas,eta,'all16','flat',  'half_comm')[0]),
    ('metric, ord-6 , half-comm', compute_S(gammas,eta,'ord6', 'metric','half_comm')[0]),
    ('flat,   ord-6 , half-comm', compute_S(gammas,eta,'ord6', 'flat',  'half_comm')[0]),
    ('metric, all-16, quarter ', compute_S(gammas,eta,'all16','metric','quarter_comm')[0]),
    ('metric, ord-6 , quarter ', compute_S(gammas,eta,'ord6', 'metric','quarter_comm')[0]),
]
for label, S in cells:
    lam = sp.Rational(-1,16)*mu_sum*S
    lam = sp.nsimplify(lam)
    # also lam without the mu-sum (mu_sum=1) for the "drop multiplicity" reading
    lam_nomu = sp.Rational(-1,16)*S
    # Z_eff from a0 = sqrt(2 Lambda/lambda) and H_Lambda=c sqrt(Lambda/3):
    #   Z_eff = c H_Lambda / a0 = sqrt(Lambda/3)/sqrt(2 Lambda/lambda) = sqrt(lambda/6)
    if lam > 0:
        Zeff = sp.sqrt(lam/6)
    else:
        Zeff = None
    print(f"  [{label}]  <S>={str(S):>6}  -> lambda(mu=4)={str(lam):>6} "
          f"| lambda(mu=1)={str(sp.nsimplify(lam_nomu)):>7} "
          f"| Z_eff=sqrt(lam/6)={ (str(sp.N(Zeff,5)) if Zeff is not None else 'n/a (lam<=0)') }")
    table.append((label,S,lam,Zeff))

print("\nReference paper value: lambda=3  =>  Z_eff = sqrt(3/6) = sqrt(1/2) =",
      sp.N(sp.sqrt(sp.Rational(1,2)),6))
print("To match Z=5.78881 one needs lambda = 6*Z^2 = 6*(32pi/3) = 64 pi =",
      sp.N(64*sp.pi,7), " (transcendental)")
