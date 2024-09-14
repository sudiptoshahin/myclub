from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# create event forms
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'description',
                  'attendees')

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM',
            'venue': '',
            'manager': 'Manager',
            'description': '',
            'attendees': 'Attendees'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Event name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Event date'}),
            'venue': forms.Select(attrs={'class': 'form-control',
                                         'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-control',
                                           'placeholder': 'Manager'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control',
                                                     'placeholder': 'Attendees'})
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'description', 'attendees')

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM',
            'venue': '',
            'description': '',
            'attendees': 'Attendees'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Event name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Event date'}),
            'venue': forms.Select(attrs={'class': 'form-control',
                                         'placeholder': 'Venue'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Description'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control',
                                                     'placeholder': 'Attendees'})
        }


# create venue froms
class VenueForms(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__"
        fields = ("name", "address", "zip_code", "phone", "web",
                  "email_address", "venue_image")

        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            "venue_image": ''
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Venue name'
                }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address'}),

            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zip code'
                }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone'}),

            'web': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Web'}),

            'email_address': forms.EmailInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Email address'})
        }
