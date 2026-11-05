import math, json, pathlib
# Planar periodic restriction of fixed-width filtered-source QUMOND.
# 4 pi G = a0 = 1, positive baryon density rho=2+h_prime.
# Uniform external Newtonian field e=3 prevents a zero of |g_N|.
# h=sin(x)+0.2*sin(2x); S is Gaussian sigma=0.7 on the periodic circle.
rows=[]
for n in (256,1024,4096,16384):
 e=3.0; sigma=0.7; s1=math.exp(-sigma*sigma/2); s2=math.exp(-2*sigma*sigma)
 originals=[]; corrected=[]; plain=[]
 for j in range(n):
  x=2*math.pi*j/n
  h=math.sin(x)+.2*math.sin(2*x); hp=math.cos(x)+.4*math.cos(2*x)
  hs=s1*math.sin(x)+.2*s2*math.sin(2*x); hsp=s1*math.cos(x)+.4*s2*math.cos(2*x)
  F=lambda z:.5*z+math.sqrt(.25*z*z+z)
  ph=F(e+hs)-(e+hs)
  # constant field subtraction integrates to zero against hp and hsp.
  originals.append(hp*ph)
  corrected.append(hsp*ph) # <rho,S ph>=<S rho,ph>
  plain.append(hp*(F(e+h)-(e+h)))
 row=dict(n=n,net_force_original=math.fsum(originals)/n,net_force_adjoint_corrected=math.fsum(corrected)/n,net_force_unfiltered_qumond=math.fsum(plain)/n)
 rows.append(row)
assert min(abs(r['net_force_original']) for r in rows)>1e-4
assert max(abs(r['net_force_adjoint_corrected']) for r in rows)<1e-13
assert max(abs(r['net_force_unfiltered_qumond']) for r in rows)<1e-13
assert abs(rows[-1]['net_force_original']-rows[-2]['net_force_original'])<1e-13
result=dict(outcome='counterexample to net internal force cancellation for fixed-width source-only filtered map',rows=rows,scope='Planar periodic QUMOND with homogeneous background subtracted, positive density rho=2+h_prime, constant external field. Not an isolated 3D two-body calculation; not a no-go for adjoint-completed or dynamic filtering.')
pathlib.Path('run/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
