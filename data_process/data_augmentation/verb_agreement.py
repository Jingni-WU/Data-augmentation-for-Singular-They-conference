import spacy

nlp = spacy.load("en_core_web_sm")

test_sentence = "Since May 2011, they has written a biweekly column for Bloomberg View. Postrel has written several articles on health care and bioethics; these include accounts of their own experiences. In March 2006 Postrel donated a kidney to an acquaintance--psychiatrist and writer Sally Satel. they has recounted the experience, and referred to it in several subsequent articles and blog posts--many of which are critical of legal prohibitions against compensating organ donors."
doc = nlp(test_sentence)

# Iterate over the sentences in the document
corrected_sentences = []
for sentence in doc.sents:
    corrected_sentence_tokens = []
    for token in sentence:
        if token.text.lower() == "has" and token.dep_ == "aux":
            # Traverse up the tree to handle coordination and find the main verb
            head = token.head
            while head.dep_ == "conj" and head.head != head:
                head = head.head

            # Check if 'they' is the subject of the verb
            subject = [child for child in head.children if child.dep_ == "nsubj" and child.text.lower() == "they"]
            if subject:
                corrected_sentence_tokens.append("have")
                continue
        corrected_sentence_tokens.append(token.text)

    # Reconstruct the sentence
    corrected_sentence = ' '.join(corrected_sentence_tokens)
    corrected_sentences.append(corrected_sentence)

corrected_text = ' '.join(corrected_sentences)
print(corrected_text)




