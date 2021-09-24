from edc_constants.choices import YES
from edc_form_validators import FormValidator


class PersonalContactInformationFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            YES,
            field='may_visit_home',
            field_required='physical_address')
        self.required_if(
            YES,
            field='may_call',
            field_required='subject_cell')
        self.validate_may_call_work()
        self.validate_may_contact_indirectly()

    def validate_may_call_work(self):
        fields = ['subject_work_place', 'subject_work_phone']

        for field in fields:
            self.required_if(
                YES,
                field='may_call_work',
                field_required=field)

    def validate_may_contact_indirectly(self):
        fields = ['indirect_contact_name',
                  'indirect_contact_relation',
                  'indirect_contact_physical_address',
                  'indirect_contact_cell', 'indirect_contact_phone']

        for field in fields:
            self.required_if(
                YES,
                field='may_contact_indirectly',
                field_required=field)
