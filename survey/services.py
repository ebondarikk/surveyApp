import datetime

from django.db import transaction

from . import models
from . import validators


def get_instances_to_delete(instances, data):
    return instances.exclude(id__in=list(map(lambda i: i.get("id"), data)))


class Option:
    def create(self, data):
        data.pop("id", None)
        return models.Option.objects.create(**data)

    def create_set(self, question, data):
        for option_data in data:
            option_data["question"] = question
            self.create(option_data)

    def update(self, option, data):
        for field in data:
            setattr(option, field, data[field])
        option.save()
        return option

    def update_set(self, question, data):
        option_set = question.options.all()
        with transaction.atomic():
            get_instances_to_delete(option_set, data).delete()
            self._update_or_create_set(question, data)

    def _update_or_create_set(self, question, data):
        for option_data in data:
            option_data["question"] = question
            option = question.options.filter(id=option_data.pop("id", -1)).first()
            if option:
                self.update(option, option_data)
            else:
                self.create(option_data)


class Question:
    def validate(self, attrs):
        if attrs.get("type") != models.Question.TEXT:
            validators.validate_question_options(attrs)
        else:
            attrs.pop("options", None)
        return attrs

    def create(self, data):
        options_data = data.pop("options", [])
        data.pop("id", None)
        with transaction.atomic():
            question = models.Question.objects.create(**data)
            Option().create_set(question, options_data)
        return question

    def create_set(self, survey, data):
        for question_data in data:
            question_data["survey"] = survey
            self.create(question_data)

    def update(self, question, data):
        options_data = data.pop("options", [])
        for field in data.keys():
            setattr(question, field, data[field])
        question.save()
        Option().update_set(question, options_data)
        return question

    def update_set(self, survey, data):
        question_set = survey.questions.all()
        with transaction.atomic():
            get_instances_to_delete(question_set, data).delete()
            self._update_or_create_set(survey, data)

    def _update_or_create_set(self, survey, data):
        for question_data in data:
            question_data["survey"] = survey
            question = survey.questions.filter(id=question_data.pop("id", -1)).first()
            if question:
                self.update(question, question_data)
            else:
                self.create(question_data)


class Survey:
    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        with transaction.atomic():
            survey = super().create(validated_data)
            Question().create_set(survey, questions_data)
        return survey

    def update(self, survey, validated_data):
        questions_data = validated_data.pop("questions", [])
        with transaction.atomic():
            survey = super().update(survey, validated_data)
            Question().update_set(survey, questions_data)
        return survey

    def save(self, **kwargs):
        old_is_active = self.instance.is_active if self.instance else False
        new_is_active = self.validated_data.get("is_active")

        if not old_is_active and new_is_active:
            date_start = self.validated_data.get("date_start")
            self.validated_data["date_start"] = (
                date_start if date_start else datetime.date.today()
            )
            self.validated_data["date_end"] = None
        elif not new_is_active and old_is_active:
            self.validated_data["date_end"] = datetime.date.today()

        return super().save(**kwargs)


class Answer:
    def validate(self, attrs):
        question_type = attrs["question"].type
        if question_type == models.Question.TEXT:
            validators.validate_answer_text_required(attrs)
            attrs.pop("selected_options", None)
        else:
            attrs.pop("text", None)
            validators.validate_answer_selected_options_required(attrs)
            validators.validate_answer_correct_options(attrs)
            if question_type == models.Question.SINGLE_SELECT:
                validators.validate_answer_single_select(attrs)

        return attrs

    def create(self, data):
        selected_options = data.pop("selected_options", [])
        data.pop("id", None)
        answer = models.Answer.objects.create(**data)
        answer.selected_options.set(selected_options)
        answer.save()
        return answer

    def create_set(self, survey_progress, data):
        for answer_data in data:
            answer_data["survey_progress"] = survey_progress
            self.create(answer_data)


class SurveyProgress:
    def validate(self, attrs):
        validators.validate_survey_missing_questions(attrs)
        return attrs

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        with transaction.atomic():
            survey_progress = super().create(validated_data)
            Answer().create_set(survey_progress, answers_data)
        return survey_progress
