from django import forms
from django.contrib.auth.models import User
from .models import Submission, UserProfile, Pertanyaan, Pilihan

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['link', 'pdf']

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['link'].required = False
        self.fields['pdf'].required = False

class KuisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pertanyaan_set = kwargs.pop('pertanyaan_set')
        super(KuisForm, self).__init__(*args, **kwargs)
        for i, pertanyaan in enumerate(pertanyaan_set):
            self.fields[f'pertanyaan_{i}'] = forms.ChoiceField(
                label=pertanyaan.teks,
                choices=[(pilihan.id, pilihan.teks) for pilihan in pertanyaan.pilihan_set.all()],
                widget=forms.RadioSelect,
                required=True
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['jenis_kelamin', 'tanggal_lahir', 'alamat', 'foto_profile']