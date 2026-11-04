"""Discriminate finite-variation versus quadrature error in the action check."""
import controls as c

def main(out):
    start=c.time.monotonic();bg=c.VertexBackground(c.BASE/'cascades/run_vertices001/result.json')
    z,w=c.np.polynomial.legendre.leggauss(4);q=[];W=[]
    for lo,hi in zip([0.,.1,1.,5.,20.],[.1,1.,5.,20.,80.]):
        qq=(lo+hi)/2+(hi-lo)*z/2;q.extend(qq);W.extend((hi-lo)*w*qq**2/2)
    q=c.np.array(q);W=c.np.array(W);rows=[]
    for phases in (24,48,96):
        model=c.GenericOrbit(bg,q,W,phase_nodes=phases);Y,orb=model.initial(1e-35)
        expected=-c.T0**3*float((orb['weights']@orb['gas']['energy'])@Y)/orb['omega']
        for dh in (1e-4,3e-5,1e-5,3e-6,1e-6):
            plus=model.orbit(0,Y*(1+dh),E=orb['E']);minus=model.orbit(0,Y*(1-dh),E=orb['E'])
            derivative=(plus['J']-minus['J'])/(2*dh)
            rows.append(dict(phases=phases,dh=dh,derivative=derivative,expected=expected,relative=abs(derivative/expected-1)))
    r=dict(rows=rows,runtime_seconds=c.time.monotonic()-start,peak_rss_bytes_macos=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss)
    c.Path(out).write_text(c.json.dumps(r,indent=2)+'\n');print(c.json.dumps(r))

if __name__=='__main__':main(c.sys.argv[1])
