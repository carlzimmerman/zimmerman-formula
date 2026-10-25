"""Necessary relative-acceleration condition for CCT's selective Xi coupling.
No Milky Way baryonic mass is assumed or observational verdict issued.
"""
import pathlib,json,csv,hashlib,math
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];mf=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json';cat=ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv';bridge=ROOT/'sol61_push/continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md';files=[pathlib.Path(__file__),mf,cat,bridge]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();models=json.loads(mf.read_text())['models'];data={r['name']:r for r in csv.DictReader(cat.open())};G=.00430091;a0s={'canonical':9.3603e-11*3.085677581491367e10,'alt':1.1312e-10*3.085677581491367e10};rows=[]
for m in models:
 name=m['name'];R=float(data[name]['distance_gc'])*1000;Mc=m['cold_mass'];Ms=m['stellar_mass'];b=m['cold_scale_pc'];gcmax=2/(3*math.sqrt(3))*G*Mc/b**2;A=(1+Ms/Mc)*gcmax
 for foot,a0 in a0s.items():
  threshold=None if A>=a0 else R*R/G*A*A/(a0-A)
  rows.append({'name':name,'footing':foot,'Galactocentric_distance_pc':R,'point_probe_max_cold_restoring_acceleration_kms2_per_pc':gcmax,'relative_COM_restoring_upper_bound_kms2_per_pc':A,'spherical_host_baryonic_source_mass_threshold_Msun':threshold})
after=hashes();assert before==after
out={'scope':'conditional action-level necessary bound for translating unchanged Plummer cold/starlight components in a slowly varying spherical host; uses actual Galactocentric distances, no adopted host mass; not a full nonlinear external-field or survival verdict','criterion':'g_X_host <= (1+Mstar/Mcold) max_r g_cold(r); with g_N_host=g_X_host^2/(a0-g_X_host)','inputs_before':before,'inputs_after':after,'results':rows};(P/'host_threshold.json').write_text(json.dumps(out,indent=2)+'\n');print(rows)
