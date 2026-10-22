import mpmath as mp
mp.mp.dps = 30

H = mp.mpf(1); nu = mp.mpf('0.2'); t = mp.mpf('0.3'); k = mp.mpf(2)
K = mp.mpf(1); Lam = mp.mpf(3); beta = mp.mpf('0.5')
a = mp.e**(H*t); ad = H*a
sig = mp.e**(nu*t); sd = nu*sig

def Lz(eps, z):
    eps = mp.mpf(eps)
    f = eps*sig*mp.cos(k*z)
    fp = -eps*sig*k*mp.sin(k*z)
    fpp = -k**2*f
    g1 = 1+f; g2 = 1-f
    R3m = -fpp/g1 + fpp/g2 + fp**2/(2*g1**2) + fp**2/(2*g2**2) - (fp*(-fp))/(2*g1*g2)
    R3 = R3m/a**2
    gd = [eps*sd*mp.cos(k*z), -eps*sd*mp.cos(k*z), mp.mpf(0)]   # d_t f at fixed z
    g = [g1, g2, mp.mpf(1)]
    hd = [2*a*ad*x + a**2*y for x, y in zip(g, gd)]
    hinv = [1/(a**2*x) for x in g]
    Kij = [x/2 for x in hd]
    theta = sum(hinv[i]*Kij[i] for i in range(3))
    Ksq = sum(hinv[i]**2*Kij[i]**2 for i in range(3))
    sqrth = a**3*mp.sqrt(g1*g2)
    return (R3 + Ksq - (1+beta)*theta**2 - 2*Lam)*sqrth/(4*K)

def Lbar(eps, n=2001):
    zs = [2*mp.pi*mp.mpf(i)/(n-1)/k for i in range(n)]
    return sum(Lz(eps, z) for z in zs)/n

L0 = Lbar(0)
print("Lbar(0) =", mp.nstr(L0, 20))
vals = []
for e in ['2e-3', '1e-3']:
    v = (Lbar(e) - L0)/mp.mpf(e)**2
    vals.append(v)
    print("eps", e, " -> coefficient =", mp.nstr(v, 20))
print("extrapolated (Richardson):", mp.nstr(2*vals[1]-vals[0], 20))

A = (1/(4*K))*a**3*(sd**2/4 - k**2*sig**2/(4*a**2) + (2+3*beta)*sig*sd*ad/a + (9*beta*H**2+2*Lam)*sig**2/4)
B = (a/(16*K))*(a**2*sd**2 - k**2*sig**2 + 4*(2+3*beta)*a*sig*sd*ad + (6+9*beta)*H**2*a**2*sig**2 + 2*Lam*a**2*sig**2)
print("A =", mp.nstr(A, 20))
print("B =", mp.nstr(B, 20))