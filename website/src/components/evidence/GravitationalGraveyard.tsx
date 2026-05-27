/**
 * =============================================================================
 * GRAVITATIONAL GRAVEYARD - LIGO GWTC-4 Visualization
 * =============================================================================
 *
 * Directive TTTT: Visualize the spatial distribution of gravitational wave
 * events relative to the T³/Z₂ fundamental domain geometry.
 *
 * Each merger rendered as a pulsing sphere:
 * - Size: logarithmic total mass
 * - Color: BBH (purple), BNS (blue), NSBH (red)
 * - Pulse: SNR-based frequency
 * - Lines: Connection to nearest boundary face
 *
 * =============================================================================
 */

import React, { useRef, useMemo, useState, useEffect } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Line, Text } from '@react-three/drei';

// Constants
const L_C = 20.6; // Fundamental domain size in Gpc
const HALF_BOX = L_C / 2;
const SCALE = 1.0; // Scale factor for visualization

// Color scheme matching data pipeline
const TYPE_COLORS = {
  BBH: '#9B59B6',  // Purple
  BNS: '#3498DB',  // Blue
  NSBH: '#E74C3C', // Red
};

// Vertex positions (8 corners of the cube)
const VERTICES = [
  [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1],
  [-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1],
].map(([x, y, z]) => new THREE.Vector3(x * HALF_BOX * SCALE, y * HALF_BOX * SCALE, z * HALF_BOX * SCALE));

// GW Event interface (matches JSON structure from gw_catalog_fetcher.py)
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

// Transformed event for visualization
interface GWEvent {
  name: string;
  type: 'BBH' | 'BNS' | 'NSBH';
  total_mass: number;
  distance_gpc: number;
  snr: number;
  position: { x: number; y: number; z: number };
  boundary_distance: number;
  nearest_boundary: string;
}

// Props
interface GravitationalGraveyardProps {
  opacity?: number;
  showBoundaryLines?: boolean;
  showVertices?: boolean;
  pulseEnabled?: boolean;
  selectedType?: 'all' | 'BBH' | 'BNS' | 'NSBH';
}

/**
 * Single GW Event marker with pulsing animation
 */
function GWEventMarker({
  event,
  pulseEnabled = true,
  showBoundaryLine = false,
}: {
  event: GWEvent;
  pulseEnabled?: boolean;
  showBoundaryLine?: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  // Compute visual properties
  const position = useMemo(() => new THREE.Vector3(
    event.position.x * SCALE,
    event.position.y * SCALE,
    event.position.z * SCALE
  ), [event]);

  const baseSize = useMemo(() => {
    // Logarithmic scaling based on total mass
    const logMass = Math.log10(event.total_mass);
    return 0.1 + (logMass - 1) * 0.15;
  }, [event.total_mass]);

  const pulseFrequency = useMemo(() => {
    // SNR-based pulse frequency (higher SNR = faster pulse)
    return 0.5 + (event.snr / 50) * 2;
  }, [event.snr]);

  const color = useMemo(() => new THREE.Color(TYPE_COLORS[event.type]), [event.type]);

  // Compute boundary line endpoint
  const boundaryPoint = useMemo(() => {
    const { nearest_boundary } = event;
    const p = position.clone();

    // Project to nearest face
    switch (nearest_boundary) {
      case '+X': return new THREE.Vector3(HALF_BOX * SCALE, p.y, p.z);
      case '-X': return new THREE.Vector3(-HALF_BOX * SCALE, p.y, p.z);
      case '+Y': return new THREE.Vector3(p.x, HALF_BOX * SCALE, p.z);
      case '-Y': return new THREE.Vector3(p.x, -HALF_BOX * SCALE, p.z);
      case '+Z': return new THREE.Vector3(p.x, p.y, HALF_BOX * SCALE);
      case '-Z': return new THREE.Vector3(p.x, p.y, -HALF_BOX * SCALE);
      default: return p;
    }
  }, [event.nearest_boundary, position]);

  // Animation
  useFrame(({ clock }) => {
    if (!meshRef.current) return;

    if (pulseEnabled) {
      const pulse = Math.sin(clock.getElapsedTime() * pulseFrequency * Math.PI) * 0.3 + 1;
      meshRef.current.scale.setScalar(pulse);

      if (glowRef.current) {
        (glowRef.current.material as THREE.MeshBasicMaterial).opacity =
          0.1 + Math.sin(clock.getElapsedTime() * pulseFrequency * Math.PI * 2) * 0.1;
      }
    }
  });

  return (
    <group position={position}>
      {/* Core sphere */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[baseSize, 16, 16]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.5}
          roughness={0.3}
          metalness={0.7}
        />
      </mesh>

      {/* Outer glow */}
      <mesh ref={glowRef}>
        <sphereGeometry args={[baseSize * 2, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Boundary connection line */}
      {showBoundaryLine && (
        <Line
          points={[new THREE.Vector3(0, 0, 0), boundaryPoint.clone().sub(position)]}
          color={color}
          lineWidth={1}
          transparent
          opacity={0.3}
          dashed
          dashSize={0.2}
          dashScale={10}
        />
      )}
    </group>
  );
}

/**
 * Vertex marker at T³/Z₂ fixed points
 */
function VertexMarker({ position, index }: { position: THREE.Vector3; index: number }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = clock.getElapsedTime() * 0.5;
      meshRef.current.rotation.y = clock.getElapsedTime() * 0.3;
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
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
 * Main Gravitational Graveyard visualization
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

  // Load GW data and transform to visualization format
  useEffect(() => {
    fetch('/data/gw_graveyard_data.json')
      .then(res => res.json())
      .then(data => {
        // Transform raw events to visualization format
        const transformedEvents: GWEvent[] = (data.events || [])
          .filter((e: GWEventRaw) => e.position_gpc !== null)
          .map((e: GWEventRaw) => {
            // Determine nearest boundary from nearest_vertex
            const vertexSigns = [
              [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1],
              [-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1],
            ];
            const vertex = vertexSigns[e.nearest_vertex] || [0, 0, 0];

            // Find which axis is closest to boundary
            const pos = e.position_gpc!;
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

            return {
              name: e.name,
              type: e.type,
              total_mass: e.mfinal_solar,
              distance_gpc: e.distance_gpc,
              snr: e.snr,
              position: e.position_gpc!,
              boundary_distance: e.boundary_distance_gpc,
              nearest_boundary,
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

  // Slow rotation
  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.02;
    }
  });

  if (loading) return null;

  return (
    <group ref={groupRef}>
      {/* GW Events */}
      {filteredEvents.map((event, i) => (
        <GWEventMarker
          key={event.name || i}
          event={event}
          pulseEnabled={pulseEnabled}
          showBoundaryLine={showBoundaryLines}
        />
      ))}

      {/* Vertex markers */}
      {showVertices && VERTICES.map((pos, i) => (
        <VertexMarker key={i} position={pos} index={i} />
      ))}

      {/* Fundamental domain wireframe (faint) */}
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
  events?: GWEvent[];
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
        <span style={{ color: TYPE_COLORS.BBH }}>BBH:</span> {counts.BBH}
      </div>
      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: TYPE_COLORS.BNS }}>BNS:</span> {counts.BNS}
      </div>
      <div style={{ marginBottom: '8px' }}>
        <span style={{ color: TYPE_COLORS.NSBH }}>NSBH:</span> {counts.NSBH}
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
        <div style={{ marginTop: '5px', fontSize: '10px', color: '#666' }}>
          Source: LIGO-Virgo-KAGRA GWTC-4
        </div>
      </div>
    </div>
  );
}

export default GravitationalGraveyard;
