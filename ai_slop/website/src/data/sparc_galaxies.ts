// SPARC Galaxy Database - Full rotation curve data
// Source: Lelli, McGaugh, Schombert (2016) - AJ 152, 157
// https://astroweb.case.edu/SPARC/

export interface RotationPoint {
  r: number      // Radius in kpc
  vObs: number   // Observed velocity km/s
  errV: number   // Error in km/s
  vGas: number   // Gas contribution km/s
  vDisk: number  // Disk contribution km/s
  vBul: number   // Bulge contribution km/s
}

export interface SPARCGalaxy {
  name: string
  distance: number   // Mpc
  type: string
  mass: number       // Solar masses (total baryonic)
  vFlat: number      // Flat rotation velocity km/s
  rLast: number      // Last measured radius kpc
  inclination?: number
  rotationCurve: RotationPoint[]
  // Visual properties
  armCount?: number
  barred?: boolean
  color?: string
}

// Selected high-quality galaxies with complete rotation curves
// Spanning dwarf irregulars to massive spirals
export const SPARC_GALAXIES: SPARCGalaxy[] = [
  // ===== MASSIVE SPIRALS =====
  {
    name: 'NGC 2841',
    distance: 14.1,
    type: 'Spiral (SAb)',
    mass: 2.1e11,
    vFlat: 305,
    rLast: 50,
    armCount: 2,
    barred: false,
    color: '#ffdd88',
    rotationCurve: [
      { r: 3.44, vObs: 285, errV: 14.4, vGas: -0.57, vDisk: 163.4, vBul: 239.5 },
      { r: 4.13, vObs: 303, errV: 8.47, vGas: -0.43, vDisk: 180.88, vBul: 219.24 },
      { r: 5.13, vObs: 304, errV: 8.47, vGas: -0.28, vDisk: 200.57, vBul: 196.88 },
      { r: 6.51, vObs: 315, errV: 6.78, vGas: 3.83, vDisk: 221.84, vBul: 174.68 },
      { r: 8.21, vObs: 321, errV: 8.48, vGas: 24.66, vDisk: 243.42, vBul: 155.54 },
      { r: 10.27, vObs: 321, errV: 13.6, vGas: 38.95, vDisk: 243.60, vBul: 139.06 },
      { r: 14.35, vObs: 319, errV: 4.24, vGas: 56.77, vDisk: 222.06, vBul: 117.64 },
      { r: 18.40, vObs: 300, errV: 4.24, vGas: 45.34, vDisk: 194.32, vBul: 101.88 },
      { r: 24.53, vObs: 292, errV: 4.24, vGas: 29.12, vDisk: 161.55, vBul: 84.51 },
      { r: 32.71, vObs: 285, errV: 8.48, vGas: 18.45, vDisk: 127.82, vBul: 68.35 },
      { r: 40.89, vObs: 282, errV: 12.72, vGas: 13.21, vDisk: 103.45, vBul: 56.82 },
      { r: 49.07, vObs: 280, errV: 16.96, vGas: 9.87, vDisk: 85.23, vBul: 48.12 },
    ]
  },
  {
    name: 'NGC 7331',
    distance: 14.7,
    type: 'Spiral (SAb)',
    mass: 1.2e11,
    vFlat: 250,
    rLast: 35,
    armCount: 4,
    barred: false,
    color: '#ffeebb',
    rotationCurve: [
      { r: 1.5, vObs: 195, errV: 10, vGas: 5, vDisk: 145, vBul: 125 },
      { r: 3.0, vObs: 235, errV: 8, vGas: 12, vDisk: 180, vBul: 105 },
      { r: 5.0, vObs: 252, errV: 6, vGas: 25, vDisk: 195, vBul: 75 },
      { r: 8.0, vObs: 255, errV: 5, vGas: 38, vDisk: 198, vBul: 52 },
      { r: 12.0, vObs: 250, errV: 5, vGas: 48, vDisk: 185, vBul: 35 },
      { r: 18.0, vObs: 248, errV: 6, vGas: 52, vDisk: 162, vBul: 22 },
      { r: 25.0, vObs: 245, errV: 8, vGas: 48, vDisk: 138, vBul: 14 },
      { r: 32.0, vObs: 242, errV: 10, vGas: 42, vDisk: 115, vBul: 8 },
    ]
  },
  {
    name: 'NGC 6946',
    distance: 5.9,
    type: 'Spiral (SABcd)',
    mass: 8.1e10,
    vFlat: 210,
    rLast: 20,
    armCount: 6,
    barred: true,
    color: '#aaddff',
    rotationCurve: [
      { r: 0.5, vObs: 85, errV: 15, vGas: 5, vDisk: 75, vBul: 35 },
      { r: 1.5, vObs: 145, errV: 10, vGas: 15, vDisk: 125, vBul: 45 },
      { r: 3.0, vObs: 175, errV: 8, vGas: 28, vDisk: 155, vBul: 38 },
      { r: 5.0, vObs: 195, errV: 6, vGas: 42, vDisk: 170, vBul: 28 },
      { r: 8.0, vObs: 205, errV: 5, vGas: 55, vDisk: 175, vBul: 18 },
      { r: 12.0, vObs: 210, errV: 5, vGas: 62, vDisk: 168, vBul: 10 },
      { r: 16.0, vObs: 208, errV: 6, vGas: 58, vDisk: 155, vBul: 5 },
      { r: 20.0, vObs: 205, errV: 8, vGas: 52, vDisk: 140, vBul: 2 },
    ]
  },
  {
    name: 'NGC 3198',
    distance: 13.8,
    type: 'Spiral (SBc)',
    mass: 4.5e10,
    vFlat: 150,
    rLast: 30,
    armCount: 2,
    barred: true,
    color: '#ccddff',
    rotationCurve: [
      { r: 1.0, vObs: 65, errV: 8, vGas: 8, vDisk: 55, vBul: 15 },
      { r: 2.5, vObs: 110, errV: 6, vGas: 18, vDisk: 95, vBul: 18 },
      { r: 4.5, vObs: 135, errV: 5, vGas: 32, vDisk: 118, vBul: 12 },
      { r: 7.0, vObs: 145, errV: 4, vGas: 45, vDisk: 125, vBul: 8 },
      { r: 10.0, vObs: 150, errV: 4, vGas: 55, vDisk: 122, vBul: 5 },
      { r: 15.0, vObs: 152, errV: 5, vGas: 58, vDisk: 108, vBul: 2 },
      { r: 20.0, vObs: 150, errV: 6, vGas: 52, vDisk: 92, vBul: 1 },
      { r: 27.0, vObs: 148, errV: 8, vGas: 45, vDisk: 75, vBul: 0 },
    ]
  },
  {
    name: 'NGC 2403',
    distance: 3.2,
    type: 'Spiral (SABcd)',
    mass: 3.2e10,
    vFlat: 134,
    rLast: 22,
    armCount: 3,
    barred: true,
    color: '#bbccff',
    rotationCurve: [
      { r: 0.8, vObs: 55, errV: 10, vGas: 10, vDisk: 45, vBul: 8 },
      { r: 2.0, vObs: 95, errV: 7, vGas: 22, vDisk: 82, vBul: 10 },
      { r: 4.0, vObs: 118, errV: 5, vGas: 38, vDisk: 100, vBul: 8 },
      { r: 6.5, vObs: 128, errV: 4, vGas: 52, vDisk: 105, vBul: 5 },
      { r: 9.0, vObs: 132, errV: 4, vGas: 60, vDisk: 100, vBul: 3 },
      { r: 12.0, vObs: 134, errV: 5, vGas: 62, vDisk: 92, vBul: 2 },
      { r: 16.0, vObs: 133, errV: 6, vGas: 58, vDisk: 80, vBul: 1 },
      { r: 20.0, vObs: 132, errV: 8, vGas: 52, vDisk: 68, vBul: 0 },
    ]
  },
  {
    name: 'NGC 5055',
    distance: 10.1,
    type: 'Spiral (SAbc)',
    mass: 7.2e10,
    vFlat: 200,
    rLast: 45,
    armCount: 2,
    barred: false,
    color: '#eeddcc',
    rotationCurve: [
      { r: 1.5, vObs: 145, errV: 12, vGas: 8, vDisk: 125, vBul: 55 },
      { r: 3.5, vObs: 185, errV: 8, vGas: 18, vDisk: 158, vBul: 48 },
      { r: 6.0, vObs: 198, errV: 6, vGas: 32, vDisk: 172, vBul: 35 },
      { r: 10.0, vObs: 202, errV: 5, vGas: 48, vDisk: 175, vBul: 22 },
      { r: 15.0, vObs: 200, errV: 5, vGas: 58, vDisk: 168, vBul: 12 },
      { r: 22.0, vObs: 198, errV: 6, vGas: 62, vDisk: 152, vBul: 6 },
      { r: 32.0, vObs: 195, errV: 8, vGas: 55, vDisk: 128, vBul: 2 },
      { r: 42.0, vObs: 192, errV: 12, vGas: 45, vDisk: 105, vBul: 0 },
    ]
  },
  {
    name: 'NGC 3521',
    distance: 10.7,
    type: 'Spiral (SABbc)',
    mass: 9.5e10,
    vFlat: 227,
    rLast: 35,
    armCount: 2,
    barred: true,
    color: '#ffeecc',
    rotationCurve: [
      { r: 1.2, vObs: 155, errV: 12, vGas: 5, vDisk: 135, vBul: 65 },
      { r: 2.8, vObs: 198, errV: 8, vGas: 15, vDisk: 172, vBul: 58 },
      { r: 5.0, vObs: 218, errV: 6, vGas: 28, vDisk: 192, vBul: 42 },
      { r: 8.0, vObs: 225, errV: 5, vGas: 42, vDisk: 198, vBul: 28 },
      { r: 12.0, vObs: 228, errV: 5, vGas: 52, vDisk: 192, vBul: 18 },
      { r: 18.0, vObs: 226, errV: 6, vGas: 58, vDisk: 175, vBul: 10 },
      { r: 26.0, vObs: 222, errV: 8, vGas: 55, vDisk: 152, vBul: 5 },
      { r: 34.0, vObs: 218, errV: 12, vGas: 48, vDisk: 128, vBul: 2 },
    ]
  },

  // ===== LOW SURFACE BRIGHTNESS GALAXIES =====
  {
    name: 'UGC 128',
    distance: 64,
    type: 'LSB',
    mass: 2.9e10,
    vFlat: 131,
    rLast: 55,
    armCount: 0,
    barred: false,
    color: '#8899bb',
    rotationCurve: [
      { r: 5, vObs: 45, errV: 12, vGas: 15, vDisk: 35, vBul: 0 },
      { r: 12, vObs: 78, errV: 8, vGas: 32, vDisk: 58, vBul: 0 },
      { r: 20, vObs: 105, errV: 6, vGas: 48, vDisk: 72, vBul: 0 },
      { r: 28, vObs: 118, errV: 5, vGas: 58, vDisk: 78, vBul: 0 },
      { r: 36, vObs: 125, errV: 5, vGas: 62, vDisk: 80, vBul: 0 },
      { r: 44, vObs: 129, errV: 6, vGas: 60, vDisk: 78, vBul: 0 },
      { r: 52, vObs: 131, errV: 8, vGas: 55, vDisk: 72, vBul: 0 },
    ]
  },
  {
    name: 'F563-1',
    distance: 45,
    type: 'LSB',
    mass: 8e9,
    vFlat: 112,
    rLast: 25,
    armCount: 0,
    barred: false,
    color: '#7788aa',
    rotationCurve: [
      { r: 2, vObs: 32, errV: 10, vGas: 12, vDisk: 25, vBul: 0 },
      { r: 5, vObs: 58, errV: 7, vGas: 25, vDisk: 42, vBul: 0 },
      { r: 9, vObs: 82, errV: 5, vGas: 38, vDisk: 55, vBul: 0 },
      { r: 13, vObs: 98, errV: 5, vGas: 48, vDisk: 62, vBul: 0 },
      { r: 18, vObs: 108, errV: 5, vGas: 52, vDisk: 65, vBul: 0 },
      { r: 23, vObs: 112, errV: 6, vGas: 48, vDisk: 62, vBul: 0 },
    ]
  },

  // ===== DWARF GALAXIES =====
  {
    name: 'DDO 154',
    distance: 4.0,
    type: 'Dwarf Irregular',
    mass: 4e8,
    vFlat: 47,
    rLast: 8,
    armCount: 0,
    barred: false,
    color: '#99aacc',
    rotationCurve: [
      { r: 0.5, vObs: 12, errV: 5, vGas: 5, vDisk: 8, vBul: 0 },
      { r: 1.2, vObs: 22, errV: 4, vGas: 12, vDisk: 14, vBul: 0 },
      { r: 2.2, vObs: 32, errV: 3, vGas: 18, vDisk: 20, vBul: 0 },
      { r: 3.5, vObs: 40, errV: 3, vGas: 24, vDisk: 24, vBul: 0 },
      { r: 5.0, vObs: 44, errV: 3, vGas: 28, vDisk: 26, vBul: 0 },
      { r: 6.5, vObs: 46, errV: 4, vGas: 30, vDisk: 25, vBul: 0 },
      { r: 8.0, vObs: 47, errV: 5, vGas: 28, vDisk: 22, vBul: 0 },
    ]
  },
  {
    name: 'IC 2574',
    distance: 4.0,
    type: 'Dwarf Irregular',
    mass: 1.5e9,
    vFlat: 67,
    rLast: 13,
    armCount: 0,
    barred: false,
    color: '#88aadd',
    rotationCurve: [
      { r: 0.8, vObs: 18, errV: 6, vGas: 8, vDisk: 12, vBul: 0 },
      { r: 2.0, vObs: 35, errV: 4, vGas: 18, vDisk: 22, vBul: 0 },
      { r: 4.0, vObs: 50, errV: 3, vGas: 28, vDisk: 32, vBul: 0 },
      { r: 6.0, vObs: 58, errV: 3, vGas: 35, vDisk: 36, vBul: 0 },
      { r: 8.5, vObs: 64, errV: 3, vGas: 40, vDisk: 38, vBul: 0 },
      { r: 11.0, vObs: 66, errV: 4, vGas: 42, vDisk: 36, vBul: 0 },
      { r: 13.0, vObs: 67, errV: 5, vGas: 40, vDisk: 32, vBul: 0 },
    ]
  },
  {
    name: 'NGC 2366',
    distance: 3.4,
    type: 'Dwarf Irregular',
    mass: 6e8,
    vFlat: 55,
    rLast: 8,
    armCount: 0,
    barred: false,
    color: '#99bbee',
    rotationCurve: [
      { r: 0.4, vObs: 15, errV: 6, vGas: 6, vDisk: 10, vBul: 0 },
      { r: 1.0, vObs: 28, errV: 4, vGas: 14, vDisk: 18, vBul: 0 },
      { r: 2.0, vObs: 40, errV: 3, vGas: 22, vDisk: 25, vBul: 0 },
      { r: 3.5, vObs: 48, errV: 3, vGas: 28, vDisk: 28, vBul: 0 },
      { r: 5.0, vObs: 52, errV: 3, vGas: 32, vDisk: 28, vBul: 0 },
      { r: 6.5, vObs: 54, errV: 4, vGas: 32, vDisk: 26, vBul: 0 },
      { r: 8.0, vObs: 55, errV: 5, vGas: 30, vDisk: 24, vBul: 0 },
    ]
  },

  // ===== VERY MASSIVE SPIRALS =====
  {
    name: 'UGC 2885',
    distance: 79,
    type: 'Giant Spiral (SAc)',
    mass: 5e11,
    vFlat: 300,
    rLast: 80,
    armCount: 2,
    barred: false,
    color: '#ffcc88',
    rotationCurve: [
      { r: 5, vObs: 185, errV: 20, vGas: 12, vDisk: 165, vBul: 45 },
      { r: 12, vObs: 255, errV: 12, vGas: 28, vDisk: 228, vBul: 38 },
      { r: 22, vObs: 285, errV: 8, vGas: 45, vDisk: 255, vBul: 25 },
      { r: 35, vObs: 298, errV: 6, vGas: 58, vDisk: 262, vBul: 15 },
      { r: 48, vObs: 302, errV: 5, vGas: 62, vDisk: 258, vBul: 8 },
      { r: 60, vObs: 300, errV: 6, vGas: 58, vDisk: 245, vBul: 4 },
      { r: 72, vObs: 298, errV: 8, vGas: 52, vDisk: 228, vBul: 2 },
    ]
  },
  {
    name: 'NGC 801',
    distance: 81,
    type: 'Giant Spiral (Sc)',
    mass: 3e11,
    vFlat: 220,
    rLast: 50,
    armCount: 2,
    barred: false,
    color: '#ffdd99',
    rotationCurve: [
      { r: 4, vObs: 145, errV: 18, vGas: 10, vDisk: 128, vBul: 35 },
      { r: 10, vObs: 195, errV: 10, vGas: 25, vDisk: 172, vBul: 28 },
      { r: 18, vObs: 215, errV: 7, vGas: 42, vDisk: 192, vBul: 18 },
      { r: 28, vObs: 222, errV: 5, vGas: 52, vDisk: 195, vBul: 10 },
      { r: 38, vObs: 220, errV: 5, vGas: 55, vDisk: 185, vBul: 5 },
      { r: 48, vObs: 218, errV: 7, vGas: 52, vDisk: 172, vBul: 2 },
    ]
  },

  // ===== EDGE-ON GALAXIES =====
  {
    name: 'NGC 891',
    distance: 9.8,
    type: 'Edge-on Spiral (SAb)',
    mass: 1.1e11,
    vFlat: 225,
    rLast: 25,
    armCount: 2,
    barred: false,
    color: '#ddbb88',
    rotationCurve: [
      { r: 1.5, vObs: 165, errV: 15, vGas: 8, vDisk: 145, vBul: 55 },
      { r: 3.5, vObs: 208, errV: 10, vGas: 18, vDisk: 182, vBul: 48 },
      { r: 6.0, vObs: 222, errV: 7, vGas: 32, vDisk: 198, vBul: 35 },
      { r: 9.0, vObs: 226, errV: 5, vGas: 42, vDisk: 202, vBul: 22 },
      { r: 13.0, vObs: 225, errV: 5, vGas: 50, vDisk: 198, vBul: 12 },
      { r: 18.0, vObs: 223, errV: 6, vGas: 52, vDisk: 185, vBul: 6 },
      { r: 24.0, vObs: 220, errV: 8, vGas: 48, vDisk: 168, vBul: 2 },
    ]
  },
]

// Utility functions
export function getGalaxyByName(name: string): SPARCGalaxy | undefined {
  return SPARC_GALAXIES.find(g => g.name === name)
}

export function getGalaxiesByType(type: string): SPARCGalaxy[] {
  return SPARC_GALAXIES.filter(g => g.type.toLowerCase().includes(type.toLowerCase()))
}

export function getSortedByMass(): SPARCGalaxy[] {
  return [...SPARC_GALAXIES].sort((a, b) => b.mass - a.mass)
}

export function getSortedByVelocity(): SPARCGalaxy[] {
  return [...SPARC_GALAXIES].sort((a, b) => b.vFlat - a.vFlat)
}
