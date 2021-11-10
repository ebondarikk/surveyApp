from rest_framework import serializers, fields

from . import models
from . import services


class Option(serializers.ModelSerializer):
    id = fields.IntegerField(required=False)
    text = fields.CharField()

    class Meta:
        model = models.Option
        fields = ("id", "text")


class Question(services.Question, serializers.ModelSerializer):
    def __init__(self, *args, nested=False, **kwargs):
        super().__init__(*args, **kwargs)
        if nested:
            self.fields.get("survey").read_only = True

    id = fields.IntegerField(required=False)
    options = Option(many=True, required=False)

    class Meta:
        model = models.Question
        fields = ("id", "description", "type", "survey", "options")


class Survey(services.Survey, serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields.get("date_start").read_only = True

    questions = Question(many=True, required=False, allow_empty=True, nested=True)

    class Meta:
        model = models.Survey
        fields = (
            "id",
            "name",
            "description",
            "questions",
            "is_active",
            "date_start",
            "date_end",
        )
        read_only_fields = ("date_end",)


class Answer(services.Answer, serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("id", "question", "text", "selected_options")
        extra_kwargs = {
            "selected_options": {"allow_empty": True, "required": False},
            "text": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["type"] = instance.question.type
        return result


class SurveyProgress(services.SurveyProgress, serializers.ModelSerializer):
    answers = Answer(many=True, required=True)
    survey = serializers.PrimaryKeyRelatedField(
        queryset=models.Survey.objects.filter(is_active=True),
        error_messages={"does_not_exist": "The Survey should be active"},
        write_only=True,
    )

    class Meta:
        model = models.SurveyProgress
        fields = ("user_id", "answers", "survey")


class QuestionList(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ("description", "type")


class AnswerList(serializers.ModelSerializer):
    question = QuestionList()
    options = fields.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = ("question", "text", "options")

    def get_options(self, instance):
        return [
            {
                "text": option.text,
                "is_selected": option in instance.selected_options.all(),
            }
            for option in instance.question.options.all()
        ]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        if instance.question.type == models.Question.TEXT:
            result.pop("options")
        else:
            result.pop("text")
        return result


class SurveyList(serializers.ModelSerializer):
    class Meta:
        model = models.Survey
        fields = ("id", "name", "description", "is_active")


class SurveyProgressList(serializers.ModelSerializer):
    answers = AnswerList(many=True)
    survey = SurveyList()

    class Meta:
        model = models.SurveyProgress
        fields = ("user_id", "survey", "answers")
