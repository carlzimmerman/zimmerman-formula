"""Read complete checksummed table HDUs from bounded public gzip prefixes."""
import argparse
import io
import json
from pathlib import Path
import warnings
import zlib
import numpy as np
from astropy.io import fits

HERE=Path(__file__).resolve().parent
TARGET=39633153882587315
KEYS=['TARGETID','RA','DEC','TARGET_RA','TARGET_DEC','Z','ZWARN','SPECTYPE','COADD_FIBERSTATUS',
      'VDISP','VDISP_IVAR','RCHI2','RCHI2_CONT','RCHI2_PHOT','SNR_B','SNR_R','SNR_Z',
      'APERCORR','APERCORR_G','APERCORR_R','APERCORR_Z','FLUX_G','FLUX_R','FLUX_Z',
      'FLUX_SYNTH_G','FLUX_SYNTH_R','FLUX_SYNTH_Z','LOGMSTAR','LOGMSTAR_IVAR','LOGMSTAR_INIT']

def scalar(value):
    if isinstance(value,bytes):return value.decode().strip()
    return value.item() if hasattr(value,'item') else value

def main(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    records={}
    for version in ['2.1','3.0']:
        path=HERE/('v'+version+'_first2mb.gz')
        compressed=path.read_bytes();raw=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(compressed)
        tables={}
        # MODELS is intentionally incomplete. Only complete verified table HDUs are used.
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter('always')
            with fits.open(io.BytesIO(raw),ignore_missing_end=True,lazy_load_hdus=True) as hdus:
                for hdu in hdus:
                    if hdu.name=='MODELS':break
                    if hdu.name not in ['METADATA','FASTSPEC','SPECPHOT']:continue
                    table=hdu.data
                    index=np.flatnonzero(table['TARGETID']==TARGET)
                    assert len(index)==1
                    checksum=int(hdu.verify_checksum());datasum=int(hdu.verify_datasum())
                    assert checksum==datasum==1
                    row=table[index[0]]
                    tables[hdu.name]={'row':int(index[0]),'rows':len(table),
                        'checksum':checksum,'datasum':datasum,
                        'values':{k:scalar(row[k]) for k in KEYS if k in hdu.columns.names}}
        dispersion=tables['FASTSPEC' if version=='2.1' else 'SPECPHOT']['values']
        assert dispersion['VDISP_IVAR']>0
        sigma=float(dispersion['VDISP']);error=float(dispersion['VDISP_IVAR']**-.5)
        records[version]={'compressed_prefix_bytes':len(compressed),'decompressed_prefix_bytes':len(raw),
            'tables':tables,'VDISP_kms':sigma,'VDISP_curvature_error_kms':error,
            'difference_from_Guo222_26_kms':sigma-222.26,
            'reader_warnings':list(dict.fromkeys(str(x.message) for x in seen))}
    result={'targetid':TARGET,'published_Guo2026_v2':{'VDISP_kms':222.26,'reported_error_kms':15.,
            'source':'https://arxiv.org/html/2602.13578v2#S2.T1'},
            'records':records,'interpretation':'Material pipeline/masking/template dependence in dispersion estimates for the same observed spectrum. Requires an independent contamination and resolution audit before treating the published narrow error as complete.',
            'non_claims':['These are alternative reductions of the same photons, not independent measurements to multiply.',
                'No independent-error significance is assigned to differences.',
                'FastSpec photometric masses are not adopted for this blended quasar lens.',
                'Only complete checksum-verified table HDUs were retrieved; model spectral cubes are not available in these prefixes.',
                'No gravity fit or theory exclusion follows from this metadata check.']}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({v:{k:r[k] for k in ['VDISP_kms','VDISP_curvature_error_kms','difference_from_Guo222_26_kms']} for v,r in records.items()}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
