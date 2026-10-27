# Coupled gradient investigation: continuation state

Base checkout at start: 351d365892a89ad5bc9cdc2179ce7ec254f20645. Goal unchanged and not achieved. Do not replace MI-14's populated/restoring branch with a new apparent solution from this directory.

Use coupled_model.py, not model.py. The original model.py caused an import collision with the inherited constants module and is retained only as the failed GC-1 input. The energy Ec=.5κ∫r²(a′−eta a q′)² is positive and has full density and conversion derivatives. Its bulk force is nonzero; the old cold-law proof does not apply unchanged. See DERIVATION.md for all base and new species forces.

GC-2 screens six L/eta pairs at beta2,K30,ell10kpc,n96/domain12, fixed total mass5.364Mb. GC-3 tests four intermediate pairs. L10 eta1→3 reduces mass outside50 by .582Mb but still leaves 1.186Mb outside, versus .56242 allowed for the exact law. Bulk-law error is about28%. Weak stiffness leaves a depleted interval.

GC-4 selected L5 eta3 with an initially incomplete support criterion and tests joint ±1kpc displacements on96/144 grids. Both signs return on each grid, but R122→176kpc upon refinement and the law remains off by about10–11%. GC-5 computes complete constrained active Hessians and local relaxed stiffnesses1.81034e-4 and4.71094e-5Eunit/kpc². These are finite-grid restoring forces, not a converged boundary certificate.

GC-9 corrects the support interpretation: the original rebound cut stopped at q=.5 and missed part of the coarse-grid cavity. Expanding the audit to1.2R and1.5R shows a cavity already on the coarse grid. Do not quote raw eligible=true as proof of a filled interface. The rendered refinement plot is also explicit about this failure.

Homology Ec→lambda^-2Ec was verified on both grids atlambda=.8,1.2 to about1e-15. Its dilation stress is outward even though the cross term can redistribute inward. This motivated, rather than proved, the combined-capacity test.

GC-6 failed its largest derivative step before optimizing. GC-7 repeats with converged steps3e-6,1e-6,3e-7 and supplied response-capacity charges.003,.03,.3. The complete charge variations are included. None repairs law/support/mass allocation; strong charge makes an extra inner mixed layer. The previous standalone charge failure therefore survives this combined test in the tested range. No microscopic production of supplied charge is claimed.

GC-8 summarizes13 screened states and four restoration trials; GC-9 adds the expanded support audit. Nine evidence records total:7completed/2failed, all validate. All experiments ended. No new commit or push. New work should retain MI-14 as the last demonstrated filled, restoring state and address the transition force/mass budget without positive-gradient expansion, hidden cavities, a target-density prior or artificial exterior conversion. This is a route checkpoint, not a claim that every possible interaction is excluded.
