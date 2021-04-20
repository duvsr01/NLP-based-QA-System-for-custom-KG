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
from .dsl import IsPerson, LabelOf, DefinitionOf, BirthDateOf, BirthPlaceOf, DaughterOf, NameOf, EmailOf, ProfessorOf


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

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


class WhereIsFromQuestion(QuestionTemplate):
    """
    Ex: "Where is Bill Gates from?"
    """

    regex = Lemmas("where be") + Person() + Lemma("from") + \
        Question(Pos("."))

    def interpret(self, match):
        birth_place = BirthPlaceOf(match.person)
        label = LabelOf(birth_place)

        return label, "enum"


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
