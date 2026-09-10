#!/usr/bin/env python3
"""Continue a matched initial-jet family; NOT radial evolution of one action."""
import json
import mpmath as mp
import high_precision_gate as h


def run():
    rows=[]
    with mp.workdps(40):
        last=list(map(mp.mpf,('4164.89540032022','.1537936934617971','.02600582459994482')))
        last_u=mp.mpf('.03')
        for u in ('.03','.128','.5','2','10','100','1000','10000'):
            try:
                guess=(last[0],last[1],last[2]*mp.mpf(u)/last_u)
                theta=mp.findroot(lambda *v:h.residual(v,mp.mpf(u)),
                    tuple(mp.log(v) for v in guess),tol=mp.mpf('1e-27'),maxsteps=35)
                a,b=h.pair(theta,mp.mpf(u))
                last=[mp.exp(v) for v in theta];last_u=mp.mpf(u)
                A1,B1=h.parts(a);A2,B2=h.parts(b);A=A1-A2;B=B1-B2
                f=-mp.fdot(A,B)/mp.fdot(B,B)
                h.check_map(f,a['F'],a['X'])
                N=h.next_drift(a,f)-h.next_drift(b,f)
                den=mp.norm(N)*mp.norm(B)
                obstruction=(N[0]*B[1]-N[1]*B[0])/den if den else (mp.mpf(0) if not mp.norm(N) else None)
                txt=lambda v:None if v is None else mp.nstr(v,32)
                row=dict(u1=u,parameters=[txt(v) for v in last],f=txt(f),
                    Dfield=txt(2*(a['F']-a['X']*f)),
                    match_residual=[txt(v) for v in h.residual(theta,mp.mpf(u))],
                    next_obstruction=txt(obstruction),
                    required_j_by_equation=[txt(-N[i]/B[i]) if B[i] else None for i in range(2)],
                    Dcoord=[txt(a['Dcoord']),txt(b['Dcoord'])])
            except (ValueError,ZeroDivisionError) as exc:row=dict(u1=u,error=str(exc))
            rows.append(row);print('CONTINUATION='+json.dumps(row),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),matched=sum('error' not in v for v in rows),
        scope='Eight prescribed initial data, not an interval theorem or preservation along a common action')))
    return rows


if __name__=='__main__':run()
