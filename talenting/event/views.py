from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import EventForm
from .models import Event


def event_list(request):
    events = Event.objects.all()
    # comment_form = CommentForm()
    context = {
        'events': events,
        'comment_form': comment_form,
    }
    return render(request, context)


@login_required
def event_create(request):
    # if not request.user.is_authenticated:
    #     return ValueError('must login')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            return render(request)
    else:
        form = EventForm()

    context = {
        'form': form,
    }
    return render(request, context)


def event_detail(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    context = {
        'event': event,
    }
    return render(request, context)


@login_required
def event_delete(request, event_pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_pk)
        if event.author == request.user:
            event.delete()
            return HttpResponse('succeed')
        else:
            raise PermissionDenied('You have no permission to delete')


