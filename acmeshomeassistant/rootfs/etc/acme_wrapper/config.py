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
from pydantic import BaseModel, ValidationInfo, EmailStr, Field, field_validator
from typing import Literal
from pathlib import Path
import json

class EnvVar(BaseModel):
    name: str
    value: str

class Config(BaseModel):
    # Values supplied via JSON
    server: str | None
    accountemail: EmailStr
    dns: str
    dnsEnvVariables: list[EnvVar]
    keylength: Literal["2048","3072","4096","8192","ec-256","ec-384","ec-521"] | None = None
    domains: list[str] = Field(..., min_items=1)
    fullchainfile: str
    keyfile: str
    
    # Must _always_ be supplied via code, never via json
    base_ssl_dir: Path
    
    @property
    def domain_ssl_dir(self) -> Path:
        primary_domain = self.domains[0]
        sanitized_primary_domain = primary_domain.replace("*", "_wildcard_")
        domain_dir_name = sanitized_primary_domain + (f"+{str(len(self.domains)-1)}" if len(self.domains) > 1 else "")
        return (self.base_ssl_dir / domain_dir_name).resolve()
    
    @property
    def fullchain_path(self) -> Path:
        return (self.domain_ssl_dir / self.fullchainfile).resolve()
    
    @property
    def key_path(self) -> Path:
        return (self.domain_ssl_dir / self.keyfile).resolve()
    
    @field_validator("domains")
    def arent_paths(cls, domains: list[str]) -> list[str]:
        for domain in domains:
            if Path(domain).name != domain:
                raise ValueError(f"Domain {domain} is invalid!")
        return domains
    
    @field_validator("fullchainfile", "keyfile")
    def is_filename_only(cls, file_name: str, info: ValidationInfo) -> str:
        save_name = Path(file_name).name
        if (file_name != save_name):
            raise ValueError(f"{info.field_name} can't be a path and must be a filename! Got {file_name}")
        return save_name
    
    @field_validator("base_ssl_dir")
    def is_absolute_and_exists(cls, path: Path, info: ValidationInfo) -> Path:
        if not path.is_absolute():
            raise ValueError(f"{info.field_name} must be an absolute path! Got {path}")
        if not path.exists():
            raise ValueError(f"{info.field_name} must exist!")
        if not path.is_dir():
            raise ValueError(f"{info.field_name} must be a directory!")
        return path

def load_config(config_path: Path, base_ssl_dir: Path) -> Config:
    with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    return Config(**config, base_ssl_dir=base_ssl_dir)

__all__ = ["load_config", "EnvVar"]