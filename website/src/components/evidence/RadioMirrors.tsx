/**
 * =============================================================================
 * RADIO MIRRORS - Topological Ghost Visualization (GPU-OPTIMIZED)
 * =============================================================================
 *
 * Directive VVVV: Visualize LOFAR/MeerKAT/ASKAP radio sources and search
 * for topological mirror images across T³/Z₂ boundaries.
 *
 * PERFORMANCE OPTIMIZED using InstancedMesh:
 * - All radio sources rendered with 3 draw calls instead of 2N+
 * - Full geometry quality preserved (12x12 spheres, 8x32 tori)
 * - Light paths combined into single LineSegments draw call
 * - Mirror lines combined into single LineSegments draw call
 *
 * GHOST PROBABILITY METHODOLOGY (T³/Z₂ Orbifold):
 * ------------------------------------------------
 * In T³/Z₂ topology with fundamental domain L = 20.6 Gpc:
 *
 * 1. T³ (3-torus): Opposite faces are identified
 *    - (x, y, z) ~ (x + nL, y + mL, z + pL) for integers n, m, p
 *    - Light can wrap around, appearing from opposite direction
 *
 * 2. Z₂ (point inversion): Antipodal identification through center
 *    - (x, y, z) ~ (-x, -y, -z)
 *    - Creates mirror image at inverted position
 *
 * Ghost image appears if:
 * - Two sources at r₁, r₂ satisfy: r₂ ≈ -r₁ (Z₂) or r₂ ≈ r₁ + L·ê (T³ face)
 * - Path length through topology < observable horizon (~13 Gpc)
 * - Source properties (size, flux, morphology) are consistent
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { Text } from '@react-three/drei';

// Constants
const L_C = 20.6;
const HALF_BOX = L_C / 2;
const SCALE = 0.5; // Scale factor for visualization

// Color scheme
const TYPE_COLORS: Record<string, THREE.Color> = {
  ORC: new THREE.Color('#FF6B6B'),     // Red
  GRG: new THREE.Color('#4ECDC4'),     // Teal
  Relic: new THREE.Color('#9B59B6'),   // Purple
  'FR-I': new THREE.Color('#3498DB'),  // Blue
  'FR-II': new THREE.Color('#E74C3C'), // Red-orange
};

const TYPE_COLORS_HEX: Record<string, string> = {
  ORC: '#FF6B6B',
  GRG: '#4ECDC4',
  Relic: '#9B59B6',
  'FR-I': '#3498DB',
  'FR-II': '#E74C3C',
};

// Observable horizon (CMB distance)
const OBSERVABLE_HORIZON_GPC = 13.0;

// =============================================================================
// RIGOROUS T³/Z₂ GHOST PROBABILITY CALCULATION
// =============================================================================

interface GhostAnalysis {
  probability: number;
  ghostType: 'Z2' | 'X_FACE' | 'Y_FACE' | 'Z_FACE' | null;
  lightPath: THREE.Vector3[];
  pathLength: number;
  geometricScore: number;
  propertyScore: number;
}

/**
 * Compute rigorous ghost probability for two radio sources in T³/Z₂ topology.
 *
 * Methodology:
 * 1. Geometric test: Does position r₂ match a topological image of r₁?
 * 2. Path length test: Is the wrapped light path < observable horizon?
 * 3. Property test: Do flux ratio, size ratio, morphology match?
 *
 * @param pos1 - Position of source 1 in Gpc (within fundamental domain)
 * @param pos2 - Position of source 2 in Gpc
 * @param flux1 - Flux density of source 1 (mJy)
 * @param flux2 - Flux density of source 2 (mJy)
 * @param size1 - Angular size of source 1 (arcmin)
 * @param size2 - Angular size of source 2 (arcmin)
 * @returns GhostAnalysis with probability and light path
 */
function computeRigorousGhostProbability(
  pos1: THREE.Vector3,
  pos2: THREE.Vector3,
  flux1: number,
  flux2: number,
  size1: number,
  size2: number
): GhostAnalysis {
  const result: GhostAnalysis = {
    probability: 0,
    ghostType: null,
    lightPath: [],
    pathLength: 0,
    geometricScore: 0,
    propertyScore: 0,
  };

  // -------------------------------------------------------------------------
  // 1. Z₂ INVERSION TEST: r₂ ≈ -r₁
  // -------------------------------------------------------------------------
  const z2Image = pos1.clone().negate();
  const z2Deviation = pos2.clone().sub(z2Image).length();
  const z2GeometricScore = Math.exp(-z2Deviation / 1.0); // Gaussian falloff, σ = 1 Gpc

  // -------------------------------------------------------------------------
  // 2. T³ FACE IDENTIFICATION TESTS: r₂ ≈ r₁ ± L·ê
  // -------------------------------------------------------------------------
  const faceScores: { axis: 'X_FACE' | 'Y_FACE' | 'Z_FACE'; score: number; sign: number }[] = [];

  // X-face: r₂ ≈ (L - r₁.x, r₁.y, r₁.z) or (-L - r₁.x, r₁.y, r₁.z)
  for (const sign of [1, -1]) {
    const xImage = new THREE.Vector3(sign * L_C - pos1.x, pos1.y, pos1.z);
    const xDeviation = pos2.clone().sub(xImage).length();
    faceScores.push({ axis: 'X_FACE', score: Math.exp(-xDeviation / 1.0), sign });
  }

  // Y-face
  for (const sign of [1, -1]) {
    const yImage = new THREE.Vector3(pos1.x, sign * L_C - pos1.y, pos1.z);
    const yDeviation = pos2.clone().sub(yImage).length();
    faceScores.push({ axis: 'Y_FACE', score: Math.exp(-yDeviation / 1.0), sign });
  }

  // Z-face
  for (const sign of [1, -1]) {
    const zImage = new THREE.Vector3(pos1.x, pos1.y, sign * L_C - pos1.z);
    const zDeviation = pos2.clone().sub(zImage).length();
    faceScores.push({ axis: 'Z_FACE', score: Math.exp(-zDeviation / 1.0), sign });
  }

  // Find best geometric match
  const bestFace = faceScores.reduce((best, current) =>
    current.score > best.score ? current : best
  );

  // -------------------------------------------------------------------------
  // 3. DETERMINE BEST GHOST TYPE
  // -------------------------------------------------------------------------
  let bestType: 'Z2' | 'X_FACE' | 'Y_FACE' | 'Z_FACE' | null = null;
  let bestGeometricScore = 0;
  let expectedImage = new THREE.Vector3();

  if (z2GeometricScore > bestFace.score && z2GeometricScore > 0.1) {
    bestType = 'Z2';
    bestGeometricScore = z2GeometricScore;
    expectedImage = z2Image;
  } else if (bestFace.score > 0.1) {
    bestType = bestFace.axis;
    bestGeometricScore = bestFace.score;
    // Compute expected image position for light path
    if (bestFace.axis === 'X_FACE') {
      expectedImage = new THREE.Vector3(bestFace.sign * L_C - pos1.x, pos1.y, pos1.z);
    } else if (bestFace.axis === 'Y_FACE') {
      expectedImage = new THREE.Vector3(pos1.x, bestFace.sign * L_C - pos1.y, pos1.z);
    } else {
      expectedImage = new THREE.Vector3(pos1.x, pos1.y, bestFace.sign * L_C - pos1.z);
    }
  }

  if (!bestType) {
    return result; // No geometric match
  }

  // -------------------------------------------------------------------------
  // 4. COMPUTE LIGHT PATH THROUGH TOPOLOGY
  // -------------------------------------------------------------------------
  // For Z₂: Light goes from origin → through center → to actual source at -r₂
  // For T³ face: Light goes from origin → to boundary face → wraps to other side → to source

  const origin = new THREE.Vector3(0, 0, 0);
  let lightPath: THREE.Vector3[] = [];
  let pathLength = 0;

  if (bestType === 'Z2') {
    // Z₂ path: direct to pos2, which is seeing the image of pos1 inverted
    // The "actual" source is at pos1, ghost appears at pos2 ≈ -pos1
    lightPath = [origin, pos2.clone()];
    pathLength = pos2.length();
  } else {
    // T³ face path: light hits boundary, wraps around
    const boundaryPoint = new THREE.Vector3();
    const actualSource = pos1.clone();

    if (bestType === 'X_FACE') {
      const t = (HALF_BOX * Math.sign(pos2.x)) / pos2.x;
      boundaryPoint.set(HALF_BOX * Math.sign(pos2.x), pos2.y * t, pos2.z * t);
    } else if (bestType === 'Y_FACE') {
      const t = (HALF_BOX * Math.sign(pos2.y)) / pos2.y;
      boundaryPoint.set(pos2.x * t, HALF_BOX * Math.sign(pos2.y), pos2.z * t);
    } else {
      const t = (HALF_BOX * Math.sign(pos2.z)) / pos2.z;
      boundaryPoint.set(pos2.x * t, pos2.y * t, HALF_BOX * Math.sign(pos2.z));
    }

    // Wrapped position (opposite boundary)
    const wrappedPoint = boundaryPoint.clone();
    if (bestType === 'X_FACE') wrappedPoint.x *= -1;
    else if (bestType === 'Y_FACE') wrappedPoint.y *= -1;
    else wrappedPoint.z *= -1;

    lightPath = [origin, boundaryPoint, wrappedPoint, actualSource];
    pathLength = boundaryPoint.length() + wrappedPoint.distanceTo(actualSource);
  }

  // -------------------------------------------------------------------------
  // 5. PATH LENGTH CONSTRAINT
  // -------------------------------------------------------------------------
  if (pathLength > OBSERVABLE_HORIZON_GPC) {
    return result; // Path too long to be observable
  }

  // -------------------------------------------------------------------------
  // 6. PROPERTY CONSISTENCY SCORE
  // -------------------------------------------------------------------------
  // Ghost images should have similar intrinsic properties
  // Flux ratio: topological ghosts have same intrinsic luminosity, but distance may differ
  // Size ratio: should be similar if same object

  const fluxRatio = Math.max(flux1, flux2) / Math.min(flux1, flux2);
  const sizeRatio = Math.max(size1, size2) / Math.min(size1, size2);

  // Penalize large ratios (indicating different sources)
  const fluxScore = Math.exp(-Math.log(fluxRatio) / 0.5); // σ = factor of 1.6
  const sizeScore = Math.exp(-Math.log(sizeRatio) / 0.3); // σ = factor of 1.3

  const propertyScore = (fluxScore + sizeScore) / 2;

  // -------------------------------------------------------------------------
  // 7. FINAL PROBABILITY
  // -------------------------------------------------------------------------
  // Combine geometric and property scores
  // Weight geometric more heavily since it's the topological constraint
  const probability = Math.min(1.0, bestGeometricScore * 0.7 + propertyScore * 0.3);

  result.probability = probability;
  result.ghostType = bestType;
  result.lightPath = lightPath;
  result.pathLength = pathLength;
  result.geometricScore = bestGeometricScore;
  result.propertyScore = propertyScore;

  return result;
}

// Interfaces
interface RadioSource {
  name: string;
  type: string;
  ra: number;
  dec: number;
  redshift: number | null;
  distance_gpc: number;
  size_arcmin: number;
  flux_mjy: number;
  position: { x: number; y: number; z: number };
  boundary_distance: number;
}

interface ProcessedSource extends RadioSource {
  visualPosition: THREE.Vector3;
  visualSize: number;
  color: THREE.Color;
  isORC: boolean;
}

interface MirrorPair {
  source1: string;
  source2: string;
  mirror_type: string;
  separation_gpc: number;
  ghost_probability: number;
}

interface RadioData {
  metadata: {
    total_sources: number;
  };
  sources: RadioSource[];
  ghost_analysis: {
    mirror_pairs: MirrorPair[];
    total_candidates: number;
  };
  orc_analysis: {
    n_orcs: number;
    clustering_ratio: number;
    interpretation: string;
  };
}

interface RadioMirrorsProps {
  opacity?: number;
  showMirrorLines?: boolean;
  showORCRings?: boolean;
  selectedType?: string;
  minGhostProbability?: number;
  showLightPaths?: boolean;
}

/**
 * Main Radio Mirrors visualization - GPU OPTIMIZED
 */
export function RadioMirrors({
  opacity = 1,
  showMirrorLines = true,
  showORCRings = true,
  selectedType = 'all',
  minGhostProbability = 0.2,
  showLightPaths = true,
}: RadioMirrorsProps) {
  const [data, setData] = useState<RadioData | null>(null);

  // InstancedMesh refs
  const coresRef = useRef<THREE.InstancedMesh>(null);
  const glowsRef = useRef<THREE.InstancedMesh>(null);
  const orcToriRef = useRef<THREE.InstancedMesh>(null);

  // Reusable objects for instance updates
  const tempMatrix = useMemo(() => new THREE.Matrix4(), []);
  const tempScale = useMemo(() => new THREE.Vector3(), []);
  const tempPosition = useMemo(() => new THREE.Vector3(), []);
  const identityQuaternion = useMemo(() => new THREE.Quaternion(), []);

  // Load data
  useEffect(() => {
    fetch('/data/radio_ghost_data.json')
      .then(res => res.json())
      .then((loadedData: RadioData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Process sources with pre-computed visual properties
  const processedSources = useMemo(() => {
    if (!data) return [];

    let sources = data.sources;
    if (selectedType !== 'all') {
      sources = sources.filter(s => s.type === selectedType);
    }

    return sources.map((source): ProcessedSource => {
      const visualPosition = new THREE.Vector3(
        source.position.x * SCALE,
        source.position.y * SCALE,
        source.position.z * SCALE
      );

      // Size based on log flux (real measurement)
      const logFlux = Math.log10(source.flux_mjy + 1);
      const visualSize = 0.05 + logFlux * 0.03;

      const color = TYPE_COLORS[source.type] || new THREE.Color('#888888');
      const isORC = source.type === 'ORC';

      return {
        ...source,
        visualPosition,
        visualSize,
        color,
        isORC,
      };
    });
  }, [data, selectedType]);

  // Count ORCs for instanced mesh sizing
  const orcCount = useMemo(() => {
    return showORCRings ? processedSources.filter(s => s.isORC).length : 0;
  }, [processedSources, showORCRings]);

  // Setup instanced meshes when data changes
  useEffect(() => {
    if (!coresRef.current || !glowsRef.current) return;
    if (processedSources.length === 0) return;

    const count = processedSources.length;

    for (let i = 0; i < count; i++) {
      const source = processedSources[i];

      // CORE SPHERE
      tempPosition.copy(source.visualPosition);
      tempScale.set(source.visualSize, source.visualSize, source.visualSize);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      coresRef.current.setMatrixAt(i, tempMatrix);
      coresRef.current.setColorAt(i, source.color);

      // GLOW SPHERE (2x size)
      tempScale.set(source.visualSize * 2, source.visualSize * 2, source.visualSize * 2);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      glowsRef.current.setMatrixAt(i, tempMatrix);
      glowsRef.current.setColorAt(i, source.color);
    }

    coresRef.current.instanceMatrix.needsUpdate = true;
    if (coresRef.current.instanceColor) coresRef.current.instanceColor.needsUpdate = true;
    glowsRef.current.instanceMatrix.needsUpdate = true;
    if (glowsRef.current.instanceColor) glowsRef.current.instanceColor.needsUpdate = true;
  }, [processedSources, tempMatrix, tempScale, tempPosition, identityQuaternion]);

  // Setup ORC tori instanced mesh
  useEffect(() => {
    if (!orcToriRef.current || orcCount === 0) return;

    const orcSources = processedSources.filter(s => s.isORC);
    const orcColor = new THREE.Color('#FF6B6B');

    for (let i = 0; i < orcSources.length; i++) {
      const source = orcSources[i];

      // ORC TORUS (ring around source)
      // Torus: tube radius = size*0.3, ring radius = size*3
      tempPosition.copy(source.visualPosition);
      const torusScale = source.visualSize;
      tempScale.set(torusScale, torusScale, torusScale);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      orcToriRef.current.setMatrixAt(i, tempMatrix);
      orcToriRef.current.setColorAt(i, orcColor);
    }

    orcToriRef.current.instanceMatrix.needsUpdate = true;
    if (orcToriRef.current.instanceColor) orcToriRef.current.instanceColor.needsUpdate = true;
  }, [processedSources, orcCount, tempMatrix, tempScale, tempPosition, identityQuaternion]);

  // Compute RIGOROUS ghost analysis for each pair
  const rigorousGhostPairs = useMemo(() => {
    if (!data) return [];

    const pairs: Array<{
      source1: RadioSource;
      source2: RadioSource;
      analysis: GhostAnalysis;
    }> = [];

    // Check all pairs of sources
    for (let i = 0; i < data.sources.length; i++) {
      for (let j = i + 1; j < data.sources.length; j++) {
        const s1 = data.sources[i];
        const s2 = data.sources[j];

        const pos1 = new THREE.Vector3(s1.position.x, s1.position.y, s1.position.z);
        const pos2 = new THREE.Vector3(s2.position.x, s2.position.y, s2.position.z);

        const analysis = computeRigorousGhostProbability(
          pos1, pos2,
          s1.flux_mjy, s2.flux_mjy,
          s1.size_arcmin, s2.size_arcmin
        );

        if (analysis.probability >= minGhostProbability && analysis.ghostType) {
          pairs.push({ source1: s1, source2: s2, analysis });
        }
      }
    }

    // Sort by probability descending
    return pairs.sort((a, b) => b.analysis.probability - a.analysis.probability);
  }, [data, minGhostProbability]);

  // Combined light path geometry (single draw call)
  const lightPathGeometry = useMemo(() => {
    if (!showLightPaths || rigorousGhostPairs.length === 0) return null;

    const positions: number[] = [];

    // Show top 5 ghost pairs
    rigorousGhostPairs.slice(0, 5).forEach(pair => {
      if (!pair.analysis.ghostType) return;

      const pos1 = new THREE.Vector3(
        pair.source1.position.x,
        pair.source1.position.y,
        pair.source1.position.z
      );
      const pos2 = new THREE.Vector3(
        pair.source2.position.x,
        pair.source2.position.y,
        pair.source2.position.z
      );

      const origin = new THREE.Vector3(0, 0, 0);

      if (pair.analysis.ghostType === 'Z2') {
        // Z₂: Origin to ghost position
        positions.push(origin.x * SCALE, origin.y * SCALE, origin.z * SCALE);
        positions.push(pos2.x * SCALE, pos2.y * SCALE, pos2.z * SCALE);
      } else {
        // T³ face: Origin to boundary, then boundary to source
        const dir = pos2.clone().normalize();
        let boundaryPoint: THREE.Vector3;

        if (pair.analysis.ghostType === 'X_FACE') {
          const t = HALF_BOX / Math.abs(dir.x);
          boundaryPoint = dir.clone().multiplyScalar(t);
        } else if (pair.analysis.ghostType === 'Y_FACE') {
          const t = HALF_BOX / Math.abs(dir.y);
          boundaryPoint = dir.clone().multiplyScalar(t);
        } else {
          const t = HALF_BOX / Math.abs(dir.z);
          boundaryPoint = dir.clone().multiplyScalar(t);
        }

        // Wrapped point (opposite boundary)
        const wrappedPoint = boundaryPoint.clone();
        if (pair.analysis.ghostType === 'X_FACE') wrappedPoint.x *= -1;
        else if (pair.analysis.ghostType === 'Y_FACE') wrappedPoint.y *= -1;
        else wrappedPoint.z *= -1;

        // Origin to boundary
        positions.push(origin.x * SCALE, origin.y * SCALE, origin.z * SCALE);
        positions.push(boundaryPoint.x * SCALE, boundaryPoint.y * SCALE, boundaryPoint.z * SCALE);

        // Wrapped to source
        positions.push(wrappedPoint.x * SCALE, wrappedPoint.y * SCALE, wrappedPoint.z * SCALE);
        positions.push(pos1.x * SCALE, pos1.y * SCALE, pos1.z * SCALE);
      }
    });

    if (positions.length === 0) return null;

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    return geometry;
  }, [showLightPaths, rigorousGhostPairs]);

  // Legacy mirror lines geometry (from JSON data)
  const legacyMirrorGeometry = useMemo(() => {
    if (!data || showLightPaths) return null;
    if (!showMirrorLines) return null;

    const positions: number[] = [];
    const filteredPairs = data.ghost_analysis.mirror_pairs.filter(
      p => p.ghost_probability >= minGhostProbability
    );

    // Build source lookup
    const sourceLookup: Record<string, RadioSource> = {};
    data.sources.forEach(s => {
      sourceLookup[s.name] = s;
    });

    filteredPairs.forEach(pair => {
      const s1 = sourceLookup[pair.source1];
      const s2 = sourceLookup[pair.source2];
      if (!s1 || !s2) return;

      positions.push(s1.position.x * SCALE, s1.position.y * SCALE, s1.position.z * SCALE);
      positions.push(s2.position.x * SCALE, s2.position.y * SCALE, s2.position.z * SCALE);
    });

    if (positions.length === 0) return null;

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    return geometry;
  }, [data, showMirrorLines, showLightPaths, minGhostProbability]);

  if (!data) return null;

  const sourceCount = processedSources.length;

  return (
    <group>
      {/* Earth marker at origin (observer position) */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.03, 16, 16]} />
        <meshStandardMaterial
          color="#4444FF"
          emissive="#4444FF"
          emissiveIntensity={0.5}
        />
      </mesh>
      <Text
        position={[0, 0.08, 0]}
        fontSize={0.05}
        color="#4444FF"
        anchorX="center"
      >
        Earth
      </Text>

      {/* INSTANCED CORE SPHERES - Full 12x12 geometry, ONE draw call */}
      {sourceCount > 0 && (
        <instancedMesh
          ref={coresRef}
          args={[undefined, undefined, sourceCount]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 12, 12]} />
          <meshStandardMaterial
            emissive="#ffffff"
            emissiveIntensity={0.5}
            roughness={0.4}
            metalness={0.6}
          />
        </instancedMesh>
      )}

      {/* INSTANCED GLOW SPHERES - Full 12x12 geometry, ONE draw call */}
      {sourceCount > 0 && (
        <instancedMesh
          ref={glowsRef}
          args={[undefined, undefined, sourceCount]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 12, 12]} />
          <meshBasicMaterial
            transparent
            opacity={0.15}
            side={THREE.BackSide}
            depthWrite={false}
          />
        </instancedMesh>
      )}

      {/* INSTANCED ORC TORI - Full 8x32 geometry, ONE draw call */}
      {orcCount > 0 && (
        <instancedMesh
          ref={orcToriRef}
          args={[undefined, undefined, orcCount]}
          frustumCulled={false}
        >
          <torusGeometry args={[3, 0.3, 8, 32]} />
          <meshStandardMaterial
            emissive="#FF6B6B"
            emissiveIntensity={0.7}
            transparent
            opacity={0.6}
          />
        </instancedMesh>
      )}

      {/* LIGHT PATHS - Combined into single LineSegments draw call */}
      {showLightPaths && lightPathGeometry && (
        <lineSegments geometry={lightPathGeometry}>
          <lineBasicMaterial
            color="#FF44FF"
            transparent
            opacity={0.5}
          />
        </lineSegments>
      )}

      {/* LEGACY MIRROR LINES - Combined into single LineSegments draw call */}
      {!showLightPaths && legacyMirrorGeometry && (
        <lineSegments geometry={legacyMirrorGeometry}>
          <lineBasicMaterial
            color="#FFFFFF"
            transparent
            opacity={0.3}
          />
        </lineSegments>
      )}

      {/* Ghost probability labels (top 3 only to reduce draw calls) */}
      {showLightPaths && rigorousGhostPairs.slice(0, 3).map((pair, i) => {
        if (pair.analysis.probability < 0.3) return null;

        const midpoint = new THREE.Vector3(
          (pair.source1.position.x + pair.source2.position.x) * 0.5 * SCALE,
          (pair.source1.position.y + pair.source2.position.y) * 0.5 * SCALE,
          (pair.source1.position.z + pair.source2.position.z) * 0.5 * SCALE
        );

        const ghostTypeLabel = pair.analysis.ghostType === 'Z2' ? 'Z₂' :
          `T³ ${pair.analysis.ghostType?.replace('_FACE', '')}`;

        return (
          <Text
            key={`label-${i}`}
            position={midpoint}
            fontSize={0.06}
            color="#FF44FF"
            anchorX="center"
          >
            {`${(pair.analysis.probability * 100).toFixed(0)}% ${ghostTypeLabel}`}
          </Text>
        );
      })}

      {/* Fundamental domain wireframe */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_C * SCALE, L_C * SCALE, L_C * SCALE)]} />
        <lineBasicMaterial color="#333" transparent opacity={0.2} />
      </lineSegments>

      {/* Boundary plane markers (kept as individual - only 6) */}
      {[
        { pos: [HALF_BOX * SCALE, 0, 0], rot: [0, Math.PI / 2, 0], label: '+X' },
        { pos: [-HALF_BOX * SCALE, 0, 0], rot: [0, -Math.PI / 2, 0], label: '-X' },
        { pos: [0, HALF_BOX * SCALE, 0], rot: [-Math.PI / 2, 0, 0], label: '+Y' },
        { pos: [0, -HALF_BOX * SCALE, 0], rot: [Math.PI / 2, 0, 0], label: '-Y' },
        { pos: [0, 0, HALF_BOX * SCALE], rot: [0, 0, 0], label: '+Z' },
        { pos: [0, 0, -HALF_BOX * SCALE], rot: [0, Math.PI, 0], label: '-Z' },
      ].map((plane, i) => (
        <group key={i} position={plane.pos as [number, number, number]} rotation={plane.rot as [number, number, number]}>
          <mesh>
            <planeGeometry args={[L_C * SCALE * 0.8, L_C * SCALE * 0.8]} />
            <meshBasicMaterial
              color={plane.label.includes('X') ? '#FF4444' :
                     plane.label.includes('Y') ? '#44FF44' : '#4444FF'}
              transparent
              opacity={0.03}
              side={THREE.DoubleSide}
              depthWrite={false}
            />
          </mesh>
        </group>
      ))}
    </group>
  );
}

/**
 * HUD overlay for Radio Ghost statistics
 */
export function RadioGhostHUD({
  totalSources = 0,
  mirrorCandidates = 0,
  bestGhostProb = 0,
  orcClustering = 0,
}: {
  totalSources?: number;
  mirrorCandidates?: number;
  bestGhostProb?: number;
  orcClustering?: number;
}) {
  return (
    <div style={{
      position: 'absolute',
      top: '440px',
      right: '20px',
      background: 'rgba(0,0,0,0.7)',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#fff',
      minWidth: '200px',
      border: '1px solid #333',
    }}>
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#FF6B6B' }}>
        RADIO GHOST HUNT
      </div>

      <div style={{ marginBottom: '5px' }}>
        Sources: {totalSources}
      </div>
      <div style={{ marginBottom: '5px' }}>
        Mirror candidates: {mirrorCandidates}
      </div>
      <div style={{ marginBottom: '5px', color: '#FFD700' }}>
        Best ghost: {(bestGhostProb * 100).toFixed(1)}%
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
      }}>
        <div style={{ marginBottom: '3px' }}>ORC Clustering</div>
        <div style={{
          background: '#333',
          borderRadius: '4px',
          height: '8px',
          overflow: 'hidden',
        }}>
          <div style={{
            width: `${Math.min(100, orcClustering * 50)}%`,
            height: '100%',
            background: orcClustering > 1.5 ? '#2ECC71' : '#E74C3C',
          }} />
        </div>
        <div style={{ fontSize: '10px', color: '#666', marginTop: '3px' }}>
          {orcClustering.toFixed(2)}x (1.0 = uniform)
        </div>
      </div>

      {/* Source Type Legend */}
      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Source Types:</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          <span style={{ color: TYPE_COLORS_HEX.ORC }}>● ORC</span>
          <span style={{ color: TYPE_COLORS_HEX.GRG }}>● GRG</span>
          <span style={{ color: TYPE_COLORS_HEX.Relic }}>● Relic</span>
          <span style={{ color: TYPE_COLORS_HEX['FR-I'] }}>● FR-I</span>
          <span style={{ color: TYPE_COLORS_HEX['FR-II'] }}>● FR-II</span>
        </div>
      </div>

      {/* Mirror Line Legend */}
      <div style={{
        marginTop: '8px',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Light Path Types:</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
          <span><span style={{ color: '#FF4444' }}>---</span> X-face wrap</span>
          <span><span style={{ color: '#44FF44' }}>---</span> Y-face wrap</span>
          <span><span style={{ color: '#4444FF' }}>---</span> Z-face wrap</span>
          <span><span style={{ color: '#FF44FF' }}>---</span> Z₂ inversion</span>
        </div>
      </div>

      {/* Methodology explanation */}
      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '9px',
        color: '#888',
      }}>
        <div style={{ marginBottom: '4px', color: '#FFD700' }}>Ghost Probability:</div>
        <div style={{ lineHeight: '1.3' }}>
          70% geometric match (position fits T³/Z₂ image) +
          30% property match (flux & size ratios).
          Dashed lines show light path through topology boundary.
        </div>
      </div>

      <div style={{
        marginTop: '8px',
        fontSize: '9px',
        color: '#555'
      }}>
        Data: LOFAR / MeerKAT / ASKAP
        <div style={{ marginTop: '2px' }}>
          GPU-optimized: 3-4 draw calls for all sources
        </div>
      </div>
    </div>
  );
}

export default RadioMirrors;
