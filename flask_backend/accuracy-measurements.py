import requests
import json

questions = {}

URL = 'http://localhost:5000/question'
questions = [
    {
        "question": "What is the email of Dan Harkey?",
        "langCode": "en",
        "answer": "dan.harkey@sjsu.edu"
    },
    {
        "question": "What is the emaul of Dan Harkey?",
        "langCode": "en",
        "answer": "dan.harkey@sjsu.edu"
    },
    {
        "question": "What is the emaul of Vinodh Gopinth?",
        "langCode": "en",
        "answer": "vinodh.gopinath@sjsu.edu"
    },
    {
        "question": "What is the email of Vinodh Gopinth?",
        "langCode": "en",
        "answer": "vinodh.gopinath@sjsu.edu"
    },
    {
        "question": "What is the email address of Dan Harky?",
        "langCode": "en",
        "answer": "dan.harkey@sjsu.edu"
    }
]


def get_answer(question):
    response = requests.post(URL, json=question)
    return response.text
    #print(response.json())

    # if "results" in response.json():
    #     bindings = response.json()["results"]["bindings"]
    #     for binding in bindings:
    #         return binding["answer"]["value"]
    # else:
    #     return "No results"


if __name__ == '__main__':
    total = len(questions)

    for version in [1, 2, 3]:
        number_of_correct_answers = 0
        number_of_questions_answered = 0

        for q in questions:
            question = json.loads(json.dumps(q, indent=4))
            question.update({"version": version})
            answer = get_answer(question)

            print("question", question)
            print("answer", answer)

            if len(answer) != 2:
                number_of_questions_answered = number_of_questions_answered + 1

            if answer == question["answer"]:
                number_of_correct_answers = number_of_correct_answers + 1

        if number_of_questions_answered == 0:
             precision = 0
        else:
            precision = number_of_correct_answers/number_of_questions_answered
        recall = number_of_correct_answers/total
        if (precision + recall) == 0:
            f_measure = 0
        else:
            f_measure = 2 * (precision * recall)/(precision + recall)

        print("version", version)
        print("precision", precision)
        print("recall", recall)
        print("f_measure", f_measure)

