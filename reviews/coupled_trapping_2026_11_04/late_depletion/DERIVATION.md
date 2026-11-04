# Necessary late depletion strength

This is an independent conditional diagnostic after capture, not the coupled
collision solution. Let n count both members of a charge-symmetric population.
For a physical particle-antiparticle pair cross section sigma v,

    ndot+3Hn=-(sigma v)n^2/2,
    1/Y_final=1/Y_start + integral dt s <sigma v>/2.

The factor 1/2 is essential: n_plus=n_minus=n/2 and each event removes two.
Use the physical lightest charged scalar masses from TP06 and a prescribed
redshifting isotropic FD momentum shape f(p/Tc). Pair removal is represented
as its normalization changing with shape fixed. This is a closure, not a
proof about selective annihilation's actual momentum distribution.

For nonrelativistic particles isotropic angular integration gives

    <1/v_rel>=(m/Tc) C_FD,
    C_FD=2 integral_0^infinity dp p f(p) integral_0^p dq q^2 f(q)
             / [integral_0^infinity dp p^2 f(p)]^2.

For the separately derived gauge-pair baseline sigma0=13g^4/(128pi m^2),
the attractive Coulomb factor obeys S(z)=z/(1-exp(-z)) <=1+z, z=2pi alpha/v.
With alpha_max=2.5g^2/(4pi) this gives the prescribed pure-gauge envelope

    <sigma v> <= sigma0 [1+B a],
    B=2pi alpha_max (m/Tc_start) C_FD,  a_start=1.

The coefficient and alpha_max are the microphysics package's pure-gauge
conventions; neither is an upper bound on all scalar-mediated reactions or
bound-state formation. Multiplying this envelope is only a sensitivity test.

Take H>=H_start/a^2 from visible radiation alone. In an entropy-conserving
visible bath, standard entropy releases only increase the visible comoving
radiation energy relative to this comparison; additional positive matter,
hidden radiation and vacuum energy also increase H. Ignoring them maximizes
the loss integral in this prescribed model up to a specified a_final. Thus

    L_gauge <= s_start sigma0/(2H_start)
                     [1-1/a_final + B log(a_final)],
    Y_final >= [1/Y_start + L_gauge]^-1.

a_final is the visible entropy-conserving scale-factor ratio to the chosen
present photon temperature. gstar=gSstar=106.75, gS0=3.909 and T0 are explicit
comparison inputs. This deliberately generous radiation-only envelope avoids
mistaking a matter-era extrapolation for an enhancement of annihilation.

The numerical experiment reports the multiplicative enhancement of this
entire gauge envelope that would be necessary to reach the 10%-DM charged
gate. It also compares the maximum s-wave inelastic expression
4pi/(m^2 v_rel), under the same prescribed FD velocity and expansion history.
That single-partial-wave comparison does not bound long-range capture with
many partial waves and is not a model-wide unitarity exclusion.
