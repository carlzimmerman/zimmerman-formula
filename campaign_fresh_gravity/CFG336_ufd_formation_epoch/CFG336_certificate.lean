import Mathlib

/-! CFG336: formation-epoch density of the native cold mass. Bounds rounded outward from cfg336_formation_epoch_results.json. -/

theorem cfg336_max_inert (ph c : ℚ) (h : c ≤ ph) : max ph c = ph := max_eq_left h

-- Aquarius II (canonical)
theorem cfg336_ufd00_canonical_bound (ph c : ℚ) (h1 : (291910 : ℚ) ≤ ph) (h2 : c ≤ (50880 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Bootes I (canonical)
theorem cfg336_ufd01_canonical_bound (ph c : ℚ) (h1 : (811102 : ℚ) ≤ ph) (h2 : c ≤ (234718 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Bootes II (canonical)
theorem cfg336_ufd02_canonical_bound (ph c : ℚ) (h1 : (40187 : ℚ) ≤ ph) (h2 : c ≤ (13758 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Bootes III (canonical)
theorem cfg336_ufd03_canonical_bound (ph c : ℚ) (h1 : (2175393 : ℚ) ≤ ph) (h2 : c ≤ (197036 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Canes Venatici II (canonical)
theorem cfg336_ufd04_canonical_bound (ph c : ℚ) (h1 : (181740 : ℚ) ≤ ph) (h2 : c ≤ (107287 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Carina II (canonical)
theorem cfg336_ufd05_canonical_bound (ph c : ℚ) (h1 : (197673 : ℚ) ≤ ph) (h2 : c ≤ (61737 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Carina III (canonical)
theorem cfg336_ufd06_canonical_bound (ph c : ℚ) (h1 : (18435 : ℚ) ≤ ph) (h2 : c ≤ (8367 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Centaurus I (canonical)
theorem cfg336_ufd07_canonical_bound (ph c : ℚ) (h1 : (260517 : ℚ) ≤ ph) (h2 : c ≤ (126633 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Columba I (canonical)
theorem cfg336_ufd08_canonical_bound (ph c : ℚ) (h1 : (213095 : ℚ) ≤ ph) (h2 : c ≤ (43909 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Coma Berenices (canonical)
theorem cfg336_ufd09_canonical_bound (ph c : ℚ) (h1 : (124353 : ℚ) ≤ ph) (h2 : c ≤ (47703 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Eridanus II (canonical)
theorem cfg336_ufd10_canonical_bound (ph c : ℚ) (h1 : (1487651 : ℚ) ≤ ph) (h2 : c ≤ (646466 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Eridanus IV (canonical)
theorem cfg336_ufd11_canonical_bound (ph c : ℚ) (h1 : (90925 : ℚ) ≤ ph) (h2 : c ≤ (24130 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Grus I (canonical)
theorem cfg336_ufd12_canonical_bound (ph c : ℚ) (h1 : (240808 : ℚ) ≤ ph) (h2 : c ≤ (41167 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Hercules (canonical)
theorem cfg336_ufd13_canonical_bound (ph c : ℚ) (h1 : (540981 : ℚ) ≤ ph) (h2 : c ≤ (193440 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Horologium I (canonical)
theorem cfg336_ufd14_canonical_bound (ph c : ℚ) (h1 : (47025 : ℚ) ≤ ph) (h2 : c ≤ (20633 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Hydrus I (canonical)
theorem cfg336_ufd15_canonical_bound (ph c : ℚ) (h1 : (143277 : ℚ) ≤ ph) (h2 : c ≤ (70234 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Leo IV (canonical)
theorem cfg336_ufd16_canonical_bound (ph c : ℚ) (h1 : (311590 : ℚ) ≤ ph) (h2 : c ≤ (87609 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Leo V (canonical)
theorem cfg336_ufd17_canonical_bound (ph c : ℚ) (h1 : (82938 : ℚ) ≤ ph) (h2 : c ≤ (52790 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Leo VI (canonical)
theorem cfg336_ufd18_canonical_bound (ph c : ℚ) (h1 : (141836 : ℚ) ≤ ph) (h2 : c ≤ (24353 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pegasus III (canonical)
theorem cfg336_ufd19_canonical_bound (ph c : ℚ) (h1 : (177023 : ℚ) ≤ ph) (h2 : c ≤ (42712 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pegasus IV (canonical)
theorem cfg336_ufd20_canonical_bound (ph c : ℚ) (h1 : (92024 : ℚ) ≤ ph) (h2 : c ≤ (45978 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pictor II (canonical)
theorem cfg336_ufd21_canonical_bound (ph c : ℚ) (h1 : (33999 : ℚ) ≤ ph) (h2 : c ≤ (10533 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pisces II (canonical)
theorem cfg336_ufd22_canonical_bound (ph c : ℚ) (h1 : (126933 : ℚ) ≤ ph) (h2 : c ≤ (47266 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Reticulum II (canonical)
theorem cfg336_ufd23_canonical_bound (ph c : ℚ) (h1 : (47816 : ℚ) ≤ ph) (h2 : c ≤ (15943 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Segue 1 (canonical)
theorem cfg336_ufd24_canonical_bound (ph c : ℚ) (h1 : (11206 : ℚ) ≤ ph) (h2 : c ≤ (3038 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana II (canonical)
theorem cfg336_ufd25_canonical_bound (ph c : ℚ) (h1 : (289085 : ℚ) ≤ ph) (h2 : c ≤ (29010 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana IV (canonical)
theorem cfg336_ufd26_canonical_bound (ph c : ℚ) (h1 : (124100 : ℚ) ≤ ph) (h2 : c ≤ (14540 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana V (canonical)
theorem cfg336_ufd27_canonical_bound (ph c : ℚ) (h1 : (11970 : ℚ) ≤ ph) (h2 : c ≤ (2527 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Ursa Major I (canonical)
theorem cfg336_ufd28_canonical_bound (ph c : ℚ) (h1 : (506734 : ℚ) ≤ ph) (h2 : c ≤ (104363 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Ursa Major II (canonical)
theorem cfg336_ufd29_canonical_bound (ph c : ℚ) (h1 : (222663 : ℚ) ≤ ph) (h2 : c ≤ (53771 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Willman 1 (canonical)
theorem cfg336_ufd30_canonical_bound (ph c : ℚ) (h1 : (20028 : ℚ) ≤ ph) (h2 : c ≤ (9431 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Aquarius III (canonical)
theorem cfg336_ufd31_canonical_bound (ph c : ℚ) (h1 : (36225 : ℚ) ≤ ph) (h2 : c ≤ (9174 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Draco II (canonical)
theorem cfg336_ufd32_canonical_bound (ph c : ℚ) (h1 : (7345 : ℚ) ≤ ph) (h2 : c ≤ (1917 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Grus II (canonical)
theorem cfg336_ufd33_canonical_bound (ph c : ℚ) (h1 : (205239 : ℚ) ≤ ph) (h2 : c ≤ (43506 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Hydra II (canonical)
theorem cfg336_ufd34_canonical_bound (ph c : ℚ) (h1 : (185123 : ℚ) ≤ ph) (h2 : c ≤ (100588 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Phoenix II (canonical)
theorem cfg336_ufd35_canonical_bound (ph c : ℚ) (h1 : (27957 : ℚ) ≤ ph) (h2 : c ≤ (10059 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Reticulum III (canonical)
theorem cfg336_ufd36_canonical_bound (ph c : ℚ) (h1 : (89906 : ℚ) ≤ ph) (h2 : c ≤ (19167 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Segue 2 (canonical)
theorem cfg336_ufd37_canonical_bound (ph c : ℚ) (h1 : (27205 : ℚ) ≤ ph) (h2 : c ≤ (5528 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Triangulum II (canonical)
theorem cfg336_ufd38_canonical_bound (ph c : ℚ) (h1 : (9840 : ℚ) ≤ ph) (h2 : c ≤ (3038 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana III (canonical)
theorem cfg336_ufd39_canonical_bound (ph c : ℚ) (h1 : (17298 : ℚ) ≤ ph) (h2 : c ≤ (3038 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Aquarius II (alt)
theorem cfg336_ufd00_alt_bound (ph c : ℚ) (h1 : (320971 : ℚ) ≤ ph) (h2 : c ≤ (50880 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Bootes I (alt)
theorem cfg336_ufd01_alt_bound (ph c : ℚ) (h1 : (892274 : ℚ) ≤ ph) (h2 : c ≤ (234718 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Bootes II (alt)
theorem cfg336_ufd02_alt_bound (ph c : ℚ) (h1 : (44219 : ℚ) ≤ ph) (h2 : c ≤ (13758 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Bootes III (alt)
theorem cfg336_ufd03_alt_bound (ph c : ℚ) (h1 : (2391131 : ℚ) ≤ ph) (h2 : c ≤ (197036 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Canes Venatici II (alt)
theorem cfg336_ufd04_alt_bound (ph c : ℚ) (h1 : (200174 : ℚ) ≤ ph) (h2 : c ≤ (107287 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Carina II (alt)
theorem cfg336_ufd05_alt_bound (ph c : ℚ) (h1 : (217476 : ℚ) ≤ ph) (h2 : c ≤ (61737 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Carina III (alt)
theorem cfg336_ufd06_alt_bound (ph c : ℚ) (h1 : (20293 : ℚ) ≤ ph) (h2 : c ≤ (8367 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Centaurus I (alt)
theorem cfg336_ufd07_alt_bound (ph c : ℚ) (h1 : (286820 : ℚ) ≤ ph) (h2 : c ≤ (126633 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Columba I (alt)
theorem cfg336_ufd08_alt_bound (ph c : ℚ) (h1 : (234340 : ℚ) ≤ ph) (h2 : c ≤ (43909 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Coma Berenices (alt)
theorem cfg336_ufd09_alt_bound (ph c : ℚ) (h1 : (136851 : ℚ) ≤ ph) (h2 : c ≤ (47703 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Eridanus II (alt)
theorem cfg336_ufd10_alt_bound (ph c : ℚ) (h1 : (1637503 : ℚ) ≤ ph) (h2 : c ≤ (646466 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Eridanus IV (alt)
theorem cfg336_ufd11_alt_bound (ph c : ℚ) (h1 : (100014 : ℚ) ≤ ph) (h2 : c ≤ (24130 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Grus I (alt)
theorem cfg336_ufd12_alt_bound (ph c : ℚ) (h1 : (264778 : ℚ) ≤ ph) (h2 : c ≤ (41167 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Hercules (alt)
theorem cfg336_ufd13_alt_bound (ph c : ℚ) (h1 : (595288 : ℚ) ≤ ph) (h2 : c ≤ (193440 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Horologium I (alt)
theorem cfg336_ufd14_alt_bound (ph c : ℚ) (h1 : (51763 : ℚ) ≤ ph) (h2 : c ≤ (20633 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Hydrus I (alt)
theorem cfg336_ufd15_alt_bound (ph c : ℚ) (h1 : (157746 : ℚ) ≤ ph) (h2 : c ≤ (70234 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Leo IV (alt)
theorem cfg336_ufd16_alt_bound (ph c : ℚ) (h1 : (342762 : ℚ) ≤ ph) (h2 : c ≤ (87609 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Leo V (alt)
theorem cfg336_ufd17_alt_bound (ph c : ℚ) (h1 : (91367 : ℚ) ≤ ph) (h2 : c ≤ (52790 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Leo VI (alt)
theorem cfg336_ufd18_alt_bound (ph c : ℚ) (h1 : (155955 : ℚ) ≤ ph) (h2 : c ≤ (24353 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pegasus III (alt)
theorem cfg336_ufd19_alt_bound (ph c : ℚ) (h1 : (194700 : ℚ) ≤ ph) (h2 : c ≤ (42712 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pegasus IV (alt)
theorem cfg336_ufd20_alt_bound (ph c : ℚ) (h1 : (101321 : ℚ) ≤ ph) (h2 : c ≤ (45978 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pictor II (alt)
theorem cfg336_ufd21_alt_bound (ph c : ℚ) (h1 : (37404 : ℚ) ≤ ph) (h2 : c ≤ (10533 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Pisces II (alt)
theorem cfg336_ufd22_alt_bound (ph c : ℚ) (h1 : (139683 : ℚ) ≤ ph) (h2 : c ≤ (47266 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Reticulum II (alt)
theorem cfg336_ufd23_alt_bound (ph c : ℚ) (h1 : (52610 : ℚ) ≤ ph) (h2 : c ≤ (15943 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Segue 1 (alt)
theorem cfg336_ufd24_alt_bound (ph c : ℚ) (h1 : (12327 : ℚ) ≤ ph) (h2 : c ≤ (3038 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana II (alt)
theorem cfg336_ufd25_alt_bound (ph c : ℚ) (h1 : (317767 : ℚ) ≤ ph) (h2 : c ≤ (29010 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana IV (alt)
theorem cfg336_ufd26_alt_bound (ph c : ℚ) (h1 : (136422 : ℚ) ≤ ph) (h2 : c ≤ (14540 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana V (alt)
theorem cfg336_ufd27_alt_bound (ph c : ℚ) (h1 : (13164 : ℚ) ≤ ph) (h2 : c ≤ (2527 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Ursa Major I (alt)
theorem cfg336_ufd28_alt_bound (ph c : ℚ) (h1 : (557255 : ℚ) ≤ ph) (h2 : c ≤ (104363 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Ursa Major II (alt)
theorem cfg336_ufd29_alt_bound (ph c : ℚ) (h1 : (244898 : ℚ) ≤ ph) (h2 : c ≤ (53771 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Willman 1 (alt)
theorem cfg336_ufd30_alt_bound (ph c : ℚ) (h1 : (22049 : ℚ) ≤ ph) (h2 : c ≤ (9431 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Aquarius III (alt)
theorem cfg336_ufd31_alt_bound (ph c : ℚ) (h1 : (39844 : ℚ) ≤ ph) (h2 : c ≤ (9174 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Draco II (alt)
theorem cfg336_ufd32_alt_bound (ph c : ℚ) (h1 : (8079 : ℚ) ≤ ph) (h2 : c ≤ (1917 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Grus II (alt)
theorem cfg336_ufd33_alt_bound (ph c : ℚ) (h1 : (225707 : ℚ) ≤ ph) (h2 : c ≤ (43506 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Hydra II (alt)
theorem cfg336_ufd34_alt_bound (ph c : ℚ) (h1 : (203860 : ℚ) ≤ ph) (h2 : c ≤ (100588 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Phoenix II (alt)
theorem cfg336_ufd35_alt_bound (ph c : ℚ) (h1 : (30764 : ℚ) ≤ ph) (h2 : c ≤ (10059 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Reticulum III (alt)
theorem cfg336_ufd36_alt_bound (ph c : ℚ) (h1 : (98872 : ℚ) ≤ ph) (h2 : c ≤ (19167 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Segue 2 (alt)
theorem cfg336_ufd37_alt_bound (ph c : ℚ) (h1 : (29917 : ℚ) ≤ ph) (h2 : c ≤ (5528 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Triangulum II (alt)
theorem cfg336_ufd38_alt_bound (ph c : ℚ) (h1 : (10826 : ℚ) ≤ ph) (h2 : c ≤ (3038 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

-- Tucana III (alt)
theorem cfg336_ufd39_alt_bound (ph c : ℚ) (h1 : (19020 : ℚ) ≤ ph) (h2 : c ≤ (3038 : ℚ)) :
    c < ph ∧ max ph c = ph := by
  have h : c < ph := by linarith
  exact ⟨h, max_eq_left h.le⟩

theorem cfg336_S_P1_UFD_canonical_fail (m e : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : e ≤ (43/500 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg336_S_P1_CLS_canonical_pass (m e : ℚ) (h1 : (27/1000 : ℚ) ≤ m) (h2 : m ≤ (271/10000 : ℚ)) (h3 : (423/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_M31col_canonical_pass (m e : ℚ) (h1 : (8/125 : ℚ) ≤ m) (h2 : m ≤ (641/10000 : ℚ)) (h3 : (103/1250 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_M31lvd_canonical_pass (m e : ℚ) (h1 : (87/2000 : ℚ) ≤ m) (h2 : m ≤ (109/2500 : ℚ)) (h3 : (181/2500 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_LVfld_canonical_pass (m e : ℚ) (h1 : (-11/250 : ℚ) ≤ m) (h2 : m ≤ (-439/10000 : ℚ)) (h3 : (147/2000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_UFD_alt_fail (m e : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : e ≤ (859/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg336_S_P1_CLS_alt_pass (m e : ℚ) (h1 : (3/400 : ℚ) ≤ m) (h2 : m ≤ (19/2500 : ℚ)) (h3 : (843/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_M31col_alt_pass (m e : ℚ) (h1 : (9/200 : ℚ) ≤ m) (h2 : m ≤ (451/10000 : ℚ)) (h3 : (823/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_M31lvd_alt_pass (m e : ℚ) (h1 : (307/10000 : ℚ) ≤ m) (h2 : m ≤ (77/2500 : ℚ)) (h3 : (367/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_LVfld_alt_pass (m e : ℚ) (h1 : (-621/10000 : ℚ) ≤ m) (h2 : m ≤ (-31/500 : ℚ)) (h3 : (733/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_S_P1_not_partial_canonical (m b : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : b ≤ (1623/5000 : ℚ)) :
    b / 2 < m := by
  linarith

theorem cfg336_S_P1_not_partial_alt (m b : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : b ≤ (609/2000 : ℚ)) :
    b / 2 < m := by
  linarith

theorem cfg336_M_P1_UFD_canonical_fail (m e : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : e ≤ (43/500 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg336_M_P1_CLS_canonical_pass (m e : ℚ) (h1 : (27/1000 : ℚ) ≤ m) (h2 : m ≤ (271/10000 : ℚ)) (h3 : (423/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_M31col_canonical_pass (m e : ℚ) (h1 : (8/125 : ℚ) ≤ m) (h2 : m ≤ (641/10000 : ℚ)) (h3 : (103/1250 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_M31lvd_canonical_pass (m e : ℚ) (h1 : (87/2000 : ℚ) ≤ m) (h2 : m ≤ (109/2500 : ℚ)) (h3 : (29/400 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_LVfld_canonical_pass (m e : ℚ) (h1 : (-11/250 : ℚ) ≤ m) (h2 : m ≤ (-439/10000 : ℚ)) (h3 : (147/2000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_UFD_alt_fail (m e : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : e ≤ (859/10000 : ℚ)) :
    2 * e ≤ m := by
  linarith

theorem cfg336_M_P1_CLS_alt_pass (m e : ℚ) (h1 : (3/400 : ℚ) ≤ m) (h2 : m ≤ (19/2500 : ℚ)) (h3 : (843/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_M31col_alt_pass (m e : ℚ) (h1 : (9/200 : ℚ) ≤ m) (h2 : m ≤ (451/10000 : ℚ)) (h3 : (823/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_M31lvd_alt_pass (m e : ℚ) (h1 : (117/5000 : ℚ) ≤ m) (h2 : m ≤ (47/2000 : ℚ)) (h3 : (361/5000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_LVfld_alt_pass (m e : ℚ) (h1 : (-621/10000 : ℚ) ≤ m) (h2 : m ≤ (-31/500 : ℚ)) (h3 : (733/10000 : ℚ) ≤ e) :
    -(2 * e) < m ∧ m < 2 * e := by
  constructor <;> linarith

theorem cfg336_M_P1_not_partial_canonical (m b : ℚ) (h1 : (649/2000 : ℚ) ≤ m) (h2 : b ≤ (1623/5000 : ℚ)) :
    b / 2 < m := by
  linarith

theorem cfg336_M_P1_not_partial_alt (m b : ℚ) (h1 : (761/2500 : ℚ) ≤ m) (h2 : b ≤ (609/2000 : ℚ)) :
    b / 2 < m := by
  linarith
