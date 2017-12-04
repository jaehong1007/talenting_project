from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView

from .forms import EventForm, CommentForm, ImageFieldForm
from .models import Event


def event_list(request):
    events = Event.objects.all()
    comment_form = CommentForm()
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


@login_required()
def event_participate_toggle(request, event_pk):
    if request.method == 'POST':
        # event_pk에 해당하는 Event객체
        event = get_object_or_404(Event, pk=event_pk)
        # 요청한 사용자
        user = request.user
        # events 목록에서 참여 할 유저가 있는지 확인
        filtered_event_participate = event.event_participate.filter(pk=user.pk)
        # 존재할경우, 목록에서 해당 유저를 삭제
        if filtered_event_participate.exists():
            event.event_participate.remove(user)
        # 없을 경우, like_posts목록에 해당 Post를 추가
        else:
            event.event_participate.add(user)

        # 이동할 path가 존재할 경우 해당 위치로, 없을 경우 Post상세페이지로 이동

        return redirect('post:post_detail', event_pk=event_pk)


