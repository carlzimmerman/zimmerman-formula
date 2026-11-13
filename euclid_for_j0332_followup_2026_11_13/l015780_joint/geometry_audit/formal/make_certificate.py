"""Generate the concrete nominal finite-array Lean instance, never a PDE claim."""
import hashlib,json
from fractions import Fraction
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
FIELD=HERE.parents[1]/"field_grid_01/positions_deflections.npz"

TEMPLATE=r'''
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! Finite four-marker source-association certificate. Coordinates are west/north
in arcseconds. This proves no image/PDE/theory goodness of fit. The declared
finite alpha arrays, zero convergence, and association premise are the scope. -/

namespace L015780Capacity

def thetaX (i : Fin 4) : ℝ := match i.val with
  | 0 => -39/20 | 1 => -11/20 | 2 => 53/20 | _ => -11/20
def thetaY (i : Fin 4) : ℝ := match i.val with
  | 0 => -37/20 | 1 => -53/20 | 2 => -3/4 | _ => 7/4

def centerAX (i : Fin 4) : ℝ := match i.val with
  | 0 => -13065/10000 | 1 => -3828/10000 | 2 => 16311/10000 | _ => -7190/10000
def centerAY (i : Fin 4) : ℝ := match i.val with
  | 0 => -9902/10000 | 1 => -15596/10000 | 2 => -4515/10000 | _ => 15525/10000

def storedAX (i : Fin 4) : ℝ := match i.val with
  | 0 => __AX0__ | 1 => __AX1__ | 2 => __AX2__ | _ => __AX3__
def storedAY (i : Fin 4) : ℝ := match i.val with
  | 0 => __AY0__ | 1 => __AY1__ | 2 => __AY2__ | _ => __AY3__

/-- Exact four-source scalar identity; apply once per sky coordinate. -/
theorem four_pair_identity (w0 w1 w2 w3 b0 b1 b2 b3 : ℝ)
    (hw : w0+w1+w2+w3=0) :
    4*(w0*b0+w1*b1+w2*b2+w3*b3) =
      (w0-w1)*(b0-b1)+(w0-w2)*(b0-b2)+(w0-w3)*(b0-b3)+
      (w1-w2)*(b1-b2)+(w1-w3)*(b1-b3)+(w2-w3)*(b2-b3) := by
  calc
    _ = ((w0-w1)*(b0-b1)+(w0-w2)*(b0-b2)+(w0-w3)*(b0-b3)+
      (w1-w2)*(b1-b2)+(w1-w3)*(b1-b3)+(w2-w3)*(b2-b3))+
        (w0+w1+w2+w3)*(b0+b1+b2+b3) := by ring
    _ = _ := by rw [hw]; ring

/-- One exact rational nuisance-null functional, scaled to integer weights. -/
def projection (x y : Fin 4 → ℝ) : ℝ :=
  -72*x 0 -69*y 0 +7*x 1 -61*y 1 +130*x 2 -65*x 3 +130*y 3

theorem projection_pair_identity (x y : Fin 4 → ℝ) :
    4*projection x y =
      -79*(x 0-x 1)-8*(y 0-y 1)-202*(x 0-x 2)-69*(y 0-y 2)
      -7*(x 0-x 3)-199*(y 0-y 3)-123*(x 1-x 2)-61*(y 1-y 2)
      +72*(x 1-x 3)-191*(y 1-y 3)+195*(x 2-x 3)-130*(y 2-y 3) := by
  unfold projection
  ring

/-- A Euclidean pair-diameter gate implies a bound on either coordinate. -/
theorem component_bound (x y : ℝ)
    (h : Real.sqrt (x^2+y^2) ≤ (3/10 : ℝ)) : |x| ≤ (3/10 : ℝ) := by
  have hs : 0 ≤ Real.sqrt (x^2+y^2) := Real.sqrt_nonneg _
  have hs2 : (Real.sqrt (x^2+y^2))^2=x^2+y^2 := Real.sq_sqrt (by positivity)
  have hp : 0 ≤ ((3/10 : ℝ)-Real.sqrt (x^2+y^2))*
      ((3/10 : ℝ)+Real.sqrt (x^2+y^2)) :=
    mul_nonneg (sub_nonneg.mpr h) (by positivity)
  have hx2 : x^2 ≤ (3/10 : ℝ)^2 := by nlinarith [sq_nonneg y]
  apply abs_le.mpr
  constructor
  · nlinarith [sq_nonneg (x+(3/10 : ℝ))]
  · nlinarith [sq_nonneg (x-(3/10 : ℝ))]

noncomputable def separation (x y : Fin 4 → ℝ) (i j : Fin 4) : ℝ :=
  Real.sqrt ((x i-x j)^2+(y i-y j)^2)

/-- Pair diameter .3 bounds the nuisance-null functional by100.2. -/
theorem gate_projection_bound (x y : Fin 4 → ℝ)
    (h : ∀ i j, separation x y i j ≤ (3/10 : ℝ)) :
    projection x y ≤ (501/5 : ℝ) := by
  have hx (i j : Fin 4) : |x i-x j| ≤ (3/10 : ℝ) :=
    component_bound _ _ (h i j)
  have hy (i j : Fin 4) : |y i-y j| ≤ (3/10 : ℝ) := by
    apply component_bound _ (x i-x j)
    simpa only [separation, add_comm] using h i j
  have h01x := (abs_le.mp (hx 0 1)).1
  have h01y := (abs_le.mp (hy 0 1)).1
  have h02x := (abs_le.mp (hx 0 2)).1
  have h02y := (abs_le.mp (hy 0 2)).1
  have h03x := (abs_le.mp (hx 0 3)).1
  have h03y := (abs_le.mp (hy 0 3)).1
  have h12x := (abs_le.mp (hx 1 2)).1
  have h12y := (abs_le.mp (hy 1 2)).1
  have h13x := (abs_le.mp (hx 1 3)).2
  have h13y := (abs_le.mp (hy 1 3)).1
  have h23x := (abs_le.mp (hx 2 3)).2
  have h23y := (abs_le.mp (hy 2 3)).1
  have hid := projection_pair_identity x y
  linarith

def sourceX (aX aY : Fin 4 → ℝ) (beta g1 g2 : ℝ) (i : Fin 4) : ℝ :=
  thetaX i-beta*aX i-g1*thetaX i-g2*thetaY i
def sourceY (aX aY : Fin 4 → ℝ) (beta g1 g2 : ℝ) (i : Fin 4) : ℝ :=
  thetaY i-beta*aY i-g2*thetaX i+g1*thetaY i

/-- Both unrestricted shear components cancel, as do constant source shifts. -/
theorem nuisance_cancels (aX aY : Fin 4 → ℝ) (beta g1 g2 : ℝ) :
    projection (sourceX aX aY beta g1 g2) (sourceY aX aY beta g1 g2) =
      (5168/5 : ℝ)-beta*projection aX aY := by
  norm_num [projection, sourceX, sourceY, thetaX, thetaY]
  ring

/-- A specified .05arcsec component box safely bounds the deflection projection.
    This box is a mathematical robustness fixture, not a proved PDE error bar. -/
theorem field_box_projection (aX aY : Fin 4 → ℝ)
    (hx : ∀ i, |aX i-centerAX i| ≤ (1/20 : ℝ))
    (hy : ∀ i, |aY i-centerAY i| ≤ (1/20 : ℝ)) :
    projection aX aY ≤ (750 : ℝ) := by
  have x0 := (abs_le.mp (hx 0)).1
  have y0 := (abs_le.mp (hy 0)).1
  have x1 := (abs_le.mp (hx 1)).2
  have y1 := (abs_le.mp (hy 1)).1
  have x2 := (abs_le.mp (hx 2)).2
  have x3 := (abs_le.mp (hx 3)).1
  have y3 := (abs_le.mp (hy 3)).2
  norm_num [centerAX, centerAY] at x0 y0 x1 y1 x2 x3 y3
  unfold projection
  linarith

/-- Source association is impossible throughout this explicit finite-field box,
    for every beta in[0,1] and arbitrary real shear, at zero convergence. -/
theorem robust_finite_field_gate_impossible
    (aX aY : Fin 4 → ℝ) (beta g1 g2 : ℝ)
    (hb0 : 0 ≤ beta) (hb1 : beta ≤ 1)
    (hx : ∀ i, |aX i-centerAX i| ≤ (1/20 : ℝ))
    (hy : ∀ i, |aY i-centerAY i| ≤ (1/20 : ℝ)) :
    ¬ (∀ i j, separation (sourceX aX aY beta g1 g2)
      (sourceY aX aY beta g1 g2) i j ≤ (3/10 : ℝ)) := by
  intro gate
  have hg := gate_projection_bound _ _ gate
  have hc := nuisance_cancels aX aY beta g1 g2
  have hf := field_box_projection aX aY hx hy
  have hm := mul_le_mul_of_nonneg_left hf hb0
  have hb := mul_le_mul_of_nonneg_right hb1 (show (0 : ℝ) ≤ 750 by norm_num)
  linarith

theorem stored_X_in_box (i : Fin 4) :
    |storedAX i-centerAX i| ≤ (1/20 : ℝ) := by
  fin_cases i <;> norm_num [storedAX,centerAX]
theorem stored_Y_in_box (i : Fin 4) :
    |storedAY i-centerAY i| ≤ (1/20 : ℝ) := by
  fin_cases i <;> norm_num [storedAY,centerAY]

/-- Instantiated stored inc90,logM11.925 finite-field source-gate incompatibility. -/
theorem nominal_stored_field_gate_impossible (beta g1 g2 : ℝ)
    (hb0 : 0 ≤ beta) (hb1 : beta ≤ 1) :
    ¬ (∀ i j, separation (sourceX storedAX storedAY beta g1 g2)
      (sourceY storedAX storedAY beta g1 g2) i j ≤ (3/10 : ℝ)) :=
  robust_finite_field_gate_impossible storedAX storedAY beta g1 g2 hb0 hb1
    stored_X_in_box stored_Y_in_box

end L015780Capacity

#print axioms L015780Capacity.four_pair_identity
#print axioms L015780Capacity.gate_projection_bound
#print axioms L015780Capacity.nuisance_cancels
#print axioms L015780Capacity.robust_finite_field_gate_impossible
#print axioms L015780Capacity.nominal_stored_field_gate_impossible
'''


def main():
    data=np.load(FIELD)
    ii=int(np.argmin(abs(data['inclination']-90)))
    jj=int(np.argmin(abs(data['logmass']-11.925)))
    assert abs(data['logmass'][jj]-11.925)<1e-12
    alpha=data['alpha_hat_sky'][ii,jj]
    text=TEMPLATE.replace('\ndef ','\nnoncomputable def ')
    rational=[]
    for coordinate,name in enumerate(['AX','AY']):
        row=[]
        for i in range(4):
            f=Fraction.from_float(float(alpha[coordinate,i]))
            row.append(str(f))
            text=text.replace(f'__{name}{i}__',f'({f.numerator} : ℝ)/{f.denominator}')
        rational.append(row)
    source=HERE/'FiniteCapacity.lean'
    source.write_text(text)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    record={'field_input':str(FIELD),'field_sha256':sha(FIELD),
        'inclination':float(data['inclination'][ii]),'logmass':float(data['logmass'][jj]),
        'alpha_hat_exact_rationals':rational,'alpha_hat_float':alpha.tolist(),
        'source_sha256':sha(source),'generator_sha256':sha(Path(__file__).resolve()),
        'scope':'Finite arrays and declared field-box/source-gate premises; no PDE, observational or full-theory certificate'}
    (HERE/'instance.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
