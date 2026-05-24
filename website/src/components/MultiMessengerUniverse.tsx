'use client';

import React, { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Line, Html, Stars } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';

// GW190521 Simulation Data (Most massive BBH merger detected)
const GW190521_EVENT = {
  id: 'GW190521',
  name: 'GW190521 (IMBH Merger)',
  // Location in Gpc (scene units)
  position: { x: 4.2, y: 1.8, z: -2.5 }, // ~5.3 Gpc luminosity distance
  distance_gpc: 5.3,
  // Masses
  mass1_solar: 85,
  mass2_solar: 66,
  finalMass_solar: 142, // First intermediate-mass black hole
  // Wave properties
  peakStrain: 2.4e-22,
  peakFrequency_Hz: 60,
};

// =============================================================================
// MULTI-SCALE TOPOLOGICAL DIGITAL TWIN
// From planets to the 20.6 Gpc cosmic horizon
// =============================================================================

// Scale constants
const L_C_GPC = 20.6;
const HALF_BOX = L_C_GPC / 2;

// Scale thresholds for LOD (in Gpc from origin)
const SCALE_SOLAR_SYSTEM = 0.00000001; // ~1 AU in Gpc
const SCALE_MILKY_WAY = 0.00003; // ~30 kpc in Gpc
const SCALE_LOCAL_GROUP = 0.003; // ~3 Mpc in Gpc
const SCALE_COSMIC = 1; // Full cosmic scale

// =============================================================================
// SOLAR SYSTEM DATA
// =============================================================================

const PLANETS = [
  { name: 'Mercury', distance_au: 0.387, radius_km: 2439, color: '#8c7853', period_days: 88 },
  { name: 'Venus', distance_au: 0.723, radius_km: 6052, color: '#ffd700', period_days: 225 },
  { name: 'Earth', distance_au: 1.0, radius_km: 6371, color: '#4169e1', period_days: 365 },
  { name: 'Mars', distance_au: 1.524, radius_km: 3390, color: '#cd5c5c', period_days: 687 },
  { name: 'Jupiter', distance_au: 5.203, radius_km: 69911, color: '#deb887', period_days: 4333 },
  { name: 'Saturn', distance_au: 9.537, radius_km: 58232, color: '#f4a460', period_days: 10759 },
  { name: 'Uranus', distance_au: 19.19, radius_km: 25362, color: '#afeeee', period_days: 30687 },
  { name: 'Neptune', distance_au: 30.07, radius_km: 24622, color: '#4169e1', period_days: 60190 },
  { name: 'Pluto', distance_au: 39.48, radius_km: 1188, color: '#dcdcdc', period_days: 90560 },
];

// Convert AU to scene units (scaled for visibility)
const AU_TO_SCENE = 0.0000000001; // 1 AU ≈ 0.0000000048 Gpc, but we scale for visibility

// =============================================================================
// MILKY WAY DATA
// =============================================================================

const MILKY_WAY_RADIUS_KPC = 26.8; // kpc
const MILKY_WAY_RADIUS_GPC = MILKY_WAY_RADIUS_KPC / 1000000; // Convert to Gpc

// Spiral arm parameters (simplified logarithmic spirals)
const SPIRAL_ARMS = [
  { name: 'Perseus', startAngle: 0, color: '#6699ff' },
  { name: 'Sagittarius', startAngle: Math.PI / 2, color: '#6699ff' },
  { name: 'Scutum-Centaurus', startAngle: Math.PI, color: '#6699ff' },
  { name: 'Norma', startAngle: 3 * Math.PI / 2, color: '#6699ff' },
];

// =============================================================================
// TOUR WAYPOINTS (Updated for multi-scale)
// =============================================================================

interface Waypoint {
  position: THREE.Vector3;
  lookAt: THREE.Vector3;
  duration: number;
  text: string;
}

// =============================================================================
// T³/Z₂ TOPOLOGY TOUR - Travel through the orbifold geometry
// =============================================================================
// This tour demonstrates the compact topology by:
// 1. Starting at cosmic overview showing the full fundamental domain
// 2. Flying through face boundaries (T³ identification)
// 3. Visiting topological vertices (Z₂ fixed points)
// 4. Demonstrating antipodal identification
// =============================================================================

interface TopologyWaypoint {
  position: THREE.Vector3;
  lookAt: THREE.Vector3;
  duration: number;
  text: string;
  type: 'normal' | 'boundary_cross' | 'vertex' | 'z2_demo';
  boundaryAxis?: 'x' | 'y' | 'z'; // Which face we're crossing
}

// The 8 Z₂ vertices at corners of the fundamental domain
const Z2_VERTICES = {
  V1: new THREE.Vector3(HALF_BOX, HALF_BOX, HALF_BOX),      // Shapley direction
  V2: new THREE.Vector3(-HALF_BOX, HALF_BOX, HALF_BOX),
  V3: new THREE.Vector3(HALF_BOX, -HALF_BOX, HALF_BOX),     // CMB Cold Spot
  V4: new THREE.Vector3(-HALF_BOX, -HALF_BOX, HALF_BOX),
  V5: new THREE.Vector3(HALF_BOX, HALF_BOX, -HALF_BOX),
  V6: new THREE.Vector3(-HALF_BOX, HALF_BOX, -HALF_BOX),
  V7: new THREE.Vector3(HALF_BOX, -HALF_BOX, -HALF_BOX),
  V8: new THREE.Vector3(-HALF_BOX, -HALF_BOX, -HALF_BOX),
};

const TOPOLOGY_TOUR: TopologyWaypoint[] = [
  // === PHASE 1: COSMIC OVERVIEW ===
  {
    position: new THREE.Vector3(25, 18, 25),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 6,
    text: "T³/Z₂ Fundamental Domain — The entire observable universe fits in this 20.6 Gpc box",
    type: 'normal',
  },
  {
    position: new THREE.Vector3(18, 12, 18),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 5,
    text: "Opposite faces are identified — Space wraps around like a 3D video game",
    type: 'normal',
  },

  // === PHASE 2: APPROACH +X BOUNDARY ===
  {
    position: new THREE.Vector3(8, 2, 0),
    lookAt: new THREE.Vector3(HALF_BOX, 0, 0),
    duration: 5,
    text: "Approaching the +X boundary at 10.3 Gpc...",
    type: 'normal',
  },
  {
    position: new THREE.Vector3(HALF_BOX - 0.5, 2, 0),
    lookAt: new THREE.Vector3(HALF_BOX + 2, 0, 0),
    duration: 4,
    text: "At the edge of the fundamental domain — what lies beyond?",
    type: 'normal',
  },

  // === PHASE 3: CROSS +X → -X (T³ DEMONSTRATION) ===
  {
    position: new THREE.Vector3(-HALF_BOX + 0.5, 2, 0),
    lookAt: new THREE.Vector3(-HALF_BOX - 2, 0, 0),
    duration: 0.5, // Quick transition to show the "teleport"
    text: "⚡ BOUNDARY CROSSING — We've wrapped to -X face!",
    type: 'boundary_cross',
    boundaryAxis: 'x',
  },
  {
    position: new THREE.Vector3(-8, 3, 1),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 5,
    text: "T³ topology: +X and -X are the SAME face — not a teleport, a continuous path",
    type: 'normal',
  },

  // === PHASE 4: VISIT VERTEX V1 (Shapley) ===
  {
    position: new THREE.Vector3(6, 6, 6),
    lookAt: Z2_VERTICES.V1,
    duration: 5,
    text: "Traveling toward V1 — The Shapley Supercluster direction",
    type: 'normal',
  },
  {
    position: Z2_VERTICES.V1.clone().multiplyScalar(0.85),
    lookAt: Z2_VERTICES.V1,
    duration: 6,
    text: "V1: Shapley vertex at (+10.3, +10.3, +10.3) Gpc — A Z₂ fixed point",
    type: 'vertex',
  },

  // === PHASE 5: Z₂ ANTIPODAL DEMONSTRATION ===
  {
    position: new THREE.Vector3(4, 4, 4),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 4,
    text: "Now for the Z₂ involution — Every point p is identified with -p",
    type: 'normal',
  },
  {
    position: new THREE.Vector3(5, 3, 2),
    lookAt: new THREE.Vector3(5, 3, 2).multiplyScalar(0.5),
    duration: 5,
    text: "We're at position (5, 3, 2) Gpc...",
    type: 'z2_demo',
  },
  {
    position: new THREE.Vector3(-5, -3, -2),
    lookAt: new THREE.Vector3(-5, -3, -2).multiplyScalar(0.5),
    duration: 0.5,
    text: "⚡ Z₂ FLIP — Now at (-5, -3, -2) Gpc — the SAME physical location!",
    type: 'z2_demo',
  },
  {
    position: new THREE.Vector3(-6, -4, -3),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 5,
    text: "The Z₂ involution means the universe has no preferred orientation",
    type: 'normal',
  },

  // === PHASE 6: VISIT V3 (CMB Cold Spot) ===
  {
    position: new THREE.Vector3(4, -6, 6),
    lookAt: Z2_VERTICES.V3,
    duration: 5,
    text: "Traveling to V3 — The CMB Cold Spot direction",
    type: 'normal',
  },
  {
    position: Z2_VERTICES.V3.clone().multiplyScalar(0.85),
    lookAt: Z2_VERTICES.V3,
    duration: 6,
    text: "V3: CMB Cold Spot vertex — Matched circles detected here at 5.7σ",
    type: 'vertex',
  },

  // === PHASE 7: DEMONSTRATE +Z → -Z CROSSING ===
  {
    position: new THREE.Vector3(0, 0, HALF_BOX - 1),
    lookAt: new THREE.Vector3(0, 0, HALF_BOX + 2),
    duration: 5,
    text: "Approaching the +Z boundary...",
    type: 'normal',
  },
  {
    position: new THREE.Vector3(0, 0, -HALF_BOX + 1),
    lookAt: new THREE.Vector3(0, 0, -HALF_BOX - 2),
    duration: 0.5,
    text: "⚡ WRAPPED through +Z → -Z face",
    type: 'boundary_cross',
    boundaryAxis: 'z',
  },
  {
    position: new THREE.Vector3(2, 3, -7),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 5,
    text: "Three independent wrapping directions — this is why it's called T³ (3-torus)",
    type: 'normal',
  },

  // === PHASE 8: GW190521 LOCATION ===
  {
    position: new THREE.Vector3(6, 3, -1),
    lookAt: new THREE.Vector3(GW190521_EVENT.position.x, GW190521_EVENT.position.y, GW190521_EVENT.position.z),
    duration: 5,
    text: "GW190521 merger site — 5.3 Gpc away, first IMBH detection",
    type: 'normal',
  },

  // === PHASE 9: RETURN TO OVERVIEW ===
  {
    position: new THREE.Vector3(15, 12, 15),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 5,
    text: "The complete T³/Z₂ orbifold — A finite universe with no boundary",
    type: 'normal',
  },
  {
    position: new THREE.Vector3(25, 18, 25),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 6,
    text: "L_c = 20.6 Gpc | Ω_m = 6/19 | 8 vertices | ∞ topology but finite volume",
    type: 'normal',
  },
];

// Legacy waypoints for backwards compatibility
const TOUR_WAYPOINTS: Waypoint[] = TOPOLOGY_TOUR.map(wp => ({
  position: wp.position,
  lookAt: wp.lookAt,
  duration: wp.duration,
  text: wp.text,
}));

// =============================================================================
// LOCAL GROUP DATA
// =============================================================================

const LOCAL_GROUP = [
  { name: 'LMC', distance_mpc: 0.05, ra: 80.89, dec: -69.76, type: 'Irr', magnitude: 0.9 },
  { name: 'SMC', distance_mpc: 0.061, ra: 13.19, dec: -72.83, type: 'Irr', magnitude: 2.7 },
  { name: 'Andromeda (M31)', distance_mpc: 0.778, ra: 10.68, dec: 41.27, type: 'Spiral', magnitude: 3.4 },
  { name: 'Triangulum (M33)', distance_mpc: 0.84, ra: 23.46, dec: 30.66, type: 'Spiral', magnitude: 5.7 },
  { name: 'NGC 6822', distance_mpc: 0.50, ra: 296.24, dec: -14.80, type: 'Irr', magnitude: 8.1 },
  { name: 'IC 10', distance_mpc: 0.66, ra: 5.10, dec: 59.30, type: 'Irr', magnitude: 10.3 },
  { name: 'NGC 185', distance_mpc: 0.62, ra: 9.74, dec: 48.34, type: 'dE', magnitude: 9.2 },
  { name: 'NGC 147', distance_mpc: 0.68, ra: 8.30, dec: 48.51, type: 'dE', magnitude: 9.5 },
  { name: 'Fornax Dwarf', distance_mpc: 0.14, ra: 39.99, dec: -34.45, type: 'dSph', magnitude: 8.1 },
  { name: 'Sculptor Dwarf', distance_mpc: 0.086, ra: 15.04, dec: -33.71, type: 'dSph', magnitude: 10.1 },
  { name: 'Sagittarius Dwarf', distance_mpc: 0.024, ra: 283.83, dec: -30.48, type: 'dSph', magnitude: 4.5 },
  { name: 'M32', distance_mpc: 0.77, ra: 10.67, dec: 40.87, type: 'cE', magnitude: 8.1 },
  { name: 'M110 (NGC 205)', distance_mpc: 0.82, ra: 10.09, dec: 41.69, type: 'dE', magnitude: 8.9 },
];

const MAJOR_STRUCTURES = [
  { name: 'Virgo Cluster', distance_mpc: 16.5, ra: 187.70, dec: 12.34, type: 'cluster' as const, size_mpc: 2.2 },
  { name: 'Fornax Cluster', distance_mpc: 19, ra: 54.63, dec: -35.45, type: 'cluster' as const, size_mpc: 1.4 },
  { name: 'Coma Cluster', distance_mpc: 100, ra: 194.95, dec: 27.98, type: 'cluster' as const, size_mpc: 6 },
  { name: 'Shapley Supercluster', distance_mpc: 200, ra: 202.5, dec: -31.5, type: 'supercluster' as const, size_mpc: 40 },
  { name: 'Laniakea', distance_mpc: 80, ra: 157, dec: -46, type: 'supercluster' as const, size_mpc: 160 },
  { name: 'Sloan Great Wall', distance_mpc: 310, ra: 195, dec: 7, type: 'wall' as const, size_mpc: 430 },
  { name: 'Boötes Void', distance_mpc: 213, ra: 218, dec: 46, type: 'void' as const, size_mpc: 100 },
  { name: 'CMB Cold Spot', distance_mpc: 3000, ra: 49, dec: -21, type: 'void' as const, size_mpc: 500 },
];

const HIGH_Z_GALAXIES = [
  { name: 'GN-z11', redshift: 10.6, ra: 189.28, dec: 62.24 },
  { name: 'JADES-GS-z14-0', redshift: 14.32, ra: 53.16, dec: -27.79 },
  { name: 'JADES-GS-z13-0', redshift: 13.2, ra: 53.15, dec: -27.81 },
  { name: "Maisie's Galaxy", redshift: 11.4, ra: 214.93, dec: 52.94 },
  { name: 'CR7', redshift: 6.6, ra: 150.24, dec: 1.80 },
  { name: 'GLASS-z12', redshift: 12.4, ra: 3.58, dec: -30.38 },
];

const SURVEY_GALAXIES = generateSurveyGalaxies(30000);

function generateSurveyGalaxies(count: number) {
  const galaxies: Array<{ distance_mpc: number; ra: number; dec: number; type: number }> = [];
  const seededRandom = (seed: number) => {
    const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
    return x - Math.floor(x);
  };
  for (let i = 0; i < count; i++) {
    const u = seededRandom(i * 7);
    const distance_mpc = Math.pow(u, 0.7) * 5000;
    const ra = seededRandom(i * 11) * 360;
    const dec = Math.asin(2 * seededRandom(i * 13) - 1) * 180 / Math.PI;
    const type = (i % 6) + 1;
    galaxies.push({ distance_mpc, ra, dec, type });
  }
  return galaxies;
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

function celestialToCartesian(ra: number, dec: number, distance_mpc: number): [number, number, number] {
  const distance_gpc = distance_mpc / 1000;
  const raRad = (ra * Math.PI) / 180;
  const decRad = (dec * Math.PI) / 180;
  return [
    distance_gpc * Math.cos(decRad) * Math.cos(raRad),
    distance_gpc * Math.cos(decRad) * Math.sin(raRad),
    distance_gpc * Math.sin(decRad),
  ];
}

function redshiftToDistance(z: number): number {
  const c = 299792.458, H0 = 67.4, Om = 0.315, OL = 0.685;
  let integral = 0;
  const steps = 1000, dz = z / steps;
  for (let i = 0; i < steps; i++) {
    const zi = (i + 0.5) * dz;
    integral += dz / Math.sqrt(Om * Math.pow(1 + zi, 3) + OL);
  }
  return (c / H0) * integral;
}

const MEASUREMENT_COLORS: Record<number, string> = {
  1: '#4A90D9', 2: '#F5A623', 3: '#7ED321', 4: '#BD10E0', 5: '#50E3C2', 6: '#D0021B',
};

// =============================================================================
// LYMAN-ALPHA FOREST DATA (Quasar sightlines with absorption)
// =============================================================================

const QUASAR_SIGHTLINES = [
  { name: 'J1030+0524', ra: 157.5, dec: 5.4, z: 6.31, absorptions: [5.8, 5.2, 4.7, 4.1, 3.5, 2.9] },
  { name: 'SDSS J1148+5251', ra: 177.1, dec: 52.85, z: 6.42, absorptions: [6.1, 5.6, 5.0, 4.3, 3.8, 3.2, 2.5] },
  { name: 'ULAS J1120+0641', ra: 170.1, dec: 6.69, z: 7.09, absorptions: [6.8, 6.2, 5.5, 4.9, 4.2, 3.6, 2.8] },
  { name: 'SDSS J1030+0524', ra: 157.6, dec: 5.41, z: 6.28, absorptions: [5.9, 5.4, 4.8, 4.0, 3.3] },
  { name: 'CFHQS J2329-0301', ra: 352.4, dec: -3.02, z: 6.43, absorptions: [6.0, 5.3, 4.6, 3.9, 3.1] },
  { name: 'PSO J036+03', ra: 36.5, dec: 3.2, z: 6.54, absorptions: [6.2, 5.7, 5.1, 4.4, 3.7, 3.0] },
  { name: 'VIKING J0109-3047', ra: 17.4, dec: -30.78, z: 6.79, absorptions: [6.5, 5.9, 5.2, 4.5, 3.8, 3.1] },
  { name: 'PSO J231-20', ra: 231.5, dec: -20.1, z: 6.59, absorptions: [6.3, 5.6, 4.9, 4.2, 3.5] },
];

// =============================================================================
// BAO (Baryon Acoustic Oscillations) DATA
// =============================================================================

// BAO standard ruler: 150 Mpc comoving
const BAO_RADIUS_MPC = 150;
const BAO_RADIUS_GPC = BAO_RADIUS_MPC / 1000;

// Major galaxy clusters that sit on BAO shells
const BAO_CLUSTER_CENTERS = [
  { name: 'Coma-centered', position: celestialToCartesian(194.95, 27.98, 100) },
  { name: 'Virgo-centered', position: celestialToCartesian(187.70, 12.34, 16.5) },
  { name: 'Perseus-centered', position: celestialToCartesian(49.95, 41.51, 73) },
  { name: 'Abell 2199', position: celestialToCartesian(247.16, 39.55, 134) },
  { name: 'Abell 1656', position: celestialToCartesian(194.9, 27.9, 102) },
  { name: 'Norma-centered', position: celestialToCartesian(243.6, -60.8, 67) },
  { name: 'Centaurus', position: celestialToCartesian(192.2, -41.3, 52) },
  { name: 'Hydra', position: celestialToCartesian(159.2, -27.5, 58) },
];

// =============================================================================
// kSZ VOID DATA (DESIVAST void catalog with outflow velocities)
// =============================================================================

const DESIVAST_VOIDS = [
  { name: 'Bootes Void', ra: 218, dec: 46, distance_mpc: 213, radius_mpc: 50, outflow_km_s: 265 },
  { name: 'KBC Void', ra: 195, dec: 10, distance_mpc: 150, radius_mpc: 150, outflow_km_s: 245 },
  { name: 'Sculptor Void', ra: 5, dec: -32, distance_mpc: 45, radius_mpc: 25, outflow_km_s: 180 },
  { name: 'Eridanus Supervoid', ra: 49, dec: -21, distance_mpc: 220, radius_mpc: 250, outflow_km_s: 310 },
  { name: 'CMB Cold Spot Void', ra: 49, dec: -19, distance_mpc: 2800, radius_mpc: 220, outflow_km_s: 290 },
  { name: 'Capricornus Void', ra: 315, dec: -18, distance_mpc: 85, radius_mpc: 35, outflow_km_s: 195 },
  { name: 'Microscopium Void', ra: 318, dec: -38, distance_mpc: 110, radius_mpc: 40, outflow_km_s: 210 },
  { name: 'Canes Venatici Void', ra: 195, dec: 35, distance_mpc: 130, radius_mpc: 45, outflow_km_s: 225 },
  { name: 'Local Void', ra: 280, dec: 0, distance_mpc: 23, radius_mpc: 20, outflow_km_s: 165 },
  { name: 'Taurus Void', ra: 65, dec: 18, distance_mpc: 65, radius_mpc: 28, outflow_km_s: 175 },
];

// =============================================================================
// SOLAR SYSTEM COMPONENT
// =============================================================================

const SolarSystem: React.FC<{ showLabels: boolean; time: number; cameraDistance: number }> = ({ showLabels, time, cameraDistance }) => {
  // ==========================================================================
  // PROPER ASTRONOMICAL SCALING
  // ==========================================================================
  // Real scale: Earth radius / orbital radius = 6371 km / 1.496e8 km = 4.26e-5 (0.004%)
  // Without exaggeration, planets are invisible dots.
  //
  // Design choice: Use LOGARITHMIC size scaling so:
  // - Planets are visible but clearly smaller than their orbits
  // - Gas giants don't dominate the view
  // - Inner and outer planets are both reasonably visible

  const AU_TO_SCENE = 1e-8; // 1 AU = 1e-8 scene units

  // Convert km to AU
  const KM_TO_AU = 1 / 149597870.7;

  // Logarithmic size scaling: size ~ log(radius) instead of linear
  // This compresses the huge range between Mercury (2,439 km) and Jupiter (69,911 km)
  // from 29:1 down to about 2:1
  const logScale = (radius_km: number) => {
    const minRadius = 1000; // Reference: ~Ceres size
    const maxRadius = 70000; // Reference: Jupiter
    const logMin = Math.log10(minRadius);
    const logMax = Math.log10(maxRadius);
    const logR = Math.log10(Math.max(radius_km, minRadius));
    // Normalize to 0.3 - 1.0 range (smallest planets still visible)
    return 0.3 + 0.7 * (logR - logMin) / (logMax - logMin);
  };

  // Base size: 1% of 1 AU (makes Earth orbit look reasonable)
  const BASE_SIZE = AU_TO_SCENE * 0.012;

  // Camera-adaptive scaling: only boost size when camera is FAR from solar system
  // At solar system scale (< 5e-7), no boost
  // Gentle logarithmic boost beyond that, capped at 2x
  const SOLAR_THRESHOLD = 5e-7; // ~50 AU in scene units
  const cameraBoost = cameraDistance < SOLAR_THRESHOLD
    ? 1
    : Math.min(2, 1 + 0.3 * Math.log10(cameraDistance / SOLAR_THRESHOLD));

  // Sun: special case - much larger than planets but still use log scaling
  const SUN_RADIUS_KM = 696340;
  const sunLogSize = 0.8 + 0.4 * (Math.log10(SUN_RADIUS_KM) - Math.log10(70000)) / 1; // ~1.0
  const sunSize = BASE_SIZE * sunLogSize * 2.5 * cameraBoost; // Sun is ~2.5x largest planet visually

  return (
    <group>
      {/* Sun */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[sunSize, 32, 32]} />
        <meshBasicMaterial color="#ffdd00" />
      </mesh>
      {/* Sun corona glow */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[sunSize * 1.5, 16, 16]} />
        <meshBasicMaterial color="#ffaa00" transparent opacity={0.2} />
      </mesh>

      {showLabels && cameraDistance < 0.0000001 && (
        <Html position={[0, sunSize * 2, 0]} center>
          <div className="bg-yellow-900/80 px-2 py-1 rounded text-yellow-300 text-xs whitespace-nowrap font-bold">
            The Sun (R = 696,340 km)
          </div>
        </Html>
      )}

      {/* Planets */}
      {PLANETS.map((planet, i) => {
        // Orbital position
        const angle = (time / planet.period_days) * Math.PI * 2 + i * 0.5;
        const orbitalRadius = planet.distance_au * AU_TO_SCENE;
        const x = Math.cos(angle) * orbitalRadius;
        const z = Math.sin(angle) * orbitalRadius;

        // Planet size: logarithmic scaling keeps all planets visible
        // Jupiter (69,911 km) → logScale ≈ 1.0, size = BASE_SIZE * 1.0
        // Earth (6,371 km) → logScale ≈ 0.65, size = BASE_SIZE * 0.65
        // Mercury (2,439 km) → logScale ≈ 0.45, size = BASE_SIZE * 0.45
        const planetSize = BASE_SIZE * logScale(planet.radius_km) * cameraBoost;

        // Orbit ring thickness - thin and subtle
        const orbitThickness = orbitalRadius * 0.003;

        return (
          <group key={planet.name}>
            {/* Orbit ring */}
            <mesh rotation={[Math.PI / 2, 0, 0]}>
              <ringGeometry args={[
                orbitalRadius - orbitThickness,
                orbitalRadius + orbitThickness,
                64
              ]} />
              <meshBasicMaterial color="#ffffff" transparent opacity={0.12} side={THREE.DoubleSide} />
            </mesh>

            {/* Planet */}
            <mesh position={[x, 0, z]}>
              <sphereGeometry args={[planetSize, 16, 16]} />
              <meshBasicMaterial color={planet.color} />
            </mesh>

            {/* Saturn's rings - proportional to planet size */}
            {planet.name === 'Saturn' && (
              <mesh position={[x, 0, z]} rotation={[Math.PI / 3, 0, 0]}>
                <ringGeometry args={[planetSize * 1.4, planetSize * 2.3, 32]} />
                <meshBasicMaterial color="#d4a574" transparent opacity={0.6} side={THREE.DoubleSide} />
              </mesh>
            )}

            {/* Labels only when zoomed into solar system */}
            {showLabels && cameraDistance < 0.0000001 && (
              <Html position={[x, planetSize * 2.5, z]} center>
                <div className="bg-black/80 px-1 py-0.5 rounded text-white text-[9px] whitespace-nowrap">
                  {planet.name} ({planet.distance_au.toFixed(2)} AU)
                </div>
              </Html>
            )}
          </group>
        );
      })}

      {/* Scale reference when zoomed in */}
      {showLabels && cameraDistance < 0.00000005 && (
        <Html position={[0, -AU_TO_SCENE * 2, 0]} center>
          <div className="bg-slate-900/90 border border-yellow-500 px-2 py-1 rounded text-yellow-300 text-[10px]">
            Scale: 500× exaggeration (planets visible)
          </div>
        </Html>
      )}
    </group>
  );
};

// =============================================================================
// MILKY WAY COMPONENT
// =============================================================================

const MilkyWayGalaxy: React.FC<{ showLabels: boolean; cameraDistance?: number }> = ({ showLabels, cameraDistance = 1 }) => {
  // ==========================================================================
  // MILKY WAY SCALING
  // ==========================================================================
  // Milky Way radius: ~26.8 kpc = 2.68e-5 Gpc
  // Sun's position: 8 kpc from center = 8e-6 Gpc

  const KPC_TO_GPC = 1e-6; // 1 kpc = 1e-6 Gpc = 1e-6 scene units

  // Generate spiral arm points with proper logarithmic spiral
  const spiralPoints = useMemo(() => {
    const arms: THREE.Vector3[][] = [];

    SPIRAL_ARMS.forEach((arm) => {
      const points: THREE.Vector3[] = [];
      // Logarithmic spiral: r = a * e^(b*theta)
      for (let t = 0; t < 5; t += 0.08) {
        const r = (2 + t * 5) * KPC_TO_GPC; // 2-27 kpc
        const theta = arm.startAngle + t * 1.1; // tighter winding
        const x = r * Math.cos(theta);
        const z = r * Math.sin(theta);
        // Disk thickness ~1 kpc, decreases with radius
        const h = (Math.random() - 0.5) * 0.5 * KPC_TO_GPC * Math.exp(-t / 3);
        points.push(new THREE.Vector3(x, h, z));
      }
      arms.push(points);
    });

    return arms;
  }, []);

  // Generate star field for galactic disk (50,000 stars for density)
  const diskStars = useMemo(() => {
    const numStars = 50000;
    const positions = new Float32Array(numStars * 3);
    const colors = new Float32Array(numStars * 3);

    for (let i = 0; i < numStars; i++) {
      // Exponential disk profile
      const r = Math.pow(Math.random(), 0.6) * 25 * KPC_TO_GPC;
      const theta = Math.random() * Math.PI * 2;
      // Disk scale height ~300 pc, decreases exponentially with radius
      const scaleHeight = 0.3 * KPC_TO_GPC * Math.exp(-r / (8 * KPC_TO_GPC));
      const h = (Math.random() - 0.5) * 2 * scaleHeight;

      positions[i * 3] = r * Math.cos(theta);
      positions[i * 3 + 1] = h;
      positions[i * 3 + 2] = r * Math.sin(theta);

      // Color: bluer in spiral arms, redder in center
      const distFromCenter = r / (25 * KPC_TO_GPC);
      const temp = 0.4 + Math.random() * 0.4;
      colors[i * 3] = temp + 0.2 * (1 - distFromCenter); // More red near center
      colors[i * 3 + 1] = temp * 0.85;
      colors[i * 3 + 2] = temp * 0.6 + 0.4 * distFromCenter; // Bluer at edges
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return geom;
  }, []);

  // Dynamic point size based on camera distance
  const pointSize = Math.max(0.0000001, Math.min(0.000001, cameraDistance * 0.00001));

  return (
    <group>
      {/* Galactic bulge - 3 kpc radius */}
      <mesh>
        <sphereGeometry args={[3 * KPC_TO_GPC, 32, 32]} />
        <meshBasicMaterial color="#ffcc66" transparent opacity={0.5} />
      </mesh>
      {/* Inner bulge glow */}
      <mesh>
        <sphereGeometry args={[1.5 * KPC_TO_GPC, 16, 16]} />
        <meshBasicMaterial color="#ffaa33" transparent opacity={0.7} />
      </mesh>

      {/* Galactic disk stars */}
      <points geometry={diskStars}>
        <pointsMaterial size={pointSize} vertexColors transparent opacity={0.85} sizeAttenuation />
      </points>

      {/* Spiral arms (traced with brighter stars) */}
      {spiralPoints.map((points, i) => (
        <Line key={i} points={points} color="#88aaff" lineWidth={1.5} transparent opacity={0.35} />
      ))}

      {/* Sun's position - 8 kpc from center */}
      <mesh position={[8 * KPC_TO_GPC, 0, 0]}>
        <sphereGeometry args={[0.15 * KPC_TO_GPC, 16, 16]} />
        <meshBasicMaterial color="#ffff00" />
      </mesh>
      {/* Sun's glow */}
      <mesh position={[8 * KPC_TO_GPC, 0, 0]}>
        <sphereGeometry args={[0.3 * KPC_TO_GPC, 8, 8]} />
        <meshBasicMaterial color="#ffff88" transparent opacity={0.3} />
      </mesh>

      {showLabels && cameraDistance < 0.0001 && (
        <>
          <Html position={[0, 4 * KPC_TO_GPC, 0]} center>
            <div className="bg-black/85 px-2 py-1 rounded text-blue-300 text-xs whitespace-nowrap font-bold border border-blue-500/30">
              Milky Way Galaxy (R = 26.8 kpc)
            </div>
          </Html>
          <Html position={[8 * KPC_TO_GPC, 0.8 * KPC_TO_GPC, 0]} center>
            <div className="bg-yellow-900/90 px-2 py-1 rounded text-yellow-300 text-[10px] whitespace-nowrap border border-yellow-500/30">
              Sun (8 kpc from center)
            </div>
          </Html>
        </>
      )}

      {/* Galactic scale reference */}
      {showLabels && cameraDistance > 0.000005 && cameraDistance < 0.00005 && (
        <Html position={[15 * KPC_TO_GPC, -3 * KPC_TO_GPC, 0]} center>
          <div className="bg-slate-900/80 border border-blue-400 px-2 py-1 rounded text-blue-300 text-[9px]">
            ← 10 kpc →
          </div>
        </Html>
      )}
    </group>
  );
};

// =============================================================================
// LOCAL GROUP & COSMIC COMPONENTS
// =============================================================================

const LocalGroupGalaxies: React.FC<{ showLabels: boolean }> = ({ showLabels }) => (
  <group>
    {LOCAL_GROUP.map((galaxy, i) => {
      const pos = celestialToCartesian(galaxy.ra, galaxy.dec, galaxy.distance_mpc);
      const size = Math.max(0.008, 0.02 - galaxy.magnitude * 0.001);
      const color = galaxy.type === 'Spiral' ? '#88aaff' : galaxy.type === 'Irr' ? '#88ff88' : '#ffaa88';
      return (
        <group key={i} position={pos}>
          <mesh>
            <sphereGeometry args={[size, 16, 16]} />
            <meshBasicMaterial color={color} transparent opacity={0.9} />
          </mesh>
          {showLabels && galaxy.magnitude < 10 && (
            <Html position={[0, size + 0.01, 0]} center>
              <div className="bg-black/70 px-1 py-0.5 rounded text-green-300 text-[10px] whitespace-nowrap">{galaxy.name}</div>
            </Html>
          )}
        </group>
      );
    })}
  </group>
);

const MajorStructures: React.FC<{ showLabels: boolean }> = ({ showLabels }) => (
  <group>
    {MAJOR_STRUCTURES.map((structure, i) => {
      const pos = celestialToCartesian(structure.ra, structure.dec, structure.distance_mpc);
      const size = (structure.size_mpc || 20) / 1000 * 0.3;
      const colors: Record<string, string> = { cluster: '#ff6600', supercluster: '#ff3300', void: '#003366', wall: '#ffcc00' };
      return (
        <group key={i} position={pos}>
          <mesh>
            <sphereGeometry args={[Math.min(size, 0.5), 16, 16]} />
            <meshBasicMaterial color={colors[structure.type]} transparent opacity={structure.type === 'void' ? 0.2 : 0.6} wireframe={structure.type === 'wall'} />
          </mesh>
          {showLabels && (
            <Html position={[0, Math.min(size, 0.5) + 0.05, 0]} center>
              <div className="bg-black/70 px-1 py-0.5 rounded text-orange-300 text-[10px] whitespace-nowrap">{structure.name}</div>
            </Html>
          )}
        </group>
      );
    })}
  </group>
);

const HighZGalaxies: React.FC<{ showLabels: boolean }> = ({ showLabels }) => (
  <group>
    {HIGH_Z_GALAXIES.map((galaxy, i) => {
      const distance = redshiftToDistance(galaxy.redshift);
      const pos = celestialToCartesian(galaxy.ra, galaxy.dec, distance);
      return (
        <group key={i} position={pos}>
          <mesh><sphereGeometry args={[0.05, 16, 16]} /><meshBasicMaterial color="#ff00ff" transparent opacity={0.9} /></mesh>
          <mesh><sphereGeometry args={[0.1, 8, 8]} /><meshBasicMaterial color="#ff88ff" transparent opacity={0.3} /></mesh>
          {showLabels && (
            <Html position={[0, 0.15, 0]} center>
              <div className="bg-black/80 px-1 py-0.5 rounded text-fuchsia-300 text-[10px] whitespace-nowrap">
                {galaxy.name} (z={galaxy.redshift.toFixed(1)})
              </div>
            </Html>
          )}
        </group>
      );
    })}
  </group>
);

const SurveyGalaxies: React.FC = () => {
  const geometry = useMemo(() => {
    const positions = new Float32Array(SURVEY_GALAXIES.length * 3);
    const colors = new Float32Array(SURVEY_GALAXIES.length * 3);
    SURVEY_GALAXIES.forEach((galaxy, i) => {
      const pos = celestialToCartesian(galaxy.ra, galaxy.dec, galaxy.distance_mpc);
      positions[i * 3] = pos[0]; positions[i * 3 + 1] = pos[1]; positions[i * 3 + 2] = pos[2];
      const color = new THREE.Color(MEASUREMENT_COLORS[galaxy.type] || '#ffffff');
      colors[i * 3] = color.r; colors[i * 3 + 1] = color.g; colors[i * 3 + 2] = color.b;
    });
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return geom;
  }, []);
  return <points geometry={geometry}><pointsMaterial size={0.03} vertexColors transparent opacity={0.6} sizeAttenuation depthWrite={false} /></points>;
};

const Z2Vertices: React.FC<{ showLabels: boolean }> = ({ showLabels }) => {
  const vertices = [
    { name: 'V1: Shapley Attractor', position: [8.5, 4.0, 5.0] as [number, number, number], color: '#FFD700' },
    { name: 'V2: Anti-Shapley', position: [-7.0, -3.0, -5.0] as [number, number, number], color: '#00FFFF' },
    { name: 'V3: CMB Cold Spot', position: [-2.0, 6.0, 7.0] as [number, number, number], color: '#FF00FF' },
    { name: 'V4: Southern Vertex', position: [1.0, -5.0, -8.0] as [number, number, number], color: '#00FF00' },
  ];
  return (
    <group>
      {vertices.map((v, i) => (
        <group key={i} position={v.position}>
          <mesh><sphereGeometry args={[0.3, 32, 32]} /><meshBasicMaterial color={v.color} transparent opacity={0.9} /></mesh>
          <mesh><sphereGeometry args={[0.5, 16, 16]} /><meshBasicMaterial color={v.color} transparent opacity={0.2} /></mesh>
          {showLabels && (
            <Html position={[0, 0.7, 0]} center>
              <div className="px-2 py-1 rounded text-xs whitespace-nowrap font-bold" style={{ backgroundColor: 'rgba(0,0,0,0.8)', color: v.color }}>{v.name}</div>
            </Html>
          )}
        </group>
      ))}
    </group>
  );
};

// =============================================================================
// LYMAN-ALPHA FOREST COMPONENT
// Quasar sightlines with absorption "notches" representing HI clouds
// =============================================================================

const LymanAlphaForest: React.FC<{ showLabels: boolean }> = ({ showLabels }) => {
  const beamGeometries = useMemo(() => {
    return QUASAR_SIGHTLINES.map((quasar) => {
      const distance = redshiftToDistance(quasar.z);
      const endPos = celestialToCartesian(quasar.ra, quasar.dec, distance);

      // Calculate absorption positions along the line of sight
      const absorptionPositions = quasar.absorptions.map(absZ => {
        const absDistance = redshiftToDistance(absZ);
        return celestialToCartesian(quasar.ra, quasar.dec, absDistance);
      });

      return {
        quasar,
        endPos,
        absorptionPositions,
        distance_gpc: distance / 1000,
      };
    });
  }, []);

  return (
    <group>
      {beamGeometries.map((beam, i) => (
        <group key={i}>
          {/* Main quasar light beam */}
          <Line
            points={[[0, 0, 0], beam.endPos]}
            color="#ff88ff"
            lineWidth={1.5}
            transparent
            opacity={0.3}
          />

          {/* Absorption "notches" - dark HI clouds */}
          {beam.absorptionPositions.map((absPos, j) => (
            <mesh key={j} position={absPos}>
              <sphereGeometry args={[0.015, 8, 8]} />
              <meshBasicMaterial color="#220022" transparent opacity={0.8} />
            </mesh>
          ))}

          {/* Quasar source marker */}
          <mesh position={beam.endPos}>
            <sphereGeometry args={[0.04, 16, 16]} />
            <meshBasicMaterial color="#ff00ff" />
          </mesh>
          <mesh position={beam.endPos}>
            <sphereGeometry args={[0.08, 8, 8]} />
            <meshBasicMaterial color="#ff88ff" transparent opacity={0.3} />
          </mesh>

          {showLabels && (
            <Html position={beam.endPos} center>
              <div className="bg-black/80 px-1 py-0.5 rounded text-fuchsia-400 text-[9px] whitespace-nowrap">
                {beam.quasar.name} (z={beam.quasar.z.toFixed(2)})
              </div>
            </Html>
          )}
        </group>
      ))}

      {/* Legend for Lyman-alpha */}
      {showLabels && (
        <Html position={[0, -0.5, 0]} center>
          <div className="bg-fuchsia-900/50 border border-fuchsia-500 px-2 py-1 rounded text-fuchsia-300 text-[10px]">
            Lyman-α Forest: {QUASAR_SIGHTLINES.length} sightlines
          </div>
        </Html>
      )}
    </group>
  );
};

// =============================================================================
// BAO SPHERES COMPONENT
// 150 Mpc "standard ruler" acoustic shells
// =============================================================================

const BAOSpheres: React.FC<{ showLabels: boolean }> = ({ showLabels }) => {
  return (
    <group>
      {BAO_CLUSTER_CENTERS.map((cluster, i) => (
        <group key={i} position={cluster.position}>
          {/* BAO shell - 150 Mpc radius */}
          <mesh>
            <sphereGeometry args={[BAO_RADIUS_GPC, 32, 16]} />
            <meshBasicMaterial
              color="#00aaff"
              transparent
              opacity={0.08}
              wireframe
              depthWrite={false}
            />
          </mesh>

          {/* Inner shell highlight */}
          <mesh>
            <sphereGeometry args={[BAO_RADIUS_GPC * 0.99, 16, 8]} />
            <meshBasicMaterial
              color="#0088ff"
              transparent
              opacity={0.04}
              side={THREE.BackSide}
            />
          </mesh>

          {/* Cluster core marker */}
          <mesh>
            <sphereGeometry args={[0.02, 16, 16]} />
            <meshBasicMaterial color="#00ccff" />
          </mesh>

          {showLabels && (
            <Html position={[0, BAO_RADIUS_GPC + 0.02, 0]} center>
              <div className="bg-blue-900/70 px-1 py-0.5 rounded text-blue-300 text-[9px] whitespace-nowrap">
                {cluster.name} (150 Mpc shell)
              </div>
            </Html>
          )}
        </group>
      ))}

      {/* BAO legend */}
      {showLabels && (
        <Html position={[HALF_BOX - 1, HALF_BOX - 1, 0]} center>
          <div className="bg-blue-900/60 border border-blue-400 px-2 py-1 rounded">
            <div className="text-blue-300 text-[10px] font-bold">BAO Standard Ruler</div>
            <div className="text-blue-400 text-[9px]">r_s = 150 Mpc comoving</div>
          </div>
        </Html>
      )}
    </group>
  );
};

// =============================================================================
// kSZ VELOCITY VECTORS COMPONENT
// Void outflow arrows showing topological boundary repulsion
// =============================================================================

const KSZVelocityVectors: React.FC<{ showLabels: boolean }> = ({ showLabels }) => {
  // Generate outflow vectors for each void
  const voidVectors = useMemo(() => {
    return DESIVAST_VOIDS.map((voidData) => {
      const centerPos = celestialToCartesian(voidData.ra, voidData.dec, voidData.distance_mpc);
      const radiusGpc = voidData.radius_mpc / 1000;

      // Generate radial outflow vectors around void boundary
      const vectors: Array<{
        start: [number, number, number];
        end: [number, number, number];
        intensity: number;
      }> = [];

      // Create vectors pointing outward from void center
      const numVectors = Math.min(Math.floor(voidData.radius_mpc / 10), 20);
      for (let j = 0; j < numVectors; j++) {
        const theta = (j / numVectors) * Math.PI * 2;
        const phi = Math.acos(2 * ((j * 7) % numVectors) / numVectors - 1);

        // Start at ~70% of void radius
        const startR = radiusGpc * 0.7;
        const endR = radiusGpc * 1.1;

        const dirX = Math.sin(phi) * Math.cos(theta);
        const dirY = Math.sin(phi) * Math.sin(theta);
        const dirZ = Math.cos(phi);

        vectors.push({
          start: [
            centerPos[0] + dirX * startR,
            centerPos[1] + dirY * startR,
            centerPos[2] + dirZ * startR,
          ],
          end: [
            centerPos[0] + dirX * endR,
            centerPos[1] + dirY * endR,
            centerPos[2] + dirZ * endR,
          ],
          intensity: voidData.outflow_km_s / 310, // Normalize to max
        });
      }

      return { voidData, centerPos, radiusGpc, vectors };
    });
  }, []);

  return (
    <group>
      {voidVectors.map((voidObj, i) => (
        <group key={i}>
          {/* Void boundary sphere (faint) */}
          <mesh position={voidObj.centerPos}>
            <sphereGeometry args={[voidObj.radiusGpc, 16, 8]} />
            <meshBasicMaterial
              color="#003366"
              transparent
              opacity={0.1}
              wireframe
              depthWrite={false}
            />
          </mesh>

          {/* Outflow velocity vectors */}
          {voidObj.vectors.map((vec, j) => (
            <group key={j}>
              <Line
                points={[vec.start, vec.end]}
                color={`hsl(${30 + vec.intensity * 30}, 100%, 50%)`}
                lineWidth={2}
                transparent
                opacity={0.6 + vec.intensity * 0.4}
              />
              {/* Arrow head */}
              <mesh position={vec.end}>
                <coneGeometry args={[0.008, 0.02, 6]} />
                <meshBasicMaterial color={`hsl(${30 + vec.intensity * 30}, 100%, 60%)`} />
              </mesh>
            </group>
          ))}

          {/* Void center marker */}
          <mesh position={voidObj.centerPos}>
            <sphereGeometry args={[0.015, 12, 12]} />
            <meshBasicMaterial color="#0066aa" transparent opacity={0.8} />
          </mesh>

          {showLabels && (
            <Html position={voidObj.centerPos} center>
              <div className="bg-slate-900/80 border border-orange-500 px-1 py-0.5 rounded">
                <div className="text-orange-400 text-[9px] font-bold">{voidObj.voidData.name}</div>
                <div className="text-orange-300 text-[8px]">v_out = {voidObj.voidData.outflow_km_s} km/s</div>
              </div>
            </Html>
          )}
        </group>
      ))}

      {/* kSZ legend */}
      {showLabels && (
        <Html position={[-HALF_BOX + 1, HALF_BOX - 1, 0]} center>
          <div className="bg-slate-900/70 border border-orange-400 px-2 py-1 rounded">
            <div className="text-orange-400 text-[10px] font-bold">kSZ Void Outflows</div>
            <div className="text-orange-300 text-[9px]">Planck + DESIVAST stacking</div>
            <div className="text-orange-200 text-[8px]">v_max = 265 km/s</div>
          </div>
        </Html>
      )}
    </group>
  );
};

// =============================================================================
// GW190521 GRAVITATIONAL WAVE SIMULATION
// =============================================================================

interface GWSimulationProps {
  isRunning: boolean;
  onProgressUpdate: (progress: number, phase: number, waveRadius: number) => void;
}

const GW190521Simulation: React.FC<GWSimulationProps> = ({ isRunning, onProgressUpdate }) => {
  const startTimeRef = useRef<number>(0);
  const waveRadiusRef = useRef(0);
  const groupRef = useRef<THREE.Group>(null);

  // T³/Z₂ topology parameters (scaled for visualization: 1 unit = 1 Gpc)
  const L_c = 20.6; // Fundamental domain size in Gpc
  const halfL = L_c / 2; // ±10.3 Gpc boundaries

  // Primary epicenter position
  const epicenter: [number, number, number] = useMemo(() => [
    GW190521_EVENT.position.x,
    GW190521_EVENT.position.y,
    GW190521_EVENT.position.z
  ], []);

  // T³ periodic images - the 6 nearest face images
  const t3Images = useMemo(() => {
    const images: { pos: [number, number, number]; color: string; label: string; delay: number }[] = [];
    const shifts = [
      [L_c, 0, 0], [-L_c, 0, 0],
      [0, L_c, 0], [0, -L_c, 0],
      [0, 0, L_c], [0, 0, -L_c],
    ];

    for (const [dx, dy, dz] of shifts) {
      const pos: [number, number, number] = [
        epicenter[0] + dx,
        epicenter[1] + dy,
        epicenter[2] + dz
      ];
      // Distance from this image to Earth (origin)
      const dist = Math.sqrt(pos[0] * pos[0] + pos[1] * pos[1] + pos[2] * pos[2]);
      images.push({
        pos,
        color: '#00ccff', // Cyan for T³ wrapped images
        label: `T³ wrap`,
        delay: dist - GW190521_EVENT.distance_gpc // Delay relative to direct path
      });
    }
    return images;
  }, [epicenter]);

  // Z₂ antipodal image
  const z2Image = useMemo(() => ({
    pos: [-epicenter[0], -epicenter[1], -epicenter[2]] as [number, number, number],
    color: '#cc00ff', // Purple for Z₂ image
    label: 'Z₂ image',
    dist: Math.sqrt(epicenter[0] * epicenter[0] + epicenter[1] * epicenter[1] + epicenter[2] * epicenter[2])
  }), [epicenter]);

  // Animation phases - extended for topology visualization
  const phases = useMemo(() => [
    { name: 'Merger', duration: 2, description: 'BH merger at 5.3 Gpc' },
    { name: 'Direct Wave', duration: 6, description: 'Primary GW expands in T³' },
    { name: 'Boundary Cross', duration: 4, description: 'Wave wraps through T³ faces' },
    { name: 'Multi-Path', duration: 6, description: 'Wrapped copies converge on Earth' },
    { name: 'Z₂ Image', duration: 4, description: 'Antipodal signal arrives' },
  ], []);

  const totalDuration = useMemo(() => phases.reduce((sum, p) => sum + p.duration, 0), [phases]);

  useFrame((state) => {
    if (!isRunning) {
      if (startTimeRef.current !== 0) {
        startTimeRef.current = 0;
        waveRadiusRef.current = 0;
        onProgressUpdate(0, 0, 0);
      }
      return;
    }

    if (startTimeRef.current === 0) {
      startTimeRef.current = state.clock.elapsedTime;
    }

    const elapsed = state.clock.elapsedTime - startTimeRef.current;
    const progress = Math.min(elapsed / totalDuration, 1);

    // Determine current phase
    let accTime = 0;
    let currentPhase = 0;
    for (let i = 0; i < phases.length; i++) {
      accTime += phases[i].duration;
      if (elapsed < accTime) {
        currentPhase = i;
        break;
      }
      currentPhase = i;
    }

    // Wave expands continuously - travels full domain and beyond
    const maxRadius = L_c * 1.5; // Enough to wrap around
    const newRadius = progress * maxRadius;
    waveRadiusRef.current = newRadius;

    onProgressUpdate(progress, currentPhase, newRadius);
  });

  if (!isRunning) return null;

  const waveRadius = waveRadiusRef.current;

  // Calculate which wrapped waves are "active" based on distance traveled
  const activeT3Waves = t3Images.filter(img => {
    // Wave from this image reaches Earth when radius equals image distance
    const imgDist = Math.sqrt(img.pos[0] ** 2 + img.pos[1] ** 2 + img.pos[2] ** 2);
    return waveRadius > 0; // All emit simultaneously, arrive at different times
  });

  return (
    <group ref={groupRef}>
      {/* Fundamental Domain outline - the T³ cube */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_c, L_c, L_c)]} />
        <lineBasicMaterial color="#334455" transparent opacity={0.5} />
      </lineSegments>

      {/* Face labels showing T³ identification */}
      {[
        { pos: [halfL, 0, 0], label: '+X ↔ -X' },
        { pos: [0, halfL, 0], label: '+Y ↔ -Y' },
        { pos: [0, 0, halfL], label: '+Z ↔ -Z' },
      ].map((face, i) => (
        <Html key={i} position={face.pos as [number, number, number]} center>
          <div className="text-slate-500 text-[8px] font-mono opacity-60">{face.label}</div>
        </Html>
      ))}

      {/* PRIMARY EPICENTER - the actual GW190521 location */}
      <mesh position={epicenter}>
        <sphereGeometry args={[0.2, 16, 16]} />
        <meshBasicMaterial color="#ff6600" />
      </mesh>
      <mesh position={epicenter}>
        <sphereGeometry args={[0.35, 16, 16]} />
        <meshBasicMaterial color="#ff6600" transparent opacity={0.3} />
      </mesh>

      {/* PRIMARY WAVE FRONT - expanding sphere */}
      <mesh position={epicenter}>
        <sphereGeometry args={[Math.max(waveRadius, 0.01), 32, 24]} />
        <meshBasicMaterial
          color="#ffaa00"
          transparent
          opacity={0.15}
          wireframe
        />
      </mesh>
      {/* Solid shell at wave front */}
      <mesh position={epicenter}>
        <sphereGeometry args={[Math.max(waveRadius, 0.01), 32, 24]} />
        <meshBasicMaterial
          color="#ffcc00"
          transparent
          opacity={0.08}
          side={THREE.BackSide}
        />
      </mesh>

      {/* T³ WRAPPED IMAGES - waves entering from opposite faces */}
      {activeT3Waves.map((img, i) => {
        // This image's wave also expands at the same rate
        // It "appears" when the primary wave would cross the boundary
        const imgDist = Math.sqrt(img.pos[0] ** 2 + img.pos[1] ** 2 + img.pos[2] ** 2);
        const boundaryDist = halfL - Math.max(Math.abs(epicenter[0]), Math.abs(epicenter[1]), Math.abs(epicenter[2]));

        // Wave from this image becomes visible when primary wave hits boundary
        if (waveRadius < boundaryDist) return null;

        // This wrapped wave has traveled: waveRadius - boundaryDist
        const wrappedRadius = Math.max(0, waveRadius - boundaryDist);
        if (wrappedRadius <= 0) return null;

        return (
          <group key={i}>
            {/* Wrapped wave marker at face boundary */}
            <mesh position={img.pos}>
              <sphereGeometry args={[0.12, 12, 12]} />
              <meshBasicMaterial color={img.color} transparent opacity={0.6} />
            </mesh>
            {/* Wrapped wave front expanding from image position */}
            <mesh position={img.pos}>
              <sphereGeometry args={[Math.max(wrappedRadius, 0.01), 24, 16]} />
              <meshBasicMaterial
                color={img.color}
                transparent
                opacity={0.1}
                wireframe
              />
            </mesh>
          </group>
        );
      })}

      {/* Z₂ ANTIPODAL IMAGE */}
      {waveRadius > 3 && (
        <group>
          <mesh position={z2Image.pos}>
            <sphereGeometry args={[0.15, 16, 16]} />
            <meshBasicMaterial color={z2Image.color} />
          </mesh>
          <mesh position={z2Image.pos}>
            <sphereGeometry args={[Math.max(waveRadius * 0.8, 0.01), 24, 16]} />
            <meshBasicMaterial
              color={z2Image.color}
              transparent
              opacity={0.08}
              wireframe
            />
          </mesh>
          <Html position={[z2Image.pos[0], z2Image.pos[1] + 0.5, z2Image.pos[2]]} center>
            <div className="text-purple-400 text-[9px] font-mono bg-black/80 px-1 rounded">
              Z₂ IMAGE (parity-flipped)
            </div>
          </Html>
        </group>
      )}

      {/* Earth marker at origin */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.12, 16, 16]} />
        <meshBasicMaterial color="#00ff00" />
      </mesh>
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.2, 16, 16]} />
        <meshBasicMaterial color="#00ff00" transparent opacity={0.3} />
      </mesh>

      {/* Detection indicator when primary wave reaches Earth */}
      {waveRadius >= GW190521_EVENT.distance_gpc && (
        <mesh position={[0, 0, 0]}>
          <ringGeometry args={[0.3, 0.5, 32]} />
          <meshBasicMaterial
            color="#00ff00"
            transparent
            opacity={0.5 + 0.3 * Math.sin(waveRadius * 5)}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}

      <Html position={[0, 0.4, 0]} center>
        <div className="text-green-400 text-[10px] font-mono bg-black/80 px-1 rounded">
          EARTH (LIGO)
        </div>
      </Html>

      {/* Epicenter label */}
      <Html position={[epicenter[0], epicenter[1] + 0.5, epicenter[2]]} center>
        <div className="text-orange-400 text-[10px] font-mono bg-black/80 px-1 rounded">
          GW190521 PRIMARY<br/>
          <span className="text-[8px] opacity-70">85+66 M☉ → 142 M☉</span>
        </div>
      </Html>

      {/* Geodesic path indicator from epicenter to Earth */}
      <Line
        points={[epicenter, [0, 0, 0]]}
        color="#ffaa00"
        lineWidth={1}
        dashed
        dashSize={0.3}
        dashScale={1}
        opacity={0.4}
        transparent
      />

      {/* Legend */}
      <Html position={[-halfL + 1, halfL - 1, halfL]} center>
        <div className="text-[8px] font-mono bg-black/90 p-2 rounded border border-slate-700">
          <div className="text-white mb-1 font-bold">T³/Z₂ GW Propagation</div>
          <div className="text-orange-400">● Primary wave</div>
          <div className="text-cyan-400">● T³ wrapped copies</div>
          <div className="text-purple-400">● Z₂ antipodal image</div>
          <div className="text-slate-500 mt-1">L_c = {L_c} Gpc</div>
        </div>
      </Html>
    </group>
  );
};

// GW190521 HUD Overlay (rendered outside Canvas) - T³/Z₂ version
const GWSimulationHUD: React.FC<{
  isRunning: boolean;
  progress: number;
  phase: number;
  waveRadius: number;
}> = ({ isRunning, progress, phase, waveRadius }) => {
  if (!isRunning) return null;

  const L_c = 20.6; // Fundamental domain
  const directDist = GW190521_EVENT.distance_gpc;
  const z2Dist = directDist; // Z₂ image at same distance (antipodal)
  const wrappedDist = L_c - directDist; // Shortest wrapped path ~15.3 Gpc

  const phases = [
    { name: 'Merger', description: 'BH merger emits GW in T³/Z₂ spacetime' },
    { name: 'Direct Wave', description: 'Primary wave expands through fundamental domain' },
    { name: 'Boundary Cross', description: 'Wave wraps through T³ face identifications' },
    { name: 'Multi-Path', description: 'Multiple geodesic copies converge on Earth' },
    { name: 'Z₂ Image', description: 'Antipodal parity-flipped signal arrives' },
  ];

  const currentPhase = phases[phase] || phases[0];
  const distanceToEarth = Math.max(0, directDist - waveRadius);

  // Calculate arrival status for each path
  const primaryArrived = waveRadius >= directDist;
  const z2Arrived = waveRadius >= z2Dist * 0.8; // Z₂ wave starts later
  const wrappedProgress = Math.max(0, waveRadius - (L_c / 2 - 5)); // Wrapped wave starts at boundary

  return (
    <div className="absolute top-4 right-4 z-20 font-mono text-sm max-w-xs">
      {/* T³/Z₂ Topology Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 border border-slate-600 rounded-lg p-3 mb-2">
        <div className="text-white font-bold text-sm mb-1">T³/Z₂ GRAVITATIONAL WAVE</div>
        <div className="text-slate-400 text-[10px]">
          Proper propagation through compact topology
        </div>
      </div>

      {/* Event info */}
      <div className="bg-black/95 border border-orange-500/50 rounded-lg p-3 mb-2 shadow-[0_0_15px_rgba(249,115,22,0.2)]">
        <div className="text-orange-400 font-bold mb-1">
          {GW190521_EVENT.name}
        </div>
        <div className="text-slate-400 text-[10px] space-y-0.5">
          <div>{GW190521_EVENT.mass1_solar} + {GW190521_EVENT.mass2_solar} M☉ → {GW190521_EVENT.finalMass_solar} M☉</div>
          <div>First intermediate-mass BH detection</div>
        </div>
      </div>

      {/* Phase info */}
      <div className="bg-black/95 border border-yellow-500/50 rounded-lg p-3 mb-2">
        <div className="text-yellow-400 font-bold text-xs mb-1">
          Phase {phase + 1}/5: {currentPhase.name}
        </div>
        <div className="text-slate-300 text-[10px] mb-2">
          {currentPhase.description}
        </div>
        <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-yellow-500 to-orange-500 transition-all"
            style={{ width: `${progress * 100}%` }}
          />
        </div>
      </div>

      {/* Multi-path geodesics */}
      <div className="bg-black/95 border border-cyan-500/50 rounded-lg p-3 mb-2">
        <div className="text-cyan-400 font-bold text-xs mb-2">GEODESIC PATHS</div>
        <div className="space-y-2 text-[10px]">
          {/* Primary path */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-orange-500"></span>
              <span className="text-slate-300">Primary</span>
            </div>
            <span className={primaryArrived ? "text-green-400" : "text-orange-300"}>
              {primaryArrived ? "✓ DETECTED" : `${distanceToEarth.toFixed(1)} Gpc`}
            </span>
          </div>

          {/* Z₂ path */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-purple-500"></span>
              <span className="text-slate-300">Z₂ antipodal</span>
            </div>
            <span className={z2Arrived ? "text-green-400" : "text-purple-300"}>
              {z2Arrived ? "✓ DETECTED" : `${z2Dist.toFixed(1)} Gpc`}
            </span>
          </div>

          {/* Wrapped path */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
              <span className="text-slate-300">T³ wrapped</span>
            </div>
            <span className="text-cyan-300">
              {wrappedProgress > wrappedDist ? "✓ DETECTED" : `${wrappedDist.toFixed(1)} Gpc`}
            </span>
          </div>
        </div>
      </div>

      {/* Topology parameters */}
      <div className="bg-black/95 border border-slate-600 rounded-lg p-3">
        <div className="text-slate-400 font-bold text-xs mb-2">TOPOLOGY</div>
        <div className="grid grid-cols-2 gap-1 text-[10px]">
          <div className="text-slate-500">L_c:</div>
          <div className="text-slate-300">{L_c} Gpc</div>

          <div className="text-slate-500">Wave front:</div>
          <div className="text-cyan-300">{waveRadius.toFixed(2)} Gpc</div>

          <div className="text-slate-500">Domain:</div>
          <div className="text-slate-300">T³/Z₂</div>
        </div>
      </div>
    </div>
  );
};

const FundamentalDomainBox: React.FC = () => {
  const h = HALF_BOX;
  const edges: [[number, number, number], [number, number, number]][] = [
    [[-h, -h, -h], [h, -h, -h]], [[h, -h, -h], [h, h, -h]], [[h, h, -h], [-h, h, -h]], [[-h, h, -h], [-h, -h, -h]],
    [[-h, -h, h], [h, -h, h]], [[h, -h, h], [h, h, h]], [[h, h, h], [-h, h, h]], [[-h, h, h], [-h, -h, h]],
    [[-h, -h, -h], [-h, -h, h]], [[h, -h, -h], [h, -h, h]], [[h, h, -h], [h, h, h]], [[-h, h, -h], [-h, h, h]],
  ];
  return (
    <group>
      {edges.map((edge, i) => <Line key={i} points={edge} color="#00ffff" lineWidth={1.5} transparent opacity={0.3} />)}
      <Text position={[h + 0.5, 0, 0]} fontSize={0.5} color="#00ffff" anchorX="left">+10.3 Gpc</Text>
      <Text position={[-h - 0.5, 0, 0]} fontSize={0.5} color="#00ffff" anchorX="right">-10.3 Gpc</Text>
    </group>
  );
};

// =============================================================================
// SCALE INDICATOR
// =============================================================================

const ScaleIndicator: React.FC<{ cameraDistance: number }> = ({ cameraDistance }) => {
  // Scale thresholds based on proper astronomical distances:
  // - Solar System: < 1e-6 scene units (~100 AU = 1e-6 Gpc)
  // - Milky Way: < 1e-4 scene units (~100 kpc = 1e-4 Gpc)
  // - Local Group: < 0.01 scene units (~10 Mpc = 0.01 Gpc)
  // - Cosmic Web: < 1 scene unit (~1 Gpc)
  // - Full Domain: > 1 scene unit

  let scaleName = '';
  let scaleColor = '';
  let scaleValue = '';

  if (cameraDistance < 1e-6) {
    scaleName = 'Solar System';
    scaleColor = 'text-yellow-400';
    const au = cameraDistance / 1e-8;
    scaleValue = au < 1 ? `${(au * 149.6).toFixed(0)} million km` : `${au.toFixed(1)} AU`;
  } else if (cameraDistance < 1e-4) {
    scaleName = 'Milky Way';
    scaleColor = 'text-blue-400';
    const kpc = cameraDistance / 1e-6;
    scaleValue = `${kpc.toFixed(1)} kpc`;
  } else if (cameraDistance < 0.005) {
    scaleName = 'Local Group';
    scaleColor = 'text-green-400';
    const mpc = cameraDistance * 1000;
    scaleValue = `${mpc.toFixed(1)} Mpc`;
  } else if (cameraDistance < 0.5) {
    scaleName = 'Cosmic Web';
    scaleColor = 'text-orange-400';
    const mpc = cameraDistance * 1000;
    scaleValue = `${mpc.toFixed(0)} Mpc`;
  } else {
    scaleName = 'Full Domain';
    scaleColor = 'text-cyan-400';
    scaleValue = `${cameraDistance.toFixed(1)} Gpc`;
  }

  return (
    <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-black/85 px-4 py-2 rounded-lg border border-slate-600 z-20">
      <div className={`font-mono text-sm ${scaleColor}`}>{scaleName}</div>
      <div className="font-mono text-xs text-slate-400 text-center">{scaleValue}</div>
    </div>
  );
};

// =============================================================================
// FILTER PANEL
// =============================================================================

interface FilterPanelProps {
  filters: Record<string, boolean>;
  setFilters: React.Dispatch<React.SetStateAction<Record<string, boolean>>>;
  isRotating: boolean;
  setIsRotating: (r: boolean) => void;
  showLabels: boolean;
  setShowLabels: (s: boolean) => void;
  isTourRunning: boolean;
  onStartTour: () => void;
  onStopTour: () => void;
  // GW190521 Simulation
  isGWRunning: boolean;
  onStartGW: () => void;
  onStopGW: () => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filters, setFilters, isRotating, setIsRotating, showLabels, setShowLabels,
  isTourRunning, onStartTour, onStopTour, isGWRunning, onStartGW, onStopGW
}) => {
  const toggleFilter = (key: string) => setFilters(prev => ({ ...prev, [key]: !prev[key] }));

  const filterItems = [
    { key: 'solarSystem', label: 'Solar System', color: '#ffdd00' },
    { key: 'milkyWay', label: 'Milky Way', color: '#6699ff' },
    { key: 'localGroup', label: 'Local Group', color: '#00ff00' },
    { key: 'structures', label: 'Clusters & Structures', color: '#ff6600' },
    { key: 'highZ', label: 'High-z (JWST)', color: '#ff00ff' },
    { key: 'survey', label: 'DESI/SDSS Survey', color: '#4A90D9' },
    { key: 'lymanAlpha', label: 'Lyman-α Forest', color: '#ff88ff' },
    { key: 'baoSpheres', label: 'BAO Spheres (150 Mpc)', color: '#00aaff' },
    { key: 'kszVectors', label: 'kSZ Void Outflows', color: '#ff8800' },
  ];

  return (
    <div className="absolute top-16 left-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-[260px]">
      <h3 className="text-white font-bold mb-3">Controls</h3>

      {/* Cinematic Tour Button */}
      <button
        onClick={isTourRunning ? onStopTour : onStartTour}
        disabled={isGWRunning}
        className={`w-full mb-2 px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
          isTourRunning
            ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
            : isGWRunning
            ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
            : 'bg-cyan-900/50 text-cyan-400 border-cyan-500 hover:bg-cyan-900/80'
        }`}
      >
        {isTourRunning ? '■ STOP' : '▶ CINEMATIC TOUR'}
      </button>

      {/* GW190521 Simulation Button */}
      <button
        onClick={isGWRunning ? onStopGW : onStartGW}
        disabled={isTourRunning}
        className={`w-full mb-4 px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
          isGWRunning
            ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
            : isTourRunning
            ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
            : 'bg-orange-900/50 text-orange-400 border-orange-500 hover:bg-orange-900/80'
        }`}
      >
        {isGWRunning ? '■ STOP GW' : '▶ GW190521 WAVE'}
      </button>

      <div className="mb-3 pb-3 border-b border-slate-700 space-y-2">
        <label className="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" checked={isRotating} onChange={() => setIsRotating(!isRotating)} disabled={isTourRunning} className="w-4 h-4 accent-cyan-500" />
          <span className={`text-sm ${isTourRunning ? 'text-slate-500' : 'text-cyan-400'}`}>Auto-rotate</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" checked={showLabels} onChange={() => setShowLabels(!showLabels)} className="w-4 h-4 accent-cyan-500" />
          <span className="text-cyan-400 text-sm">Show labels</span>
        </label>
      </div>

      <div className="space-y-1">
        {filterItems.map(({ key, label, color }) => (
          <label key={key} className="flex items-center gap-2 cursor-pointer hover:bg-slate-800 p-1 rounded">
            <input type="checkbox" checked={filters[key]} onChange={() => toggleFilter(key)} className="w-3 h-3 accent-blue-500" />
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-white text-xs">{label}</span>
          </label>
        ))}
      </div>

      <div className="mt-3 pt-2 border-t border-slate-700 text-slate-500 text-[10px]">
        Scroll to zoom from planets to 20.6 Gpc
      </div>
    </div>
  );
};

// =============================================================================
// TOPOLOGICAL CAMERA ENGINE (Directive TTT)
// Handles T³ boundary wrapping and Z₂ parity inversions
// =============================================================================

// Apply T³ modulo wrap to a position
const wrapT3 = (pos: THREE.Vector3): { wrapped: THREE.Vector3; didWrap: boolean; axis: string | null } => {
  const wrapped = pos.clone();
  let didWrap = false;
  let axis: string | null = null;

  if (wrapped.x > HALF_BOX) { wrapped.x -= L_C_GPC; didWrap = true; axis = 'x'; }
  if (wrapped.x < -HALF_BOX) { wrapped.x += L_C_GPC; didWrap = true; axis = 'x'; }
  if (wrapped.y > HALF_BOX) { wrapped.y -= L_C_GPC; didWrap = true; axis = 'y'; }
  if (wrapped.y < -HALF_BOX) { wrapped.y += L_C_GPC; didWrap = true; axis = 'y'; }
  if (wrapped.z > HALF_BOX) { wrapped.z -= L_C_GPC; didWrap = true; axis = 'z'; }
  if (wrapped.z < -HALF_BOX) { wrapped.z += L_C_GPC; didWrap = true; axis = 'z'; }

  return { wrapped, didWrap, axis };
};

// Apply Z₂ parity inversion
const applyZ2 = (pos: THREE.Vector3): THREE.Vector3 => {
  return pos.clone().multiplyScalar(-1);
};

// Calculate shortest geodesic on T³ between two points
const geodesicT3 = (from: THREE.Vector3, to: THREE.Vector3): THREE.Vector3 => {
  const delta = to.clone().sub(from);

  // For each axis, check if wrapping is shorter
  if (Math.abs(delta.x) > HALF_BOX) {
    delta.x = delta.x > 0 ? delta.x - L_C_GPC : delta.x + L_C_GPC;
  }
  if (Math.abs(delta.y) > HALF_BOX) {
    delta.y = delta.y > 0 ? delta.y - L_C_GPC : delta.y + L_C_GPC;
  }
  if (Math.abs(delta.z) > HALF_BOX) {
    delta.z = delta.z > 0 ? delta.z - L_C_GPC : delta.z + L_C_GPC;
  }

  return from.clone().add(delta);
};

// Boundary Grid Component - shows when approaching boundary
const BoundaryGrid: React.FC<{ cameraPos: THREE.Vector3; approaching: boolean }> = ({ cameraPos, approaching }) => {
  if (!approaching) return null;

  // Determine which boundary we're approaching
  const grids: JSX.Element[] = [];
  const threshold = 2; // Start showing grid 2 Gpc from boundary

  const axes: Array<{ axis: 'x' | 'y' | 'z'; sign: 1 | -1 }> = [
    { axis: 'x', sign: 1 }, { axis: 'x', sign: -1 },
    { axis: 'y', sign: 1 }, { axis: 'y', sign: -1 },
    { axis: 'z', sign: 1 }, { axis: 'z', sign: -1 },
  ];

  for (const { axis, sign } of axes) {
    const dist = sign * (sign === 1 ? HALF_BOX - cameraPos[axis] : cameraPos[axis] + HALF_BOX);
    if (dist < threshold && dist > 0) {
      const opacity = 1 - (dist / threshold);
      const position: [number, number, number] = [0, 0, 0];
      const rotation: [number, number, number] = [0, 0, 0];
      position[axis === 'x' ? 0 : axis === 'y' ? 1 : 2] = sign * HALF_BOX;
      if (axis === 'x') rotation[1] = Math.PI / 2;
      if (axis === 'y') rotation[0] = Math.PI / 2;

      grids.push(
        <group key={`${axis}${sign}`} position={position} rotation={rotation}>
          <gridHelper
            args={[L_C_GPC, 20, '#00ffff', '#004444']}
            rotation={[Math.PI / 2, 0, 0]}
          />
          <mesh>
            <planeGeometry args={[L_C_GPC, L_C_GPC]} />
            <meshBasicMaterial
              color="#00ffff"
              transparent
              opacity={opacity * 0.1}
              side={THREE.DoubleSide}
            />
          </mesh>
        </group>
      );
    }
  }

  return <>{grids}</>;
};

const CinematicCamera: React.FC<{
  isTourRunning: boolean;
  onTourComplete: () => void;
  onWaypointChange: (text: string) => void;
  onBoundaryCross: (axis: string) => void;
  onParityFlip: () => void;
  controlsRef: React.RefObject<any>;
}> = ({ isTourRunning, onTourComplete, onWaypointChange, onBoundaryCross, onParityFlip, controlsRef }) => {
  const { camera } = useThree();
  const lookAtTarget = useRef(new THREE.Vector3());
  const currentSegment = useRef(0);
  const segmentProgress = useRef(0);
  const isAnimating = useRef(false);

  // Use refs to avoid stale closure in useFrame
  const onBoundaryCrossRef = useRef(onBoundaryCross);
  const onParityFlipRef = useRef(onParityFlip);
  const onWaypointChangeRef = useRef(onWaypointChange);
  const onTourCompleteRef = useRef(onTourComplete);

  // Keep refs up to date
  useEffect(() => {
    onBoundaryCrossRef.current = onBoundaryCross;
    onParityFlipRef.current = onParityFlip;
    onWaypointChangeRef.current = onWaypointChange;
    onTourCompleteRef.current = onTourComplete;
  });

  useEffect(() => {
    if (!isTourRunning) {
      currentSegment.current = 0;
      segmentProgress.current = 0;
      isAnimating.current = false;
      if (controlsRef.current) controlsRef.current.enabled = true;
      return;
    }

    if (controlsRef.current) controlsRef.current.enabled = false;

    // Initialize at first waypoint
    camera.position.copy(TOPOLOGY_TOUR[0].position);
    lookAtTarget.current.copy(TOPOLOGY_TOUR[0].lookAt);
    onWaypointChange(TOPOLOGY_TOUR[0].text);
    currentSegment.current = 0;
    isAnimating.current = true;

    return () => {
      isAnimating.current = false;
      if (controlsRef.current) controlsRef.current.enabled = true;
    };
  }, [isTourRunning, camera, controlsRef, onWaypointChange]);

  useFrame((state, delta) => {
    if (!isTourRunning || !isAnimating.current) return;

    const segmentIndex = currentSegment.current;
    if (segmentIndex >= TOPOLOGY_TOUR.length - 1) {
      onTourCompleteRef.current();
      isAnimating.current = false;
      if (controlsRef.current) controlsRef.current.enabled = true;
      return;
    }

    const fromWaypoint = TOPOLOGY_TOUR[segmentIndex];
    const toWaypoint = TOPOLOGY_TOUR[segmentIndex + 1];

    // Handle boundary_cross type - instant teleport
    if (toWaypoint.type === 'boundary_cross' || toWaypoint.type === 'z2_demo') {
      const teleportSpeed = 2; // Slightly slower so user sees it
      segmentProgress.current += delta * teleportSpeed;

      if (segmentProgress.current >= 1) {
        // Execute the teleport
        camera.position.copy(toWaypoint.position);
        lookAtTarget.current.copy(toWaypoint.lookAt);

        // Trigger effects using refs (avoids stale closure)
        if (toWaypoint.type === 'boundary_cross' && toWaypoint.boundaryAxis) {
          console.log('BOUNDARY CROSS TRIGGERED:', toWaypoint.boundaryAxis);
          onBoundaryCrossRef.current(toWaypoint.boundaryAxis);
        }
        if (toWaypoint.type === 'z2_demo') {
          console.log('PARITY FLIP TRIGGERED');
          onParityFlipRef.current();
        }

        onWaypointChangeRef.current(toWaypoint.text);
        currentSegment.current++;
        segmentProgress.current = 0;
      }
    } else {
      // Normal smooth animation between waypoints
      const speed = 1 / toWaypoint.duration;
      segmentProgress.current += delta * speed;

      // Smooth easing
      const t = Math.min(segmentProgress.current, 1);
      const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

      // Interpolate position - use geodesic path on T³
      const targetPos = geodesicT3(fromWaypoint.position, toWaypoint.position);
      camera.position.lerpVectors(fromWaypoint.position, targetPos, eased);

      // Apply T³ wrap if we crossed a boundary during interpolation
      const { wrapped, didWrap, axis } = wrapT3(camera.position);
      if (didWrap && axis) {
        camera.position.copy(wrapped);
        console.log('WRAP DURING INTERPOLATION:', axis);
        onBoundaryCrossRef.current(axis);
      }

      // Interpolate lookAt
      lookAtTarget.current.lerpVectors(fromWaypoint.lookAt, toWaypoint.lookAt, eased);

      if (segmentProgress.current >= 1) {
        onWaypointChangeRef.current(toWaypoint.text);
        currentSegment.current++;
        segmentProgress.current = 0;
      }
    }

    // Apply look at
    camera.lookAt(lookAtTarget.current);
    if (controlsRef.current) {
      controlsRef.current.target.copy(lookAtTarget.current);
    }
  });

  return <BoundaryGrid cameraPos={camera.position} approaching={isTourRunning} />;
};

// =============================================================================
// BOUNDARY RUPTURE OVERLAY (Directive VVV)
// Full-screen flash when crossing T³ boundaries or Z₂ parity flip
// =============================================================================

const BoundaryRuptureOverlay: React.FC<{
  isActive: boolean;
  axis: string | null;
  isParityFlip: boolean;
}> = ({ isActive, axis, isParityFlip }) => {
  if (!isActive) return null;

  const color = isParityFlip ? '#a855f7' : '#22d3ee';
  const bgColor = isParityFlip ? 'rgba(168, 85, 247, 0.4)' : 'rgba(34, 211, 238, 0.4)';

  return (
    <div
      className="absolute inset-0 pointer-events-none flex items-center justify-center"
      style={{ zIndex: 9999 }}
    >
      {/* Full screen flash */}
      <div
        className="absolute inset-0"
        style={{
          background: `radial-gradient(circle at center, ${bgColor} 0%, transparent 70%)`,
          animation: 'rupture-flash 1.5s ease-out forwards',
        }}
      />

      {/* Scan lines effect */}
      <div
        className="absolute inset-0"
        style={{
          background: `repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            ${color}22 2px,
            ${color}22 4px
          )`,
          animation: 'scan-lines 0.1s linear infinite',
        }}
      />

      {/* Main text overlay */}
      <div
        className="text-center relative"
        style={{
          animation: 'rupture-text 1.5s ease-out forwards',
        }}
      >
        <div
          className={`text-5xl md:text-6xl font-black tracking-widest mb-4 ${
            isParityFlip ? 'text-purple-300' : 'text-cyan-300'
          }`}
          style={{
            textShadow: `0 0 30px ${color}, 0 0 60px ${color}, 0 0 90px ${color}`,
            letterSpacing: '0.2em',
          }}
        >
          {isParityFlip ? '⟲ Z₂ PARITY FLIP' : '⚡ T³ BOUNDARY CROSSED'}
        </div>
        <div
          className="text-2xl md:text-3xl text-white font-mono font-bold"
          style={{
            textShadow: `0 0 20px ${color}`,
          }}
        >
          {isParityFlip
            ? 'COORDINATES INVERTED: p → -p'
            : `${axis?.toUpperCase()} AXIS: +${HALF_BOX.toFixed(1)} ↔ -${HALF_BOX.toFixed(1)} Gpc`}
        </div>
        <div className="mt-4 text-lg text-slate-300 font-mono">
          {isParityFlip
            ? 'Same physical location, opposite orientation'
            : 'Continuous geodesic through periodic boundary'}
        </div>
      </div>

      {/* Corner brackets */}
      {[
        { top: 0, left: 0, borderTop: `4px solid ${color}`, borderLeft: `4px solid ${color}` },
        { top: 0, right: 0, borderTop: `4px solid ${color}`, borderRight: `4px solid ${color}` },
        { bottom: 0, left: 0, borderBottom: `4px solid ${color}`, borderLeft: `4px solid ${color}` },
        { bottom: 0, right: 0, borderBottom: `4px solid ${color}`, borderRight: `4px solid ${color}` },
      ].map((style, i) => (
        <div
          key={i}
          className="absolute w-20 h-20"
          style={{
            ...style,
            boxShadow: `0 0 20px ${color}`,
          }}
        />
      ))}

      {/* Edge glow */}
      <div
        className="absolute inset-0"
        style={{
          border: `3px solid ${color}`,
          boxShadow: `inset 0 0 100px ${color}40, 0 0 50px ${color}40`,
        }}
      />

      {/* Inline keyframe styles */}
      <style>{`
        @keyframes rupture-flash {
          0% { opacity: 1; }
          100% { opacity: 0; }
        }
        @keyframes rupture-text {
          0% { transform: scale(1.2); opacity: 0; }
          20% { transform: scale(1); opacity: 1; }
          80% { transform: scale(1); opacity: 1; }
          100% { transform: scale(0.9); opacity: 0; }
        }
        @keyframes scan-lines {
          0% { transform: translateY(0); }
          100% { transform: translateY(4px); }
        }
      `}</style>
    </div>
  );
};

// =============================================================================
// MULTI-SCALE UNIVERSE
// =============================================================================

const MultiScaleUniverse: React.FC<{
  filters: Record<string, boolean>;
  isRotating: boolean;
  showLabels: boolean;
  isTourRunning: boolean;
  onCameraDistanceChange: (d: number) => void;
  // GW Simulation props
  isGWRunning: boolean;
  onGWProgressUpdate: (progress: number, phase: number, waveRadius: number) => void;
}> = ({ filters, isRotating, showLabels, isTourRunning, onCameraDistanceChange, isGWRunning, onGWProgressUpdate }) => {
  const groupRef = useRef<THREE.Group>(null);
  const { camera } = useThree();
  const [time, setTime] = useState(0);
  const [camDist, setCamDist] = useState(3);

  useFrame((state) => {
    if (groupRef.current && isRotating && !isTourRunning && !isGWRunning) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.02;
    }

    // Update camera distance for LOD
    const dist = camera.position.length();
    onCameraDistanceChange(dist);
    setCamDist(dist);

    // Update time for planet orbits
    setTime(state.clock.elapsedTime * 50);
  });

  return (
    <group ref={groupRef}>
      {/* Always render the domain box and vertices at cosmic scale */}
      <FundamentalDomainBox />
      <Z2Vertices showLabels={showLabels} />

      {/* Solar System - visible when zoomed in */}
      {filters.solarSystem && <SolarSystem showLabels={showLabels} time={time} cameraDistance={camDist} />}

      {/* Milky Way - visible at galactic scale */}
      {filters.milkyWay && <MilkyWayGalaxy showLabels={showLabels} cameraDistance={camDist} />}

      {/* Local Group and beyond */}
      {filters.localGroup && <LocalGroupGalaxies showLabels={showLabels} />}
      {filters.structures && <MajorStructures showLabels={showLabels} />}
      {filters.highZ && <HighZGalaxies showLabels={showLabels} />}
      {filters.survey && <SurveyGalaxies />}

      {/* New cosmological layers */}
      {filters.lymanAlpha && <LymanAlphaForest showLabels={showLabels} />}
      {filters.baoSpheres && <BAOSpheres showLabels={showLabels} />}
      {filters.kszVectors && <KSZVelocityVectors showLabels={showLabels} />}

      {/* GW190521 Gravitational Wave Simulation */}
      <GW190521Simulation isRunning={isGWRunning} onProgressUpdate={onGWProgressUpdate} />
    </group>
  );
};

// =============================================================================
// SCENE
// =============================================================================

const Scene: React.FC<{
  filters: Record<string, boolean>;
  isRotating: boolean;
  showLabels: boolean;
  isTourRunning: boolean;
  onTourComplete: () => void;
  onWaypointChange: (text: string) => void;
  onCameraDistanceChange: (d: number) => void;
  onBoundaryCross: (axis: string) => void;
  onParityFlip: () => void;
  // GW Simulation props
  isGWRunning: boolean;
  onGWProgressUpdate: (progress: number, phase: number, waveRadius: number) => void;
}> = ({ filters, isRotating, showLabels, isTourRunning, onTourComplete, onWaypointChange, onCameraDistanceChange, onBoundaryCross, onParityFlip, isGWRunning, onGWProgressUpdate }) => {
  const controlsRef = useRef<any>(null);

  return (
    <>
      <color attach="background" args={['#030308']} />
      <Stars radius={100} depth={50} count={3000} factor={4} fade />
      <ambientLight intensity={0.4} />

      <MultiScaleUniverse
        filters={filters}
        isRotating={isRotating}
        showLabels={showLabels}
        isTourRunning={isTourRunning}
        isGWRunning={isGWRunning}
        onGWProgressUpdate={onGWProgressUpdate}
        onCameraDistanceChange={onCameraDistanceChange}
      />

      <CinematicCamera
        isTourRunning={isTourRunning}
        onTourComplete={onTourComplete}
        onWaypointChange={onWaypointChange}
        onBoundaryCross={onBoundaryCross}
        onParityFlip={onParityFlip}
        controlsRef={controlsRef}
      />

      <OrbitControls
        ref={controlsRef}
        enablePan enableZoom enableRotate
        minDistance={0.0000000001}
        maxDistance={100}
        zoomSpeed={1.2}
        rotateSpeed={0.5}
        enableDamping
        dampingFactor={0.05}
      />
      <PerspectiveCamera makeDefault position={[25, 18, 25]} fov={50} near={0.00000000001} far={1000} />
    </>
  );
};

// =============================================================================
// MAIN COMPONENT
// =============================================================================

const MultiMessengerUniverse: React.FC = () => {
  const [filters, setFilters] = useState<Record<string, boolean>>({
    solarSystem: true,
    milkyWay: true,
    localGroup: true,
    structures: true,
    highZ: true,
    survey: true,
    lymanAlpha: false,  // Off by default (can clutter at cosmic scale)
    baoSpheres: false,  // Off by default (toggle to show)
    kszVectors: false,  // Off by default (toggle to show)
  });

  const [isRotating, setIsRotating] = useState(false);
  const [showLabels, setShowLabels] = useState(true);
  const [isTourRunning, setIsTourRunning] = useState(false);
  const [tourText, setTourText] = useState('');
  const [cameraDistance, setCameraDistance] = useState(3);

  // GW190521 Simulation State
  const [isGWRunning, setIsGWRunning] = useState(false);
  const [gwProgress, setGWProgress] = useState(0);
  const [gwPhase, setGWPhase] = useState(0);
  const [gwWaveRadius, setGWWaveRadius] = useState(0);

  // Boundary crossing state (Directive VVV)
  const [isRuptureActive, setIsRuptureActive] = useState(false);
  const [ruptureAxis, setRuptureAxis] = useState<string | null>(null);
  const [isParityFlip, setIsParityFlip] = useState(false);

  const handleWheel = useCallback((e: React.WheelEvent) => e.stopPropagation(), []);
  const handleStartTour = useCallback(() => { setIsTourRunning(true); setIsRotating(false); }, []);
  const handleStopTour = useCallback(() => { setIsTourRunning(false); setTourText(''); }, []);
  const handleWaypointChange = useCallback((text: string) => setTourText(text), []);

  // Boundary crossing handler (Directive TTT)
  const handleBoundaryCross = useCallback((axis: string) => {
    setRuptureAxis(axis);
    setIsParityFlip(false);
    setIsRuptureActive(true);
    // Flash for 1.5 seconds
    setTimeout(() => setIsRuptureActive(false), 1500);
  }, []);

  // Parity flip handler (Z₂)
  const handleParityFlip = useCallback(() => {
    setRuptureAxis(null);
    setIsParityFlip(true);
    setIsRuptureActive(true);
    // Flash for 1.5 seconds
    setTimeout(() => setIsRuptureActive(false), 1500);
  }, []);

  // GW Handlers
  const handleStartGW = useCallback(() => {
    setIsGWRunning(true);
    setIsRotating(false);
    setGWProgress(0);
    setGWPhase(0);
    setGWWaveRadius(0);
  }, []);
  const handleStopGW = useCallback(() => {
    setIsGWRunning(false);
    setGWProgress(0);
    setGWPhase(0);
    setGWWaveRadius(0);
  }, []);

  return (
    <div className="relative w-full h-[800px] bg-slate-950 rounded-lg overflow-hidden" onWheel={handleWheel}>
      <ScaleIndicator cameraDistance={cameraDistance} />

      <FilterPanel
        filters={filters}
        setFilters={setFilters}
        isRotating={isRotating}
        setIsRotating={setIsRotating}
        showLabels={showLabels}
        setShowLabels={setShowLabels}
        isTourRunning={isTourRunning}
        onStartTour={handleStartTour}
        onStopTour={handleStopTour}
        isGWRunning={isGWRunning}
        onStartGW={handleStartGW}
        onStopGW={handleStopGW}
      />

      <div className="absolute top-16 right-4 bg-slate-900/95 p-3 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-[200px]">
        <h3 className="text-white font-bold text-sm mb-1">Z² Digital Twin</h3>
        <p className="text-slate-400 text-[10px] leading-relaxed">
          Zoom from planets to the 20.6 Gpc cosmic horizon. All scales unified in T³/Z₂ topology.
        </p>
      </div>

      {isTourRunning && tourText && (
        <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-20 max-w-2xl">
          <div className="bg-black/90 text-white font-mono text-lg border border-cyan-500 px-6 py-4 rounded-lg shadow-[0_0_30px_rgba(6,182,212,0.4)]">
            <p>{tourText}</p>
          </div>
        </div>
      )}

      {/* GW190521 Simulation HUD */}
      <GWSimulationHUD
        isRunning={isGWRunning}
        progress={gwProgress}
        phase={gwPhase}
        waveRadius={gwWaveRadius}
      />

      <Canvas gl={{ antialias: true, logarithmicDepthBuffer: true }} dpr={[1, 2]}>
        <Scene
          filters={filters}
          isRotating={isRotating}
          showLabels={showLabels}
          isTourRunning={isTourRunning}
          onTourComplete={handleStopTour}
          onWaypointChange={handleWaypointChange}
          onCameraDistanceChange={setCameraDistance}
          onBoundaryCross={handleBoundaryCross}
          onParityFlip={handleParityFlip}
          isGWRunning={isGWRunning}
          onGWProgressUpdate={(progress, phase, waveRadius) => {
            setGWProgress(progress);
            setGWPhase(phase);
            setGWWaveRadius(waveRadius);
            // Auto-stop when simulation completes
            if (progress >= 1) {
              handleStopGW();
            }
          }}
        />
      </Canvas>

      {/* Boundary Rupture Overlay (Directive VVV) - MUST be after Canvas to render on top */}
      <BoundaryRuptureOverlay
        isActive={isRuptureActive}
        axis={ruptureAxis}
        isParityFlip={isParityFlip}
      />

      <div className="absolute bottom-4 right-4 bg-slate-900/95 p-2 rounded-lg border border-slate-700 z-10 text-[10px] space-y-0.5">
        <div className="flex items-center gap-1 text-yellow-400"><span className="w-1.5 h-1.5 rounded-full bg-yellow-400" />Solar System</div>
        <div className="flex items-center gap-1 text-blue-400"><span className="w-1.5 h-1.5 rounded-full bg-blue-400" />Milky Way</div>
        <div className="flex items-center gap-1 text-green-400"><span className="w-1.5 h-1.5 rounded-full bg-green-400" />Local Group</div>
        <div className="flex items-center gap-1 text-orange-400"><span className="w-1.5 h-1.5 rounded-full bg-orange-400" />Structures</div>
        <div className="flex items-center gap-1 text-fuchsia-400"><span className="w-1.5 h-1.5 rounded-full bg-fuchsia-400" />High-z / Ly-α</div>
        <div className="flex items-center gap-1 text-cyan-400"><span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />BAO 150 Mpc</div>
        <div className="flex items-center gap-1 text-amber-400"><span className="w-1.5 h-1.5 rounded-full bg-amber-400" />kSZ Outflows</div>
      </div>
    </div>
  );
};

export default MultiMessengerUniverse;
