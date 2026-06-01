/**
 * =============================================================================
 * GRAVITATIONAL GRAVEYARD - LIGO GWTC-4 Visualization (GPU-OPTIMIZED)
 * =============================================================================
 *
 * Directive TTTT: Visualize the spatial distribution of gravitational wave
 * events relative to the T³/Z₂ fundamental domain geometry.
 *
 * PERFORMANCE OPTIMIZED using InstancedMesh:
 * - 90+ events rendered with 2 draw calls instead of 180+
 * - Full geometry quality preserved (16x16 sphere segments)
 * - All features retained (glow, boundary lines, type colors)
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Text } from '@react-three/drei';

// Constants
const L_C = 20.6; // Fundamental domain size in Gpc
const HALF_BOX = L_C / 2;
const SCALE = 1.0;

// Color scheme
const TYPE_COLORS = {
  BBH: new THREE.Color('#9B59B6'),  // Purple
  BNS: new THREE.Color('#3498DB'),  // Blue
  NSBH: new THREE.Color('#E74C3C'), // Red
};

const TYPE_COLORS_HEX = {
  BBH: '#9B59B6',
  BNS: '#3498DB',
  NSBH: '#E74C3C',
};

// Vertex positions (8 corners of the cube)
const VERTICES = [
  [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1],
  [-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1],
].map(([x, y, z]) => new THREE.Vector3(x * HALF_BOX * SCALE, y * HALF_BOX * SCALE, z * HALF_BOX * SCALE));

// GW Event interfaces
interface GWEventRaw {
  name: string;
  type: 'BBH' | 'BNS' | 'NSBH';
  mfinal_solar: number;
  distance_gpc: number;
  snr: number;
  position_gpc: { x: number; y: number; z: number } | null;
  boundary_distance_gpc: number;
  nearest_vertex: number;
}

interface GWEvent {
  name: string;
  type: 'BBH' | 'BNS' | 'NSBH';
  total_mass: number;
  distance_gpc: number;
  snr: number;
  position: THREE.Vector3;
  baseSize: number;
  boundary_distance: number;
  nearest_boundary: string;
  boundaryPoint: THREE.Vector3;
}

interface GravitationalGraveyardProps {
  opacity?: number;
  showBoundaryLines?: boolean;
  showVertices?: boolean;
  pulseEnabled?: boolean;
  selectedType?: 'all' | 'BBH' | 'BNS' | 'NSBH';
}

/**
 * Vertex marker at T³/Z₂ fixed points
 */
function VertexMarker({ position, index }: { position: THREE.Vector3; index: number }) {
  return (
    <group position={position}>
      <mesh>
        <octahedronGeometry args={[0.4]} />
        <meshStandardMaterial
          color="#FFD700"
          emissive="#FFD700"
          emissiveIntensity={0.3}
          wireframe
        />
      </mesh>
      <Text
        position={[0, 0.6, 0]}
        fontSize={0.3}
        color="#FFD700"
        anchorX="center"
        anchorY="middle"
      >
        {`V${index + 1}`}
      </Text>
    </group>
  );
}

/**
 * GPU-Optimized Gravitational Graveyard visualization
 */
export function GravitationalGraveyard({
  opacity = 1,
  showBoundaryLines = false,
  showVertices = true,
  pulseEnabled = true,
  selectedType = 'all',
}: GravitationalGraveyardProps) {
  const [events, setEvents] = useState<GWEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const groupRef = useRef<THREE.Group>(null);
  const coreRef = useRef<THREE.InstancedMesh>(null);
  const glowRef = useRef<THREE.InstancedMesh>(null);

  // Load and transform GW data
  useEffect(() => {
    fetch('/data/gw_graveyard_data.json')
      .then(res => res.json())
      .then(data => {
        const transformedEvents: GWEvent[] = (data.events || [])
          .filter((e: GWEventRaw) => {
            const pos = e.position_gpc;
            return pos !== null && pos !== undefined &&
                   typeof pos.x === 'number' &&
                   typeof pos.y === 'number' &&
                   typeof pos.z === 'number';
          })
          .map((e: GWEventRaw) => {
            const pos = e.position_gpc as { x: number; y: number; z: number };

            // Compute nearest boundary
            const distX = Math.min(HALF_BOX - Math.abs(pos.x), Math.abs(pos.x) + HALF_BOX);
            const distY = Math.min(HALF_BOX - Math.abs(pos.y), Math.abs(pos.y) + HALF_BOX);
            const distZ = Math.min(HALF_BOX - Math.abs(pos.z), Math.abs(pos.z) + HALF_BOX);

            let nearest_boundary = '+X';
            if (distX <= distY && distX <= distZ) {
              nearest_boundary = pos.x > 0 ? '+X' : '-X';
            } else if (distY <= distX && distY <= distZ) {
              nearest_boundary = pos.y > 0 ? '+Y' : '-Y';
            } else {
              nearest_boundary = pos.z > 0 ? '+Z' : '-Z';
            }

            // Pre-compute visual properties
            const position = new THREE.Vector3(pos.x * SCALE, pos.y * SCALE, pos.z * SCALE);
            const logMass = Math.log10(e.mfinal_solar);
            const baseSize = 0.1 + (logMass - 1) * 0.15;

            // Compute boundary point
            let boundaryPoint = position.clone();
            switch (nearest_boundary) {
              case '+X': boundaryPoint = new THREE.Vector3(HALF_BOX * SCALE, position.y, position.z); break;
              case '-X': boundaryPoint = new THREE.Vector3(-HALF_BOX * SCALE, position.y, position.z); break;
              case '+Y': boundaryPoint = new THREE.Vector3(position.x, HALF_BOX * SCALE, position.z); break;
              case '-Y': boundaryPoint = new THREE.Vector3(position.x, -HALF_BOX * SCALE, position.z); break;
              case '+Z': boundaryPoint = new THREE.Vector3(position.x, position.y, HALF_BOX * SCALE); break;
              case '-Z': boundaryPoint = new THREE.Vector3(position.x, position.y, -HALF_BOX * SCALE); break;
            }

            return {
              name: e.name,
              type: e.type,
              total_mass: e.mfinal_solar,
              distance_gpc: e.distance_gpc,
              snr: e.snr,
              position,
              baseSize,
              boundary_distance: e.boundary_distance_gpc,
              nearest_boundary,
              boundaryPoint,
            };
          });

        setEvents(transformedEvents);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load GW data:', err);
        setLoading(false);
      });
  }, []);

  // Filter events by type
  const filteredEvents = useMemo(() => {
    if (selectedType === 'all') return events;
    return events.filter(e => e.type === selectedType);
  }, [events, selectedType]);

  // Reusable objects for instance updates
  const tempMatrix = useMemo(() => new THREE.Matrix4(), []);
  const tempColor = useMemo(() => new THREE.Color(), []);
  const tempScale = useMemo(() => new THREE.Vector3(), []);
  const tempPosition = useMemo(() => new THREE.Vector3(), []);
  const identityQuaternion = useMemo(() => new THREE.Quaternion(), []);

  // Setup instanced meshes
  useEffect(() => {
    if (!coreRef.current || !glowRef.current || filteredEvents.length === 0) return;

    const count = filteredEvents.length;

    for (let i = 0; i < count; i++) {
      const event = filteredEvents[i];

      // CORE SPHERE
      tempPosition.copy(event.position);
      tempScale.set(event.baseSize, event.baseSize, event.baseSize);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      coreRef.current.setMatrixAt(i, tempMatrix);
      tempColor.copy(TYPE_COLORS[event.type]);
      coreRef.current.setColorAt(i, tempColor);

      // GLOW SPHERE (2x size)
      tempScale.set(event.baseSize * 2, event.baseSize * 2, event.baseSize * 2);
      tempMatrix.compose(tempPosition, identityQuaternion, tempScale);
      glowRef.current.setMatrixAt(i, tempMatrix);
      glowRef.current.setColorAt(i, tempColor);
    }

    coreRef.current.instanceMatrix.needsUpdate = true;
    if (coreRef.current.instanceColor) coreRef.current.instanceColor.needsUpdate = true;
    glowRef.current.instanceMatrix.needsUpdate = true;
    if (glowRef.current.instanceColor) glowRef.current.instanceColor.needsUpdate = true;

  }, [filteredEvents, tempMatrix, tempColor, tempScale, tempPosition, identityQuaternion]);

  // Boundary lines geometry (combined into single draw call)
  const boundaryLinesGeometry = useMemo(() => {
    if (!showBoundaryLines || filteredEvents.length === 0) return null;

    const positions: number[] = [];

    for (const event of filteredEvents) {
      // Start point
      positions.push(event.position.x, event.position.y, event.position.z);
      // End point
      positions.push(event.boundaryPoint.x, event.boundaryPoint.y, event.boundaryPoint.z);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    return geometry;
  }, [showBoundaryLines, filteredEvents]);

  if (loading) return null;

  const count = filteredEvents.length;

  return (
    <group ref={groupRef}>
      {/* INSTANCED CORE SPHERES - Full 16x16 geometry, ONE draw call */}
      {count > 0 && (
        <instancedMesh
          ref={coreRef}
          args={[undefined, undefined, count]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 16, 16]} />
          <meshStandardMaterial
            emissive="#ffffff"
            emissiveIntensity={0.5}
            roughness={0.3}
            metalness={0.7}
            toneMapped={false}
          />
        </instancedMesh>
      )}

      {/* INSTANCED GLOW SPHERES - Full 16x16 geometry, ONE draw call */}
      {count > 0 && (
        <instancedMesh
          ref={glowRef}
          args={[undefined, undefined, count]}
          frustumCulled={false}
        >
          <sphereGeometry args={[1, 16, 16]} />
          <meshBasicMaterial
            transparent
            opacity={0.15}
            side={THREE.BackSide}
            depthWrite={false}
          />
        </instancedMesh>
      )}

      {/* BOUNDARY LINES - Combined into single LineSegments draw call */}
      {showBoundaryLines && boundaryLinesGeometry && (
        <lineSegments geometry={boundaryLinesGeometry}>
          <lineBasicMaterial
            color="#888888"
            transparent
            opacity={0.3}
          />
        </lineSegments>
      )}

      {/* Vertex markers (only 8, kept as individual meshes) */}
      {showVertices && VERTICES.map((pos, i) => (
        <VertexMarker key={i} position={pos} index={i} />
      ))}

      {/* Fundamental domain wireframe */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(L_C * SCALE, L_C * SCALE, L_C * SCALE)]} />
        <lineBasicMaterial color="#444" transparent opacity={0.3} />
      </lineSegments>
    </group>
  );
}

/**
 * HUD overlay for Gravitational Graveyard statistics
 */
export function GraveyardHUD({
  events = [],
  clusteringRatio = 0,
}: {
  events?: Array<{ type: 'BBH' | 'BNS' | 'NSBH' }>;
  clusteringRatio?: number;
}) {
  const counts = useMemo(() => {
    const c = { BBH: 0, BNS: 0, NSBH: 0 };
    events.forEach(e => { c[e.type] = (c[e.type] || 0) + 1; });
    return c;
  }, [events]);

  return (
    <div style={{
      position: 'absolute',
      top: '120px',
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
      <div style={{ marginBottom: '10px', fontWeight: 'bold', color: '#FFD700' }}>
        GRAVITATIONAL WAVE GRAVEYARD
      </div>

      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: TYPE_COLORS_HEX.BBH }}>BBH:</span> {counts.BBH}
      </div>
      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: TYPE_COLORS_HEX.BNS }}>BNS:</span> {counts.BNS}
      </div>
      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: TYPE_COLORS_HEX.NSBH }}>NSBH:</span> {counts.NSBH}
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '11px',
        color: '#aaa'
      }}>
        <div>Total Events: {events.length}</div>
        <div>Clustering Ratio: {clusteringRatio.toFixed(2)}</div>
      </div>

      <div style={{
        marginTop: '10px',
        paddingTop: '10px',
        borderTop: '1px solid #444',
        fontSize: '10px',
      }}>
        <div style={{ marginBottom: '5px', color: '#888' }}>Event Types:</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <span><span style={{ color: TYPE_COLORS_HEX.BBH }}>●</span> BBH = Binary Black Hole</span>
          <span><span style={{ color: TYPE_COLORS_HEX.BNS }}>●</span> BNS = Binary Neutron Star</span>
          <span><span style={{ color: TYPE_COLORS_HEX.NSBH }}>●</span> NSBH = Neutron Star + Black Hole</span>
        </div>
      </div>

      <div style={{ marginTop: '8px', fontSize: '9px', color: '#888' }}>
        GPU-optimized: 2 draw calls for {events.length} events
      </div>

      <div style={{ marginTop: '4px', fontSize: '10px', color: '#666' }}>
        Source: LIGO-Virgo-KAGRA GWTC-4
      </div>
    </div>
  );
}

export default GravitationalGraveyard;
