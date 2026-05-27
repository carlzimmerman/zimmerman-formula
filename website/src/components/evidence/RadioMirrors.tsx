/**
 * =============================================================================
 * RADIO MIRRORS - Topological Ghost Visualization
 * =============================================================================
 *
 * Directive VVVV: Visualize LOFAR/MeerKAT/ASKAP radio sources and search
 * for topological mirror images across T³/Z₂ boundaries.
 *
 * Features:
 * - Radio sources color-coded by type
 * - ORC markers as glowing rings
 * - Mirror pair connection lines
 * - Ghost probability indicators
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { Line, Text } from '@react-three/drei';

// Constants
const L_C = 20.6;
const HALF_BOX = L_C / 2;
const SCALE = 0.5; // Scale factor for visualization

// Color scheme
const TYPE_COLORS: Record<string, string> = {
  ORC: '#FF6B6B',     // Red
  GRG: '#4ECDC4',     // Teal
  Relic: '#9B59B6',   // Purple
  'FR-I': '#3498DB',  // Blue
  'FR-II': '#E74C3C', // Red-orange
};

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
}

/**
 * Radio source marker
 */
/**
 * Radio source marker - REAL DATA
 * Position from LOFAR/MeerKAT/ASKAP catalogs, size by flux, color by type
 */
function RadioSourceMarker({
  source,
  isORC = false,
}: {
  source: RadioSource;
  isORC?: boolean;
}) {
  const position = useMemo(() => new THREE.Vector3(
    source.position.x * SCALE,
    source.position.y * SCALE,
    source.position.z * SCALE
  ), [source]);

  const color = useMemo(() => new THREE.Color(TYPE_COLORS[source.type] || '#888'), [source.type]);

  // Size based on log flux (real measurement)
  const size = useMemo(() => {
    const logFlux = Math.log10(source.flux_mjy + 1);
    return 0.05 + logFlux * 0.03;
  }, [source.flux_mjy]);

  // Static - no pulsing/rotation (radio sources are fixed sky positions)

  return (
    <group position={position}>
      {/* Core marker */}
      <mesh>
        <sphereGeometry args={[size, 12, 12]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.5}
          roughness={0.4}
          metalness={0.6}
        />
      </mesh>

      {/* Outer glow */}
      <mesh>
        <sphereGeometry args={[size * 2, 12, 12]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* ORC-specific ring - static (ORCs are Odd Radio Circles at fixed sky positions) */}
      {isORC && (
        <mesh>
          <torusGeometry args={[size * 3, size * 0.3, 8, 32]} />
          <meshStandardMaterial
            color="#FF6B6B"
            emissive="#FF6B6B"
            emissiveIntensity={0.7}
            transparent
            opacity={0.6}
          />
        </mesh>
      )}
    </group>
  );
}

/**
 * Mirror pair connection line
 */
function MirrorLine({
  source1,
  source2,
  probability,
  mirrorType,
}: {
  source1: THREE.Vector3;
  source2: THREE.Vector3;
  probability: number;
  mirrorType: string;
}) {
  const lineRef = useRef<THREE.Line>(null);

  // Color based on mirror type
  const color = useMemo(() => {
    switch (mirrorType) {
      case 'X': return '#FF4444';
      case 'Y': return '#44FF44';
      case 'Z': return '#4444FF';
      case 'INV': return '#FF44FF';
      default: return '#FFFFFF';
    }
  }, [mirrorType]);

  // Midpoint for label
  const midpoint = useMemo(() => {
    return source1.clone().add(source2).multiplyScalar(0.5);
  }, [source1, source2]);

  return (
    <group>
      <Line
        points={[source1, source2]}
        color={color}
        lineWidth={1 + probability * 3}
        transparent
        opacity={0.3 + probability * 0.5}
        dashed
        dashSize={0.1}
        dashScale={5}
      />

      {/* Ghost probability indicator at midpoint */}
      {probability > 0.3 && (
        <Text
          position={midpoint}
          fontSize={0.08}
          color={color}
          anchorX="center"
        >
          {`${(probability * 100).toFixed(0)}%`}
        </Text>
      )}
    </group>
  );
}

/**
 * Main Radio Mirrors visualization
 */
export function RadioMirrors({
  opacity = 1,
  showMirrorLines = true,
  showORCRings = true,
  selectedType = 'all',
  minGhostProbability = 0.2,
}: RadioMirrorsProps) {
  const [data, setData] = useState<RadioData | null>(null);

  // Load data
  useEffect(() => {
    fetch('/data/radio_ghost_data.json')
      .then(res => res.json())
      .then((loadedData: RadioData) => {
        setData(loadedData);
      })
      .catch(console.error);
  }, []);

  // Filter sources
  const filteredSources = useMemo(() => {
    if (!data) return [];
    if (selectedType === 'all') return data.sources;
    return data.sources.filter(s => s.type === selectedType);
  }, [data, selectedType]);

  // Build position lookup for mirror lines
  const positionLookup = useMemo(() => {
    if (!data) return {};
    const lookup: Record<string, THREE.Vector3> = {};
    data.sources.forEach(s => {
      lookup[s.name] = new THREE.Vector3(
        s.position.x * SCALE,
        s.position.y * SCALE,
        s.position.z * SCALE
      );
    });
    return lookup;
  }, [data]);

  // Filter mirror pairs by probability
  const filteredPairs = useMemo(() => {
    if (!data) return [];
    return data.ghost_analysis.mirror_pairs.filter(
      p => p.ghost_probability >= minGhostProbability
    );
  }, [data, minGhostProbability]);

  // Static - no group rotation (sources are at fixed sky positions)

  if (!data) return null;

  return (
    <group>
      {/* Radio sources */}
      {filteredSources.map((source, i) => (
        <RadioSourceMarker
          key={source.name || i}
          source={source}
          isORC={showORCRings && source.type === 'ORC'}
        />
      ))}

      {/* Mirror pair lines */}
      {showMirrorLines && filteredPairs.map((pair, i) => {
        const pos1 = positionLookup[pair.source1];
        const pos2 = positionLookup[pair.source2];
        if (!pos1 || !pos2) return null;

        return (
          <MirrorLine
            key={i}
            source1={pos1}
            source2={pos2}
            probability={pair.ghost_probability}
            mirrorType={pair.mirror_type}
          />
        );
      })}

      {/* Fundamental domain wireframe */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_C * SCALE, L_C * SCALE, L_C * SCALE)]} />
        <lineBasicMaterial color="#333" transparent opacity={0.2} />
      </lineSegments>

      {/* Boundary plane markers */}
      {[
        { pos: [HALF_BOX * SCALE, 0, 0], rot: [0, Math.PI/2, 0], label: '+X' },
        { pos: [-HALF_BOX * SCALE, 0, 0], rot: [0, -Math.PI/2, 0], label: '-X' },
        { pos: [0, HALF_BOX * SCALE, 0], rot: [-Math.PI/2, 0, 0], label: '+Y' },
        { pos: [0, -HALF_BOX * SCALE, 0], rot: [Math.PI/2, 0, 0], label: '-Y' },
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

      <div style={{
        marginTop: '10px',
        fontSize: '10px',
        color: '#666'
      }}>
        LOFAR / MeerKAT / ASKAP
      </div>
    </div>
  );
}

export default RadioMirrors;
