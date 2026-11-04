import Std
namespace AZ20

def singleResponse (B y : Rat) : Rat := 1 - 1 / (1 + B*y)^2
def paired (b eta y : Rat) : Rat :=
  (singleResponse (eta*b) y + singleResponse (eta/b) y) / 2
def unequal (b eta y : Rat) : Rat :=
  singleResponse (eta*b) y / 3 + 2*singleResponse (eta/b) y / 3

theorem reciprocal_known_answer : paired 2 3 2 = paired (1/2) 3 2 := by
  decide +kernel

theorem unequal_breaks_exchange : unequal 2 3 2 ≠ unequal (1/2) 3 2 := by
  decide +kernel
end AZ20
#print axioms AZ20.reciprocal_known_answer
#print axioms AZ20.unequal_breaks_exchange
