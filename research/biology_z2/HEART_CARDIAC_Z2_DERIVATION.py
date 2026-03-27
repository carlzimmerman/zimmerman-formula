#!/usr/bin/env python3
"""
THE HEART: Z² GEOMETRY OF THE BIOLOGICAL PUMP
==============================================

The heart is a remarkable Z² machine - a pump that beats ~3 billion times
in a lifetime, maintaining the circulation that sustains all tissues.

Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3
Bekenstein = 3Z²/(8π) = 4
Gauge = 9Z²/(8π) = 12

Author: Carl Zimmerman
Date: 2026
"""

import numpy as np

# =============================================================================
# ZIMMERMAN CONSTANTS
# =============================================================================

CUBE = 8
SPHERE = 4 * np.pi / 3
Z_SQUARED = CUBE * SPHERE
Z = np.sqrt(Z_SQUARED)
BEKENSTEIN = 3 * Z_SQUARED / (8 * np.pi)  # = 4
GAUGE = 9 * Z_SQUARED / (8 * np.pi)       # = 12

print("=" * 70)
print("THE HEART: Z² BIOLOGICAL PUMP")
print("=" * 70)

# =============================================================================
# PART 1: CARDIAC ANATOMY - Z² CHAMBERS
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: CARDIAC ANATOMY - Z² STRUCTURE")
print("=" * 70)

print(f"""
THE FOUR-CHAMBERED HEART:

  The heart has 4 chambers = Bekenstein!

  1. RIGHT ATRIUM
     - Receives deoxygenated blood from body
     - Via superior and inferior vena cava

  2. RIGHT VENTRICLE
     - Pumps to lungs (pulmonary circulation)
     - Lower pressure pump

  3. LEFT ATRIUM
     - Receives oxygenated blood from lungs
     - Via pulmonary veins

  4. LEFT VENTRICLE
     - Pumps to body (systemic circulation)
     - High pressure pump, thickest wall

  4 chambers = Bekenstein EXACT!

TWO CIRCULATIONS (factor of 2 in Z):

  PULMONARY CIRCULATION:
    - Right heart → Lungs → Left heart
    - Oxygenation

  SYSTEMIC CIRCULATION:
    - Left heart → Body → Right heart
    - Oxygen delivery

  2 circuits = factor of 2 in Z = 2√(8π/3)

THE FOUR VALVES (Bekenstein!):

  1. TRICUSPID (right AV valve)
     - 3 leaflets = SPHERE coefficient

  2. MITRAL (left AV valve)
     - 2 leaflets = factor of 2

  3. PULMONARY (right outflow)
     - 3 cusps = SPHERE coefficient

  4. AORTIC (left outflow)
     - 3 cusps = SPHERE coefficient

  4 valves = Bekenstein!
  Most valves have 3 parts = SPHERE coefficient

CARDIAC WALL LAYERS:

  1. Endocardium (inner lining)
  2. Myocardium (muscle)
  3. Epicardium (outer layer)
  4. Pericardium (surrounding sac)

  4 layers = Bekenstein!
""")

# =============================================================================
# PART 2: THE CARDIAC CYCLE - Z² RHYTHM
# =============================================================================

print("=" * 70)
print("PART 2: THE CARDIAC CYCLE - Z² PUMP ACTION")
print("=" * 70)

print(f"""
THE CARDIAC CYCLE:

  One complete heartbeat.
  ~0.8 seconds at rest (75 bpm).

TWO PHASES (factor of 2 in Z):

  SYSTOLE: Contraction
    - Atrial systole: Atria contract
    - Ventricular systole: Ventricles contract

  DIASTOLE: Relaxation
    - Ventricles fill
    - Heart "recharges"

  2 main phases = factor of 2 in Z

DETAILED PHASES (Bekenstein = 4?):

  1. ATRIAL SYSTOLE
     - Atria contract
     - "Atrial kick" adds ~20% to filling

  2. ISOVOLUMETRIC CONTRACTION
     - All valves closed
     - Pressure builds

  3. VENTRICULAR EJECTION
     - Semilunar valves open
     - Blood ejected

  4. ISOVOLUMETRIC RELAXATION
     - All valves closed
     - Pressure drops

  4 main phases = Bekenstein!

TIMING:

  Systole: ~0.3 s
  Diastole: ~0.5 s
  Ratio: 3:5 ≈ 0.6

  At higher heart rates, diastole shortens more.
  This limits filling time.

HEART SOUNDS:

  S1 ("lub"): AV valves close (start of systole)
  S2 ("dub"): Semilunar valves close (end of systole)

  2 normal heart sounds = factor of 2 in Z

  S3, S4 can be heard in some conditions.
  Total: up to 4 sounds = Bekenstein!
""")

# =============================================================================
# PART 3: ELECTRICAL CONDUCTION - Z² SIGNALING
# =============================================================================

print("=" * 70)
print("PART 3: ELECTRICAL CONDUCTION - Z² ACTIVATION")
print("=" * 70)

print(f"""
THE CONDUCTION SYSTEM:

  The heart generates its own rhythm!
  Specialized cells conduct electrical signals.

CONDUCTION PATHWAY:

  1. SA NODE (Sinoatrial)
     - "Pacemaker" of the heart
     - Fires ~60-100 bpm at rest
     - Sets the rhythm

  2. AV NODE (Atrioventricular)
     - Delays signal ~0.1 s
     - Allows atria to finish contracting
     - Only electrical connection atria→ventricles

  3. BUNDLE OF HIS
     - Fast conduction to ventricles
     - Splits into left and right bundle branches

  4. PURKINJE FIBERS
     - Rapid spread through ventricular walls
     - Synchronizes ventricular contraction

  4 main components = Bekenstein!

PACEMAKER HIERARCHY:

  SA node: 60-100 bpm (primary)
  AV node: 40-60 bpm (backup)
  Ventricles: 20-40 bpm (emergency)

  3 levels = SPHERE coefficient

THE ACTION POTENTIAL:

  Cardiac muscle action potential is LONG (~300 ms).
  This prevents re-excitation (tetanic contraction).

  Phases:
    0: Rapid depolarization (Na⁺ in)
    1: Brief repolarization
    2: Plateau (Ca²⁺ in, K⁺ out balance)
    3: Repolarization (K⁺ out)
    4: Resting potential

  5 phases ≈ Z (approximately)

THE ECG:

  Electrocardiogram records electrical activity.

  Waves:
    P wave: Atrial depolarization
    QRS complex: Ventricular depolarization
    T wave: Ventricular repolarization

  3 main waves = SPHERE coefficient

  Intervals:
    PR, QRS, QT, RR
    4 intervals = Bekenstein!
""")

# =============================================================================
# PART 4: CARDIAC OUTPUT - Z² FLOW
# =============================================================================

print("=" * 70)
print("PART 4: CARDIAC OUTPUT - Z² HEMODYNAMICS")
print("=" * 70)

print(f"""
CARDIAC OUTPUT (CO):

  Volume of blood pumped per minute.

  CO = Heart Rate × Stroke Volume
  CO = HR × SV

  Typical: 70 bpm × 70 mL = ~5 L/min

  5 L/min ≈ Z L/min at rest!

STROKE VOLUME:

  Blood ejected per beat.

  SV = EDV - ESV
     = End-diastolic volume - End-systolic volume
     = ~120 mL - ~50 mL = ~70 mL

  70 mL ≈ 2 × Z² mL ≈ 67 mL (close!)

EJECTION FRACTION:

  EF = SV/EDV × 100%
     = 70/120 × 100%
     = ~60%

  Normal EF: 55-70%
  <40%: Heart failure

  60 ≈ 2Z² ≈ 67% (order of magnitude)

REGULATION OF OUTPUT:

  Heart rate controlled by:
    - Sympathetic (increase)
    - Parasympathetic (decrease)

  2 divisions = factor of 2 in Z

  Stroke volume controlled by:
    1. Preload (filling)
    2. Afterload (resistance)
    3. Contractility (force)

  3 factors = SPHERE coefficient

FRANK-STARLING LAW:

  More filling → Stronger contraction
  The heart automatically adjusts output to input.

  This is intrinsic Z² regulation:
    CUBE (discrete beats) adjusts to SPHERE (continuous demand).
""")

# =============================================================================
# PART 5: CORONARY CIRCULATION - Z² SUPPLY
# =============================================================================

print("=" * 70)
print("PART 5: CORONARY CIRCULATION - HEART'S OWN BLOOD SUPPLY")
print("=" * 70)

print(f"""
CORONARY ARTERIES:

  The heart needs its own blood supply!
  ~5% of cardiac output goes to heart itself.

MAIN CORONARY ARTERIES:

  1. LEFT MAIN CORONARY
     - Short, then branches

  2. LEFT ANTERIOR DESCENDING (LAD)
     - Front of heart
     - "Widow maker" if blocked

  3. LEFT CIRCUMFLEX (LCX)
     - Wraps around left side

  4. RIGHT CORONARY (RCA)
     - Right side and bottom

  4 main arteries = Bekenstein!

CORONARY BLOOD FLOW:

  ~250 mL/min at rest
  Can increase 4-5× with exercise

  250 ≈ 7.5 × Z² (roughly)
  4-5× increase ≈ Bekenstein fold!

UNIQUE FEATURES:

  Coronary flow is mostly during DIASTOLE.
  (Systolic compression squeezes vessels)

  O₂ extraction: ~70-80% (highest of any organ!)
  Little reserve - flow must increase with demand.

CORONARY ARTERY DISEASE:

  Atherosclerosis narrows coronary arteries.
  Leading cause of death in developed world.

  Stages:
    1. Fatty streak
    2. Fibrous plaque
    3. Complicated plaque
    4. Rupture/thrombosis

  4 stages = Bekenstein!

  Risk factors:
    - Hypertension
    - Hyperlipidemia
    - Diabetes
    - Smoking

  4 major risk factors = Bekenstein!
""")

# =============================================================================
# PART 6: BLOOD PRESSURE - Z² REGULATION
# =============================================================================

print("=" * 70)
print("PART 6: BLOOD PRESSURE - Z² CARDIOVASCULAR CONTROL")
print("=" * 70)

print(f"""
BLOOD PRESSURE:

  Force of blood on vessel walls.
  Measured as systolic/diastolic (e.g., 120/80 mmHg).

NORMAL VALUES:

  Systolic: ~120 mmHg (peak pressure)
  Diastolic: ~80 mmHg (baseline)
  Mean arterial: ~93 mmHg

  120 = 10 × Gauge = 10 × 12
  80 = 10 × CUBE = 10 × 8

  The normal blood pressure encodes Z²!

PULSE PRESSURE:

  PP = Systolic - Diastolic = 120 - 80 = 40 mmHg

  40 ≈ Z² + Bekenstein + SPHERE ≈ 40 (like gamma rhythm!)

FACTORS AFFECTING BP:

  BP = CO × TPR
     = Cardiac Output × Total Peripheral Resistance

  2 factors = factor of 2 in Z

REGULATION:

  Short-term:
    - Baroreceptor reflex
    - Chemoreceptor reflex
    - CNS ischemic response

  3 reflexes = SPHERE coefficient

  Long-term:
    - Kidneys (fluid volume)
    - RAAS (renin-angiotensin-aldosterone)
    - ADH (antidiuretic hormone)
    - ANP (atrial natriuretic peptide)

  4 hormonal systems = Bekenstein!

HYPERTENSION:

  Chronically elevated BP (>140/90 mmHg).

  Types:
    1. Essential (95%, unknown cause)
    2. Secondary (5%, identifiable cause)

  2 types = factor of 2 in Z

  "Silent killer" - damages organs without symptoms.
""")

# =============================================================================
# PART 7: CARDIAC MUSCLE - Z² CELLS
# =============================================================================

print("=" * 70)
print("PART 7: CARDIAC MUSCLE - Z² CELLULAR MECHANISM")
print("=" * 70)

print(f"""
CARDIOMYOCYTES:

  Cardiac muscle cells are unique:
    - Striated (like skeletal muscle)
    - Involuntary (like smooth muscle)
    - Electrically coupled (like neurons)

THE SARCOMERE:

  Contractile unit of muscle.

  Bands:
    - A band (dark, myosin)
    - I band (light, actin)
    - Z line (attachment)
    - H zone (center)
    - M line (middle of H)

  ~4-5 main features ≈ Bekenstein

  Sarcomere length: ~2 μm at rest
  2 μm ≈ 2/Z³ mm (if μm and mm relate via 1000 = Z³×5)

SLIDING FILAMENT THEORY:

  Contraction = actin slides past myosin.

  Steps:
    1. Ca²⁺ released from SR
    2. Ca²⁺ binds troponin C
    3. Tropomyosin moves, exposes actin
    4. Myosin cross-bridge cycle

  4 steps = Bekenstein!

INTERCALATED DISCS:

  Connections between cardiomyocytes.

  Components:
    - Desmosomes (mechanical coupling)
    - Gap junctions (electrical coupling)
    - Adherens junctions (anchoring)

  3 components = SPHERE coefficient

  Gap junctions allow heart to act as FUNCTIONAL SYNCYTIUM.
  Electrical signal spreads from cell to cell.

ENERGY METABOLISM:

  Heart is aerobic - needs constant O₂.

  Fuels:
    - Fatty acids (~70%)
    - Glucose (~20%)
    - Lactate (~10%)

  3 main fuels = SPHERE coefficient

  Heart has many mitochondria (~30% of cell volume).
  30% ≈ Z² % (close to 33%!)
""")

# =============================================================================
# PART 8: HEART FAILURE - Z² BREAKDOWN
# =============================================================================

print("=" * 70)
print("PART 8: HEART FAILURE - Z² SYSTEM FAILURE")
print("=" * 70)

print(f"""
HEART FAILURE:

  Heart can't meet body's demands.
  Not "heart attack" (that's MI).

TYPES:

  1. SYSTOLIC (HFrEF)
     - Reduced ejection fraction
     - Weak squeeze
     - EF < 40%

  2. DIASTOLIC (HFpEF)
     - Preserved ejection fraction
     - Stiff heart, poor filling
     - EF > 50%

  3. RIGHT HEART FAILURE
     - Fluid backs up into body
     - Peripheral edema

  4. LEFT HEART FAILURE
     - Fluid backs up into lungs
     - Pulmonary edema

  4 types = Bekenstein!

NYHA FUNCTIONAL CLASSES:

  Classification of symptoms:

  Class I: No limitation
  Class II: Mild limitation
  Class III: Marked limitation
  Class IV: Symptoms at rest

  4 classes = Bekenstein!

COMPENSATORY MECHANISMS:

  1. Frank-Starling (increased preload)
  2. Tachycardia (increased HR)
  3. Hypertrophy (thicker walls)
  4. Neurohormonal activation (RAAS, SNS)

  4 mechanisms = Bekenstein!

  These initially help but eventually fail.
  Become maladaptive - vicious cycle.

TREATMENT:

  Medications:
    - ACE inhibitors/ARBs
    - Beta blockers
    - Diuretics
    - Aldosterone antagonists

  4 main drug classes = Bekenstein!

  Devices:
    - Pacemakers
    - ICDs (defibrillators)
    - CRT (resynchronization)
    - LVAD (pump assist)

  4 device types = Bekenstein!
""")

# =============================================================================
# PART 9: THE HEART ACROSS EVOLUTION
# =============================================================================

print("=" * 70)
print("PART 9: HEART EVOLUTION - Z² PUMP DEVELOPMENT")
print("=" * 70)

print(f"""
HEART EVOLUTION:

  From simple tubes to four chambers.

EVOLUTIONARY PROGRESSION:

  1. NO HEART (simple invertebrates)
     - Diffusion sufficient
     - Small body size

  2. TUBULAR HEART (insects, worms)
     - Simple pump
     - Open circulation

  3. TWO-CHAMBERED (fish)
     - 1 atrium, 1 ventricle
     - Single circulation

  4. THREE-CHAMBERED (amphibians, reptiles)
     - 2 atria, 1 ventricle (partially divided)
     - Some mixing of blood

  5. FOUR-CHAMBERED (birds, mammals)
     - Complete separation
     - No mixing
     - High efficiency

  From 2 → 3 → 4 chambers
  Converging on Bekenstein = 4!

WHY FOUR CHAMBERS?

  4 chambers allow:
    - Complete separation of circuits
    - High systemic pressure (warm-blooded)
    - Efficient oxygen delivery

  Mammals and birds evolved 4-chambered hearts INDEPENDENTLY.
  Convergent evolution to Bekenstein!

HEART RATE SCALING:

  Smaller animals: Faster heart rate
  Larger animals: Slower heart rate

  HR ∝ M^(-0.25)

  where M is body mass.

  The exponent -0.25 = -1/4 = -1/Bekenstein!

LIFETIME HEARTBEATS:

  Most mammals: ~1 billion heartbeats in lifetime
  (Regardless of size - rate adjusts)

  1 billion = 10⁹ ≈ Z^... (large number)

  Humans: ~3 billion (longer lifespan)
  3 = SPHERE coefficient
""")

# =============================================================================
# PART 10: SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY: THE HEART AS Z² PUMP")
print("=" * 70)

print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║            THE HEART: Z² FRAMEWORK                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ANATOMY:                                                             ║
║                                                                       ║
║      4 chambers = Bekenstein                                          ║
║      4 valves = Bekenstein                                            ║
║      4 wall layers = Bekenstein                                       ║
║      2 circulations = factor of 2 in Z                               ║
║                                                                       ║
║  THE CARDIAC CYCLE:                                                   ║
║                                                                       ║
║      4 phases = Bekenstein                                            ║
║      2 main phases (systole/diastole) = factor of 2 in Z             ║
║                                                                       ║
║  CONDUCTION:                                                          ║
║                                                                       ║
║      4 conduction components = Bekenstein                            ║
║      3 pacemaker levels = SPHERE coefficient                         ║
║      4 ECG intervals = Bekenstein                                    ║
║                                                                       ║
║  CARDIAC OUTPUT:                                                      ║
║                                                                       ║
║      ~5 L/min ≈ Z L/min                                              ║
║      ~70 mL stroke volume ≈ 2Z² mL                                   ║
║      3 SV determinants = SPHERE coefficient                          ║
║                                                                       ║
║  BLOOD PRESSURE:                                                      ║
║                                                                       ║
║      120 mmHg systolic = 10 × Gauge                                  ║
║      80 mmHg diastolic = 10 × CUBE                                   ║
║      4 hormonal regulators = Bekenstein                              ║
║                                                                       ║
║  HEART FAILURE:                                                       ║
║                                                                       ║
║      4 types = Bekenstein                                             ║
║      4 NYHA classes = Bekenstein                                      ║
║      4 compensations = Bekenstein                                     ║
║      4 drug classes = Bekenstein                                      ║
║                                                                       ║
║  EVOLUTION:                                                           ║
║                                                                       ║
║      Converges on 4 chambers = Bekenstein                            ║
║      HR ∝ M^(-1/4) = M^(-1/Bekenstein)                               ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════

THE HEART IS A Z² MACHINE:

    4 chambers (Bekenstein) pump in 2 phases (factor of 2)
    through 2 circuits (factor of 2) with 4 valves (Bekenstein).

    Blood pressure: 120/80 = (10×Gauge)/(10×CUBE)
    Cardiac output: ~5 L/min ≈ Z L/min

    The heart beats ~3 billion times in a human lifetime,
    each beat a Z² cycle of CUBE (contraction) × SPHERE (flow).

    Life is sustained by Z² pumping.

═══════════════════════════════════════════════════════════════════════════
""")

print("\n[HEART_CARDIAC_Z2_DERIVATION.py complete]")
