#!/usr/bin/env python3
"""
Z² AUTONOMOUS RESEARCH TOPICS
==============================

500+ research topics for autonomous web research and Z² pattern discovery.
Each topic is designed to yield numerical constants via web search.

Usage:
    from research_topics import RESEARCH_TOPICS, get_topics_by_domain

    # Get all topics
    all_topics = RESEARCH_TOPICS

    # Get topics for a specific domain
    physics_topics = get_topics_by_domain("physics")

Author: Carl Zimmerman
Date: May 6, 2026
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ResearchTopic:
    """A research topic for autonomous investigation."""
    query: str           # Search query for web research
    domain: str          # Scientific domain
    expected_type: str   # "constant", "ratio", "exponent", "angle", etc.
    priority: int        # 1=high, 2=medium, 3=low
    notes: str = ""      # Additional context


# =============================================================================
# RESEARCH TOPICS BY DOMAIN
# =============================================================================

RESEARCH_TOPICS: List[ResearchTopic] = [

    # =========================================================================
    # FUNDAMENTAL PHYSICS (50 topics)
    # =========================================================================

    # Particle Physics
    ResearchTopic("fine structure constant alpha 1/137", "particle_physics", "constant", 1),
    ResearchTopic("weak mixing angle Weinberg sin squared theta", "particle_physics", "constant", 1),
    ResearchTopic("strong coupling constant alpha_s QCD", "particle_physics", "constant", 1),
    ResearchTopic("proton to electron mass ratio 1836", "particle_physics", "ratio", 1),
    ResearchTopic("neutron to proton mass ratio", "particle_physics", "ratio", 1),
    ResearchTopic("muon to electron mass ratio 206", "particle_physics", "ratio", 1),
    ResearchTopic("tau to electron mass ratio", "particle_physics", "ratio", 2),
    ResearchTopic("W boson to Z boson mass ratio", "particle_physics", "ratio", 1),
    ResearchTopic("Higgs boson mass 125 GeV", "particle_physics", "constant", 1),
    ResearchTopic("top quark to bottom quark mass ratio", "particle_physics", "ratio", 2),
    ResearchTopic("charm to strange quark mass ratio", "particle_physics", "ratio", 2),
    ResearchTopic("up to down quark mass ratio", "particle_physics", "ratio", 2),
    ResearchTopic("Cabibbo angle sin theta_c 0.22", "particle_physics", "angle", 1),
    ResearchTopic("CKM matrix Jarlskog invariant", "particle_physics", "constant", 2),
    ResearchTopic("CP violation epsilon K kaon", "particle_physics", "constant", 2),
    ResearchTopic("neutron lifetime 14.7 minutes", "particle_physics", "constant", 1),
    ResearchTopic("muon lifetime 2.2 microseconds", "particle_physics", "constant", 2),
    ResearchTopic("pion lifetime charged", "particle_physics", "constant", 2),
    ResearchTopic("deuteron binding energy 2.22 MeV", "particle_physics", "constant", 1),
    ResearchTopic("alpha particle binding energy per nucleon", "particle_physics", "constant", 2),

    # Nuclear Physics
    ResearchTopic("nuclear magic numbers 2 8 20 28 50 82 126", "nuclear_physics", "constant", 1),
    ResearchTopic("nuclear binding energy per nucleon iron-56 8.79 MeV", "nuclear_physics", "constant", 1),
    ResearchTopic("semi-empirical mass formula coefficients", "nuclear_physics", "constant", 2),
    ResearchTopic("nuclear radius constant r0 1.2 femtometers", "nuclear_physics", "constant", 2),
    ResearchTopic("nuclear saturation density", "nuclear_physics", "constant", 2),
    ResearchTopic("spin-orbit coupling strength nuclei", "nuclear_physics", "constant", 2),
    ResearchTopic("pairing gap energy nuclei", "nuclear_physics", "constant", 2),
    ResearchTopic("Weizsacker mass formula volume term", "nuclear_physics", "constant", 2),
    ResearchTopic("Weizsacker mass formula surface term", "nuclear_physics", "constant", 2),
    ResearchTopic("Weizsacker mass formula Coulomb term", "nuclear_physics", "constant", 2),

    # Cosmology
    ResearchTopic("dark energy density Omega Lambda 0.68", "cosmology", "constant", 1),
    ResearchTopic("dark matter density Omega DM 0.27", "cosmology", "constant", 1),
    ResearchTopic("baryon density Omega b 0.05", "cosmology", "constant", 1),
    ResearchTopic("Hubble constant H0 70 km/s/Mpc", "cosmology", "constant", 1),
    ResearchTopic("CMB temperature 2.725 Kelvin", "cosmology", "constant", 1),
    ResearchTopic("primordial helium abundance Y_p 0.24", "cosmology", "constant", 1),
    ResearchTopic("spectral index n_s inflation 0.96", "cosmology", "constant", 1),
    ResearchTopic("sigma 8 matter fluctuation amplitude", "cosmology", "constant", 1),
    ResearchTopic("optical depth reionization tau", "cosmology", "constant", 2),
    ResearchTopic("tensor to scalar ratio r inflation", "cosmology", "constant", 2),
    ResearchTopic("age of universe 13.8 billion years", "cosmology", "constant", 1),
    ResearchTopic("cosmological constant dark energy", "cosmology", "constant", 1),
    ResearchTopic("matter radiation equality redshift", "cosmology", "constant", 2),
    ResearchTopic("recombination redshift z 1100", "cosmology", "constant", 2),
    ResearchTopic("reionization redshift", "cosmology", "constant", 2),

    # Quantum Mechanics
    ResearchTopic("Bohr radius 0.529 angstroms", "quantum_mechanics", "constant", 1),
    ResearchTopic("Rydberg constant 13.6 eV", "quantum_mechanics", "constant", 1),
    ResearchTopic("Compton wavelength electron", "quantum_mechanics", "constant", 2),
    ResearchTopic("de Broglie wavelength thermal", "quantum_mechanics", "constant", 2),
    ResearchTopic("quantum of conductance e^2/h", "quantum_mechanics", "constant", 1),

    # =========================================================================
    # ASTROPHYSICS (50 topics)
    # =========================================================================

    ResearchTopic("Chandrasekhar mass limit 1.4 solar masses", "astrophysics", "constant", 1),
    ResearchTopic("Eddington luminosity ratio", "astrophysics", "ratio", 1),
    ResearchTopic("Schwarzschild radius formula", "astrophysics", "constant", 1),
    ResearchTopic("stellar mass luminosity relation exponent", "astrophysics", "exponent", 1),
    ResearchTopic("main sequence lifetime scaling", "astrophysics", "exponent", 2),
    ResearchTopic("Salpeter IMF slope 2.35", "astrophysics", "exponent", 1),
    ResearchTopic("stellar IMF turnover mass", "astrophysics", "constant", 2),
    ResearchTopic("star formation efficiency per free fall", "astrophysics", "constant", 1),
    ResearchTopic("Tully-Fisher relation slope", "astrophysics", "exponent", 1),
    ResearchTopic("Faber-Jackson relation slope", "astrophysics", "exponent", 1),
    ResearchTopic("M-sigma black hole mass relation", "astrophysics", "exponent", 1),
    ResearchTopic("Eddington ratio AGN typical", "astrophysics", "constant", 2),
    ResearchTopic("jet Lorentz factor relativistic", "astrophysics", "constant", 2),
    ResearchTopic("supernova explosion energy 10^51 erg", "astrophysics", "constant", 1),
    ResearchTopic("gamma ray burst beaming factor", "astrophysics", "constant", 2),
    ResearchTopic("pulsar braking index", "astrophysics", "constant", 2),
    ResearchTopic("magnetar magnetic field strength", "astrophysics", "constant", 2),
    ResearchTopic("neutron star maximum mass TOV limit", "astrophysics", "constant", 1),
    ResearchTopic("white dwarf mass radius relation", "astrophysics", "exponent", 2),
    ResearchTopic("Kerr black hole efficiency maximum", "astrophysics", "constant", 1),
    ResearchTopic("accretion disk viscosity alpha parameter", "astrophysics", "constant", 2),
    ResearchTopic("Thomson scattering cross section", "astrophysics", "constant", 1),
    ResearchTopic("Lane-Emden polytrope constants", "astrophysics", "constant", 2),
    ResearchTopic("solar luminosity to mass ratio", "astrophysics", "ratio", 1),
    ResearchTopic("solar neutrino flux", "astrophysics", "constant", 2),
    ResearchTopic("Roche limit coefficient 2.44", "astrophysics", "constant", 1),
    ResearchTopic("Hill sphere radius factor", "astrophysics", "constant", 2),
    ResearchTopic("Titius-Bode law planetary spacing", "astrophysics", "constant", 1),
    ResearchTopic("planetary migration timescale", "astrophysics", "constant", 3),
    ResearchTopic("circumstellar habitable zone width", "astrophysics", "constant", 2),
    ResearchTopic("exoplanet occurrence rate", "astrophysics", "constant", 2),
    ResearchTopic("hot Jupiter frequency", "astrophysics", "constant", 2),
    ResearchTopic("super Earth frequency", "astrophysics", "constant", 2),
    ResearchTopic("galactic rotation curve flat velocity", "astrophysics", "constant", 2),
    ResearchTopic("NFW dark matter halo concentration", "astrophysics", "constant", 2),
    ResearchTopic("galaxy correlation function slope", "astrophysics", "exponent", 2),
    ResearchTopic("Schechter luminosity function parameters", "astrophysics", "constant", 2),
    ResearchTopic("cosmic star formation rate density peak", "astrophysics", "constant", 2),
    ResearchTopic("intergalactic medium temperature", "astrophysics", "constant", 2),
    ResearchTopic("Lyman alpha forest opacity", "astrophysics", "constant", 3),
    ResearchTopic("quasar luminosity function slope", "astrophysics", "exponent", 3),
    ResearchTopic("AGN duty cycle fraction", "astrophysics", "constant", 3),
    ResearchTopic("cosmic ray spectrum knee energy", "astrophysics", "constant", 2),
    ResearchTopic("cosmic ray spectrum slope", "astrophysics", "exponent", 2),
    ResearchTopic("diffuse gamma ray background", "astrophysics", "constant", 3),
    ResearchTopic("gravitational wave strain sensitivity", "astrophysics", "constant", 2),
    ResearchTopic("binary pulsar orbital decay", "astrophysics", "constant", 2),
    ResearchTopic("fast radio burst dispersion measure", "astrophysics", "constant", 3),
    ResearchTopic("kilonova luminosity peak", "astrophysics", "constant", 3),
    ResearchTopic("r-process nucleosynthesis yield", "astrophysics", "constant", 3),

    # =========================================================================
    # FLUID DYNAMICS (50 topics)
    # =========================================================================

    ResearchTopic("von Karman constant turbulence 0.41", "fluid_dynamics", "constant", 1),
    ResearchTopic("Strouhal number cylinder vortex shedding 0.21", "fluid_dynamics", "constant", 1),
    ResearchTopic("critical Reynolds number pipe flow 2300", "fluid_dynamics", "constant", 1),
    ResearchTopic("critical Reynolds number flat plate 500000", "fluid_dynamics", "constant", 1),
    ResearchTopic("Kolmogorov constant energy spectrum", "fluid_dynamics", "constant", 1),
    ResearchTopic("Kolmogorov -5/3 inertial range exponent", "fluid_dynamics", "exponent", 1),
    ResearchTopic("Richardson 4/3 turbulent diffusion", "fluid_dynamics", "exponent", 1),
    ResearchTopic("Smagorinsky constant LES 0.17", "fluid_dynamics", "constant", 1),
    ResearchTopic("critical Rayleigh number convection 1708", "fluid_dynamics", "constant", 1),
    ResearchTopic("critical Taylor number Couette flow", "fluid_dynamics", "constant", 1),
    ResearchTopic("critical Weber number droplet breakup 12", "fluid_dynamics", "constant", 1),
    ResearchTopic("sphere drag coefficient 0.47", "fluid_dynamics", "constant", 1),
    ResearchTopic("cylinder drag coefficient 1.2", "fluid_dynamics", "constant", 1),
    ResearchTopic("flat plate friction coefficient Blasius 1.328", "fluid_dynamics", "constant", 1),
    ResearchTopic("turbulent Prandtl number 0.85", "fluid_dynamics", "constant", 1),
    ResearchTopic("log law intercept B constant 5.2", "fluid_dynamics", "constant", 1),
    ResearchTopic("boundary layer shape factor Blasius 2.59", "fluid_dynamics", "constant", 1),
    ResearchTopic("jet entrainment coefficient 0.08", "fluid_dynamics", "constant", 2),
    ResearchTopic("Kelvin wake angle ship 19.47 degrees", "fluid_dynamics", "angle", 1),
    ResearchTopic("added mass coefficient sphere 0.5", "fluid_dynamics", "constant", 2),
    ResearchTopic("Basset history force coefficient", "fluid_dynamics", "constant", 2),
    ResearchTopic("Oseen drag correction 3/8", "fluid_dynamics", "constant", 2),
    ResearchTopic("critical Dean number curved pipe 36", "fluid_dynamics", "constant", 2),
    ResearchTopic("critical Grashof number natural convection", "fluid_dynamics", "constant", 2),
    ResearchTopic("Nusselt number turbulent correlation", "fluid_dynamics", "exponent", 2),
    ResearchTopic("Manning roughness coefficient natural channel", "fluid_dynamics", "constant", 2),
    ResearchTopic("Darcy Weisbach friction factor", "fluid_dynamics", "constant", 2),
    ResearchTopic("Moody diagram transition region", "fluid_dynamics", "constant", 2),
    ResearchTopic("Batchelor constant scalar variance", "fluid_dynamics", "constant", 2),
    ResearchTopic("Obukhov Corrsin constant temperature", "fluid_dynamics", "constant", 2),
    ResearchTopic("skewness factor velocity derivative -0.4", "fluid_dynamics", "constant", 2),
    ResearchTopic("flatness factor intermittency 7-8", "fluid_dynamics", "constant", 2),
    ResearchTopic("Taylor microscale Reynolds number", "fluid_dynamics", "constant", 2),
    ResearchTopic("integral length scale ratio", "fluid_dynamics", "ratio", 2),
    ResearchTopic("Kolmogorov microscale ratio", "fluid_dynamics", "ratio", 2),
    ResearchTopic("energy dissipation rate constant", "fluid_dynamics", "constant", 2),
    ResearchTopic("enstrophy production rate", "fluid_dynamics", "constant", 3),
    ResearchTopic("helicity cascade rate", "fluid_dynamics", "constant", 3),
    ResearchTopic("passive scalar variance decay", "fluid_dynamics", "exponent", 2),
    ResearchTopic("turbulent Schmidt number", "fluid_dynamics", "constant", 2),
    ResearchTopic("capillary number critical breakup", "fluid_dynamics", "constant", 2),
    ResearchTopic("Ohnesorge number atomization", "fluid_dynamics", "constant", 2),
    ResearchTopic("Eotvos number bubble shape", "fluid_dynamics", "constant", 2),
    ResearchTopic("Morton number buoyancy", "fluid_dynamics", "constant", 2),
    ResearchTopic("Froude number critical", "fluid_dynamics", "constant", 2),
    ResearchTopic("Mach number critical transonic", "fluid_dynamics", "constant", 2),
    ResearchTopic("lift coefficient airfoil 2pi", "fluid_dynamics", "constant", 1),
    ResearchTopic("lift to drag ratio optimal glider", "fluid_dynamics", "ratio", 2),
    ResearchTopic("boundary layer thickness ratio", "fluid_dynamics", "ratio", 2),
    ResearchTopic("separation bubble length ratio", "fluid_dynamics", "ratio", 3),

    # =========================================================================
    # GEOPHYSICS & EARTH SCIENCE (50 topics)
    # =========================================================================

    ResearchTopic("Earth oblateness flattening 1/298", "geophysics", "constant", 1),
    ResearchTopic("Chandler wobble period 433 days", "geophysics", "constant", 1),
    ResearchTopic("length of day secular change", "geophysics", "constant", 2),
    ResearchTopic("core mantle boundary radius ratio 0.546", "geophysics", "ratio", 1),
    ResearchTopic("inner outer core radius ratio 0.35", "geophysics", "ratio", 1),
    ResearchTopic("Moho depth continental crust 35 km", "geophysics", "constant", 1),
    ResearchTopic("lithosphere thickness thermal 100 km", "geophysics", "constant", 1),
    ResearchTopic("P wave S wave velocity ratio sqrt(3)", "geophysics", "ratio", 1),
    ResearchTopic("mantle Q attenuation factor 200-400", "geophysics", "constant", 2),
    ResearchTopic("adiabatic temperature gradient mantle", "geophysics", "constant", 2),
    ResearchTopic("plate velocity mean 5 cm/year", "geophysics", "constant", 1),
    ResearchTopic("subduction angle mean 45 degrees", "geophysics", "angle", 2),
    ResearchTopic("ridge push force magnitude", "geophysics", "constant", 2),
    ResearchTopic("slab pull force magnitude", "geophysics", "constant", 2),
    ResearchTopic("magnetic reversal rate per million years", "geophysics", "constant", 1),
    ResearchTopic("geomagnetic dipole tilt 11 degrees", "geophysics", "angle", 1),
    ResearchTopic("secular variation rate degrees per year", "geophysics", "constant", 2),
    ResearchTopic("dipole decay time constant", "geophysics", "constant", 2),
    ResearchTopic("critical magnetic Reynolds number dynamo", "geophysics", "constant", 1),
    ResearchTopic("Elsasser number Earth core", "geophysics", "constant", 2),
    ResearchTopic("heat flow global mean mW/m2", "geophysics", "constant", 1),
    ResearchTopic("radiogenic heat fraction", "geophysics", "constant", 2),
    ResearchTopic("mantle viscosity upper lower ratio", "geophysics", "ratio", 2),
    ResearchTopic("Gutenberg-Richter b value 1.0", "geophysics", "constant", 1),
    ResearchTopic("Omori aftershock p value", "geophysics", "exponent", 1),
    ResearchTopic("Bath law magnitude difference 1.2", "geophysics", "constant", 1),
    ResearchTopic("earthquake stress drop typical MPa", "geophysics", "constant", 2),
    ResearchTopic("seismic moment magnitude relation", "geophysics", "exponent", 1),
    ResearchTopic("fault rupture velocity ratio", "geophysics", "ratio", 2),
    ResearchTopic("earthquake recurrence interval", "geophysics", "constant", 2),
    ResearchTopic("volcano spacing arc 70 km", "geophysics", "constant", 2),
    ResearchTopic("eruption VEI frequency scaling", "geophysics", "exponent", 2),
    ResearchTopic("caldera collapse depth diameter ratio", "geophysics", "ratio", 2),
    ResearchTopic("magma viscosity range basalt rhyolite", "geophysics", "ratio", 2),
    ResearchTopic("tsunami wave speed scaling", "geophysics", "exponent", 2),
    ResearchTopic("landslide runout distance ratio", "geophysics", "ratio", 2),
    ResearchTopic("soil liquefaction threshold", "geophysics", "constant", 2),
    ResearchTopic("rock friction coefficient typical", "geophysics", "constant", 2),
    ResearchTopic("Byerlee law friction coefficient 0.6-0.85", "geophysics", "constant", 1),
    ResearchTopic("fault healing rate", "geophysics", "constant", 3),
    ResearchTopic("rate state friction parameters a-b", "geophysics", "constant", 2),
    ResearchTopic("slow slip event duration scaling", "geophysics", "exponent", 3),
    ResearchTopic("tremor amplitude scaling", "geophysics", "exponent", 3),
    ResearchTopic("GPS velocity uncertainty mm/year", "geophysics", "constant", 3),
    ResearchTopic("InSAR deformation precision cm", "geophysics", "constant", 3),
    ResearchTopic("gravity anomaly Bouguer correction", "geophysics", "constant", 2),
    ResearchTopic("geoid undulation maximum", "geophysics", "constant", 2),
    ResearchTopic("isostatic compensation depth", "geophysics", "constant", 2),
    ResearchTopic("flexural rigidity lithosphere", "geophysics", "constant", 2),
    ResearchTopic("effective elastic thickness", "geophysics", "constant", 2),

    # =========================================================================
    # ATMOSPHERIC & CLIMATE (50 topics)
    # =========================================================================

    ResearchTopic("atmospheric lapse rate 6.5 K/km", "atmospheric", "constant", 1),
    ResearchTopic("tropopause height mid-latitude 11 km", "atmospheric", "constant", 1),
    ResearchTopic("scale height atmosphere 8.5 km", "atmospheric", "constant", 1),
    ResearchTopic("critical Richardson number 0.25", "atmospheric", "constant", 1),
    ResearchTopic("bulk aerodynamic drag coefficient ocean", "atmospheric", "constant", 1),
    ResearchTopic("Charnock constant wave roughness 0.015", "atmospheric", "constant", 2),
    ResearchTopic("Priestley Taylor evaporation 1.26", "atmospheric", "constant", 2),
    ResearchTopic("Bowen ratio ocean typical 0.1", "atmospheric", "ratio", 2),
    ResearchTopic("Earth albedo planetary 0.30", "atmospheric", "constant", 1),
    ResearchTopic("effective emissivity greenhouse 0.61", "atmospheric", "constant", 1),
    ResearchTopic("solar constant 1361 W/m2", "atmospheric", "constant", 1),
    ResearchTopic("climate sensitivity ECS 3 degrees C", "atmospheric", "constant", 1),
    ResearchTopic("transient climate response TCR", "atmospheric", "constant", 1),
    ResearchTopic("TCR to ECS ratio 0.6", "atmospheric", "ratio", 1),
    ResearchTopic("carbon dioxide airborne fraction 0.45", "atmospheric", "constant", 1),
    ResearchTopic("ocean carbon uptake fraction 0.25", "atmospheric", "constant", 1),
    ResearchTopic("Revelle buffer factor 10", "atmospheric", "constant", 2),
    ResearchTopic("water vapor feedback W/m2/K 1.8", "atmospheric", "constant", 1),
    ResearchTopic("ice albedo feedback W/m2/K 0.3", "atmospheric", "constant", 1),
    ResearchTopic("cloud feedback W/m2/K", "atmospheric", "constant", 1),
    ResearchTopic("Planck feedback W/m2/K -3.2", "atmospheric", "constant", 1),
    ResearchTopic("Junge aerosol exponent 3", "atmospheric", "exponent", 2),
    ResearchTopic("CCN activation fraction", "atmospheric", "constant", 2),
    ResearchTopic("precipitation efficiency 0.2-0.5", "atmospheric", "constant", 2),
    ResearchTopic("hurricane wind pressure relation", "atmospheric", "exponent", 2),
    ResearchTopic("tornado intensity EF scale", "atmospheric", "constant", 2),
    ResearchTopic("lightning NOx production yield", "atmospheric", "constant", 2),
    ResearchTopic("Clausius Clapeyron scaling 7%/K", "atmospheric", "constant", 1),
    ResearchTopic("stratospheric ozone column Dobson", "atmospheric", "constant", 2),
    ResearchTopic("tropopause temperature 217 K", "atmospheric", "constant", 2),
    ResearchTopic("stratopause altitude 50 km", "atmospheric", "constant", 2),
    ResearchTopic("mesopause altitude 85 km", "atmospheric", "constant", 2),
    ResearchTopic("thermosphere temperature maximum", "atmospheric", "constant", 3),
    ResearchTopic("Karman line altitude 100 km", "atmospheric", "constant", 1),
    ResearchTopic("atmospheric CO2 concentration ppm", "atmospheric", "constant", 1),
    ResearchTopic("methane concentration ppb", "atmospheric", "constant", 2),
    ResearchTopic("N2O concentration ppb", "atmospheric", "constant", 2),
    ResearchTopic("ozone hole minimum Dobson units", "atmospheric", "constant", 2),
    ResearchTopic("polar vortex temperature threshold", "atmospheric", "constant", 2),
    ResearchTopic("QBO period months 28", "atmospheric", "constant", 2),
    ResearchTopic("ENSO period years 2-7", "atmospheric", "constant", 1),
    ResearchTopic("NAO index standard deviation", "atmospheric", "constant", 2),
    ResearchTopic("PDO period decades", "atmospheric", "constant", 2),
    ResearchTopic("AMO period decades", "atmospheric", "constant", 2),
    ResearchTopic("Madden Julian Oscillation period", "atmospheric", "constant", 2),
    ResearchTopic("monsoon onset date variability", "atmospheric", "constant", 3),
    ResearchTopic("jet stream latitude mean", "atmospheric", "constant", 2),
    ResearchTopic("Hadley cell extent latitude", "atmospheric", "constant", 2),
    ResearchTopic("Ferrel cell latitude range", "atmospheric", "constant", 2),
    ResearchTopic("trade wind speed typical m/s", "atmospheric", "constant", 2),

    # =========================================================================
    # OCEANOGRAPHY (40 topics)
    # =========================================================================

    ResearchTopic("Ekman depth wind mixing 100 m", "oceanography", "constant", 1),
    ResearchTopic("Ekman transport angle 45 degrees", "oceanography", "angle", 1),
    ResearchTopic("thermocline depth typical 500 m", "oceanography", "constant", 1),
    ResearchTopic("mixed layer depth seasonal", "oceanography", "constant", 1),
    ResearchTopic("thermohaline circulation strength 20 Sv", "oceanography", "constant", 1),
    ResearchTopic("Gulf Stream transport Sverdrups 30", "oceanography", "constant", 1),
    ResearchTopic("Antarctic Circumpolar Current 140 Sv", "oceanography", "constant", 1),
    ResearchTopic("tidal dissipation global 3.7 TW", "oceanography", "constant", 1),
    ResearchTopic("wind power input ocean 1 TW", "oceanography", "constant", 2),
    ResearchTopic("mesoscale eddy kinetic energy ratio", "oceanography", "ratio", 2),
    ResearchTopic("Rossby radius of deformation", "oceanography", "constant", 2),
    ResearchTopic("wave breaking steepness limit H/L 1/7", "oceanography", "ratio", 1),
    ResearchTopic("Stokes drift velocity ratio 0.01", "oceanography", "ratio", 2),
    ResearchTopic("significant wave height factor 4", "oceanography", "constant", 1),
    ResearchTopic("diapycnal mixing diffusivity background", "oceanography", "constant", 2),
    ResearchTopic("isopycnal mixing diffusivity 1000 m2/s", "oceanography", "constant", 2),
    ResearchTopic("mixing efficiency Osborn 0.2", "oceanography", "constant", 1),
    ResearchTopic("thermal expansion coefficient seawater", "oceanography", "constant", 2),
    ResearchTopic("haline contraction coefficient", "oceanography", "constant", 2),
    ResearchTopic("density ratio double diffusion", "oceanography", "ratio", 2),
    ResearchTopic("sea surface temperature global mean", "oceanography", "constant", 1),
    ResearchTopic("sea surface salinity global mean psu", "oceanography", "constant", 1),
    ResearchTopic("ocean heat content trend J/year", "oceanography", "constant", 2),
    ResearchTopic("sea level rise rate mm/year", "oceanography", "constant", 1),
    ResearchTopic("thermal expansion contribution SLR", "oceanography", "constant", 2),
    ResearchTopic("ice sheet mass loss Gt/year", "oceanography", "constant", 1),
    ResearchTopic("ocean pH current 8.1", "oceanography", "constant", 1),
    ResearchTopic("carbonate saturation state", "oceanography", "constant", 2),
    ResearchTopic("aragonite saturation horizon depth", "oceanography", "constant", 2),
    ResearchTopic("biological pump efficiency", "oceanography", "constant", 2),
    ResearchTopic("primary production global Gt C/year", "oceanography", "constant", 1),
    ResearchTopic("export production ratio e-ratio", "oceanography", "ratio", 2),
    ResearchTopic("remineralization length scale", "oceanography", "constant", 2),
    ResearchTopic("Redfield ratio C:N:P 106:16:1", "oceanography", "ratio", 1),
    ResearchTopic("oxygen minimum zone depth", "oceanography", "constant", 2),
    ResearchTopic("SOFAR channel depth 1000 m", "oceanography", "constant", 2),
    ResearchTopic("sound speed minimum depth", "oceanography", "constant", 2),
    ResearchTopic("acoustic transmission loss", "oceanography", "constant", 3),
    ResearchTopic("coral reef calcification rate", "oceanography", "constant", 2),
    ResearchTopic("marine biodiversity latitudinal gradient", "oceanography", "exponent", 2),

    # =========================================================================
    # BIOLOGY - ALLOMETRY & SCALING (50 topics)
    # =========================================================================

    ResearchTopic("Kleiber law metabolic exponent 3/4", "biology_scaling", "exponent", 1),
    ResearchTopic("heart rate body mass scaling -1/4", "biology_scaling", "exponent", 1),
    ResearchTopic("lifespan body mass scaling 1/4", "biology_scaling", "exponent", 1),
    ResearchTopic("brain size body mass exponent 0.75", "biology_scaling", "exponent", 1),
    ResearchTopic("respiratory quotient RQ 0.82", "biology_scaling", "constant", 1),
    ResearchTopic("oxygen extraction fraction 0.25", "biology_scaling", "constant", 2),
    ResearchTopic("VO2max body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("blood pressure mammals constant 100 mmHg", "biology_scaling", "constant", 1),
    ResearchTopic("hematocrit optimal 0.45", "biology_scaling", "constant", 1),
    ResearchTopic("cardiac output body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("stroke volume body mass scaling 1.0", "biology_scaling", "exponent", 2),
    ResearchTopic("capillary spacing diffusion distance", "biology_scaling", "constant", 2),
    ResearchTopic("mitochondrial density scaling -0.25", "biology_scaling", "exponent", 2),
    ResearchTopic("synapse density cortex per mm3", "biology_scaling", "constant", 2),
    ResearchTopic("nerve conduction velocity myelinated", "biology_scaling", "constant", 1),
    ResearchTopic("reaction time body mass scaling 0.25", "biology_scaling", "exponent", 2),
    ResearchTopic("gestation period body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("age at maturity body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("maximum lifespan body mass scaling", "biology_scaling", "exponent", 1),
    ResearchTopic("maximum running speed body mass", "biology_scaling", "exponent", 2),
    ResearchTopic("cost of transport body mass -0.25", "biology_scaling", "exponent", 1),
    ResearchTopic("Froude number optimal walk run 0.25", "biology_scaling", "constant", 1),
    ResearchTopic("muscle power output scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("bone strength body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("flight speed body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("swimming speed body mass scaling 0.5", "biology_scaling", "exponent", 2),
    ResearchTopic("wing loading body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("tree height diameter scaling 2/3", "biology_scaling", "exponent", 1),
    ResearchTopic("leaf area index typical", "biology_scaling", "constant", 2),
    ResearchTopic("root shoot ratio plants", "biology_scaling", "ratio", 2),
    ResearchTopic("specific leaf area scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("stem hydraulic conductivity scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("stomatal conductance scaling", "biology_scaling", "exponent", 3),
    ResearchTopic("photosynthesis light saturation", "biology_scaling", "constant", 2),
    ResearchTopic("respiration Q10 temperature coefficient", "biology_scaling", "constant", 1),
    ResearchTopic("enzyme turnover number typical", "biology_scaling", "constant", 2),
    ResearchTopic("Michaelis constant Km typical", "biology_scaling", "constant", 2),
    ResearchTopic("catalytic perfection limit", "biology_scaling", "constant", 2),
    ResearchTopic("protein folding rate scaling", "biology_scaling", "exponent", 3),
    ResearchTopic("DNA replication rate bp/s", "biology_scaling", "constant", 2),
    ResearchTopic("mutation rate per base pair", "biology_scaling", "constant", 2),
    ResearchTopic("genome size body mass scaling", "biology_scaling", "exponent", 3),
    ResearchTopic("cell division rate body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("telomere shortening rate", "biology_scaling", "constant", 3),
    ResearchTopic("circadian period hours", "biology_scaling", "constant", 1),
    ResearchTopic("sleep duration body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("fasting endurance body mass scaling", "biology_scaling", "exponent", 2),
    ResearchTopic("population density body mass -0.75", "biology_scaling", "exponent", 1),
    ResearchTopic("home range body mass scaling 1.0", "biology_scaling", "exponent", 1),
    ResearchTopic("territory size body mass scaling", "biology_scaling", "exponent", 2),

    # =========================================================================
    # ECOLOGY & POPULATION (40 topics)
    # =========================================================================

    ResearchTopic("species area exponent z 0.25", "ecology", "exponent", 1),
    ResearchTopic("Fisher alpha diversity index", "ecology", "constant", 2),
    ResearchTopic("Preston lognormal parameter", "ecology", "constant", 2),
    ResearchTopic("predator prey mass ratio 100-1000", "ecology", "ratio", 1),
    ResearchTopic("trophic transfer efficiency 10%", "ecology", "constant", 1),
    ResearchTopic("assimilation efficiency herbivore 0.7", "ecology", "constant", 2),
    ResearchTopic("production efficiency 0.3", "ecology", "constant", 2),
    ResearchTopic("intrinsic rate of increase r_max", "ecology", "constant", 2),
    ResearchTopic("carrying capacity body mass scaling", "ecology", "exponent", 2),
    ResearchTopic("generation time body mass scaling 0.25", "ecology", "exponent", 1),
    ResearchTopic("background extinction rate per Myr", "ecology", "constant", 1),
    ResearchTopic("speciation rate per Myr", "ecology", "constant", 2),
    ResearchTopic("species turnover rate", "ecology", "constant", 2),
    ResearchTopic("food web connectance 0.1", "ecology", "constant", 1),
    ResearchTopic("food chain length typical 4", "ecology", "constant", 1),
    ResearchTopic("omnivory index food webs", "ecology", "constant", 2),
    ResearchTopic("succession half life years", "ecology", "constant", 2),
    ResearchTopic("fire return interval years", "ecology", "constant", 2),
    ResearchTopic("decomposition rate litter k", "ecology", "constant", 2),
    ResearchTopic("seed dispersal kernel decay", "ecology", "exponent", 2),
    ResearchTopic("seed bank half life years", "ecology", "constant", 2),
    ResearchTopic("pollinator visitation rate", "ecology", "constant", 3),
    ResearchTopic("herbivory fraction biomass 0.1", "ecology", "constant", 2),
    ResearchTopic("net primary production global", "ecology", "constant", 1),
    ResearchTopic("gross primary production global", "ecology", "constant", 1),
    ResearchTopic("autotrophic respiration fraction", "ecology", "constant", 2),
    ResearchTopic("carbon use efficiency plants", "ecology", "constant", 2),
    ResearchTopic("nitrogen use efficiency", "ecology", "constant", 2),
    ResearchTopic("nutrient limitation threshold", "ecology", "constant", 2),
    ResearchTopic("light compensation point", "ecology", "constant", 2),
    ResearchTopic("photoinhibition threshold", "ecology", "constant", 3),
    ResearchTopic("carbon flux NEE typical", "ecology", "constant", 2),
    ResearchTopic("soil respiration Q10", "ecology", "constant", 2),
    ResearchTopic("mycorrhizal colonization fraction", "ecology", "constant", 2),
    ResearchTopic("nitrogen fixation rate", "ecology", "constant", 2),
    ResearchTopic("denitrification rate", "ecology", "constant", 2),
    ResearchTopic("methane flux wetlands", "ecology", "constant", 2),
    ResearchTopic("biodiversity productivity relationship", "ecology", "exponent", 2),
    ResearchTopic("stability diversity relationship", "ecology", "exponent", 2),
    ResearchTopic("resilience recovery time scaling", "ecology", "exponent", 2),

    # =========================================================================
    # CONDENSED MATTER PHYSICS (40 topics)
    # =========================================================================

    ResearchTopic("Lindemann melting criterion 0.1-0.2", "condensed_matter", "constant", 1),
    ResearchTopic("Born stability criterion", "condensed_matter", "constant", 2),
    ResearchTopic("glass transition Tg/Tm ratio 0.6", "condensed_matter", "ratio", 1),
    ResearchTopic("Kauzmann temperature ratio Tk/Tm", "condensed_matter", "ratio", 2),
    ResearchTopic("fragility index glass formers", "condensed_matter", "constant", 2),
    ResearchTopic("Poisson ratio typical metals 0.3", "condensed_matter", "constant", 1),
    ResearchTopic("Gruneisen parameter typical 2", "condensed_matter", "constant", 2),
    ResearchTopic("Debye temperature typical K", "condensed_matter", "constant", 2),
    ResearchTopic("Hall Petch grain size exponent 0.5", "condensed_matter", "exponent", 1),
    ResearchTopic("creep power law exponent 3-5", "condensed_matter", "exponent", 2),
    ResearchTopic("fatigue S-N curve exponent", "condensed_matter", "exponent", 2),
    ResearchTopic("fracture toughness Griffith", "condensed_matter", "constant", 2),
    ResearchTopic("percolation threshold 2D square 0.59", "condensed_matter", "constant", 1),
    ResearchTopic("percolation threshold 3D simple cubic", "condensed_matter", "constant", 1),
    ResearchTopic("percolation nu exponent 2D 4/3", "condensed_matter", "exponent", 1),
    ResearchTopic("percolation beta exponent 2D 5/36", "condensed_matter", "exponent", 1),
    ResearchTopic("Ising beta exponent 2D 1/8", "condensed_matter", "exponent", 1),
    ResearchTopic("Ising gamma exponent 2D 7/4", "condensed_matter", "exponent", 1),
    ResearchTopic("Ising nu exponent 2D 1", "condensed_matter", "exponent", 1),
    ResearchTopic("3D Ising beta exponent 0.326", "condensed_matter", "exponent", 1),
    ResearchTopic("3D Ising gamma exponent 1.237", "condensed_matter", "exponent", 1),
    ResearchTopic("3D Ising nu exponent 0.630", "condensed_matter", "exponent", 1),
    ResearchTopic("3D XY beta exponent 0.348", "condensed_matter", "exponent", 2),
    ResearchTopic("3D Heisenberg beta exponent 0.365", "condensed_matter", "exponent", 2),
    ResearchTopic("BCS gap ratio 2Delta/kTc 3.5", "condensed_matter", "constant", 1),
    ResearchTopic("London penetration depth nm", "condensed_matter", "constant", 2),
    ResearchTopic("coherence length superconductor", "condensed_matter", "constant", 2),
    ResearchTopic("upper critical field Hc2", "condensed_matter", "constant", 2),
    ResearchTopic("quantum Hall plateau width", "condensed_matter", "constant", 2),
    ResearchTopic("von Klitzing constant h/e^2", "condensed_matter", "constant", 1),
    ResearchTopic("Laughlin 1/3 filling fraction", "condensed_matter", "constant", 1),
    ResearchTopic("Jain sequence filling fractions", "condensed_matter", "constant", 2),
    ResearchTopic("Kondo temperature typical K", "condensed_matter", "constant", 2),
    ResearchTopic("Anderson localization threshold", "condensed_matter", "constant", 2),
    ResearchTopic("Mott transition density", "condensed_matter", "constant", 2),
    ResearchTopic("Fermi liquid effective mass ratio", "condensed_matter", "ratio", 2),
    ResearchTopic("heavy fermion mass enhancement", "condensed_matter", "ratio", 2),
    ResearchTopic("magnetoresistance giant ratio", "condensed_matter", "ratio", 2),
    ResearchTopic("spin Hall angle typical", "condensed_matter", "constant", 2),
    ResearchTopic("topological insulator gap meV", "condensed_matter", "constant", 2),

    # =========================================================================
    # CHEMISTRY & MOLECULAR (40 topics)
    # =========================================================================

    ResearchTopic("water bond angle H-O-H 104.5 degrees", "chemistry", "angle", 1),
    ResearchTopic("ammonia bond angle H-N-H 107 degrees", "chemistry", "angle", 1),
    ResearchTopic("methane tetrahedral angle 109.47", "chemistry", "angle", 1),
    ResearchTopic("carbon dioxide linear 180 degrees", "chemistry", "angle", 1),
    ResearchTopic("hydrogen sulfide bond angle 92 degrees", "chemistry", "angle", 2),
    ResearchTopic("phosphine bond angle PH3", "chemistry", "angle", 2),
    ResearchTopic("sulfur dioxide bond angle", "chemistry", "angle", 2),
    ResearchTopic("sp3 hybridization angle tetrahedral", "chemistry", "angle", 1),
    ResearchTopic("sp2 hybridization angle trigonal 120", "chemistry", "angle", 1),
    ResearchTopic("gauche dihedral angle 60 degrees", "chemistry", "angle", 2),
    ResearchTopic("anti dihedral angle 180 degrees", "chemistry", "angle", 2),
    ResearchTopic("peptide bond planarity omega angle", "chemistry", "angle", 2),
    ResearchTopic("protein phi psi alpha helix angles", "chemistry", "angle", 2),
    ResearchTopic("DNA base pair rise 0.34 nm", "chemistry", "constant", 1),
    ResearchTopic("DNA helix pitch 3.4 nm", "chemistry", "constant", 1),
    ResearchTopic("DNA base pairs per turn 10.5", "chemistry", "constant", 1),
    ResearchTopic("alpha helix rise per residue 0.15 nm", "chemistry", "constant", 2),
    ResearchTopic("alpha helix pitch 0.54 nm", "chemistry", "constant", 2),
    ResearchTopic("alpha helix residues per turn 3.6", "chemistry", "constant", 1),
    ResearchTopic("beta sheet rise per residue 0.35 nm", "chemistry", "constant", 2),
    ResearchTopic("Ramachandran allowed region fraction", "chemistry", "constant", 2),
    ResearchTopic("hydrogen bond energy kJ/mol", "chemistry", "constant", 1),
    ResearchTopic("van der Waals radius carbon", "chemistry", "constant", 2),
    ResearchTopic("covalent bond length C-C", "chemistry", "constant", 1),
    ResearchTopic("electronegativity Pauling scale oxygen", "chemistry", "constant", 1),
    ResearchTopic("ionization energy hydrogen 13.6 eV", "chemistry", "constant", 1),
    ResearchTopic("electron affinity chlorine", "chemistry", "constant", 2),
    ResearchTopic("lattice energy NaCl kJ/mol", "chemistry", "constant", 2),
    ResearchTopic("activation energy typical kJ/mol", "chemistry", "constant", 2),
    ResearchTopic("Arrhenius pre-exponential factor", "chemistry", "constant", 2),
    ResearchTopic("rate constant diffusion limit", "chemistry", "constant", 2),
    ResearchTopic("Marcus reorganization energy", "chemistry", "constant", 3),
    ResearchTopic("Born solvation energy", "chemistry", "constant", 2),
    ResearchTopic("dielectric constant water 80", "chemistry", "constant", 1),
    ResearchTopic("surface tension water 72 mN/m", "chemistry", "constant", 1),
    ResearchTopic("viscosity water 1 mPa s", "chemistry", "constant", 1),
    ResearchTopic("thermal conductivity water", "chemistry", "constant", 2),
    ResearchTopic("heat capacity water 4.18 J/g/K", "chemistry", "constant", 1),
    ResearchTopic("ice water density ratio 0.917", "chemistry", "ratio", 1),
    ResearchTopic("critical point water temperature K", "chemistry", "constant", 1),

    # =========================================================================
    # NETWORKS & COMPLEXITY (30 topics)
    # =========================================================================

    ResearchTopic("scale free network exponent 2-3", "networks", "exponent", 1),
    ResearchTopic("small world clustering coefficient 0.6", "networks", "constant", 1),
    ResearchTopic("six degrees of separation", "networks", "constant", 1),
    ResearchTopic("Dunbar number social group 150", "networks", "constant", 1),
    ResearchTopic("network modularity optimal 0.3-0.7", "networks", "constant", 2),
    ResearchTopic("assortative mixing coefficient", "networks", "constant", 2),
    ResearchTopic("rich club coefficient", "networks", "constant", 2),
    ResearchTopic("cascading failure threshold 0.18", "networks", "constant", 2),
    ResearchTopic("epidemic threshold R0 = 1", "networks", "constant", 1),
    ResearchTopic("voter model consensus time scaling", "networks", "exponent", 2),
    ResearchTopic("Schelling segregation threshold 0.35", "networks", "constant", 2),
    ResearchTopic("El Farol bar attendance 0.6", "networks", "constant", 2),
    ResearchTopic("traffic congestion phase transition", "networks", "constant", 2),
    ResearchTopic("Braess paradox efficiency factor", "networks", "constant", 2),
    ResearchTopic("Metcalfe law network value exponent 2", "networks", "exponent", 1),
    ResearchTopic("power grid failure cascade exponent", "networks", "exponent", 2),
    ResearchTopic("internet degree distribution exponent", "networks", "exponent", 1),
    ResearchTopic("WWW hyperlink distribution exponent", "networks", "exponent", 2),
    ResearchTopic("citation network exponent", "networks", "exponent", 2),
    ResearchTopic("protein interaction degree exponent", "networks", "exponent", 2),
    ResearchTopic("metabolic network diameter", "networks", "constant", 2),
    ResearchTopic("neural network connectivity", "networks", "constant", 2),
    ResearchTopic("airline network hub dominance", "networks", "constant", 2),
    ResearchTopic("social network transitivity", "networks", "constant", 2),
    ResearchTopic("collaboration network clustering", "networks", "constant", 2),
    ResearchTopic("Wikipedia link structure", "networks", "exponent", 3),
    ResearchTopic("email network reciprocity", "networks", "constant", 3),
    ResearchTopic("mobile phone call duration exponent", "networks", "exponent", 3),
    ResearchTopic("Twitter follower distribution", "networks", "exponent", 2),
    ResearchTopic("Facebook friend distribution", "networks", "exponent", 2),

    # =========================================================================
    # URBAN SCALING & ECONOMICS (30 topics)
    # =========================================================================

    ResearchTopic("urban population scaling exponent 1.15", "urban", "exponent", 1),
    ResearchTopic("urban infrastructure scaling 0.85", "urban", "exponent", 1),
    ResearchTopic("crime rate city size scaling 1.16", "urban", "exponent", 1),
    ResearchTopic("patent production scaling 1.27", "urban", "exponent", 1),
    ResearchTopic("GDP city size scaling 1.13", "urban", "exponent", 1),
    ResearchTopic("walking pace city size scaling", "urban", "exponent", 2),
    ResearchTopic("Marchetti constant commute time 30 min", "urban", "constant", 1),
    ResearchTopic("travel time budget 1.1 hours/day", "urban", "constant", 1),
    ResearchTopic("trip rate per day 3.5", "urban", "constant", 2),
    ResearchTopic("Gini coefficient inequality 0.3-0.5", "urban", "constant", 1),
    ResearchTopic("Pareto wealth exponent", "urban", "exponent", 1),
    ResearchTopic("Zipf city size exponent", "urban", "exponent", 1),
    ResearchTopic("rank size rule exponent", "urban", "exponent", 1),
    ResearchTopic("gravity model distance exponent", "urban", "exponent", 2),
    ResearchTopic("Phillips curve unemployment inflation", "urban", "exponent", 2),
    ResearchTopic("Okun law GDP unemployment coefficient 2", "urban", "constant", 1),
    ResearchTopic("Verdoorn productivity output coefficient", "urban", "constant", 2),
    ResearchTopic("learning curve cost reduction 0.2", "urban", "exponent", 1),
    ResearchTopic("technology S-curve inflection 0.5", "urban", "constant", 1),
    ResearchTopic("Bass diffusion innovation p 0.03", "urban", "constant", 2),
    ResearchTopic("Bass diffusion imitation q 0.38", "urban", "constant", 2),
    ResearchTopic("Engel coefficient food expenditure 0.3", "urban", "constant", 2),
    ResearchTopic("price elasticity of demand food -0.5", "urban", "constant", 2),
    ResearchTopic("income elasticity luxury goods", "urban", "constant", 2),
    ResearchTopic("firm size distribution exponent", "urban", "exponent", 2),
    ResearchTopic("stock return distribution tail exponent", "urban", "exponent", 2),
    ResearchTopic("volatility clustering GARCH parameters", "urban", "constant", 3),
    ResearchTopic("housing price income ratio", "urban", "ratio", 2),
    ResearchTopic("rent to price ratio", "urban", "ratio", 2),
    ResearchTopic("infrastructure investment multiplier", "urban", "constant", 2),

    # =========================================================================
    # PSYCHOLOGY & COGNITION (30 topics)
    # =========================================================================

    ResearchTopic("Miller number working memory 7 plus minus 2", "psychology", "constant", 1),
    ResearchTopic("Ebbinghaus forgetting curve exponent 0.5", "psychology", "exponent", 1),
    ResearchTopic("power law of learning exponent 0.4", "psychology", "exponent", 1),
    ResearchTopic("spacing effect optimal gap ratio", "psychology", "ratio", 2),
    ResearchTopic("Weber fraction just noticeable difference", "psychology", "constant", 1),
    ResearchTopic("Stevens power law brightness 0.33", "psychology", "exponent", 1),
    ResearchTopic("Stevens power law loudness 0.67", "psychology", "exponent", 1),
    ResearchTopic("Stevens power law pain 2.0", "psychology", "exponent", 2),
    ResearchTopic("Fitts law movement time slope", "psychology", "constant", 1),
    ResearchTopic("Hick law choice reaction time slope", "psychology", "constant", 1),
    ResearchTopic("Stroop interference effect ms", "psychology", "constant", 2),
    ResearchTopic("attentional blink duration 500 ms", "psychology", "constant", 2),
    ResearchTopic("change blindness detection rate", "psychology", "constant", 2),
    ResearchTopic("inattentional blindness rate", "psychology", "constant", 2),
    ResearchTopic("false memory DRM paradigm rate", "psychology", "constant", 2),
    ResearchTopic("overconfidence bias calibration error", "psychology", "constant", 2),
    ResearchTopic("anchoring effect adjustment factor", "psychology", "constant", 2),
    ResearchTopic("confirmation bias selection rate", "psychology", "constant", 2),
    ResearchTopic("loss aversion ratio 2.0", "psychology", "ratio", 1),
    ResearchTopic("time discounting hyperbolic k", "psychology", "constant", 2),
    ResearchTopic("risk aversion coefficient", "psychology", "constant", 2),
    ResearchTopic("prospect theory value function alpha", "psychology", "exponent", 2),
    ResearchTopic("mental rotation rate degrees/second", "psychology", "constant", 2),
    ResearchTopic("subitizing limit 4 items", "psychology", "constant", 1),
    ResearchTopic("iconic memory duration ms", "psychology", "constant", 2),
    ResearchTopic("echoic memory duration seconds", "psychology", "constant", 2),
    ResearchTopic("long term memory capacity bits", "psychology", "constant", 2),
    ResearchTopic("reading speed words per minute", "psychology", "constant", 2),
    ResearchTopic("speech rate syllables per second", "psychology", "constant", 2),
    ResearchTopic("saccade duration ms", "psychology", "constant", 2),

    # =========================================================================
    # CHAOS & FRACTALS (30 topics)
    # =========================================================================

    ResearchTopic("Feigenbaum delta constant 4.669", "chaos", "constant", 1),
    ResearchTopic("Feigenbaum alpha constant 2.502", "chaos", "constant", 1),
    ResearchTopic("logistic map onset of chaos r 3.57", "chaos", "constant", 1),
    ResearchTopic("period 3 window logistic map", "chaos", "constant", 2),
    ResearchTopic("Lorenz attractor dimension 2.06", "chaos", "constant", 1),
    ResearchTopic("Henon attractor dimension 1.26", "chaos", "constant", 2),
    ResearchTopic("Rossler attractor dimension", "chaos", "constant", 2),
    ResearchTopic("coastline fractal dimension Britain 1.25", "chaos", "constant", 1),
    ResearchTopic("Mandelbrot set boundary dimension 2", "chaos", "constant", 1),
    ResearchTopic("Cantor set fractal dimension ln2/ln3", "chaos", "constant", 1),
    ResearchTopic("Sierpinski triangle dimension ln3/ln2", "chaos", "constant", 1),
    ResearchTopic("Koch snowflake dimension ln4/ln3", "chaos", "constant", 1),
    ResearchTopic("Menger sponge dimension ln20/ln3", "chaos", "constant", 2),
    ResearchTopic("Hurst exponent long memory 0.7", "chaos", "exponent", 1),
    ResearchTopic("DFA scaling exponent healthy heart 1.0", "chaos", "exponent", 2),
    ResearchTopic("Lyapunov exponent positive chaos", "chaos", "constant", 2),
    ResearchTopic("Kolmogorov-Sinai entropy rate", "chaos", "constant", 2),
    ResearchTopic("correlation dimension strange attractor", "chaos", "constant", 2),
    ResearchTopic("embedding dimension typical", "chaos", "constant", 2),
    ResearchTopic("recurrence rate time series", "chaos", "constant", 2),
    ResearchTopic("lacunarity fractal measure", "chaos", "constant", 3),
    ResearchTopic("multifractal spectrum width", "chaos", "constant", 2),
    ResearchTopic("Holder exponent singularity", "chaos", "exponent", 3),
    ResearchTopic("intermittency exponent type I", "chaos", "exponent", 2),
    ResearchTopic("crisis induced intermittency", "chaos", "exponent", 3),
    ResearchTopic("transient chaos escape rate", "chaos", "constant", 2),
    ResearchTopic("riddled basin fractal dimension", "chaos", "constant", 3),
    ResearchTopic("blowout bifurcation threshold", "chaos", "constant", 3),
    ResearchTopic("synchronization threshold coupling", "chaos", "constant", 2),
    ResearchTopic("chimera state frequency ratio", "chaos", "ratio", 3),

    # =========================================================================
    # INFORMATION THEORY (20 topics)
    # =========================================================================

    ResearchTopic("Shannon entropy maximum binary 1 bit", "information", "constant", 1),
    ResearchTopic("English language entropy bits/char 1.3", "information", "constant", 1),
    ResearchTopic("English redundancy 0.75", "information", "constant", 1),
    ResearchTopic("Shannon channel capacity limit", "information", "constant", 1),
    ResearchTopic("Huffman coding efficiency 0.95", "information", "constant", 2),
    ResearchTopic("LZ77 compression ratio text 0.4", "information", "ratio", 2),
    ResearchTopic("JPEG compression ratio typical", "information", "ratio", 2),
    ResearchTopic("video compression H264 ratio", "information", "ratio", 2),
    ResearchTopic("Hamming 7,4 code rate 4/7", "information", "ratio", 1),
    ResearchTopic("Reed-Solomon code rate typical", "information", "ratio", 2),
    ResearchTopic("turbo code capacity approach", "information", "constant", 2),
    ResearchTopic("LDPC code rate 5G", "information", "ratio", 2),
    ResearchTopic("error correction threshold quantum", "information", "constant", 2),
    ResearchTopic("Kolmogorov complexity random string", "information", "constant", 2),
    ResearchTopic("transfer entropy causality measure", "information", "constant", 2),
    ResearchTopic("mutual information typical correlation", "information", "constant", 2),
    ResearchTopic("channel capacity AWGN", "information", "constant", 2),
    ResearchTopic("rate distortion function", "information", "constant", 3),
    ResearchTopic("source coding theorem efficiency", "information", "constant", 2),
    ResearchTopic("cryptographic key length bits", "information", "constant", 2),

    # =========================================================================
    # ACOUSTICS & MUSIC (20 topics)
    # =========================================================================

    ResearchTopic("perfect fifth frequency ratio 3/2", "acoustics", "ratio", 1),
    ResearchTopic("perfect fourth frequency ratio 4/3", "acoustics", "ratio", 1),
    ResearchTopic("major third just intonation 5/4", "acoustics", "ratio", 1),
    ResearchTopic("equal temperament semitone 2^(1/12)", "acoustics", "ratio", 1),
    ResearchTopic("Pythagorean comma frequency ratio", "acoustics", "ratio", 1),
    ResearchTopic("syntonic comma 81/80", "acoustics", "ratio", 2),
    ResearchTopic("concert hall reverberation time 2 sec", "acoustics", "constant", 1),
    ResearchTopic("speech clarity C50 dB", "acoustics", "constant", 2),
    ResearchTopic("critical distance room acoustics", "acoustics", "constant", 2),
    ResearchTopic("A-weighting 1kHz reference", "acoustics", "constant", 2),
    ResearchTopic("hearing threshold 0 dB SPL", "acoustics", "constant", 1),
    ResearchTopic("pain threshold 120 dB SPL", "acoustics", "constant", 1),
    ResearchTopic("speech frequency range Hz", "acoustics", "constant", 1),
    ResearchTopic("music frequency range Hz", "acoustics", "constant", 1),
    ResearchTopic("voice fundamental frequency male Hz", "acoustics", "constant", 2),
    ResearchTopic("masking threshold bandwidth", "acoustics", "constant", 2),
    ResearchTopic("binaural localization threshold degrees", "acoustics", "constant", 2),
    ResearchTopic("temporal resolution hearing ms", "acoustics", "constant", 2),
    ResearchTopic("frequency resolution hearing cents", "acoustics", "constant", 2),
    ResearchTopic("loudness scaling sone relation", "acoustics", "exponent", 2),

    # =========================================================================
    # OPTICS & VISION (20 topics)
    # =========================================================================

    ResearchTopic("human eye focal length 17 mm", "optics", "constant", 1),
    ResearchTopic("pupil diameter range 2-8 mm", "optics", "constant", 1),
    ResearchTopic("accommodation range young adult 10 D", "optics", "constant", 1),
    ResearchTopic("rod cone ratio retina 20:1", "optics", "ratio", 1),
    ResearchTopic("foveal cone spacing microns", "optics", "constant", 2),
    ResearchTopic("visual angle resolution 1 arc minute", "optics", "constant", 1),
    ResearchTopic("L cone peak wavelength 564 nm", "optics", "constant", 1),
    ResearchTopic("M cone peak wavelength 534 nm", "optics", "constant", 1),
    ResearchTopic("S cone peak wavelength 420 nm", "optics", "constant", 1),
    ResearchTopic("rod peak wavelength 498 nm", "optics", "constant", 1),
    ResearchTopic("luminous efficacy maximum 683 lm/W", "optics", "constant", 1),
    ResearchTopic("water refractive index 1.333", "optics", "constant", 1),
    ResearchTopic("crown glass refractive index 1.52", "optics", "constant", 1),
    ResearchTopic("diamond refractive index 2.42", "optics", "constant", 1),
    ResearchTopic("cornea refractive index 1.376", "optics", "constant", 2),
    ResearchTopic("eye lens refractive index 1.406", "optics", "constant", 2),
    ResearchTopic("critical angle total internal reflection", "optics", "angle", 2),
    ResearchTopic("Brewster angle glass", "optics", "angle", 2),
    ResearchTopic("rainbow angle 42 degrees", "optics", "angle", 1),
    ResearchTopic("diffraction limit Rayleigh criterion", "optics", "constant", 2),

    # =========================================================================
    # GEOMORPHOLOGY (20 topics)
    # =========================================================================

    ResearchTopic("Hack law river length area exponent 0.57", "geomorphology", "exponent", 1),
    ResearchTopic("Horton bifurcation ratio 3-5", "geomorphology", "ratio", 1),
    ResearchTopic("Horton length ratio 2-3", "geomorphology", "ratio", 1),
    ResearchTopic("stream order fractal dimension", "geomorphology", "constant", 2),
    ResearchTopic("drainage density typical km/km2", "geomorphology", "constant", 2),
    ResearchTopic("Manning roughness natural channel 0.035", "geomorphology", "constant", 1),
    ResearchTopic("channel width depth ratio 10", "geomorphology", "ratio", 2),
    ResearchTopic("sinuosity meandering rivers 1.5", "geomorphology", "constant", 2),
    ResearchTopic("meander wavelength width ratio 10", "geomorphology", "ratio", 2),
    ResearchTopic("pool riffle spacing width ratio 6", "geomorphology", "ratio", 2),
    ResearchTopic("hillslope angle of repose 35 degrees", "geomorphology", "angle", 1),
    ResearchTopic("relief ratio typical basin 0.1", "geomorphology", "ratio", 2),
    ResearchTopic("hypsometric integral mature 0.5", "geomorphology", "constant", 2),
    ResearchTopic("denudation rate global mm/kyr", "geomorphology", "constant", 2),
    ResearchTopic("soil production rate mm/kyr", "geomorphology", "constant", 2),
    ResearchTopic("glacier accumulation area ratio 0.65", "geomorphology", "ratio", 2),
    ResearchTopic("beach slope sandy degrees", "geomorphology", "angle", 2),
    ResearchTopic("Bruun rule sea level response 100", "geomorphology", "constant", 2),
    ResearchTopic("cliff retreat rate m/year", "geomorphology", "constant", 2),
    ResearchTopic("delta progradation rate km/kyr", "geomorphology", "constant", 2),
]


def get_topics_by_domain(domain: str) -> List[ResearchTopic]:
    """Get all topics for a specific domain."""
    return [t for t in RESEARCH_TOPICS if t.domain == domain]


def get_topics_by_priority(priority: int) -> List[ResearchTopic]:
    """Get all topics with a specific priority level."""
    return [t for t in RESEARCH_TOPICS if t.priority == priority]


def get_all_domains() -> List[str]:
    """Get list of all unique domains."""
    return sorted(set(t.domain for t in RESEARCH_TOPICS))


def get_topic_count() -> int:
    """Get total number of research topics."""
    return len(RESEARCH_TOPICS)


if __name__ == "__main__":
    print("Z² AUTONOMOUS RESEARCH TOPICS")
    print("=" * 50)
    print(f"Total topics: {get_topic_count()}")
    print()
    print("Topics by domain:")
    for domain in get_all_domains():
        count = len(get_topics_by_domain(domain))
        print(f"  {domain}: {count}")
    print()
    print("Topics by priority:")
    for p in [1, 2, 3]:
        count = len(get_topics_by_priority(p))
        print(f"  Priority {p}: {count}")
