/**
 * =============================================================================
 * LODManager.ts - LEVEL OF DETAIL SYSTEM
 * =============================================================================
 *
 * Work-Order III: True LOD and UI Marker Swapping
 *
 * KEY PRINCIPLE: Stop trying to inflate planets!
 * - When camera is far: UNMOUNT 3D geometry entirely, show CSS labels
 * - When camera is close: UNMOUNT labels, show true-scale 3D geometry
 * - Crossfade during transitions
 *
 * DIRECTIVE LLL COMPLIANCE:
 * - DOM labels aggregate for performance
 * - WebGL point clouds (empirical data) NEVER get culled
 * - User always sees raw data behind aggregated labels
 *
 * Z² Framework v11.1.0
 * Work-Order HHH: Float64 Camera-Relative Engine
 * =============================================================================
 */

import { LOD_THRESHOLDS, type LODLevel, AU, KPC, MPC, GPC } from './CosmicConstants';

// =============================================================================
// LOD OBJECT TYPES
// =============================================================================

export type CosmicObjectType =
  | 'planet'
  | 'star'
  | 'galaxy'
  | 'cluster'
  | 'supercluster'
  | 'void'
  | 'z2_vertex'
  | 'z2_domain'
  | 'empirical_point'; // DESI, SDSS, etc. - NEVER culled

// =============================================================================
// RENDER MODE ENUM
// =============================================================================

export enum RenderMode {
  GEOMETRY_3D = 'GEOMETRY_3D',    // Full 3D mesh/geometry
  BILLBOARD = 'BILLBOARD',         // Camera-facing sprite
  POINT = 'POINT',                 // Single GL point
  LABEL_ONLY = 'LABEL_ONLY',       // CSS/HTML label, no geometry
  HIDDEN = 'HIDDEN',               // Not rendered at all
}

// =============================================================================
// LOD CONFIGURATION PER OBJECT TYPE
// =============================================================================

interface LODConfig {
  // At what camera distance (km) do we transition between modes?
  geometry3D_maxDistance: number;
  billboard_maxDistance: number;
  point_maxDistance: number;
  label_minDistance: number;

  // Size thresholds
  minVisibleSize_pixels: number;

  // Priority for label decluttering (higher = more important)
  labelPriority: number;
}

export const LOD_CONFIGS: Record<CosmicObjectType, LODConfig> = {
  planet: {
    geometry3D_maxDistance: 100 * AU,          // 3D within 100 AU
    billboard_maxDistance: 1000 * AU,          // Billboard to 1000 AU
    point_maxDistance: 1 * KPC,                // Point to 1 kpc
    label_minDistance: 0,                      // Always show label when visible
    minVisibleSize_pixels: 2,
    labelPriority: 100,
  },

  star: {
    geometry3D_maxDistance: 100 * AU,          // Sun only gets 3D within 100 AU
    billboard_maxDistance: 100 * KPC,          // Billboard across MW
    point_maxDistance: 10 * MPC,               // Point in local group
    label_minDistance: 0,
    minVisibleSize_pixels: 1,
    labelPriority: 80,
  },

  galaxy: {
    geometry3D_maxDistance: 10 * MPC,          // 3D spiral within 10 Mpc
    billboard_maxDistance: 500 * MPC,          // Billboard in cosmic web
    point_maxDistance: 5 * GPC,                // Point at cosmic scale
    label_minDistance: 100 * KPC,              // No label when inside galaxy
    minVisibleSize_pixels: 1,
    labelPriority: 50,
  },

  cluster: {
    geometry3D_maxDistance: 500 * MPC,         // 3D cluster structure
    billboard_maxDistance: 5 * GPC,            // Billboard at cosmic scale
    point_maxDistance: 20 * GPC,               // Point at domain edge
    label_minDistance: 10 * MPC,
    minVisibleSize_pixels: 3,
    labelPriority: 300,
  },

  supercluster: {
    geometry3D_maxDistance: 2 * GPC,
    billboard_maxDistance: 10 * GPC,
    point_maxDistance: 30 * GPC,
    label_minDistance: 100 * MPC,
    minVisibleSize_pixels: 5,
    labelPriority: 500,
  },

  void: {
    geometry3D_maxDistance: 5 * GPC,           // Wireframe sphere
    billboard_maxDistance: 20 * GPC,
    point_maxDistance: 30 * GPC,
    label_minDistance: 100 * MPC,
    minVisibleSize_pixels: 10,
    labelPriority: 400,
  },

  z2_vertex: {
    geometry3D_maxDistance: 30 * GPC,          // ALWAYS render as geometry
    billboard_maxDistance: 30 * GPC,
    point_maxDistance: 30 * GPC,
    label_minDistance: 0,
    minVisibleSize_pixels: 10,
    labelPriority: 1000,                       // Highest priority - always visible
  },

  z2_domain: {
    geometry3D_maxDistance: 30 * GPC,          // ALWAYS render wireframe box
    billboard_maxDistance: 30 * GPC,
    point_maxDistance: 30 * GPC,
    label_minDistance: 1 * GPC,
    minVisibleSize_pixels: 1,
    labelPriority: 900,
  },

  empirical_point: {
    // DIRECTIVE LLL: Empirical data NEVER gets culled
    geometry3D_maxDistance: Infinity,
    billboard_maxDistance: Infinity,
    point_maxDistance: Infinity,
    label_minDistance: Infinity,               // Never show individual labels
    minVisibleSize_pixels: 0.5,
    labelPriority: 0,                          // No labels for individual data points
  },
};

// =============================================================================
// LOD MANAGER CLASS
// =============================================================================

export class LODManager {
  /**
   * Determine how to render an object based on camera distance.
   */
  static getRenderMode(
    objectType: CosmicObjectType,
    distanceFromCamera_km: number,
    objectSize_km: number,
    screenPixels?: number
  ): RenderMode {
    const config = LOD_CONFIGS[objectType];

    // Empirical data points: always render as points (Directive LLL)
    if (objectType === 'empirical_point') {
      return RenderMode.POINT;
    }

    // Z² framework elements: always render as geometry
    if (objectType === 'z2_vertex' || objectType === 'z2_domain') {
      return RenderMode.GEOMETRY_3D;
    }

    // Check screen size threshold
    if (screenPixels !== undefined && screenPixels < config.minVisibleSize_pixels) {
      // Too small to see - demote to point or hide
      if (distanceFromCamera_km < config.point_maxDistance) {
        return RenderMode.POINT;
      }
      return RenderMode.HIDDEN;
    }

    // Distance-based LOD
    if (distanceFromCamera_km < config.geometry3D_maxDistance) {
      return RenderMode.GEOMETRY_3D;
    }

    if (distanceFromCamera_km < config.billboard_maxDistance) {
      return RenderMode.BILLBOARD;
    }

    if (distanceFromCamera_km < config.point_maxDistance) {
      return RenderMode.POINT;
    }

    return RenderMode.HIDDEN;
  }

  /**
   * Should we show a label for this object?
   */
  static shouldShowLabel(
    objectType: CosmicObjectType,
    distanceFromCamera_km: number
  ): boolean {
    const config = LOD_CONFIGS[objectType];

    // Empirical points never get individual labels (Directive LLL)
    if (objectType === 'empirical_point') {
      return false;
    }

    // Too close (e.g., inside a galaxy)
    if (distanceFromCamera_km < config.label_minDistance) {
      return false;
    }

    // Z² vertices always show labels
    if (objectType === 'z2_vertex') {
      return true;
    }

    // Beyond visible range
    if (distanceFromCamera_km > config.point_maxDistance) {
      return false;
    }

    return true;
  }

  /**
   * Get label priority for decluttering.
   * Higher priority = more likely to be shown when labels overlap.
   */
  static getLabelPriority(
    objectType: CosmicObjectType,
    objectName?: string
  ): number {
    const config = LOD_CONFIGS[objectType];
    let priority = config.labelPriority;

    // Boost priority for named/important objects
    if (objectName) {
      const upperName = objectName.toUpperCase();

      // Z² framework objects
      if (upperName.includes('SHAPLEY')) priority += 200;
      if (upperName.includes('CMB') || upperName.includes('COLD SPOT')) priority += 200;
      if (upperName.includes('ANTI-')) priority += 100;

      // Solar system
      if (upperName === 'SUN') priority += 500;
      if (upperName === 'EARTH') priority += 400;

      // Major structures
      if (upperName.includes('ANDROMEDA') || upperName === 'M31') priority += 150;
      if (upperName.includes('MILKY WAY')) priority += 300;
      if (upperName.includes('LANIAKEA')) priority += 150;
      if (upperName.includes('VIRGO')) priority += 100;
      if (upperName.includes('COMA')) priority += 100;
    }

    return priority;
  }

  /**
   * Calculate opacity for smooth transitions between LOD levels.
   * Returns 0-1 opacity to crossfade between geometry and labels.
   */
  static getTransitionOpacity(
    objectType: CosmicObjectType,
    distanceFromCamera_km: number,
    targetMode: RenderMode
  ): number {
    const config = LOD_CONFIGS[objectType];

    // Define transition zones (10% of threshold)
    const transitionWidth = 0.1;

    if (targetMode === RenderMode.GEOMETRY_3D) {
      const threshold = config.geometry3D_maxDistance;
      const fadeStart = threshold * (1 - transitionWidth);

      if (distanceFromCamera_km < fadeStart) return 1;
      if (distanceFromCamera_km > threshold) return 0;

      return 1 - (distanceFromCamera_km - fadeStart) / (threshold - fadeStart);
    }

    if (targetMode === RenderMode.BILLBOARD) {
      const thresholdIn = config.geometry3D_maxDistance;
      const thresholdOut = config.billboard_maxDistance;

      // Fade in from geometry threshold
      if (distanceFromCamera_km < thresholdIn) return 0;
      const fadeInEnd = thresholdIn * (1 + transitionWidth);
      if (distanceFromCamera_km < fadeInEnd) {
        return (distanceFromCamera_km - thresholdIn) / (fadeInEnd - thresholdIn);
      }

      // Fade out to point threshold
      const fadeOutStart = thresholdOut * (1 - transitionWidth);
      if (distanceFromCamera_km < fadeOutStart) return 1;
      if (distanceFromCamera_km > thresholdOut) return 0;

      return 1 - (distanceFromCamera_km - fadeOutStart) / (thresholdOut - fadeOutStart);
    }

    if (targetMode === RenderMode.LABEL_ONLY) {
      // Labels fade in as geometry fades out
      const threshold = config.geometry3D_maxDistance;
      const fadeStart = threshold * (1 - transitionWidth);

      if (distanceFromCamera_km < fadeStart) return 0;
      if (distanceFromCamera_km > threshold) return 1;

      return (distanceFromCamera_km - fadeStart) / (threshold - fadeStart);
    }

    return 1;
  }
}

// =============================================================================
// AGGREGATION HELPERS (Directive LLL)
// =============================================================================

export interface AggregatedLabel {
  name: string;
  position_km: [number, number, number];
  childCount: number;
  dominantType: CosmicObjectType;
  priority: number;
}

/**
 * Aggregate nearby labels into cluster labels.
 * Only affects DOM labels - WebGL points remain fully rendered.
 */
export function aggregateLabels(
  labels: Array<{
    name: string;
    position_km: [number, number, number];
    type: CosmicObjectType;
    priority: number;
  }>,
  aggregationRadius_km: number,
  lodLevel: LODLevel
): AggregatedLabel[] {
  // At planetary/stellar scale, don't aggregate
  if (lodLevel === 'PLANETARY' || lodLevel === 'STELLAR') {
    return labels.map(l => ({
      name: l.name,
      position_km: l.position_km,
      childCount: 1,
      dominantType: l.type,
      priority: l.priority,
    }));
  }

  // Simple grid-based clustering
  const cellSize = aggregationRadius_km;
  const clusters = new Map<string, AggregatedLabel>();

  for (const label of labels) {
    const cellX = Math.floor(label.position_km[0] / cellSize);
    const cellY = Math.floor(label.position_km[1] / cellSize);
    const cellZ = Math.floor(label.position_km[2] / cellSize);
    const cellKey = `${cellX},${cellY},${cellZ}`;

    const existing = clusters.get(cellKey);
    if (existing) {
      existing.childCount++;
      // Keep highest priority name
      if (label.priority > existing.priority) {
        existing.name = label.name;
        existing.priority = label.priority;
        existing.dominantType = label.type;
      }
      // Update centroid (running average)
      const n = existing.childCount;
      existing.position_km[0] = existing.position_km[0] * (n-1)/n + label.position_km[0]/n;
      existing.position_km[1] = existing.position_km[1] * (n-1)/n + label.position_km[1]/n;
      existing.position_km[2] = existing.position_km[2] * (n-1)/n + label.position_km[2]/n;
    } else {
      clusters.set(cellKey, {
        name: label.name,
        position_km: [...label.position_km],
        childCount: 1,
        dominantType: label.type,
        priority: label.priority,
      });
    }
  }

  return Array.from(clusters.values());
}

// =============================================================================
// EXPORT
// =============================================================================

export default LODManager;
