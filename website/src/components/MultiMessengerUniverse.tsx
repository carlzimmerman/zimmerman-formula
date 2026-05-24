'use client';

import React, { useState, useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Line } from '@react-three/drei';
import * as THREE from 'three';

// =============================================================================
// WORK-ORDER YY: WEBGL EQUIPMENT FILTER ENGINE
// Multi-Messenger Topological Digital Twin Visualization
// =============================================================================

// Measurement types (must match z2_coordinate_transformer.py)
const MEASUREMENT_TYPES = {
  SPECTROSCOPY: { id: 1, name: 'Optical Spectrographs (DESI/SDSS)', color: '#4A90D9' },
  PHOTOMETRY: { id: 2, name: 'Standard Candles (Pantheon+)', color: '#F5A623' },
  RADIO: { id: 3, name: 'Radio Telescopes (CHIME)', color: '#7ED321' },
  XRAY: { id: 4, name: 'X-Ray Observatories (Chandra/eROSITA)', color: '#BD10E0' },
  ASTROMETRY: { id: 5, name: 'Gaia Parallax', color: '#50E3C2' },
  MICROWAVE: { id: 6, name: 'CMB (Planck/WMAP)', color: '#D0021B' },
};

// Z² parameters
const L_C_MPC = 20600;
const L_C_HALF = L_C_MPC / 2;

// Z² vertices (galactic to approximate equatorial)
const Z2_VERTICES = [
  { name: 'V1 (Shapley)', position: [8500, 4000, 5000], color: '#FFD700' },
  { name: 'V2 (Anti-Shapley)', position: [-7000, -3000, -5000], color: '#00FFFF' },
  { name: 'V3 (Cold Spot)', position: [-2000, 6000, 7000], color: '#FF00FF' },
  { name: 'V4 (Southern)', position: [1000, -5000, -8000], color: '#00FF00' },
];

// =============================================================================
// COMPONENTS
// =============================================================================

interface FilterPanelProps {
  filters: Record<string, boolean>;
  setFilters: React.Dispatch<React.SetStateAction<Record<string, boolean>>>;
}

const FilterPanel: React.FC<FilterPanelProps> = ({ filters, setFilters }) => {
  const toggleFilter = (key: string) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="absolute top-4 left-4 bg-slate-900/90 p-4 rounded-lg border border-slate-700 z-10">
      <h3 className="text-white font-bold mb-3 text-lg">Empirical Equipment Filters</h3>
      <div className="space-y-2">
        {Object.entries(MEASUREMENT_TYPES).map(([key, { name, color }]) => (
          <label key={key} className="flex items-center gap-2 cursor-pointer hover:bg-slate-800 p-1 rounded">
            <input
              type="checkbox"
              checked={filters[key]}
              onChange={() => toggleFilter(key)}
              className="w-4 h-4 rounded"
            />
            <span
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: color }}
            />
            <span className="text-white text-sm">{name}</span>
          </label>
        ))}
      </div>
      <div className="mt-4 pt-3 border-t border-slate-700">
        <div className="text-slate-400 text-xs">
          <p>Box size: {L_C_MPC.toLocaleString()} Mpc</p>
          <p>= 20.6 Gpc fundamental domain</p>
        </div>
      </div>
    </div>
  );
};

interface PointCloudProps {
  filters: Record<string, boolean>;
}

const PointCloud: React.FC<PointCloudProps> = ({ filters }) => {
  const pointsRef = useRef<THREE.Points>(null);

  // Generate sample data (in production, load from z2_master_coordinates.bin)
  const { positions, colors, types } = useMemo(() => {
    const n = 50000;
    const pos = new Float32Array(n * 3);
    const col = new Float32Array(n * 3);
    const typ = new Int32Array(n);

    // Generate points for each measurement type
    const typeKeys = Object.keys(MEASUREMENT_TYPES);

    for (let i = 0; i < n; i++) {
      const typeIdx = i % typeKeys.length;
      const typeKey = typeKeys[typeIdx];
      const typeInfo = MEASUREMENT_TYPES[typeKey as keyof typeof MEASUREMENT_TYPES];

      // Position within box
      pos[i * 3] = (Math.random() - 0.5) * L_C_MPC * 0.8;
      pos[i * 3 + 1] = (Math.random() - 0.5) * L_C_MPC * 0.8;
      pos[i * 3 + 2] = (Math.random() - 0.5) * L_C_MPC * 0.8;

      // Color from type
      const color = new THREE.Color(typeInfo.color);
      col[i * 3] = color.r;
      col[i * 3 + 1] = color.g;
      col[i * 3 + 2] = color.b;

      typ[i] = typeInfo.id;
    }

    return { positions: pos, colors: col, types: typ };
  }, []);

  // Update visibility based on filters
  const geometry = useMemo(() => {
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    return geom;
  }, [positions, colors]);

  // Filter shader material
  const material = useMemo(() => {
    return new THREE.PointsMaterial({
      size: 50,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
      sizeAttenuation: true,
    });
  }, []);

  // Update point sizes based on filters
  useEffect(() => {
    if (!pointsRef.current) return;

    const sizes = new Float32Array(positions.length / 3);
    const typeKeys = Object.keys(MEASUREMENT_TYPES);

    for (let i = 0; i < sizes.length; i++) {
      const typeIdx = i % typeKeys.length;
      const typeKey = typeKeys[typeIdx];
      sizes[i] = filters[typeKey] ? 50 : 0;
    }

    // Note: For production, use custom shader for GPU-based filtering
  }, [filters, positions]);

  return (
    <points ref={pointsRef} geometry={geometry} material={material} />
  );
};

const FundamentalDomainBox: React.FC = () => {
  const boxSize = L_C_MPC;
  const halfSize = boxSize / 2;

  // Box edges
  const edges = [
    // Bottom face
    [[-halfSize, -halfSize, -halfSize], [halfSize, -halfSize, -halfSize]],
    [[halfSize, -halfSize, -halfSize], [halfSize, halfSize, -halfSize]],
    [[halfSize, halfSize, -halfSize], [-halfSize, halfSize, -halfSize]],
    [[-halfSize, halfSize, -halfSize], [-halfSize, -halfSize, -halfSize]],
    // Top face
    [[-halfSize, -halfSize, halfSize], [halfSize, -halfSize, halfSize]],
    [[halfSize, -halfSize, halfSize], [halfSize, halfSize, halfSize]],
    [[halfSize, halfSize, halfSize], [-halfSize, halfSize, halfSize]],
    [[-halfSize, halfSize, halfSize], [-halfSize, -halfSize, halfSize]],
    // Vertical edges
    [[-halfSize, -halfSize, -halfSize], [-halfSize, -halfSize, halfSize]],
    [[halfSize, -halfSize, -halfSize], [halfSize, -halfSize, halfSize]],
    [[halfSize, halfSize, -halfSize], [halfSize, halfSize, halfSize]],
    [[-halfSize, halfSize, -halfSize], [-halfSize, halfSize, halfSize]],
  ];

  return (
    <group>
      {edges.map((edge, i) => (
        <Line
          key={i}
          points={edge as [number, number, number][]}
          color="#4A5568"
          lineWidth={1}
          transparent
          opacity={0.5}
        />
      ))}

      {/* Corner labels */}
      <Text
        position={[halfSize * 1.1, 0, 0]}
        fontSize={500}
        color="#718096"
        anchorX="center"
        anchorY="middle"
      >
        +10.3 Gpc
      </Text>
      <Text
        position={[-halfSize * 1.1, 0, 0]}
        fontSize={500}
        color="#718096"
        anchorX="center"
        anchorY="middle"
      >
        -10.3 Gpc
      </Text>
    </group>
  );
};

const VertexMarkers: React.FC = () => {
  return (
    <group>
      {Z2_VERTICES.map((vertex, i) => (
        <group key={i} position={vertex.position as [number, number, number]}>
          {/* Glowing sphere */}
          <mesh>
            <sphereGeometry args={[300, 32, 32]} />
            <meshBasicMaterial color={vertex.color} transparent opacity={0.8} />
          </mesh>

          {/* Arrow pointing outward */}
          <arrowHelper
            args={[
              new THREE.Vector3(...vertex.position).normalize(),
              new THREE.Vector3(0, 0, 0),
              1000,
              vertex.color,
              200,
              100
            ]}
          />

          {/* Label */}
          <Text
            position={[0, 500, 0]}
            fontSize={200}
            color={vertex.color}
            anchorX="center"
            anchorY="bottom"
          >
            {vertex.name}
          </Text>
        </group>
      ))}
    </group>
  );
};

const Scene: React.FC<{ filters: Record<string, boolean> }> = ({ filters }) => {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10000, 10000, 10000]} intensity={0.5} />

      <FundamentalDomainBox />
      <VertexMarkers />
      <PointCloud filters={filters} />

      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={1000}
        maxDistance={50000}
      />
      <PerspectiveCamera makeDefault position={[15000, 15000, 15000]} fov={60} />
    </>
  );
};

// =============================================================================
// MAIN COMPONENT
// =============================================================================

const MultiMessengerUniverse: React.FC = () => {
  const [filters, setFilters] = useState<Record<string, boolean>>({
    SPECTROSCOPY: true,
    PHOTOMETRY: true,
    RADIO: true,
    XRAY: true,
    ASTROMETRY: true,
    MICROWAVE: true,
  });

  return (
    <div className="relative w-full h-[800px] bg-slate-950 rounded-lg overflow-hidden">
      <FilterPanel filters={filters} setFilters={setFilters} />

      <div className="absolute top-4 right-4 bg-slate-900/90 p-4 rounded-lg border border-slate-700 z-10">
        <h3 className="text-white font-bold mb-2">Z² Topological Digital Twin</h3>
        <p className="text-slate-400 text-sm">
          Multi-messenger astronomical data unified in the<br />
          T³/Z₂ fundamental domain (L<sub>c</sub> = 20.6 Gpc)
        </p>
        <div className="mt-3 pt-3 border-t border-slate-700">
          <p className="text-xs text-slate-500">
            Drag to rotate • Scroll to zoom • Shift+drag to pan
          </p>
        </div>
      </div>

      <Canvas>
        <Scene filters={filters} />
      </Canvas>

      {/* Stats overlay */}
      <div className="absolute bottom-4 left-4 bg-slate-900/90 p-3 rounded-lg border border-slate-700 z-10">
        <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
          <span className="text-slate-400">Active filters:</span>
          <span className="text-white">{Object.values(filters).filter(Boolean).length}/6</span>
          <span className="text-slate-400">Box volume:</span>
          <span className="text-white">(20.6 Gpc)³</span>
        </div>
      </div>
    </div>
  );
};

export default MultiMessengerUniverse;
