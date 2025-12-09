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
import shutil
import logging
from pathlib import Path
from pydantic import EmailStr
from utils import run_command
from enum import IntEnum

logger = logging.getLogger(__name__)

class AcmeClient():
    binary_name = "acme.sh"
    
    class IssueResultCode(IntEnum):
        OK = 0
        RENEWAL_SKIPPED = 2
    
    def __init__(self, config_path: Path):
        file = shutil.which(self.binary_name)
        if not file:
            raise FileNotFoundError(f"{self.binary_name} binary not found!")
        
        self.bin = Path(file)
        self.config_path = config_path

    @property
    def base_args(self) -> list[str | Path]:
        return ["--config-home", self.config_path]
    
    def enable_auto_upgrade(self):
        logger.info("Configuring Auto Upgrade...")
        cmd = [self.bin, "--upgrade", "--auto-upgrade"] \
            + self.base_args
        run_command(cmd)
        
    def enable_cronjob(self):
        logger.info("Installing acme.sh cron job...")
        cmd = [self.bin] \
            + ["--install-cronjob"] \
            + self.base_args
        run_command(cmd)
    
    def register(self, accountemail: EmailStr, server: str | None):
        logger.info("Registering account...")
        cmd = [self.bin] \
            + ["--register-account", "-m", accountemail] \
            + (["--server", server] if server is not None else []) \
            + self.base_args
        run_command(cmd)
    
    def issue(
        self,
        domains: list[str],
        keylength: str | None,
        server: str | None,
        dns: str,
        dns_env_vars: dict[str, str] | None,
    ):
        logger.info(f"Issuing certificate for domain(s): {domains}...")
        domain_args = [item for d in domains for item in ("--domain", d)]
        cmd = [self.bin, "--issue"] \
            + domain_args \
            + (["--keylength", keylength] if keylength else []) \
            + ["--dns", dns] \
            + (["--server", server] if server is not None else []) \
            + self.base_args
        ok_codes = {self.IssueResultCode.OK, self.IssueResultCode.RENEWAL_SKIPPED}
        run_command(cmd, dns_env_vars, ok_codes)
    
    def install(self, domains: list[str], keylength: str | None, key_file: Path, fullchain_file: Path):
        logger.info(f"Installing certificate to: {fullchain_file} and keyfile to {key_file}...")
        cmd = [self.bin, "--install-cert"] \
            + ["--domain", domains[0]] \
            + (["--ecc"] if keylength and keylength.startswith("ec-") else []) \
            + ["--key-file", key_file] \
            + ["--fullchain-file", fullchain_file] \
            + self.base_args
        run_command(cmd)

__all__ = ["AcmeClient"]
