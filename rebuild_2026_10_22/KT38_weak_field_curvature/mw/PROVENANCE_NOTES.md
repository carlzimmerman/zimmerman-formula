# Preserved preliminary records and data representation

`full_001` failed at final alternate-footing JSON serialization because the
unchanged scale-length diagnostic returns positive infinity when its fitted
log-K slope is nonnegative. Its saved result contains canonical profiles only.
Those 6,875 profiles were independently regraded, but the overall run is not
promoted to completed and its unsaved alternate profiles are not evidence.

`search_v2.py` evaluates all original scores and cuts before encoding. It
represents a positive infinite scale length as `h: null` plus the explicit
`h_status` reason, asserting the unchanged strict Lh result is false. It does
not turn infinity into a finite fit, omit failing rows or accept NaN. Fresh
`full_002` replays the original five lengths; `focused_001` tests the new five
intermediate lengths selected after the initial canonical results.

The frozen contracts copied a non-claim sentence beginning "Six discrete
lengths" from KT37. Their authoritative assertions, bounds and execution
arguments specify five lengths each, and every resulting population count
must be checked against those actual arrays. This stale prose is disclosed
rather than silently rewriting a hash-pinned record. It grants no sixth
length of coverage and does not alter the computation or scientific cuts.
