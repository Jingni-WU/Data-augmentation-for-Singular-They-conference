import spacy

nlp = spacy.load("en_core_web_sm")

test_sentence = """
Since May 2011, they has written a biweekly column for Bloomberg View. Postrel has written several articles on health care and bioethics; 
these include accounts of their own experiences. In March 2006 Postrel donated a kidney to an acquaintance--psychiatrist and writer Sally Satel. 
they has recounted the experience, and referred to it in several subsequent articles and blog posts--many of which are critical of legal prohibitions 
against compensating organ donors. They eats so many apples when they is playing together.
"""

doc = nlp(test_sentence)

corrected_sentences = []
for sentence in doc.sents:
    corrected_sentence_tokens = []
    tokens = list(sentence)
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.lower_ == "they":
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token.tag_ == "VBZ":
                    # Directly handle "is" and "has" to avoid incorrect lemmatization
                    if next_token.lower_ == "has":
                        corrected_sentence_tokens.append("they")
                        corrected_sentence_tokens.append("have")
                    elif next_token.lower_ == "is":
                        corrected_sentence_tokens.append("they")
                        corrected_sentence_tokens.append("are")
                    # handle 3rd-person singular verbs 
                    else:
                        corrected_sentence_tokens.append("they")
                        corrected_sentence_tokens.append(next_token.lemma_)
                    i += 2  # Skip the next token as it's already processed
                    continue
                else:
                    corrected_sentence_tokens.append(token.text)
            else:
                corrected_sentence_tokens.append(token.text)
        else:
            corrected_sentence_tokens.append(token.text)

        i += 1

    corrected_sentence = ' '.join(corrected_sentence_tokens)
    corrected_sentences.append(corrected_sentence)

corrected_text = ' '.join(corrected_sentences)
print(corrected_text)






# import spacy

# nlp = spacy.load("en_core_web_sm")

# test_sentence = "Since May 2011, they has written a biweekly column for Bloomberg View. Postrel has written several articles on health care and bioethics; these include accounts of their own experiences. In March 2006 Postrel donated a kidney to an acquaintance--psychiatrist and writer Sally Satel. they has recounted the experience, and referred to it in several subsequent articles and blog posts--many of which are critical of legal prohibitions against compensating organ donors. They eats so many apple when they is playing together."

# doc = nlp(test_sentence)

# # Iterate over the sentences in the document
# corrected_sentences = []
# for sentence in doc.sents:
#     corrected_sentence_tokens = []
#     for token in sentence:
#         # Traverse up the tree to handle coordination and find the main verb
#         head = token.head
#         while head.dep_ == "conj" and head.head != head:
#             head = head.head

#         # Check if 'they' is the subject of the verb
#         subject = [child for child in head.children if child.dep_ == "nsubj" and child.text.lower() == "they"]
        
#         if token.text.lower() == "has" and (token.dep_ == "aux" or token.dep_ == "ROOT") and subject:
#             corrected_sentence_tokens.append("have")
#             continue  # Skip to next token after correction
        
#         elif token.text.lower() == "is" and (token.dep_ == "auxpass" or token.dep_ == "ROOT") and subject:
#             corrected_sentence_tokens.append("are")
#             continue  # Skip to next token after correction

#         elif token.text.lower() == "was" and (token.dep_ == "auxpass" or token.dep_ == "ROOT") and subject:
#             corrected_sentence_tokens.append("were")
#             continue  # Skip to next token after correction

#         elif token.pos_ == spacy.symbols.VERB and token.dep_ == "ROOT" and subject and token.tag_ == "VBZ":
#             # Use Spacy's lemmatization to get the base form of the verb for 'they'
#             base_form = token.lemma_
#             corrected_sentence_tokens.append(base_form)
#         else:
#             corrected_sentence_tokens.append(token.text)


#     # Reconstruct the sentence
#     corrected_sentence = ' '.join(corrected_sentence_tokens)
#     corrected_sentences.append(corrected_sentence)

# corrected_text = ' '.join(corrected_sentences)
# print(corrected_text)
