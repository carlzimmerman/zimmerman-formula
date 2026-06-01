'use client';

/**
 * ================================================================================
 * WORK-ORDER LL: THE OCTREE & LOGARITHMIC DEPTH ENGINE
 * ================================================================================
 *
 * Extreme-scale WebGL architecture for rendering AU to Gpc scales.
 *
 * Key Technologies:
 * - Logarithmic Depth Buffer: Prevents Z-fighting across 20+ orders of magnitude
 * - Octree LOD: Dynamically loads/unloads scale-appropriate data chunks
 * - Instanced Rendering: GPU-efficient rendering of millions of objects
 * - Dynamic Streaming: Fetches binary chunks based on camera position
 *
 * Author: Carl Zimmerman + Claude
 * Date: May 23, 2026
 * Framework: Z² Unified Action v11.1.0
 * ================================================================================
 */

import { useRef, useState, useEffect, useMemo, useCallback } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

// =============================================================================
// CONSTANTS
// =============================================================================

// Scale definitions (in scene units, 1 unit = 1 Mpc at cosmic scale)
const SCALES = {
  AU: 1 / 206265 / 1e6,      // AU to Mpc
  PC: 1e-6,                   // pc to Mpc
  KPC: 0.001,                 // kpc to Mpc
  MPC: 1,                     // Mpc
  GPC: 1000,                  // Gpc to Mpc
};

// LOD thresholds (camera distance in Mpc determines which chunks load)
const LOD_THRESHOLDS = {
  solar: { load: 0.001, unload: 0.01 },      // < 1 kpc: show planets
  stellar: { load: 0.1, unload: 1 },          // < 100 kpc: show stars
  local: { load: 10, unload: 100 },           // < 10 Mpc: show local galaxies
  cosmic: { load: 500, unload: 5000 },        // < 500 Mpc: show cosmic web
  edge: { load: 10000, unload: 20000 },       // > 10 Gpc: show quasars
};

// Chunk metadata
interface ChunkData {
  positions: Float32Array;
  colors: Float32Array;
  types: Int32Array;
  loaded: boolean;
  visible: boolean;
}

// =============================================================================
// BINARY DATA LOADER
// =============================================================================

async function loadBinaryChunk(filename: string): Promise<ChunkData | null> {
  try {
    const response = await fetch(`/data/binary/${filename}`);
    if (!response.ok) return null;

    const buffer = await response.arrayBuffer();
    const view = new DataView(buffer);

    // Parse header
    const magic = String.fromCharCode(
      view.getUint8(0), view.getUint8(1), view.getUint8(2), view.getUint8(3)
    );

    if (magic !== 'Z2MK') {
      console.warn(`Invalid chunk magic: ${magic}`);
      return null;
    }

    const nObjects = view.getUint32(4, true);
    const level = view.getUint32(8, true);

    // Calculate offsets
    const headerSize = 12;
    const positionsSize = nObjects * 3 * 4;
    const typesSize = nObjects * 4;
    const colorsSize = nObjects * 3 * 4;

    // Extract arrays
    const positions = new Float32Array(
      buffer, headerSize, nObjects * 3
    );
    const types = new Int32Array(
      buffer, headerSize + positionsSize, nObjects
    );
    const colors = new Float32Array(
      buffer, headerSize + positionsSize + typesSize, nObjects * 3
    );

    console.log(`Loaded chunk: ${filename} (${nObjects} objects, level ${level})`);

    return {
      positions,
      colors,
      types,
      loaded: true,
      visible: true,
    };
  } catch (error) {
    console.error(`Failed to load chunk ${filename}:`, error);
    return null;
  }
}

// =============================================================================
// LOD MANAGER HOOK
// =============================================================================

interface LODState {
  currentLevel: number;
  loadedChunks: Set<string>;
  activeChunks: Map<string, ChunkData>;
}

export function useLODManager() {
  const [state, setState] = useState<LODState>({
    currentLevel: 4, // Start at cosmic scale
    loadedChunks: new Set(),
    activeChunks: new Map(),
  });

  const loadChunk = useCallback(async (chunkName: string) => {
    if (state.loadedChunks.has(chunkName)) return;

    const data = await loadBinaryChunk(`${chunkName}.bin`);
    if (data) {
      setState((prev) => ({
        ...prev,
        loadedChunks: new Set([...prev.loadedChunks, chunkName]),
        activeChunks: new Map([...prev.activeChunks, [chunkName, data]]),
      }));
    }
  }, [state.loadedChunks]);

  const unloadChunk = useCallback((chunkName: string) => {
    setState((prev) => {
      const newActive = new Map(prev.activeChunks);
      newActive.delete(chunkName);
      const newLoaded = new Set(prev.loadedChunks);
      newLoaded.delete(chunkName);
      return {
        ...prev,
        loadedChunks: newLoaded,
        activeChunks: newActive,
      };
    });
  }, []);

  const updateLOD = useCallback((cameraDistance: number) => {
    // Determine which chunks should be visible
    const shouldLoadSolar = cameraDistance < LOD_THRESHOLDS.solar.unload;
    const shouldLoadStellar = cameraDistance < LOD_THRESHOLDS.stellar.unload;
    const shouldLoadLocal = cameraDistance < LOD_THRESHOLDS.local.unload;
    const shouldLoadCosmic = cameraDistance < LOD_THRESHOLDS.cosmic.unload;
    const shouldLoadEdge = cameraDistance > LOD_THRESHOLDS.edge.load;

    // Load/unload based on camera distance
    if (shouldLoadSolar && !state.loadedChunks.has('chunk_0_solar')) {
      loadChunk('chunk_0_solar');
    }
    if (shouldLoadStellar && !state.loadedChunks.has('chunk_1_stellar')) {
      loadChunk('chunk_1_stellar');
    }
    if (shouldLoadLocal && !state.loadedChunks.has('chunk_3_local')) {
      loadChunk('chunk_3_local');
    }
    if (shouldLoadCosmic && !state.loadedChunks.has('chunk_4_cosmic')) {
      loadChunk('chunk_4_cosmic');
    }
    if (shouldLoadEdge && !state.loadedChunks.has('chunk_5_edge')) {
      loadChunk('chunk_5_edge');
    }

    // Update current level
    let newLevel = 5;
    if (cameraDistance < 0.001) newLevel = 0;
    else if (cameraDistance < 0.1) newLevel = 1;
    else if (cameraDistance < 10) newLevel = 3;
    else if (cameraDistance < 500) newLevel = 4;

    if (newLevel !== state.currentLevel) {
      setState((prev) => ({ ...prev, currentLevel: newLevel }));
    }
  }, [state, loadChunk]);

  return { state, loadChunk, unloadChunk, updateLOD };
}

// =============================================================================
// INSTANCED POINT CLOUD COMPONENT
// =============================================================================

interface PointCloudProps {
  positions: Float32Array;
  colors: Float32Array;
  scale?: number;
  pointSize?: number;
}

export function PointCloud({
  positions,
  colors,
  scale = 1,
  pointSize = 0.02,
}: PointCloudProps) {
  const points = useRef<THREE.Points>(null);

  const count = positions.length / 3;

  // Scale positions if needed
  const scaledPositions = useMemo(() => {
    if (scale === 1) return positions;
    const scaled = new Float32Array(positions.length);
    for (let i = 0; i < positions.length; i++) {
      scaled[i] = positions[i] * scale;
    }
    return scaled;
  }, [positions, scale]);

  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={scaledPositions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={count}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={pointSize}
        vertexColors
        transparent
        opacity={0.9}
        sizeAttenuation
      />
    </points>
  );
}

// =============================================================================
// INSTANCED MESH FOR LARGER OBJECTS (PLANETS, STARS)
// =============================================================================

interface InstancedObjectsProps {
  positions: Float32Array;
  colors: Float32Array;
  scale?: number;
  radius?: number;
}

export function InstancedSpheres({
  positions,
  colors,
  scale = 1,
  radius = 0.01,
}: InstancedObjectsProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);

  const count = positions.length / 3;

  useEffect(() => {
    if (!meshRef.current) return;

    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      dummy.position.set(
        positions[i * 3] * scale,
        positions[i * 3 + 1] * scale,
        positions[i * 3 + 2] * scale
      );
      dummy.scale.setScalar(radius);
      dummy.updateMatrix();

      meshRef.current.setMatrixAt(i, dummy.matrix);

      color.setRGB(
        colors[i * 3],
        colors[i * 3 + 1],
        colors[i * 3 + 2]
      );
      meshRef.current.setColorAt(i, color);
    }

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }
  }, [positions, colors, scale, radius, count]);

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 8, 8]} />
      <meshBasicMaterial transparent opacity={0.9} />
    </instancedMesh>
  );
}

// =============================================================================
// CAMERA DISTANCE TRACKER
// =============================================================================

interface CameraTrackerProps {
  onDistanceChange: (distance: number) => void;
  scaleReference?: 'mpc' | 'pc' | 'au';
}

export function CameraTracker({
  onDistanceChange,
  scaleReference = 'mpc',
}: CameraTrackerProps) {
  const { camera } = useThree();

  useFrame(() => {
    let distance = camera.position.length();

    // Convert to Mpc if needed
    if (scaleReference === 'pc') {
      distance *= 1e-6;
    } else if (scaleReference === 'au') {
      distance *= SCALES.AU;
    }

    onDistanceChange(distance);
  });

  return null;
}

// =============================================================================
// LOGARITHMIC DEPTH SHADER MATERIAL
// =============================================================================

export const logDepthVertexShader = `
  varying vec3 vColor;
  varying float vLogDepth;

  void main() {
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    // Logarithmic depth
    float FC = 2.0 / log2(1.0e10 + 1.0);
    gl_Position.z = log2(max(1.0e-6, 1.0 + gl_Position.w)) * FC - 1.0;
    gl_Position.z *= gl_Position.w;
    vLogDepth = 1.0 + gl_Position.w;
  }
`;

export const logDepthFragmentShader = `
  varying vec3 vColor;
  varying float vLogDepth;

  void main() {
    float FC = 2.0 / log2(1.0e10 + 1.0);
    gl_FragDepthEXT = log2(vLogDepth) * FC * 0.5;
    gl_FragColor = vec4(vColor, 1.0);
  }
`;

// =============================================================================
// FRUSTUM CULLING OCTREE
// =============================================================================

interface OctreeNode {
  center: THREE.Vector3;
  halfSize: number;
  children: OctreeNode[] | null;
  objects: number[]; // Indices into position array
  isVisible: boolean;
}

export function createOctree(
  positions: Float32Array,
  maxDepth: number = 5,
  maxObjectsPerNode: number = 100
): OctreeNode {
  // Find bounding box
  let minX = Infinity, minY = Infinity, minZ = Infinity;
  let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;

  const count = positions.length / 3;
  for (let i = 0; i < count; i++) {
    const x = positions[i * 3];
    const y = positions[i * 3 + 1];
    const z = positions[i * 3 + 2];
    minX = Math.min(minX, x);
    minY = Math.min(minY, y);
    minZ = Math.min(minZ, z);
    maxX = Math.max(maxX, x);
    maxY = Math.max(maxY, y);
    maxZ = Math.max(maxZ, z);
  }

  const center = new THREE.Vector3(
    (minX + maxX) / 2,
    (minY + maxY) / 2,
    (minZ + maxZ) / 2
  );
  const halfSize = Math.max(maxX - minX, maxY - minY, maxZ - minZ) / 2;

  // Create root node with all objects
  const root: OctreeNode = {
    center,
    halfSize,
    children: null,
    objects: Array.from({ length: count }, (_, i) => i),
    isVisible: true,
  };

  // Recursively subdivide
  subdivideOctree(root, positions, 0, maxDepth, maxObjectsPerNode);

  return root;
}

function subdivideOctree(
  node: OctreeNode,
  positions: Float32Array,
  depth: number,
  maxDepth: number,
  maxObjects: number
): void {
  if (depth >= maxDepth || node.objects.length <= maxObjects) {
    return;
  }

  node.children = [];
  const hs = node.halfSize / 2;

  // Create 8 children
  for (let i = 0; i < 8; i++) {
    const offsetX = i & 1 ? hs : -hs;
    const offsetY = i & 2 ? hs : -hs;
    const offsetZ = i & 4 ? hs : -hs;

    const child: OctreeNode = {
      center: new THREE.Vector3(
        node.center.x + offsetX,
        node.center.y + offsetY,
        node.center.z + offsetZ
      ),
      halfSize: hs,
      children: null,
      objects: [],
      isVisible: true,
    };

    // Distribute objects to children
    for (const idx of node.objects) {
      const x = positions[idx * 3];
      const y = positions[idx * 3 + 1];
      const z = positions[idx * 3 + 2];

      if (
        x >= child.center.x - hs && x < child.center.x + hs &&
        y >= child.center.y - hs && y < child.center.y + hs &&
        z >= child.center.z - hs && z < child.center.z + hs
      ) {
        child.objects.push(idx);
      }
    }

    if (child.objects.length > 0) {
      node.children.push(child);
      subdivideOctree(child, positions, depth + 1, maxDepth, maxObjects);
    }
  }

  // Clear objects from parent (they're now in children)
  node.objects = [];
}

// =============================================================================
// FRUSTUM VISIBILITY CHECK
// =============================================================================

export function updateOctreeVisibility(
  node: OctreeNode,
  frustum: THREE.Frustum
): void {
  const box = new THREE.Box3(
    new THREE.Vector3(
      node.center.x - node.halfSize,
      node.center.y - node.halfSize,
      node.center.z - node.halfSize
    ),
    new THREE.Vector3(
      node.center.x + node.halfSize,
      node.center.y + node.halfSize,
      node.center.z + node.halfSize
    )
  );

  node.isVisible = frustum.intersectsBox(box);

  if (node.isVisible && node.children) {
    for (const child of node.children) {
      updateOctreeVisibility(child, frustum);
    }
  }
}

// =============================================================================
// EXPORTS
// =============================================================================

export { SCALES, LOD_THRESHOLDS };
