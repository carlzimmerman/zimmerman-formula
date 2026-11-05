#!/usr/bin/env python3
"""Frozen numerical gates on already-authenticated single-grid sample records."""
import math
import numpy as np
import sampling3d as S
REQUIRED=[('plummer',32,4000.),('plummer',64,4000.),('plummer',128,4000.),('bullet',64,4000.),('bullet',128,4000.),('bullet',256,4000.),('bullet',256,8000.)]

def evaluate(records,foot,prerequisites_verified=False,mutate_grader=False):
    """Caller must authenticate files and prerequisite evidence; no I/O trust shortcut."""
    checks=[];lookup={};threshold=S.inherited_threshold(foot)
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def finite(value):return bool(np.all(np.isfinite(np.asarray(value,float))))
    check('prerequisite_evidence_verified',prerequisites_verified)
    try:
        for record in records:
            config=record['field_identity']['arguments'];key=(config['source'],config['n'],config['half_width'])
            check('unique_'+str(key),key not in lookup)
            check('footing_'+str(key),config['foot']==foot)
            lookup[key]=record
        check('exact_required_coverage',set(lookup)==set(REQUIRED))
        for key in REQUIRED:check('required_'+str(key),key in lookup)
        identities=[(r['field_identity']['source_hashes'],r['field_identity']['versions'],r['source_hashes'],r['mutate']) for r in records]
        check('consistent_engine_environment_mode',bool(identities) and all(v==identities[0] for v in identities))
        for key,r in lookup.items():
            name=str(key)
            check(name+'_production_status',r['status']=='SINGLE GRID ONLY')
            check(name+'_residual',r['finite'] and r['residual_eligible'] and finite(r['residual']) and 0<=r['residual']<=1e-8)
            check(name+'_ellipticity',finite(r['principal_min']) and r['principal_min']>0)
            check(name+'_threshold_identity',r['inherited_threshold']==threshold)
            check(name+'_norm_scale',finite(r['max_hessian_norm']) and r['max_hessian_norm']>0)
            tiny_line=64*np.finfo(float).eps*r['max_hessian_norm']
            if key[0]=='bullet':
                check(name+'_point_coverage',set(r['points'])==set(S.POINTS))
                check(name+'_disc_coverage',set(r['discs'])==set(S.POINTS))
                for point,position in S.POINTS.items():
                    v=r['points'][point]
                    check(name+'_'+point+'_position',v['position_kpc']==position)
                    check(name+'_'+point+'_finite_stable',finite([v['s'],v['norm']]) and not v['tiny'] and v['norm']>tiny_line)
                    ds=r['discs'][point]
                    check(name+'_'+point+'_quadrature_nodes',[(d['nr'],d['ntheta']) for d in ds]==[(32,64),(64,128)])
                    for i,d in enumerate(ds):
                        check(name+'_'+point+'_disc_finite_'+str(i),finite([d['mean_s'],d['on_fraction'],d['min_hessian_norm']]) and 0<=d['on_fraction']<=1 and d['tiny_samples']==0 and d['min_hessian_norm']>tiny_line)
                    mean_change=abs(ds[0]['mean_s']-ds[1]['mean_s']);fraction_change=abs(ds[0]['on_fraction']-ds[1]['on_fraction'])
                    check(name+'_'+point+'_disc_quadrature',mean_change<=.01 and fraction_change<=.01 and (ds[0]['mean_s']>=threshold)==(ds[1]['mean_s']>=threshold),dict(mean=mean_change,fraction=fraction_change))
            elif key[0]=='plummer':
                expected=S.plummer_oracle(foot);p=r['plummer']
                check(name+'_oracle_identity',r['oracle']==expected)
                complete=len(p['s'])==len(p['norm'])==len(p['tiny'])==70
                check(name+'_70_finite_samples',complete and finite(p['s']) and finite(p['norm']) and not any(p['tiny']) and min(p['norm'])>tiny_line)
                if complete and key[1]==128:
                    error=float(np.max(abs(np.asarray(p['s'])-np.asarray(expected['s']))))
                    check(name+'_oracle_error',error<=.02,error)
                    check(name+'_oracle_threshold_flags',np.array_equal(np.asarray(p['s'])>=threshold,expected['on']))
        if all(key in lookup for key in REQUIRED):
            coarse=lookup[('plummer',64,4000.)]['plummer']['s'];fine=lookup[('plummer',128,4000.)]['plummer']['s']
            if len(coarse)==len(fine)==70:
                change=float(np.max(abs(np.asarray(coarse)-fine)))
                check('plummer_64_128_pair',change<=.02,change)
                check('plummer_64_128_flags',np.array_equal(np.asarray(coarse)>=threshold,np.asarray(fine)>=threshold))
            else:check('plummer_64_128_pair',False)
            for label,a,b in [('resolution',('bullet',128,4000.),('bullet',256,4000.)),('box',('bullet',256,4000.),('bullet',256,8000.))]:
                a,b=lookup[a],lookup[b]
                for point in S.POINTS:
                    av,bv=a['points'][point]['s'],b['points'][point]['s'];change=abs(av-bv)
                    check(label+'_'+point+'_point',mutate_grader or change<=.02,change)
                    check(label+'_'+point+'_point_flags',(av>=threshold)==(bv>=threshold))
                    ad,bd=a['discs'][point][1],b['discs'][point][1]
                    mean_change=abs(ad['mean_s']-bd['mean_s']);fraction_change=abs(ad['on_fraction']-bd['on_fraction'])
                    check(label+'_'+point+'_disc',mean_change<=.03 and fraction_change<=.03,dict(mean=mean_change,fraction=fraction_change))
                    check(label+'_'+point+'_disc_flags',(ad['mean_s']>=threshold)==(bd['mean_s']>=threshold))
    except (KeyError,TypeError,ValueError,IndexError) as exc:
        check('valid_record_structure',False,type(exc).__name__+': '+str(exc))
    passed=all(c['passed'] for c in checks)
    reading=None
    if passed:
        fine=lookup[('bullet',256,4000.)]
        reading=S.threshold_reading({name:v['s'] for name,v in fine['points'].items()},threshold)
    return dict(footing=foot,numerical_status='PASS' if passed else 'UNDECIDED',checks=checks,failed=[c['name'] for c in checks if not c['passed']],conditional_reading=reading,scope='Conditional on authenticated inputs and known-answer prerequisites; numerical eligibility is not an observational lensing PASS or a healthy action. kappa=1/2 FITTED; not theory closed')
