# JNT2R RESULT

**Blind label, unchanged: JOINT FAILS ON G2 (coverage) / JOINT FAILS ON G2 (coverage) (canonical / alt), FRAGILE.** JNT2 had no RESULT.md when its folder was opened on 2026-11-13 (only its criteria, scripts, outputs and logs, none of which were read), so no comparison is made.

**Commit ids and the lead's note (added 2026-11-13, after landing; no number or label changes).** Local / origin:
READING 5abea0324b / 44c243040b; scripts and outputs 6f571f0e87 / 9391163ae9; RESULT_BLIND e8517dce96 / be794b7645;
RESULT b5d4177ef6 / a76a069a34. Pushed. This lane's scripts were NOT re-run by the lead.

**The two builds side by side (the lead's comparison, 2026-11-13; neither lane wrote one because each landed before
it could see the other).** Same frozen label on both footings: JOINT FAILS ON G2 (coverage). Same boundary (668.5 /
807.9 km/s), same RC100 membership on the model rule (10 / 2 of 100 above, all at z 2.1 to 2.5), SPARC 0 of 175 above,
KiDS 0 above, X-COP 7 of 7 above, the same G4 words (fails at f 0.75 and 1, passes from 1.25), the same group q
(0.651 / 0.654). Differences that move no label below f = 3: the forest at f = 3 (JNT2 1.99 holds / 6.43 fails;
JNT2R 17.6 / 29.2, both fail), the forest halo counts above the boundary at z 2.2 (170 / 160 against 155 / 151), and one
group on canonical (IC1633 above in JNT2 at 666 against 661 km/s; none above in JNT2R, largest 658). So the ungraded
window without the coverage line is [1.25, 2] in both builds on both footings; f = 3 is not agreed. The cause of the
f = 3 forest difference was not traced.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
