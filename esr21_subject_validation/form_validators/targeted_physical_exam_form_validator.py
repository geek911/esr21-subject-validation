from edc_constants.choices import YES, NO
from edc_form_validators import FormValidator


class TargetedPhysicalExamFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            NO,
            field='physical_exam_performed',
            field_required='reason_not_done')

        self.validate_physical_exam_performed()

        self.required_if(
            YES,
            field='abnormalities',
            field_required='if_abnormalities')

    def validate_physical_exam_performed(self):
        fields = ['area_performed', 'exam_date', 'abnormalities']
        for field in fields:
            self.required_if(
                YES,
                field='physical_exam_performed',
                field_required=field)
