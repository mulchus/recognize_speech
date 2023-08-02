import json
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from main import project_id


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent, "language_code": "ru", }
    )

    print("Intent created: {}".format(response))


def get_questions_from_file():
    with open('questions.json', "r", encoding="UTF-8") as my_file:
        questions = json.loads(my_file.read())
    return questions


questions_array = get_questions_from_file()
for question_subject, questions in questions_array.items():
    if len(questions['answer']) > 300:
        questions['answer'] = questions['answer'][0:300]
    try:
        create_intent(project_id, question_subject, questions['questions'], [questions['answer']])
    except InvalidArgument:
        pass
