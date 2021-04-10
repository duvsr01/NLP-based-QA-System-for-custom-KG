import requests

questions = {}

URL = 'http://localhost:8080/ok'
questions = [
    {
        "data": "What is email of Dan Harkey?",
        "langCode": "en"
    },
    {"data": "What is email id of Dan Harkey?",
        "langCode": "en"} ,
    {"data": "What is email address of Dan Harkey?",
            "langCode": "en"}
]


def get_answer(question):
    response = requests.post(URL, json=question)
    print(response.json())

    if "results" in response.json():
        bindings = response.json()["results"]["bindings"]
        for binding in bindings:
            print(binding["answer"]["value"])
    else:
        print("No results")


if __name__ == '__main__':
    print("Hello world")
    for question in questions:
        get_answer(question)

