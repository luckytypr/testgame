from django.db.models import TextChoices


class DictionarableTextChoices(TextChoices):

    @classmethod
    def as_dict(cls):
        return {key: value for key, value in cls.choices}


class TournamentStages(DictionarableTextChoices):
    PREPARATION = "PREPARATION", "Preparation"
    GROUP_STAGE = "GROUP_STAGE", "Group Stage"
    QUARTER_FINAL = "QUARTER_FINAL", "Quarter Final"
    SEMI_FINAL = "SEMI_FINAL", "Semi Final"
    FINAL = "FINAL", "Final"



ADJECTIVES = [
    'familiar',
    'domineering',
    'lean',
    'absorbing',
    'probable',
    'significant',
    'frightening',
    'ludicrous',
    'imminent',
    'public',
    'mere',
    'abhorrent',
    'practical',
    'aboard',
    'highfalutin',
]

NOUNS = [
    'midnight',
    'society',
    'week',
    'employment',
    'entertainment',
    'emphasis',
    'sympathy',
    'contract',
    'device',
    'physics',
    'news',
    'dirt',
    'suggestion',
    'product',
    'presence',
]

CITIES = [
    'Almaty',
    'Nur-Sultan',
    'Shymkent',
    'Aktobe',
    'Karaganda',
    'Taraz',
    'Semey',
    'Pavlodar',
    'Oskemen',
    'Atyrau',
    'Kostanay',
    'Kyzylorda',
    'Uralsk',
    'Petropavl',
    'Aktau',
]

