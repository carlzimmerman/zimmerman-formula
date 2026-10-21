import math, time
import numpy as np
import core as K

h = 0.005
Rf = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zfh = K.make_faces(K.XMAX, [(0.0, h), (0.5, h)])
zff = K.make_faces_sym(K.XMAX, [(0.0, h), (0.5, h)])
gh = K.Grid(Rf, zfh); mh = K.plummer(gh, K.BFAC, 1.0, (0.5,))
gf = K.Grid(Rf, zff); mf = K.plummer(gf, K.BFAC, 2.0, (0.5, -0.5))
t0 = time.time()
print("=== QUMOND ===")
for tag, g, m in (("half", gh, mh), ("full", gf, mf)):
    for e in (0.0, 0.3, 1.0, 3.0):
        C, _, _, res = K.qumond(g, m, e=e)
        S, row = K.column_S(g, C)
        print(f" {tag:4s} e={e:4.1f} S={S:+.6f} C02={np.interp(0.2,g.Rc,row):+.4f} res={res:.1e} t={time.time()-t0:.1f}")
    C, _, _, res = K.qumond(g, m, e=3.0, include_ext=False)
    S, row = K.column_S(g, C)
    print(f" {tag:4s} own-source e=3 S={S:+.6f} C02={np.interp(0.2,g.Rc,row):+.4f}")
# symmetry check at z=h/2
C0h,_,_,_ = K.qumond(gh,mh,0.0)
C0f,_,_,_ = K.qumond(gf,mf,0.0)
j=np.argmin(abs(gf.zc-h/2))
print("sym check QUMOND: half C[:,0] vs full C[:,j] max diff", np.max(np.abs(C0h[:,0]-C0f[:,j])))
S_h,_=K.column_S(gh,C0h); 
row_f=C0f[:,j]; S_f=float(2*np.sum(np.minimum(row_f,0)*np.diff(gf.Rf)))
print("S at z=h/2: half",S_h,"full",S_f)
