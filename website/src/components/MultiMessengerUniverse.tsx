'use client';

import React, { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Line, Html, Stars } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';

// Player Mode imports (Directives WWW, XXX, YYY, ZZZ)
import dynamic from 'next/dynamic';
import { usePlayerStore } from '../store/playerStore';

// CMB Evidence Layer (Phase 4 - Topology Proof)
import { CMBEvidenceLayer, CMBEvidenceHUD, getCMBViewPosition, CMB_CIRCLE_DATA } from './CMBEvidenceLayer';

// Evidence Layer Components (Directives QQQQ, RRRR, SSSS, TTTT, UUUU, VVVV, WWWW, XXXX, YYYY)
import { CMBParitySphere, ParityEvidenceHUD } from './evidence/CMBParitySphere';
import { IsotropyBreaker, IsotropyBreakerHUD } from './evidence/IsotropyBreaker';
import { KinematicFlowMap, DarkFlowHUD } from './evidence/KinematicFlowMap';
import { GravitationalGraveyard, GraveyardHUD } from './evidence/GravitationalGraveyard';
import { GeometricGravity, MONDHUD } from './evidence/GeometricGravity';
import { RadioMirrors, RadioGhostHUD } from './evidence/RadioMirrors';
import { LocalMONDAnchor, WideBinaryHUD } from './evidence/LocalMONDAnchor';
import { DispersionTomography, DispersionHUD } from './evidence/DispersionTomography';
import { CosmicWindShader, CosmicWindHUD } from './evidence/CosmicWindShader';
import { DESIGalaxies, DESIGalaxiesHUD } from './evidence/DESIGalaxies';
import { GalaxyClusterMap, ClusterMapHUD } from './evidence/GalaxyClusterMap';

// Performance Monitoring
import { MinimalFPS } from './PerformanceHUD';

// Dynamic imports to avoid SSR issues with THREE.js
const PlayerController = dynamic(() => import('./PlayerMode/PlayerController'), { ssr: false });
const PlayerHUD = dynamic(() => import('./PlayerMode/PlayerController').then(mod => ({ default: mod.PlayerHUD })), { ssr: false });
const VesselSelector = dynamic(() => import('./PlayerMode/VesselSelector'), { ssr: false });
const OtherPlayersRenderer = dynamic(() => import('./PlayerMode/OtherPlayersRenderer'), { ssr: false });
const MultiplayerHUD = dynamic(() => import('./PlayerMode/OtherPlayersRenderer').then(mod => ({ default: mod.MultiplayerHUD })), { ssr: false });

// =============================================================================
// GRAVITATIONAL WAVE EVENT CATALOG
// GWTC-1, GWTC-2, GWTC-3, GWTC-4 events from LIGO-Virgo-KAGRA
// =============================================================================

interface GWEvent {
  id: string;
  name: string;
  type: 'BBH' | 'BNS' | 'NSBH';
  description: string;
  position: { x: number; y: number; z: number };
  distance_gpc: number;
  mass1_solar: number;
  mass2_solar: number;
  finalMass_solar: number;
  peakStrain: number;
  peakFrequency_Hz: number;
  date: string;
  significance: string;
}

// Generate random position at given distance
function positionAtDistance(d: number, seed: number): { x: number; y: number; z: number } {
  const phi = (seed * 137.5) % 360 * Math.PI / 180;
  const theta = Math.acos(2 * ((seed * 0.618) % 1) - 1);
  return {
    x: d * Math.sin(theta) * Math.cos(phi),
    y: d * Math.sin(theta) * Math.sin(phi),
    z: d * Math.cos(theta)
  };
}

const GW_EVENTS: GWEvent[] = [
  // === HISTORIC FIRSTS ===
  {
    id: 'GW150914',
    name: 'GW150914 (First Detection)',
    type: 'BBH',
    description: 'First direct detection of gravitational waves',
    position: positionAtDistance(0.44, 1),
    distance_gpc: 0.44,
    mass1_solar: 36,
    mass2_solar: 29,
    finalMass_solar: 62,
    peakStrain: 1.0e-21,
    peakFrequency_Hz: 150,
    date: '2015-09-14',
    significance: 'Nobel Prize 2017 - Confirmed Einstein\'s prediction'
  },
  {
    id: 'GW170817',
    name: 'GW170817 (BNS + Kilonova)',
    type: 'BNS',
    description: 'First binary neutron star merger with EM counterpart',
    position: positionAtDistance(0.04, 2),
    distance_gpc: 0.04,
    mass1_solar: 1.46,
    mass2_solar: 1.27,
    finalMass_solar: 2.7,
    peakStrain: 1.0e-22,
    peakFrequency_Hz: 400,
    date: '2017-08-17',
    significance: 'Multi-messenger astronomy birth - GRB 170817A + AT 2017gfo'
  },
  // === EXTREME MASS EVENTS ===
  {
    id: 'GW190521',
    name: 'GW190521 (IMBH Merger)',
    type: 'BBH',
    description: 'First intermediate-mass black hole detection',
    position: { x: 4.2, y: 1.8, z: -2.5 },
    distance_gpc: 5.3,
    mass1_solar: 85,
    mass2_solar: 66,
    finalMass_solar: 142,
    peakStrain: 2.4e-22,
    peakFrequency_Hz: 60,
    date: '2019-05-21',
    significance: 'First BH in 100-1000 M☉ range - IMBH confirmed'
  },
  {
    id: 'GW231123',
    name: 'GW231123 (Most Massive)',
    type: 'BBH',
    description: 'Highest total mass BBH merger observed',
    position: positionAtDistance(7.2, 4),
    distance_gpc: 7.2,
    mass1_solar: 137,
    mass2_solar: 103,
    finalMass_solar: 228,
    peakStrain: 1.8e-22,
    peakFrequency_Hz: 35,
    date: '2023-11-23',
    significance: 'GWTC-4 record holder - 240 M☉ total mass'
  },
  // === MASS GAP MYSTERIES ===
  {
    id: 'GW190814',
    name: 'GW190814 (Mass Gap)',
    type: 'NSBH',
    description: 'Mystery object in the mass gap',
    position: positionAtDistance(0.24, 5),
    distance_gpc: 0.24,
    mass1_solar: 23,
    mass2_solar: 2.6,
    finalMass_solar: 25,
    peakStrain: 5.0e-22,
    peakFrequency_Hz: 250,
    date: '2019-08-14',
    significance: '2.6 M☉ object: heaviest NS or lightest BH?'
  },
  {
    id: 'GW230627',
    name: 'GW230627 (Lightest BH)',
    type: 'BBH',
    description: 'Lowest mass component in GWTC-4',
    position: positionAtDistance(1.1, 6),
    distance_gpc: 1.1,
    mass1_solar: 8.2,
    mass2_solar: 5.79,
    finalMass_solar: 13.5,
    peakStrain: 3.0e-22,
    peakFrequency_Hz: 180,
    date: '2023-06-27',
    significance: '5.79 M☉ - probing the lower mass gap'
  },
  // === HIGH SNR / PRECISION EVENTS ===
  {
    id: 'GW240615',
    name: 'GW240615 (Best Localized)',
    type: 'BBH',
    description: 'Most precisely localized GW event',
    position: positionAtDistance(0.85, 7),
    distance_gpc: 0.85,
    mass1_solar: 30,
    mass2_solar: 26,
    finalMass_solar: 53,
    peakStrain: 8.0e-22,
    peakFrequency_Hz: 120,
    date: '2024-06-15',
    significance: '6 sq deg localization - 30x moon size'
  },
  {
    id: 'GW250114',
    name: 'GW250114 (Kerr Verified)',
    type: 'BBH',
    description: 'Strongest evidence for Kerr black holes',
    position: positionAtDistance(0.405, 8),
    distance_gpc: 0.405,
    mass1_solar: 33.76,
    mass2_solar: 32.26,
    finalMass_solar: 62.9,
    peakStrain: 1.2e-21,
    peakFrequency_Hz: 140,
    date: '2025-01-14',
    significance: 'Ringdown confirms GR black hole predictions'
  },
  // === NSBH EVENTS ===
  {
    id: 'GW200115',
    name: 'GW200115 (NS-BH Merger)',
    type: 'NSBH',
    description: 'Confirmed neutron star-black hole merger',
    position: positionAtDistance(0.30, 9),
    distance_gpc: 0.30,
    mass1_solar: 5.7,
    mass2_solar: 1.5,
    finalMass_solar: 7.0,
    peakStrain: 4.0e-22,
    peakFrequency_Hz: 200,
    date: '2020-01-15',
    significance: 'First confirmed NSBH detection'
  },
  {
    id: 'GW230518',
    name: 'GW230518 (NSBH Candidate)',
    type: 'NSBH',
    description: 'O4 neutron star-black hole candidate',
    position: positionAtDistance(0.94, 10),
    distance_gpc: 0.94,
    mass1_solar: 6.8,
    mass2_solar: 1.8,
    finalMass_solar: 8.4,
    peakStrain: 2.5e-22,
    peakFrequency_Hz: 220,
    date: '2023-05-18',
    significance: 'Associated with SN 2023ixf search window'
  },
  // === DISTANT / COSMOLOGICAL EVENTS ===
  {
    id: 'GW250118',
    name: 'GW250118 (Distant BBH)',
    type: 'BBH',
    description: 'High-redshift BBH merger',
    position: positionAtDistance(5.8, 11),
    distance_gpc: 5.8,
    mass1_solar: 44,
    mass2_solar: 31,
    finalMass_solar: 71,
    peakStrain: 1.5e-22,
    peakFrequency_Hz: 55,
    date: '2025-01-18',
    significance: 'Probes BH populations at z~0.9'
  },
  {
    id: 'GW250108',
    name: 'GW250108 (Heavy Distant)',
    type: 'BBH',
    description: 'Massive merger at cosmological distance',
    position: positionAtDistance(3.8, 12),
    distance_gpc: 3.8,
    mass1_solar: 54,
    mass2_solar: 36,
    finalMass_solar: 86,
    peakStrain: 2.0e-22,
    peakFrequency_Hz: 65,
    date: '2025-01-08',
    significance: '90 M☉ total at 3.8 Gpc'
  }
];

// Default event for backwards compatibility
const GW190521_EVENT = GW_EVENTS.find(e => e.id === 'GW190521')!;

// =============================================================================
// MULTI-SCALE TOPOLOGICAL DIGITAL TWIN
// From planets to the 20.6 Gpc cosmic horizon
// =============================================================================

// Scale constants
const L_C_GPC = 20.6;
const HALF_BOX = L_C_GPC / 2;

// Scale thresholds for LOD (in Gpc from origin) - TRUE HYPERREAL SCALE
const TRUE_AU_GPC = 4.848e-15; // 1 AU in Gpc (true scale)
const SCALE_EARTH_SURFACE = TRUE_AU_GPC * 4e-5;    // ~6000 km in Gpc (Earth radius)
const SCALE_SOLAR_SYSTEM = TRUE_AU_GPC * 50;       // ~50 AU in Gpc (Kuiper belt)
const SCALE_OORT_CLOUD = TRUE_AU_GPC * 50000;      // ~50000 AU in Gpc (Oort cloud)
const SCALE_MILKY_WAY = 0.00003;                   // ~30 kpc in Gpc
const SCALE_LOCAL_GROUP = 0.003;                   // ~3 Mpc in Gpc
const SCALE_COSMIC = 1;                            // Full cosmic scale

// =============================================================================
// SOLAR SYSTEM DATA - J2000 Keplerian Elements for TRUE positions
// =============================================================================
// Source: NASA JPL Horizons ephemeris data
// Reference epoch: J2000.0 = January 1, 2000, 12:00 TT

interface PlanetData {
  name: string;
  radius_km: number;
  color: string;
  // Keplerian orbital elements (J2000 epoch)
  a: number;           // Semi-major axis (AU)
  e: number;           // Eccentricity
  i: number;           // Inclination (degrees)
  omega: number;       // Longitude of ascending node (degrees)
  w: number;           // Argument of perihelion (degrees)
  M0: number;          // Mean anomaly at J2000 (degrees)
  n: number;           // Mean motion (degrees/day)
}

const PLANETS: PlanetData[] = [
  // Mercury - fastest, most eccentric inner planet
  { name: 'Mercury', radius_km: 2439.7, color: '#8c7853',
    a: 0.38709927, e: 0.20563593, i: 7.00497902, omega: 48.33076593, w: 77.45779628, M0: 174.796, n: 4.09233445 },
  // Venus - nearly circular orbit
  { name: 'Venus', radius_km: 6051.8, color: '#ffd700',
    a: 0.72333566, e: 0.00677672, i: 3.39467605, omega: 76.67984255, w: 131.60246718, M0: 50.115, n: 1.60213034 },
  // Earth - our reference point
  { name: 'Earth', radius_km: 6371.0, color: '#4169e1',
    a: 1.00000261, e: 0.01671123, i: 0.00001531, omega: -11.26064, w: 102.93768193, M0: 357.529, n: 0.98560028 },
  // Mars - red planet
  { name: 'Mars', radius_km: 3389.5, color: '#cd5c5c',
    a: 1.52371034, e: 0.09339410, i: 1.84969142, omega: 49.55953891, w: -23.94362959, M0: 19.373, n: 0.52402068 },
  // Jupiter - gas giant king
  { name: 'Jupiter', radius_km: 69911, color: '#deb887',
    a: 5.20288700, e: 0.04838624, i: 1.30439695, omega: 100.47390909, w: 14.72847983, M0: 20.020, n: 0.08308529 },
  // Saturn - ringed wonder
  { name: 'Saturn', radius_km: 58232, color: '#f4a460',
    a: 9.53667594, e: 0.05386179, i: 2.48599187, omega: 113.66242448, w: 92.59887831, M0: 317.020, n: 0.03349791 },
  // Uranus - tilted ice giant
  { name: 'Uranus', radius_km: 25362, color: '#afeeee',
    a: 19.18916464, e: 0.04725744, i: 0.77263783, omega: 74.01692503, w: 170.95427630, M0: 142.238, n: 0.01176904 },
  // Neptune - distant blue giant
  { name: 'Neptune', radius_km: 24622, color: '#1e90ff',
    a: 30.06992276, e: 0.00859048, i: 1.77004347, omega: 131.78422574, w: 44.96476227, M0: 256.228, n: 0.00606020 },
  // Pluto - dwarf planet (for completeness)
  { name: 'Pluto', radius_km: 1188.3, color: '#dcdcdc',
    a: 39.48211675, e: 0.24882730, i: 17.14001206, omega: 110.30393684, w: 224.06891629, M0: 14.53, n: 0.00397459 },
];

// J2000 epoch in JavaScript Date
const J2000_EPOCH = new Date('2000-01-01T12:00:00Z').getTime();

/**
 * Calculate planet position using Keplerian orbital mechanics
 * Returns position in AU relative to Sun at origin
 */
function calculatePlanetPosition(planet: PlanetData, date: Date): { x: number; y: number; z: number } {
  // Days since J2000
  const daysSinceJ2000 = (date.getTime() - J2000_EPOCH) / (1000 * 60 * 60 * 24);

  // Mean anomaly at current date (degrees)
  const M = (planet.M0 + planet.n * daysSinceJ2000) % 360;
  const M_rad = M * Math.PI / 180;

  // Solve Kepler's equation for eccentric anomaly (Newton-Raphson)
  let E = M_rad;
  for (let i = 0; i < 10; i++) {
    E = E - (E - planet.e * Math.sin(E) - M_rad) / (1 - planet.e * Math.cos(E));
  }

  // True anomaly
  const nu = 2 * Math.atan2(
    Math.sqrt(1 + planet.e) * Math.sin(E / 2),
    Math.sqrt(1 - planet.e) * Math.cos(E / 2)
  );

  // Distance from Sun
  const r = planet.a * (1 - planet.e * Math.cos(E));

  // Convert orbital elements to radians
  const i_rad = planet.i * Math.PI / 180;
  const omega_rad = planet.omega * Math.PI / 180;
  const w_rad = planet.w * Math.PI / 180;

  // Position in orbital plane
  const x_orb = r * Math.cos(nu);
  const y_orb = r * Math.sin(nu);

  // Transform to ecliptic coordinates (simplified - ignoring nutation)
  const cos_w = Math.cos(w_rad);
  const sin_w = Math.sin(w_rad);
  const cos_omega = Math.cos(omega_rad);
  const sin_omega = Math.sin(omega_rad);
  const cos_i = Math.cos(i_rad);
  const sin_i = Math.sin(i_rad);

  const x = (cos_w * cos_omega - sin_w * sin_omega * cos_i) * x_orb +
            (-sin_w * cos_omega - cos_w * sin_omega * cos_i) * y_orb;
  const y = (cos_w * sin_omega + sin_w * cos_omega * cos_i) * x_orb +
            (-sin_w * sin_omega + cos_w * cos_omega * cos_i) * y_orb;
  const z = (sin_w * sin_i) * x_orb + (cos_w * sin_i) * y_orb;

  return { x, y, z };
}

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
  // Great Attractor: center of Laniakea, direction RA 201° Dec -44°, distance ~65 Mpc (Tully et al. 2014)
  { name: 'Great Attractor', distance_mpc: 65, ra: 201, dec: -44, type: 'supercluster' as const, size_mpc: 50 },
  { name: 'Sloan Great Wall', distance_mpc: 310, ra: 195, dec: 7, type: 'wall' as const, size_mpc: 430 },
  { name: 'Boötes Void', distance_mpc: 213, ra: 218, dec: 46, type: 'void' as const, size_mpc: 100 },
  { name: 'CMB Cold Spot', distance_mpc: 3000, ra: 49, dec: -19, type: 'void' as const, size_mpc: 500 },
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
  // TRUE HYPERREAL ASTRONOMICAL SCALING
  // ==========================================================================
  // This is REAL SCALE. No exaggeration. The beauty is in how small we are.
  //
  // Conversion chain:
  // 1 AU = 149,597,870.7 km
  // 1 parsec = 206,265 AU = 3.086e13 km
  // 1 kpc = 206,265,000 AU
  // 1 Gpc = 206,265,000,000,000 AU
  // Therefore: 1 AU = 4.848e-15 Gpc
  //
  // At true scale, if the Sun were 1 meter diameter:
  // - Earth would be 1 cm, located 107 meters away
  // - Jupiter would be 10 cm, located 556 meters away
  // - Neptune would be 3.5 cm, located 3.2 kilometers away

  const TRUE_AU_TO_GPC = 4.848e-15; // TRUE SCALE: 1 AU in Gpc
  const KM_TO_GPC = TRUE_AU_TO_GPC / 149597870.7; // 1 km in Gpc

  // True physical radii (in Gpc)
  const SUN_RADIUS_GPC = 696340 * KM_TO_GPC;      // 2.26e-17 Gpc
  const EARTH_RADIUS_GPC = 6371 * KM_TO_GPC;      // 2.06e-19 Gpc
  const JUPITER_RADIUS_GPC = 69911 * KM_TO_GPC;   // 2.27e-18 Gpc

  // Finder marker scale: visible at intermediate zoom levels
  // These help you FIND the planets, then disappear when you're close enough to see them
  const FINDER_SCALE = Math.max(0, Math.min(1, (cameraDistance - 1e-16) / (1e-13 - 1e-16)));
  const showFinders = cameraDistance > 1e-16 && cameraDistance < 1e-12;

  // At extremely close zoom (< 1e-16), show true scale
  // Between 1e-16 and 1e-13, blend between true and finder scale
  const sunDisplaySize = SUN_RADIUS_GPC * (1 + FINDER_SCALE * 1e4);

  // Scale indicator for how far we are from true scale
  const scaleExaggeration = showFinders ? Math.round(1 + FINDER_SCALE * 1e4) : 1;

  return (
    <group>
      {/* Sun - TRUE SCALE */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[sunDisplaySize, 32, 32]} />
        <meshBasicMaterial color="#ffdd00" />
      </mesh>
      {/* Sun corona glow - helps locate at intermediate zoom */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[sunDisplaySize * 2, 16, 16]} />
        <meshBasicMaterial color="#ffaa00" transparent opacity={showFinders ? 0.4 : 0.15} />
      </mesh>

      {/* Sun finder beacon - visible from galactic scale */}
      {showFinders && (
        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[cameraDistance * 0.02, 8, 8]} />
          <meshBasicMaterial color="#ffff00" transparent opacity={0.6} />
        </mesh>
      )}

      {showLabels && cameraDistance < 1e-13 && (
        <Html position={[0, sunDisplaySize * 3, 0]} center>
          <div className="bg-yellow-900/80 px-2 py-1 rounded text-yellow-300 text-xs whitespace-nowrap font-bold border border-yellow-400/50">
            <div className="text-center">
              <span className="text-yellow-200">☀ The Sun</span>
              <div className="text-[9px] text-yellow-400/80 mt-0.5">R = 696,340 km</div>
              {scaleExaggeration > 1 && (
                <div className="text-[8px] text-orange-400 mt-0.5">
                  Finder mode: {scaleExaggeration.toLocaleString()}× size
                </div>
              )}
              <div className="text-[8px] text-cyan-400 mt-1 border-t border-yellow-400/30 pt-1">
                YOU ARE HERE
              </div>
            </div>
          </div>
        </Html>
      )}

      {/* Planets - TRUE POSITIONS based on current datetime */}
      {PLANETS.map((planet) => {
        // Calculate TRUE position using Keplerian mechanics
        const now = new Date();
        const pos = calculatePlanetPosition(planet, now);

        // Convert AU to Gpc (TRUE SCALE)
        const x = pos.x * TRUE_AU_TO_GPC;
        const y = pos.z * TRUE_AU_TO_GPC; // Swap y/z for Three.js coordinate system
        const z = pos.y * TRUE_AU_TO_GPC;

        // Orbital radius for ring display
        const orbitalRadius = planet.a * TRUE_AU_TO_GPC;

        // Planet physical size - TRUE SCALE with finder mode
        const trueRadius = planet.radius_km * KM_TO_GPC;
        const planetDisplaySize = trueRadius * (1 + FINDER_SCALE * 1e4);

        // Orbit ring - true scale but visible thickness
        const orbitThickness = Math.max(orbitalRadius * 0.001, trueRadius * 10);

        return (
          <group key={planet.name}>
            {/* Orbit ring - always visible as reference */}
            <mesh rotation={[Math.PI / 2, 0, 0]}>
              <ringGeometry args={[
                orbitalRadius - orbitThickness,
                orbitalRadius + orbitThickness,
                128
              ]} />
              <meshBasicMaterial color="#ffffff" transparent opacity={0.08} side={THREE.DoubleSide} />
            </mesh>

            {/* Planet - TRUE SCALE (with finder boost when far) */}
            <mesh position={[x, y, z]}>
              <sphereGeometry args={[planetDisplaySize, 16, 16]} />
              <meshBasicMaterial color={planet.color} />
            </mesh>

            {/* Planet finder beacon - visible at intermediate zoom */}
            {showFinders && (
              <mesh position={[x, y, z]}>
                <sphereGeometry args={[cameraDistance * 0.008, 8, 8]} />
                <meshBasicMaterial color={planet.color} transparent opacity={0.5} />
              </mesh>
            )}

            {/* Saturn's rings - proportional to planet size */}
            {planet.name === 'Saturn' && (
              <mesh position={[x, y, z]} rotation={[Math.PI / 3, 0, 0]}>
                <ringGeometry args={[planetDisplaySize * 1.4, planetDisplaySize * 2.3, 32]} />
                <meshBasicMaterial color="#d4a574" transparent opacity={0.6} side={THREE.DoubleSide} />
              </mesh>
            )}

            {/* Earth detail - show continents hint when very close */}
            {planet.name === 'Earth' && cameraDistance < trueRadius * 100 && (
              <mesh position={[x, y, z]}>
                <sphereGeometry args={[planetDisplaySize * 1.01, 32, 32]} />
                <meshBasicMaterial color="#228B22" transparent opacity={0.3} wireframe />
              </mesh>
            )}

            {/* Labels when zoomed to solar system scale */}
            {showLabels && cameraDistance < 1e-13 && cameraDistance > orbitalRadius * 0.1 && (
              <Html position={[x, y + planetDisplaySize * 3, z]} center>
                <div className="bg-black/80 px-1 py-0.5 rounded text-white text-[9px] whitespace-nowrap">
                  {planet.name} ({planet.a.toFixed(planet.a < 2 ? 2 : 1)} AU)
                  {planet.name === 'Earth' && (
                    <span className="text-cyan-400 ml-1">← HOME</span>
                  )}
                </div>
              </Html>
            )}
          </group>
        );
      })}

      {/* Scale indicator - shows current zoom level */}
      {showLabels && cameraDistance < 1e-12 && cameraDistance > 1e-16 && (
        <Html position={[0, -cameraDistance * 0.3, 0]} center>
          <div className="bg-slate-900/90 border border-cyan-500 px-2 py-1 rounded text-cyan-300 text-[10px]">
            <div className="text-center">
              <div className="text-[8px] text-slate-400">Zoom depth</div>
              <div className="font-mono">
                {cameraDistance > 1e-14
                  ? `${(cameraDistance / TRUE_AU_TO_GPC).toFixed(0)} AU`
                  : `${(cameraDistance / TRUE_AU_TO_GPC * 149597870.7).toExponential(1)} km`
                }
              </div>
              {scaleExaggeration > 1 && (
                <div className="text-[8px] text-orange-400 mt-1">
                  Planets enlarged {scaleExaggeration.toLocaleString()}× to find
                </div>
              )}
            </div>
          </div>
        </Html>
      )}

      {/* TRUE SCALE indicator when finally at real scale */}
      {showLabels && cameraDistance < 1e-16 && (
        <Html position={[0, -sunDisplaySize * 5, 0]} center>
          <div className="bg-green-900/90 border border-green-400 px-2 py-1 rounded text-green-300 text-[10px] font-bold">
            TRUE SCALE - No exaggeration
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
  // MILKY WAY SCALING - HYPERREAL POSITIONING
  // ==========================================================================
  // Milky Way radius: ~26.8 kpc = 2.68e-5 Gpc
  // Sun's position: 8.178 kpc from center (Reid et al. 2019, GRAVITY Collab.)
  //
  // HYPERREAL APPROACH: The observer (Solar System) is at origin [0,0,0].
  // The Milky Way center is 8.178 kpc AWAY from us, toward Sagittarius A*.
  // We offset the entire galaxy so the Sun's position coincides with origin.

  const KPC_TO_GPC = 1e-6; // 1 kpc = 1e-6 Gpc = 1e-6 scene units
  const SUN_GALACTIC_RADIUS_KPC = 8.178; // GRAVITY Collaboration 2019

  // Offset to place Sun at origin: shift galaxy center by -8.178 kpc
  const GALACTIC_CENTER_OFFSET: [number, number, number] = [
    -SUN_GALACTIC_RADIUS_KPC * KPC_TO_GPC,
    0,
    0
  ];

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
    <group position={GALACTIC_CENTER_OFFSET}>
      {/*
       * HYPERREAL: This group is offset so that Sun's position (8.178 kpc from center)
       * coincides with the scene origin [0,0,0]. The Solar System component renders
       * at [0,0,0], which is exactly where the Sun should be within the Milky Way.
       */}

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

      {/*
       * NOTE: No separate Sun mesh needed here anymore!
       * The Sun IS at the origin, rendered by SolarSystem component.
       * This creates true hyperreal nesting: zoom from cosmic scale → Milky Way → Sun → planets
       */}

      {/* "YOU ARE HERE" marker at Sun's position within the galaxy */}
      {showLabels && cameraDistance > 0.000001 && cameraDistance < 0.0001 && (
        <Html position={[SUN_GALACTIC_RADIUS_KPC * KPC_TO_GPC, 1.5 * KPC_TO_GPC, 0]} center>
          <div className="bg-yellow-900/95 px-2 py-1 rounded text-yellow-300 text-[10px] whitespace-nowrap font-bold border border-yellow-400/60 animate-pulse">
            <div className="text-center">
              <span className="text-cyan-400">← YOU ARE HERE</span>
              <div className="text-[8px] text-yellow-400/80 mt-0.5">Sun • 8.178 kpc from center</div>
            </div>
          </div>
        </Html>
      )}

      {/* Galactic Center label (Sagittarius A*) */}
      {showLabels && cameraDistance < 0.0001 && (
        <>
          <Html position={[0, 4 * KPC_TO_GPC, 0]} center>
            <div className="bg-black/85 px-2 py-1 rounded text-orange-300 text-xs whitespace-nowrap font-bold border border-orange-500/30">
              Sagittarius A* (Galactic Center)
            </div>
          </Html>
          <Html position={[0, -2 * KPC_TO_GPC, 0]} center>
            <div className="bg-black/85 px-1 py-0.5 rounded text-blue-300 text-[9px] whitespace-nowrap border border-blue-500/30">
              Supermassive Black Hole: 4×10⁶ M☉
            </div>
          </Html>
        </>
      )}

      {/* Galactic scale reference - shows when zoomed to galactic scale */}
      {showLabels && cameraDistance > 0.000005 && cameraDistance < 0.00005 && (
        <Html position={[7 * KPC_TO_GPC, -3 * KPC_TO_GPC, 0]} center>
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
    {/* HYPERREAL: Milky Way marker at origin - "You Are Here" at Local Group scale */}
    <group position={[0, 0, 0]}>
      <mesh>
        <sphereGeometry args={[0.015, 16, 16]} />
        <meshBasicMaterial color="#88aaff" transparent opacity={0.9} />
      </mesh>
      {/* Spiral structure hint */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.008, 0.025, 32]} />
        <meshBasicMaterial color="#88aaff" transparent opacity={0.4} side={THREE.DoubleSide} />
      </mesh>
      {showLabels && (
        <Html position={[0, 0.03, 0]} center>
          <div className="bg-blue-900/90 px-2 py-1 rounded text-blue-200 text-[10px] whitespace-nowrap font-bold border border-cyan-400/60">
            <div className="text-center">
              <span className="text-cyan-400">MILKY WAY</span>
              <div className="text-[8px] text-blue-300/80 mt-0.5">You Are Here</div>
            </div>
          </div>
        </Html>
      )}
    </group>

    {/* Other Local Group members */}
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

// T³ coordinate wrapping - keeps positions within ±HALF_BOX
function wrapCoordinate(value: number): number {
  const wrapped = ((value + HALF_BOX) % L_C_GPC + L_C_GPC) % L_C_GPC - HALF_BOX;
  return wrapped;
}

const SurveyGalaxies: React.FC = () => {
  const geometry = useMemo(() => {
    const positions = new Float32Array(SURVEY_GALAXIES.length * 3);
    const colors = new Float32Array(SURVEY_GALAXIES.length * 3);
    SURVEY_GALAXIES.forEach((galaxy, i) => {
      const pos = celestialToCartesian(galaxy.ra, galaxy.dec, galaxy.distance_mpc);
      // Apply T³ wrapping to keep within fundamental domain (±10.3 Gpc)
      positions[i * 3] = wrapCoordinate(pos[0]);
      positions[i * 3 + 1] = wrapCoordinate(pos[1]);
      positions[i * 3 + 2] = wrapCoordinate(pos[2]);
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
  // The 8 Z₂ fixed points are at the corners of the fundamental domain (±10.3 Gpc)
  // These are orbifold singularities where fermion generations are localized
  // NOT locations of specific astronomical structures - purely topological features
  const vertices = [
    { name: 'Z₂ (+,+,+)', position: [HALF_BOX, HALF_BOX, HALF_BOX] as [number, number, number], color: '#FFD700' },
    { name: 'Z₂ (-,+,+)', position: [-HALF_BOX, HALF_BOX, HALF_BOX] as [number, number, number], color: '#FF6B6B' },
    { name: 'Z₂ (+,-,+)', position: [HALF_BOX, -HALF_BOX, HALF_BOX] as [number, number, number], color: '#4ECDC4' },
    { name: 'Z₂ (-,-,+)', position: [-HALF_BOX, -HALF_BOX, HALF_BOX] as [number, number, number], color: '#45B7D1' },
    { name: 'Z₂ (+,+,-)', position: [HALF_BOX, HALF_BOX, -HALF_BOX] as [number, number, number], color: '#96CEB4' },
    { name: 'Z₂ (-,+,-)', position: [-HALF_BOX, HALF_BOX, -HALF_BOX] as [number, number, number], color: '#FFEAA7' },
    { name: 'Z₂ (+,-,-)', position: [HALF_BOX, -HALF_BOX, -HALF_BOX] as [number, number, number], color: '#DDA0DD' },
    { name: 'Z₂ (-,-,-)', position: [-HALF_BOX, -HALF_BOX, -HALF_BOX] as [number, number, number], color: '#00FFFF' },
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
// GRAVITATIONAL WAVE SIMULATION - Configurable for any event
// =============================================================================

interface GWSimulationProps {
  isRunning: boolean;
  selectedEvent: GWEvent;
  onProgressUpdate: (progress: number, phase: number, waveRadius: number) => void;
}

const GWSimulation: React.FC<GWSimulationProps> = ({ isRunning, selectedEvent, onProgressUpdate }) => {
  const startTimeRef = useRef<number>(0);
  const waveRadiusRef = useRef(0);
  const groupRef = useRef<THREE.Group>(null);

  // T³/Z₂ topology parameters (scaled for visualization: 1 unit = 1 Gpc)
  const L_c = 20.6; // Fundamental domain size in Gpc
  const halfL = L_c / 2; // ±10.3 Gpc boundaries

  // Primary epicenter position - from selected event
  const epicenter: [number, number, number] = useMemo(() => [
    selectedEvent.position.x,
    selectedEvent.position.y,
    selectedEvent.position.z
  ], [selectedEvent]);

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
        delay: dist - selectedEvent.distance_gpc // Delay relative to direct path
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
    { name: 'Merger', duration: 2, description: `${selectedEvent.type} merger at ${selectedEvent.distance_gpc.toFixed(1)} Gpc` },
    { name: 'Direct Wave', duration: 6, description: 'Primary GW expands in T³' },
    { name: 'Boundary Cross', duration: 4, description: 'Wave wraps through T³ faces' },
    { name: 'Multi-Path', duration: 6, description: 'Wrapped copies converge on Earth' },
    { name: 'Z₂ Image', duration: 4, description: 'Antipodal signal arrives' },
  ], [selectedEvent]);

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
      {waveRadius >= selectedEvent.distance_gpc && (
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
          {selectedEvent.id} PRIMARY<br/>
          <span className="text-[8px] opacity-70">{selectedEvent.mass1_solar}+{selectedEvent.mass2_solar} M☉ → {selectedEvent.finalMass_solar} M☉</span>
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

// GW Simulation HUD Overlay (rendered outside Canvas) - T³/Z₂ version
const GWSimulationHUD: React.FC<{
  isRunning: boolean;
  selectedEvent: GWEvent;
  progress: number;
  phase: number;
  waveRadius: number;
}> = ({ isRunning, selectedEvent, progress, phase, waveRadius }) => {
  if (!isRunning) return null;

  const L_c = 20.6; // Fundamental domain
  const directDist = selectedEvent.distance_gpc;
  const z2Dist = directDist; // Z₂ image at same distance (antipodal)
  const wrappedDist = L_c - directDist; // Shortest wrapped path

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
          {selectedEvent.name}
        </div>
        <div className="text-slate-400 text-[10px] space-y-0.5">
          <div>{selectedEvent.mass1_solar} + {selectedEvent.mass2_solar} M☉ → {selectedEvent.finalMass_solar} M☉</div>
          <div className="text-slate-500">{selectedEvent.significance}</div>
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
  // TRUE HYPERREAL scale thresholds
  // 1 AU = 4.848e-15 Gpc (true astronomical scale)
  // 1 kpc = 1e-6 Gpc
  // 1 Mpc = 1e-3 Gpc
  const AU_IN_GPC = 4.848e-15;
  const KM_IN_GPC = AU_IN_GPC / 149597870.7;

  let scaleName = '';
  let scaleColor = '';
  let scaleValue = '';

  if (cameraDistance < AU_IN_GPC * 0.01) {
    // Sub-AU scale: planetary distances (< 0.01 AU = ~1.5 million km)
    scaleName = 'Planetary';
    scaleColor = 'text-green-400';
    const km = cameraDistance / KM_IN_GPC;
    if (km < 1000) {
      scaleValue = `${km.toFixed(0)} km`;
    } else if (km < 1e6) {
      scaleValue = `${(km / 1000).toFixed(0)} thousand km`;
    } else {
      scaleValue = `${(km / 1e6).toFixed(2)} million km`;
    }
  } else if (cameraDistance < AU_IN_GPC * 10) {
    // Inner Solar System (0.01 - 10 AU)
    scaleName = 'Inner Solar System';
    scaleColor = 'text-yellow-400';
    const au = cameraDistance / AU_IN_GPC;
    scaleValue = `${au.toFixed(2)} AU`;
  } else if (cameraDistance < AU_IN_GPC * 100) {
    // Outer Solar System (10 - 100 AU)
    scaleName = 'Outer Solar System';
    scaleColor = 'text-orange-400';
    const au = cameraDistance / AU_IN_GPC;
    scaleValue = `${au.toFixed(1)} AU`;
  } else if (cameraDistance < AU_IN_GPC * 100000) {
    // Oort Cloud region (100 - 100,000 AU)
    scaleName = 'Oort Cloud';
    scaleColor = 'text-red-400';
    const au = cameraDistance / AU_IN_GPC;
    scaleValue = au < 1000 ? `${au.toFixed(0)} AU` : `${(au / 1000).toFixed(1)}k AU`;
  } else if (cameraDistance < 1e-6) {
    // Interstellar to galactic (100k AU to 1 kpc)
    scaleName = 'Interstellar';
    scaleColor = 'text-purple-400';
    const ly = cameraDistance / (AU_IN_GPC * 63241); // 1 ly = 63241 AU
    scaleValue = ly < 1000 ? `${ly.toFixed(0)} ly` : `${(ly / 1000).toFixed(1)}k ly`;
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
  // GW Simulation
  isGWRunning: boolean;
  selectedGWEvent: GWEvent;
  onSelectGWEvent: (event: GWEvent) => void;
  onStartGW: () => void;
  onStopGW: () => void;
  // Player Mode (Directive WWW)
  isPlayerMode: boolean;
  onStartPlayerMode: () => void;
  // CMB Proof Mode (Phase 4)
  isCMBProofActive: boolean;
  onToggleCMBProof: () => void;
  // Evidence Layers (Directives QQQQ, RRRR, SSSS)
  isParityActive: boolean;
  onToggleParity: () => void;
  isAxisOfEvilActive: boolean;
  onToggleAxisOfEvil: () => void;
  isDarkFlowActive: boolean;
  onToggleDarkFlow: () => void;
  // Evidence Layers (Directives TTTT, UUUU, VVVV)
  isGWGraveyardActive: boolean;
  onToggleGWGraveyard: () => void;
  isMONDActive: boolean;
  onToggleMOND: () => void;
  isRadioGhostsActive: boolean;
  onToggleRadioGhosts: () => void;
  // Evidence Layers (Directives WWWW, XXXX, YYYY)
  isWideBinariesActive: boolean;
  onToggleWideBinaries: () => void;
  isFRBActive: boolean;
  onToggleFRB: () => void;
  isKSZActive: boolean;
  onToggleKSZ: () => void;
  isDESIActive: boolean;
  onToggleDESI: () => void;
  isClusterMapActive: boolean;
  onToggleClusterMap: () => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filters, setFilters, isRotating, setIsRotating, showLabels, setShowLabels,
  isTourRunning, onStartTour, onStopTour, isGWRunning, selectedGWEvent, onSelectGWEvent, onStartGW, onStopGW,
  isPlayerMode, onStartPlayerMode, isCMBProofActive, onToggleCMBProof,
  isParityActive, onToggleParity, isAxisOfEvilActive, onToggleAxisOfEvil, isDarkFlowActive, onToggleDarkFlow,
  isGWGraveyardActive, onToggleGWGraveyard, isMONDActive, onToggleMOND, isRadioGhostsActive, onToggleRadioGhosts,
  isWideBinariesActive, onToggleWideBinaries, isFRBActive, onToggleFRB, isKSZActive, onToggleKSZ,
  isDESIActive, onToggleDESI, isClusterMapActive, onToggleClusterMap
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

  const isOtherModeRunning = isTourRunning || isGWRunning;

  return (
    <div className="absolute top-16 left-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-[260px]">
      <h3 className="text-white font-bold mb-3">Controls</h3>

      {/* Evidence Layers (Directives QQQQ, RRRR, SSSS) */}
      <div className="mb-3 space-y-1.5">
        <label className="text-cyan-400 text-xs font-bold block">TOPOLOGY EVIDENCE</label>

        {/* CMB Matched Circles (Phase 4) */}
        <button
          onClick={onToggleCMBProof}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isCMBProofActive
              ? 'bg-yellow-900/50 text-yellow-400 border-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-yellow-500/50 hover:text-yellow-300'
          }`}
        >
          <span>CMB Circles</span>
          <span className={`w-2 h-2 rounded-full ${isCMBProofActive ? 'bg-yellow-400' : 'bg-slate-600'}`} />
        </button>

        {/* Parity Asymmetry (QQQQ) */}
        <button
          onClick={onToggleParity}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isParityActive
              ? 'bg-cyan-900/50 text-cyan-400 border-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-cyan-500/50 hover:text-cyan-300'
          }`}
        >
          <span>Z₂ Parity</span>
          <span className={`w-2 h-2 rounded-full ${isParityActive ? 'bg-cyan-400' : 'bg-slate-600'}`} />
        </button>

        {/* Axis of Evil (RRRR) */}
        <button
          onClick={onToggleAxisOfEvil}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isAxisOfEvilActive
              ? 'bg-yellow-900/50 text-yellow-400 border-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-yellow-500/50 hover:text-yellow-300'
          }`}
        >
          <span>Axis of Evil</span>
          <span className={`w-2 h-2 rounded-full ${isAxisOfEvilActive ? 'bg-yellow-400' : 'bg-slate-600'}`} />
        </button>

        {/* Dark Flow (SSSS) */}
        <button
          onClick={onToggleDarkFlow}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isDarkFlowActive
              ? 'bg-red-900/50 text-red-400 border-red-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-red-500/50 hover:text-red-300'
          }`}
        >
          <span>Dark Flow</span>
          <span className={`w-2 h-2 rounded-full ${isDarkFlowActive ? 'bg-red-400' : 'bg-slate-600'}`} />
        </button>

        {/* GW Graveyard (TTTT) */}
        <button
          onClick={onToggleGWGraveyard}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isGWGraveyardActive
              ? 'bg-purple-900/50 text-purple-400 border-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-purple-500/50 hover:text-purple-300'
          }`}
        >
          <span>GW Graveyard</span>
          <span className={`w-2 h-2 rounded-full ${isGWGraveyardActive ? 'bg-purple-400' : 'bg-slate-600'}`} />
        </button>

        {/* MOND Gravity (UUUU) */}
        <button
          onClick={onToggleMOND}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isMONDActive
              ? 'bg-green-900/50 text-green-400 border-green-500 shadow-[0_0_10px_rgba(34,197,94,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-green-500/50 hover:text-green-300'
          }`}
        >
          <span>MOND Lensing</span>
          <span className={`w-2 h-2 rounded-full ${isMONDActive ? 'bg-green-400' : 'bg-slate-600'}`} />
        </button>

        {/* Radio Ghosts (VVVV) */}
        <button
          onClick={onToggleRadioGhosts}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isRadioGhostsActive
              ? 'bg-orange-900/50 text-orange-400 border-orange-500 shadow-[0_0_10px_rgba(251,146,60,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-orange-500/50 hover:text-orange-300'
          }`}
        >
          <span>Radio Ghosts</span>
          <span className={`w-2 h-2 rounded-full ${isRadioGhostsActive ? 'bg-orange-400' : 'bg-slate-600'}`} />
        </button>

        {/* Wide Binaries (WWWW) */}
        <button
          onClick={onToggleWideBinaries}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isWideBinariesActive
              ? 'bg-emerald-900/50 text-emerald-400 border-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-emerald-500/50 hover:text-emerald-300'
          }`}
        >
          <span>Wide Binaries</span>
          <span className={`w-2 h-2 rounded-full ${isWideBinariesActive ? 'bg-emerald-400' : 'bg-slate-600'}`} />
        </button>

        {/* FRB Tomography (XXXX) */}
        <button
          onClick={onToggleFRB}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isFRBActive
              ? 'bg-teal-900/50 text-teal-400 border-teal-500 shadow-[0_0_10px_rgba(20,184,166,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-teal-500/50 hover:text-teal-300'
          }`}
        >
          <span>FRB Tomography</span>
          <span className={`w-2 h-2 rounded-full ${isFRBActive ? 'bg-teal-400' : 'bg-slate-600'}`} />
        </button>

        {/* kSZ Cosmic Wind (YYYY) */}
        <button
          onClick={onToggleKSZ}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isKSZActive
              ? 'bg-amber-900/50 text-amber-400 border-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-amber-500/50 hover:text-amber-300'
          }`}
        >
          <span>kSZ Wind</span>
          <span className={`w-2 h-2 rounded-full ${isKSZActive ? 'bg-amber-400' : 'bg-slate-600'}`} />
        </button>

        {/* DESI Galaxies */}
        <button
          onClick={onToggleDESI}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isDESIActive
              ? 'bg-blue-900/50 text-blue-400 border-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-blue-500/50 hover:text-blue-300'
          }`}
        >
          <span>DESI Galaxies</span>
          <span className={`w-2 h-2 rounded-full ${isDESIActive ? 'bg-blue-400' : 'bg-slate-600'}`} />
        </button>

        {/* Galaxy Clusters */}
        <button
          onClick={onToggleClusterMap}
          disabled={isOtherModeRunning || isPlayerMode}
          className={`w-full px-3 py-1.5 text-xs uppercase tracking-wider transition-all border rounded flex items-center justify-between ${
            isClusterMapActive
              ? 'bg-yellow-900/50 text-yellow-400 border-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.3)]'
              : 'bg-slate-800/50 text-slate-400 border-slate-600 hover:border-yellow-500/50 hover:text-yellow-300'
          }`}
        >
          <span>Galaxy Clusters</span>
          <span className={`w-2 h-2 rounded-full ${isClusterMapActive ? 'bg-yellow-400' : 'bg-slate-600'}`} />
        </button>
      </div>

      {/* Player Mode Button (Directive WWW) - Primary action */}
      <button
        onClick={onStartPlayerMode}
        disabled={isOtherModeRunning || isPlayerMode}
        className={`w-full mb-2 px-4 py-3 font-bold text-sm uppercase tracking-wider transition-all border-2 rounded ${
          isPlayerMode
            ? 'bg-purple-900/50 text-purple-400 border-purple-500 animate-pulse'
            : isOtherModeRunning
            ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
            : 'bg-purple-900/60 text-purple-300 border-purple-400 hover:bg-purple-800/80 hover:shadow-[0_0_25px_rgba(168,85,247,0.5)] hover:scale-[1.02]'
        }`}
      >
        🚀 START CRAFT
      </button>

      {/* Cinematic Tour Button */}
      <button
        onClick={isTourRunning ? onStopTour : onStartTour}
        disabled={isGWRunning || isPlayerMode}
        className={`w-full mb-2 px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
          isTourRunning
            ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
            : (isGWRunning || isPlayerMode)
            ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
            : 'bg-cyan-900/50 text-cyan-400 border-cyan-500 hover:bg-cyan-900/80'
        }`}
      >
        {isTourRunning ? '■ STOP' : '▶ CINEMATIC TOUR'}
      </button>

      {/* GW Event Selector & Simulation */}
      <div className="mb-4 space-y-2">
        <label className="text-orange-400 text-xs font-bold block">GRAVITATIONAL WAVE EVENT</label>
        <select
          value={selectedGWEvent.id}
          onChange={(e) => {
            const event = GW_EVENTS.find(ev => ev.id === e.target.value);
            if (event) onSelectGWEvent(event);
          }}
          disabled={isGWRunning || isTourRunning || isPlayerMode}
          className="w-full bg-slate-800 text-white text-xs p-2 rounded border border-orange-500/50 focus:border-orange-400 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <optgroup label="Historic Firsts">
            {GW_EVENTS.filter(e => ['GW150914', 'GW170817'].includes(e.id)).map(event => (
              <option key={event.id} value={event.id}>
                {event.id} - {event.type} ({event.mass1_solar}+{event.mass2_solar}M☉)
              </option>
            ))}
          </optgroup>
          <optgroup label="Extreme Mass">
            {GW_EVENTS.filter(e => ['GW190521', 'GW231123'].includes(e.id)).map(event => (
              <option key={event.id} value={event.id}>
                {event.id} - {event.type} ({event.mass1_solar}+{event.mass2_solar}M☉)
              </option>
            ))}
          </optgroup>
          <optgroup label="Mass Gap / Precision">
            {GW_EVENTS.filter(e => ['GW190814', 'GW230627', 'GW240615', 'GW250114'].includes(e.id)).map(event => (
              <option key={event.id} value={event.id}>
                {event.id} - {event.type} ({event.mass1_solar}+{event.mass2_solar}M☉)
              </option>
            ))}
          </optgroup>
          <optgroup label="NS-BH Mergers">
            {GW_EVENTS.filter(e => ['GW200115', 'GW230518'].includes(e.id)).map(event => (
              <option key={event.id} value={event.id}>
                {event.id} - {event.type} ({event.mass1_solar}+{event.mass2_solar}M☉)
              </option>
            ))}
          </optgroup>
          <optgroup label="Distant Events">
            {GW_EVENTS.filter(e => ['GW250118', 'GW250108'].includes(e.id)).map(event => (
              <option key={event.id} value={event.id}>
                {event.id} - {event.type} ({event.distance_gpc.toFixed(1)} Gpc)
              </option>
            ))}
          </optgroup>
        </select>
        <div className="text-[10px] text-slate-400 px-1">
          {selectedGWEvent.description}
        </div>
        <button
          onClick={isGWRunning ? onStopGW : onStartGW}
          disabled={isTourRunning || isPlayerMode}
          className={`w-full px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
            isGWRunning
              ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
              : (isTourRunning || isPlayerMode)
              ? 'bg-slate-800/50 text-slate-500 border-slate-600 cursor-not-allowed'
              : 'bg-orange-900/50 text-orange-400 border-orange-500 hover:bg-orange-900/80'
          }`}
        >
          {isGWRunning ? '■ STOP SIMULATION' : '▶ SIMULATE GW'}
        </button>
      </div>

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

  // Track isTourRunning in a ref to avoid stale closure
  const isTourRunningRef = useRef(isTourRunning);
  useEffect(() => {
    isTourRunningRef.current = isTourRunning;
  }, [isTourRunning]);

  useFrame((state, delta) => {
    if (!isTourRunningRef.current || !isAnimating.current) return;

    const segmentIndex = currentSegment.current;

    // Debug logging every 60 frames
    if (Math.floor(state.clock.elapsedTime * 60) % 60 === 0) {
      const nextWp = TOPOLOGY_TOUR[segmentIndex + 1];
      console.log(`Segment ${segmentIndex}, next type: ${nextWp?.type}, progress: ${segmentProgress.current.toFixed(2)}`);
    }

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
        console.log('=== TELEPORT WAYPOINT REACHED ===');
        console.log('Type:', toWaypoint.type, 'Axis:', toWaypoint.boundaryAxis);

        // Execute the teleport
        camera.position.copy(toWaypoint.position);
        lookAtTarget.current.copy(toWaypoint.lookAt);

        // Trigger effects using refs (avoids stale closure)
        if (toWaypoint.type === 'boundary_cross' && toWaypoint.boundaryAxis) {
          console.log('>>> CALLING onBoundaryCross with:', toWaypoint.boundaryAxis);
          onBoundaryCrossRef.current(toWaypoint.boundaryAxis);
        }
        if (toWaypoint.type === 'z2_demo') {
          console.log('>>> CALLING onParityFlip');
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
// CMB CAMERA CONTROLLER (Phase 4 - CMB Proof Flight)
// Smooth camera animation to view the matched topology circles
// =============================================================================

const CMBCameraController: React.FC<{
  isCMBProofActive: boolean;
  controlsRef: React.RefObject<any>;
}> = ({ isCMBProofActive, controlsRef }) => {
  const { camera } = useThree();
  const hasAnimatedRef = useRef(false);
  const isFlightCompleteRef = useRef(false);
  const originalPositionRef = useRef<THREE.Vector3 | null>(null);
  const originalTargetRef = useRef<THREE.Vector3 | null>(null);
  const startTimeRef = useRef<number | null>(null);

  useEffect(() => {
    if (isCMBProofActive && !hasAnimatedRef.current) {
      // Store original camera state
      originalPositionRef.current = camera.position.clone();
      if (controlsRef.current) {
        originalTargetRef.current = controlsRef.current.target.clone();
      }

      // Get CMB view position
      const cmbView = getCMBViewPosition();
      isFlightCompleteRef.current = false;

      // Animate camera to CMB view - smooth flight
      gsap.to(camera.position, {
        x: cmbView.position.x,
        y: cmbView.position.y,
        z: cmbView.position.z,
        duration: 4,
        ease: 'power2.inOut',
        onComplete: () => {
          isFlightCompleteRef.current = true;
          startTimeRef.current = null; // Reset for orbit
        }
      });

      if (controlsRef.current) {
        gsap.to(controlsRef.current.target, {
          x: cmbView.target.x,
          y: cmbView.target.y,
          z: cmbView.target.z,
          duration: 4,
          ease: 'power2.inOut',
        });
      }

      hasAnimatedRef.current = true;
    } else if (!isCMBProofActive && hasAnimatedRef.current) {
      // Return to original position
      isFlightCompleteRef.current = false;

      if (originalPositionRef.current) {
        gsap.to(camera.position, {
          x: originalPositionRef.current.x,
          y: originalPositionRef.current.y,
          z: originalPositionRef.current.z,
          duration: 3,
          ease: 'power2.inOut',
        });
      }

      if (controlsRef.current && originalTargetRef.current) {
        gsap.to(controlsRef.current.target, {
          x: originalTargetRef.current.x,
          y: originalTargetRef.current.y,
          z: originalTargetRef.current.z,
          duration: 3,
          ease: 'power2.inOut',
        });
      }

      hasAnimatedRef.current = false;
    }
  }, [isCMBProofActive, camera, controlsRef]);

  // Very slow rotation ONLY after flight is complete - no bouncing
  useFrame((state) => {
    if (isCMBProofActive && isFlightCompleteRef.current && controlsRef.current) {
      // Initialize start time on first frame after flight
      if (startTimeRef.current === null) {
        startTimeRef.current = state.clock.elapsedTime;
      }

      const elapsed = state.clock.elapsedTime - startTimeRef.current;
      const cmbView = getCMBViewPosition();
      const radius = cmbView.position.length();
      const rotationSpeed = 0.015; // Very slow

      // Calculate orbit position based on initial CMB view angle
      const baseAngle = Math.atan2(cmbView.position.z, cmbView.position.x);
      const currentAngle = baseAngle + elapsed * rotationSpeed;

      // Smooth orbit at fixed radius and height
      camera.position.x = Math.cos(currentAngle) * radius * 0.85;
      camera.position.z = Math.sin(currentAngle) * radius * 0.85;
      camera.position.y = cmbView.position.y; // Keep height stable

      camera.lookAt(0, 0, 0);
      controlsRef.current.target.set(0, 0, 0);
    }
  });

  return null;
};

// =============================================================================
// BOUNDARY RUPTURE OVERLAY (Directive VVV)
// Smooth cinematic transition when crossing T³ boundaries or Z₂ parity flip
// =============================================================================

const BoundaryRuptureOverlay: React.FC<{
  isActive: boolean;
  axis: string | null;
  isParityFlip: boolean;
}> = ({ isActive, axis, isParityFlip }) => {
  if (!isActive) return null;

  const color = isParityFlip ? '#a855f7' : '#22d3ee';

  return (
    <div
      className="absolute inset-0 pointer-events-none flex items-center justify-center"
      style={{ zIndex: 9999 }}
    >
      {/* Smooth vignette overlay */}
      <div
        className="absolute inset-0"
        style={{
          background: `radial-gradient(ellipse at center, transparent 30%, ${color}30 100%)`,
          animation: 'smooth-vignette 2s ease-in-out forwards',
        }}
      />

      {/* Subtle horizontal line sweep */}
      <div
        className="absolute inset-0 overflow-hidden"
        style={{
          animation: 'line-sweep 2s ease-in-out forwards',
        }}
      >
        <div
          className="absolute left-0 right-0 h-1"
          style={{
            background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
            boxShadow: `0 0 30px 10px ${color}`,
            top: '50%',
            transform: 'translateY(-50%)',
          }}
        />
      </div>

      {/* Main text overlay - smooth fade */}
      <div
        className="text-center relative"
        style={{
          animation: 'smooth-text 2s ease-in-out forwards',
        }}
      >
        <div
          className={`text-3xl md:text-4xl font-bold tracking-wide mb-3 ${
            isParityFlip ? 'text-purple-200' : 'text-cyan-200'
          }`}
          style={{
            textShadow: `0 0 40px ${color}`,
            letterSpacing: '0.15em',
          }}
        >
          {isParityFlip ? 'Z₂ PARITY INVERSION' : 'T³ BOUNDARY TRANSITION'}
        </div>
        <div
          className="text-xl md:text-2xl text-white/90 font-mono"
          style={{
            textShadow: `0 0 20px ${color}80`,
          }}
        >
          {isParityFlip
            ? 'p → −p'
            : `${axis?.toUpperCase()}: +${HALF_BOX.toFixed(1)} ↔ −${HALF_BOX.toFixed(1)} Gpc`}
        </div>
      </div>

      {/* Subtle corner accents */}
      {[
        { top: 20, left: 20 },
        { top: 20, right: 20 },
        { bottom: 20, left: 20 },
        { bottom: 20, right: 20 },
      ].map((pos, i) => (
        <div
          key={i}
          className="absolute w-12 h-12"
          style={{
            ...pos,
            borderTop: i < 2 ? `2px solid ${color}80` : 'none',
            borderBottom: i >= 2 ? `2px solid ${color}80` : 'none',
            borderLeft: i % 2 === 0 ? `2px solid ${color}80` : 'none',
            borderRight: i % 2 === 1 ? `2px solid ${color}80` : 'none',
            animation: 'smooth-corners 2s ease-in-out forwards',
          }}
        />
      ))}

      {/* Inline keyframe styles - all smooth, no bounce */}
      <style>{`
        @keyframes smooth-vignette {
          0% { opacity: 0; }
          15% { opacity: 1; }
          85% { opacity: 1; }
          100% { opacity: 0; }
        }
        @keyframes smooth-text {
          0% { opacity: 0; transform: translateY(10px); }
          15% { opacity: 1; transform: translateY(0); }
          85% { opacity: 1; transform: translateY(0); }
          100% { opacity: 0; transform: translateY(-10px); }
        }
        @keyframes smooth-corners {
          0% { opacity: 0; transform: scale(0.8); }
          15% { opacity: 1; transform: scale(1); }
          85% { opacity: 1; transform: scale(1); }
          100% { opacity: 0; transform: scale(1.1); }
        }
        @keyframes line-sweep {
          0% { opacity: 0; }
          10% { opacity: 1; }
          50% { opacity: 1; }
          100% { opacity: 0; }
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
  selectedGWEvent: GWEvent;
  onGWProgressUpdate: (progress: number, phase: number, waveRadius: number) => void;
}> = ({ filters, isRotating, showLabels, isTourRunning, onCameraDistanceChange, isGWRunning, selectedGWEvent, onGWProgressUpdate }) => {
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

      {/* Gravitational Wave Simulation */}
      {isGWRunning && <GWSimulation isRunning={isGWRunning} selectedEvent={selectedGWEvent} onProgressUpdate={onGWProgressUpdate} />}
    </group>
  );
};

// =============================================================================
// SCENE
// =============================================================================

// FPS Monitor Component
const FPSMonitor: React.FC<{ onFPSUpdate: (fps: number) => void }> = ({ onFPSUpdate }) => {
  const framesRef = useRef<number[]>([]);
  const lastTimeRef = useRef(performance.now());

  useFrame(() => {
    const now = performance.now();
    const delta = now - lastTimeRef.current;
    lastTimeRef.current = now;

    framesRef.current.push(delta);
    if (framesRef.current.length > 30) {
      framesRef.current.shift();
    }

    // Calculate FPS every 10 frames to avoid excessive updates
    if (framesRef.current.length % 10 === 0) {
      const avgDelta = framesRef.current.reduce((a, b) => a + b, 0) / framesRef.current.length;
      const fps = Math.round(1000 / avgDelta);
      onFPSUpdate(fps);
    }
  });

  return null;
};

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
  selectedGWEvent: GWEvent;
  onGWProgressUpdate: (progress: number, phase: number, waveRadius: number) => void;
  // Player Mode props (Directive WWW)
  isPlayerMode: boolean;
  // CMB Proof props (Phase 4)
  isCMBProofActive: boolean;
  // Evidence Layer props (Directives QQQQ, RRRR, SSSS)
  isParityActive: boolean;
  isAxisOfEvilActive: boolean;
  isDarkFlowActive: boolean;
  // Evidence Layer props (Directives TTTT, UUUU, VVVV)
  isGWGraveyardActive: boolean;
  isMONDActive: boolean;
  isRadioGhostsActive: boolean;
  // Evidence Layer props (Directives WWWW, XXXX, YYYY)
  isWideBinariesActive: boolean;
  isFRBActive: boolean;
  isKSZActive: boolean;
  // Survey data layers
  isDESIActive: boolean;
  isClusterMapActive: boolean;
  // Performance monitoring
  onFPSUpdate: (fps: number) => void;
}> = ({ filters, isRotating, showLabels, isTourRunning, onTourComplete, onWaypointChange, onCameraDistanceChange, onBoundaryCross, onParityFlip, isGWRunning, selectedGWEvent, onGWProgressUpdate, isPlayerMode, isCMBProofActive, isParityActive, isAxisOfEvilActive, isDarkFlowActive, isGWGraveyardActive, isMONDActive, isRadioGhostsActive, isWideBinariesActive, isFRBActive, isKSZActive, isDESIActive, isClusterMapActive, onFPSUpdate }) => {
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
        selectedGWEvent={selectedGWEvent}
        onGWProgressUpdate={onGWProgressUpdate}
        onCameraDistanceChange={onCameraDistanceChange}
      />

      {/* CMB Evidence Layer (Phase 4 - Topology Proof) */}
      <CMBEvidenceLayer visible={isCMBProofActive} />

      {/* Evidence Layers (Directives QQQQ, RRRR, SSSS) */}
      <CMBParitySphere visible={isParityActive} />
      <IsotropyBreaker visible={isAxisOfEvilActive} />
      <KinematicFlowMap visible={isDarkFlowActive} />

      {/* Evidence Layers (Directives TTTT, UUUU, VVVV) */}
      {isGWGraveyardActive && <GravitationalGraveyard />}
      {isMONDActive && <GeometricGravity position={[0, -3, 0]} scale={4} />}
      {isRadioGhostsActive && <RadioMirrors />}

      {/* Evidence Layers (Directives WWWW, XXXX, YYYY) */}
      {isWideBinariesActive && <LocalMONDAnchor />}
      {isFRBActive && <DispersionTomography />}
      {isKSZActive && <CosmicWindShader />}

      {/* Survey data layers */}
      {isDESIActive && <DESIGalaxies />}
      {isClusterMapActive && <GalaxyClusterMap visible={true} />}

      <CinematicCamera
        isTourRunning={isTourRunning}
        onTourComplete={onTourComplete}
        onWaypointChange={onWaypointChange}
        onBoundaryCross={onBoundaryCross}
        onParityFlip={onParityFlip}
        controlsRef={controlsRef}
      />

      {/* CMB Camera Flight Controller */}
      <CMBCameraController
        isCMBProofActive={isCMBProofActive}
        controlsRef={controlsRef}
      />

      {/* Player Mode Controller (Directive XXX) */}
      {isPlayerMode && (
        <PlayerController
          onBoundaryCross={onBoundaryCross}
          onParityFlip={onParityFlip}
        />
      )}

      {/* Multiplayer Other Players (Firebase Realtime) */}
      {isPlayerMode && <OtherPlayersRenderer />}

      {/* Disable OrbitControls during player mode or CMB proof */}
      {/* HYPERREAL: minDistance allows zoom to Earth surface scale (~1e-20 Gpc) */}
      <OrbitControls
        ref={controlsRef}
        enabled={!isPlayerMode && !isCMBProofActive}
        enablePan enableZoom enableRotate
        minDistance={1e-22}
        maxDistance={100}
        zoomSpeed={1.5}
        rotateSpeed={0.5}
        enableDamping
        dampingFactor={0.05}
      />
      {/* HYPERREAL: Camera supports zoom from cosmic scale (100 Gpc) to Earth surface (~1e-20 Gpc) */}
      {/* Logarithmic depth buffer handles this 22 order of magnitude range */}
      <PerspectiveCamera makeDefault position={[0.00005, 0.00003, 0.00005]} fov={50} near={1e-24} far={1000} />

      {/* FPS Monitoring */}
      <FPSMonitor onFPSUpdate={onFPSUpdate} />
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
    survey: false,  // DISABLED: Was 30,000 SIMULATED random positions (not real data). Use DESI Galaxies toggle instead for real data.
    lymanAlpha: false,  // Off by default (can clutter at cosmic scale)
    baoSpheres: false,  // Off by default (toggle to show)
    kszVectors: false,  // Off by default (toggle to show)
  });

  const [isRotating, setIsRotating] = useState(false);
  const [showLabels, setShowLabels] = useState(true);
  const [isTourRunning, setIsTourRunning] = useState(false);
  const [tourText, setTourText] = useState('');

  // CMB Proof Mode state (Phase 4)
  const [isCMBProofActive, setIsCMBProofActive] = useState(false);
  const [cameraDistance, setCameraDistance] = useState(3);

  // Evidence Layers state (Directives QQQQ, RRRR, SSSS)
  const [isParityActive, setIsParityActive] = useState(false);
  const [isAxisOfEvilActive, setIsAxisOfEvilActive] = useState(false);
  const [isDarkFlowActive, setIsDarkFlowActive] = useState(false);

  // Evidence Layers state (Directives TTTT, UUUU, VVVV)
  const [isGWGraveyardActive, setIsGWGraveyardActive] = useState(false);
  const [isMONDActive, setIsMONDActive] = useState(false);
  const [isRadioGhostsActive, setIsRadioGhostsActive] = useState(false);

  // Evidence Layers state (Directives WWWW, XXXX, YYYY)
  const [isWideBinariesActive, setIsWideBinariesActive] = useState(false);
  const [isFRBActive, setIsFRBActive] = useState(false);
  const [isKSZActive, setIsKSZActive] = useState(false);

  // Survey data layers
  const [isDESIActive, setIsDESIActive] = useState(false);
  const [isClusterMapActive, setIsClusterMapActive] = useState(false);

  // Onboarding overlay state (shows scroll instructions on first visit)
  const [showOnboarding, setShowOnboarding] = useState(true);

  // Performance monitoring
  const [fps, setFps] = useState(60);

  // GW Simulation State
  const [isGWRunning, setIsGWRunning] = useState(false);
  const [selectedGWEvent, setSelectedGWEvent] = useState<GWEvent>(GW_EVENTS[2]); // Default to GW190521
  const [gwProgress, setGWProgress] = useState(0);
  const [gwPhase, setGWPhase] = useState(0);
  const [gwWaveRadius, setGWWaveRadius] = useState(0);

  // Boundary crossing state (Directive VVV)
  const [isRuptureActive, setIsRuptureActive] = useState(false);
  const [ruptureAxis, setRuptureAxis] = useState<string | null>(null);
  const [isParityFlip, setIsParityFlip] = useState(false);

  // Player Mode state (Directives WWW, XXX, YYY, ZZZ)
  const { isPlayerMode, isSelectingVessel, openVesselSelector, stopPlayerMode } = usePlayerStore();

  // ESC key to exit player mode
  useEffect(() => {
    if (!isPlayerMode) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Escape') {
        stopPlayerMode();
        // Exit pointer lock
        if (document.pointerLockElement) {
          document.exitPointerLock();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isPlayerMode, stopPlayerMode]);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.stopPropagation();
    // Dismiss onboarding on scroll
    if (showOnboarding) setShowOnboarding(false);
  }, [showOnboarding]);

  // Auto-dismiss onboarding after 8 seconds
  useEffect(() => {
    if (showOnboarding) {
      const timer = setTimeout(() => setShowOnboarding(false), 8000);
      return () => clearTimeout(timer);
    }
  }, [showOnboarding]);

  // Dismiss onboarding on any click or key
  useEffect(() => {
    if (!showOnboarding) return;
    const dismiss = () => setShowOnboarding(false);
    window.addEventListener('click', dismiss);
    window.addEventListener('keydown', dismiss);
    return () => {
      window.removeEventListener('click', dismiss);
      window.removeEventListener('keydown', dismiss);
    };
  }, [showOnboarding]);
  const handleStartTour = useCallback(() => {
    setIsTourRunning(true);
    setIsRotating(false);
  }, []);
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

  // CMB Proof Handler (Phase 4)
  const handleToggleCMBProof = useCallback(() => {
    setIsCMBProofActive((prev) => !prev);
    if (!isCMBProofActive) {
      setIsRotating(false); // Disable rotation when entering CMB mode
    }
  }, [isCMBProofActive]);

  // Evidence Layer Handlers (Directives QQQQ, RRRR, SSSS)
  const handleToggleParity = useCallback(() => {
    setIsParityActive((prev) => !prev);
  }, []);

  const handleToggleAxisOfEvil = useCallback(() => {
    setIsAxisOfEvilActive((prev) => !prev);
  }, []);

  const handleToggleDarkFlow = useCallback(() => {
    setIsDarkFlowActive((prev) => !prev);
  }, []);

  return (
    <div className="relative w-full h-[800px] bg-slate-950 rounded-lg overflow-hidden" onWheel={handleWheel}>
      {/* Hide regular UI when in Player Mode */}
      {!isPlayerMode && <ScaleIndicator cameraDistance={cameraDistance} />}

      {!isPlayerMode && <FilterPanel
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
        selectedGWEvent={selectedGWEvent}
        onSelectGWEvent={setSelectedGWEvent}
        onStartGW={handleStartGW}
        onStopGW={handleStopGW}
        isPlayerMode={isPlayerMode}
        onStartPlayerMode={openVesselSelector}
        isCMBProofActive={isCMBProofActive}
        onToggleCMBProof={handleToggleCMBProof}
        isParityActive={isParityActive}
        onToggleParity={handleToggleParity}
        isAxisOfEvilActive={isAxisOfEvilActive}
        onToggleAxisOfEvil={handleToggleAxisOfEvil}
        isDarkFlowActive={isDarkFlowActive}
        onToggleDarkFlow={handleToggleDarkFlow}
        isGWGraveyardActive={isGWGraveyardActive}
        onToggleGWGraveyard={() => setIsGWGraveyardActive(p => !p)}
        isMONDActive={isMONDActive}
        onToggleMOND={() => setIsMONDActive(p => !p)}
        isRadioGhostsActive={isRadioGhostsActive}
        onToggleRadioGhosts={() => setIsRadioGhostsActive(p => !p)}
        isWideBinariesActive={isWideBinariesActive}
        onToggleWideBinaries={() => setIsWideBinariesActive(p => !p)}
        isFRBActive={isFRBActive}
        onToggleFRB={() => setIsFRBActive(p => !p)}
        isKSZActive={isKSZActive}
        onToggleKSZ={() => setIsKSZActive(p => !p)}
        isDESIActive={isDESIActive}
        onToggleDESI={() => setIsDESIActive(p => !p)}
        isClusterMapActive={isClusterMapActive}
        onToggleClusterMap={() => setIsClusterMapActive(p => !p)}
      />}

      {!isPlayerMode && <div className="absolute top-16 right-4 bg-slate-900/95 p-3 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-[200px]">
        <h3 className="text-white font-bold text-sm mb-1">Z² Digital Twin</h3>
        <p className="text-slate-400 text-[10px] leading-relaxed">
          Zoom from planets to the 20.6 Gpc cosmic horizon. All scales unified in T³/Z₂ topology.
        </p>
      </div>}

      {isTourRunning && tourText && (
        <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-20 max-w-2xl">
          <div className="bg-black/90 text-white font-mono text-lg border border-cyan-500 px-6 py-4 rounded-lg shadow-[0_0_30px_rgba(6,182,212,0.4)]">
            <p>{tourText}</p>
          </div>
        </div>
      )}

      {/* GW Simulation HUD */}
      <GWSimulationHUD
        isRunning={isGWRunning}
        selectedEvent={selectedGWEvent}
        progress={gwProgress}
        phase={gwPhase}
        waveRadius={gwWaveRadius}
      />

      {/* CMB Evidence HUD (Phase 4 - Topology Proof) */}
      <CMBEvidenceHUD visible={isCMBProofActive} />

      {/* Evidence Layer HUDs (Directives QQQQ, RRRR, SSSS) */}
      <ParityEvidenceHUD visible={isParityActive} />
      <IsotropyBreakerHUD visible={isAxisOfEvilActive} />
      <DarkFlowHUD visible={isDarkFlowActive} />

      {/* Evidence Layer HUDs (Directives TTTT, UUUU, VVVV) */}
      {isGWGraveyardActive && <GraveyardHUD events={[]} clusteringRatio={0.38} />}
      {isMONDActive && <MONDHUD totalLenses={16} deepMONDCount={3} transitionCount={5} newtonianCount={8} maxSourceRedshift={9.1} />}
      {isRadioGhostsActive && <RadioGhostHUD totalSources={20} mirrorCandidates={169} bestGhostProb={0.623} orcClustering={0.37} />}

      {/* Evidence Layer HUDs (Directives WWWW, XXXX, YYYY) */}
      {isWideBinariesActive && <WideBinaryHUD deepMondCount={11} transitionalCount={3} newtonianCount={2} meanBoostDeepMond={1.62} meanBoostNewtonian={1.02} />}
      {isFRBActive && <DispersionHUD totalFRBs={19} axisCount={8} diagonalCount={9} anisotropyRatio={0.14} maxDM={1426} />}
      {isKSZActive && <CosmicWindHUD totalClusters={14} windMagnitude={1271} windDirection={{ l: 262.6, b: -18.7 }} bestAxis="Y" alignmentAngle={20.1} />}
      {isDESIActive && <DESIGalaxiesHUD visible={isDESIActive} />}
      {isClusterMapActive && <ClusterMapHUD visible={isClusterMapActive} comaMembers={800} virgoMembers={600} shapleyMembers={900} />}

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
          selectedGWEvent={selectedGWEvent}
          onGWProgressUpdate={(progress, phase, waveRadius) => {
            setGWProgress(progress);
            setGWPhase(phase);
            setGWWaveRadius(waveRadius);
            // Auto-stop when simulation completes
            if (progress >= 1) {
              handleStopGW();
            }
          }}
          isPlayerMode={isPlayerMode}
          isCMBProofActive={isCMBProofActive}
          isParityActive={isParityActive}
          isAxisOfEvilActive={isAxisOfEvilActive}
          isDarkFlowActive={isDarkFlowActive}
          isGWGraveyardActive={isGWGraveyardActive}
          isMONDActive={isMONDActive}
          isRadioGhostsActive={isRadioGhostsActive}
          isWideBinariesActive={isWideBinariesActive}
          isFRBActive={isFRBActive}
          isKSZActive={isKSZActive}
          isDESIActive={isDESIActive}
          isClusterMapActive={isClusterMapActive}
          onFPSUpdate={setFps}
        />
      </Canvas>

      {/* Boundary Rupture Overlay (Directive VVV) - MUST be after Canvas to render on top */}
      <BoundaryRuptureOverlay
        isActive={isRuptureActive}
        axis={ruptureAxis}
        isParityFlip={isParityFlip}
      />

      {/* Player Mode Overlays (Directives WWW, XXX) */}
      <VesselSelector />
      <PlayerHUD />
      <MultiplayerHUD />

      {/* Onboarding Overlay - shows scroll instructions on first load */}
      {/* z-[9999] ensures it's above drei Html labels which have their own stacking context */}
      {showOnboarding && !isPlayerMode && (
        <div className="absolute inset-0 flex items-center justify-center z-[9999] pointer-events-none">
          <div className="bg-black/95 backdrop-blur-xl border-2 border-cyan-400 rounded-xl p-10 max-w-lg text-center shadow-[0_0_80px_rgba(0,255,255,0.5)]">
            <div className="text-cyan-400 text-7xl mb-6">⟳</div>
            <h2 className="text-white text-3xl font-bold mb-4">You are here</h2>
            <p className="text-slate-200 text-xl mb-6">
              Starting at the <span className="text-yellow-400 font-bold text-2xl">Milky Way</span>
            </p>
            <div className="flex items-center justify-center gap-4 text-cyan-400 text-2xl mb-6">
              <span className="text-4xl">↕</span>
              <span>Scroll to zoom out to the cosmos</span>
            </div>
            <div className="text-slate-400 text-base space-y-2">
              <p><span className="text-cyan-400 font-semibold">Drag</span> to rotate • <span className="text-cyan-400 font-semibold">Scroll</span> to zoom</p>
              <p className="text-sm mt-3 opacity-80">Click anywhere to dismiss</p>
            </div>
          </div>
        </div>
      )}

      {/* Clickable layer legend - Hide when in Player Mode */}
      {!isPlayerMode && (
        <div className="absolute bottom-4 right-4 bg-slate-900/95 p-2 rounded-lg border border-slate-700 z-10 text-[10px] space-y-0.5">
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.solarSystem ? 'text-yellow-400' : 'text-yellow-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, solarSystem: !prev.solarSystem }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.solarSystem ? 'bg-yellow-400' : 'bg-yellow-400/30 ring-1 ring-yellow-400/50'}`} />
            Solar System
          </div>
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.milkyWay ? 'text-blue-400' : 'text-blue-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, milkyWay: !prev.milkyWay }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.milkyWay ? 'bg-blue-400' : 'bg-blue-400/30 ring-1 ring-blue-400/50'}`} />
            Milky Way
          </div>
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.localGroup ? 'text-green-400' : 'text-green-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, localGroup: !prev.localGroup }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.localGroup ? 'bg-green-400' : 'bg-green-400/30 ring-1 ring-green-400/50'}`} />
            Local Group
          </div>
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.structures ? 'text-orange-400' : 'text-orange-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, structures: !prev.structures }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.structures ? 'bg-orange-400' : 'bg-orange-400/30 ring-1 ring-orange-400/50'}`} />
            Structures
          </div>
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.highZ ? 'text-fuchsia-400' : 'text-fuchsia-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, highZ: !prev.highZ }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.highZ ? 'bg-fuchsia-400' : 'bg-fuchsia-400/30 ring-1 ring-fuchsia-400/50'}`} />
            High-z / Ly-α
          </div>
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.baoSpheres ? 'text-cyan-400' : 'text-cyan-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, baoSpheres: !prev.baoSpheres }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.baoSpheres ? 'bg-cyan-400' : 'bg-cyan-400/30 ring-1 ring-cyan-400/50'}`} />
            BAO 150 Mpc
          </div>
          <div
            className={`flex items-center gap-1 cursor-pointer hover:bg-slate-800 px-1 rounded transition-opacity ${filters.kszVectors ? 'text-amber-400' : 'text-amber-400/30'}`}
            onClick={() => setFilters(prev => ({ ...prev, kszVectors: !prev.kszVectors }))}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${filters.kszVectors ? 'bg-amber-400' : 'bg-amber-400/30 ring-1 ring-amber-400/50'}`} />
            kSZ Outflows
          </div>
        </div>
      )}

      {/* Minimal FPS Counter */}
      <MinimalFPS fps={fps} />
    </div>
  );
};

export default MultiMessengerUniverse;
