from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, YES, OTHER

from ..form_validators import PregnancyTestFormValidator


class TestPregnencyTestFormValidator(TestCase):

    def test_result_invalid(self):
        data = {
            'preg_performed': YES
        }

        form = PregnancyTestFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)
