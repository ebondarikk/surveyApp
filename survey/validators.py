from rest_framework import serializers

FIELD_REQUIRED_FOR_QUESTION_TYPE = "This field is required for this type of question"


def validate_answer_text_required(attrs):
    if not attrs.get("text"):
        raise serializers.ValidationError({"text": FIELD_REQUIRED_FOR_QUESTION_TYPE})


def validate_answer_selected_options_required(attrs):
    if not attrs.get("selected_options"):
        raise serializers.ValidationError(
            {"selected_options": FIELD_REQUIRED_FOR_QUESTION_TYPE}
        )


def validate_answer_correct_options(attrs):
    valid_options = set(attrs.get("question").options.all())
    selected_options_set = set(attrs.get("selected_options"))
    incorrect_options = selected_options_set.difference(valid_options)
    if incorrect_options:
        raise serializers.ValidationError(
            {
                "selected_options": f"Allowable options are: {[o.id for o in valid_options]}"
            }
        )


def validate_answer_single_select(attrs):
    if len(attrs.get("selected_options")) != 1:
        raise serializers.ValidationError(
            {"selected_options": "Only one item can be selected"}
        )


def validate_survey_missing_questions(attrs):
    questions_set = set(attrs["survey"].questions.all())
    answered_questions_set = set(a["question"] for a in attrs["answers"])
    missing_questions = questions_set.difference(answered_questions_set)
    if missing_questions:
        raise serializers.ValidationError(
            {
                "answers": f"Missing answers for the following questions: {[q.id for q in missing_questions]}"
            }
        )


def validate_question_options(attrs):
    if not attrs.get("options"):
        raise serializers.ValidationError({"options": FIELD_REQUIRED_FOR_QUESTION_TYPE})
