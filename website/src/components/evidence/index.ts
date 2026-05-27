/**
 * =============================================================================
 * EVIDENCE LAYER COMPONENTS
 * =============================================================================
 *
 * Three independent evidence layers demonstrating T³/Z₂ topology:
 *
 * 1. CMBParitySphere (QQQQ) - Z₂ parity asymmetry visualization
 * 2. IsotropyBreaker (RRRR) - "Axis of Evil" alignment
 * 3. KinematicFlowMap (SSSS) - Dark Flow toward boundary
 *
 * Each layer provides both a 3D visualization component and a 2D HUD overlay.
 *
 * =============================================================================
 */

// Original evidence layers (QQQQ, RRRR, SSSS)
export { CMBParitySphere, ParityEvidenceHUD } from './CMBParitySphere';
export { IsotropyBreaker, IsotropyBreakerHUD } from './IsotropyBreaker';
export { KinematicFlowMap, DarkFlowHUD } from './KinematicFlowMap';

// Multi-messenger layers (TTTT, UUUU, VVVV)
export { GravitationalGraveyard, GraveyardHUD } from './GravitationalGraveyard';
export { GeometricGravity, MONDHUD } from './GeometricGravity';
export { RadioMirrors, RadioGhostHUD } from './RadioMirrors';

// Frontier layers (WWWW, XXXX, YYYY)
export { LocalMONDAnchor, WideBinaryHUD } from './LocalMONDAnchor';
export { DispersionTomography, DispersionHUD } from './DispersionTomography';
export { CosmicWindShader, CosmicWindHUD } from './CosmicWindShader';
