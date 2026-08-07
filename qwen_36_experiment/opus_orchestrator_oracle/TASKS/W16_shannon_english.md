# W16 — Shannon's entropy of English, measured three ways
COST: S | script: `wacky_shannon_english.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Shannon estimated English at ~1.0–1.3 bits/character. Measure it on a real corpus (Gutenberg text) by:
(1) zeroth-order symbol frequency; (2) n-gram conditional entropy for n = 1…8, plotting the decay;
(3) an actual compressor as an upper bound (`zlib`, `lzma`, `bz2` — bits/char achieved). Report all three
and where the n-gram estimate saturates from data sparsity rather than from language structure (that
saturation point is the real finding — quantify how much text n = 8 would need). Then compare against
Shannon's own 1951 human-prediction experiment value of ~1.1.
