from django import forms
from.models import Fee
class FeeForm(forms.ModelForm):
    class Meta:
        model=Fee
        fields=['member','fee_month','fee_amount','fee_deposit_date']