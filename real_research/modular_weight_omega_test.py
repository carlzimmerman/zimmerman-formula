#!/usr/bin/env python3
"""
MODULAR WEIGHT-OMEGA TEST (Koide Q from framework-forced modular weight).

QUESTION (non-circular): does a FRAMEWORK-FORCED modular weight k of the finite
modular group A4=Gamma_3 (and S4, A5 cross-checks) land Koide Q = 2/3 at the
fixed point tau = omega = exp(2 pi i/3), WITHOUT scanning weights to hit 2/3?

GROUND TRUTH used (primary sources, not fitted here):
  Weight-2 A4 triplet (Feruglio 1706.08749), q = exp(2 pi i tau):
     Y1 = 1 + 12 q + 36 q^2 + 12 q^3 + ...
     Y2 = -6 q^(1/3) (1 + 7 q + 8 q^2 + ...)
     Y3 = -18 q^(2/3) (1 + 2 q + 5 q^2 + ...)
  Constraint Y2^2 + 2 Y1 Y3 = 0 (all tau).
  Closed form via Dedekind eta log-derivatives (Feruglio Eq. 16-17):
     Y1 = (i/2pi)[ d1 + d2 + d3 - 27 d9 ]
     Y2 = (-i/pi) [ d1 + w^2 d2 + w   d3 ]
     Y3 = (-i/pi) [ d1 + w   d2 + w^2 d3 ]
   with d_j = eta'(arg_j)/eta(arg_j), args = tau/3, (tau+1)/3, (tau+2)/3, 3 tau.

Higher-weight A4 multiplets built from the weight-2 triplet by A4 Clebsch-Gordan
(standard rules), exactly. We then read Koide Q from each triplet-valued channel.

Koide Q = (sum m_i) / (sum sqrt(m_i))^2, with sqrt(m_i) := |component_i| (the
modular-form value gives the sqrt-mass / diagonal Yukawa magnitude). Q is
phase-independent only via Q = 1/3 + r^2/6 when written in (1,1,1)-aligned coords;
here we compute Q directly from the three magnitudes, the honest map.
"""
import mpmath as mp
mp.mp.dps = 40

W   = mp.exp(2j*mp.pi/3)          # omega = exp(2 pi i /3)
TAU = W                           # fixed point tau = omega
I   = mp.mpc(0,1)
PI  = mp.pi

def eta(tau):
    """Dedekind eta via mpmath.jtheta/qpochhammer-free: use mp.eta? -> use product."""
    # mpmath has mp.eta? No standard. Use q-product with q=exp(2 pi i tau).
    q = mp.exp(2j*PI*tau)
    # eta = q^(1/24) prod (1-q^n)
    prod = mp.mpf(1)
    qn = q
    n = 1
    while True:
        term = (1 - qn)
        prod *= term
        if abs(qn) < mp.mpf(10)**(-(mp.mp.dps+10)):
            break
        n += 1
        qn = q**n
        if n > 5000:
            break
    return mp.exp(2j*PI*tau/24) * prod

def dlog_eta(tau):
    """eta'(tau)/eta(tau) via series: d/dtau log eta = (i pi/12) E2(tau),
       E2 = 1 - 24 sum_{n>=1} sigma1(n) q^n.  Robust closed form."""
    q = mp.exp(2j*PI*tau)
    s = mp.mpf(0)
    n = 1
    while True:
        # sigma1(n)
        sig = sum(d for d in range(1, n+1) if n % d == 0)
        term = sig * q**n
        s += term
        if abs(q**n) * n < mp.mpf(10)**(-(mp.mp.dps+10)):
            break
        n += 1
        if n > 8000:
            break
    E2 = 1 - 24*s
    # d/dtau log eta = i pi E2 /12 ; and eta'/eta = that
    return I*PI*E2/12

def Y_triplet(tau):
    d1 = dlog_eta(tau/3)
    d2 = dlog_eta((tau+1)/3)
    d3 = dlog_eta((tau+2)/3)
    d9 = dlog_eta(3*tau)
    Y1 = (I/(2*PI))*( d1 + d2 + d3 - 27*d9 )
    Y2 = (-I/PI)*( d1 + W**2*d2 + W*d3 )
    Y3 = (-I/PI)*( d1 + W*d2 + W**2*d3 )
    return [Y1, Y2, Y3]

# A4 Clebsch-Gordan: (a)x(b) triplets -> singlets + sym triplet
def A4_products(a, b):
    a1,a2,a3 = a; b1,b2,b3 = b
    s1   = a1*b1 + a2*b3 + a3*b2          # 1
    s1p  = a3*b3 + a1*b2 + a2*b1          # 1'  (1''-type label conventions vary)
    s1pp = a2*b2 + a1*b3 + a3*b1          # 1''
    t = [ 2*a1*b1 - a2*b3 - a3*b2,
          2*a3*b3 - a1*b2 - a2*b1,
          2*a2*b2 - a3*b1 - a1*b3 ]       # 3_s
    return s1, s1p, s1pp, t

def koide_Q(vec3):
    sm = [abs(v) for v in vec3]            # sqrt-mass magnitudes
    num = sum(s*s for s in sm)             # sum m_i
    den = sum(sm)**2                       # (sum sqrt m_i)^2
    if den == 0: return None
    return num/den

def angle_to_diag(vec3):
    """angle of (sqrt m) vector to (1,1,1), in degrees (Koide picture)."""
    sm = mp.matrix([abs(v) for v in vec3])
    n  = mp.sqrt(sum(s*s for s in sm))
    ones = mp.matrix([1,1,1]); o = mp.sqrt(mp.mpf(3))
    dot = sum(sm[i]*1 for i in range(3))
    c = dot/(n*o)
    return mp.degrees(mp.acos(c))

print("="*72)
print("Weight-2 A4 triplet at tau = omega")
print("="*72)
Y = Y_triplet(TAU)
for i,y in enumerate(Y,1):
    print(f"  Y{i}(omega) = {mp.nstr(y, 12)}    |Y{i}| = {mp.nstr(abs(y),12)}")
# check constraint Y2^2 + 2 Y1 Y3
con = Y[1]**2 + 2*Y[0]*Y[2]
print(f"  constraint Y2^2 + 2 Y1 Y3 = {mp.nstr(con, 6)}  (should be ~0)")
print(f"  Koide Q(weight-2 triplet @omega) = {mp.nstr(koide_Q(Y), 12)}")
print(f"  angle to (1,1,1) = {mp.nstr(angle_to_diag(Y),10)} deg")
print()

# Build higher-weight triplet channels from the weight-2 triplet.
# Weight 4: Y(x)Y -> 1,1',1'',3.   3-channel = t4.
# Weight 6: Y(x)Y(x)Y, take (Y x t4) and (Y x singlet*Y) etc -> 1,3,3.
# We enumerate all triplet-valued channels we can form at each even weight.
results = []  # (weight, label, Q, angle)

def record(w, label, vec):
    Q = koide_Q(vec)
    if Q is None: return
    results.append((w, label, Q, angle_to_diag(vec)))

# weight 2
record(2, "3 (Y)", Y)

# weight 4 triplet
s1_4, s1p_4, s1pp_4, t4 = A4_products(Y, Y)
record(4, "3_s (YxY)", t4)

# weight 6: products of Y with weight-4 multiplets
# Y x t4 -> 1,1',1'',3
_,_,_, t6a = A4_products(Y, t4)
record(6, "3 (Y x [YY]_3)", t6a)
# triplet times singlet just rescales triplet -> same Q; singlet*Y:
for lab, sg in [("1", s1_4), ("1'", s1p_4), ("1''", s1pp_4)]:
    vec = [sg*Y[0], sg*Y[1], sg*Y[2]]
    record(6, f"3 ( {lab}_4 . Y )", vec)

# weight 8: Y x t6a, and t4 x t4
_,_,_, t8a = A4_products(Y, t6a)
record(8, "3 (Y x w6_3)", t8a)
_,_,_, t8b = A4_products(t4, t4)
record(8, "3_s ([YY]x[YY])", t8b)

# weight 10: Y x t8a ; t4 x t6a
_,_,_, t10a = A4_products(Y, t8a)
record(10, "3 (Y x w8_3)", t10a)
_,_,_, t10b = A4_products(t4, t6a)
record(10, "3 (w4 x w6_3)", t10b)

# weight 12: Y x t10a ; t6a x t6a
_,_,_, t12a = A4_products(Y, t10a)
record(12, "3 (Y x w10_3)", t12a)
_,_,_, t12b = A4_products(t6a, t6a)
record(12, "3_s (w6 x w6)", t12b)

print("="*72)
print("Q(k) table at tau = omega  (triplet-valued channels)")
print("="*72)
print(f"{'wt':>3} {'channel':<22} {'Koide Q':>16} {'angle(deg)':>12}")
hit23 = []
for w, lab, Q, ang in results:
    flag = "  <-- 2/3 !!" if abs(Q - mp.mpf(2)/3) < mp.mpf('1e-6') else ""
    print(f"{w:>3} {lab:<22} {mp.nstr(Q,12):>16} {mp.nstr(ang,8):>12}{flag}")
    if abs(Q - mp.mpf(2)/3) < mp.mpf('1e-4'):
        hit23.append((w, lab, Q))

print()
print(f"target 2/3 = {mp.nstr(mp.mpf(2)/3, 12)}")
print(f"channels within 1e-4 of 2/3: {len(hit23)}")
for w,lab,Q in hit23:
    print(f"    weight {w}, {lab}, Q={mp.nstr(Q,12)}")
print()
print("Distinct Q values seen (rounded 6dp):")
seen = sorted(set(round(float(Q),6) for _,_,Q,_ in results))
print("   ", seen)
