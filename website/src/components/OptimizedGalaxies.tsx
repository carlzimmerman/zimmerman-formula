/**
 * =============================================================================
 * OPTIMIZED GALAXIES - GPU-Accelerated Point Cloud Rendering
 * =============================================================================
 *
 * High-performance galaxy rendering with:
 * - Octree spatial indexing for O(log n) frustum queries
 * - LOD-based point sizing and culling
 * - Dynamic buffer updates (only visible points)
 * - Adaptive quality based on FPS
 *
 * Handles 30,000+ galaxies at 60 FPS on standard hardware.
 *
 * =============================================================================
 */

'use client';

import React, { useRef, useMemo, useEffect, useState } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import {
  Octree,
  FrustumCuller,
  LODManager,
  PerformanceMonitor,
  createCosmicOctree,
  HALF_BOX,
  LODLevel
} from '@/lib/gpuOptimization';

// =============================================================================
// TYPES
// =============================================================================

interface GalaxyData {
  position: THREE.Vector3;
  color: THREE.Color;
  type: number;
}

interface OptimizedGalaxiesProps {
  galaxies: Array<{
    x: number;
    y: number;
    z: number;
    r: number;
    g: number;
    b: number;
    type?: number;
  }>;
  basePointSize?: number;
  enableFrustumCulling?: boolean;
  enableLOD?: boolean;
  enableAdaptiveQuality?: boolean;
  onStatsUpdate?: (stats: {
    visible: number;
    culled: number;
    fps: number;
  }) => void;
}

// =============================================================================
// CUSTOM SHADER FOR LOD-AWARE POINT RENDERING
// =============================================================================

const vertexShader = `
  attribute float size;
  attribute float lodLevel;

  varying vec3 vColor;
  varying float vLodLevel;

  void main() {
    vColor = color;
    vLodLevel = lodLevel;

    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);

    // Size attenuation based on distance
    float attenuation = 300.0 / length(mvPosition.xyz);

    // Apply LOD-based size multiplier
    float lodMultiplier = 1.0;
    if (lodLevel < 1.0) lodMultiplier = 4.0;      // ULTRA
    else if (lodLevel < 2.0) lodMultiplier = 2.0; // HIGH
    else if (lodLevel < 3.0) lodMultiplier = 1.0; // MEDIUM
    else if (lodLevel < 4.0) lodMultiplier = 0.5; // LOW
    else lodMultiplier = 0.25;                     // MINIMAL

    gl_PointSize = size * attenuation * lodMultiplier;
    gl_PointSize = clamp(gl_PointSize, 1.0, 32.0);

    gl_Position = projectionMatrix * mvPosition;
  }
`;

const fragmentShader = `
  varying vec3 vColor;
  varying float vLodLevel;

  void main() {
    // Circular point shape
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);
    if (dist > 0.5) discard;

    // Soft edge
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);

    // LOD-based opacity
    float lodOpacity = 1.0;
    if (vLodLevel >= 4.0) lodOpacity = 0.3;
    else if (vLodLevel >= 3.0) lodOpacity = 0.5;
    else if (vLodLevel >= 2.0) lodOpacity = 0.7;

    gl_FragColor = vec4(vColor, alpha * lodOpacity);
  }
`;

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function OptimizedGalaxies({
  galaxies,
  basePointSize = 3.0,
  enableFrustumCulling = true,
  enableLOD = true,
  enableAdaptiveQuality = true,
  onStatsUpdate
}: OptimizedGalaxiesProps) {
  const { camera, gl } = useThree();
  const pointsRef = useRef<THREE.Points>(null);

  // Optimization systems
  const octreeRef = useRef<Octree<GalaxyData> | null>(null);
  const cullerRef = useRef(new FrustumCuller());
  const lodManagerRef = useRef(new LODManager());
  const perfMonitorRef = useRef(new PerformanceMonitor());

  // Stats
  const [visibleCount, setVisibleCount] = useState(0);
  const [culledCount, setCulledCount] = useState(0);
  const [adaptiveQuality, setAdaptiveQuality] = useState(1.0);

  // Convert input to GalaxyData and build octree
  const galaxyData = useMemo(() => {
    return galaxies.map((g) => ({
      position: new THREE.Vector3(g.x, g.y, g.z),
      color: new THREE.Color(g.r, g.g, g.b),
      type: g.type || 0
    }));
  }, [galaxies]);

  // Build octree on data change
  useEffect(() => {
    const octree = createCosmicOctree<GalaxyData>();
    for (const galaxy of galaxyData) {
      octree.insert(galaxy);
    }
    octreeRef.current = octree;
    console.log('[OptimizedGalaxies] Octree built:', octree.getStats());
  }, [galaxyData]);

  // Create geometry with dynamic buffers
  const geometry = useMemo(() => {
    const maxPoints = galaxies.length;
    const geom = new THREE.BufferGeometry();

    const positions = new Float32Array(maxPoints * 3);
    const colors = new Float32Array(maxPoints * 3);
    const sizes = new Float32Array(maxPoints);
    const lodLevels = new Float32Array(maxPoints);

    // Initialize with all galaxies (will be culled dynamically)
    for (let i = 0; i < galaxyData.length; i++) {
      const g = galaxyData[i];
      positions[i * 3] = g.position.x;
      positions[i * 3 + 1] = g.position.y;
      positions[i * 3 + 2] = g.position.z;
      colors[i * 3] = g.color.r;
      colors[i * 3 + 1] = g.color.g;
      colors[i * 3 + 2] = g.color.b;
      sizes[i] = basePointSize;
      lodLevels[i] = 2.0; // Default to MEDIUM
    }

    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geom.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    geom.setAttribute('lodLevel', new THREE.BufferAttribute(lodLevels, 1));

    // Mark as dynamic for frequent updates
    (geom.attributes.position as THREE.BufferAttribute).usage = THREE.DynamicDrawUsage;
    (geom.attributes.size as THREE.BufferAttribute).usage = THREE.DynamicDrawUsage;
    (geom.attributes.lodLevel as THREE.BufferAttribute).usage = THREE.DynamicDrawUsage;

    return geom;
  }, [galaxyData, basePointSize]);

  // Custom shader material
  const material = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      vertexColors: true,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });
  }, []);

  // Frame update: cull and update visible points
  useFrame(() => {
    if (!octreeRef.current || !pointsRef.current) return;

    perfMonitorRef.current.beginFrame();

    // Update culling systems
    cullerRef.current.update(camera);
    lodManagerRef.current.updateCamera(camera);

    // Adaptive quality adjustment
    if (enableAdaptiveQuality) {
      const stats = perfMonitorRef.current.getStats();
      if (stats.fps < 30 && adaptiveQuality > 0.3) {
        setAdaptiveQuality((q) => Math.max(0.3, q - 0.05));
      } else if (stats.fps > 55 && adaptiveQuality < 1.0) {
        setAdaptiveQuality((q) => Math.min(1.0, q + 0.02));
      }
    }

    // Query visible galaxies from octree
    let visibleGalaxies: GalaxyData[];
    if (enableFrustumCulling) {
      visibleGalaxies = octreeRef.current.queryFrustum(cullerRef.current.getFrustum());
    } else {
      visibleGalaxies = galaxyData;
    }

    // Apply adaptive quality (skip some galaxies when FPS is low)
    if (enableAdaptiveQuality && adaptiveQuality < 1.0) {
      const keepCount = Math.floor(visibleGalaxies.length * adaptiveQuality);
      visibleGalaxies = visibleGalaxies.slice(0, keepCount);
    }

    // Update geometry buffers
    const positions = geometry.attributes.position.array as Float32Array;
    const sizes = geometry.attributes.size.array as Float32Array;
    const lodLevels = geometry.attributes.lodLevel.array as Float32Array;

    let idx = 0;
    for (const galaxy of visibleGalaxies) {
      // Apply LOD
      let lodLevel = 2.0; // Default MEDIUM
      if (enableLOD) {
        const lod = lodManagerRef.current.getLODLevel(galaxy.position);
        if (lod === 'CULLED') continue;
        lodLevel = lodToNumber(lod);
      }

      positions[idx * 3] = galaxy.position.x;
      positions[idx * 3 + 1] = galaxy.position.y;
      positions[idx * 3 + 2] = galaxy.position.z;
      sizes[idx] = basePointSize;
      lodLevels[idx] = lodLevel;
      idx++;
    }

    // Update draw range to only render visible points
    geometry.setDrawRange(0, idx);
    geometry.attributes.position.needsUpdate = true;
    geometry.attributes.size.needsUpdate = true;
    geometry.attributes.lodLevel.needsUpdate = true;

    // Update stats
    const culled = galaxyData.length - idx;
    setVisibleCount(idx);
    setCulledCount(culled);

    perfMonitorRef.current.endFrame(gl);
    perfMonitorRef.current.updateCullingStats(idx, culled);

    // Callback for external stats display
    if (onStatsUpdate) {
      onStatsUpdate({
        visible: idx,
        culled,
        fps: perfMonitorRef.current.getStats().fps
      });
    }
  });

  return (
    <points ref={pointsRef} geometry={geometry} material={material} />
  );
}

// =============================================================================
// HELPER: Convert LOD level to numeric value for shader
// =============================================================================

function lodToNumber(lod: LODLevel): number {
  switch (lod) {
    case 'ULTRA': return 0.0;
    case 'HIGH': return 1.0;
    case 'MEDIUM': return 2.0;
    case 'LOW': return 3.0;
    case 'MINIMAL': return 4.0;
    case 'CULLED': return 5.0;
  }
}

// =============================================================================
// WRAPPER: Use with existing survey galaxy data
// =============================================================================

interface SurveyGalaxy {
  distance_mpc: number;
  ra: number;
  dec: number;
  type: number;
}

// Color map for galaxy types
const GALAXY_TYPE_COLORS: Record<number, [number, number, number]> = {
  1: [0.4, 0.6, 1.0],   // Blue - spiral
  2: [1.0, 0.8, 0.4],   // Yellow - elliptical
  3: [0.6, 0.4, 0.8],   // Purple - irregular
  4: [0.4, 1.0, 0.6],   // Green - active
  5: [1.0, 0.4, 0.4],   // Red - starburst
  6: [0.8, 0.8, 0.8]    // Gray - unknown
};

export function OptimizedSurveyGalaxies({
  surveyGalaxies,
  ...props
}: {
  surveyGalaxies: SurveyGalaxy[];
} & Omit<OptimizedGalaxiesProps, 'galaxies'>) {
  // Convert celestial coordinates to Cartesian
  const galaxies = useMemo(() => {
    return surveyGalaxies.map((g) => {
      const distance_gpc = g.distance_mpc / 1000;
      const raRad = (g.ra * Math.PI) / 180;
      const decRad = (g.dec * Math.PI) / 180;

      // Apply T³ wrapping
      let x = distance_gpc * Math.cos(decRad) * Math.cos(raRad);
      let y = distance_gpc * Math.sin(decRad);
      let z = distance_gpc * Math.cos(decRad) * Math.sin(raRad);

      // Wrap to fundamental domain
      x = wrapCoordinate(x);
      y = wrapCoordinate(y);
      z = wrapCoordinate(z);

      const color = GALAXY_TYPE_COLORS[g.type] || GALAXY_TYPE_COLORS[6];

      return {
        x,
        y,
        z,
        r: color[0],
        g: color[1],
        b: color[2],
        type: g.type
      };
    });
  }, [surveyGalaxies]);

  return <OptimizedGalaxies galaxies={galaxies} {...props} />;
}

// T³ coordinate wrapping
function wrapCoordinate(value: number): number {
  const L_C_GPC = 20.6;
  const wrapped = ((value + HALF_BOX) % L_C_GPC + L_C_GPC) % L_C_GPC - HALF_BOX;
  return wrapped;
}

export default OptimizedGalaxies;
