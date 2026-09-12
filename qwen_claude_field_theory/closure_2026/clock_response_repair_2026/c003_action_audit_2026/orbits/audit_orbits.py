#!/usr/bin/env python3
"""Bounded C003 audit: angle integral and stationary tracer orbits, no fitting.

The potential is an untruncated Newtonian NFW. Eddington inversion gives its
isotropic DF. Restricting that DF to binding energies E >= psi(100 rs) makes
a finite stationary tracer population, without imposing a spatial wall. This
population is NOT the source of an evolving/self-consistent gravitational field.
The initial NFW source and final fixed potential are explicitly prescribed.
"""
import argparse
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, cumulative_trapezoid
from scipy.special import gammainc
from scipy.stats import poisson

VK = 650.0
MEAN = 2.3077948724637416
G0 = 0.382508632299176
OM, OL, H0 = .3138, .6862, .6736 / 9.778
G, KM = 4.30091e-6, 1.02271217
HOSTS = [('spiral', 70., 250., .5), ('milky_way', 110., 480., 1.19),
         ('group', 300., 900., 2.2), ('cluster', 1000., 2600., 2.71)]
SOURCE = Path('fable_independent_2026/L189_results.json')


def m(x):
    x = np.asarray(x)
    direct = np.log1p(x) - x / (1 + x)
    small = x*x*(.5 + x*(-2/3 + x*(.75 + x*(-.8 + x*5/6))))
    return np.where(x < 1e-3, small, direct)


def psi(x):
    return np.log1p(x) / x


def rho(x):
    return 1 / (x * (1+x)**2)


def age(z):
    return 2/(3*H0*np.sqrt(OL))*np.arcsinh(np.sqrt(OL/OM)/(1+z)**1.5)


def intensity(t):
    beta = 1.5 * H0 * np.sqrt(OL)
    start = age(6.)
    return G0/OL * (t-start - (np.tanh(beta*t)-np.tanh(beta*start))/beta)


def bound_angle(v, kick, escape):
    if v == 0 or kick == 0:
        return float(v*v+kick*kick < escape*escape)
    return float(np.clip((escape*escape-v*v-kick*kick)/(2*v*kick)+1, 0, 2)/2)


def analytic_audit():
    data = json.loads(SOURCE.read_text())
    assert data['vk'] == VK and data['kicks_by_z0'] == MEAN
    assert abs(data['G0_per_DEGyr']-G0) < 1e-14
    assert abs(intensity(age(0.))-MEAN) < 1e-10
    assert bound_angle(1, 1, math.sqrt(2)) == .5000000000000001
    assert bound_angle(50, 650, 250) == 0
    assert bound_angle(100, 1, 250) == 1
    out = []
    rng = np.random.default_rng(935706)
    for name, sig, ve, x in HOSTS:
        norm = gammainc(1.5, ve*ve/(2*sig*sig))
        pdf = lambda v: np.sqrt(2/np.pi)*v*v/sig**3*np.exp(-v*v/(2*sig*sig))
        exact, err = quad(lambda v: pdf(v)*bound_angle(v,VK,ve), 0, ve,
                          points=[v for v in [abs(ve-VK),ve+VK] if 0 < v < ve],
                          epsabs=1e-12)
        det = gammainc(1.5, max(ve*ve-VK*VK,0)/(2*sig*sig)) / norm
        a = ve*ve*x/(2*np.log1p(x))
        j, je = quad(lambda y: float(m(y))/(y**3*(1+y)**2), x, np.inf,
                     epsabs=1e-13)
        sig_eq = np.sqrt(a*x*(1+x)**2*j)
        # An independent Cartesian sample of bound Maxwellian velocities.
        vv = rng.normal(size=(400000,3))*sig
        vv = vv[np.sum(vv*vv,axis=1) < ve*ve]
        directions = rng.normal(size=vv.shape)
        directions /= np.linalg.norm(directions,axis=1)[:,None]
        frac = np.mean(np.sum((vv+VK*directions)**2,axis=1) < ve*ve)
        se = np.sqrt(frac*(1-frac)/len(vv))
        assert abs(frac-exact/norm) < max(6*se,2e-5)
        out.append(dict(host=name, sigma_supplied=sig, sigma_equilibrium_nfw=sig_eq,
                        sigma_equilibrium_ratio=sig_eq/sig, vesc=ve, x_anchor=x,
                        amplitude_kms_squared=a, single_kick_exact_bound=exact/norm,
                        angle_quadrature_abs_error=err/norm,
                        single_kick_deterministic_bound=det,
                        cartesian_MC_bound=float(frac), MC_se=float(se), MC_n=len(vv),
                        L189_retention=data['f'][len(out)]))
    return out


class Equilibrium:
    """Numerical Eddington DF with energy cutoff, in units (rs, sqrt(A))."""
    def __init__(self):
        x = np.geomspace(1e-8, 1e10, 16000)
        p = psi(x)
        logprime = -1/x - 2/(1+x)
        rp = rho(x)*logprime
        rpp = rho(x)*(logprime**2 + 1/x**2+2/(1+x)**2)
        pp = -m(x)/x**2
        ppp = 2*m(x)/x**3 - 1/(x*(1+x)**2)
        derivative = (rpp*pp-rp*ppp)/pp**3
        assert np.all(derivative > 0)
        energy = np.unique(np.r_[np.geomspace(1e-7,.1,300),
                                 1-np.geomspace(1e-8,.9,1200)[::-1]])
        gu, gw = leggauss(192)
        gu, gw = (gu+1)/2, gw/2
        q = energy[:,None]*(1-gu[None,:]**2)
        vals = np.exp(np.interp(np.log(q), np.log(p[::-1]), np.log(derivative[::-1])))
        f = 2*np.sqrt(energy)/(np.sqrt(8)*np.pi**2) * (vals @ gw)
        assert np.all(np.isfinite(f)) and np.all(f > 0)
        self.energy, self.f = energy, f
        self.cutoff = float(psi(100.))
        self.rgrid = np.geomspace(1e-5,100,2400)
        self.qgrid = np.linspace(0,1,384)
        ps = psi(self.rgrid)
        vmax = np.sqrt(2*np.maximum(ps-self.cutoff,0))
        vel = vmax[:,None]*self.qgrid[None,:]
        fp = self.df(ps[:,None]-.5*vel**2)
        speed_pdf = vel**2 * fp
        speed_cdf = cumulative_trapezoid(speed_pdf,self.qgrid,axis=1,initial=0)
        self.density = 4*np.pi*vmax*speed_cdf[:,-1]
        self.speed_cdf = speed_cdf/np.maximum(speed_cdf[:,-1,None],1e-200)
        self.radial_cdf = cumulative_trapezoid(self.rgrid**2*self.density,
                                               self.rgrid,initial=0)
        # Orthogonal recovery of uncut NFW density and Jeans moment.
        self.recovery = []
        for _,_,_,xx in HOSTS:
            vm = np.sqrt(2*psi(xx))
            v = vm*gu
            integ = 4*np.pi*vm*np.sum(gw*v*v*self.df(psi(xx)-.5*v*v))
            cut_v = np.sqrt(2*(psi(xx)-self.cutoff))*gu
            cut_den = 4*np.pi*np.sqrt(2*(psi(xx)-self.cutoff))*np.sum(
                gw*cut_v*cut_v*self.df(psi(xx)-.5*cut_v*cut_v))
            assert abs(integ/rho(xx)-1) < 1e-3
            assert cut_den <= integ
            self.recovery.append(dict(x=xx,uncut_density_ratio=float(integ/rho(xx)),
                                      cutoff_density_ratio=float(cut_den/rho(xx))))

    def df(self, e):
        return np.exp(np.interp(np.log(np.maximum(e,1e-300)),
                                np.log(self.energy),np.log(self.f)))

    def sample(self, n, seed):
        rng = np.random.default_rng(seed)
        boundaries = np.array([1e-5,.5,1.19,2.2,2.71,5,10,30,100])
        if n % 8:
            raise ValueError('n must be divisible by 8')
        c = np.interp(boundaries,self.rgrid,self.radial_cdf)
        u = np.concatenate([rng.uniform(c[i],c[i+1],n//8) for i in range(8)])
        r = np.interp(u,self.radial_cdf,self.rgrid)
        w = np.repeat(np.diff(c)/(n//8),n//8)
        bins = np.searchsorted(self.rgrid,r).clip(1,len(self.rgrid)-1)
        mix = (r-self.rgrid[bins-1])/(self.rgrid[bins]-self.rgrid[bins-1])
        cdf = (1-mix[:,None])*self.speed_cdf[bins-1]+mix[:,None]*self.speed_cdf[bins]
        q = np.array([np.interp(ui,ci,self.qgrid) for ui,ci in zip(rng.uniform(size=n),cdf)])
        v = np.sqrt(2*(psi(r)-self.cutoff))*q
        d = rng.normal(size=(n,3)); d /= np.linalg.norm(d,axis=1)[:,None]
        vd = rng.normal(size=(n,3)); vd /= np.linalg.norm(vd,axis=1)[:,None]
        return r[:,None]*d,v[:,None]*vd,w


def host_params():
    result = []
    rho_crit = 3*(67.36/1000)**2/(8*np.pi*G)
    for name,sig,ve,xx in HOSTS:
        a = ve*ve*xx/(2*np.log1p(xx))
        if name == 'spiral':
            rs = 3*2*(1.2)**.35/xx
            prescription = '3 Rd, Rd=2 kpc*(Mb/1e10 Msun)^.35, Mb=1.2e10 Msun'
        elif name == 'milky_way':
            rs = 30/xx
            prescription = 'anchor=30 kpc'
        else:
            rs = np.sqrt(a*float(m(xx))/(G*(4*np.pi/3)*500*rho_crit*xx**3))
            prescription = 'anchor=R500 at H0=67.36, critical density definition'
        result.append(dict(name=name,A=a,rs_kpc=float(rs),r_anchor_kpc=float(rs*xx),
                           M_anchor_Msun=float(a*rs/G*m(xx)),x_anchor=xx,
                           scale_time_gyr=float(rs/(KM*np.sqrt(a))),scale_rule=prescription))
    return result


def acceleration(x):
    r = np.linalg.norm(x,axis=-1)
    return -m(r)[:,:,None]/np.maximum(r,1e-14)[:,:,None]**3*x


def specific_energy(x,v):
    return .5*np.sum(v*v,axis=-1)-psi(np.linalg.norm(x,axis=-1))


def events(n,seed):
    rng=np.random.default_rng(seed+71000)
    counts=rng.poisson(MEAN,size=n)
    ids=np.repeat(np.arange(n),counts)
    pp=rng.uniform(0,MEAN,len(ids))
    tg=np.linspace(age(6.),age(0.),20000)
    tt=np.interp(pp,intensity(tg),tg)
    directions=rng.normal(size=(len(ids),3))
    directions/=np.linalg.norm(directions,axis=1)[:,None]
    order=np.argsort(tt)
    return tt[order],ids[order],directions[order],counts


def integrate(eq,n,seed,dt):
    begin=time.time()
    params=host_params()
    a=np.array([p['A'] for p in params])
    scales=np.array([p['scale_time_gyr'] for p in params])
    anchors=np.array([p['x_anchor'] for p in params])
    ix,iv,w=eq.sample(n,seed)
    # First four populations get kicks, latter four are exactly matched controls.
    x=np.broadcast_to(ix,(8,n,3)).copy(); v=np.broadcast_to(iv,(8,n,3)).copy()
    orig_e=specific_energy(x,v)
    ework=np.zeros((8,n))
    tt,ids,directions,counts=events(n,seed)
    t0,tend=age(6.),age(0.)
    nsteps=int(np.ceil((tend-t0)/dt)); dt=(tend-t0)/nsteps
    h=dt/np.r_[scales,scales]
    acc=acceleration(x)
    cursor=0
    sum_occ=np.zeros((8,n)); nsamp=0
    early_occ=np.zeros((8,n)); early_samples=0
    # z=.4 KiDS enclosed/shell diagnostic, sampled over +/- .1 Gyr.
    kids_sum=np.zeros((8,n)); kids_samples=0
    shells=np.array([100,300])[:,None]/np.array([p['rs_kpc'] for p in params])[None,:]
    for step in range(nsteps):
        v+=.5*h[:,None,None]*acc
        x+=h[:,None,None]*v
        acc=acceleration(x)
        v+=.5*h[:,None,None]*acc
        t=t0+(step+1)*dt
        stop=np.searchsorted(tt,t,side='right')
        # Events at the same endpoint are processed sequentially, preserving repeated ids.
        for ev in range(cursor,stop):
            k=ids[ev]; dv=VK/np.sqrt(a)[:,None]*directions[ev]
            ework[:4,k]+=np.sum(v[:4,k]*dv,axis=1)+.5*np.sum(dv*dv,axis=1)
            v[:4,k]+=dv
        cursor=stop
        if step % max(1,round(.02/dt)) == 0:
            r=np.linalg.norm(x,axis=-1)
            inside=r<np.r_[anchors,anchors][:,None]
            if t>=tend-.5:
                sum_occ+=inside; nsamp+=1
            if t<t0+.5:
                early_occ+=inside; early_samples+=1
            if abs(t-age(.4))<.1:
                kids_sum+=(r>np.r_[shells[0],shells[0]][:,None]) & (r<np.r_[shells[1],shells[1]][:,None])
                kids_samples+=1
    occ=sum_occ/nsamp
    early=early_occ/max(early_samples,1)
    kids=kids_sum/max(kids_samples,1)
    final_e=specific_energy(x,v)
    # Work subtraction audits integration between vector kicks too.
    drift=np.abs(final_e-orig_e-ework)/np.maximum(np.abs(orig_e),.03)
    rows=[]
    for host in range(4):
        f=np.sum(w*occ[host])/np.sum(w*occ[host+4])
        # Stratified independent particle estimator; time samples are not independent draws.
        residual=w*(occ[host]-f*occ[host+4])
        variance=sum(len(z)*np.var(z,ddof=1) for z in np.split(residual,8))
        se=np.sqrt(variance)/np.sum(w*occ[host+4])
        cdrift=np.sum(w*occ[host+4])/np.sum(w*early[host+4])-1
        denom=np.sum(w*kids[host+4])
        kfrac=np.sum(w*kids[host])/denom if denom>0 else None
        kres=w*(kids[host]-kfrac*kids[host+4]) if denom>0 else np.zeros(n)
        kse=np.sqrt(sum(len(z)*np.var(z,ddof=1) for z in np.split(kres,8)))/denom if denom>0 else None
        rows.append(dict(host=params[host]['name'],retention=float(f),particle_se=float(se),
                         CI95_normal=[float(f-1.96*se),float(f+1.96*se)],
                         control_early_to_late_fractional_drift=float(cdrift),
                         energy_relative_median=float(np.median(drift[host+4])),
                         energy_relative_p99=float(np.quantile(drift[host+4],.99)),
                         energy_relative_max=float(np.max(drift[host+4])),
                         kicked_work_energy_p99=float(np.quantile(drift[host],.99)),
                         bound_weighted_fraction=float(np.sum(w*(final_e[host]<0))/w.sum()),
                         kids_shell_100_300kpc_z04_retention=None if kfrac is None else float(kfrac),
                         kids_shell_particle_se=None if kse is None else float(kse),
                         numerical_control_pass=bool(abs(cdrift)<.1 and np.quantile(drift[host+4],.99)<.01)))
    result=dict(n_per_host=n,seed=seed,dt_gyr=dt,steps=nsteps,elapsed_seconds=time.time()-begin,
                event_count=int(len(tt)),mean_kicks_realized=float(counts.mean()),
                zero_kick_fraction=float(np.mean(counts==0)),samples_final=nsamp,
                samples_kids=kids_samples,rows=rows)
    print(json.dumps(result),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--n',type=int,default=8192)
    parser.add_argument('--steps',default='0.002,0.001')
    parser.add_argument('--seeds',default='307011,307012')
    parser.add_argument('--analytic-only',action='store_true')
    args=parser.parse_args()
    result=dict(contract='C003 fixed650/G0; isotropic vector kicks; stationary energy-cut isotropic NFW tracers',
                python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                vk=VK,mean_kicks=MEAN,G0=G0,analytic=analytic_audit(),hosts=host_params())
    print(json.dumps(result),flush=True)
    if not args.analytic_only:
        eq=Equilibrium()
        result['Eddington_density_recovery']=eq.recovery
        print('Eddington density recovery '+json.dumps(eq.recovery),flush=True)
        result['runs']=[]
        for seed in map(int,args.seeds.split(',')):
            for dt in map(float,args.steps.split(',')):
                result['runs'].append(integrate(eq,args.n,seed,dt))
        result['all_numerical_controls_pass']=all(row['numerical_control_pass']
                                               for run in result['runs'] for row in run['rows'])
        # The scientific gate is separate from numerical execution success.
        result['spiral_gate']=all(r['rows'][0]['retention']<=.15 for r in result['runs'])
        result['cluster_gate']=all(.45<=r['rows'][3]['retention']<=.70 for r in result['runs'])
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
