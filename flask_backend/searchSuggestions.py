from search_suggestion import SearchSuggestion
# from app import rich_entity

suggestions = SearchSuggestion()

questions =['What is the email of Dan Harkey?'
,'What is the email of Vinodh Gopinath?'
,'How many courses are in SJSU?'
,'How many courses are taught by Dan Harkey?'
,'What is the deadline to pay Fall 2021 Tuition Fee?'
,'What are the pre-requisites for Masters in Software Engineering at SJSU?'
,'How to apply for graduation?'
,'Where is location for CMPE 255 office hours?'
,'How to request for travel I-20 at SJSU?'
,'Who is the professor for CMPE-273?'
,'Where can I find Bursars office?'
,'What are some of the student clubs for Computer Science students?'
,'Library Timings?'
,'Where can I find printers on-campus?'
,'What are the office hours of a Professor?'
,'How many min credits are required to enroll in a semester?'
,'What is minimum of courses one needs to enroll in MS?'
,'What is the maximum number of courses one can take in a semester?'
,'What are the steps to apply for SSN?'
,'Is SSN mandatory to do a job on campus?'
,'What are prerequisites for GWAR?'
,'What are the prerequisites of course 255?'
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