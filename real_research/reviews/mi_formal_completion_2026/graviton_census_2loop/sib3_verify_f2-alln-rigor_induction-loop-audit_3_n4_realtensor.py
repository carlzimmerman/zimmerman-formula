#!/usr/bin/env python3
r"""Push the REAL graviton-dressed seagull tensor to n=4 (2n=8 covariant derivatives),
both TT polarizations, and read the p^2 spatial-cone seed + explicit-p. This is the order the
lane's full-tensor CAS did NOT reach (rigor_1's n=8 was a graviton-DROPPED scalar)."""
import sympy as sp, functools, time, importlib.util
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
for pol,cross in (('same',False),('cross',True)):
    t0=time.time()
    c=s1.build_seagull(4, cross=cross, mode='dS')
    cl=s1.classify(c)
    print(f"n=4 {pol}: p2_spatial={sp.simplify(cl['p2_spatial'])} | p_explicit={cl['p_explicit']} | q_explicit={cl['q_explicit']} | mass_nonzero={sp.simplify(cl['mass'])!=0} [{time.time()-t0:.1f}s]")
