#!/usr/bin/env python3
"""One saved, actual-code halo example; scientific figure, not new evidence coverage."""
import argparse
import csv
import json
import os
from pathlib import Path
import tempfile

os.environ['MPLCONFIGDIR']=tempfile.mkdtemp(prefix='mass-budget-mpl-')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'codex_mass_budget_2026_11_14/calculation/run_001'


def run(out):
    h=json.loads((BASE/'results.json').read_text())['constants']['h']
    a=np.load(BASE/'representative_profiles.npz')['canonical_z0_f3_i160']
    rr,source,bar,raw,cb,cr,ms,mj=a.T
    row=next(r for r in csv.DictReader((BASE/'halo_masses.csv').open()) if r['foot']=='canonical' and r['z']=='0.0' and r['f']=='3.0' and r['grid_index']=='160')
    R=rr/h*1000; b=bar/h; total=ms/h
    G=4.30091e-6; a0=9.3603e-11*3.0856775814913673e22/1e9
    valid=R>=1; R=R[valid];b=b[valid];total=total[valid]
    gn=G*b/R**2; exactbar=(gn+np.sqrt(gn**2+4*gn*a0))/2*R**2/G-b
    def epsilon(mass,baryons):
        g=G*mass/R**2;gb=G*baryons/R**2
        return g*g/(gb*(a0+g))-1
    eps_source=epsilon(total,source[valid]/h)
    eps_all=epsilon(total,b)
    eps_b=epsilon((bar[valid]+cb[valid])/h,source[valid]/h)
    rset=float(row['R_set_nominal_kpc'])
    charge=float(row['cosmic_patch_cold_Msun_h'])/h
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axs=plt.subplots(1,2,figsize=(12.4,5.2),gridspec_kw={'wspace':.30})
    ax=axs[0]
    ax.plot(R,raw[valid]/h/1e12,color='#9c3b10',lw=1.9,label='Raw law: retained central baryons')
    ax.plot(R,exactbar/1e12,color='#9c3b10',lw=1.5,ls=':',label='Raw law: all explicit Bar baryons')
    ax.plot(R,cb[valid]/h/1e12,color='#756bb1',lw=1.7,ls='--',label='Form B (already capped)')
    ax.plot(R,cr[valid]/h/1e12,color='#8296a5',lw=2.0,ls='-.',label='Cold reference')
    ax.plot(R,(ms[valid]-bar[valid])/h/1e12,color='#00796b',lw=2.1,label='Actual FZS1 / JNT2')
    ax.axhline(charge/1e12,color='#252525',lw=1,ls=':',label='Entire patch cold charge')
    ax.set(xscale='log',yscale='log',xlim=(1,R[-1]),ylim=(.004,20),ylabel=r'Enclosed cold mass ($10^{12}\,M_\odot$)',xlabel='Physical radius (kpc)',title='Enclosed charge and its finite budget')
    ax.legend(loc='upper left',fontsize=8.0,frameon=False,handlelength=2.6)
    ax=axs[1]
    ax.plot(R,eps_source,color='#00796b',lw=2.1,label='Actual joined: retained central source')
    ax.plot(R,eps_all,color='#00796b',lw=2.1,ls='--',label='Actual joined: all explicit Bar baryons')
    ax.plot(R,eps_b,color='#756bb1',lw=1.6,ls=':',label='Unscaled B: retained central source')
    ax.axhline(0,color='#252525',lw=1,label='Exact raw law')
    ax.set(xscale='log',xlim=(1,R[-1]),ylim=(-1.05,.55),xlabel='Physical radius (kpc)',ylabel=r'$\epsilon = g^2/[g_N(a_0+g)] - 1$',title='A local force-law test is separate')
    ax.legend(loc='upper left',fontsize=8.0,frameon=False)
    for ax in axs:
        ax.axvline(rset,color='#444444',lw=1,ls='--')
        ax.text(rset,.02,r'$R_{\rm set}$',transform=ax.get_xaxis_transform(),ha='right',va='bottom',fontsize=9,bbox={'facecolor':'white','alpha':.8,'edgecolor':'none','pad':1})
        ax.grid(True,which='major',alpha=.16)
    fig.suptitle('A conserved patch can change the force law',fontsize=16,y=.985)
    fig.text(.5,.915,r'One actual slow halo: canonical, $z=0$, $M_{200m}=10^{12}\,M_\odot/h$, $f=3$',ha='center',fontsize=11)
    fig.text(.5,.025,'Patch mass conserved to < 10⁻¹⁵. At R_set = 447.33 kpc, s = 0.6860; the raw retained-source charge exceeds the patch budget.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.82,bottom=.16,left=.08,right=.98)
    out.mkdir(parents=True,exist_ok=True)
    fig.savefig(out/'mass_budget_example.png',dpi=180)
    fig.savefig(out/'mass_budget_example.svg')
    (out/'figure_context.json').write_text(json.dumps({'profile_key':'canonical_z0_f3_i160','row':row,'nonclaim':'A single finite example, not population coverage. Bar is the complete modeled baryon profile in this galaxy-branch example.'},indent=2)+'\n')
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
