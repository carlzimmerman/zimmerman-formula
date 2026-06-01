/**
 * =============================================================================
 * CosmicConstants.ts - UNIVERSAL METRIC SYSTEM
 * =============================================================================
 *
 * The canonical unit for all CPU-side calculations is KILOMETERS (km).
 * JavaScript's Number type (Float64) can safely represent up to 9×10^15
 * exactly, and handles 10^23 with sufficient precision for cosmic scales.
 *
 * Z² Framework v11.1.0
 * Work-Order HHH: Float64 Camera-Relative Engine
 * =============================================================================
 */

// =============================================================================
// FUNDAMENTAL DISTANCE CONVERSIONS (all to km)
// =============================================================================

export const KM = 1;
export const M = 1e-3;                          // 1 meter in km
export const AU = 1.495978707e8;                // 1 AU in km
export const LY = 9.4607304725808e12;           // 1 light-year in km
export const PC = 3.0856775814913673e13;        // 1 parsec in km
export const KPC = 3.0856775814913673e16;       // 1 kiloparsec in km
export const MPC = 3.0856775814913673e19;       // 1 megaparsec in km
export const GPC = 3.0856775814913673e22;       // 1 gigaparsec in km

// =============================================================================
// Z² FRAMEWORK LOCKED PARAMETERS
// =============================================================================

export const Z2 = {
  // Fundamental domain size
  L_C_GPC: 20.6,
  L_C_KM: 20.6 * GPC,                           // 6.356×10^23 km
  HALF_BOX_KM: 10.3 * GPC,                      // 3.178×10^23 km

  // Matter density
  OMEGA_M: 6 / 19,                              // 0.315789...

  // Hubble constant
  H0: 67.4,                                     // km/s/Mpc

  // Speed of light
  C_KM_S: 299792.458,                           // km/s

  // Topological MOND acceleration
  A_TOPO: (299792.458 ** 2) / (20.6 * GPC),     // c²/L_c in km/s²
} as const;

// =============================================================================
// SOLAR SYSTEM DATA (distances in km)
// =============================================================================

export const SUN = {
  name: 'Sun',
  radius_km: 696340,
  mass_kg: 1.989e30,
  position_km: [0, 0, 0] as [number, number, number],
  type: 'star' as const,
};

export const PLANETS = [
  { name: 'Mercury', orbit_km: 0.387 * AU, radius_km: 2439.7, period_days: 87.97, color: '#8c7853' },
  { name: 'Venus', orbit_km: 0.723 * AU, radius_km: 6051.8, period_days: 224.7, color: '#ffd700' },
  { name: 'Earth', orbit_km: 1.0 * AU, radius_km: 6371.0, period_days: 365.25, color: '#4169e1' },
  { name: 'Mars', orbit_km: 1.524 * AU, radius_km: 3389.5, period_days: 687.0, color: '#cd5c5c' },
  { name: 'Jupiter', orbit_km: 5.203 * AU, radius_km: 69911, period_days: 4333, color: '#deb887' },
  { name: 'Saturn', orbit_km: 9.537 * AU, radius_km: 58232, period_days: 10759, color: '#f4a460' },
  { name: 'Uranus', orbit_km: 19.19 * AU, radius_km: 25362, period_days: 30687, color: '#afeeee' },
  { name: 'Neptune', orbit_km: 30.07 * AU, radius_km: 24622, period_days: 60190, color: '#4169e1' },
  { name: 'Pluto', orbit_km: 39.48 * AU, radius_km: 1188.3, period_days: 90560, color: '#dcdcdc' },
] as const;

// =============================================================================
// MILKY WAY DATA (distances in km)
// =============================================================================

export const MILKY_WAY = {
  name: 'Milky Way',
  radius_km: 26.8 * KPC,                        // 26.8 kpc radius
  bulge_radius_km: 3 * KPC,
  disk_height_km: 0.3 * KPC,
  sun_distance_from_center_km: 8 * KPC,         // Sun is 8 kpc from galactic center
  position_km: [0, 0, 0] as [number, number, number], // MW center at origin
  type: 'galaxy' as const,
};

// =============================================================================
// LOCAL GROUP DATA (distances in km from Milky Way center)
// =============================================================================

export const LOCAL_GROUP = [
  { name: 'LMC', distance_km: 0.05 * MPC, ra: 80.89, dec: -69.76, type: 'galaxy' as const },
  { name: 'SMC', distance_km: 0.061 * MPC, ra: 13.19, dec: -72.83, type: 'galaxy' as const },
  { name: 'Andromeda (M31)', distance_km: 0.778 * MPC, ra: 10.68, dec: 41.27, type: 'galaxy' as const },
  { name: 'Triangulum (M33)', distance_km: 0.84 * MPC, ra: 23.46, dec: 30.66, type: 'galaxy' as const },
  { name: 'NGC 6822', distance_km: 0.50 * MPC, ra: 296.24, dec: -14.80, type: 'galaxy' as const },
] as const;

// =============================================================================
// Z² TOPOLOGICAL VERTICES (distances in km from origin)
// =============================================================================

export const Z2_VERTICES = [
  {
    id: 'V1',
    name: 'Shapley Supercluster',
    position_km: [8.5 * GPC, 4.0 * GPC, 5.0 * GPC] as [number, number, number],
    color: '#FFD700',
    type: 'z2_vertex' as const,
  },
  {
    id: 'V2',
    name: 'Anti-Shapley',
    position_km: [-7.0 * GPC, -3.0 * GPC, -5.0 * GPC] as [number, number, number],
    color: '#00FFFF',
    type: 'z2_vertex' as const,
  },
  {
    id: 'V3',
    name: 'CMB Cold Spot',
    position_km: [-2.0 * GPC, 6.0 * GPC, 7.0 * GPC] as [number, number, number],
    color: '#FF00FF',
    type: 'z2_vertex' as const,
  },
  {
    id: 'V4',
    name: 'Southern Vertex',
    position_km: [1.0 * GPC, -5.0 * GPC, -8.0 * GPC] as [number, number, number],
    color: '#00FF00',
    type: 'z2_vertex' as const,
  },
] as const;

// =============================================================================
// MAJOR COSMIC STRUCTURES (distances in km)
// =============================================================================

export const MAJOR_STRUCTURES = [
  { name: 'Virgo Cluster', distance_km: 16.5 * MPC, ra: 187.70, dec: 12.34, radius_km: 2.2 * MPC, type: 'cluster' as const },
  { name: 'Coma Cluster', distance_km: 100 * MPC, ra: 194.95, dec: 27.98, radius_km: 6 * MPC, type: 'cluster' as const },
  { name: 'Shapley Supercluster', distance_km: 200 * MPC, ra: 202.5, dec: -31.5, radius_km: 40 * MPC, type: 'supercluster' as const },
  { name: 'Laniakea', distance_km: 80 * MPC, ra: 157, dec: -46, radius_km: 160 * MPC, type: 'supercluster' as const },
  { name: 'Boötes Void', distance_km: 213 * MPC, ra: 218, dec: 46, radius_km: 100 * MPC, type: 'void' as const },
] as const;

// =============================================================================
// LOD SCALE THRESHOLDS (camera distance in km)
// =============================================================================

export const LOD_THRESHOLDS = {
  // Show individual planets when camera is within 100 AU
  PLANETARY: {
    maxDistance_km: 100 * AU,                   // ~1.5×10^10 km
    sceneScale_km: AU,                          // 1 scene unit = 1 AU
    nearPlane: 0.0001,
    farPlane: 200,
  },

  // Show stars/stellar neighborhood: 100 AU - 1000 ly
  STELLAR: {
    maxDistance_km: 1000 * LY,                  // ~9.5×10^15 km
    sceneScale_km: LY,                          // 1 scene unit = 1 ly
    nearPlane: 0.001,
    farPlane: 2000,
  },

  // Show Milky Way structure: 1000 ly - 1 Mpc
  GALACTIC: {
    maxDistance_km: 1 * MPC,                    // ~3.1×10^19 km
    sceneScale_km: KPC,                         // 1 scene unit = 1 kpc
    nearPlane: 0.01,
    farPlane: 100,
  },

  // Show galaxy clusters: 1 Mpc - 100 Mpc
  CLUSTER: {
    maxDistance_km: 100 * MPC,                  // ~3.1×10^21 km
    sceneScale_km: MPC,                         // 1 scene unit = 1 Mpc
    nearPlane: 0.01,
    farPlane: 200,
  },

  // Show cosmic web / full domain: 100 Mpc - 20.6 Gpc
  COSMIC: {
    maxDistance_km: Z2.L_C_KM,                  // ~6.4×10^23 km
    sceneScale_km: GPC,                         // 1 scene unit = 1 Gpc
    nearPlane: 0.01,
    farPlane: 50,
  },
} as const;

export type LODLevel = keyof typeof LOD_THRESHOLDS;

// =============================================================================
// UTILITY: Get LOD level for camera distance
// =============================================================================

export function getLODLevel(cameraDistance_km: number): LODLevel {
  if (cameraDistance_km < LOD_THRESHOLDS.PLANETARY.maxDistance_km) return 'PLANETARY';
  if (cameraDistance_km < LOD_THRESHOLDS.STELLAR.maxDistance_km) return 'STELLAR';
  if (cameraDistance_km < LOD_THRESHOLDS.GALACTIC.maxDistance_km) return 'GALACTIC';
  if (cameraDistance_km < LOD_THRESHOLDS.CLUSTER.maxDistance_km) return 'CLUSTER';
  return 'COSMIC';
}

// =============================================================================
// UTILITY: Convert celestial coordinates to Cartesian km
// =============================================================================

export function celestialToCartesian(
  ra_deg: number,
  dec_deg: number,
  distance_km: number
): [number, number, number] {
  const ra_rad = (ra_deg * Math.PI) / 180;
  const dec_rad = (dec_deg * Math.PI) / 180;

  return [
    distance_km * Math.cos(dec_rad) * Math.cos(ra_rad),
    distance_km * Math.cos(dec_rad) * Math.sin(ra_rad),
    distance_km * Math.sin(dec_rad),
  ];
}

// =============================================================================
// UTILITY: Format distance for display
// =============================================================================

export function formatDistance(distance_km: number): string {
  if (distance_km < 1e6) {
    return `${(distance_km).toLocaleString()} km`;
  }
  if (distance_km < AU * 0.1) {
    return `${(distance_km / 1e6).toFixed(2)} million km`;
  }
  if (distance_km < 1000 * AU) {
    return `${(distance_km / AU).toFixed(2)} AU`;
  }
  if (distance_km < 1000 * LY) {
    return `${(distance_km / LY).toFixed(1)} ly`;
  }
  if (distance_km < 1000 * KPC) {
    return `${(distance_km / KPC).toFixed(2)} kpc`;
  }
  if (distance_km < 1000 * MPC) {
    return `${(distance_km / MPC).toFixed(2)} Mpc`;
  }
  return `${(distance_km / GPC).toFixed(2)} Gpc`;
}
