"""Wraps the rrrocket CLI (Rust/boxcars) to turn a .replay file into parsed JSON."""

import json
import subprocess
from pathlib import Path

RRROCKET_EXE = Path(__file__).resolve().parent.parent / "tools" / "rrrocket.exe"


def parse_replay(replay_path: str | Path, network: bool = True) -> dict:
    """Run rrrocket on a single .replay file and return the parsed JSON as a dict.

    network=True includes per-frame actor telemetry (position, rotation,
    velocity, etc). Without it you only get header metadata (score, players).
    """
    replay_path = Path(replay_path)
    if not replay_path.exists():
        raise FileNotFoundError(replay_path)
    if not RRROCKET_EXE.exists():
        raise FileNotFoundError(f"rrrocket binary not found at {RRROCKET_EXE}")

    args = [str(RRROCKET_EXE)]
    if network:
        args.append("--network-parse")
    args.append(str(replay_path))

    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"rrrocket failed ({result.returncode}): {result.stderr}")

    return json.loads(result.stdout)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m rl_coach.parse <path-to-.replay>")
        sys.exit(1)

    data = parse_replay(sys.argv[1])
    print(json.dumps(list(data.keys())))
