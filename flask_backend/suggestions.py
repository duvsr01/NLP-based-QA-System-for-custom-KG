import string
from collections import defaultdict
from nltk.util import ngrams
import pickle

quad_prob_dict = defaultdict(list)         #for storing the probable  words for Quadgram sentences     
tri_prob_dict = defaultdict(list)          #for storing the probable  words for Trigram sentences     
bi_prob_dict = defaultdict(list)           #for storing the probable  words for Bigram sentences
#returns: string
#arg: string
#remove punctuations, change to lowercase ,retain the apostrophe mark
def removePunctuations(sen):
    #split the string into word tokens
    temp_l = sen.split()
    #print(temp_l)
    i = 0
    j = 0
    
    #changes the word to lowercase and removes punctuations from it
    for word in temp_l :
        j = 0
        #print(len(word))
        for l in word :
            if l in string.punctuation:
                if l == "'":
                    if j+1<len(word) and word[j+1] == 's':
                        j = j + 1
                        continue
                word = word.replace(l," ")
                #print(j,word[j])
            j += 1

        temp_l[i] = word.lower()
        i=i+1   

    #spliting is being done here beacause in sentences line here---so after punctuation removal it should 
    #become "here so"   
    content = " ".join(temp_l)

    return content

def loadCorpus(file_path, bi_dict, tri_dict, quad_dict, vocab_dict):   
    w1 = ''    #for storing the 3rd last word to be used for next token set
    w2 = ''    #for storing the 2nd last word to be used for next token set
    w3 = ''    #for storing the last word to be used for next token set
    token = []
    
    #total no. of words in the corpus
    word_len = 0
    
    
    with open(file_path,'r') as file:
        for line in file:
            #split the string into word tokens
            temp_l = line.split()
#             print(temp_l)
            
            i=0
            j=0
            
            #remove punctuations
            for word in temp_l:
                j=0
                for l in word:
                    if l in string.punctuation:
#                         print(l)
                        if(j+1<len(word) and word[j+1]=='s'):
                            j=j+1
                            continue
    
                        word = word.replace(l," ")
                    j=j+1
                temp_l[i] = word.lower()
                i=i+1
        
        
            content = " ".join(temp_l) 
#             print(content)     
            token = content.split()
#             print(token)
            word_len = word_len + len(token)
#             print(word_len)

            #add new unique words to the vocaulary set if available
            for word in token:
                if word not in vocab_dict:
                    vocab_dict[word] = 1
                else:
                    vocab_dict[word]+= 1
            
            if not token:
                continue
                
                
            #add word from previous line
            if w3!='':
                token.insert(0,w3)
                
            #tokens for bigrams  
            temp0 = list(ngrams(token,2))
            
            
            if w2!='':
                token.insert(0,w2)
            
            #tokens for trigrams
            temp1 = list(ngrams(token,3))
            
            
            if w1!='':
                token.insert(0,w1)
            
            #tokens for quadgrams
            temp2 = list(ngrams(token,4))
                  
                  
            #count the frequency of the bigram sentences
            for t in temp0:
                sen = ' '.join(t)
                bi_dict[sen] += 1

            #count the frequency of the trigram sentences
            for t in temp1:
                sen = ' '.join(t)
                tri_dict[sen] += 1

            #count the frequency of the quadgram sentences
            for t in temp2:
                sen = ' '.join(t)
                quad_dict[sen] += 1


            #then take out the last 3 words
            n = len(token)
           
            #store the last few words for the next sentence pairing
            if (n -3) >= 0:
                w1 = token[n -3]
            if (n -2) >= 0:
                w2 = token[n -2]
            if (n -1) >= 0:
                w3 = token[n -1]
                  
    return word_len


#creates dict for storing probable words with their probabilities 
# ADD 1 Smoothing used

#returns: void
#arg: dict,dict,dict,dict,dict
def findQuadgramProbAdd1(vocab_dict, bi_dict, tri_dict, quad_dict, quad_prob_dict):
    i = 0
    V = len(vocab_dict)
    
    #using the fourth word of the quadgram sentence as the probable word and calculate its
    #probability,here ADD 1 smoothing has been used during the probability calculation
    for quad_sen in quad_dict:
        quad_token = quad_sen.split()

        #trigram sentence for key
        tri_sen = ' '.join(quad_token[:3])

        #find the probability
        #add 1 smoothing has been used
        prob = ( quad_dict[quad_sen] + 1 ) / ( tri_dict[tri_sen] + V)
        
        #if the trigram sentence is not present in the Dictionary then add it
        if tri_sen not in quad_prob_dict:
            quad_prob_dict[tri_sen] = []
            quad_prob_dict[tri_sen].append([prob,quad_token[-1]])
        #the trigram sentence is present but the probable word is missing,then add it
        else:
            quad_prob_dict[tri_sen].append([prob,quad_token[-1]])
        
    prob = None
    quad_token = None
    tri_sen = None

#for creating prob dict for trigram probabilities
# ADD 1 Smoothing used

#returns: void
#arg: dict,dict,dict,dict
def findTrigramProbAdd1(vocab_dict, bi_dict, tri_dict, tri_prob_dict):
   
    #vocabulary length
    V = len(vocab_dict)
    
    #create a dictionary of probable words with their probabilities for
    #trigram probabilites,key is a bigram and value is a list of prob and word
    for tri in tri_dict:
        tri_token = tri.split()
        #bigram sentence for key
        bi_sen = ' '.join(tri_token[:2])
        
        #find the probability
        #add 1 smoothing has been used
        prob = ( tri_dict[tri] + 1 ) / ( bi_dict[bi_sen] + V)

        #tri_prob_dict is a dict of list
        #if the bigram sentence is not present in the Dictionary then add it
        if bi_sen not in tri_prob_dict:
            tri_prob_dict[bi_sen] = []
            tri_prob_dict[bi_sen].append([prob,tri_token[-1]])
        #the bigram sentence is present but the probable word is missing,then add it
        else:
            tri_prob_dict[bi_sen].append([prob,tri_token[-1]])
            
    prob = None
    tri_token = None
    bi_sen = None


#for creating prob dict for bigram probabilities
# ADD 1 Smoothing used

#returns: void
#arg: dict,dict,dict,dict
def findBigramProbAdd1(vocab_dict, bi_dict, bi_prob_dict):
    
    V = len(vocab_dict)
    
    print(V)
    
    #create a dictionary of probable words with their probabilities for bigram probabilites
    for bi in bi_dict:
        #print("bi: ",bi)
        bi_token = bi.split()
        #print("bi_token: ",bi_token)
        #print(bi_token[-1])
        #unigram for key
        unigram = bi_token[0]
        
        #find the probability
        #add 1 smoothing has been used
        prob = ( bi_dict[bi] + 1 ) / ( vocab_dict[unigram] + V)

        #bi_prob_dict is a dict of list
        #if the unigram sentence is not present in the Dictionary then add it
        if unigram not in bi_prob_dict:
            bi_prob_dict[unigram] = []
            bi_prob_dict[unigram].append([prob,bi_token[-1]])
        #the unigram sentence is present but the probable word is missing,then add it
        else:
            bi_prob_dict[unigram].append([prob,bi_token[-1]])

    prob = None
    bi_token = None
    unigram = None

#for sorting the probable word acc. to their probabilities

#returns: void
#arg: dict, dict, dict
def sortProbWordDict(bi_prob_dict, tri_prob_dict, quad_prob_dict):
    #sort bigram dict
    for key in bi_prob_dict:
        if len(bi_prob_dict[key])>1:
            bi_prob_dict[key] = sorted(bi_prob_dict[key],reverse = True)
    
    #sort trigram dict
    for key in tri_prob_dict:
        if len(tri_prob_dict[key])>1:
            tri_prob_dict[key] = sorted(tri_prob_dict[key],reverse = True)
    
    #sort quadgram dict
    for key in quad_prob_dict:
        if len(quad_prob_dict[key])>1:
            quad_prob_dict[key] = sorted(quad_prob_dict[key],reverse = True)[:2]

#pick the top most probable words from bi,tri and quad prob dict as word prediction candidates

#returns: list[float,string]
#arg: string,dict,dict,dict
def chooseWords(sen,bi_prob_dict,tri_prob_dict,quad_prob_dict):
    word_choice = []
    token = sen.split()

    if token[-1] in bi_prob_dict:
        word_choice +=  bi_prob_dict[token[-1]][:1]
        print('Word Choice bi dict:' , word_choice)
    if ' '.join(token[1:]) in tri_prob_dict:
        word_choice +=  tri_prob_dict[' '.join(token[1:])][:1]
        print('Word Choice tri_dict:', word_choice)
    if ' '.join(token) in quad_prob_dict:
        word_choice += quad_prob_dict[' '.join(token)][:1]
        print('Word Choice quad_dict', word_choice)
    
    return word_choice

def main():
    vocab_dict = defaultdict(int)          #for storing the different words with their frequencies  
    bi_dict = defaultdict(int)             #for keeping count of sentences of two words
    tri_dict = defaultdict(int)            #for keeping count of sentences of three words
    quad_dict = defaultdict(int)           #for keeping count of sentences of four words
  
    #loading the file to train the model
    train_file = './corpus/corpusfile.txt'

    #load the corpus for the dataset
    token_len = loadCorpus(train_file, bi_dict, tri_dict, quad_dict, vocab_dict)
    print(token_len)

    #create bigram Probability Dictionary
    findBigramProbAdd1(vocab_dict, bi_dict, bi_prob_dict)
    #create trigram Probability Dictionary
    findTrigramProbAdd1(vocab_dict, bi_dict, tri_dict, tri_prob_dict)
    #create quadgram Probability Dictionary
    findQuadgramProbAdd1(vocab_dict, bi_dict, tri_dict, quad_dict, quad_prob_dict)
    #sort the probability dictionaries
    sortProbWordDict(bi_prob_dict, tri_prob_dict, quad_prob_dict)

    # pickling bi_prob_dict
    bi_prob_dict_file = open("./pickle/bi_prob_dict.pickle", "wb")
    pickle.dump(bi_prob_dict, bi_prob_dict_file)

    # pickling tri_prob_dict
    tri_prob_dict_file = open("./pickle/tri_prob_dict.pickle","wb")
    pickle.dump(tri_prob_dict, tri_prob_dict_file)

    # pickling quad_prob_dict
    quad_prob_dict_file = open("./pickle/quad_prob_dict.pickle","wb")
    pickle.dump(quad_prob_dict, quad_prob_dict_file)


if __name__ == '__main__':
    main()
