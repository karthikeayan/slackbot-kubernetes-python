
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

def find_env(message):
    env = ""

    if isinstance(message, str):
        doc3 = nlp(message)

        for token in doc3:
            print(token.text, token.pos_, token.dep_)
            if token.pos_ == "PROPN" or token.pos_ =="NOUN":
                env = token.text

    return env