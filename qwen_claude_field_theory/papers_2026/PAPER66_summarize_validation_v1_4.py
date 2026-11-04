#!/usr/bin/env python3
"""Summarize fresh mock validation without replacing historical prediction tables."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
V = ROOT/'reviews/alma_readiness_2026_11_04/revision_v1_4'


def truth(radius, pressure):
    # Exactly the generating curve in ac1_score.spec: V_PB(3)=430, sigma0=40, Rt=.5.
    rdg = 1.56/1.678
    vf = math.sqrt(430**2-2*40**2*3/rdg)/(2/math.pi*math.atan(3/.5))
    rot = vf*2/math.pi*math.atan(radius/.5)
    return math.sqrt(rot**2+2*40**2*radius/rdg) if pressure=='P-B' else rot


def main():
    artifacts = {}
    def read(path):
        artifacts[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text())
    st=read(V/'selftest/ac1_score_selftest_results.json')
    summary={'selftest':st['checks'],'suites':{},'artifact_sha256':artifacts,
             'note':'New validation, not changed frozen predictions. RMS and coverage use the generating curve at each scored radius, separately by pressure/inclination.'}
    lines=[]
    for label,file in [('archive','power_archive/ac1_score_power_results.json'),('sister-like','power_sister/ac1_score_power_div2.54_condorbeam_results.json')]:
        data=read(V/file); oldname='ac1_score_power_results.json' if label=='archive' else 'ac1_score_power_div2.54_condorbeam_results.json'
        old=read(ROOT/'rebuild_2026_10_22/AC1_alma_condor_predictions'/oldname)
        classes={}
        for kind,rows in data['runs'].items():
            metrics={}
            for inc in ('incl-mom0','incl-Tadaki'):
                fits=[r['fit_diagnostics'][inc] for r in rows if inc in r['fit_diagnostics'] and r['fit_diagnostics'][inc]['valid']]
                for pressure,key in [('P-B','Vc_PB'),('P0','Vc_P0')]:
                    residuals=[(f['V'][key]/truth(f['R_score'],pressure)-1) for f in fits]
                    covered=[abs(f['V'][key]-truth(f['R_score'],pressure))<=f['error_calibration'][pressure]['error'] for f in fits]
                    metrics[inc+'|'+pressure]=dict(n=len(fits),rms_fraction=math.sqrt(sum(x*x for x in residuals)/len(residuals)) if fits else None,bias_fraction=sum(residuals)/len(residuals) if fits else None,covered=sum(covered))
            new_valid=sum(r['valid'] for r in rows); old_valid=sum(r['valid'] for r in old['runs'][kind])
            classes[kind]=dict(N=len(rows),detections=sum(r['det'] for r in rows),valid_primary=new_valid,historical_valid_primary=old_valid,metrics=metrics)
            lines.append(f"{label} & {kind.replace('realistic','smooth')} & {sum(r['det'] for r in rows)}/6 & {old_valid}/6 & {new_valid}/6 \\\\")
        summary['suites'][label]=classes
    (V/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    n=sum(bool(x) for _,x in st['checks']); nt=len(st['checks'])
    ac=summary['suites']['archive']['compact']['metrics']
    ss=summary['suites']['sister-like']['realistic']['metrics']
    sc=summary['suites']['sister-like']['compact']['metrics']
    def metric(group,key):
        m=group[key]
        return f"{100*m['rms_fraction']:.1f}\\,\\% RMS, truth within the reported error in {m['covered']}/{m['n']} accepted fits"
    coverage=(r"\textbf{Recovery and error coverage.} At archive noise the compact Tadaki P-B branch has "
              +metric(ac,'incl-Tadaki|P-B')+r"; the compact moment-0 P-B branch has "
              +metric(ac,'incl-mom0|P-B')+r". In the sister-like suite the smooth Tadaki P-B branch has "
              +metric(ss,'incl-Tadaki|P-B')+r", and the compact Tadaki P-B branch has "
              +metric(sc,'incl-Tadaki|P-B')+r". The sister-like compact moment-0 P-B branch still has "
              +metric(sc,'incl-mom0|P-B')+r". These small-sample frequencies are descriptive, not a coverage calibration. Passing the fit gate does not remove inclination bias. Consequently the fixed-floor intervals and the labels ``consistent''/``in tension'' are operational diagnostics, not calibrated confidence statements or model exclusions.")
    text=r''' \section{Validation of the repaired scorer}\label{s:validation}
The corrected code passes six regression tests covering disagreeing or missing starts, invalid speeds, the 15\,\% boundary, the fixed error floor, and refusal to overwrite historical outputs. The end-to-end five-class selftest passes SELFTEST, including the velocity-axis mutation. No release data enter these checks.

\begin{table}[ht]\centering\small
\caption{Fresh six-seed suites, primary Tadaki-inclination P-B branch. Historical columns retain the earlier code's validity counts; they do not include the separate selftest seed. The sister-like rerun uses the quoted rounded forecast beam (0.109 by 0.085 arcsec); exact command arguments are retained with the run record. These are validation results, not new physical predictions.}
\begin{tabular}{llccc}\toprule
Noise/beam & Disc & Detected & Old fit valid & Corrected fit valid \\ \midrule
ROWS
\bottomrule\end{tabular}\end{table}

COVERAGE

The archived 8.9\,\% floor is retained, not refitted on these outcomes. The validation record reports bias, fractional RMS and empirical error coverage for every accepted inclination/pressure branch against the generating curve at the radius actually scored. It keeps a poorly recovered or rejected branch visible. Six noise seeds per case cannot establish general confidence coverage. The two power suites retain the original generating speed, flux and smooth/compact shapes; clumpy gas, bulges and a broad velocity grid remain untested. Detection and fit validity are distinct, and an accepted numerical fit alone does not establish that a real galaxy is a thin disc.
'''.replace('SELFTEST',f'{n}/{nt} checks').replace('ROWS','\n'.join(lines)).replace('COVERAGE',coverage)
    (HERE/'PAPER66_validation_v1_4.tex').write_text(text)
    print(json.dumps({k:{c:(d['detections'],d['valid_primary']) for c,d in v.items()} for k,v in summary['suites'].items()},indent=2))

if __name__=='__main__':
    main()
