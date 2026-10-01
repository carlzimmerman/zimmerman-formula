"""Check independently recorded repeated solver run; deliberate mutation swaps an unequal-input run into repeat slot."""
import pathlib,json,os,sys
p=pathlib.Path(__file__).resolve().parent
j=json.loads((p/'convergence_results.json').read_text());runs=j['runs'];a=runs['N600_nb24'];mut=os.environ.get('MUTATE')=='1';b=runs['N600_tiny_spectrum_shift'] if mut else runs['repeat_N600_nb24']
checks={'same_input_arrays':a['initial_profile_sha256']==b['initial_profile_sha256'],'same_output_profiles':a['profile_sha256']==b['profile_sha256'],'same_conversion_budget':a['budget']==b['budget']}
out={'mutation':mut,'checks':checks,'compared_runs':['N600_nb24','N600_tiny_spectrum_shift' if mut else 'repeat_N600_nb24'],'scope':'Stored full-run input/output fingerprint and budget check; mutation misidentifies a perturbed-input run as a repeat'}
f=pathlib.Path(os.environ.get('CONVERGENCE_VERIFY_OUTPUT',str(p/('convergence_verify_MUTATE.json' if mut else 'convergence_verify.json'))));f.write_text(json.dumps(out,indent=2))
for k,v in checks.items():print('PASS' if v else 'FAIL',k)
sys.exit(0 if all(checks.values()) else 1)
