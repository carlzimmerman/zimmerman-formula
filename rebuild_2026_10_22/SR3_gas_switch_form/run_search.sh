#!/bin/bash
# Two chains, one Julia thread each, nice 19. Finished jobs are skipped; rerun this after any kill (SIGTERM stops a job at once, it restarts from scratch).
cd "$(dirname "$0")"; export SR3_NIT=300
(for a in "planted canonical T1FY free" "real canonical T1FY free" "real canonical T1F free" "real alt T1FY free" "real alt T1F free" "real canonical T1FY fixed" "scrambled canonical T1FY free"; do nice -n 19 python3 sr3_search.py $a; done) > logs/chain_a.log 2>&1 &
(for a in "planted canonical T0 free" "real canonical T0 free" "label canonical T0 free" "scrambled canonical T0 free" "real alt T0 free" "real canonical T0 fixed"; do nice -n 19 python3 sr3_search.py $a; done) > logs/chain_b.log 2>&1 &
wait; echo ALLDONE > logs/search.done
