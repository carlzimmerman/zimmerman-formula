"""Generated exact constrained adapted momentum RHS; see derive_expanded.py."""
def rate(M,U,E,p,r,b1,b2,N,N1,w,L,P,P1,F,FD,FD1,d,r1):
    x0 = p**2
    x1 = N*r
    x2 = N*x0
    x3 = M*U
    x4 = 2*E*x0*x3
    x5 = E**2
    x6 = M**2*x5
    x7 = 4*x6
    x8 = p*x1
    x9 = b1*x7
    x10 = x2*x6
    x11 = N1*x0
    x12 = 4*x5
    x13 = x12*x2
    x14 = FD*x3
    x15 = P*x14
    x16 = U**2
    x17 = F*x16
    x18 = b1**2
    x19 = E**4*M**3*N
    x20 = x17*x19
    x21 = 8*b2
    x22 = FD*d*x16*x19
    x23 = 12*x18
    return (1/2)*(-FD1*P*x13*x3 + L*r*x4 + M*x13*x17 + N*p**4 + N1*p*r*x9 - P1*x13*x14 - 8*b1*x15*x2*x5 - 2*b2*x10 + b2*x7*x8 - 3*p**3*x1 + r**2*x2 + r1*w*x4 - 5*x10*x18 - x11*x12*x15 - x11*x9 + 8*x18*x6*x8 + x20*x21 + x20*x23 - x21*x22 - x22*x23)/(E*M*U*x0)
