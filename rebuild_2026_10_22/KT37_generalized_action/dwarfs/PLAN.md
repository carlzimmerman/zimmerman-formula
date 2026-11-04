# KT37 isolated Plummer dwarf discriminator

Authorized fourth-route diagnostic with original 24-object KT15 sample,
Plummer scale a=R2, M=Upsilon L+1.33 M_HI, original 41 Upsilon values from
1 to3, both original a0 footings and unchanged 2-sigma dispersion cuts.
The new fixed physical ell values are .03,.1,.3,1 kpc for every object.
No Gaussian smoothing or object-dependent scale is used.

The exact spherical reduction retains the complete Hessian term. With
g=GM r/(r^2+a^2)^(3/2), its first two radial derivatives are analytic.
Write A_r=Cg and B=Br nn+Bt(I-nn). Then

    g_ph=A_r-Br'-2(Br-Bt)/r.

Use the analytic R',R'' functions and the full derivative of Br. The
line-of-sight virial variance is exact Newton pi GM/(32a) plus
int W(r)g_ph dr, W=4pi rho_unit r^3/3.

Independent integral checks:

    sigma_ph^2=int [W A+(W'-2W/r)Br+2W Bt/r]dr-[W Br]_inner^outer,

and the fixed-mass energy variation under rho_lambda= lambda^3 rho(lambda r):

    sigma_ph^2=(1/(3GM)) int r^2
      [A(2g+rg')+Br(3g'+rg'')+2Bt(2g/r+g')]dr.

The latter uses the direct field variation at fixed physical radius. A naive
rescaling of the logarithmically divergent MOND energy integral without its
outer boundary term is not used. Selected finite differences of the energy
at a exp(+/-h) provide an additional check.

Before interpretation require: finite results; direct/weak/energy virial
agreement within1e-3 relative or1e-7(km/s)^2 absolute; Newtonian Plummer
virial relative error<1e-3; plain isolated QUMOND reproduces19/24 on each
footing; n1000/2000 and doubled-domain dispersions change by<.02km/s.
Use rmin=1e-6 a, rmax=200a+40ell, with an independent doubled outer domain.
No finite-radius mass loss is used to renormalize the input.

Every Upsilon is explicitly evaluated. No monotonicity in Upsilon is assumed
for this generalized action, and no continuous-Upsilon exclusion is claimed.
Negative predicted variance, if encountered, is a physical failure and is
reported without clipping. This is isolated spherical evidence, not a
satellite external-field calculation or a proof that isolation is an upper
bound. Original primary EFE labels do not transfer.

Wall cap600s, CPU550s, one numerical thread,1MiBlogs, no randomness. Retain
all outputs and failed checks in fresh bounded run directories.

Amendment before any dwarf physical run: the coordinator found a provisional
Milky Way witness at ell=3 kpc and explicitly added ell=3 and10 kpc to this
discriminator. All six lengths will be reported. This extension is disclosed
as prompted by the Milky Way result, not a blind original range.
