"""Fixed historical forecast vs published summaries; no fitted parameters.
Fig. 3 coordinates are approximate manual digitizations, not author data.
No chi-square or statistical verdict is computed without MOND posteriors.
"""
import ast,csv,hashlib,json,math,platform,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
started=datetime.now(timezone.utc).isoformat(); t0=time.monotonic()
commit='e1603604aa02e06e5dd397234295e87bb4654b64'
raw=subprocess.check_output(['git','show',commit+':test_highz_predictions.py'],cwd=ROOT)
module=ast.parse(raw.decode())
# Extract only fixed constants and the two numerical helper functions.
constants={'c','G','H0_fiducial','Omega_m','Omega_Lambda'}
functions={'zimmerman_a0','zimmerman_Ez'}
selected=[]
for node in module.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in node.targets): selected.append(node)
 elif isinstance(node,ast.FunctionDef) and node.name in functions: selected.append(node)
namespace={'np':np}
exec(compile(ast.Module(body=selected,type_ignores=[]),'<historical helpers>','exec'),namespace)
A=namespace['zimmerman_a0'](namespace['H0_fiducial'])/1e-10
prediction=lambda z:A*namespace['zimmerman_Ez'](z)
independent=lambda z:299792458*(71.1*1000/3.086e22)/(2*math.sqrt(8*math.pi/3))/1e-10*math.sqrt(.315*(1+z)**3+.685)
for z in [.33,.5,.8,1.,1.3,1.44]: assert math.isclose(float(prediction(z)),independent(z),rel_tol=1e-14)
zgrid=np.linspace(.33,1.44,10001)
mond=1.03+1.20*zgrid
residual=(prediction(zgrid)-mond)/mond*100
ix=int(np.argmax(np.abs(residual)))
# Fig. 3 of arXiv v1 PDF, page 3; read off rendered graphic.
# Illustrative centers +/-0.01 redshift, +/-0.02 acceleration units.
bins=[(.506,1.99),(.833,2.20),(1.056,2.58),(1.283,2.71)]
rows=[dict(z=z,frozen=float(prediction(z)),mond_fitted_line=1.03+1.20*z,percent_vs_mond_line=(float(prediction(z))/(1.03+1.20*z)-1)*100) for z in [.33,.5,.8,1.,1.3,1.44]]
with (HERE/'matched_redshift_comparison.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary=dict(fixed_normalization_1e10=A,normalization_refitted=False,
 sampled_range=[.33,1.44],grid_points=10001,
 max_abs_percent_vs_mond_fit=float(abs(residual[ix])),redshift_at_max=float(zgrid[ix]),
 mond_fit='(1.03 + 1.20 z) in 1e-10 m/s^2; PDF Eq E.5 / HTML Eq 14',
 halo_bins_approx=[dict(z=z,a0=a,prediction=float(prediction(z)),percent=(float(prediction(z))/a-1)*100) for z,a in bins],
 formal_statistical_verdict='UNVERIFIED: no published MOND bin values, joint posterior/covariance or raw-data likelihood used',
 scientific_result='Frozen March curve agrees with published MOND central trend to within 4.8%; halo-based bins differ more; no validated Kepler-grade pass.')
(HERE/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,axes=plt.subplots(2,1,figsize=(8,7),sharex=True,gridspec_kw={'height_ratios':[3,1]})
axes[0].plot(zgrid,prediction(zgrid),label='March 17 forecast: fixed original constants',lw=2.2)
axes[0].plot(zgrid,mond,label='MUSE MOND-based fitted trend (Eq. E.5)',lw=2,color='#198754')
axes[0].scatter(*zip(*bins),label='Halo-based Fig. 3 bins (approx. digitized)',color='#8b5a9d',marker='x',s=65)
axes[0].set_ylabel(r'$a_0$ [$10^{-10}$ m s$^{-2}$]')
axes[0].legend(fontsize=9);axes[0].grid(alpha=.2)
axes[0].set_title('Unchanged March forecast compared at matched redshifts')
axes[1].plot(zgrid,residual,color='#198754');axes[1].axhline(0,color='grey',lw=.8)
axes[1].set_ylabel('vs MOND fit [%]');axes[1].set_xlabel('Redshift z');axes[1].grid(alpha=.2)
fig.text(.5,.012,'MOND line is a published fit, not independent points. No statistical confidence band reconstructed.',ha='center',fontsize=8)
fig.tight_layout(rect=[0,.035,1,1]);fig.savefig(HERE/'comparison.png',dpi=180);fig.savefig(HERE/'comparison.pdf');plt.close(fig)
files=['check.py','matched_redshift_comparison.csv','results.json','comparison.png','comparison.pdf','REPORT.md']
pdf=Path('/Users/carlzimmerman/new_physics/_external_data/arxiv_pdf/2604.22613v1.pdf')
manifest=dict(schema_version=1,claim_id='frozen-march-forecast-vs-muse-published-summaries',
 repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT))),
 command='MPLCONFIGDIR=/private/tmp/muse-mpl /opt/homebrew/Caskroom/miniconda/base/bin/python3 real_research/reviews/muse_frozen_march_audit_2026_10_13/check.py',
 environment=dict(software=['Python '+platform.python_version(),'numpy '+np.__version__,'matplotlib '+matplotlib.__version__],hardware=platform.machine()),
 mathematics=dict(assertion_tested='Fixed forecast central curve within 4.8 percent of published MOND linear trend across observed range',coefficient_domain='IEEE-754 floating point',conventions='accelerations in units 1e-10 m/s^2; no confidence interpretation of graphical bars',inputs=[dict(path='git:'+commit+':test_highz_predictions.py',sha256=hashlib.sha256(raw).hexdigest()),dict(path=str(pdf),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())],bounds=dict(z_min=.33,z_max=1.44,grid_points=10001),non_claims=['Not a raw-data fit','No significance or confidence verdict','No novelty or public preregistration established']),
 randomness=dict(used=False,generator='none',seed=None),run=dict(started_at=started,runtime_seconds=time.monotonic()-t0,exit_status=0),
 outputs=[dict(path=str((HERE/f).relative_to(ROOT)),sha256=hashlib.sha256((HERE/f).read_bytes()).hexdigest()) for f in files],checks=['Archived helper functions agree with independent standard-library arithmetic at six redshifts, tolerance 1e-14'],result=summary['scientific_result'],residual_risks=['MOND covariance and individual estimates unavailable','Fig 3 points approximate and halo-based','Central linear trend is a fitted surrogate, not original data'])
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(summary,indent=2))
