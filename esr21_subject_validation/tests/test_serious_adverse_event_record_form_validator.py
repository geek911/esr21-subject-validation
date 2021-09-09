from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, YES, OTHER

from ..form_validators import SeriousAdverseEventRecordFormValidator
from .models import AdverseEvent, Appointment, SubjectVisit, ListModel


class TestSeriousAdverseEventRecordFormValidator(TestCase):

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
            serious_event=YES)
        ListModel.objects.create(name='life_threatening')
        self.sae_options = {
            'adverse_event': adverse_event,
            'start_date': get_utcnow().date(),
            'status': 'ongoing',
            'date_aware_of': get_utcnow().date(),
            'seriousness_criteria': ListModel.objects.all(),
            'rationale': 'blah',
            'event_abate': NO,
            'event_reappear': NO,
            'describe_sae_treatmnt': 'blahblah',
            'test_performed': 'a bunch of tests',
            'additional_info': 'additions'}

    def test_dt_aware_before_start_dt_invalid(self):
        """ Assert that the SAE aware date raises an error if date is before
            the SAE start date.
        """
        self.sae_options.update(
            date_aware_of=get_utcnow().date() - relativedelta(days=2),)
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_aware_of', form_validator._errors)

    def test_dt_aware_after_start_dt_valid(self):
        """ Tests if the SAE aware date is after/equal to start date, cleaned
            data validates or fails the tests if the Validation Error is raised
            unexpectedly.
        """
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_admission_dt_specified_not_hosp(self):
        """ Assert that the SAE admission date raises an error if seriousness
            criteria is not hospitalization but admission date provided.
        """
        self.sae_options.update(admission_date=get_utcnow().date())
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('admission_date', form_validator._errors)

    def test_hospitalisation_admission_dt_missing(self):
        """ Assert that the SAE admission date raises an error if seriousness
            criteria is hospitalization but admission date missing.
        """
        ListModel.objects.create(name='hospitalization')
        self.sae_options.update(
            seriousness_criteria=ListModel.objects.all(),
            admission_date=None)
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('admission_date', form_validator._errors)

    def test_hospitalisation_admission_dt_specified(self):
        """ Tests if seriousness criteria is hospitalization and admission date
            is provided, cleaned data validates or fails the tests if the
            Validation Error is raised unexpectedly.
        """
        ListModel.objects.create(name='hospitalization')
        self.sae_options.update(
            seriousness_criteria=ListModel.objects.all(),
            admission_date=get_utcnow().date())
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_discharged_dt_admission_dt_missing(self):
        """ Assert that the SAE discharge date raises an error if date of admission
            is missing but admission date missing.
        """
        self.sae_options.update(
            admission_date=None,
            discharge_date=get_utcnow().date())
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('discharge_date', form_validator._errors)

    def test_admission_dt_within_start_end_dt(self):
        """ Assert that the SAE admission date raises an error if date is outside
            the bound of start ≤ dt ≤ end but admission date missing.
        """
        ListModel.objects.create(name='hospitalization')
        self.sae_options.update(
            start_date=get_utcnow().date() - relativedelta(days=2),
            admission_date=get_utcnow().date() - relativedelta(days=5))
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('admission_date', form_validator._errors)

    def test_incapacity_specify_required(self):
        """ Assert that the SAE incapacity specify raises an error if seriousness
            criteria includes incapacity, but not specified.
        """
        ListModel.objects.create(name='incapacity')
        self.sae_options.update(
            seriousness_criteria=ListModel.objects.all(),
            incapacity_specify=None)
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('incapacity_specify', form_validator._errors)

    def test_incapacity_specify_valid(self):
        """ Tests if seriousness criteria includes incapacity and incapacity
            is specified, cleaned data validates or fails the tests if the
            Validation Error is raised unexpectedly.
        """
        ListModel.objects.create(name='incapacity')
        self.sae_options.update(
            seriousness_criteria=ListModel.objects.all(),
            incapacity_specify='blah')
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_medical_event_specify_required(self):
        """ Assert that the SAE incapacity specify raises an error if seriousness
            criteria includes other medical event, but not specified.
        """
        ListModel.objects.create(name=OTHER)
        self.sae_options.update(
            seriousness_criteria=ListModel.objects.all(),
            medical_event_other=None)
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('medical_event_other', form_validator._errors)

    def test_medical_event_specify_valid(self):
        """ Tests if seriousness criteria includes other medical event and
            medical event is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """
        ListModel.objects.create(name=OTHER)
        self.sae_options.update(
            seriousness_criteria=ListModel.objects.all(),
            medical_event_other='blah')
        form_validator = SeriousAdverseEventRecordFormValidator(
            cleaned_data=self.sae_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
