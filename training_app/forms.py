from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'minutes_played', 'training_load', 'prev_injuries', 'age']
        labels = {
            'name': 'اسم اللاعب',
            'minutes_played': 'دقائق اللعب',
            'training_load': 'الأحمال التدريبية',
            'prev_injuries': 'إصابات سابقة',
            'age': 'العمر'
        }
