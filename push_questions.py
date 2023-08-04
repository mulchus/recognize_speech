import os
import json
import argparse

from dotenv import load_dotenv
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
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


def get_questions_from_file(file_name):
    with open(file_name, "r", encoding="UTF-8") as my_file:
        questions = json.loads(my_file.read())
    return questions


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Скрипт звгрузки в DialogFlow ожидаемых от пользователя вопросов и ответы на них'
    )
    parser.add_argument(
        'file_name',
        nargs='?',
        default='questions.json',
        help='Имя файла .json с вопросами и ответами'
    )
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    questions_array = get_questions_from_file(parser.parse_args().file_name)
    for question_subject, questions in questions_array.items():
        if len(questions['answer']) > 300:
            questions['answer'] = questions['answer'][0:300]
        try:
            create_intent(project_id, question_subject, questions['questions'], [questions['answer']])
        except InvalidArgument:
            pass


if __name__ == '__main__':
    main()
