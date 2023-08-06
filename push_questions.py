import os
import json
import argparse
import dialogflow_functions

from dotenv import load_dotenv
from google.api_core.exceptions import InvalidArgument
from contextlib import suppress


def get_questions_from_file(file_name):
    with open(file_name, "r", encoding="UTF-8") as questions_file:
        questions = json.loads(questions_file.read())
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
        with suppress(InvalidArgument):
            dialogflow_functions.create_intent(project_id, question_subject,
                                               questions['questions'], [questions['answer']])


if __name__ == '__main__':
    main()
