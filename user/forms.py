from django import forms
from .models import *
from account.forms import FormSettings


class PersonForm(FormSettings):
    class Meta:
        model = Person
        fields = ['phone']


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_score']


class CandidateForm(FormSettings):
    class Meta:
        model = Products
        fields = ['fullname', 'position', 'photo']
