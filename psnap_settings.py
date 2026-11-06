from typing import Sequence, Any
import settings

class UseProject64(settings.Bool):
    """If this is set to False, Pokemon Snap launches in BizHawk instead."""
    description = ("Whether to use Project64 as the default emulator or not. By having this enabled, "
        "extra setup is required to enable communication between AP and PJ64.")

class Project64Executable(settings.UserFilePath):
    """The path for Project64 executable. If using Flatpak, specify this path instead."""
    description = "Project64 executable path"
    is_exe = True

class EmulatorSettings(settings.Group):
    """Project64 specific settings"""
    path: Project64Executable = Project64Executable(None)
    auto_start: bool = True

class SnapRomPath(settings.UserFilePath):
    """Locate your Pokemon Snap ROM path."""
    description = "Pokemon Snap ROM path"

    def browse(self, filetypes: Sequence[tuple[str, Sequence[str]]] | None = None, **kwargs: Any):
        if not filetypes:
            filetypes = [("N64 ROM", ["*.z64"]), ("File", ['*.*'])]
        return super().browse(filetypes, **kwargs)

class PokemonSnapSettings(settings.Group):
    rom_path: SnapRomPath = SnapRomPath(None)
    use_pj64: UseProject64 | bool = False
    emulator_settings: EmulatorSettings = EmulatorSettings()