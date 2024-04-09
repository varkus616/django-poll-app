from django.shortcuts import render

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
from django.shortcuts import render


from django.views import generic
from django.shortcuts import render, redirect
from .forms import PollForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

    def post(self, request, *args, **kwargs):
        form = PollForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("polls:index"))
        else:

            context = {'form':form}
            return self.render_to_response(context)


class PollsList(generic.ListView):
    model = Question
    template_name = "polls/polls_list.html"

    def get_queryset(self):
        return Question.objects.order_by("id")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

