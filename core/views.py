from django.shortcuts import render
from django.db.models.query import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from core.forms import WorkerForm, WorkerCreationForm
from core.models import Worker
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login


def index(request: WSGIRequest, superior_id: int = -1):
    subordinates: QuerySet[Worker] = Worker.objects.filter(superior_id=superior_id)
    if not subordinates:
        ceo: Worker = Worker.objects.get(position=Worker.Position.CEO)
        subordinates: QuerySet[Worker] = Worker.objects.filter(superior_id=ceo.id)
    if 'search' in request.GET:
        limit = int(request.GET['amount'])
        q = Q(first_name__contains=request.GET['search']) \
            | Q(last_name__contains=request.GET['search']) \
            | Q(salary__contains=request.GET['search'])
        subordinates = Worker.objects.filter(q)[:limit]

    context: dict = {
        'subordinates': subordinates,
        'Position': Worker.Position,
        'fields': ('First', 'Last', 'Position', 'Salary', 'Superior')
    }

    return render(request, 'core/index.html', context=context)


def edit_worker(request: WSGIRequest):
    worker = WorkerForm()
    context: dict = {
        'WorkerForm': worker,
    }
    return render(request, 'core/edit.html', context=context)


class SignUpView(generic.CreateView):
    form_class = WorkerCreationForm
    success_url = reverse_lazy('main')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
