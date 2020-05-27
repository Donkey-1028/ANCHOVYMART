from django import forms

from .models import Rate

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate']

    def clean_rate(self):
        cd = self.cleaned_data['rate']
        if 1 > cd or cd > 5:
            print('11111111111111111111111111111111111111111')
            raise forms.ValidationError('평점 에러')
        return cd