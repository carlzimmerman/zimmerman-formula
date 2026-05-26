/**
 * =============================================================================
 * PERFORMANCE HUD - Real-time GPU/Rendering Statistics
 * =============================================================================
 *
 * Displays:
 * - FPS counter with color-coded grade
 * - Draw calls and triangle count
 * - Objects rendered vs culled
 * - Memory usage
 * - Camera scale/position
 *
 * =============================================================================
 */

'use client';

import React, { useState, useEffect } from 'react';
import { usePerformance, useCameraScale, useLOD } from '@/hooks/useGPUOptimization';

interface PerformanceHUDProps {
  visible?: boolean;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  compact?: boolean;
}

// Wrapper component that provides Three.js context
export function PerformanceHUDCanvas(props: PerformanceHUDProps) {
  // This component must be used INSIDE a Canvas
  return <PerformanceHUDInner {...props} />;
}

function PerformanceHUDInner({
  visible = true,
  position = 'top-right',
  compact = false
}: PerformanceHUDProps) {
  const { stats, grade, isGood } = usePerformance();
  const { scale, distanceGpc } = useCameraScale();
  const { cameraDistance } = useLOD();

  if (!visible) return null;

  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  const gradeColors = {
    'A': 'text-green-400',
    'B': 'text-lime-400',
    'C': 'text-yellow-400',
    'D': 'text-orange-400',
    'F': 'text-red-400'
  };

  const fpsColor = stats.fps >= 55 ? 'text-green-400' :
                   stats.fps >= 30 ? 'text-yellow-400' :
                   'text-red-400';

  if (compact) {
    return (
      <div className={`absolute ${positionClasses[position]} z-50`}>
        <div className="bg-black/70 px-2 py-1 rounded text-xs font-mono flex items-center gap-2">
          <span className={fpsColor}>{stats.fps} FPS</span>
          <span className={gradeColors[grade]}>[{grade}]</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`absolute ${positionClasses[position]} z-50`}>
      <div className="bg-black/80 border border-gray-700 rounded-lg p-3 backdrop-blur-sm min-w-[200px]">
        {/* Header */}
        <div className="flex items-center justify-between mb-2 pb-2 border-b border-gray-700">
          <span className="text-gray-400 text-xs font-bold">PERFORMANCE</span>
          <span className={`${gradeColors[grade]} text-lg font-bold`}>{grade}</span>
        </div>

        {/* FPS */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">FPS:</span>
          <span className={`${fpsColor} font-mono font-bold`}>
            {stats.fps}
            <span className="text-gray-600 ml-1 text-[10px]">
              ({stats.frameTime.toFixed(1)}ms)
            </span>
          </span>
        </div>

        {/* Draw Calls */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Draw Calls:</span>
          <span className="text-cyan-400 font-mono text-sm">{stats.drawCalls}</span>
        </div>

        {/* Triangles */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Triangles:</span>
          <span className="text-blue-400 font-mono text-sm">
            {formatNumber(stats.triangles)}
          </span>
        </div>

        {/* Points */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Points:</span>
          <span className="text-purple-400 font-mono text-sm">
            {formatNumber(stats.points)}
          </span>
        </div>

        {/* Culling Stats */}
        {(stats.objectsRendered > 0 || stats.objectsCulled > 0) && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500 text-xs">Culled:</span>
            <span className="text-orange-400 font-mono text-sm">
              {stats.objectsCulled} / {stats.objectsRendered + stats.objectsCulled}
            </span>
          </div>
        )}

        {/* Divider */}
        <div className="border-t border-gray-700 my-2" />

        {/* Camera Info */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Scale:</span>
          <span className="text-white font-mono text-sm">{scale}</span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-gray-500 text-xs">Distance:</span>
          <span className="text-gray-300 font-mono text-sm">
            {formatDistance(distanceGpc)}
          </span>
        </div>

        {/* Warning if performance is bad */}
        {!isGood && (
          <div className="mt-2 pt-2 border-t border-red-900">
            <div className="text-red-400 text-[10px] flex items-center gap-1">
              <span className="animate-pulse">!</span>
              <span>Low FPS - Quality reduced</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// =============================================================================
// HTML VERSION (for use outside Canvas)
// =============================================================================

interface PerformanceHUDHTMLProps {
  visible?: boolean;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  stats?: {
    fps: number;
    drawCalls: number;
    triangles: number;
    points: number;
    objectsRendered: number;
    objectsCulled: number;
  };
  scale?: string;
  distanceGpc?: number;
}

export function PerformanceHUDHTML({
  visible = true,
  position = 'top-right',
  stats = { fps: 60, drawCalls: 0, triangles: 0, points: 0, objectsRendered: 0, objectsCulled: 0 },
  scale = 'COSMIC',
  distanceGpc = 0
}: PerformanceHUDHTMLProps) {
  if (!visible) return null;

  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  const getGrade = (fps: number): string => {
    if (fps >= 55) return 'A';
    if (fps >= 45) return 'B';
    if (fps >= 30) return 'C';
    if (fps >= 20) return 'D';
    return 'F';
  };

  const grade = getGrade(stats.fps);

  const gradeColors: Record<string, string> = {
    'A': 'text-green-400',
    'B': 'text-lime-400',
    'C': 'text-yellow-400',
    'D': 'text-orange-400',
    'F': 'text-red-400'
  };

  const fpsColor = stats.fps >= 55 ? 'text-green-400' :
                   stats.fps >= 30 ? 'text-yellow-400' :
                   'text-red-400';

  return (
    <div className={`absolute ${positionClasses[position]} z-50`}>
      <div className="bg-black/80 border border-gray-700 rounded-lg p-3 backdrop-blur-sm min-w-[200px]">
        {/* Header */}
        <div className="flex items-center justify-between mb-2 pb-2 border-b border-gray-700">
          <span className="text-gray-400 text-xs font-bold">PERFORMANCE</span>
          <span className={`${gradeColors[grade]} text-lg font-bold`}>{grade}</span>
        </div>

        {/* FPS */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">FPS:</span>
          <span className={`${fpsColor} font-mono font-bold`}>{stats.fps}</span>
        </div>

        {/* Draw Calls */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Draw Calls:</span>
          <span className="text-cyan-400 font-mono text-sm">{stats.drawCalls}</span>
        </div>

        {/* Points */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Points:</span>
          <span className="text-purple-400 font-mono text-sm">
            {formatNumber(stats.points)}
          </span>
        </div>

        {/* Culling */}
        {stats.objectsCulled > 0 && (
          <div className="flex justify-between items-center mb-1">
            <span className="text-gray-500 text-xs">Culled:</span>
            <span className="text-orange-400 font-mono text-sm">
              {Math.round((stats.objectsCulled / (stats.objectsRendered + stats.objectsCulled)) * 100)}%
            </span>
          </div>
        )}

        {/* Divider */}
        <div className="border-t border-gray-700 my-2" />

        {/* Scale */}
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-500 text-xs">Scale:</span>
          <span className="text-white font-mono text-sm">{scale}</span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-gray-500 text-xs">Distance:</span>
          <span className="text-gray-300 font-mono text-sm">
            {formatDistance(distanceGpc)}
          </span>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// HELPERS
// =============================================================================

function formatNumber(n: number): string {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
  return n.toString();
}

function formatDistance(gpc: number): string {
  if (gpc < 0.000001) {
    // Show in AU
    const au = gpc * 206264806; // Gpc to AU
    return au.toFixed(1) + ' AU';
  }
  if (gpc < 0.001) {
    // Show in Mpc
    return (gpc * 1000).toFixed(2) + ' Mpc';
  }
  return gpc.toFixed(3) + ' Gpc';
}

// =============================================================================
// MINIMAL FPS TEXT - Bottom right footer style
// =============================================================================

interface MinimalFPSProps {
  fps: number;
  visible?: boolean;
}

export function MinimalFPS({ fps, visible = true }: MinimalFPSProps) {
  if (!visible) return null;

  const color = fps >= 55 ? 'text-green-500' :
                fps >= 30 ? 'text-yellow-500' :
                'text-red-500';

  return (
    <div className="fixed bottom-2 right-4 z-50">
      <span className={`${color} font-mono text-xs opacity-60 hover:opacity-100 transition-opacity`}>
        {fps} FPS
      </span>
    </div>
  );
}

export default PerformanceHUDHTML;
