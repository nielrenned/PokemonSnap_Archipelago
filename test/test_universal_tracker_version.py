
from .bases import PokemonSnapTestBase
from ..client import _has_invalid_universal_tracker, PokemonSnapContext

class TestSparseLocationGeneration(PokemonSnapTestBase):

    def test_minimum_unit_version(self):

        invalid_versions = [ "v2.11.11.11","wre.121","30.0.0.0", "3", "0.0.0", "v0.2.10"]
        valid_versions = [ "v2.11.11", "v3.0.0", "0.25.120202", PokemonSnapContext.min_universal_tracker_version]

        for invalid_version in invalid_versions:
            if not _has_invalid_universal_tracker(invalid_version):
                self.fail(f" Incorrectly flagged Invalid version: {invalid_version}")

        for valid_version in valid_versions:
            if _has_invalid_universal_tracker(valid_version):
                self.fail(f" Incorrectly flagged Invalid version: {valid_version}")