import json
d = json.load(open('W02_floor_family_results.json'))
for k, v in d['families'].items():
    print(k, {kk: round(vv, 6) if isinstance(vv, float) else vv for kk, vv in v.items() if kk != 'binding'})
    print('   binding:', v['binding'])
print('checks:', {k: v['detail'] for k, v in d['checks'].items()})
w3 = json.load(open('W03_wallaby_card_results.json'))
print('W3 sample:', w3['census']['sample_gals_with_deep'][:3])
print('W3 deep_galaxies:', w3['census']['deep_galaxies'], 'deep_rings:', w3['census']['deep_rings'])
print('W3 verdict:', w3['verdict'])
w1 = json.load(open('W01_chord_finish_results.json'))
print('W1:', {k: v['detail'] for k, v in w1['checks'].items()})
