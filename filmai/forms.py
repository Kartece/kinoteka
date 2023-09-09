from .models import User, Profilis, AReview, Review,  FilmasInstance
from django import forms
from .models import Review


class FilmasReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'movie', 'reviewer')
        widgets = {  # paslepia laukus
            'movie': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }

class AktoriusReviewForm(forms.ModelForm):
    class Meta:
        model = AReview
        fields = ('aktorius', 'reviewer')
        widgets = {  # paslepia laukus
            'aktorius': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = 'date'


class UserFilmasCreateForm(forms.ModelForm):
    class Meta:
        model = FilmasInstance
        fields = ['filmas', 'reader', 'due_back']
        widgets = {'reader': forms.HiddenInput(),
                   'due_back': DateInput()
                   }

