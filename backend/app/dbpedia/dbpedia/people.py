# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
People related regex
"""

from refo import Plus, Question
from backend.app.quepy.dsl import HasKeyword
from backend.app.quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle, Token
from .dsl import IsPerson, LabelOf, DefinitionOf, BirthDateOf, BirthPlaceOf, DaughterOf, NameOf, EmailOf, ProfessorOf, Fees, PreReq, IsGraduate, HasInfo, ScholarshipName, IsSchool


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)


class TutionFees(Particle):
    regex = Pos("NN") + Pos("NNS")

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)

class CollegeYear(Particle):
    regex = Pos("NN") + Pos("CD")

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)

class CourseName(Particle):
    regex = Pos("NNP")

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)

class Scholarship(Particle):
    regex = Pos("NN") | Pos("JJ") | Pos("NNS") | Pos("VBZ")

    def interpret(self, match):
        name = match.words.tokens
        print("name is", name)
        return HasKeyword(name)

class Graduate(Particle):
    regex = Pos("VB")

    def interpret(self, match):
        name = match.words.tokens
        print("name is", name)
        return name

class ETS(Particle):
    regex = Pos("NNP") + Pos("NN")

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)

class ParkingService(Particle):
    regex = Pos("NNP") + (Pos("NN") | Pos("NNS")) | (Pos("VBG") + Pos("NN"))

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)

class CentralMachine(Particle):
    regex = Pos("JJ") + Pos("NN")

    def interpret(self, match):
        name = match.words.tokens
        return HasKeyword(name)

class WhoIs(QuestionTemplate):
    """
    Ex: "Who is Tom Cruise?"
    """

    regex = Lemma("who") + Lemma("be") + Person() + \
            Question(Pos("."))

    def interpret(self, match):
        definition = DefinitionOf(match.person)
        return definition, "define"

class EmailOfQuestion(QuestionTemplate):
    """
    Regex for questions about the capital of a country.
    Ex: "What is the email of Dan Harkey?"
    """

    opening = Lemma("what") + Token("is")
    professor = Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS")
    regex = opening + Pos("DT") + Lemma("email") + Pos("IN") + \
        Question(Pos("DT")) +  Person() +  Question(Pos("."))

    def interpret(self, match):
        # email = ProfessorOf(match.person) + EmailOf(match.person)
        email = EmailOf(match.person)
        print("rdf :")
        print(email)
        return  email, "enum"

class HowOldIsQuestion(QuestionTemplate):
    """
    Ex: "How old is Bob Dylan".
    """

    regex = Pos("WRB") + Lemma("old") + Lemma("be") + Person() + \
            Question(Pos("."))

    def interpret(self, match):
        birth_date = BirthDateOf(match.person)
        return birth_date, "age"





class DaughterOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the daughter of Obama?"

    """

    regex = ((Lemmas("who be") + Pos("DT")) | (Lemmas("who") + Question(Lemma("be") + Pos("DT")))) + \
            (Lemma("daughter") | Lemma("child") | Lemma("children") | Lemma("son")) + \
            Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        daughter = IsPerson() + DaughterOf(match.person)
        father_name = NameOf(daughter)
        return father_name, "literal"


class CollegeQuestionFees(QuestionTemplate):
    """
    Ex: "What is the tuition fees of Spring 2021?"
        "How much is the tuition fees of Fall 2021?"
    """

    regex = (Lemmas("what be") + Pos("DT") + TutionFees() + Pos("IN") + CollegeYear() + Question(Pos(".")))| \
            (Pos("WRB") + Lemma("much") + Lemma("be") +  Pos("DT") + TutionFees() + Pos("IN") + CollegeYear()+ Question(Pos(".")))

    def interpret(self, match):
        print(match)
        m = Fees(match.collegeyear)

        return m, "literal"

        #return movie_name, "enum"

class CollegeQuestionPrereq(QuestionTemplate):
    """
    Ex: "What are the prerequisites of GWAR?"
        "What is the preRequisites for GWAR?"
        "What are the preRequisites of GWAR?"
        "What is the prereq of GWAR?"
        "Does GWAR have any prereq?"
        "Does GWAR has any prereq?"
    """

    regex = (Lemmas("what be") + Pos("DT") + (Pos("NNS") | Pos("NN") | (Pos("NN") + Pos("VBZ")))  + Pos("IN") + CourseName() + Question(Pos("."))) | \
            ((Pos("VBZ") | Pos("NNP")) + CourseName() + (Pos("VB") | Pos("VBZ")) + Pos("DT") + (Pos("NNS") | Pos("NN") | (Pos("NN") + Pos("VBZ"))) + Question(Pos(".")))

    def interpret(self, match):
        print(match)
        m = PreReq(match.coursename)

        return m, "literal"

class CollegeQuestionScholarship(QuestionTemplate):
    """
    Ex:
        "What are the scholarships available to graduate students?"
    """

    regex = (Lemmas("what be") + Pos("DT") + Scholarship() + Pos("JJ") + Lemma("to") + Graduate() + Pos("NNS") + Question(Pos(".")))

    def interpret(self, match):
        print(match)
        k = IsGraduate(match.scholarship)
        print("l is", k)
        m = ScholarshipName(k)

        return m, "literal"

class CollegeQuestionTOEFL(QuestionTemplate):
    """
    Ex:
        "What is the ETS code to send TOEFL score?"
        "ETS code to send TOEFL score?"
    """

    regex = (Lemmas("what be") + Pos("DT") + ETS() + Lemma("to") + Lemma("send") + Pos("NNP") + Lemma("score") + Question(Pos("."))) | \
            (ETS() + Lemma("to") + Lemma("send") + Pos("NNP") + Lemma("score") + Question(Pos(".")))

    def interpret(self, match):
        print(match)
        m = HasInfo(match.ets)

        return m, "literal"

class CollegeQuestionParking(QuestionTemplate):
    """
    Ex:
        "How to use Parking service?"
        "How to make use of Parking service?"
    """

    regex = Lemma("how") + Lemma("to") + Lemma("use") + ParkingService() + Question(Pos("."))| \
            Lemma("how") + Lemma("to") + Lemma("make") + Lemma("use") + Lemma("of") + ParkingService() + Question(Pos("."))

    def interpret(self, match):
        print(match)
        m = HasInfo(match.parkingservice)

        return m, "literal"

class CollegeQuestionShop(QuestionTemplate):
    """
    Ex:
        "Where is central machine shop situated?"
        "Where is central machine shop located?"
    """

    regex = Lemma("where") + Lemma("be") + CentralMachine() + Lemma("shop") + (Pos("VBD") | Pos("VBN")) + Question(Pos("."))

    def interpret(self, match):
        print(match)
        m = HasInfo(match.centralmachine)

        return m, "literal"

class CollegeQuestionScholarshipNursing(QuestionTemplate):
    """
    Ex:
        "What scholarships are available to graduate students under nursing school?"
        "What scholarships can graduate students under nursing school avail?"
    """

    regex = (Lemma("what") + Scholarship() + Lemma("be") + Pos("JJ") + Lemma("to") + Graduate() + Pos("NNS") + Pos("IN") + Pos("VBG") + Lemma("school") + Question(Pos("."))) | \
            (Lemma("what") + Scholarship() + Pos("MD") + Graduate() + Pos("NNS") + Pos("IN") + Pos("VBG") + Lemma("school") + Pos("NN") + Question(Pos(".")))

    def interpret(self, match):
        print(match)
        k = IsSchool(match.scholarship)

        print("l is", k)
        m = ScholarshipName(k)

        return m, "literal"


