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

file_name = 'gender_neutral_data_v2.csv'
output_file_name = 'replaced_gender_neutral_data_v2.csv'

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

# keep the capitalization form after replacement wherever needed
def replace_pronoun(original, replacement_map):
    if original.istitle():
        return replacement_map.get(original.lower(), original).capitalize()
    else:
        return replacement_map.get(original.lower(), original)
    
rows = []

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

        # replace the pronoun 
        for cluster in coref_clusters:
            # only process pronouns that are related to the antecedent identified
            if any(antecedent in doc[start:end+1].text.lower() for start, end in cluster):
                for start, end in cluster:
                    for i in range(start, end + 1):
                        word = tokens[i].strip()
                        if word.lower() == 'her':
                            if doc[i].tag_ == 'PRP$':
                                replacement = 'Their' if word.istitle() else 'their'
                                tokens[i] = replacement + tokens[i][len(word):]
                            else:
                                replacement = 'Them' if word.istitle() else 'them'
                                tokens[i] = replacement + tokens[i][len(word):]
                        elif word.lower() in pronoun_replacements and doc[i].tag_ in ['PRP', 'PRP$']:
                            tokens[i] = replace_pronoun(word, pronoun_replacements) + tokens[i][len(word):]

        updated_text = ''.join(tokens)  
        row['Replaced_Text'] = updated_text
        rows.append(row)


fieldnames = csv_reader.fieldnames + ['Replaced_Text']

with open(output_file_name, mode='w', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(rows)
        
