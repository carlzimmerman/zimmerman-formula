import json
txt = open('raw_output.json').read()
d = json.loads(txt[:txt.index('BOUNDS_OK')])
for foot in ('canonical', 'alternative'):
    kt = d['kernel_table'][foot]
    print('='*20, foot)
    for pt in ('pointA_transition', 'pointB_deep_disk'):
        r = kt[pt]
        print(f"--- {pt}: r_pc={r['r_pc']:.4f} y_true={r['y_true']:.5f} "
              f"M_enc2={r['M_enc2_true_Msun']:.3e} M_env={r['M_env_only_Msun']:.3e}")
        print('  deep-limit ratios: const', round(r['deep_limit_ratio_const_flip'], 6),
              'strip', round(r['deep_limit_ratio_strip_flip'], 6))
        for k in ('ratio_const_flip_over_true', 'ratio_strip_flip_over_true'):
            print(' ', k, {b: round(v, 6) for b, v in r[k].items()})