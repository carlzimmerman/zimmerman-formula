import numpy as np
A0 = 9.36e-11
def nu_can(y): return 0.5*(1+np.sqrt(1+4/y))
def u_of_y(y, yt=None):
    nu = nu_can(y)
    if yt is None: return A0*y*(nu-1), A0*y + A0*y*(nu-1)
    nuf = 1 + (nu-1)/(1+(y/yt)**2)
    return A0*y*(nuf-1), A0*y + A0*y*(nuf-1)
yt = 66.2999
ys = np.geomspace(1e-3, 1e12, 400000)
u_c, g_c = u_of_y(ys); u_p, g_p = u_of_y(ys, yt)
print("canonical: u/a0 max =", u_c.max()/A0, " at y=", ys[np.argmax(u_c)])
print("patched  : u/a0 max =", u_p.max()/A0, " at y=", ys[np.argmax(u_p)])
j = np.argmax(u_p); print("  u at y=1e2,1e3,1e5,6.3e7,1e9 (a0):", [u_of_y(y,yt)[0]/A0 for y in (1e2,1e3,1e5,6.3e7,1e9)])
dgdy_p = np.gradient(g_p, ys); dudy_p = np.gradient(u_p, ys)
print("patched: min dg/dg_N over y in [1e-2,1e9] =", (dgdy_p/A0)[(ys>1e-2)&(ys<1e9)].min(),
      "at y=", ys[(ys>1e-2)&(ys<1e9)][np.argmin((dgdy_p/A0)[(ys>1e-2)&(ys<1e9)])])
dgdu_p = dgdy_p/dudy_p
m = (ys>0.3)&(ys<1e10)
print("patched: dg/du at y=1,10,66,1e3,6.3e7 :", [dgdu_p[np.argmin(abs(ys-y))] for y in (1,10,66,1e3,6.3e7)])
print("patched: y where dg/du changes sign  :", ys[m][np.argmin(abs(dgdu_p[m]))], " (du/dy zero crossing)")
print("canonical: dg/du at y=1,1e3,6.3e7   :", [ (1- (A0**2)/((g_c[np.argmin(abs(ys-y))]+A0)**2))**(-1) for y in (1,1e3,6.3e7)])
# is u(y) single valued -> two y for same u ?
for target in (0.1,0.3,0.5):
    ii = np.where(np.abs(u_p/A0-target)<2e-4)[0]
    if len(ii):
        print(f"u/a0={target}: {len(ii)} y-solutions, y span {ys[ii[0]]:.3g} .. {ys[ii[-1]]:.3g}, g/a0 span {g_p[ii[0]]/A0:.3g} .. {g_p[ii[-1]]/A0:.3g}")
print("patched u->0 as y->inf:", u_p[-1]/A0, " g/a0=", g_p[-1]/A0)
print("W' at u=0 must be 0 => g=0; patched needs g=inf at u=0 -> contradiction")
# what y does dg/dg_N first drop below 1 ?
idx = np.where((dgdy_p/A0)[m] < 1.0)[0]
print("first y with dg/dg_N<1:", ys[m][idx[0]] if len(idx) else None)