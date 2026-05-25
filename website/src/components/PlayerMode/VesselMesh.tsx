// =============================================================================
// VESSEL MESH COMPONENTS (Directive WWW)
// =============================================================================
// Procedural low-poly meshes for each vessel type
// These can be replaced with GLTF models later
// =============================================================================

'use client';

import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { VesselType, VESSEL_CONFIGS } from '../../store/playerStore';

interface VesselMeshProps {
  vesselType: VesselType;
  isWarping?: boolean;
  parity?: 1 | -1;
}

// UFO - Classic flying saucer
const UFOMesh: React.FC<{ color: string; isWarping: boolean }> = ({ color, isWarping }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      // Gentle hover animation
      groupRef.current.position.y = Math.sin(state.clock.elapsedTime * 2) * 0.02;
      // Spin when warping
      if (isWarping) {
        groupRef.current.rotation.y += 0.05;
      }
    }
  });

  return (
    <group ref={groupRef}>
      {/* Main saucer body */}
      <mesh>
        <cylinderGeometry args={[0.5, 0.8, 0.15, 16]} />
        <meshStandardMaterial color={color} metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Dome */}
      <mesh position={[0, 0.12, 0]}>
        <sphereGeometry args={[0.25, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2]} />
        <meshStandardMaterial color="#88ffff" metalness={0.3} roughness={0.1} transparent opacity={0.7} />
      </mesh>
      {/* Bottom glow */}
      <mesh position={[0, -0.1, 0]}>
        <ringGeometry args={[0.3, 0.7, 16]} />
        <meshBasicMaterial color={isWarping ? '#00ffff' : '#004444'} side={THREE.DoubleSide} />
      </mesh>
      {/* Lights */}
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <mesh key={i} position={[Math.cos(i * Math.PI / 3) * 0.6, 0, Math.sin(i * Math.PI / 3) * 0.6]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color={isWarping ? '#ffffff' : '#ffff00'} />
        </mesh>
      ))}
    </group>
  );
};

// Space Truck - Futuristic hauler
const TruckMesh: React.FC<{ color: string; isWarping: boolean }> = ({ color, isWarping }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame(() => {
    if (groupRef.current && isWarping) {
      groupRef.current.children.forEach((child, i) => {
        if (i > 0) child.rotation.x += 0.02;
      });
    }
  });

  return (
    <group ref={groupRef}>
      {/* Cab */}
      <mesh position={[0, 0.15, 0.4]}>
        <boxGeometry args={[0.5, 0.4, 0.4]} />
        <meshStandardMaterial color={color} metalness={0.6} roughness={0.3} />
      </mesh>
      {/* Windshield */}
      <mesh position={[0, 0.25, 0.55]}>
        <boxGeometry args={[0.45, 0.2, 0.05]} />
        <meshStandardMaterial color="#88ccff" metalness={0.3} roughness={0.1} transparent opacity={0.6} />
      </mesh>
      {/* Trailer */}
      <mesh position={[0, 0.1, -0.4]}>
        <boxGeometry args={[0.6, 0.5, 1.2]} />
        <meshStandardMaterial color="#666666" metalness={0.5} roughness={0.5} />
      </mesh>
      {/* Engine pods */}
      {[-0.4, 0.4].map((x) => (
        <mesh key={x} position={[x, -0.1, -0.8]}>
          <cylinderGeometry args={[0.1, 0.15, 0.4, 8]} />
          <meshStandardMaterial color="#333333" metalness={0.7} roughness={0.3} />
          <mesh position={[0, -0.25, 0]}>
            <coneGeometry args={[0.12, 0.2, 8]} />
            <meshBasicMaterial color={isWarping ? '#ff6600' : '#442200'} />
          </mesh>
        </mesh>
      ))}
    </group>
  );
};

// Sedan - Space taxi
const SedanMesh: React.FC<{ color: string; isWarping: boolean }> = ({ color, isWarping }) => {
  return (
    <group>
      {/* Body */}
      <mesh>
        <boxGeometry args={[0.4, 0.2, 0.8]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>
      {/* Roof */}
      <mesh position={[0, 0.15, 0]}>
        <boxGeometry args={[0.35, 0.15, 0.4]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>
      {/* Windows */}
      <mesh position={[0, 0.15, 0]}>
        <boxGeometry args={[0.36, 0.12, 0.35]} />
        <meshStandardMaterial color="#4488ff" metalness={0.2} roughness={0.1} transparent opacity={0.5} />
      </mesh>
      {/* Hover pads */}
      {[[-0.15, 0.25], [-0.15, -0.25], [0.15, 0.25], [0.15, -0.25]].map(([x, z], i) => (
        <mesh key={i} position={[x, -0.12, z]}>
          <cylinderGeometry args={[0.08, 0.08, 0.03, 8]} />
          <meshBasicMaterial color={isWarping ? '#00ffff' : '#004466'} />
        </mesh>
      ))}
      {/* Headlights */}
      {[-0.12, 0.12].map((x) => (
        <mesh key={x} position={[x, 0, 0.42]}>
          <sphereGeometry args={[0.04, 8, 8]} />
          <meshBasicMaterial color={isWarping ? '#ffffff' : '#ffff88'} />
        </mesh>
      ))}
    </group>
  );
};

// Plane - Starfighter
const PlaneMesh: React.FC<{ color: string; isWarping: boolean }> = ({ color, isWarping }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame(() => {
    if (groupRef.current && isWarping) {
      // Slight wobble when warping
      groupRef.current.rotation.z = Math.sin(Date.now() * 0.01) * 0.05;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Fuselage */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <coneGeometry args={[0.15, 1.2, 8]} />
        <meshStandardMaterial color={color} metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Cockpit */}
      <mesh position={[0, 0.08, 0.2]}>
        <sphereGeometry args={[0.12, 8, 8, 0, Math.PI * 2, 0, Math.PI / 2]} />
        <meshStandardMaterial color="#88ddff" metalness={0.2} roughness={0.1} transparent opacity={0.6} />
      </mesh>
      {/* Wings */}
      {[-1, 1].map((side) => (
        <mesh key={side} position={[side * 0.4, 0, 0]} rotation={[0, 0, side * 0.1]}>
          <boxGeometry args={[0.5, 0.02, 0.3]} />
          <meshStandardMaterial color={color} metalness={0.8} roughness={0.2} />
        </mesh>
      ))}
      {/* Tail fins */}
      <mesh position={[0, 0.15, -0.4]} rotation={[0.3, 0, 0]}>
        <boxGeometry args={[0.02, 0.2, 0.15]} />
        <meshStandardMaterial color={color} metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Engine */}
      <mesh position={[0, 0, -0.55]}>
        <cylinderGeometry args={[0.12, 0.08, 0.15, 8]} />
        <meshBasicMaterial color={isWarping ? '#ff4400' : '#441100'} />
      </mesh>
    </group>
  );
};

// Donut - The cosmic pastry
const DonutMesh: React.FC<{ color: string; isWarping: boolean }> = ({ color, isWarping }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      // Slow rotation
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
      groupRef.current.rotation.z += isWarping ? 0.02 : 0.005;
    }
  });

  // Generate sprinkle positions
  const sprinkles = React.useMemo(() => {
    const positions: [number, number, number, string][] = [];
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
    for (let i = 0; i < 30; i++) {
      const angle = (i / 30) * Math.PI * 2;
      const radius = 0.35 + Math.random() * 0.1;
      const height = 0.08 + Math.random() * 0.05;
      positions.push([
        Math.cos(angle) * radius,
        height,
        Math.sin(angle) * radius,
        colors[i % colors.length],
      ]);
    }
    return positions;
  }, []);

  return (
    <group ref={groupRef}>
      {/* Donut body */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.35, 0.15, 16, 32]} />
        <meshStandardMaterial color={color} metalness={0.1} roughness={0.8} />
      </mesh>
      {/* Frosting */}
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0.05, 0]}>
        <torusGeometry args={[0.35, 0.12, 16, 32, Math.PI]} />
        <meshStandardMaterial color="#ffaacc" metalness={0.2} roughness={0.6} />
      </mesh>
      {/* Sprinkles */}
      {sprinkles.map(([x, y, z, col], i) => (
        <mesh key={i} position={[x, y, z]} rotation={[Math.random(), Math.random(), Math.random()]}>
          <capsuleGeometry args={[0.01, 0.03, 4, 4]} />
          <meshBasicMaterial color={col} />
        </mesh>
      ))}
      {/* Warp glow in center */}
      {isWarping && (
        <mesh>
          <sphereGeometry args={[0.15, 16, 16]} />
          <meshBasicMaterial color="#ff00ff" transparent opacity={0.5} />
        </mesh>
      )}
    </group>
  );
};

// Main vessel component that switches between types
export const VesselMesh: React.FC<VesselMeshProps> = ({
  vesselType,
  isWarping = false,
  parity = 1,
}) => {
  const config = VESSEL_CONFIGS[vesselType];

  const getMesh = () => {
    switch (vesselType) {
      case 'ufo':
        return <UFOMesh color={config.color} isWarping={isWarping} />;
      case 'truck':
        return <TruckMesh color={config.color} isWarping={isWarping} />;
      case 'sedan':
        return <SedanMesh color={config.color} isWarping={isWarping} />;
      case 'plane':
        return <PlaneMesh color={config.color} isWarping={isWarping} />;
      case 'donut':
        return <DonutMesh color={config.color} isWarping={isWarping} />;
      default:
        return <UFOMesh color={config.color} isWarping={isWarping} />;
    }
  };

  return (
    <group scale={config.scale * (parity === -1 ? -1 : 1)}>
      {getMesh()}
    </group>
  );
};

export default VesselMesh;
