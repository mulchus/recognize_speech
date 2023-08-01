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


questions = get_questions_from_file()
for question in questions.values():
    if len(question['answer']) > 300:
        question['answer'] = question['answer'][0:300]
    try:
        create_intent(project_id, question['questions'][0], question['questions'], [question['answer']])
    except InvalidArgument:
        pass

