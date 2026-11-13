"""Offline provenance/identity checks for target-only DESI extraction."""
from pathlib import Path
import json,hashlib,platform
import numpy as np
import astropy
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
P=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=json.loads((P/'coadd_range_manifest.json').read_text())
rs=[]
for f in sorted((P/'ranges').glob('*.json')):
    r=json.loads(f.read_text());raw=f.with_suffix('.bin')
    assert raw.stat().st_size==r['nbytes'] and sha(raw)==r['sha256']
    assert r['status']==206 and r['headers']['Content-Range']==f"bytes {r['start']}-{r['start']+r['nbytes']-1}/{m['parent_bytes']}"
    rs.append(r)
assert sum(r['nbytes'] for r in rs)==m['downloaded_bytes']
published={line.split()[1]:line.split()[0] for line in (P/'healpix_checksums.txt').read_text().splitlines()}
assert sha(P/'redrock-main-dark-9907.fits')==published['redrock-main-dark-9907.fits']
x=np.load(P/'target_coadd.npz');v=np.load(P/'viewer_spectrum.npz');bands={}
with fits.open(P/'target_coadd_derived.fits') as f:
    assert all(h.verify_checksum()==1 and h.verify_datasum()==1 for h in f)
    assert int(f['FIBERMAP'].data['TARGETID'][0])==m['targetid']
    for band in 'BRZ':
        for key in [k for k in x.files if k.startswith(band+'_')]:
            assert np.array_equal(f[key].data,x[key])
        wave=x[band+'_WAVELENGTH'];flux=x[band+'_FLUX'][0];iv=x[band+'_IVAR'][0];mask=x[band+'_MASK'][0]
        vw=v[band.lower()+'_origwave'];vf=v[band.lower()+'_origflux0'];vn=v[band.lower()+'_orignoise0']
        good=np.isfinite(vf);assert np.array_equal(wave,vw)
        assert np.array_equal(flux[good],vf[good])
        assert np.array_equal(~good,iv<=0) and np.array_equal(mask!=0,iv<=0)
        assert np.all(np.isfinite(x[band+'_RESOLUTION']))
        bands[band]=dict(nwave=len(wave),range_angstrom=[wave[0],wave[-1]],
            finite_flux_equal=True,wavelength_equal=True,masked_pixels=int(sum(mask!=0)),
            maximum_noise_absolute_difference=float(np.max(abs(iv[good]**-.5-vn[good]))),
            median_per_pixel_SN=float(np.median(flux[good]*np.sqrt(iv[good]))),
            resolution_shape=list(x[band+'_RESOLUTION'].shape))
fm=json.loads((P/'target_fibermap.json').read_text())
a=SkyCoord(231.19015110938125*u.deg,44.16376016502161*u.deg)
b=SkyCoord(fm['TARGET_RA']*u.deg,fm['TARGET_DEC']*u.deg)
result=dict(scope='Data extraction and identity validation only; no stellar dispersion fit or theory test.',
    targetid=m['targetid'],catalog_separation_arcsec=a.separation(b).arcsec,
    redrock_published_sha256_verified=True,whole_coadd_sha256_verified=False,
    derived_fits_internal_checksums_verified=True,raw_range_count=len(rs),raw_range_bytes=sum(r['nbytes'] for r in rs),
    bands=bands,versions=dict(python=platform.python_version(),numpy=np.__version__,astropy=astropy.__version__),
    artifacts={str(f.relative_to(P)):sha(f) for f in [P/'target_coadd.npz',P/'target_coadd_derived.fits',P/'redrock-main-dark-9907.fits',P/'viewer_spectrum.npz',P/'extract_coadd_ranges.py',P/'extract_viewer.py',P/'validate.py']})
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
