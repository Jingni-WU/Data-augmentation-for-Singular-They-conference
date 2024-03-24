from allennlp.predictors.predictor import Predictor
import csv
import spacy 

# use spacy
# the function to retokenize the sentence by tokens instead of by characters
nlp = spacy.load("en_core_web_sm")

def find_token_index(doc, char_offset):
    for i, token in enumerate(doc):
        # print("position, word: ", i, token)
        if token.idx <= char_offset < token.idx + len(token):
            return i
    return -1

# use the coref model
model_url = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
predictor = Predictor.from_path(model_url)

file_name = 'pos_mapping_all_gap_v2.csv'

# make the replacement rule for normal pronouns 
pronoun_replacements = {
    'he': 'they',
    'she': 'they',
    'his': 'their',
    'him': 'them',
    'hers': 'theirs',
    "he's": "they're",
    "she's": "they're"
}

# process each row in the CSV file
with open(file_name, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        text = row['Text']
        pronoun = row['Pronoun'].lower()
        antecedent = row['A'].lower()
        char_offset = int(row['Pronoun-offset'])  
        pronoun_pos_tag = row['pron_pos_tag']

        # tokenize the text 
        doc = nlp(text)

        # convert character offset to token index
        target_index = find_token_index(doc, char_offset)

        # process the text with the coref model
        coref_result = predictor.predict(document=text)
        coref_clusters = coref_result['clusters']
        tokens = [token.text_with_ws for token in doc] 

        # replace the target pronoun 'her' based on its POS tag
        for cluster in coref_clusters:
            # only process pronouns that are related to the antecedent identified
            if any(antecedent in doc[start:end+1].text.lower() for start, end in cluster):
                for start, end in cluster:
                    for i in range(start, end + 1):
                        word_lower = tokens[i].strip().lower()
                        if word_lower == 'her':
                            if doc[i].tag_ == 'PRP$':
                                tokens[i] = 'their' + tokens[i][len(word_lower):]
                            else:
                                tokens[i] = 'them' + tokens[i][len(word_lower):]
                        elif word_lower in pronoun_replacements and doc[i].tag_ in ['PRP', 'PRP$']:
                            tokens[i] = pronoun_replacements[word_lower] + tokens[i][len(word_lower):]

        updated_text = ''.join(tokens)  
        print(updated_text)

        

