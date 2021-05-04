from search_suggestion import SearchSuggestion
# from app import rich_entity

suggestions = SearchSuggestion()

questions =['What is the email of Dan Harkey?'
,'What is the email of Vinodh Gopinath?'
,'How many courses are in SJSU?'
,'How many courses are taught by Dan Harkey?'
,'What is the deadline to pay Fall 2021 Tuition Fee?'
,'What are the pre-requisites for Masters in Software Engineering at SJSU?'
,"How can I reach the Student Health Center ?"
,"What is the contact number of admissions office?"
,"What are scholarships available to graduate students?"
,"What scholarships are available to grad students under nursing school?"
,"What is the criteria for an interdisciplinary studies major?"
,"Whom should I contact for interdisciplinary major?"
,"How to avail parking services?"
,"What is the ETS code to send TOEFL/ GRE score?"
,"Where is the central machine shop located?"
,"What is the application fees for graduate school?"
,"Dan Harkey"
,"ISSS Department"
,"SJSU"
,"San Jose State University"
,"Software Engineering"
,"Computer Engineering"
,"Vinodh Gopinath"
,"CMPE 255"
,"CMPE 273"
,"CMPE 281"
,"CMPE 295A"
,"CMPE 295B"
]

# print(rich_entity)


for i in range(len(questions)):
    questions[i] = questions[i].lower()


entities = {'dan harkey':'Director - MSSE','vinodh gopinath':'Professor - MSSE','cmpe 273':'Enterprise Distributed Systems','cmpe 255':'Data Mining','cmpe 281':'Cloud Computing'}

# print(questions)

suggestions.batch_insert(questions)



# input = "cmp"
# result = suggestions.search(input.lower(), max_suggestions=10)
# print(result)


def showSuggestions(result):

    class Helper(object):
        def __init__(self, suggestion, tag):
            self.suggestion = suggestion
            self.tag = tag

    displaySuggestions = []
    for i in range(len(result)):
        suggestion = result[i]
        tag = ""
        if(suggestion in entities.keys()):
            # print(entities[suggestion])
            tag = entities[suggestion]
        
        displaySuggestions.append(Helper(suggestion,tag))

    return displaySuggestions

# sug = showSuggestions(result)

# for obj in sug:
#     print(obj.suggestion)
#     print(obj.tag)