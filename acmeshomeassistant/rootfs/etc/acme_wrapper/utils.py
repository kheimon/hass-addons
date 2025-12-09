# acme.sHomeassistant - A homeassistant add-on wrapper for acme.sh
# Copyright (C) 2025  hupf

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging
import subprocess
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def ensure_path_or_str(value: str | Path) -> str:
    if isinstance(value, (Path, str)):
        return str(value)
    raise ValueError(f"Command contains invalid object {str(value)}! Only str and Path allowed!")

def normalize_command(cmd: list[str | Path]) -> list[str]:
    return [ensure_path_or_str(c) for c in cmd]

def log_output(stdout: str, stderr: str, success=True):
    for line in stdout.splitlines():
        if line.strip(): 
            logger.debug(line)
    for line in stderr.splitlines():
        if line.strip(): 
            logger.warning(line) if success else logger.critical(line)

def run_command(cmd: list[str | Path],
                env: dict[str, str] | None = None,
                ok_codes={0}):
    normalize_cmd = normalize_command(cmd)
    logger.debug("Executing: " + " ".join(normalize_cmd))
    result = subprocess.run(
        normalize_cmd,
        env=env,
        capture_output=True,
        text=True
    )
    success = result.returncode in ok_codes
    log_output(result.stdout, result.stderr, success)

    if not success:
        raise subprocess.CalledProcessError(
            result.returncode, normalize_cmd, result.stdout, result.stderr
        )

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno <= logging.INFO)
    stdout_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    if not root.handlers:
        root.addHandler(stdout_handler)
        root.addHandler(stderr_handler)