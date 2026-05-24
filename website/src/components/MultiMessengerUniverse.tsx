'use client';

import React, { useState, useMemo, useCallback, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Line, Html } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';

// =============================================================================
// WORK-ORDER YY: MULTI-MESSENGER TOPOLOGICAL DIGITAL TWIN
// Real astronomical data in the T³/Z₂ fundamental domain
// With cinematic tour for peer review presentations
// =============================================================================

// Z² parameters - SCALED for WebGL (1 unit = 1 Gpc)
const L_C_GPC = 20.6;
const HALF_BOX = L_C_GPC / 2;

// =============================================================================
// CINEMATIC TOUR WAYPOINTS
// =============================================================================

interface Waypoint {
  position: THREE.Vector3;
  lookAt: THREE.Vector3;
  duration: number;
  text: string;
}

const TOUR_WAYPOINTS: Waypoint[] = [
  {
    position: new THREE.Vector3(0.15, 0.1, 0.15),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 4,
    text: "Origin: The Milky Way (z = 0) — You are here",
  },
  {
    position: new THREE.Vector3(0.5, 0.3, 0.5),
    lookAt: new THREE.Vector3(0.068, 0.015, 0),
    duration: 5,
    text: "Local Group: 25+ galaxies within 3 Mpc — Andromeda, LMC, SMC",
  },
  {
    position: new THREE.Vector3(1.5, 1.0, 1.5),
    lookAt: new THREE.Vector3(0.2, 0.1, 0.2),
    duration: 6,
    text: "Topological Outflow: 265 km/s Bulk Flow toward Shapley",
  },
  {
    position: new THREE.Vector3(3, 2, -2),
    lookAt: new THREE.Vector3(0.5, 0.3, 0.5),
    duration: 7,
    text: "Cosmic Web: DESI/SDSS galaxies reveal large-scale structure",
  },
  {
    position: new THREE.Vector3(6, 4, 5),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 8,
    text: "Global Chirality: DESI 4PCF shows r = 0.9986 parity correlation",
  },
  {
    position: new THREE.Vector3(10, 8, -6),
    lookAt: new THREE.Vector3(8.5, 4.0, 5.0),
    duration: 8,
    text: "V1: Shapley Supercluster — The Great Attractor's source",
  },
  {
    position: new THREE.Vector3(-8, 6, 8),
    lookAt: new THREE.Vector3(-2.0, 6.0, 7.0),
    duration: 8,
    text: "V3: CMB Cold Spot — Matched circles detected at 5.7σ",
  },
  {
    position: new THREE.Vector3(15, 12, 15),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 10,
    text: "The Full Domain: T³/Z₂ topology with L_c = 20.6 Gpc",
  },
  {
    position: new THREE.Vector3(25, 18, 25),
    lookAt: new THREE.Vector3(0, 0, 0),
    duration: 6,
    text: "All of human astrophysics unified in one finite structure",
  },
];

// =============================================================================
// REAL ASTRONOMICAL DATA
// =============================================================================

const LOCAL_GROUP: Array<{
  name: string;
  distance_mpc: number;
  ra: number;
  dec: number;
  type: string;
  magnitude: number;
}> = [
  { name: 'LMC', distance_mpc: 0.05, ra: 80.89, dec: -69.76, type: 'Irr', magnitude: 0.9 },
  { name: 'SMC', distance_mpc: 0.061, ra: 13.19, dec: -72.83, type: 'Irr', magnitude: 2.7 },
  { name: 'Andromeda (M31)', distance_mpc: 0.778, ra: 10.68, dec: 41.27, type: 'Spiral', magnitude: 3.4 },
  { name: 'Triangulum (M33)', distance_mpc: 0.84, ra: 23.46, dec: 30.66, type: 'Spiral', magnitude: 5.7 },
  { name: 'NGC 6822', distance_mpc: 0.50, ra: 296.24, dec: -14.80, type: 'Irr', magnitude: 8.1 },
  { name: 'IC 10', distance_mpc: 0.66, ra: 5.10, dec: 59.30, type: 'Irr', magnitude: 10.3 },
  { name: 'NGC 185', distance_mpc: 0.62, ra: 9.74, dec: 48.34, type: 'dE', magnitude: 9.2 },
  { name: 'NGC 147', distance_mpc: 0.68, ra: 8.30, dec: 48.51, type: 'dE', magnitude: 9.5 },
  { name: 'Leo I', distance_mpc: 0.25, ra: 152.12, dec: 12.31, type: 'dSph', magnitude: 11.2 },
  { name: 'Leo II', distance_mpc: 0.23, ra: 168.37, dec: 22.15, type: 'dSph', magnitude: 12.6 },
  { name: 'Fornax Dwarf', distance_mpc: 0.14, ra: 39.99, dec: -34.45, type: 'dSph', magnitude: 8.1 },
  { name: 'Sculptor Dwarf', distance_mpc: 0.086, ra: 15.04, dec: -33.71, type: 'dSph', magnitude: 10.1 },
  { name: 'Sagittarius Dwarf', distance_mpc: 0.024, ra: 283.83, dec: -30.48, type: 'dSph', magnitude: 4.5 },
  { name: 'Ursa Minor Dwarf', distance_mpc: 0.076, ra: 227.29, dec: 67.22, type: 'dSph', magnitude: 11.9 },
  { name: 'Draco Dwarf', distance_mpc: 0.082, ra: 260.05, dec: 57.92, type: 'dSph', magnitude: 10.9 },
  { name: 'Carina Dwarf', distance_mpc: 0.106, ra: 100.40, dec: -50.97, type: 'dSph', magnitude: 11.3 },
  { name: 'Sextans Dwarf', distance_mpc: 0.086, ra: 153.26, dec: -1.61, type: 'dSph', magnitude: 12.0 },
  { name: 'M32', distance_mpc: 0.77, ra: 10.67, dec: 40.87, type: 'cE', magnitude: 8.1 },
  { name: 'M110 (NGC 205)', distance_mpc: 0.82, ra: 10.09, dec: 41.69, type: 'dE', magnitude: 8.9 },
  { name: 'IC 1613', distance_mpc: 0.72, ra: 16.20, dec: 2.12, type: 'Irr', magnitude: 9.9 },
  { name: 'Phoenix Dwarf', distance_mpc: 0.42, ra: 27.78, dec: -44.44, type: 'dIrr', magnitude: 13.1 },
  { name: 'Tucana Dwarf', distance_mpc: 0.87, ra: 340.46, dec: -64.42, type: 'dSph', magnitude: 15.7 },
  { name: 'Cetus Dwarf', distance_mpc: 0.78, ra: 6.55, dec: -11.04, type: 'dSph', magnitude: 14.4 },
  { name: 'Pegasus Dwarf', distance_mpc: 0.92, ra: 352.15, dec: 14.74, type: 'dIrr', magnitude: 13.2 },
  { name: 'WLM', distance_mpc: 0.93, ra: 0.49, dec: -15.46, type: 'Irr', magnitude: 11.0 },
];

const MAJOR_STRUCTURES: Array<{
  name: string;
  distance_mpc: number;
  ra: number;
  dec: number;
  type: 'cluster' | 'supercluster' | 'void' | 'wall';
  size_mpc?: number;
}> = [
  { name: 'Virgo Cluster', distance_mpc: 16.5, ra: 187.70, dec: 12.34, type: 'cluster', size_mpc: 2.2 },
  { name: 'Fornax Cluster', distance_mpc: 19, ra: 54.63, dec: -35.45, type: 'cluster', size_mpc: 1.4 },
  { name: 'Coma Cluster', distance_mpc: 100, ra: 194.95, dec: 27.98, type: 'cluster', size_mpc: 6 },
  { name: 'Perseus Cluster', distance_mpc: 73, ra: 49.95, dec: 41.51, type: 'cluster', size_mpc: 3 },
  { name: 'Centaurus Cluster', distance_mpc: 52, ra: 192.20, dec: -41.31, type: 'cluster', size_mpc: 2 },
  { name: 'Hydra Cluster', distance_mpc: 58, ra: 159.18, dec: -27.53, type: 'cluster', size_mpc: 2 },
  { name: 'Shapley Supercluster', distance_mpc: 200, ra: 202.5, dec: -31.5, type: 'supercluster', size_mpc: 40 },
  { name: 'Laniakea', distance_mpc: 80, ra: 157, dec: -46, type: 'supercluster', size_mpc: 160 },
  { name: 'Hercules Supercluster', distance_mpc: 150, ra: 241, dec: 17, type: 'supercluster', size_mpc: 30 },
  { name: 'Corona Borealis SC', distance_mpc: 320, ra: 230, dec: 27, type: 'supercluster', size_mpc: 50 },
  { name: 'Sloan Great Wall', distance_mpc: 310, ra: 195, dec: 7, type: 'wall', size_mpc: 430 },
  { name: 'CfA2 Great Wall', distance_mpc: 100, ra: 180, dec: 30, type: 'wall', size_mpc: 150 },
  { name: 'Hercules-Corona Wall', distance_mpc: 3000, ra: 225, dec: 30, type: 'wall', size_mpc: 3000 },
  { name: 'Boötes Void', distance_mpc: 213, ra: 218, dec: 46, type: 'void', size_mpc: 100 },
  { name: 'CMB Cold Spot', distance_mpc: 3000, ra: 49, dec: -21, type: 'void', size_mpc: 500 },
  { name: 'Local Void', distance_mpc: 23, ra: 295, dec: 5, type: 'void', size_mpc: 45 },
  { name: 'Sculptor Void', distance_mpc: 65, ra: 10, dec: -30, type: 'void', size_mpc: 50 },
];

const HIGH_Z_GALAXIES: Array<{
  name: string;
  redshift: number;
  ra: number;
  dec: number;
  discovery: string;
}> = [
  { name: 'GN-z11', redshift: 10.6, ra: 189.28, dec: 62.24, discovery: 'HST/JWST' },
  { name: 'JADES-GS-z14-0', redshift: 14.32, ra: 53.16, dec: -27.79, discovery: 'JWST' },
  { name: 'JADES-GS-z13-0', redshift: 13.2, ra: 53.15, dec: -27.81, discovery: 'JWST' },
  { name: 'JADES-GS-z12-0', redshift: 12.63, ra: 53.17, dec: -27.80, discovery: 'JWST' },
  { name: "Maisie's Galaxy", redshift: 11.4, ra: 214.93, dec: 52.94, discovery: 'JWST CEERS' },
  { name: 'CEERS-93316', redshift: 11.04, ra: 214.82, dec: 52.88, discovery: 'JWST CEERS' },
  { name: 'CR7', redshift: 6.6, ra: 150.24, dec: 1.80, discovery: 'VLT' },
  { name: 'Himiko', redshift: 6.6, ra: 34.49, dec: -5.15, discovery: 'Subaru' },
  { name: 'IOK-1', redshift: 6.96, ra: 198.38, dec: 27.42, discovery: 'Subaru' },
  { name: 'z8_GND_5296', redshift: 7.51, ra: 189.14, dec: 62.31, discovery: 'Keck' },
  { name: 'A1689-zD1', redshift: 7.5, ra: 197.87, dec: -1.34, discovery: 'HST' },
  { name: 'EGS-zs8-1', redshift: 7.73, ra: 214.80, dec: 52.83, discovery: 'Keck' },
  { name: 'GLASS-z12', redshift: 12.4, ra: 3.58, dec: -30.38, discovery: 'JWST GLASS' },
  { name: 'SMACS-z16', redshift: 16.7, ra: 110.83, dec: -73.45, discovery: 'JWST (candidate)' },
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

function celestialToCartesian(ra: number, dec: number, distance_mpc: number): [number, number, number] {
  const distance_gpc = distance_mpc / 1000;
  const raRad = (ra * Math.PI) / 180;
  const decRad = (dec * Math.PI) / 180;
  const x = distance_gpc * Math.cos(decRad) * Math.cos(raRad);
  const y = distance_gpc * Math.cos(decRad) * Math.sin(raRad);
  const z = distance_gpc * Math.sin(decRad);
  return [x, y, z];
}

function redshiftToDistance(z: number): number {
  const c = 299792.458;
  const H0 = 67.4;
  const Om = 0.315;
  const OL = 0.685;
  let integral = 0;
  const steps = 1000;
  const dz = z / steps;
  for (let i = 0; i < steps; i++) {
    const zi = (i + 0.5) * dz;
    const E = Math.sqrt(Om * Math.pow(1 + zi, 3) + OL);
    integral += dz / E;
  }
  return (c / H0) * integral;
}

const MEASUREMENT_COLORS: Record<number, string> = {
  1: '#4A90D9', 2: '#F5A623', 3: '#7ED321', 4: '#BD10E0', 5: '#50E3C2', 6: '#D0021B',
};

// =============================================================================
// COMPONENTS
// =============================================================================

interface FilterPanelProps {
  filters: Record<string, boolean>;
  setFilters: React.Dispatch<React.SetStateAction<Record<string, boolean>>>;
  isRotating: boolean;
  setIsRotating: (r: boolean) => void;
  showLabels: boolean;
  setShowLabels: (s: boolean) => void;
  stats: { local: number; structures: number; highz: number; survey: number };
  isTourRunning: boolean;
  onStartTour: () => void;
  onStopTour: () => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filters, setFilters, isRotating, setIsRotating, showLabels, setShowLabels, stats,
  isTourRunning, onStartTour, onStopTour
}) => {
  const toggleFilter = (key: string) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const filterItems = [
    { key: 'localGroup', label: 'Local Group', color: '#00ff00', count: stats.local },
    { key: 'structures', label: 'Clusters & Structures', color: '#ff6600', count: stats.structures },
    { key: 'highZ', label: 'High-z Galaxies (JWST)', color: '#ff00ff', count: stats.highz },
    { key: 'survey', label: 'DESI/SDSS Survey', color: '#4A90D9', count: stats.survey },
  ];

  return (
    <div className="absolute top-4 left-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-[280px]">
      <h3 className="text-white font-bold mb-3 text-lg">Digital Twin Controls</h3>

      {/* Cinematic Tour Button */}
      <button
        onClick={isTourRunning ? onStopTour : onStartTour}
        className={`w-full mb-4 px-4 py-2 font-bold text-sm uppercase tracking-wider transition-all border rounded ${
          isTourRunning
            ? 'bg-red-900/50 text-red-400 border-red-500 hover:bg-red-900/80 animate-pulse'
            : 'bg-cyan-900/50 text-cyan-400 border-cyan-500 hover:bg-cyan-900/80 hover:shadow-[0_0_15px_rgba(6,182,212,0.5)]'
        }`}
      >
        {isTourRunning ? '■ STOP TOUR' : '▶ CINEMATIC TOUR'}
      </button>

      {/* Rotation & Labels */}
      <div className="mb-4 pb-3 border-b border-slate-700">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={isRotating}
            onChange={() => setIsRotating(!isRotating)}
            className="w-4 h-4 rounded accent-cyan-500"
            disabled={isTourRunning}
          />
          <span className={`text-sm font-medium ${isTourRunning ? 'text-slate-500' : 'text-cyan-400'}`}>Auto-rotate</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer mt-2">
          <input
            type="checkbox"
            checked={showLabels}
            onChange={() => setShowLabels(!showLabels)}
            className="w-4 h-4 rounded accent-cyan-500"
          />
          <span className="text-cyan-400 text-sm font-medium">Show labels</span>
        </label>
      </div>

      {/* Data filters */}
      <div className="space-y-2">
        {filterItems.map(({ key, label, color, count }) => (
          <label key={key} className="flex items-center gap-2 cursor-pointer hover:bg-slate-800 p-1 rounded transition-colors">
            <input
              type="checkbox"
              checked={filters[key]}
              onChange={() => toggleFilter(key)}
              className="w-4 h-4 rounded accent-blue-500"
            />
            <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: color, boxShadow: `0 0 6px ${color}` }} />
            <span className="text-white text-sm flex-1">{label}</span>
            <span className="text-slate-500 text-xs">{count > 1000 ? `${(count/1000).toFixed(0)}k` : count}</span>
          </label>
        ))}
      </div>

      <div className="mt-4 pt-3 border-t border-slate-700">
        <div className="text-slate-400 text-xs space-y-1">
          <p>Fundamental domain: <strong className="text-white">20.6 Gpc</strong></p>
          <p>T³/Z₂ topology</p>
        </div>
      </div>
    </div>
  );
};

// Milky Way
const MilkyWay: React.FC<{ showLabels: boolean }> = ({ showLabels }) => (
  <group position={[0, 0, 0]}>
    <mesh rotation={[Math.PI / 2, 0, 0]}>
      <ringGeometry args={[0.01, 0.05, 64]} />
      <meshBasicMaterial color="#ffdd88" transparent opacity={0.8} side={THREE.DoubleSide} />
    </mesh>
    <mesh rotation={[Math.PI / 2, 0, 0]}>
      <ringGeometry args={[0.02, 0.04, 64]} />
      <meshBasicMaterial color="#ffeeaa" transparent opacity={0.5} side={THREE.DoubleSide} />
    </mesh>
    <mesh>
      <sphereGeometry args={[0.015, 32, 32]} />
      <meshBasicMaterial color="#ffcc66" />
    </mesh>
    <mesh>
      <sphereGeometry args={[0.08, 16, 16]} />
      <meshBasicMaterial color="#4488ff" transparent opacity={0.1} />
    </mesh>
    {showLabels && (
      <Html position={[0, 0.12, 0]} center>
        <div className="bg-black/80 px-2 py-1 rounded text-green-400 text-xs whitespace-nowrap font-bold">
          Milky Way (You are here)
        </div>
      </Html>
    )}
  </group>
);

// Local Group
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

// Major Structures
const MajorStructures: React.FC<{ showLabels: boolean }> = ({ showLabels }) => (
  <group>
    {MAJOR_STRUCTURES.map((structure, i) => {
      const pos = celestialToCartesian(structure.ra, structure.dec, structure.distance_mpc);
      const size = (structure.size_mpc || 20) / 1000 * 0.3;
      const colors: Record<string, string> = { cluster: '#ff6600', supercluster: '#ff3300', void: '#003366', wall: '#ffcc00' };
      const opacity = structure.type === 'void' ? 0.2 : 0.6;
      return (
        <group key={i} position={pos}>
          <mesh>
            <sphereGeometry args={[Math.min(size, 0.5), 16, 16]} />
            <meshBasicMaterial color={colors[structure.type]} transparent opacity={opacity} wireframe={structure.type === 'wall'} />
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

// High-z
const HighZGalaxies: React.FC<{ showLabels: boolean }> = ({ showLabels }) => (
  <group>
    {HIGH_Z_GALAXIES.map((galaxy, i) => {
      const distance = redshiftToDistance(galaxy.redshift);
      const pos = celestialToCartesian(galaxy.ra, galaxy.dec, distance);
      const intensity = Math.min(1, galaxy.redshift / 15);
      return (
        <group key={i} position={pos}>
          <mesh><sphereGeometry args={[0.05, 16, 16]} /><meshBasicMaterial color="#ff00ff" transparent opacity={0.9} /></mesh>
          <mesh><sphereGeometry args={[0.1, 8, 8]} /><meshBasicMaterial color="#ff88ff" transparent opacity={0.3 * intensity} /></mesh>
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

// Survey
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

// Z² Vertices
const Z2Vertices: React.FC<{ showLabels: boolean }> = ({ showLabels }) => {
  const vertices = [
    { name: 'V1: Shapley Attractor', position: [8.5, 4.0, 5.0] as [number, number, number], color: '#FFD700' },
    { name: 'V2: Anti-Shapley', position: [-7.0, -3.0, -5.0] as [number, number, number], color: '#00FFFF' },
    { name: 'V3: CMB Cold Spot', position: [-2.0, 6.0, 7.0] as [number, number, number], color: '#FF00FF' },
    { name: 'V4: Southern Vertex', position: [1.0, -5.0, -8.0] as [number, number, number], color: '#00FF00' },
  ];
  return (
    <group>
      {vertices.map((vertex, i) => (
        <group key={i} position={vertex.position}>
          <mesh><sphereGeometry args={[0.3, 32, 32]} /><meshBasicMaterial color={vertex.color} transparent opacity={0.9} /></mesh>
          <mesh><sphereGeometry args={[0.5, 16, 16]} /><meshBasicMaterial color={vertex.color} transparent opacity={0.2} /></mesh>
          {showLabels && (
            <Html position={[0, 0.7, 0]} center>
              <div className="px-2 py-1 rounded text-xs whitespace-nowrap font-bold" style={{ backgroundColor: 'rgba(0,0,0,0.8)', color: vertex.color }}>
                {vertex.name}
              </div>
            </Html>
          )}
        </group>
      ))}
    </group>
  );
};

// Fundamental Domain Box
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
// CINEMATIC CAMERA CONTROLLER
// =============================================================================

interface CinematicCameraProps {
  isTourRunning: boolean;
  onTourComplete: () => void;
  onWaypointChange: (text: string) => void;
  controlsRef: React.RefObject<any>;
}

const CinematicCamera: React.FC<CinematicCameraProps> = ({ isTourRunning, onTourComplete, onWaypointChange, controlsRef }) => {
  const { camera } = useThree();
  const lookAtTarget = useRef(new THREE.Vector3());
  const timelineRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    if (!isTourRunning) {
      if (timelineRef.current) {
        timelineRef.current.kill();
        timelineRef.current = null;
      }
      if (controlsRef.current) controlsRef.current.enabled = true;
      return;
    }

    // Disable manual controls during tour
    if (controlsRef.current) controlsRef.current.enabled = false;

    // Create smooth spline through waypoints
    const positions = TOUR_WAYPOINTS.map(wp => wp.position);
    const curve = new THREE.CatmullRomCurve3(positions);
    curve.tension = 0.3;

    // Set initial position
    camera.position.copy(TOUR_WAYPOINTS[0].position);
    lookAtTarget.current.copy(TOUR_WAYPOINTS[0].lookAt);
    onWaypointChange(TOUR_WAYPOINTS[0].text);

    const totalDuration = TOUR_WAYPOINTS.reduce((acc, wp) => acc + wp.duration, 0);
    const proxy = { progress: 0 };

    // Build lookAt interpolation points
    const lookAtCurve = new THREE.CatmullRomCurve3(TOUR_WAYPOINTS.map(wp => wp.lookAt));

    timelineRef.current = gsap.timeline({
      onComplete: () => {
        onTourComplete();
        if (controlsRef.current) controlsRef.current.enabled = true;
      }
    });

    // Calculate cumulative times for waypoint text changes
    let cumulativeTime = 0;
    TOUR_WAYPOINTS.forEach((wp, i) => {
      if (i > 0) {
        timelineRef.current!.call(() => onWaypointChange(wp.text), [], cumulativeTime);
      }
      cumulativeTime += wp.duration;
    });

    timelineRef.current.to(proxy, {
      progress: 1,
      duration: totalDuration,
      ease: "power1.inOut",
      onUpdate: () => {
        const point = curve.getPointAt(proxy.progress);
        camera.position.copy(point);
        const lookAtPoint = lookAtCurve.getPointAt(proxy.progress);
        lookAtTarget.current.copy(lookAtPoint);
      }
    }, 0);

    return () => {
      if (timelineRef.current) {
        timelineRef.current.kill();
        timelineRef.current = null;
      }
      if (controlsRef.current) controlsRef.current.enabled = true;
    };
  }, [isTourRunning, camera, controlsRef, onTourComplete, onWaypointChange]);

  useFrame(() => {
    if (isTourRunning) {
      camera.lookAt(lookAtTarget.current);
      if (controlsRef.current) {
        controlsRef.current.target.copy(lookAtTarget.current);
      }
    }
  });

  return null;
};

// =============================================================================
// ROTATING UNIVERSE
// =============================================================================

interface RotatingUniverseProps {
  filters: Record<string, boolean>;
  isRotating: boolean;
  showLabels: boolean;
  isTourRunning: boolean;
}

const RotatingUniverse: React.FC<RotatingUniverseProps> = ({ filters, isRotating, showLabels, isTourRunning }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current && isRotating && !isTourRunning) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.03;
    }
  });

  return (
    <group ref={groupRef}>
      <FundamentalDomainBox />
      <Z2Vertices showLabels={showLabels} />
      <MilkyWay showLabels={showLabels} />
      {filters.localGroup && <LocalGroupGalaxies showLabels={showLabels} />}
      {filters.structures && <MajorStructures showLabels={showLabels} />}
      {filters.highZ && <HighZGalaxies showLabels={showLabels} />}
      {filters.survey && <SurveyGalaxies />}
    </group>
  );
};

// =============================================================================
// SCENE
// =============================================================================

interface SceneProps {
  filters: Record<string, boolean>;
  isRotating: boolean;
  showLabels: boolean;
  isTourRunning: boolean;
  onTourComplete: () => void;
  onWaypointChange: (text: string) => void;
}

const Scene: React.FC<SceneProps> = ({ filters, isRotating, showLabels, isTourRunning, onTourComplete, onWaypointChange }) => {
  const controlsRef = useRef<any>(null);

  return (
    <>
      <color attach="background" args={['#050510']} />
      <ambientLight intensity={0.6} />

      <RotatingUniverse filters={filters} isRotating={isRotating} showLabels={showLabels} isTourRunning={isTourRunning} />

      <CinematicCamera
        isTourRunning={isTourRunning}
        onTourComplete={onTourComplete}
        onWaypointChange={onWaypointChange}
        controlsRef={controlsRef}
      />

      <OrbitControls
        ref={controlsRef}
        enablePan
        enableZoom
        enableRotate
        minDistance={0.1}
        maxDistance={80}
        zoomSpeed={0.8}
        rotateSpeed={0.5}
        enableDamping
        dampingFactor={0.05}
      />
      <PerspectiveCamera makeDefault position={[2, 1.5, 2]} fov={50} />
    </>
  );
};

// =============================================================================
// MAIN COMPONENT
// =============================================================================

const MultiMessengerUniverse: React.FC = () => {
  const [filters, setFilters] = useState<Record<string, boolean>>({
    localGroup: true,
    structures: true,
    highZ: true,
    survey: true,
  });

  const [isRotating, setIsRotating] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [isTourRunning, setIsTourRunning] = useState(false);
  const [tourText, setTourText] = useState('');

  const stats = useMemo(() => ({
    local: LOCAL_GROUP.length,
    structures: MAJOR_STRUCTURES.length,
    highz: HIGH_Z_GALAXIES.length,
    survey: SURVEY_GALAXIES.length,
  }), []);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.stopPropagation();
  }, []);

  const handleStartTour = useCallback(() => {
    setIsTourRunning(true);
    setIsRotating(false);
  }, []);

  const handleStopTour = useCallback(() => {
    setIsTourRunning(false);
    setTourText('');
  }, []);

  const handleWaypointChange = useCallback((text: string) => {
    setTourText(text);
  }, []);

  return (
    <div className="relative w-full h-[800px] bg-slate-950 rounded-lg overflow-hidden" onWheel={handleWheel}>
      <FilterPanel
        filters={filters}
        setFilters={setFilters}
        isRotating={isRotating}
        setIsRotating={setIsRotating}
        showLabels={showLabels}
        setShowLabels={setShowLabels}
        stats={stats}
        isTourRunning={isTourRunning}
        onStartTour={handleStartTour}
        onStopTour={handleStopTour}
      />

      <div className="absolute top-4 right-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-xs">
        <h3 className="text-white font-bold mb-2">Z² Topological Digital Twin</h3>
        <p className="text-slate-400 text-sm leading-relaxed">
          Real astronomical data from the Local Group to z~15 JWST galaxies,
          unified in the T³/Z₂ fundamental domain.
        </p>
        <div className="mt-3 pt-3 border-t border-slate-700 text-xs text-slate-500">
          <span className="text-cyan-400">Scroll</span> to zoom into Milky Way
        </div>
      </div>

      {/* Tour narration overlay */}
      {isTourRunning && tourText && (
        <div className="absolute bottom-24 left-1/2 -translate-x-1/2 z-20 max-w-2xl">
          <div className="bg-black/90 text-white font-mono text-lg border border-cyan-500 px-6 py-4 rounded-lg shadow-[0_0_30px_rgba(6,182,212,0.4)]">
            <p className="animate-pulse">{tourText}</p>
          </div>
        </div>
      )}

      <Canvas gl={{ antialias: true, alpha: false }} dpr={[1, 2]}>
        <Scene
          filters={filters}
          isRotating={isRotating}
          showLabels={showLabels}
          isTourRunning={isTourRunning}
          onTourComplete={handleStopTour}
          onWaypointChange={handleWaypointChange}
        />
      </Canvas>

      <div className="absolute bottom-4 left-4 bg-slate-900/95 p-3 rounded-lg border border-slate-700 z-10 backdrop-blur-sm text-sm">
        <div className="grid grid-cols-2 gap-x-4 gap-y-1">
          <span className="text-slate-400">Total objects:</span>
          <span className="text-white font-mono">{(stats.local + stats.structures + stats.highz + stats.survey).toLocaleString()}</span>
          <span className="text-slate-400">Domain:</span>
          <span className="text-white font-mono">(20.6 Gpc)³</span>
        </div>
      </div>

      <div className="absolute bottom-4 right-4 bg-slate-900/95 p-3 rounded-lg border border-slate-700 z-10 backdrop-blur-sm text-xs space-y-1">
        <div className="flex items-center gap-2 text-green-400"><span className="w-2 h-2 rounded-full bg-green-400" />Local Group</div>
        <div className="flex items-center gap-2 text-orange-400"><span className="w-2 h-2 rounded-full bg-orange-400" />Clusters/Structures</div>
        <div className="flex items-center gap-2 text-fuchsia-400"><span className="w-2 h-2 rounded-full bg-fuchsia-400" />High-z (JWST)</div>
        <div className="flex items-center gap-2 text-blue-400"><span className="w-2 h-2 rounded-full bg-blue-400" />Survey galaxies</div>
        <div className="flex items-center gap-2 text-yellow-400"><span className="w-2 h-2 rounded-full bg-yellow-400" />Z² Vertices</div>
      </div>
    </div>
  );
};

export default MultiMessengerUniverse;
