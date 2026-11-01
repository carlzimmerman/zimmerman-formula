"""All ten finite vacuum graph classes on the canonical SU5 valley.

The reduced two-loop coefficient additionally includes heavy displacement.
No RG-resummed logarithm is added to the explicit finite two-loop result.
"""
import sys,math
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'two_loop'))
sys.path.insert(0,str(BASE/'master_integrals'))
from model import build_model,graph_weights
from master_integrals import fSSS,fSS,fFFS,fbarFFS
from vertices import gauge_parts,evaluate_weights
ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'reviews/quantum_matching_2026_11_01/rg_threshold'))
from relaxation import normal_data
LOOP=16*math.pi**2


def nonvector(data,Q2):
    w=graph_weights(data)
    sm=np.array([p['mass2'] for p in w['scalar_groups']]);fm=np.array([p['mass2'] for p in w['fermion_groups']])
    out={};diag={}
    for name,masses,fun in [('SSS',[sm,sm,sm],fSSS),('SS',[sm,sm],fSS),
                            ('FFS',[fm,fm,sm],fFFS),('barFFS',[fm,fm,sm],fbarFFS)]:
        out[name],ab,terms=evaluate_weights(w[name],masses,fun,Q2)
        diag[name]={'absolute_sum':ab,'nonzero_mass_group_terms':terms}
    return out,diag


def calculate(X,h,lam,g,f,Q2,heavy=True):
    data=build_model(X,h,lam,g,f,vertices=True)
    p,diag=nonvector(data,Q2)
    gp=gauge_parts(data['z'],data['R'],g,data['mS2'],data['O'],data['mF'],data['U'],data['mV2'],data['Ov'],Q2)
    p.update(gp['parts']);diag.update(gp['diagnostic'])
    v1=0.
    for weight,m2 in [(1,data['mS2']),(-2,data['mF2']),(3,data['mV2'])]:
        positive=m2[m2>0]
        v1+=weight*float(np.sum(positive**2*(np.log(positive/Q2)-1.5)))/4
    v2=sum(p.values())
    out={'X':float(X),'h':float(h),'lambda':float(lam),'g':float(g),'f':float(f),'Q2':float(Q2),
         'V0':float(np.vdot(data['F'],data['F']).real),'V1_coefficient':v1,
         'CW':v1/LOOP,'V2_diagrams_coefficient':v2,'V2_diagrams':v2/LOOP**2,
         'diagram_parts_coefficient':p,'diagram_diagnostic':diag,
         'model_controls':data['controls'],'gauge_controls':gp['controls'],
         'mass_group_counts':gp['mass_group_counts']}
    if heavy:
        nd=normal_data(X,[h,lam,g,f],math.sqrt(Q2))
        out.update(normal_data=nd,deltaU_heavy=nd['deltaU_vac'],
                   V2_reduced_coefficient=v2+nd['deltaU_vac']*LOOP**2,
                   V2_reduced=v2/LOOP**2+nd['deltaU_vac'],
                   F_tree=nd['F0'],deltaF_heavy=nd['deltaF_angular'],
                   J_heavy=nd['F_b']**2/nd['Hbb'])
    return out
