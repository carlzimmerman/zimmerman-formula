from pathlib import Path
import csv,json,io,numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
base=Path('euclid_for_j0332_followup_2026_11_13/external_sl2s_match');out=base/'run_01'
e=list(csv.DictReader(open('euclid_eclipse_screen_2026_11_13/run_02/screen_all_15072.csv')))
lines=Path('euclid_for_j0332_followup_2026_11_13/external_spectroscopic_matches/inputs/sl2s_table.tsv').read_text().splitlines();lines=[x for x in lines if x and not x.startswith('#')];s=list(csv.DictReader(io.StringIO('\n'.join([lines[0]]+lines[3:])),delimiter='\t'))
assert len(e)==15072 and len(s)==47
ce=SkyCoord([float(x['RA_obj']) for x in e]*u.deg,[float(x['DEC_obj']) for x in e]*u.deg);cs=SkyCoord([x['RAJ2000'] for x in s],[x['DEJ2000'] for x in s],unit=(u.hourangle,u.deg))
i,j,d,_=ce.search_around_sky(cs,10*u.arcsec); rows=[]
for a,b,sep in zip(i,j,d.arcsec):
 r={**s[a],**{'eclipse_id':e[b]['Unique_Identifier'],'eclipse_ra':e[b]['RA_obj'],'eclipse_dec':e[b]['DEC_obj'],'separation_arcsec':float(sep),'within_2arcsec':bool(sep<=2),'eclipse_final_sample':e[b]['final_sample'],'eclipse_model_consensus':e[b]['lens_model_consensus_50']}};rows.append(r)
idx,dd,_=cs.match_to_catalog_sky(ce);near=[{'sl2s_name':x['Name'],'nearest_eclipse':e[k]['Unique_Identifier'],'separation_arcsec':float(sep)} for x,k,sep in zip(s,idx,dd.arcsec)]
# Independent haversine-distance check on every nearest pair.
ra1=np.radians(cs.ra.deg);de1=np.radians(cs.dec.deg);ra2=np.radians(ce.ra.deg[idx]);de2=np.radians(ce.dec.deg[idx]);hh=np.sin((de1-de2)/2)**2+np.cos(de1)*np.cos(de2)*np.sin((ra1-ra2)/2)**2;ind=2*np.arcsin(np.sqrt(hh))*180/np.pi*3600
assert np.max(np.abs(ind-dd.arcsec))<1e-7
for name,rr in [('matches_10arcsec.csv',rows),('nearest_all47.csv',near)]:
 with open(out/name,'w') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]) if rr else ['no_matches']);w.writeheader();w.writerows(rr)
r={'eclipse_rows':len(e),'sl2s_spectrum_rows':len(s),'unique_sl2s_names':len(set(x['Name'] for x in s)),'pairs_within_2arcsec':sum(x['within_2arcsec'] for x in rows),'pairs_within_10arcsec':len(rows),'nearest_min_arcsec':float(dd.arcsec.min()),'haversine_max_delta_arcsec':float(np.max(np.abs(ind-dd.arcsec))),'matches':rows};(out/'result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
