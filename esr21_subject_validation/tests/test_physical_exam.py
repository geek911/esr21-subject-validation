

from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO, YES
import datetime

from ..form_validators import PhysicalFormValidator


class TestPhysicalExamForm(TestCase):



    def test_exam_check_required(self):
        data = {
            'physical_exam': NO
        }
        form = PhysicalFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)


    def test_checks_description_invalid(self):

        data = {
            'abnormalities_found': YES
        }
        form = PhysicalFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)

    def test_for_checks_if_abnormal_then_description_is_required(self):

        data_check1 = { 'general_appearance': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check1)
        self.assertRaises(ValidationError, form.validate)

        data_check2 = { 'face_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check2)
        self.assertRaises(ValidationError, form.validate)
        
        data_check3 = { 'neck_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check3)
        self.assertRaises(ValidationError, form.validate)

        data_check4 = { 'respiratory_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check4)
        self.assertRaises(ValidationError, form.validate)

        data_check5 = { 'cardiovascular_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check5)
        self.assertRaises(ValidationError, form.validate)

        data_check6 = { 'abdominal_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check6)
        self.assertRaises(ValidationError, form.validate)

        data_check7 = { 'skin_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check7)
        self.assertRaises(ValidationError, form.validate)

        data_check8 = { 'neurological_check': 'abnormal'}
        form = PhysicalFormValidator(cleaned_data=data_check8)
        self.assertRaises(ValidationError, form.validate)


