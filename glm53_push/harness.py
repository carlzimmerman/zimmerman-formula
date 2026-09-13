"""GLM-5.3 push harness: same discipline as hermes_push/harness.py, paths=("glm53_push",)."""
import subprocess, sys

def commit_guard(paths=("glm53_push",)):
    """No personal data, no absolute machine paths, no literal-True checks."""
    pat = "|".join(["gm" + "ail", "/Us" + "ers/", r"check\([^,]*,\s*True\)", r"\bok\s*=\s*True\b"])
    bad = subprocess.run(["grep", "-rn", "-i", "-E", "--exclude=harness.py", pat, *paths],
                         capture_output=True, text=True).stdout
    if bad.strip():
        print("COMMIT GUARD FAILED:\n" + bad)
        sys.exit(1)
    print("commit guard ok")

if __name__ == "__main__":
    commit_guard()
