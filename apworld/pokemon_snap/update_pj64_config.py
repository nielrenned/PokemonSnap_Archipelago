# Massive credit to Donkey Kong 64 Randomizer for figuring out PJ64 LUA support.
from configparser import ConfigParser
import uuid
from .constants import CLIENT_NAME
import Utils

from logging import getLogger
logger = getLogger(CLIENT_NAME)
pj64_encoding: str = "cp1252"

def safe_load_pj64_config():
    # Through some various controller setup testing, PJ64 does some weird formatting and sometimes
    #   pushes values to new lines. allow_no_value=True stops crashes on these corrupted/stray lines
    config: ConfigParser = ConfigParser(allow_no_value=True)
    config.optionxform = str # Forces output in the same format as the input in cfg
    config_updated: bool = False

    with open(pj64_cfg_path, 'r', encoding=pj64_encoding) as f:
        config.read_file(f)

    if "Basic Mode" not in config["Settings"]:
        config.set("Settings", "Basic Mode", "0")
        config_updated = True

    if "Debugger" not in config:
        config.add_section("Debugger")
        config.set("Debugger", "Debugger", "1")
        config.set("Debugger", "Autorun Scripts", "ap_pj64_adapter.js")
        port = str(40000 + (uuid.uuid4().int % 10000))
        config.set("Debugger", "ap_port", port)
        logger.info("Set port to " + str(port))
        config_updated = True

    if config_updated:
        try:
            with open(pj64_cfg_path, 'w', encoding=pj64_encoding) as f:
                config.write(f, space_around_delimiters=False)
            logger.info("Config successfully updated.")
        except Exception as e:
            logger.error("Error while updated PJ64 configuration. If this is your first time playing Pokemon Snap AP, "
                "you may need to close PJ64 and open the Pokemon Snap client first to update PJ64's settings file.")
            logger.error(f"Additional details about failure: {str(e)}")

if __name__ == "__main__":
    use_pj64 = True
    pj64_cfg_path = r"C:\Users\jackm\Desktop\PJ64\Config\Project64.cfg"
    safe_load_pj64_config()

else:
    from settings import get_settings, Settings

    options: Settings = get_settings()
    use_pj64: bool = bool(options["pokemon_snap_options"]["use_pj64"])
    pj64_cfg_path: str = str(options["pokemon_snap_options"]["emulator_settings"]["cfg_path"])
    if not pj64_cfg_path:
        pj64_cfg_path = Utils.user_path(pj64_cfg_path)