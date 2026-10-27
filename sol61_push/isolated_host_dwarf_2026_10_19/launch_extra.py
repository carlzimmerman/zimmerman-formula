"""Additional diagnostic precision check; v1 scientific inputs stay immutable."""
import sys
import launch

launch.INPUT_NAMES=launch.INPUT_NAMES+['launch_extra.py']
launch.CASES['eps_iso']=['--dt','1','--eps','20']

if __name__=='__main__':
    for name in sys.argv[1:]:
        if name!='eps_iso':
            raise ValueError('Only the declared isolated softening check is allowed')
        rc=launch.launch(name)
        if rc:
            raise SystemExit(rc)
