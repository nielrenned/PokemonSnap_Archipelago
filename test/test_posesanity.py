from .bases import PokemonSnapTestBase
from ..options import PoseSanity

class TestPoseSanity(PokemonSnapTestBase):
    options = { 
        'posesanity': PoseSanity.range_end,
        'hard_checks': 'true',
        'rng_checks': 'true',
    }