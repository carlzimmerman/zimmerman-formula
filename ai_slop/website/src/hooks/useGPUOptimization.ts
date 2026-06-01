/**
 * =============================================================================
 * GPU OPTIMIZATION HOOKS - React-Three-Fiber Integration
 * =============================================================================
 *
 * Custom hooks for optimized rendering in the T³/Z₂ Digital Twin:
 * - useFrustumCulling: Skip rendering objects outside camera view
 * - useLOD: Level of Detail management
 * - usePerformance: FPS and memory monitoring
 * - useOptimizedPoints: Frustum-culled point cloud rendering
 *
 * =============================================================================
 */

'use client';

import { useRef, useMemo, useCallback, useEffect, useState } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import {
  FrustumCuller,
  LODManager,
  PerformanceMonitor,
  Octree,
  AdaptiveQuality,
  createCosmicOctree,
  LODLevel,
  PerformanceStats,
  HALF_BOX
} from '@/lib/gpuOptimization';

// =============================================================================
// FRUSTUM CULLING HOOK
// =============================================================================

interface UseFrustumCullingResult {
  isVisible: (position: THREE.Vector3) => boolean;
  isBoxVisible: (box: THREE.Box3) => boolean;
  getVisibleObjects: <T extends { position: THREE.Vector3 }>(objects: T[]) => T[];
  culledCount: number;
  visibleCount: number;
}

export function useFrustumCulling(): UseFrustumCullingResult {
  const { camera } = useThree();
  const cullerRef = useRef(new FrustumCuller());
  const statsRef = useRef({ culled: 0, visible: 0 });

  // Update frustum every frame
  useFrame(() => {
    cullerRef.current.update(camera);
  });

  const isVisible = useCallback((position: THREE.Vector3) => {
    return cullerRef.current.isPointVisible(position);
  }, []);

  const isBoxVisible = useCallback((box: THREE.Box3) => {
    return cullerRef.current.isBoxVisible(box);
  }, []);

  const getVisibleObjects = useCallback(<T extends { position: THREE.Vector3 }>(
    objects: T[]
  ): T[] => {
    const visible: T[] = [];
    let culled = 0;

    for (const obj of objects) {
      if (cullerRef.current.isPointVisible(obj.position)) {
        visible.push(obj);
      } else {
        culled++;
      }
    }

    statsRef.current = { culled, visible: visible.length };
    return visible;
  }, []);

  return {
    isVisible,
    isBoxVisible,
    getVisibleObjects,
    culledCount: statsRef.current.culled,
    visibleCount: statsRef.current.visible
  };
}

// =============================================================================
// LOD HOOK
// =============================================================================

interface UseLODResult {
  getLOD: (position: THREE.Vector3) => LODLevel;
  getPointSize: (position: THREE.Vector3) => number;
  getOpacity: (position: THREE.Vector3) => number;
  batchByLOD: <T extends { position: THREE.Vector3 }>(objects: T[]) => Map<LODLevel, T[]>;
  cameraDistance: number;
}

export function useLOD(): UseLODResult {
  const { camera } = useThree();
  const lodManagerRef = useRef(new LODManager());
  const [cameraDistance, setCameraDistance] = useState(0);

  useFrame(() => {
    lodManagerRef.current.updateCamera(camera);
    const pos = new THREE.Vector3();
    camera.getWorldPosition(pos);
    setCameraDistance(pos.length());
  });

  const getLOD = useCallback((position: THREE.Vector3) => {
    return lodManagerRef.current.getLODLevel(position);
  }, []);

  const getPointSize = useCallback((position: THREE.Vector3) => {
    const lod = lodManagerRef.current.getLODLevel(position);
    return lodManagerRef.current.getPointSize(lod);
  }, []);

  const getOpacity = useCallback((position: THREE.Vector3) => {
    const lod = lodManagerRef.current.getLODLevel(position);
    return lodManagerRef.current.getOpacity(lod);
  }, []);

  const batchByLOD = useCallback(<T extends { position: THREE.Vector3 }>(
    objects: T[]
  ) => {
    return lodManagerRef.current.batchByLOD(objects);
  }, []);

  return {
    getLOD,
    getPointSize,
    getOpacity,
    batchByLOD,
    cameraDistance
  };
}

// =============================================================================
// PERFORMANCE MONITORING HOOK
// =============================================================================

interface UsePerformanceResult {
  stats: PerformanceStats;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  isGood: boolean;
  updateCullingStats: (rendered: number, culled: number) => void;
}

export function usePerformance(): UsePerformanceResult {
  const { gl } = useThree();
  const monitorRef = useRef(new PerformanceMonitor());
  const [stats, setStats] = useState<PerformanceStats>({
    fps: 60,
    frameTime: 16.67,
    drawCalls: 0,
    triangles: 0,
    points: 0,
    memoryUsed: 0,
    objectsRendered: 0,
    objectsCulled: 0
  });

  useFrame(() => {
    monitorRef.current.beginFrame();
  });

  // End frame measurement (runs after render)
  useEffect(() => {
    const interval = setInterval(() => {
      monitorRef.current.endFrame(gl);
      setStats(monitorRef.current.getStats());
    }, 100); // Update stats 10x per second

    return () => clearInterval(interval);
  }, [gl]);

  const updateCullingStats = useCallback((rendered: number, culled: number) => {
    monitorRef.current.updateCullingStats(rendered, culled);
  }, []);

  return {
    stats,
    grade: monitorRef.current.getGrade(),
    isGood: monitorRef.current.isPerformanceGood(),
    updateCullingStats
  };
}

// =============================================================================
// ADAPTIVE QUALITY HOOK
// =============================================================================

interface UseAdaptiveQualityResult {
  quality: number;
  recommendedPointCount: (base: number) => number;
  lodBias: number;
}

export function useAdaptiveQuality(targetFPS: number = 55): UseAdaptiveQualityResult {
  const monitorRef = useRef(new PerformanceMonitor());
  const qualityRef = useRef(new AdaptiveQuality(monitorRef.current, targetFPS));
  const [quality, setQuality] = useState(1.0);

  useFrame((_, delta) => {
    qualityRef.current.update(delta);
    setQuality(qualityRef.current.getQuality());
  });

  const recommendedPointCount = useCallback((base: number) => {
    return qualityRef.current.getRecommendedPointCount(base);
  }, []);

  return {
    quality,
    recommendedPointCount,
    lodBias: qualityRef.current.getLODBias()
  };
}

// =============================================================================
// OPTIMIZED POINT CLOUD HOOK
// =============================================================================

interface PointData {
  position: THREE.Vector3;
  color: THREE.Color;
  size?: number;
}

interface UseOptimizedPointsResult {
  geometry: THREE.BufferGeometry;
  visibleCount: number;
  totalCount: number;
  update: () => void;
}

export function useOptimizedPoints(
  points: PointData[],
  options: {
    frustumCull?: boolean;
    useLOD?: boolean;
    maxPoints?: number;
  } = {}
): UseOptimizedPointsResult {
  const { frustumCull = true, useLOD = true, maxPoints = 100000 } = options;
  const { camera } = useThree();

  const cullerRef = useRef(new FrustumCuller());
  const lodManagerRef = useRef(new LODManager());
  const octreeRef = useRef<Octree<PointData> | null>(null);

  const [visibleCount, setVisibleCount] = useState(points.length);

  // Build octree on mount
  useEffect(() => {
    const octree = createCosmicOctree<PointData>();
    for (const point of points) {
      octree.insert(point);
    }
    octreeRef.current = octree;
  }, [points]);

  // Create geometry
  const geometry = useMemo(() => {
    const geom = new THREE.BufferGeometry();
    const positions = new Float32Array(maxPoints * 3);
    const colors = new Float32Array(maxPoints * 3);
    const sizes = new Float32Array(maxPoints);

    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geom.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    // Mark as dynamic
    (geom.attributes.position as THREE.BufferAttribute).usage = THREE.DynamicDrawUsage;
    (geom.attributes.color as THREE.BufferAttribute).usage = THREE.DynamicDrawUsage;
    (geom.attributes.size as THREE.BufferAttribute).usage = THREE.DynamicDrawUsage;

    return geom;
  }, [maxPoints]);

  // Update visible points each frame
  const update = useCallback(() => {
    if (!octreeRef.current) return;

    cullerRef.current.update(camera);
    lodManagerRef.current.updateCamera(camera);

    // Query octree for visible points
    let visiblePoints: PointData[];
    if (frustumCull) {
      visiblePoints = octreeRef.current.queryFrustum(cullerRef.current.getFrustum());
    } else {
      visiblePoints = points;
    }

    // Update geometry
    const positions = geometry.attributes.position.array as Float32Array;
    const colors = geometry.attributes.color.array as Float32Array;
    const sizes = geometry.attributes.size.array as Float32Array;

    let idx = 0;
    for (const point of visiblePoints) {
      if (idx >= maxPoints) break;

      // Apply LOD
      let size = point.size || 1.0;
      if (useLOD) {
        const lod = lodManagerRef.current.getLODLevel(point.position);
        if (lod === 'CULLED') continue;
        size *= lodManagerRef.current.getPointSize(lod);
      }

      positions[idx * 3] = point.position.x;
      positions[idx * 3 + 1] = point.position.y;
      positions[idx * 3 + 2] = point.position.z;

      colors[idx * 3] = point.color.r;
      colors[idx * 3 + 1] = point.color.g;
      colors[idx * 3 + 2] = point.color.b;

      sizes[idx] = size;
      idx++;
    }

    // Update draw range
    geometry.setDrawRange(0, idx);
    geometry.attributes.position.needsUpdate = true;
    geometry.attributes.color.needsUpdate = true;
    geometry.attributes.size.needsUpdate = true;

    setVisibleCount(idx);
  }, [camera, frustumCull, useLOD, points, geometry, maxPoints]);

  // Update on each frame
  useFrame(() => {
    update();
  });

  return {
    geometry,
    visibleCount,
    totalCount: points.length,
    update
  };
}

// =============================================================================
// SPATIAL QUERY HOOK
// =============================================================================

interface UseSpatialQueryResult<T> {
  queryNearby: (center: THREE.Vector3, radius: number) => T[];
  queryVisible: () => T[];
  insert: (obj: T) => void;
  rebuild: (objects: T[]) => void;
}

export function useSpatialQuery<T extends { position: THREE.Vector3 }>(): UseSpatialQueryResult<T> {
  const { camera } = useThree();
  const octreeRef = useRef<Octree<T>>(createCosmicOctree<T>());
  const cullerRef = useRef(new FrustumCuller());

  useFrame(() => {
    cullerRef.current.update(camera);
  });

  const queryNearby = useCallback((center: THREE.Vector3, radius: number) => {
    return octreeRef.current.querySphere(center, radius);
  }, []);

  const queryVisible = useCallback(() => {
    return octreeRef.current.queryFrustum(cullerRef.current.getFrustum());
  }, []);

  const insert = useCallback((obj: T) => {
    octreeRef.current.insert(obj);
  }, []);

  const rebuild = useCallback((objects: T[]) => {
    octreeRef.current = createCosmicOctree<T>();
    for (const obj of objects) {
      octreeRef.current.insert(obj);
    }
  }, []);

  return {
    queryNearby,
    queryVisible,
    insert,
    rebuild
  };
}

// =============================================================================
// CAMERA SCALE HOOK - Determine appropriate scale for current view
// =============================================================================

export type ScaleLevel = 'SOLAR' | 'STELLAR' | 'GALACTIC' | 'CLUSTER' | 'COSMIC';

interface UseCameraScaleResult {
  scale: ScaleLevel;
  distanceGpc: number;
  shouldRender: (objectScale: ScaleLevel) => boolean;
}

export function useCameraScale(): UseCameraScaleResult {
  const { camera } = useThree();
  const [scale, setScale] = useState<ScaleLevel>('COSMIC');
  const [distanceGpc, setDistanceGpc] = useState(0);

  useFrame(() => {
    const pos = new THREE.Vector3();
    camera.getWorldPosition(pos);
    const dist = pos.length();
    setDistanceGpc(dist);

    // Determine scale based on camera distance from origin
    if (dist < 0.0000001) {
      setScale('SOLAR');        // < 0.1 pc
    } else if (dist < 0.00001) {
      setScale('STELLAR');      // < 10 pc
    } else if (dist < 0.001) {
      setScale('GALACTIC');     // < 1 Mpc
    } else if (dist < 0.5) {
      setScale('CLUSTER');      // < 500 Mpc
    } else {
      setScale('COSMIC');       // > 500 Mpc
    }
  });

  const shouldRender = useCallback((objectScale: ScaleLevel) => {
    const scaleOrder: ScaleLevel[] = ['SOLAR', 'STELLAR', 'GALACTIC', 'CLUSTER', 'COSMIC'];
    const currentIdx = scaleOrder.indexOf(scale);
    const objectIdx = scaleOrder.indexOf(objectScale);

    // Render objects at current scale and one level above/below
    return Math.abs(currentIdx - objectIdx) <= 1;
  }, [scale]);

  return {
    scale,
    distanceGpc,
    shouldRender
  };
}
