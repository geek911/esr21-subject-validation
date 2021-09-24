from dateutil.relativedelta import relativedelta
from edc_constants.choices import YES
from edc_form_validators import FormValidator
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, POS, NEG, IND


class RapidHivTestingFormValidator(FormValidator):

    def clean(self):
        super().clean()
        self.applicable_if(
            YES,
            field='hiv_testing_consent',
            field_applicable='prev_hiv_test',)
        

        self.not_required_if(
            NO,
            field='hiv_testing_consent',
            field_required='rapid_test_done',
            inverse=False
        )

        prev_hiv_fields = ['hiv_test_date', 'hiv_result', 'evidence_hiv_status']

        for field in prev_hiv_fields:
            self.required_if(
                YES,
                field='prev_hiv_test',
                field_required=field
            )

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='rapid_test_date')

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='rapid_test_result')

        if (self.cleaned_data.get('hiv_result') and self.cleaned_data.get('hiv_result') != POS
                and self.cleaned_data.get('rapid_test_done') != YES):
            message = {'rapid_test_done': 'Rapid test must be performed '}
            raise ValidationError(message)
        elif (self.cleaned_data.get('hiv_result') and self.cleaned_data.get('hiv_result') == POS
                and self.cleaned_data.get('rapid_test_done') == YES):
            message = {'rapid_test_done': 'Participant is HIV positive, rapid test is not required'}
            raise ValidationError(message)
        
        if (self.cleaned_data.get('prev_hiv_test') == NO
                and self.cleaned_data.get('rapid_test_done') == NO):
            message = {'rapid_test_done': 'Rapid test must be performed if participant has no '
                                        'previous hiv results.'}
            raise ValidationError(message)
