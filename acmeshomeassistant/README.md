# Acme.sHomeassistant Add-on
Wrapper add-on for [acme.sh](https://acme.sh) written mostly in Python. 
Licensed under the GNU General Public License v3.0 (GPLv3). See [LICENSE](https://codeberg.org/hupf/homeassistant-addons/src/branch/main/acmeshomeassistant/LICENSE) for details.

## Features
- Mutliple DNS Api's are supported. Check the [acme.sh wiki](https://github.com/acmesh-official/acme.sh/wiki/dnsapi) for more information
- Multi domain certificates and wildcard certificates are supported 
- The wrapper supports auto-renewal of certificates
- The certificates and keys are installed in `/ssl/<your_domain_name>/` (wildcards and multi domains differ slightly in naming conventions. Simply look at the contente of `/ssl` if you are unsure about this path)

## Installation
Follow these steps install the add-on on your homeassistant instance:
1. In Homeassistant navigate to **Settings** -> **Add-ons** -> **Add-on Store** -> **Repositories**
2. Add the repository: `https://codeberg.org/hupf/homeassistant-addons`
3. Seach acme.sHomeassistant add-on
4. Click on the **Install** button.
5. Set Add-on configuration
6. Start the add-on
7. Chrck the logd for wny unexpected error
8. Configure autostart + watchdog + autoupdate to your personal preferences.

## Configuartion
See [DOCS.md](https://codeberg.org/hupf/homeassistant-addons/src/branch/main/acmeshomeassistant/DOCS.md) for more details.

## Thanks
This project was heavily inspired by Angoll's [acme.sh-homeassistant-addon](https://github.com/Angoll/acme.sh-homeassistant-addon).  
In fact, it's a Python reimplementation of the acme.sh wrapper with config and path validation (via [pydantic](https://docs.pydantic.dev/latest/) and pathlib), updated dependencies and support for SAN certificates.