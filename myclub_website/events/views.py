from django.http import HttpRequest
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForms, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
# pdf lib
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# ends pdf lib

# pagination
from django.core.paginator import Paginator
from django.contrib import messages

# get the django's user model
from django.contrib.auth.models import User

from django.conf import settings


def venue_events(request: HttpRequest, venue_id):
    # print(f"Type: {type(venue_id)} venue id: {venue_id}")
    venue = Venue.objects.get(id=venue_id)

    venue_events = venue.event_set.all()

    # print('venue_events: ', venue_events)

    return render(request, 'events/venue_events.html', {
        'venue_name': venue.name,
        'venue_events': venue_events
    })


def admin_approval(request: HttpRequest):

    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    venue_list = Venue.objects.all()
    event_list = Event.objects.all().order_by('-event_date')

    if request.user.is_superuser:

        if request.method == 'POST':

            id_list = request.POST.getlist('boxes')
            # print(id_list)

            # uncheck all events
            event_list.update(approved=False)

            for id in id_list:
                # __________update database___________________________
                Event.objects.filter(pk=int(id)).update(approved=True)

            messages.success(request, 'Event are approved successfully!')
            return redirect('event-list')

        else:
            return render(request, 'events/admin_approval.html', {
                        'event_list': enumerate(event_list),
                        'event_count': event_count,
                        'venue_count': venue_count,
                        'user_count': user_count,
                        'venue_list': enumerate(venue_list)
                    })
      
    else:
        messages.success(request, 'You are not authorized to view this page.')
        return redirect('home')


def search_events(request: HttpRequest):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains=searched)

        return render(request, 'events/search_events.html', {
            'searched': searched,
            'events': events
        })
    else:
        return render(request, 'events/search_events.html')


def my_events(request: HttpRequest):

    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)

        return render(request, 'events/my_events.html', {
            'events': events
        })
    else:
        messages.success(request, "You are not authorized to view this page. \
                         Please login!")
        return redirect('home')
    

def venue_pdf(request: HttpRequest):
    # create byte stream buffer
    buf = io.BytesIO()
    # create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # add some lines of text
    venues = Venue.objects.all()
    lines = []
    for (indx, venue) in enumerate(venues):
        lines.append(str(indx+1))
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("==========================")

    # loop
    for line in lines:
        textob.textLine(line)

    # finishing up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # return response
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


def venue_csv(request: HttpRequest):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # create a csv writer
    writer = csv.writer(response)

    # designate the model
    venues = Venue.objects.all()

    # add column heading to csv file
    writer.writerow(['Venue name', 'Address', 'Zipcode', 'Phone',
                     'Web address', 'Email address'])

    # loop through the outputs
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code,
                         venue.phone, venue.web, venue.email_address])

    return response


def venue_text(request: HttpRequest):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # designate the model
    venues = Venue.objects.all()
    lines = []
    for (indx, venue) in enumerate(venues):
        lines.append(
            f"\n\n{indx + 1}. {venue.name}\n{venue.address}\
                \n{venue.zip_code}\n{venue.web}\n{venue.email_address}")

    # write to text files
    response.writelines(lines)
    return response


def delete_venue(request: HttpRequest, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()

    return redirect('venue-list')


def delete_event(request: HttpRequest, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event is deleted successfully!')
        return redirect('event-list')
    else:
        messages.success(request, 'You are not authorize to \
                         delete this events.')
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
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid:
                form.save()
                return redirect('event-list')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event_form = form.save(commit=False)
                event_form.manager = request.user
                event_form.save()
                return redirect('event-list')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
        if "submitted" in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {
        "form": form,
        "submitted": submitted
    })


def update_venue(request: HttpRequest, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_form = VenueForms(request.POST or None, request.FILES or None,
                            instance=venue)

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


def show_venue(request: HttpRequest, venue_id: int):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)

    events = venue.event_set.all()

    if request.method == 'POST':
        venue_image = request.POST.get('venue_image')
        Venue.objects.filter(pk=venue_id).update(
            venue_image=f"{settings.MEDIA_ROOT}/{venue_image}",
        )        
  
    return render(request, 'events/show_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner,
        'events': events
    })


def list_venues(request: HttpRequest):
    # order by randomly
    # ?
    # all_venues = Venue.objects.all().order_by('?')
    all_venues = Venue.objects.all()

    # setup pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages

    return render(request, 'events/venues.html', {
        'venue_list': all_venues,
        'venues': venues,
        'nums': nums
    })


def add_venue(request: HttpRequest):
    submitted = False

    if request.method == "POST":
        form = VenueForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add-venue?submitted=True')
    else:
        form = VenueForms()
        if "submitted" in request.GET:
            submitted = True

    forms = VenueForms()
    return render(request, 'events/add_venue.html', {
        "forms": forms,
        "submitted": submitted
    })


def all_events(request: HttpRequest):
    """event list"""
    event_list = Event.objects.all().order_by('-event_date')

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

    # Query the events model with dates
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=7
    )

    # get current time
    time = now.strftime('%I:%M %p')

    return render(request, 'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        "event_list": event_list
    })
