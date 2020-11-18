from django.db.models import TextChoices


class Divisions(TextChoices):
    NOT_ASSIGNED = "NOT_ASSIGNED", "Not assigned"
    FIRST_DIVISION = "FIRST_DIVISION", "First Division"
    SECOND_DIVISION = "SECOND_DIVISION", "Second Division"