import mpmath as mp
from mpmath import mpf
mp.mp.dps = 30

# concrete background: a=e^{Ht}, sigma=e^{nu t}, H=1, nu=0.2, t=0.3, k=2, K=1, Lambda=3, beta=0.5
H = mpf(1); nu = mpf('0.2'); t = mpf('0.3'); k = mpf(2); K = mpf(1); Lam = mpf(3); beta = mpf('0.5')
a = mp.e** (H*t); ad = H*a
sig = mp.e**(nu*t); sd = nu*sig
print("a=",a,"ad=",ad,"sig=",sig,"sd=",sd)

def Lnum(eps):
    eps = mpf(eps)
    f = eps*sig*mp.cos(k*0)  # z=0 -> cos=1 ; average handled separately below
    # build m = diag(1+f,1-f,1), h=a^2 m ; Kij = d_t h /2 ; exact inverse
    g = [1+f, 1-f, mpf(1)]
    gd = [eps*sd, -eps*sd, mpf(0)]
    h = [a**2*x for x in g]
    hd = [2*a*ad*x + a**2*y for x,y in zip(g,gd)]
    hinv = [1/x for x in h]
    Kij = [x/2 for x in hd]
    theta = sum(hinv[i]*Kij[i] for i in range(3))
    Ksq = sum(hinv[i]**2*Kij[i]**2 for i in range(3))
    # R3 for diagonal m=diag(1+f,1-f,1) at a point where f'=0 (z=0): use exact formula
    # R3 = -g1''/g1 - g2''/g2 + g1'^2/(2g1^2)+g2'^2/(2g2^2) - g1'g2'/(2g1g2), with f=eps*sig*cos(kz)
    # at z=0: f'=0, f''=-k^2 f
    fpp = -k**2*f
    g1 = 1+f; g2 = 1-f
    R3m = -fpp/g1 + fpp/g2      # g1''=fpp, g2''=-fpp
    R3 = R3m/a**2
    sqrth = a**3*mp.sqrt(g1*g2)
    return (R3 + Ksq - (1+beta)*theta**2 - 2*Lam)*sqrth/(4*K)

L0 = Lnum(0)
for e in ['1e-3','2e-3']:
    print("eps",e," (L-L0)/eps^2 =", mp.nstr((Lnum(e)-L0)/mpf(e)**2, 20))

A = (1/(4*K))*a**3*(sd**2/4 - k**2*sig**2/(4*a**2) + (2+3*beta)*sig*sd*ad/a + (9*beta*H**2+2*Lam)*sig**2/4)
B = (a/(16*K))*(a**2*sd**2 - k**2*sig**2 + 4*(2+3*beta)*a*sig*sd*ad + (6+9*beta)*H**2*a**2*sig**2 + 2*Lam*a**2*sig**2)
print("candidate A:", mp.nstr(A,20))
print("candidate B:", mp.nstr(B,20))