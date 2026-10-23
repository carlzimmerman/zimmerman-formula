"""Long homogeneous control; excludes fragmentation and is not a relic calculation."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
s=json.loads((P/'screening_exit_bound_v2_run/results.json').read_text());A=s['probe']['X_envelope_GeV'];a=s['probe']['a']
m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292
Om=np.sqrt(2*g*A);F=Om/np.sqrt(lam);mp=m/Om;mx=M/Om;c=g/(np.sqrt(2)*lam*F);unit=Om**4/lam
E=s['radiation_energy_constant_GeV4']/a**4/unit;period=2*np.pi/mx;rows={}
for name,angle,kinfrac,dt in [('radial',0.,0.,.02),('mixed',np.pi/4,0.,.02),('kinetic',np.pi/4,1.,.02),('time',np.pi/4,0.,.01)]:
    q=np.zeros(4);v=np.zeros(4);r2=4*(1-kinfrac)*E/(mp*mp+np.sqrt(mp**4+4*(1-kinfrac)*E)) if kinfrac<1 else 0
    q[:2]=np.sqrt(r2)*np.array([np.cos(angle),np.sin(angle)])
    v[:2]=np.sqrt(2*kinfrac*E)*np.array([np.cos(angle),np.sin(angle)])
    v[2]=mx*np.sqrt(2)*A/F
    end=round(1000*period/dt)*dt
    ip=O/(name+'_initial.bin');op=O/(name+'_final.bin');hist=O/(name+'.csv')
    np.concatenate(([1,32,dt,end,0,mp,mx,c,1],q,v)).astype('<f8').tofile(ip)
    subprocess.run([str(P/'late_conversion_lattice'),str(ip),str(hist),str(op)],check=True)
    h=np.genfromtxt(hist,delimiter=',',names=True)
    ex=h['X_kinetic']+h['X_potential'];ep=h['phi_kinetic_physical']+h['phi_potential'];t=h['z']/period
    # Reversible valley energy is an exact fixed-X minimum, not a time average.
    Xabs=np.sqrt(h['X_mean_physical_squared']/2)*F
    depth=np.maximum(2*g*Xabs-m*m,0)**2/(4*lam)/unit
    exc=ep+h['interaction']+depth
    windows={}
    for lo,hi in [(0,4),(90,100),(990,1000)]:
        sel=(t>=lo)&(t<=hi)
        windows[str(hi)]={'mean_X_loss':float(np.mean(1-ex[sel]/ex[0])), 'mean_energy_above_valley_over_X':float(np.mean(exc[sel]/ex[0])), 'max_X_loss':float(np.max(1-ex[sel]/ex[0]))}
    rows[name]={'windows':windows,'energy_error':float(np.max(abs(h['Econf']-h['Econf'][0]))/ex[0]),'charge_error':float(np.max(abs(h['charge']-h['charge'][0]))),'min_excitation_energy':float(exc.min()),'final_X_loss':float(1-ex[-1]/ex[0])}
    print(name,json.dumps(rows[name]),flush=True)
checks={'energy_below_1e-6':all(x['energy_error']<1e-6 for x in rows.values()),'charge_below_1e-7':all(x['charge_error']<1e-7 for x in rows.values()),'positive_energy_above_valley':all(x['min_excitation_energy']>-1e-10 for x in rows.values())}
out={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'cases':rows,'scope':'Homogeneous neutral conditional states for 1000 X cycles. No spatial fragmentation, no quantum collision closure, no cosmological continuation.'};(O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
