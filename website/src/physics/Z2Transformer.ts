/**
 * ================================================================================
 * Z2Transformer.ts - KINEMATIC ISOLATION PROTOCOL
 * ================================================================================
 *
 * STRICT ACCELERATION SANDBOXING
 *
 * This module enforces the critical separation between:
 * 1. GEOMETRIC SOLVER (For Light) - Photon paths, redshifts, lensing
 * 2. KINEMATIC SOLVER (For Matter) - Orbital dynamics, rotation curves
 *
 * The topological MOND effect (a_topo = c²/L_c) only affects matter kinematics
 * in the ultra-low acceleration regime. It NEVER touches photon geometry.
 *
 * Z² Framework v11.1.0
 * Author: Carl Zimmerman + Claude
 * Date: May 2026
 * ================================================================================
 */

// =============================================================================
// FUNDAMENTAL CONSTANTS - Z² LOCKED
// =============================================================================

export const Z2_CONSTANTS = {
  // Fundamental domain size
  L_C_GPC: 20.6,                           // Gpc
  L_C_MPC: 20600,                          // Mpc
  L_C_M: 6.355e26,                         // meters (20.6 Gpc)

  // Matter density (locked)
  OMEGA_M: 6/19,                           // = 0.315789...
  OMEGA_M_DECIMAL: 0.3158,

  // Speed of light
  C_M_S: 299792458,                        // m/s
  C_KM_S: 299792.458,                      // km/s

  // Newton's gravitational constant
  G_SI: 6.67430e-11,                       // m³/(kg·s²)

  // Hubble constant (Z² derived)
  H0_KM_S_MPC: 67.4,                       // km/s/Mpc

  // Topological MOND acceleration
  // a_topo = c² / L_c
  A_TOPO_M_S2: (299792458 ** 2) / (6.355e26),  // ≈ 1.41e-10 m/s²
  A0_MOND: 1.2e-10,                        // Classic MOND a0 (for reference)

  // Scale factors for visualization
  SCALE_MPC_TO_SCENE: 0.001,               // Mpc to scene units
  SCALE_AU_TO_SCENE: 0.00000000002,        // AU to scene units
  SCALE_KPC_TO_SCENE: 0.000001,            // kpc to scene units
} as const;

// Derived constants
export const DERIVED = {
  HALF_BOX_MPC: Z2_CONSTANTS.L_C_MPC / 2,
  HALF_BOX_SCENE: (Z2_CONSTANTS.L_C_MPC / 2) * Z2_CONSTANTS.SCALE_MPC_TO_SCENE,
  A_TOPO: Z2_CONSTANTS.A_TOPO_M_S2,
} as const;

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

export interface CartesianCoord {
  x: number;  // Mpc
  y: number;  // Mpc
  z: number;  // Mpc
}

export interface SphericalCoord {
  ra: number;   // degrees
  dec: number;  // degrees
  d: number;    // Mpc (comoving distance)
}

export interface CelestialObject {
  name?: string;
  position: CartesianCoord;
  redshift?: number;
  type: 'galaxy' | 'quasar' | 'cmb' | 'void' | 'cluster' | 'star' | 'planet';
  mass_solar?: number;
  measurement_type?: 'SPECTROSCOPY' | 'PHOTOMETRY' | 'RADIO' | 'XRAY' | 'ASTROMETRY' | 'MICROWAVE';
}

export interface OrbitalBody {
  name: string;
  position: CartesianCoord;
  velocity: { vx: number; vy: number; vz: number };  // km/s
  mass_kg: number;
  orbital_radius_m: number;
  central_mass_kg: number;
}

export type SolverMode = 'GEOMETRIC' | 'KINEMATIC';

// =============================================================================
// GEOMETRIC SOLVER (FOR LIGHT)
// =============================================================================
//
// This solver handles ALL photon-related calculations:
// - DESI redshift-to-distance conversions
// - Quasar light paths
// - CMB geometry
// - Gravitational lensing paths
//
// CRITICAL: This solver uses ONLY the macroscopic boundary geometry.
// NO velocity modifications. NO MOND corrections.
// =============================================================================

export class GeometricSolver {
  /**
   * Convert spherical (RA, Dec, distance) to Z² Cartesian coordinates
   * Uses standard cosmological coordinate transformation
   * NO MOND corrections applied - pure geometry
   */
  static sphericalToCartesian(coord: SphericalCoord): CartesianCoord {
    const ra_rad = (coord.ra * Math.PI) / 180;
    const dec_rad = (coord.dec * Math.PI) / 180;

    // Standard spherical to Cartesian (cosmological convention)
    return {
      x: coord.d * Math.cos(dec_rad) * Math.cos(ra_rad),
      y: coord.d * Math.cos(dec_rad) * Math.sin(ra_rad),
      z: coord.d * Math.sin(dec_rad),
    };
  }

  /**
   * Convert Cartesian to spherical coordinates
   */
  static cartesianToSpherical(coord: CartesianCoord): SphericalCoord {
    const d = Math.sqrt(coord.x ** 2 + coord.y ** 2 + coord.z ** 2);
    const dec = Math.asin(coord.z / d) * (180 / Math.PI);
    const ra = Math.atan2(coord.y, coord.x) * (180 / Math.PI);

    return { ra: ra < 0 ? ra + 360 : ra, dec, d };
  }

  /**
   * Redshift to comoving distance using Z² cosmology
   * Pure geometric calculation - no kinematic corrections
   */
  static redshiftToDistance(z: number): number {
    // Hubble distance in Mpc
    const D_H = Z2_CONSTANTS.C_KM_S / Z2_CONSTANTS.H0_KM_S_MPC;

    // For Z² cosmology with Ω_m = 6/19
    const Om = Z2_CONSTANTS.OMEGA_M;
    const Ode = 1 - Om;  // Dark energy density

    // Numerical integration of comoving distance
    // d_c = D_H * integral(0 to z) dz' / E(z')
    // E(z) = sqrt(Ω_m(1+z)³ + Ω_de)

    const steps = 1000;
    const dz = z / steps;
    let integral = 0;

    for (let i = 0; i < steps; i++) {
      const z_mid = (i + 0.5) * dz;
      const E_z = Math.sqrt(Om * Math.pow(1 + z_mid, 3) + Ode);
      integral += dz / E_z;
    }

    return D_H * integral;  // Mpc
  }

  /**
   * Distance to redshift (inverse of above)
   */
  static distanceToRedshift(d_mpc: number): number {
    // Binary search for redshift
    let z_low = 0;
    let z_high = 10;

    for (let i = 0; i < 50; i++) {
      const z_mid = (z_low + z_high) / 2;
      const d_test = this.redshiftToDistance(z_mid);

      if (d_test < d_mpc) {
        z_low = z_mid;
      } else {
        z_high = z_mid;
      }
    }

    return (z_low + z_high) / 2;
  }

  /**
   * Apply T³/Z₂ periodic boundary wrapping
   * Light paths wrap around the fundamental domain
   */
  static wrapCoordinate(coord: CartesianCoord): CartesianCoord {
    const half = DERIVED.HALF_BOX_MPC;

    const wrap = (v: number) => {
      let wrapped = v;
      while (wrapped > half) wrapped -= Z2_CONSTANTS.L_C_MPC;
      while (wrapped < -half) wrapped += Z2_CONSTANTS.L_C_MPC;
      return wrapped;
    };

    return {
      x: wrap(coord.x),
      y: wrap(coord.y),
      z: wrap(coord.z),
    };
  }

  /**
   * Calculate ghost image positions for an object
   * Objects near boundaries have "ghosts" on opposite sides
   */
  static getGhostImages(coord: CartesianCoord, threshold_mpc: number = 1000): CartesianCoord[] {
    const ghosts: CartesianCoord[] = [];
    const L = Z2_CONSTANTS.L_C_MPC;
    const half = DERIVED.HALF_BOX_MPC;

    // Check each axis
    const offsets = [-L, 0, L];

    for (const dx of offsets) {
      for (const dy of offsets) {
        for (const dz of offsets) {
          if (dx === 0 && dy === 0 && dz === 0) continue;

          const ghost = {
            x: coord.x + dx,
            y: coord.y + dy,
            z: coord.z + dz,
          };

          // Only include if within fundamental domain + threshold
          if (
            Math.abs(ghost.x) < half + threshold_mpc &&
            Math.abs(ghost.y) < half + threshold_mpc &&
            Math.abs(ghost.z) < half + threshold_mpc
          ) {
            ghosts.push(ghost);
          }
        }
      }
    }

    return ghosts;
  }

  /**
   * Calculate gravitational lensing deflection angle
   * Pure geometric calculation using GR
   */
  static lensingDeflection(
    mass_solar: number,
    impact_parameter_mpc: number
  ): number {
    // Einstein radius calculation
    // θ_E = 4GM / (c² * b)
    const M_kg = mass_solar * 1.989e30;  // Solar mass to kg
    const b_m = impact_parameter_mpc * 3.086e22;  // Mpc to meters

    const theta_rad = (4 * Z2_CONSTANTS.G_SI * M_kg) /
                      (Z2_CONSTANTS.C_M_S ** 2 * b_m);

    return theta_rad * (180 / Math.PI) * 3600;  // arcseconds
  }
}

// =============================================================================
// KINEMATIC SOLVER (FOR MATTER)
// =============================================================================
//
// This solver handles ALL matter dynamics:
// - Galaxy rotation curves
// - Binary star orbits
// - Cluster dynamics
// - Void outflows
//
// CRITICAL: This solver applies topological MOND corrections
// when local acceleration drops below a_topo = c²/L_c
// =============================================================================

export class KinematicSolver {
  /**
   * Check if we're in the deep topological regime
   * Returns true if acceleration is below a_topo
   */
  static isInTopologicalRegime(acceleration_m_s2: number): boolean {
    return acceleration_m_s2 < Z2_CONSTANTS.A_TOPO_M_S2;
  }

  /**
   * Calculate Newtonian gravitational acceleration
   */
  static newtonianAcceleration(
    mass_kg: number,
    radius_m: number
  ): number {
    return (Z2_CONSTANTS.G_SI * mass_kg) / (radius_m ** 2);
  }

  /**
   * Calculate orbital velocity with topological MOND correction
   * Transitions from Newtonian to MOND when a < a_topo
   */
  static orbitalVelocity(
    central_mass_kg: number,
    orbital_radius_m: number
  ): number {
    const a_newton = this.newtonianAcceleration(central_mass_kg, orbital_radius_m);

    if (!this.isInTopologicalRegime(a_newton)) {
      // Standard Newtonian regime
      // v = sqrt(GM/r)
      return Math.sqrt((Z2_CONSTANTS.G_SI * central_mass_kg) / orbital_radius_m);
    }

    // Deep topological limit (MOND regime)
    // v⁴ = G * M * a_topo
    // v = (G * M * a_topo)^(1/4)
    const v4 = Z2_CONSTANTS.G_SI * central_mass_kg * Z2_CONSTANTS.A_TOPO_M_S2;
    return Math.pow(v4, 0.25);
  }

  /**
   * Calculate rotation curve for a galaxy
   * Returns array of [radius_kpc, velocity_km_s] pairs
   */
  static rotationCurve(
    baryonic_mass_solar: number,
    radii_kpc: number[]
  ): Array<[number, number]> {
    const M_kg = baryonic_mass_solar * 1.989e30;
    const curve: Array<[number, number]> = [];

    for (const r_kpc of radii_kpc) {
      const r_m = r_kpc * 3.086e19;  // kpc to meters
      const v_m_s = this.orbitalVelocity(M_kg, r_m);
      const v_km_s = v_m_s / 1000;
      curve.push([r_kpc, v_km_s]);
    }

    return curve;
  }

  /**
   * SPARC-style rotation curve fit
   * Uses topological MOND for outer regions
   */
  static sparcRotationCurve(
    disk_mass_solar: number,
    scale_length_kpc: number,
    bulge_mass_solar: number,
    radii_kpc: number[]
  ): Array<{ r: number; v_obs: number; v_newton: number; v_topo: number }> {
    const results: Array<{ r: number; v_obs: number; v_newton: number; v_topo: number }> = [];

    for (const r_kpc of radii_kpc) {
      const r_m = r_kpc * 3.086e19;

      // Enclosed mass from exponential disk + bulge
      // Simplified: assume exponential profile
      const x = r_kpc / scale_length_kpc;
      const enclosed_disk = disk_mass_solar * (1 - (1 + x) * Math.exp(-x));
      const enclosed_bulge = bulge_mass_solar * Math.pow(r_kpc / (r_kpc + 0.5), 3);
      const total_enclosed = (enclosed_disk + enclosed_bulge) * 1.989e30;

      // Newtonian prediction
      const v_newton = Math.sqrt((Z2_CONSTANTS.G_SI * total_enclosed) / r_m) / 1000;

      // Topological (MOND) prediction
      const v_topo = this.orbitalVelocity(total_enclosed, r_m) / 1000;

      // Observed = topological in outer regions, Newtonian in inner
      const a_newton = this.newtonianAcceleration(total_enclosed, r_m);
      const transition = 1 / (1 + Math.pow(a_newton / Z2_CONSTANTS.A_TOPO_M_S2, 2));
      const v_obs = v_newton * (1 - transition) + v_topo * transition;

      results.push({ r: r_kpc, v_obs, v_newton, v_topo });
    }

    return results;
  }

  /**
   * Calculate wide binary relative velocity
   * For Gaia binaries at large separations
   */
  static wideBinaryVelocity(
    total_mass_solar: number,
    separation_au: number
  ): number {
    const M_kg = total_mass_solar * 1.989e30;
    const r_m = separation_au * 1.496e11;  // AU to meters

    // Relative orbital velocity
    return this.orbitalVelocity(M_kg, r_m) / 1000;  // km/s
  }

  /**
   * Calculate void outflow velocity (kSZ effect)
   * Matter is pushed out of voids by topological boundary repulsion
   */
  static voidOutflowVelocity(
    void_radius_mpc: number,
    position_in_void_mpc: number
  ): number {
    // The outflow is driven by the boundary condition
    // v ~ a_topo * t_age * (r/R_void)
    // Simplified: v_max ≈ 265 km/s at void edge (from kSZ measurements)

    const fractional_radius = position_in_void_mpc / void_radius_mpc;
    const v_max_km_s = 265;  // Observed kSZ void outflow

    return v_max_km_s * fractional_radius;
  }
}

// =============================================================================
// SOLAR SYSTEM SOLVER (KEPLERIAN BYPASS)
// =============================================================================
//
// HARDCODED EXCEPTION: The Solar System operates in the high-acceleration
// regime where a >> a_topo. Standard Keplerian dynamics apply.
// This solver bypasses all MOND corrections.
// =============================================================================

export class SolarSystemSolver {
  static readonly SOLAR_MASS_KG = 1.989e30;
  static readonly AU_TO_M = 1.496e11;

  // Verify that Solar System is safely Newtonian
  static readonly EARTH_ORBITAL_RADIUS_M = 1.496e11;
  static readonly EARTH_ORBITAL_ACCELERATION =
    (6.67430e-11 * 1.989e30) / (1.496e11 ** 2);  // ≈ 5.93e-3 m/s²

  // This is ~4e7 times larger than a_topo, confirming Newtonian regime
  static readonly ACCELERATION_RATIO =
    SolarSystemSolver.EARTH_ORBITAL_ACCELERATION / Z2_CONSTANTS.A_TOPO_M_S2;

  /**
   * Pure Keplerian orbital velocity
   * NO MOND corrections - high acceleration regime
   */
  static keplerianVelocity(
    central_mass_kg: number,
    orbital_radius_m: number
  ): number {
    // v = sqrt(GM/r) - exact Kepler
    return Math.sqrt((Z2_CONSTANTS.G_SI * central_mass_kg) / orbital_radius_m);
  }

  /**
   * Keplerian orbital period
   */
  static orbitalPeriod(
    orbital_radius_m: number,
    central_mass_kg: number = SolarSystemSolver.SOLAR_MASS_KG
  ): number {
    // T = 2π * sqrt(r³/GM)
    return 2 * Math.PI * Math.sqrt(
      Math.pow(orbital_radius_m, 3) / (Z2_CONSTANTS.G_SI * central_mass_kg)
    );
  }

  /**
   * Planet position at time t (simplified circular orbit)
   */
  static planetPosition(
    orbital_radius_au: number,
    period_days: number,
    time_days: number,
    initial_angle_rad: number = 0
  ): { x: number; y: number; z: number } {
    const angle = initial_angle_rad + (2 * Math.PI * time_days) / period_days;
    const r = orbital_radius_au;

    return {
      x: r * Math.cos(angle),
      y: r * Math.sin(angle),
      z: 0,  // Simplified: assume ecliptic plane
    };
  }

  /**
   * Full planetary ephemeris (position and velocity)
   */
  static planetEphemeris(
    orbital_radius_au: number,
    period_days: number,
    time_days: number
  ): { position: CartesianCoord; velocity: { vx: number; vy: number; vz: number } } {
    const pos = this.planetPosition(orbital_radius_au, period_days, time_days);

    // Orbital velocity (perpendicular to radius)
    const r_m = orbital_radius_au * this.AU_TO_M;
    const v_m_s = this.keplerianVelocity(this.SOLAR_MASS_KG, r_m);
    const v_km_s = v_m_s / 1000;

    const angle = (2 * Math.PI * time_days) / period_days;

    return {
      position: pos,
      velocity: {
        vx: -v_km_s * Math.sin(angle),
        vy: v_km_s * Math.cos(angle),
        vz: 0,
      },
    };
  }
}

// =============================================================================
// UNIFIED TRANSFORMER (ROUTER)
// =============================================================================
//
// Routes calculations to the appropriate solver based on context
// =============================================================================

export class Z2Transformer {
  /**
   * Automatically select solver based on object type and scale
   */
  static getSolverMode(obj: CelestialObject): SolverMode {
    switch (obj.type) {
      case 'quasar':
      case 'cmb':
        // Always geometric - these are photon observations
        return 'GEOMETRIC';

      case 'galaxy':
      case 'cluster':
        // Kinematic for dynamics, geometric for positioning
        return 'KINEMATIC';

      case 'void':
        // Kinematic for outflow calculations
        return 'KINEMATIC';

      case 'star':
      case 'planet':
        // Solar System bypass - but still "kinematic" category
        return 'KINEMATIC';

      default:
        return 'GEOMETRIC';
    }
  }

  /**
   * Transform raw observational coordinates to Z² Cartesian
   */
  static toCartesian(
    ra: number,
    dec: number,
    redshift?: number,
    distance_mpc?: number
  ): CartesianCoord {
    const d = distance_mpc ??
              (redshift ? GeometricSolver.redshiftToDistance(redshift) : 0);

    return GeometricSolver.sphericalToCartesian({ ra, dec, d });
  }

  /**
   * Check if an object is in the MOND regime
   */
  static inMondRegime(
    mass_kg: number,
    radius_m: number
  ): boolean {
    const a = KinematicSolver.newtonianAcceleration(mass_kg, radius_m);
    return KinematicSolver.isInTopologicalRegime(a);
  }

  /**
   * Get appropriate velocity calculation
   */
  static getOrbitalVelocity(
    central_mass_kg: number,
    orbital_radius_m: number,
    isSolarSystem: boolean = false
  ): number {
    if (isSolarSystem) {
      return SolarSystemSolver.keplerianVelocity(central_mass_kg, orbital_radius_m);
    }
    return KinematicSolver.orbitalVelocity(central_mass_kg, orbital_radius_m);
  }
}

// =============================================================================
// EXPORT DEFAULT INSTANCE
// =============================================================================

export default Z2Transformer;
