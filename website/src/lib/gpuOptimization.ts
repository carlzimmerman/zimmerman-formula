/**
 * =============================================================================
 * GPU OPTIMIZATION SYSTEM - 60 FPS Mandate for T³/Z₂ Digital Twin
 * =============================================================================
 *
 * Performance utilities for rendering millions of objects:
 * - Octree spatial indexing
 * - Frustum culling
 * - Level of Detail (LOD) management
 * - Instance batching
 * - Memory pooling
 *
 * =============================================================================
 */

import * as THREE from 'three';

// =============================================================================
// CONSTANTS
// =============================================================================

export const HALF_BOX = 10.3; // Gpc - fundamental domain half-size
export const L_C_GPC = 20.6;  // Gpc - fundamental domain size

// LOD distance thresholds (in Gpc)
export const LOD_THRESHOLDS = {
  ULTRA: 0.001,    // < 1 Mpc: Full detail
  HIGH: 0.1,       // < 100 Mpc: High detail
  MEDIUM: 1.0,     // < 1 Gpc: Medium detail
  LOW: 5.0,        // < 5 Gpc: Low detail
  MINIMAL: 10.0,   // < 10 Gpc: Minimal detail
  CULLED: Infinity // Beyond: Don't render
};

// =============================================================================
// OCTREE - Spatial Partitioning for O(log n) queries
// =============================================================================

interface OctreeNode<T> {
  bounds: THREE.Box3;
  children: OctreeNode<T>[] | null;
  objects: T[];
  depth: number;
}

export class Octree<T extends { position: THREE.Vector3 }> {
  private root: OctreeNode<T>;
  private maxDepth: number;
  private maxObjectsPerNode: number;

  constructor(
    bounds: THREE.Box3,
    maxDepth: number = 8,
    maxObjectsPerNode: number = 32
  ) {
    this.maxDepth = maxDepth;
    this.maxObjectsPerNode = maxObjectsPerNode;
    this.root = this.createNode(bounds, 0);
  }

  private createNode(bounds: THREE.Box3, depth: number): OctreeNode<T> {
    return {
      bounds,
      children: null,
      objects: [],
      depth
    };
  }

  insert(object: T): void {
    this.insertIntoNode(this.root, object);
  }

  private insertIntoNode(node: OctreeNode<T>, object: T): void {
    // If this node has children, insert into appropriate child
    if (node.children) {
      const childIndex = this.getChildIndex(node, object.position);
      if (childIndex !== -1) {
        this.insertIntoNode(node.children[childIndex], object);
        return;
      }
    }

    // Add to this node
    node.objects.push(object);

    // Split if needed
    if (
      node.objects.length > this.maxObjectsPerNode &&
      node.depth < this.maxDepth &&
      !node.children
    ) {
      this.splitNode(node);
    }
  }

  private splitNode(node: OctreeNode<T>): void {
    const center = new THREE.Vector3();
    node.bounds.getCenter(center);
    const min = node.bounds.min;
    const max = node.bounds.max;

    // Create 8 children
    node.children = [];
    for (let i = 0; i < 8; i++) {
      const childMin = new THREE.Vector3(
        (i & 1) ? center.x : min.x,
        (i & 2) ? center.y : min.y,
        (i & 4) ? center.z : min.z
      );
      const childMax = new THREE.Vector3(
        (i & 1) ? max.x : center.x,
        (i & 2) ? max.y : center.y,
        (i & 4) ? max.z : center.z
      );
      node.children.push(
        this.createNode(new THREE.Box3(childMin, childMax), node.depth + 1)
      );
    }

    // Redistribute objects
    const objects = node.objects;
    node.objects = [];
    for (const obj of objects) {
      const childIndex = this.getChildIndex(node, obj.position);
      if (childIndex !== -1) {
        this.insertIntoNode(node.children[childIndex], obj);
      } else {
        node.objects.push(obj); // Keep at this level if on boundary
      }
    }
  }

  private getChildIndex(node: OctreeNode<T>, position: THREE.Vector3): number {
    const center = new THREE.Vector3();
    node.bounds.getCenter(center);

    let index = 0;
    if (position.x >= center.x) index |= 1;
    if (position.y >= center.y) index |= 2;
    if (position.z >= center.z) index |= 4;

    return index;
  }

  /**
   * Query all objects within the camera frustum
   */
  queryFrustum(frustum: THREE.Frustum): T[] {
    const results: T[] = [];
    this.queryFrustumNode(this.root, frustum, results);
    return results;
  }

  private queryFrustumNode(
    node: OctreeNode<T>,
    frustum: THREE.Frustum,
    results: T[]
  ): void {
    // Check if node bounds intersect frustum
    if (!frustum.intersectsBox(node.bounds)) {
      return; // Entire subtree culled
    }

    // Add objects from this node
    for (const obj of node.objects) {
      if (frustum.containsPoint(obj.position)) {
        results.push(obj);
      }
    }

    // Recurse into children
    if (node.children) {
      for (const child of node.children) {
        this.queryFrustumNode(child, frustum, results);
      }
    }
  }

  /**
   * Query all objects within a sphere (for distance-based LOD)
   */
  querySphere(center: THREE.Vector3, radius: number): T[] {
    const results: T[] = [];
    const sphere = new THREE.Sphere(center, radius);
    this.querySphereNode(this.root, sphere, results);
    return results;
  }

  private querySphereNode(
    node: OctreeNode<T>,
    sphere: THREE.Sphere,
    results: T[]
  ): void {
    if (!sphere.intersectsBox(node.bounds)) {
      return;
    }

    for (const obj of node.objects) {
      if (sphere.containsPoint(obj.position)) {
        results.push(obj);
      }
    }

    if (node.children) {
      for (const child of node.children) {
        this.querySphereNode(child, sphere, results);
      }
    }
  }

  /**
   * Get statistics about the octree
   */
  getStats(): { nodeCount: number; objectCount: number; maxDepth: number } {
    let nodeCount = 0;
    let objectCount = 0;
    let maxDepth = 0;

    const traverse = (node: OctreeNode<T>) => {
      nodeCount++;
      objectCount += node.objects.length;
      maxDepth = Math.max(maxDepth, node.depth);
      if (node.children) {
        node.children.forEach(traverse);
      }
    };

    traverse(this.root);
    return { nodeCount, objectCount, maxDepth };
  }
}

// =============================================================================
// FRUSTUM CULLER - Skip rendering objects outside camera view
// =============================================================================

export class FrustumCuller {
  private frustum: THREE.Frustum;
  private projScreenMatrix: THREE.Matrix4;

  constructor() {
    this.frustum = new THREE.Frustum();
    this.projScreenMatrix = new THREE.Matrix4();
  }

  /**
   * Update frustum from camera
   */
  update(camera: THREE.Camera): void {
    this.projScreenMatrix.multiplyMatrices(
      camera.projectionMatrix,
      camera.matrixWorldInverse
    );
    this.frustum.setFromProjectionMatrix(this.projScreenMatrix);
  }

  /**
   * Check if a point is visible
   */
  isPointVisible(point: THREE.Vector3): boolean {
    return this.frustum.containsPoint(point);
  }

  /**
   * Check if a bounding box is visible
   */
  isBoxVisible(box: THREE.Box3): boolean {
    return this.frustum.intersectsBox(box);
  }

  /**
   * Check if a bounding sphere is visible
   */
  isSphereVisible(sphere: THREE.Sphere): boolean {
    return this.frustum.intersectsSphere(sphere);
  }

  /**
   * Get the frustum for octree queries
   */
  getFrustum(): THREE.Frustum {
    return this.frustum;
  }
}

// =============================================================================
// LOD MANAGER - Level of Detail based on distance
// =============================================================================

export type LODLevel = 'ULTRA' | 'HIGH' | 'MEDIUM' | 'LOW' | 'MINIMAL' | 'CULLED';

export interface LODObject {
  position: THREE.Vector3;
  lodLevel: LODLevel;
  distanceToCamera: number;
}

export class LODManager {
  private cameraPosition: THREE.Vector3;

  constructor() {
    this.cameraPosition = new THREE.Vector3();
  }

  /**
   * Update camera position for LOD calculations
   */
  updateCamera(camera: THREE.Camera): void {
    camera.getWorldPosition(this.cameraPosition);
  }

  /**
   * Get LOD level for a position
   */
  getLODLevel(position: THREE.Vector3): LODLevel {
    const distance = this.cameraPosition.distanceTo(position);
    return this.distanceToLOD(distance);
  }

  /**
   * Convert distance to LOD level
   */
  distanceToLOD(distance: number): LODLevel {
    if (distance < LOD_THRESHOLDS.ULTRA) return 'ULTRA';
    if (distance < LOD_THRESHOLDS.HIGH) return 'HIGH';
    if (distance < LOD_THRESHOLDS.MEDIUM) return 'MEDIUM';
    if (distance < LOD_THRESHOLDS.LOW) return 'LOW';
    if (distance < LOD_THRESHOLDS.MINIMAL) return 'MINIMAL';
    return 'CULLED';
  }

  /**
   * Get point size multiplier for LOD level
   */
  getPointSize(lodLevel: LODLevel): number {
    switch (lodLevel) {
      case 'ULTRA': return 4.0;
      case 'HIGH': return 2.0;
      case 'MEDIUM': return 1.0;
      case 'LOW': return 0.5;
      case 'MINIMAL': return 0.25;
      case 'CULLED': return 0;
    }
  }

  /**
   * Get opacity for LOD level
   */
  getOpacity(lodLevel: LODLevel): number {
    switch (lodLevel) {
      case 'ULTRA': return 1.0;
      case 'HIGH': return 0.9;
      case 'MEDIUM': return 0.7;
      case 'LOW': return 0.5;
      case 'MINIMAL': return 0.3;
      case 'CULLED': return 0;
    }
  }

  /**
   * Batch objects by LOD level for efficient rendering
   */
  batchByLOD<T extends { position: THREE.Vector3 }>(
    objects: T[]
  ): Map<LODLevel, T[]> {
    const batches = new Map<LODLevel, T[]>();

    for (const level of ['ULTRA', 'HIGH', 'MEDIUM', 'LOW', 'MINIMAL'] as LODLevel[]) {
      batches.set(level, []);
    }

    for (const obj of objects) {
      const level = this.getLODLevel(obj.position);
      if (level !== 'CULLED') {
        batches.get(level)!.push(obj);
      }
    }

    return batches;
  }
}

// =============================================================================
// PERFORMANCE MONITOR - Track FPS, memory, draw calls
// =============================================================================

export interface PerformanceStats {
  fps: number;
  frameTime: number;
  drawCalls: number;
  triangles: number;
  points: number;
  memoryUsed: number;
  objectsRendered: number;
  objectsCulled: number;
}

export class PerformanceMonitor {
  private frames: number[] = [];
  private lastTime: number = 0;
  private stats: PerformanceStats;

  constructor() {
    this.stats = {
      fps: 60,
      frameTime: 16.67,
      drawCalls: 0,
      triangles: 0,
      points: 0,
      memoryUsed: 0,
      objectsRendered: 0,
      objectsCulled: 0
    };
  }

  /**
   * Call at start of each frame
   */
  beginFrame(): void {
    this.lastTime = performance.now();
  }

  /**
   * Call at end of each frame
   */
  endFrame(renderer?: THREE.WebGLRenderer): void {
    const now = performance.now();
    const frameTime = now - this.lastTime;

    this.frames.push(frameTime);
    if (this.frames.length > 60) {
      this.frames.shift();
    }

    const avgFrameTime = this.frames.reduce((a, b) => a + b, 0) / this.frames.length;
    this.stats.fps = Math.round(1000 / avgFrameTime);
    this.stats.frameTime = Math.round(avgFrameTime * 100) / 100;

    if (renderer) {
      const info = renderer.info;
      this.stats.drawCalls = info.render.calls;
      this.stats.triangles = info.render.triangles;
      this.stats.points = info.render.points;
      this.stats.memoryUsed = info.memory.geometries + info.memory.textures;
    }
  }

  /**
   * Update culling stats
   */
  updateCullingStats(rendered: number, culled: number): void {
    this.stats.objectsRendered = rendered;
    this.stats.objectsCulled = culled;
  }

  /**
   * Get current stats
   */
  getStats(): PerformanceStats {
    return { ...this.stats };
  }

  /**
   * Check if performance is acceptable
   */
  isPerformanceGood(): boolean {
    return this.stats.fps >= 30;
  }

  /**
   * Get performance grade
   */
  getGrade(): 'A' | 'B' | 'C' | 'D' | 'F' {
    if (this.stats.fps >= 55) return 'A';
    if (this.stats.fps >= 45) return 'B';
    if (this.stats.fps >= 30) return 'C';
    if (this.stats.fps >= 20) return 'D';
    return 'F';
  }
}

// =============================================================================
// INSTANCED BUFFER MANAGER - Efficient batch updates
// =============================================================================

export class InstancedBufferManager {
  private instancedMesh: THREE.InstancedMesh | null = null;
  private tempMatrix: THREE.Matrix4;
  private tempColor: THREE.Color;

  constructor() {
    this.tempMatrix = new THREE.Matrix4();
    this.tempColor = new THREE.Color();
  }

  /**
   * Create an instanced mesh for many identical objects
   */
  createInstancedMesh(
    geometry: THREE.BufferGeometry,
    material: THREE.Material,
    count: number
  ): THREE.InstancedMesh {
    this.instancedMesh = new THREE.InstancedMesh(geometry, material, count);
    this.instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    return this.instancedMesh;
  }

  /**
   * Update instance at index
   */
  updateInstance(
    index: number,
    position: THREE.Vector3,
    scale: number = 1,
    rotation?: THREE.Euler
  ): void {
    if (!this.instancedMesh) return;

    this.tempMatrix.makeScale(scale, scale, scale);
    if (rotation) {
      this.tempMatrix.makeRotationFromEuler(rotation);
    }
    this.tempMatrix.setPosition(position);

    this.instancedMesh.setMatrixAt(index, this.tempMatrix);
  }

  /**
   * Mark instance matrix as needing update
   */
  needsUpdate(): void {
    if (this.instancedMesh) {
      this.instancedMesh.instanceMatrix.needsUpdate = true;
    }
  }

  /**
   * Set instance color (if material supports it)
   */
  setInstanceColor(index: number, color: THREE.Color | string): void {
    if (!this.instancedMesh) return;

    if (typeof color === 'string') {
      this.tempColor.set(color);
    } else {
      this.tempColor.copy(color);
    }

    this.instancedMesh.setColorAt(index, this.tempColor);
    if (this.instancedMesh.instanceColor) {
      this.instancedMesh.instanceColor.needsUpdate = true;
    }
  }
}

// =============================================================================
// GEOMETRY POOL - Reuse geometries to reduce GC pressure
// =============================================================================

export class GeometryPool {
  private sphereGeometries: Map<string, THREE.SphereGeometry> = new Map();
  private boxGeometries: Map<string, THREE.BoxGeometry> = new Map();

  /**
   * Get or create a sphere geometry
   */
  getSphere(radius: number, segments: number = 16): THREE.SphereGeometry {
    const key = `${radius}-${segments}`;
    let geom = this.sphereGeometries.get(key);
    if (!geom) {
      geom = new THREE.SphereGeometry(radius, segments, segments);
      this.sphereGeometries.set(key, geom);
    }
    return geom;
  }

  /**
   * Get or create a box geometry
   */
  getBox(width: number, height: number, depth: number): THREE.BoxGeometry {
    const key = `${width}-${height}-${depth}`;
    let geom = this.boxGeometries.get(key);
    if (!geom) {
      geom = new THREE.BoxGeometry(width, height, depth);
      this.boxGeometries.set(key, geom);
    }
    return geom;
  }

  /**
   * Clear all pooled geometries
   */
  dispose(): void {
    this.sphereGeometries.forEach((g) => g.dispose());
    this.boxGeometries.forEach((g) => g.dispose());
    this.sphereGeometries.clear();
    this.boxGeometries.clear();
  }
}

// =============================================================================
// ADAPTIVE QUALITY - Auto-adjust based on performance
// =============================================================================

export class AdaptiveQuality {
  private targetFPS: number;
  private currentQuality: number; // 0-1
  private performanceMonitor: PerformanceMonitor;
  private adjustmentCooldown: number = 0;

  constructor(performanceMonitor: PerformanceMonitor, targetFPS: number = 55) {
    this.performanceMonitor = performanceMonitor;
    this.targetFPS = targetFPS;
    this.currentQuality = 1.0;
  }

  /**
   * Update quality based on current performance
   */
  update(deltaTime: number): void {
    this.adjustmentCooldown -= deltaTime;
    if (this.adjustmentCooldown > 0) return;

    const stats = this.performanceMonitor.getStats();

    if (stats.fps < this.targetFPS * 0.8) {
      // Performance too low, reduce quality
      this.currentQuality = Math.max(0.1, this.currentQuality - 0.1);
      this.adjustmentCooldown = 1.0; // Wait 1 second before next adjustment
    } else if (stats.fps > this.targetFPS && this.currentQuality < 1.0) {
      // Performance good, try increasing quality
      this.currentQuality = Math.min(1.0, this.currentQuality + 0.05);
      this.adjustmentCooldown = 2.0; // Wait longer when increasing
    }
  }

  /**
   * Get current quality level (0-1)
   */
  getQuality(): number {
    return this.currentQuality;
  }

  /**
   * Get recommended point count based on quality
   */
  getRecommendedPointCount(baseCount: number): number {
    return Math.floor(baseCount * this.currentQuality);
  }

  /**
   * Get recommended LOD bias
   */
  getLODBias(): number {
    // Lower quality = more aggressive culling (higher bias)
    return 1.0 + (1.0 - this.currentQuality) * 2.0;
  }
}

// =============================================================================
// EXPORT SINGLETON INSTANCES
// =============================================================================

export const frustumCuller = new FrustumCuller();
export const lodManager = new LODManager();
export const performanceMonitor = new PerformanceMonitor();
export const geometryPool = new GeometryPool();

// Create default octree for the fundamental domain
export function createCosmicOctree<T extends { position: THREE.Vector3 }>(): Octree<T> {
  const bounds = new THREE.Box3(
    new THREE.Vector3(-HALF_BOX, -HALF_BOX, -HALF_BOX),
    new THREE.Vector3(HALF_BOX, HALF_BOX, HALF_BOX)
  );
  return new Octree<T>(bounds, 8, 64);
}
