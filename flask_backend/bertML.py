import pandas as pd;
import numpy
import sklearn
from sklearn.metrics.pairwise import cosine_similarity;
import nltk
from bert_serving.client import BertClient
import re
import gensim
from gensim.parsing.preprocessing import remove_stopwords

cleaned_sentences = []
sent_bertphrase_embeddings = []
print("Reading the csv....")
df = pd.read_csv("questionList.csv")
print("Completed.")
df.columns = ["questions", "answers"]

#preprocessing
def clean_sentence(sentence, stopwords=False):
    sentence = sentence.lower().strip()
    # print("Clean Sentence",clean_sentence)
    sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
    # sentence = re.sub(r'\s{2,}', ' ', sentence)
    if stopwords:
        sentence = remove_stopwords(sentence)
    return sentence


def get_cleaned_sentences(df, stopwords=False):
    sents = df["questions"];
    # print(sents)
    for index, row in df.iterrows():
        # print(index,row)
        # print(row["questions"])
        cleaned = clean_sentence(row["questions"], stopwords);
        cleaned_sentences.append(cleaned);
    return cleaned_sentences


#calculate cosine similairty between word embeddings
def retrieveAndPrintFAQAnswer(question_embedding, sentence_embeddings, FAQdf, sentences):
    max_sim = -1;
    index_sim = -1;
    # print(sentence_embeddings)
    for index, faq_embedding in enumerate(sentence_embeddings):
        # sim=cosine_similarity(embedding.reshape(1, -1),question_embedding.reshape(1, -1))[0][0];
        sim = cosine_similarity(faq_embedding, question_embedding)[0][0];
        # print(index, sim, sentences[index])
        if sim > max_sim:
            max_sim = sim;
            index_sim = index;
    # print("index_sim:: ", index_sim)
    if index_sim == -1:
        return ""
    else:
        return FAQdf.iloc[index_sim, 1]


#bertModel to produce contextua word embeddings
bc = BertClient()
res=bc.encode(['ML', 'AI'])

def preComputedSentenceEmbeddings():
    cleaned_sentences = get_cleaned_sentences(df, stopwords=False)
    # print(cleaned_sentences)
    for sent in cleaned_sentences:
        sent_bertphrase_embeddings.append(bc.encode([sent]));

def bertMatchinQuestion(question_orig):
    print("Bert Embedding...")
    question = clean_sentence(question_orig, stopwords=False);
    print("Output: ",question)
    question_embedding = bc.encode([question]);
    question_new = retrieveAndPrintFAQAnswer(question_embedding,sent_bertphrase_embeddings, df, cleaned_sentences);
    return question_new


# preComputedSentenceEmbeddings()
# bertMatchinQuestion("courses taken in fall")preComputedSentenceEmbeddings()
# bertMatchinQuestion("courses taken in fall")
