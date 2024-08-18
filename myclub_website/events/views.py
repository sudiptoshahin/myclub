from django.http import HttpRequest
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForms, EventForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def delete_venue(request: HttpRequest, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()

    return redirect('venue-list')

def delete_event(request: HttpRequest, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()

    return redirect('event-list')

def update_event(request: HttpRequest, event_id):
    event = Event.objects.get(pk=event_id)
    event_form = EventForm(request.POST or None, instance=event)

    if event_form.is_valid():
        event_form.save()
        return redirect('event-list')

    return render(request, 'events/update_event.html', {
        'event': event,
        'event_form': event_form
    })

def add_event(request: HttpRequest):
    submitted = False

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
        if "submitted" in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', { "form": form, "submitted": submitted })

def update_venue(request: HttpRequest, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_form = VenueForms(request.POST or None, instance=venue)

    if venue_form.is_valid():
        venue_form.save()
        return redirect('list_venues')

    return render(request, 'events/update_venue.html', {
        'venue': venue,
        'venue_form': venue_form
    })


def search_venues(request: HttpRequest):
    
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venues.html', {
            'searched': searched,
            'venues': venues
        })
    else:
        return render(request, 'events/search_venues.html')

def show_venue(requet: HttpRequest, venue_id: int):
    venue = Venue.objects.get(pk=venue_id)

    return render(requet, 'events/show_venue.html', {
        'venue': venue
    })


def list_venues(request: HttpRequest):
    # order by randomly
    # ?
    all_venues = Venue.objects.all().order_by('-id')
    
    return render(request, 'events/venues.html', {
        'venue_list': all_venues
    })

def add_venue(request: HttpRequest):
    submitted = False

    if request.method == "POST":
        form = VenueForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add-venue?submitted=True')
    else:
        form = VenueForms()
        if "submitted" in request.GET:
            submitted = True

    forms = VenueForms()
    return render(request, 'events/add_venue.html', { "forms": forms, "submitted": submitted })

def all_events(request: HttpRequest):
    """event list"""
    event_list = Event.objects.all().order_by('event_date')

    return render(request, 'events/event_list.html', {
        "event_list": event_list
    })


def home(request: HttpRequest, year=datetime.now().year, 
         month=datetime.now().strftime('%B')):
    """
        {} -> is a context dictionary
              pass data from backend to frontend
    """
    name = "Sudipto Shahin"
    month = month.capitalize()
    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # get current year
    now = datetime.now()
    current_year = now.year

    # get current time
    time = now.strftime('%I:%M %p')

    return render(request, 'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time
    })
