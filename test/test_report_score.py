from .bases import PokemonSnapTestBase
from ..constants import REPORT_SCORE_130_000

class TestPoseSanity(PokemonSnapTestBase):
    options = { 
        'report_score_total': 'true',
    }

    def test_max_report_score_achievable(self):
        rule = self.multiworld.get_location(REPORT_SCORE_130_000, self.player).access_rule
        max_score = rule.achievable_total(self.multiworld.get_all_state())
        print(f'Max report score in logic: {max_score}')
        self.assertGreaterEqual(max_score, 250_000)