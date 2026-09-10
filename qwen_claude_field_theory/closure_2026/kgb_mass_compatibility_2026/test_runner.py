import subprocess
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

# Physics helpers add sibling research folders to sys.path. Bind THIS runner
# explicitly so a preceding physics test cannot select an older run_suite.py.
spec=importlib.util.spec_from_file_location('conformal_checkpoint_runner',Path(__file__).with_name('run_suite.py'))
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
run_case=runner.run_case


class RunnerFailureRecording(unittest.TestCase):
    def test_timeout_keeps_command_and_status(self):
        with patch.object(runner.subprocess,'run',side_effect=subprocess.TimeoutExpired(['python3'],300,output=b'partial')):
            record,out,err=run_case('bounded',['python3'],'.')
        self.assertEqual(record['exit_status'],124)
        self.assertEqual(record['argv'],['python3'])
        self.assertEqual(out,'partial')
        self.assertIn('TimeoutExpired',err)

    def test_launch_failure_keeps_command_and_status(self):
        with patch.object(runner.subprocess,'run',side_effect=FileNotFoundError('missing')):
            record,_,err=run_case('missing',['absent-command'],'.')
        self.assertEqual(record['exit_status'],127)
        self.assertIn('FileNotFoundError',err)

    def test_child_failure_not_changed_to_success(self):
        with patch.object(runner.subprocess,'run',return_value=subprocess.CompletedProcess(['cmd'],3,'','failure')):
            record,_,_=run_case('failed',['cmd'],'.')
        self.assertEqual(record['exit_status'],3)


if __name__=='__main__':unittest.main()
