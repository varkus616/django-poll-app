# forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Question, Choice

from django.utils import timezone


class PollForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)

        question_text = self.data.get('question_text')
        num_choices = int(self.data.get('Number-of-choices', 0))

        if question_text:
            self.fields['question_text'] = forms.CharField(
                label="Question Text",
                initial=question_text
            )

        for i in range(1, num_choices + 1):
            choice_text = self.data.get(f"choice{i}_text")
            if choice_text:
                self.fields[f"choice{i}_text"] = forms.CharField(
                    label=f"Choice {i}",
                    initial=choice_text
                )

    def clean(self):
        cleaned_data = super().clean()
        question_text = cleaned_data.get('question_text')
        choices = [cleaned_data.get(f'choice{i}_text') for i in range(1, len(self.fields)) if
                   cleaned_data.get(f'choice{i}_text')]

        if not question_text:
            raise ValidationError("Please eneter a question")

        if len(choices) < 1:
            raise ValidationError("Please eneter all choices")

        return cleaned_data

    def save(self):
        question_text = self.cleaned_data.get('question_text')

        if question_text:
            question = Question.objects.create(question_text=question_text,
                                               pub_date=timezone.now())

            num_choices = int(self.data.get('Number-of-choices', 0))
            for i in range(1, num_choices + 1):
                choice_text = self.cleaned_data.get(f"choice{i}_text")
                if choice_text:
                    Choice.objects.create(question=question,
                                          choice_text=choice_text,
                                          votes=0)
