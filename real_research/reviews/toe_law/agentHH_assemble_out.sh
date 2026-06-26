#!/bin/bash
# agentHH .out assembler — appends the session's step logs in canonical order.
# The .out already contains step0/step1/step2 (banked) + step3a0 (appended live).
# Several steps were split across processes after the QoS-throttle diagnosis: their
# partial logs are concatenated in content order (each piece is a complete section).
cd /Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/toe_law
emit () {
    f="$1"
    if [ -s "$f" ]; then
        cat "$f" >> agentHH_pump_profile.out
    else
        echo "[assembler] MISSING OR EMPTY: $f" >> agentHH_pump_profile.out
    fi
}
emit /tmp/hh_step3a0b.log
emit /tmp/hh_step3a.log
emit /tmp/hh_step3a1.log          # [a]-[d] + C(p) rows p = 2/3, 1, 4/3 (run truncated at the throttle fix)
emit /tmp/hh_3a1f.log             # [e] completion (p = 2, 8/3 + exact anchors) + [f]
emit /tmp/hh_3a1f_refit.log       # [f] well-posed (ct, lock) extraction (in-run fit ran away: bug log)
emit /tmp/hh_step3b.log
emit /tmp/hh_step3c.log           # B + L (run truncated at the throttle fix)
emit /tmp/hh_step3c2.log          # [3c2-a] eps-linearity
emit /tmp/hh_step3c3.log
emit /tmp/hh_step3c4.log          # [3c4-a] kernel-side band check
emit /tmp/hh_leftovers.log        # [3c-X], [3c-E], [3c2-b], [3c4-b]
emit /tmp/hh_3dK.log              # [3d-0..3] + linearity
emit /tmp/hh_3dK_refit.log        # [3d] well-posed (ct, lock) extraction
emit /tmp/hh_3d4_c3.log           # [3d-4] hostile rows (standalone, parallel)
emit /tmp/hh_3d4_wlo.log
emit /tmp/hh_3d4_canon.log
emit /tmp/hh_3d4_hostile.log
emit /tmp/hh_3d4_lin.log
emit /tmp/hh_3d4_refit.log    # [3d-4] row extractions (in-process fits superseded: bug 11)
emit /tmp/hh_3d2_v2.log
emit /tmp/hh_3d2_refit.log    # [3d2] extraction + amplitude addendum
emit /tmp/hh_step3e.log
emit /tmp/hh_step4.log
emit /tmp/hh_step5.log
echo "assembled: $(wc -l < agentHH_pump_profile.out) lines"
