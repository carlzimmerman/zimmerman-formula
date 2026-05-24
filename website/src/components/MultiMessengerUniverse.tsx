'use client';

import React, { useState, useRef, useMemo, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
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

// Z² parameters - SCALED for WebGL (1 unit = 1000 Mpc = 1 Gpc)
const SCALE = 0.001; // Convert Mpc to Gpc for manageable scene units
const L_C_GPC = 20.6; // Fundamental domain in Gpc (scene units)
const HALF_BOX = L_C_GPC / 2; // ±10.3 Gpc

// Z² vertices (scaled to Gpc)
const Z2_VERTICES = [
  { name: 'V1 (Shapley)', position: [8.5, 4.0, 5.0] as [number, number, number], color: '#FFD700' },
  { name: 'V2 (Anti-Shapley)', position: [-7.0, -3.0, -5.0] as [number, number, number], color: '#00FFFF' },
  { name: 'V3 (Cold Spot)', position: [-2.0, 6.0, 7.0] as [number, number, number], color: '#FF00FF' },
  { name: 'V4 (Southern)', position: [1.0, -5.0, -8.0] as [number, number, number], color: '#00FF00' },
];

// =============================================================================
// COMPONENTS
// =============================================================================

interface FilterPanelProps {
  filters: Record<string, boolean>;
  setFilters: React.Dispatch<React.SetStateAction<Record<string, boolean>>>;
  pointCounts: Record<string, number>;
}

const FilterPanel: React.FC<FilterPanelProps> = ({ filters, setFilters, pointCounts }) => {
  const toggleFilter = (key: string) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const totalVisible = Object.entries(filters)
    .filter(([_, enabled]) => enabled)
    .reduce((sum, [key]) => sum + (pointCounts[key] || 0), 0);

  return (
    <div className="absolute top-4 left-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm">
      <h3 className="text-white font-bold mb-3 text-lg">Equipment Filters</h3>
      <div className="space-y-2">
        {Object.entries(MEASUREMENT_TYPES).map(([key, { name, color }]) => (
          <label key={key} className="flex items-center gap-2 cursor-pointer hover:bg-slate-800 p-1 rounded transition-colors">
            <input
              type="checkbox"
              checked={filters[key]}
              onChange={() => toggleFilter(key)}
              className="w-4 h-4 rounded accent-blue-500"
            />
            <span
              className="w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: color, boxShadow: `0 0 6px ${color}` }}
            />
            <span className="text-white text-sm">{name}</span>
            <span className="text-slate-500 text-xs ml-auto">
              {((pointCounts[key] || 0) / 1000).toFixed(1)}k
            </span>
          </label>
        ))}
      </div>
      <div className="mt-4 pt-3 border-t border-slate-700">
        <div className="text-slate-400 text-xs space-y-1">
          <p><strong className="text-white">{(totalVisible / 1000).toFixed(1)}k</strong> points visible</p>
          <p>Box: L<sub>c</sub> = 20.6 Gpc</p>
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

  // Generate points with proper filtering via geometry regeneration
  const { geometry, visibleCount } = useMemo(() => {
    const n = 50000;
    const typeKeys = Object.keys(MEASUREMENT_TYPES);

    // First pass: count visible points
    const visibleIndices: number[] = [];
    for (let i = 0; i < n; i++) {
      const typeIdx = i % typeKeys.length;
      const typeKey = typeKeys[typeIdx];
      if (filters[typeKey]) {
        visibleIndices.push(i);
      }
    }

    const visibleCount = visibleIndices.length;
    const pos = new Float32Array(visibleCount * 3);
    const col = new Float32Array(visibleCount * 3);

    // Use seeded random for consistent positions
    const seededRandom = (seed: number) => {
      const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
      return x - Math.floor(x);
    };

    for (let j = 0; j < visibleCount; j++) {
      const i = visibleIndices[j];
      const typeIdx = i % typeKeys.length;
      const typeKey = typeKeys[typeIdx];
      const typeInfo = MEASUREMENT_TYPES[typeKey as keyof typeof MEASUREMENT_TYPES];

      // Seeded random position within box (consistent across filter changes)
      pos[j * 3] = (seededRandom(i * 3) - 0.5) * L_C_GPC * 0.9;
      pos[j * 3 + 1] = (seededRandom(i * 3 + 1) - 0.5) * L_C_GPC * 0.9;
      pos[j * 3 + 2] = (seededRandom(i * 3 + 2) - 0.5) * L_C_GPC * 0.9;

      // Color from type
      const color = new THREE.Color(typeInfo.color);
      col[j * 3] = color.r;
      col[j * 3 + 1] = color.g;
      col[j * 3 + 2] = color.b;
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(col, 3));

    return { geometry: geom, visibleCount };
  }, [filters]);

  // Slow rotation
  useFrame((state) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y = state.clock.elapsedTime * 0.02;
    }
  });

  return (
    <points ref={pointsRef} geometry={geometry}>
      <pointsMaterial
        size={0.08}
        vertexColors
        transparent
        opacity={0.85}
        sizeAttenuation={true}
        depthWrite={false}
      />
    </points>
  );
};

const FundamentalDomainBox: React.FC = () => {
  const h = HALF_BOX;

  // Box edges as proper tuples
  const edges: [[number, number, number], [number, number, number]][] = [
    // Bottom face
    [[-h, -h, -h], [h, -h, -h]],
    [[h, -h, -h], [h, h, -h]],
    [[h, h, -h], [-h, h, -h]],
    [[-h, h, -h], [-h, -h, -h]],
    // Top face
    [[-h, -h, h], [h, -h, h]],
    [[h, -h, h], [h, h, h]],
    [[h, h, h], [-h, h, h]],
    [[-h, h, h], [-h, -h, h]],
    // Vertical edges
    [[-h, -h, -h], [-h, -h, h]],
    [[h, -h, -h], [h, -h, h]],
    [[h, h, -h], [h, h, h]],
    [[-h, h, -h], [-h, h, h]],
  ];

  return (
    <group>
      {edges.map((edge, i) => (
        <Line
          key={i}
          points={edge}
          color="#00ffff"
          lineWidth={1.5}
          transparent
          opacity={0.4}
        />
      ))}

      {/* Axis labels */}
      <Text position={[h + 1, 0, 0]} fontSize={0.8} color="#00ffff" anchorX="left">
        +10.3 Gpc
      </Text>
      <Text position={[-h - 1, 0, 0]} fontSize={0.8} color="#00ffff" anchorX="right">
        -10.3 Gpc
      </Text>
      <Text position={[0, h + 1, 0]} fontSize={0.8} color="#00ffff" anchorX="center">
        +10.3 Gpc
      </Text>
      <Text position={[0, 0, h + 1]} fontSize={0.8} color="#00ffff" anchorX="center">
        +10.3 Gpc
      </Text>
    </group>
  );
};

const VertexMarkers: React.FC = () => {
  return (
    <group>
      {Z2_VERTICES.map((vertex, i) => (
        <group key={i} position={vertex.position}>
          {/* Glowing sphere */}
          <mesh>
            <sphereGeometry args={[0.3, 32, 32]} />
            <meshBasicMaterial color={vertex.color} transparent opacity={0.9} />
          </mesh>

          {/* Outer glow */}
          <mesh>
            <sphereGeometry args={[0.5, 16, 16]} />
            <meshBasicMaterial color={vertex.color} transparent opacity={0.3} />
          </mesh>

          {/* Label */}
          <Text
            position={[0, 0.8, 0]}
            fontSize={0.4}
            color={vertex.color}
            anchorX="center"
            anchorY="bottom"
            outlineWidth={0.02}
            outlineColor="#000000"
          >
            {vertex.name}
          </Text>
        </group>
      ))}

      {/* Earth/Observer at origin */}
      <group position={[0, 0, 0]}>
        <mesh>
          <sphereGeometry args={[0.2, 32, 32]} />
          <meshBasicMaterial color="#00ff00" />
        </mesh>
        <Text
          position={[0, 0.5, 0]}
          fontSize={0.35}
          color="#00ff00"
          anchorX="center"
          outlineWidth={0.02}
          outlineColor="#000000"
        >
          Earth (Observer)
        </Text>
      </group>
    </group>
  );
};

const Scene: React.FC<{ filters: Record<string, boolean> }> = ({ filters }) => {
  return (
    <>
      <color attach="background" args={['#0a0a1a']} />
      <ambientLight intensity={0.6} />

      <FundamentalDomainBox />
      <VertexMarkers />
      <PointCloud filters={filters} />

      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={5}
        maxDistance={80}
        zoomSpeed={0.8}
        rotateSpeed={0.5}
        // Don't capture events when pointer leaves canvas
        enableDamping={true}
        dampingFactor={0.05}
      />
      <PerspectiveCamera makeDefault position={[25, 18, 25]} fov={50} />
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

  // Point counts per type (50k total, evenly distributed)
  const pointCounts = useMemo(() => {
    const perType = Math.floor(50000 / 6);
    return {
      SPECTROSCOPY: perType,
      PHOTOMETRY: perType,
      RADIO: perType,
      XRAY: perType,
      ASTROMETRY: perType,
      MICROWAVE: perType + (50000 % 6),
    };
  }, []);

  // Prevent scroll from propagating to page when over canvas
  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.stopPropagation();
  }, []);

  return (
    <div
      className="relative w-full h-[800px] bg-slate-950 rounded-lg overflow-hidden"
      onWheel={handleWheel}
    >
      <FilterPanel filters={filters} setFilters={setFilters} pointCounts={pointCounts} />

      <div className="absolute top-4 right-4 bg-slate-900/95 p-4 rounded-lg border border-slate-700 z-10 backdrop-blur-sm max-w-xs">
        <h3 className="text-white font-bold mb-2">Z² Topological Digital Twin</h3>
        <p className="text-slate-400 text-sm leading-relaxed">
          Multi-messenger astronomical data unified in the
          T³/Z₂ fundamental domain (L<sub>c</sub> = 20.6 Gpc)
        </p>
        <div className="mt-3 pt-3 border-t border-slate-700">
          <p className="text-xs text-slate-500">
            <span className="text-cyan-400">Drag</span> to rotate • <span className="text-cyan-400">Scroll</span> to zoom • <span className="text-cyan-400">Right-drag</span> to pan
          </p>
        </div>
      </div>

      <Canvas
        gl={{ antialias: true, alpha: false }}
        dpr={[1, 2]}
      >
        <Scene filters={filters} />
      </Canvas>

      {/* Stats overlay */}
      <div className="absolute bottom-4 left-4 bg-slate-900/95 p-3 rounded-lg border border-slate-700 z-10 backdrop-blur-sm">
        <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
          <span className="text-slate-400">Active filters:</span>
          <span className="text-white font-mono">{Object.values(filters).filter(Boolean).length}/6</span>
          <span className="text-slate-400">Domain:</span>
          <span className="text-white font-mono">(20.6 Gpc)³</span>
        </div>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-slate-900/95 p-3 rounded-lg border border-slate-700 z-10 backdrop-blur-sm text-xs">
        <div className="flex items-center gap-2 text-yellow-400">
          <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
          <span>Z² Topological Vertices</span>
        </div>
        <div className="flex items-center gap-2 text-green-400 mt-1">
          <span className="w-2 h-2 rounded-full bg-green-400"></span>
          <span>Observer (Earth)</span>
        </div>
        <div className="flex items-center gap-2 text-cyan-400 mt-1">
          <span className="w-2 h-2 rounded-full bg-cyan-400 opacity-50"></span>
          <span>Fundamental Domain</span>
        </div>
      </div>
    </div>
  );
};

export default MultiMessengerUniverse;
