import sympy as sp, functools, time, importlib.util
print=functools.partial(print,flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
x,p,q=s1.x,s1.p,s1.q
for n in (2,3):
    t0=time.time(); cb=s1.build_seagull(n,cross=False,mode='dS',break_F2=True)
    cb=sp.expand_trig(sp.expand(cb))
    print(f"n={n} F2-BROKEN: sin(px) present (=d_x hit frame leg)? {cb.has(sp.sin(p*x))} "
          f"| algebraic p after phase-strip? {sp.expand(cb.replace(lambda e:e.func in (sp.cos,sp.sin) and e.args[0].has(x), lambda e: sp.Symbol('N'))).has(p)} [{time.time()-t0:.1f}s]")
