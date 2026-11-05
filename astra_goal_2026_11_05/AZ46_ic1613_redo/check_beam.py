#!/usr/bin/env python3
"""Beam-only known-answer and deliberately wrong robust-beam checks."""
import hashlib,json,math
from pathlib import Path
import numpy as np
import io_beam as B
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DATA=ROOT.parent/'_external_data/fn4a_ic1613_2026_11'
def run(mutate=False):
    checks=[];rows=[];headers={}
    def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
    beams={}
    for weight in ['NA','R']:
        header,_=B.metadata(DATA/f'IC1613_{weight}_ICL001.FITS');beam=B.clean_beam(header);beams[weight]=beam
        headers[weight]=hashlib.sha256(header.tostring().encode()).hexdigest()
    # Independent anchor values from the pre-freeze diagnostic's CLEAN records.
    anchors=json.loads((HERE/'diagnosis.json').read_text())['header_evidence']
    for weight in ['NA','R']:
        truth=np.array(anchors[f'IC1613_{weight}_ICL001.FITS']['beam_arcsec_deg'])
        beam=beams['NA'] if mutate and weight=='R' else beams[weight]
        check(weight+'_CLEAN_header',np.array_equal(beam,truth),dict(used=beam.tolist(),expected=truth.tolist()))
        p=math.radians(truth[2]);major=np.array([math.sin(p),math.cos(p)]);minor=np.array([-math.cos(p),math.sin(p)])
        sigma=truth[:2]/math.sqrt(8*math.log(2))
        for pix in [3.,6.]:
            expected=sigma**2+pix**2/12;moments=[]
            for sub in [5,9]:
                k=B.beam_kernel(128,128,pix,beam,sub)
                y,x=np.meshgrid(np.fft.fftfreq(128)*128*pix,-np.fft.fftfreq(128)*128*pix,indexing='ij')
                u=x*major[0]+y*major[1];v=x*minor[0]+y*minor[1]
                observed=np.array([np.sum(k*u*u),np.sum(k*v*v)])
                err=abs(observed/expected-1);moments.append(observed)
                check(f'{weight}_pix{pix}_sub{sub}_moments',np.max(err)<=.02,dict(relative=err.tolist(),observed=observed.tolist(),expected=expected.tolist()))
                check(f'{weight}_pix{pix}_sub{sub}_DC',abs(k.sum()-1)<=1e-12,float(k.sum()-1))
            rows.append(dict(weight=weight,pixel_arcsec=pix,second_moment_change=(abs(moments[0]/moments[1]-1)).tolist()))
    return dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),pairs=rows,header_hashes=headers,mutate=mutate,
                scope='Beam numerical controls only; both a0 footings share this geometry; no local-cube verdict; kappa=1/2 FITTED; not theory closed',
                source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(B.__file__),HERE/'FROZEN_CRITERIA.md']})
if __name__=='__main__':
    main=run();mut=run(True)
    for name,obj in [('beam_checks.json',main),('mutate/beam_checks.json',mut)]:B.atomic(HERE/name,obj)
    main_header=next(c['passed'] for c in main['checks'] if c['name']=='R_CLEAN_header')
    mut_header=next(c['passed'] for c in mut['checks'] if c['name']=='R_CLEAN_header')
    bite=main_header and not mut_header
    print(json.dumps(dict(main_passed=main['passed'],main_total=main['total'],mutation_bites=bite,failed=[c['name'] for c in main['checks'] if not c['passed']]),indent=2))
    raise SystemExit(int(main['passed']!=main['total'] or not bite))
