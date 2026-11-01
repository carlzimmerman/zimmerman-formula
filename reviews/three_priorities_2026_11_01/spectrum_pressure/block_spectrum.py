"""Representation-block implementation, independent of the 49-field mass assembly."""
import math
import mpmath as mp

def real_scalar(M,B,extra=None):
    A=M.H*M;n=M.rows
    H=mp.matrix(2*n)
    for i in range(n):
        for j in range(n):
            H[i,j]=mp.re(A[i,j]+B[i,j]);H[n+i,n+j]=mp.re(A[i,j]-B[i,j])
            H[i,n+j]=-mp.im(A[i,j]+B[i,j]);H[n+i,j]=mp.im(A[i,j]-B[i,j])
    if extra is not None:H+=extra*extra.T
    return list(mp.eigsy(H,eigvals_only=True))

def sectors(X,h,lam,g,f=1):
    X,h,lam,g,f=map(mp.mpf,(X,h,lam,g,f))
    a=mp.sqrt(2*f*h/(30*h*h+lam*lam));b=h*X/lam;c=lam*lam*f*h/(30*h*h+lam*lam)
    out=[]
    for label,r,mult in [('SU3',mp.mpf(2),8),('SU2',mp.mpf(-3),3),('broken',mp.mpf('-.5'),12)]:
        m=(1+r)*h*X;q=r*lam*a;split=(1+r)*c
        M=mp.matrix([[m,mp.j*q],[mp.j*q,0]])
        B=mp.matrix([[split,0],[0,0]])
        extra=mp.matrix([5*g*a,0,0,-5*g*b]) if label=='broken' else None
        es=real_scalar(M,B,extra)
        if label=='broken':
            MF=mp.matrix([[m,mp.j*q,5*g*a],[mp.j*q,0,5*mp.j*g*b],[5*g*a,5*mp.j*g*b,0]])
            ev=[25*g*g*(a*a+b*b)]
        else:MF=M;ev=[]
        ef=list(mp.eighe(MF.H*MF,eigvals_only=True))
        out.append({'label':label,'multiplicity':mult,'scalars':es,'Weyls':ef,'vectors':ev})
    out.append({'label':'singlets','multiplicity':1,'scalars':[0,0,2*f*h,2*f*h,2*f*h,2*f*h],
                'Weyls':[0,2*f*h,2*f*h],'vectors':[]})
    out.append({'label':'unbroken_gauge','multiplicity':12,'scalars':[],'Weyls':[0],'vectors':[0]})
    return out

def flattened(ss,key):
    return [v for s in ss for v in s[key] for _ in range(s['multiplicity'])]

def cw_value(X,h,lam,g,f=1,parts=False):
    ss=sectors(X,h,lam,g,f);cs=[]
    for s in ss:
        def ht(vals):
            terms=[]
            for v in vals:
                if v < -mp.mpf('1e-40'):raise ValueError('Physical negative scalar/eigenvalue in block spectrum')
                if v>mp.mpf('1e-40'):terms.append(v*v*(mp.log(v)-mp.mpf('1.5')))
            return sum(terms)
        cs.append(s['multiplicity']*(ht(s['scalars'])-2*ht(s['Weyls'])+3*ht(s['vectors']))/(64*mp.pi**2))
    val=sum(cs)
    return (val,dict(zip([s['label'] for s in ss],cs))) if parts else val

def derivatives(X,h,lam,g,step=mp.mpf('.005')):
    step=mp.mpf(step);xs=mp.mpf(X)
    vs=[cw_value(xs*mp.exp(i*step),h,lam,g) for i in (-2,-1,0,1,2)]
    first=(vs[0]-8*vs[1]+8*vs[3]-vs[4])/(12*step)
    second=(-vs[0]+16*vs[1]-30*vs[2]+16*vs[3]-vs[4])/(12*step**2)
    return first,second

if __name__=='__main__':
    mp.mp.dps=50
    import sys,json
    import numpy as np
    from spectrum import spectrum
    rows=[]
    for X in (0,.1,1,3,10):
        h=lam=.6;g=math.sqrt(29/200)*lam
        dense=spectrum(X,h,lam,g,full=True)
        ss=sectors(X,h,lam,g)
        row={'X':X,'CW_blocks':float(cw_value(X,h,lam,g)),'CW_dense':dense['CW']}
        for key in ['scalars','Weyls','vectors']:
            # Unbroken gauge vectors have 2 polarizations, but zero mass in the potential.
            ours=sorted(float(v) for v in flattened(ss,key))
            theirs=sorted(v['m2'] for v in dense[key] for _ in range(v['multiplicity']))
            row[key+'_max_abs_difference']=float(np.max(abs(np.array(ours)-theirs)))
        rows.append(row)
    assert max(r[k+'_max_abs_difference'] for r in rows for k in ['scalars','Weyls','vectors'])<1e-8
    out={'comparison':rows,'mp_dps':mp.mp.dps,'all_spectra_match':True}
    Path=None
    from pathlib import Path
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
