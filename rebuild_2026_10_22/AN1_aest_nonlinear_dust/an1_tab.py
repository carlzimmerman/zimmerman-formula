import json,sys
fn=sys.argv[1]
print("key mu foot amp G KB N eta | label z_f t_f r_f cell m_f gridlim edge | hbar/c2 Q0need warn steps | masses")
for l in open(fn):
    d=json.loads(l)
    m=d.get('masses',{})
    ms=' '.join(f"{k}:Md{v['Md']:.2e},Mb{v['Mb']:.2e},Mph{v['Mph']:.2e}" for k,v in m.items())
    f=lambda x,s='.3g':format(x,s) if isinstance(x,(int,float)) and not isinstance(x,bool) else str(x)
    print(d['key'],d['mu'],d['foot'][:3],d.get('amp'),d.get('MGdiv'),d.get('KB'),d.get('N'),d.get('eta'),'|',d.get('label'),f(d.get('z_fold')),f(d.get('t_fold_Gyr')),f(d.get('r_fold_kpc')),d.get('cell_fold'),f(d.get('m_fold')),d.get('grid_limited'),d.get('edge_artefact'),'|',f(d.get('hbar_zi_over_c2')),f(d.get('Q0_need_perMpc')),d.get('newton_warn'),d.get('nstep'),'stop',f(d.get('baryon_stopped_on_profile')),'|',ms)
