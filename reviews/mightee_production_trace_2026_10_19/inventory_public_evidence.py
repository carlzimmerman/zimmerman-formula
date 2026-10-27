"""Reproducible inventory of cached primary release and repository metadata."""
from pathlib import Path
import csv,json,hashlib,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'_external_data/mightee_production_trace_2026_10_19';OUT=Path(__file__).resolve().parent

def main():
    tree=ET.parse(DATA/'release_bucket.xml');ns={'s':'http://s3.amazonaws.com/doc/2006-03-01/'}
    assert tree.find('s:IsTruncated',ns).text=='false','Listing is incomplete'
    rows=[]
    for c in tree.findall('s:Contents',ns):
        key=c.find('s:Key',ns).text;name=Path(key).name
        rows.append(dict(key=key,name=name,bytes=int(c.find('s:Size',ns).text),last_modified=c.find('s:LastModified',ns).text,etag=c.find('s:ETag',ns).text,kind='FITS cube' if name.endswith('.fits') else 'HTML page' if name.endswith('.html') else 'Other',url='https://archive-gw-1.kat.ac.za/public/'+key))
    with (OUT/'release_inventory.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    names=[r['name'].lower() for r in rows]
    intermediate_names=[r['name'] for r in rows if any(w in r['name'].lower() for w in ['psf','model','residual','kernel','weight','mask','log','config','recipe'])]
    branches=json.load(open(DATA/'branches.json'));source_main=ROOT/'_external_data/mightee_pipeline_2026_10_19/source/clean__convolve_channels.py';source_mod=DATA/'modular/clean__convolve_channels.py'
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    branch_rows=[dict(name=b['name'],commit=b['commit']['sha']) for b in branches]
    datacite=[]
    for name in ['datacite_mightee.json','datacite_mightee_page2.json']:datacite+=json.load(open(DATA/name))['data']
    advertised=BeautifulSoup((DATA/'idia_page.html').read_text(),'html.parser')
    idia_fits=sorted({a['href'] for a in advertised.find_all('a',href=True) if a['href'].endswith('.fits')})
    result=dict(outcome='Public production provenance and intermediate products not recovered',scope='Public default/modular branches and full listed history, release bucket, advertised IDIA page, collaboration branches, software-container metadata and DataCite search. This does not establish that unlisted or non-public products do not exist.',release=dict(n_objects=len(rows),n_fits=sum(r['kind']=='FITS cube' for r in rows),n_html=sum(r['kind']=='HTML page' for r in rows),truncated=False,names_matching_intermediate_keywords=intermediate_names),idia=dict(n_advertised_fits=len(idia_fits),note='Advertised links are final cubes, not per-pointing PSF/model/residual/kernel products; directory requests returned404, which does not establish that individual linked files are unavailable.'),repository=dict(branches=branch_rows,n_tags=len(json.load(open(DATA/'tags.json'))),n_releases=len(json.load(open(DATA/'releases.json'))),n_forks=len(json.load(open(DATA/'forks.json'))),n_main_commits_cached=len(json.load(open(DATA/'commits.json'))),n_modular_commits_cached=len(json.load(open(DATA/'modular_commits.json'))),convolution_routine_identical_across_branches=h(source_main)==h(source_mod),convolution_sha256=h(source_mod),production_commit_matched_to_fits=False),container=dict(public_filename='oxkat-0.41.sif',full_size_bytes=1619615744,prefix_bytes_read=262144,build_metadata_date='Thursday_16_June_2022_13:39:48_BST',pypher_install_recipe='pip3 install pypher',exact_installed_version_recovered=False,production_digest_matched=False,note='The public HI scripts reference0.42, while the general oxkat download is0.41; neither establishes what was run for the released cubes. No container was executed.'),local_cube_hdus=json.load(open(DATA/'local_hdu_inventory.json')),registry=dict(datacite_records_cached=len(datacite),declared_total=json.load(open(DATA/'datacite_mightee.json'))['meta']['total'],note='No separate DR1 production-code or intermediate-PSF deposit identified; relevant HI DOI resolves to the inspected release.'),conclusion='Cannot confirm a production beam normalization bug or explain the remaining flux deficit without the actual production execution record and per-pointing intermediates. Public code demonstrates a suspect implementation, not its use in these cubes.')
    (OUT/'findings.json').write_text(json.dumps(result,indent=2))
    records=[dict(file=str(f.relative_to(ROOT)),bytes=f.stat().st_size,sha256=h(f)) for f in sorted(DATA.rglob('*')) if f.is_file()]
    (OUT/'source_hashes.json').write_text(json.dumps(records,indent=2))
    print(json.dumps({k:result[k] for k in ['outcome','release','repository','registry']},indent=2))

if __name__=='__main__':main()
