# NQ1_near_miss_census: how close did each lane get?

Owner's request, 2026-11-02: review the last two weeks' lanes for what came close, since pass/fail gates can bury a near miss. **This reads the record. It changes no frozen label or verdict, and a near miss isn't a pass.** Not blind. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework. The cold sector stays retired unless the owner says otherwise, but near misses from retired routes are still listed, marked as such.

For each lane README in your batch list, read it (and its numbers file only if the README is unclear) and fill one row:

| lane | idea | frozen label | closest number against its line, as margin | which gaps it touches (S, Tl, LT, G, K, X, Ln, Dw, MW, DM, IC, CMB, action) | class | what would test it next, cheaply |

Class is one of:
- A near miss on measured data, one number or one cell from passing
- B failure resting on a defect, a shaky input or a contested gate; name it
- C partial: fixes a gap another route can't, breaks something else; name both
- D clear failure, far from its line
- E not a physics test, or superseded by a later lane; name it

Skip nothing: every line of your list gets a row, even if E. Quote margins from the file, never from memory. Don't round a fail up: the row states the real number. Note anything that combines naturally with UX3's gas term, g = law x (1 + k g_gas/a0), k about 13 fitted, or that UX3's term would make worse.
