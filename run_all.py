"""Execute all four examples from any working directory."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
if __name__ == "__main__":
    for script in ("gas", "packed_bed", "brake", "rainfall"):
        subprocess.run([sys.executable, str(ROOT/"code"/f"{script}.py")], cwd=ROOT, check=True)
