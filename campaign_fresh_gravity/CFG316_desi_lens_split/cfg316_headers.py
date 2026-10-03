"""CFG316: print the column schema (headers only, no values) of each FITS catalogue.
Usage: python3 cfg316_headers.py <path-to-_external_data>
Parses header cards directly so a partially downloaded file still works."""
import sys, os, json
ROOT = sys.argv[1] if len(sys.argv) > 1 else '_external_data'
FILES = {
 'kids1000_som_gold': 'kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits',
 'desi_dr1_bgs_full': 'desi_dr1_bgs/BGS_BRIGHT_full_HPmapcut.dat.fits',
 'desi_dr1_cigale':   'desi_dr1_cigale/IronPhysProp_v1.2.fits',
}
def headers(path):
    out = []; f = open(path, 'rb'); pos = 0; size = os.path.getsize(path)
    while pos < size:
        f.seek(pos); cards = {}; order = []; nblk = 0
        while True:
            blk = f.read(2880); nblk += 1
            if len(blk) < 2880: return out
            done = False
            for i in range(36):
                c = blk[80*i:80*i+80].decode('ascii', 'replace')
                k = c[:8].strip()
                if k == 'END': done = True; break
                if c[8:10] == '= ':
                    v = c[10:].split('/')[0].strip().strip("'").strip()
                    cards[k] = v; order.append(k)
            if done: break
        hdr_bytes = 2880*nblk
        bitpix = abs(int(cards.get('BITPIX', 8))); nax = int(cards.get('NAXIS', 0))
        n = 1 if nax else 0
        for a in range(1, nax+1): n *= int(cards.get(f'NAXIS{a}', 0))
        n = n * bitpix // 8 + int(cards.get('PCOUNT', 0))
        data = (n + 2879)//2880*2880
        cols = []
        for j in range(1, int(cards.get('TFIELDS', 0))+1):
            cols.append({'name': cards.get(f'TTYPE{j}'), 'format': cards.get(f'TFORM{j}'),
                         'unit': cards.get(f'TUNIT{j}', '')})
        out.append({'extname': cards.get('EXTNAME', ''), 'naxis1': cards.get('NAXIS1'),
                    'naxis2': cards.get('NAXIS2'), 'ncols': len(cols), 'columns': cols,
                    'hdu_end_byte': pos + hdr_bytes + data})
        pos += hdr_bytes + data
    return out
res = {}
for key, rel in FILES.items():
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): res[key] = 'missing'; continue
    res[key] = {'file': rel, 'hdus': headers(p)}
json.dump(res, open('cfg316_column_schema.json', 'w'), indent=1)
for key, v in res.items():
    if v == 'missing': print(key, 'missing'); continue
    for h in v['hdus']:
        if h['ncols']:
            print(f"{key} [{h['extname']}] rows={h['naxis2']} rowbytes={h['naxis1']} ncols={h['ncols']} end={h['hdu_end_byte']}")
            print('  ' + ' '.join(c['name'] for c in h['columns']))
