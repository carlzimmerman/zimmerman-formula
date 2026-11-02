#!/usr/bin/env python3
"""DA1: reruns of K and X on FG1's inputs, using CRG1's clean-room code (a scratch copy; DA1_CRG points to it, CRG1's inputs symlinked), so no other lane is written. Parts: gas grid (D1), data-side definitions (D2), R500 and X-COP h brackets (D6). DA1_KIDS: directory with zb.npy, w.npy (one in 20 used, as M3A1). kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework."""
import io, json, math, os, sys, tarfile
CRG=os.environ['DA1_CRG']; sys.path.insert(0,CRG); sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); REPO=os.path.dirname(RB)
os.chdir(CRG)
import numpy as np
import crg1_clusters as C
from scipy.interpolate import PchipInterpolator
OUT=[]
def P(s): print(s,flush=True); OUT.append(str(s))
D=C.Data(); ST=C.stacks(); CSS=C.all_css(); HN={0.672:'h0672',0.686:'h0686'}
def cell_C1(fs,gd,tag=''):
    return lambda h: C.load_or_build(f"DA1{tag}_C1_f{fs:g}_g{gd:g}_h{h}",C.fn_C1(D,ST,CSS,h,fs,gd))
def summ(cf,Vk='V',vCk='vC_own_canonical',foot='canonical',mode='template',fac=None,B1=False,noleak=False):
    tabs={}
    for h,_,_,hn in C.HS:
        d=cf(h); M=C.Meas(D,h)
        if B1:
            b=M.g['Bst'][None,:]
            for a in ('n','nraw','nx','nRR'): setattr(M,a,getattr(M,a)/b)
        if fac is not None:
            f=fac(hn)
            for a in ('n','nraw','nx','nRR'): setattr(M,a,getattr(M,a)*f)
        tabs[hn]=C.keys_table(M,d[Vk],d[vCk],foot,mode)
    s=C.k_summary(tabs); s['tables']=tabs; return s
def line(lab,s):
    w=max(((abs(v['Z']),k,hn,v['Z']) for hn,t in s['tables'].items() for k,v in t.items())); m3=[s['tables'][h]['G-OUT-M3']['Z'] for h in ('h0672','h0686')]; gi=[s['tables'][h]['G-IN-Mall']['Z'] for h in ('h0672','h0686')]
    P(f"  {lab}: {s['n_pass']} of 15, over 2: {','.join(s['failing']) or 'none'}; worst {w[1]} {w[3]:+.2f}; G-OUT-M3 {m3[0]:+.2f}/{m3[1]:+.2f}; G-IN-Mall {gi[0]:+.2f}/{gi[1]:+.2f}")
    return dict(lab=lab,n_pass=s['n_pass'],failing=s['failing'],worst=[w[1],w[3]],M3=m3,GIN=gi,Z={h:{k:v['Z'] for k,v in t.items()} for h,t in s['tables'].items()},A={h:{k:v['A'] for k,v in t.items()} for h,t in s['tables'].items()},pred={h:{k:v['pred'] for k,v in t.items()} for h,t in s['tables'].items()})
RES={}
# ---- check against ZN4
zn=json.load(open(os.path.join(RB,'ZN4_cluster_resolution','zn4_results.json')))['runs']['f* 0.034, gas +0.005']['cells']
base=summ(cell_C1(0.034,0.005)); dz=max(abs(base['tables'][h][k]['Z']-zn[h][k]['Z']) for h in zn for k in zn[h]); P(f"K-rerun: C1 f* 0.034, gas +0.005 against ZN4's JSON: max |dZ| {dz:.4f}"); RES['check_vs_ZN4']=dz
if dz>0.02: sys.exit('harness does not reproduce ZN4')
# ---- gas grid
P("D1 gas grid, C1 and C3's K, canonical"); RES['gas']={}
for gd in (0.005,0.023,0.032,0.072,0.092,0.099,0.111,0.117,0.129):
    for fs in (0.034,0.0615): RES['gas'][f'{gd}|{fs}']=line(f"gas {gd:+.3f}, f* {fs}",summ(cell_C1(fs,gd)))
# ---- n(z)
PCH=PchipInterpolator(np.r_[0,0.295,[0.510,0.706,0.934,1.321,1.484,2.330]],np.r_[0,np.sqrt(7.942**3/(0.295*(21.863+(21.863-19.455)/(0.706-0.510)*(0.510-0.295)))),[13.588,17.351,21.576,27.601,30.512,38.988]])
HV={'h0672':0.672,'h0686':0.686}; DM=lambda z,h:PCH(np.minimum(np.asarray(z,float),2.33))*101.54/HV[h]
NZ={}
with tarfile.open(os.path.join(os.path.dirname(REPO),'_external_data','kids_lensing_zsplit','KiDS1000_SOM_N_of_Z.tar.gz')) as tf:
    for m in tf.getmembers():
        if m.name.endswith('_Nz.asc'): a=np.loadtxt(io.TextIOWrapper(tf.extractfile(m))); NZ[int(m.name.split('TOMO')[1][0])]=(a[:,0],a[:,1])
KD=os.environ['DA1_KIDS']; zb=np.load(os.path.join(KD,'zb.npy'),mmap_mode='r')[::20].astype(float); w=np.load(os.path.join(KD,'w.npy'),mmap_mode='r')[::20].astype(float); TB=[0.1,0.3,0.5,0.7,0.9,1.2]
def isc(zl,zs,h): DlM=float(DM(zl,h)); DMs=DM(zs,h); return np.clip((DMs-DlM)/DMs,0,None)*DlM/(1+zl)
def F(zl,h,whole_bins_only=False):
    s=(zb>zl+0.2)&(zb<=1.2); i=isc(zl,zb[s],h); t_=np.digitize(zb[s],TB); it=i.copy()
    for t in range(1,6):
        if whole_bins_only and TB[t-1]<zl+0.2: continue   # a bin the Z_B cut slices keeps its point Z_B
        zz,nn=NZ[t]; it[t_==t]=np.trapz(nn*isc(zl,zz,h),zz)/np.trapz(nn,zz)
    return float((w[s]*i**2).sum()/(w[s]*i*it).sum())
GR=np.array([0.05,0.1,0.2,0.3,0.4,0.5,0.6]); FA={h:np.array([F(z,h) for z in GR]) for h in HV}; FB={h:np.array([F(z,h,True) for z in GR]) for h in HV}
P(f"F(z_l), h 0.672, z {GR.tolist()}: full bin n(z) {np.round(FA['h0672'],3).tolist()}; only bins wholly above the cut {np.round(FB['h0672'],3).tolist()} (M3A1 printed 1.021 1.038 1.089 1.114 1.149 1.139 to z 0.5)"); RES['F']={k:v.tolist() for k,v in FA.items()}; RES['F_whole']={k:v.tolist() for k,v in FB.items()}
fac=lambda T:(lambda hn:np.interp(D.z,GR,T[hn])[:,None]); M1=lambda v:(lambda hn:np.full((D.N,1),v))
c1=cell_C1(0.034,0.005); c1b=cell_C1(0.0615,0.005); c1x=cell_C1(0.034,0.111)
c2=lambda h:C.load_or_build(f"C2_h{h}",None); c4=lambda h:C.load_or_build(f"C4_h{h}",None)
P("D2 data-side definitions"); RES['D2']={}
for cn,cf,kw in (('C1,C3 f* .034',c1,{}),('C1,C3 f* .0615',c1b,{}),('C1,C3 f* .034 gas +.111',c1x,{}),('C2',c2,{}),('C4 canonical one-template',c4,dict(Vk='V_canonical')),('C4 alt one-template',c4,dict(Vk='V_alt',vCk='vC_own_alt',foot='alt'))):
    r={}; P(' '+cn)
    r['base']=line('as chain',summ(cf,**kw)); r['nz']=line('bin n(z) in Sigma_crit (KiDS form), F',summ(cf,fac=fac(FA),**kw)); r['nz_whole']=line('n(z) only in bins wholly above the cut',summ(cf,fac=fac(FB),**kw)); r['B1']=line('boost B = 1',summ(cf,B1=True,**kw)); r['nzB1']=line('n(z) and B = 1',summ(cf,fac=fac(FA),B1=True,**kw))
    r['m+']=line('m +0.014 in place of -0.01 (Brouwer+21 prints 0.014, sign not shown)',summ(cf,fac=M1(0.99/1.014),**kw)); r['m-']=line('m -0.014',summ(cf,fac=M1(0.99/0.986),**kw)); RES['D2'][cn]=r
# ---- R500 bracket: same gas, the aperture moved. Radius lower by dex, gas read at that radius by slope 1.19
P("D6 eRASS1 R500 (LCDM cosmology run), C1 f* .034, gas +0.005: same gas, R500 lower by dex"); RES['R500']={}
RO,MO=D.R500.copy(),D.Mgas.copy()
for dx in (0.05,0.075,0.10):
    D.R500=RO*10**-dx; D.Mgas=MO*10**(-dx*1.19)
    cf=lambda h,dx=dx:C.fn_C1(D,ST,CSS,h,0.034,0.005)()
    tab={h:cf(h) for h,*_ in C.HS}; RES['R500'][str(dx)]=line(f"R500 -{dx} dex",summ(lambda h:tab[h]))
D.R500,D.Mgas=RO,MO
# ---- X-COP at native h
P("D6 X-COP's published (70, 0.3) masses and radii against the native chain: C1 f* .034"); XC=C.xcop_load(); o=C.x_cell(XC,ST,'C1',0.034); P(f"  as chain: mean {o['mean']:+.3f}, rms {o['rms']:.3f}, passed {o['passed']}"); RES['X']=dict(chain=o)
def DAq(z,hn=0.6856427,Om=0.2976016):
    x=np.linspace(0,z,400); a=np.trapz(1/np.sqrt(0.3*(1+x)**3+0.7),x)/70; b=float(PCH(min(z,2.33)))*101.54/hn*hn/100/ (299792.458/100) if False else float(PCH(min(z,2.33)))*101.54/hn/299792.458
    return b/a
XN=[]
for c in XC:
    q=DAq(c['z']); n=dict(c); n['R500']=c['R500']*q; n['hr']=c['hr']*q; n['gr']=c['gr']*q; n['sr']=c['sr']*q; n['hm']=c['hm']*q; n['gm']=c['gm']*q**2.5; n['sm']=c['sm']*q**2; XN.append(n)
P(f"  q = D_A native / D_A(70,0.3): {[round(DAq(c['z']),4) for c in XC]}")
o2=C.x_cell(XN,ST,'C1',0.034); P(f"  all scaled to native D_A: mean {o2['mean']:+.3f}, rms {o2['rms']:.3f}, passed {o2['passed']}"); RES['X']['native']=o2
o3=C.x_cell(XC,ST,'C2',0.034,nr=C.get_nr('a')); o4=C.x_cell(XN,ST,'C2',0.034,nr=C.get_nr('a')); P(f"  C2: chain mean {o3['mean']:+.3f} rms {o3['rms']:.3f} {o3['passed']}; native {o4['mean']:+.3f} rms {o4['rms']:.3f} {o4['passed']}"); RES['X']['C2']=o3; RES['X']['C2_native']=o4
json.dump(RES,open(os.path.join(HERE,'da1_keys.json'),'w'),indent=1,default=float); open(os.path.join(HERE,'da1_keys.out'),'w').write('\n'.join(OUT)+'\n')
