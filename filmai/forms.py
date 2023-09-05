from .models import Filmas, User, Profilis, Review, FilmasInstance
from django import forms
from .models import Review


class FilmasReviewForm(forms.ModelForm):
    class Meta:
        model = Filmas
        fields = ('pavadinimas', 'aktoriusFK')
        widgets = {  # paslepia laukus
            'filmas': forms.HiddenInput(),
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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["author", "stars", "movie", "comment"]
