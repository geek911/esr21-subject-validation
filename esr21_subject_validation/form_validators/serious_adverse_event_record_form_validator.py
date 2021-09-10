from django.core.exceptions import ValidationError
from edc_constants.constants import OTHER
from edc_form_validators import FormValidator


class SeriousAdverseEventRecordFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_date_aware_of(cleaned_data=cleaned_data)
        self.validate_hospitalization(cleaned_data=cleaned_data)
        self.validate_incapacity()
        self.validate_medical_event()

    def validate_date_aware_of(self, cleaned_data=None):
        date_aware_of = cleaned_data.get('date_aware_of')
        start_date = cleaned_data.get('start_date')
        if date_aware_of and date_aware_of < start_date:
            message = {'date_aware_of':
                       'The date investigator became aware of SAE can not be '
                       'before the start date.'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_hospitalization(self, cleaned_data=None):
        qs = cleaned_data.get('seriousness_criteria')
        if qs and qs.count() > 0:
            selected = {obj.short_name: obj.name for obj in qs}
            self.required_if_true(
                'hospitalization' in selected,
                field_required='admission_date',
                required_msg=('Seriousness criteria includes `Hospitalization`,'
                              ' specify date of admission.'))

        self.not_required_if(
            None,
            field='admission_date',
            field_required='discharge_date',
            not_required_msg=('Seriousness criteria does not include '
                              '`Hospitalization`, this field is not required.'),
            inverse=False)

        admission_date = cleaned_data.get('admission_date')
        discharge_date = cleaned_data.get('discharge_date')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('resolution_date')
        if admission_date:
            if admission_date < start_date:
                message = {'admission_date':
                           'Admission date cannot be before the SAE start date'}
                self._errors.update(message)
                raise ValidationError(message)
            if end_date and admission_date > end_date:
                message = {'admission_date':
                           'Admission date cannot be after the SAE end date'}
                self._errors.update(message)
                raise ValidationError(message)
        if discharge_date and discharge_date < admission_date:
            message = {'discharge_date':
                       'Discharge date cannot be before the admission date'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_incapacity(self):
        self.m2m_other_specify(
            'incapacity',
            m2m_field='seriousness_criteria',
            field_other='incapacity_specify')

    def validate_medical_event(self):
        self.m2m_other_specify(
            OTHER,
            m2m_field='seriousness_criteria',
            field_other='medical_event_other')
