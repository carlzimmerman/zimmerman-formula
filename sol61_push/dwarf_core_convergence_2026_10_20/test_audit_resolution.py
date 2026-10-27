"""Admission-audit regressions using complete, tiny saved-record fixtures."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

import audit_resolution as audit


def write_case(root, name="complete", internal_work=0., host_work=0.):
    folder = root / ("run_" + name)
    folder.mkdir()
    (folder / "manifest.json").write_text(json.dumps({"run": {"status": "completed"}}))
    x = np.column_stack((np.arange(9.) * 5., np.zeros((9, 2))))
    v = np.zeros_like(x)
    m = np.ones(9)
    cold = np.arange(9) < 8
    for epoch in ("initial", "final"):
        np.savez(folder / (epoch + ".npz"), x=x, v=v, m=m, cold=cold)
    np.savez(folder / "trajectory.npz", time_Myr=[0., 100.],
             x=np.array([x, x]), v=np.array([v, v]))
    row = dict(centre=[0., 0., 0.], M100=8., M300=8.,
               conservation=dict(Eint=0., Jint=[0., 0., 0.]))
    result = dict(args=dict(ncold=8, duration=100., record_interval=100.,
                            collisionless=True, backend="cpu"),
                  maxima=dict(E=0., internal_work=internal_work, host_work=host_work,
                              Jint=0., Jorb=0., Jtotal=0., P=0.),
                  energy_scale=1., J_scale=1., collisions=0,
                  collision_energy_defect=0., collision_J_defect=[0., 0., 0.],
                  host_work_particle_sum_residual=0., host_torque_particle_sum_residual=[0., 0., 0.],
                  fixed_membership_groups={"all": dict(delta_E=0., delta_J=[0., 0., 0.])},
                  snapshots=[dict(row, time_Myr=0.), dict(row, time_Myr=100.)])
    (folder / "results.json").write_text(json.dumps(result))
    return folder


class AuditTests(unittest.TestCase):
    def run_main(self, root, output):
        args = argparse.Namespace(output=str(output), case=None, include_pilots=False)
        with patch.object(audit, "HERE", root), contextlib.redirect_stdout(io.StringIO()):
            audit.main(args)
        return json.loads((output / "audit.json").read_text())

    def test_default_discovers_completed_manifests_and_skips_active(self):
        # Removing the completion filter must try to open the absent active results.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_case(root)
            active = root / "run_active"
            active.mkdir()
            (active / "manifest.json").write_text(json.dumps({"run": {"status": "running"}}))
            result = self.run_main(root, root / "audit")
            self.assertEqual(set(result["cases"]), {"complete"})
            self.assertEqual(result["completed_case_count"], 1)
            self.assertTrue(result["all_checks_pass"])

    def test_no_completed_cases_cannot_report_success(self):
        # Replacing the nonempty admission rule by all([]) would make this fail.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_main(root, root / "audit")
            self.assertEqual(result["completed_case_count"], 0)
            self.assertFalse(result["all_checks_pass"])
            self.assertEqual(result["status"], "inconclusive_no_completed_cases")

    def test_receipt_energy_defects_fail_even_when_total_energy_and_partitions_pass(self):
        # Omitting either independent host-work closure gate would admit its bad fixture.
        for field, check in [("internal_work", "internal_energy_host_work_gate_0p1_percent"),
                             ("host_work", "host_potential_work_gate_0p1_percent")]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                folder = write_case(Path(directory), **{field: .001001})
                result = audit.audit_case(folder)
                self.assertIn(check, result["failed"])
                self.assertFalse(result["all_checks_pass"])

    def test_receipt_gate_includes_threshold_in_initial_dwarf_energy_units(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = write_case(Path(directory), internal_work=.001, host_work=.001)
            result = audit.audit_case(folder)
            checks = {entry["name"]: entry["passed"] for entry in result["checks"]}
            self.assertTrue(checks.get("internal_energy_host_work_gate_0p1_percent", False))
            self.assertTrue(checks.get("host_potential_work_gate_0p1_percent", False))
            self.assertTrue(result["all_checks_pass"])


if __name__ == "__main__":
    unittest.main()
