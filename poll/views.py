from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from ems.decorators import admin_only
from poll.forms import PollForm, ChoiceForm
from poll.models import *

class PollView(View):
    decorators = [login_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(choice.id), instance=choice) for choice in choices]
            template = 'polls/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(4)]
            template = 'polls/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 4)]

        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.q = new_poll
                new_choice.save()
            return HttpResponseRedirect('/polls/list/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/edit_poll.html', context)

def poll_delete(request, id):
    u = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        u.delete()
        return HttpResponseRedirect(reverse('polls_list'))
    else:
        context = {}
        context['u'] = u
        return render(request, 'polls/delete.html', context)

@login_required(login_url="/login/")
def index(request):
    context = {}
    q = Question.objects.all()
    context['ques'] = q
    context['title'] = 'polls'
    return render(request, 'polls/index.html', context)

@login_required(login_url="/login/")
def details(request, id):
    context = {}
    try:
        qu = Question.objects.get(id=id)
    except:
        raise Http404
    context['quest'] = qu
    return render(request, 'polls/details.html', context)

@login_required(login_url="/login/")
def poll(request, id):
    if request.method == 'GET':
        context = {}
        try:
            qu = Question.objects.get(id=id)
        except:
            raise Http404
        context['quest'] = qu
        return render(request, 'polls/polls.html', context)
    if request.method == 'POST':
        ur_id = 22
        print(request.POST)
        d = request.POST
        ret = Answer.objects.create(u_id=ur_id, ch_id=d['choice'])
        context = {}
        context['title'] = 'Your Vote is Count Succesfully'
        if ret:
            return render(request, 'polls/re.html', context)
        else:
            return HttpResponse('Your vote is not count successfully')


