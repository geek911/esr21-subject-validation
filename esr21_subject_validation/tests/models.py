from django.db import models
from edc_base.model_mixins import BaseUuidModel, ListModelMixin


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class EligibilityConfirmation(BaseUuidModel):

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    age_in_years = age_in_years = models.IntegerField()


class InformedConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=50)

    gender = models.CharField(max_length=25)

    is_literate = models.CharField(max_length=25,
                                   blank=True,
                                   null=True)

    witness_name = models.CharField(max_length=25,
                                    blank=True,
                                    null=True)

    dob = models.DateField()

    consent_datetime = models.DateTimeField()

    version = models.CharField(
        max_length=10,
        editable=False)
