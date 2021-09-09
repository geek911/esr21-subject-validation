from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import YES

from ..form_validators import SpecialInterestAERecordFormValidator
from .models import AdverseEvent, Appointment, SubjectVisit


class TestSpecialInterestAdverseEventFormValidator(TestCase):

    def setUp(self):
        subject_identifier = '1234567'
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1001')
        subject_visit = SubjectVisit.objects.create(
            appointment=appointment)
        adverse_event = AdverseEvent.objects.create(
            subject_visit=subject_visit,
            special_interest_ae=YES)
        self.aesi_options = {
            'adverse_event': adverse_event,
            'start_date': get_utcnow().date(),
            'date_aware_of': get_utcnow().date(),
            'aesi_category': 'cat',
            'rationale': 'blah',
            'describe_aesi_treatmnt': 'blahblah',
            'additional_info': 'additions'}

    def test_dt_aware_before_start_dt_invalid(self):
        """ Assert that the AESI aware date raises an error if date is before
            the AESI start date.
        """
        self.aesi_options.update(
            date_aware_of=get_utcnow().date() - relativedelta(days=2),)
        form_validator = SpecialInterestAERecordFormValidator(
            cleaned_data=self.aesi_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_aware_of', form_validator._errors)

    def test_dt_aware_after_start_dt_valid(self):
        """ Tests if the AESI aware date is after/equal to start date, cleaned
            data validates or fails the tests if the Validation Error is raised
            unexpectedly.
        """
        form_validator = SpecialInterestAERecordFormValidator(
            cleaned_data=self.aesi_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
