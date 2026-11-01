import json,sys
from pathlib import Path
from orbits import harmonic_control

def main():
    out=Path(sys.argv[1]);r=harmonic_control()
    errors=[row[key] for row in r['orbits'] for key in ('Omega_r_relative_error','Omega_phi_relative_error','r_squared_scaled_error','invariant_residual')]
    errors+=r['shell_measure']['relative_errors']
    r['maximum_relevant_error']=max(errors);r['passed']=max(errors)<2e-6
    (out/'result.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'passed':r['passed'],'maximum_error':max(errors)}))
    if not r['passed']:raise SystemExit(1)
if __name__=='__main__':main()
