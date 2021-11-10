from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT = "t"
    SINGLE_SELECT = "s"
    MULTI_SELECT = "ms"

    QUESTION_TYPE_CHOICES = [
        (TEXT, "Text"),
        (SINGLE_SELECT, "Single Select"),
        (MULTI_SELECT, "Multi Select"),
    ]

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions"
    )
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES, default=TEXT)

    class Meta:
        unique_together = ("survey", "description", "type")

    def __str__(self):
        return f"{self.description} ({self.survey})"


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    text = models.CharField(max_length=1000)

    class Meta:
        unique_together = ("question", "text")

    def __str__(self):
        return f"{self.text} ({self.question})"


class SurveyProgress(models.Model):
    user_id = models.IntegerField()
    survey = models.ForeignKey(
        Survey, related_name="progresses", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user_id", "survey")


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, null=True, blank=True)
    selected_options = models.ManyToManyField(Option, related_name="answers")
    survey_progress = models.ForeignKey(
        SurveyProgress, related_name="answers", on_delete=models.CASCADE
    )
