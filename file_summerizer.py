
import nltk
import string
from heapq import nlargest
from wordcloud import WordCloud, STOPWORDS
from rake_nltk import Rake


def return_summary(text) :
    rk=Rake()
    rk.extract_keywords_from_text(text)
    extract_keyword=rk.get_ranked_phrases()
    extract_keyword

    nopuch = []

    for c in text :
        if c not in string.punctuation :
            nopuch.append(c)

    nopuch = "".join(nopuch)

    process_text = []
    for word in nopuch.split() :
        if word not in nltk.corpus.stopwords.words('english') :
            process_text.append(word)

    word_freq={}
    for word in process_text:
        if word not in word_freq:
            word_freq[word]=1
        else:
            word_freq[word]=word_freq[word]+1

    max_freq=max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word]=(word_freq[word]/max_freq)

    #create sent freq
    sent_list=nltk.sent_tokenize(text)

    sent_score={}
    for sent in sent_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent]=word_freq[word]
                else:
                    sent_score[sent]=sent_score[sent]+word_freq[word]

    summary_sent=nlargest(7,sent_score, key=sent_score.get)

    summary=" ".join(summary_sent)

    return summary


# text = '''We are currently experiencing another gold rush in AI. Billions are being invested in AI startups across every imaginable industry and business function. Google, Amazon, Microsoft and IBM are in a heavyweight fight investing over $20 billion in AI in 2016. Corporates are scrambling to ensure they realise the productivity benefits of AI ahead of their competitors while looking over their shoulders at the startups. China is putting its considerable weight behind AI and the European Union is talking about a $22 billion AI investment as it fears losing ground to China and the US.

# AI is everywhere. From the 3.5 billion daily searches on Google to the new Apple iPhone X that uses facial recognition to Amazon Alexa that cutely answers our questions. Media headlines tout the stories of how AI is helping doctors diagnose diseases, banks better assess customer loan risks, farmers predict crop yields, marketers target and retain customers, and manufacturers improve quality control. And there are think tanks dedicated to studying the physical, cyber and political risks of AI.


# So who will make the money in AI?
# AI and machine learning will become ubiquitous and woven into the fabric of society. But as with any gold rush the question is who will find gold? Will it just be the brave, the few and the large? Or can the snappy upstarts grab their nuggets? Will those providing the picks and shovel make most of the money? And who will hit pay dirt?

# So where is the value being created with AI?
# As I started thinking about who was going to make money in AI I ended up with seven questions. Who will make money across the (1) chip makers, (2) platform and infrastructure providers, (3) enabling models and algorithm providers, (4) enterprise solution providers, (5) industry vertical solution providers, (6) corporate users of AI and (7) nations? While there are many ways to skin the cat of the AI landscape, hopefully below provides a useful explanatory framework — a value chain of sorts. The companies noted are representative of larger players in each category but in no way is this list intended to be comprehensive or predictive.'''

# if __name__ == "__main__" :
#     print(return_summary(text))
