import os
import tempfile
import subprocess
import textwrap
import shutil

IMAGE_NAME = "python:3.11-slim"
EXEC_TIMEOUT_SECONDS = 10
MEMORY_LIMIT = "128m"
NETWORK_MODE = "none"


def _docker_available() -> bool:
    return shutil.which("docker") is not None


def run_code_in_docker(code: str) -> tuple[str, int]:
    code = textwrap.dedent(code)

    if not _docker_available():
        return "Docker is not installed or not available in PATH.", -1

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "script.py")

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        docker_cmd = [
            "docker", "run", "--rm",
            f"--memory={MEMORY_LIMIT}",
            "--network", NETWORK_MODE,
            "-v", f"{tmpdir}:/app:ro",
            IMAGE_NAME,
            "python", "/app/script.py"
        ]

        try:
            proc = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=EXEC_TIMEOUT_SECONDS
            )
        except subprocess.TimeoutExpired:
            return f"Execution timed out after {EXEC_TIMEOUT_SECONDS} seconds.", -2
        except Exception as e:
            return f"Internal error: {e}", -1

        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        combined = (stdout + "\n" + stderr).strip()

        if proc.returncode != 0:
            low = combined.lower()
            if "killed" in low or "out of memory" in low:
                return "Execution failed: container was killed due to excessive memory usage.", proc.returncode

            return combined, proc.returncode

        return stdout.strip(), proc.returncode