# updates: added elif statements for is and was

import spacy

nlp = spacy.load("en_core_web_sm")

test_sentence = "Since May 2011, they has written a biweekly column for Bloomberg View. Postrel has written several articles on health care and bioethics; these include accounts of their own experiences. In March 2006 Postrel donated a kidney to an acquaintance--psychiatrist and writer Sally Satel. they has recounted the experience, and referred to it in several subsequent articles and blog posts--many of which are critical of legal prohibitions against compensating organ donors."
# test_sentence = "they was known in Sweden as Kloke-Hans (``Wise Hans''). Prof. Larsson was a humanist and an author. they was also a mentor for several Swedish authors and a prominent essayist. Prof. Larsson was the son of the farmer Lars Persson and Kersti Nilsdotter, and cousin of author Ola Hansson. After studentexamen in 1881 they began their studies at Lund University."
# test_sentence = "they was delivered to the Norwegian passenger ship company Det Bergenske Dampskibsselskab of Bergen in 1905. Irma sailed for the company until they was attacked and sunk by two MTBs belonging to the Royal Norwegian Navy on 13 February 1944. After delivery, Irma served on the Bergen-- Newcastle route until they was transferred to Norway in the autumn of 1921 to carry out tourist voyages to the North Cape and Spitsbergen in the summer seasons."


doc = nlp(test_sentence)

# Iterate over the sentences in the document
corrected_sentences = []
for sentence in doc.sents:
    corrected_sentence_tokens = []
    for token in sentence:

        # FOR HAS -- notice: token.dep_ = aux and child.dep_ = nsubj
        if token.text.lower() == "has" and token.dep_ == "aux" or token.dep_ == "ROOT":
            # Traverse up the tree to handle coordination and find the main verb
            head = token.head
            while head.dep_ == "conj" and head.head != head:
                head = head.head

            # Check if 'they' is the subject of the verb
            subject = [child for child in head.children if child.dep_ == "nsubj" and child.text.lower() == "they"]
            if subject:
                corrected_sentence_tokens.append("have")
                continue
        
        # FOR IS -- notice: token.dep_ = auxpass and child.dep_ = nsubjpass
        elif token.text.lower() == "is" and token.dep_ == "auxpass" or token.dep_ == "ROOT":
            # Traverse up the tree to handle coordination and find the main verb
            head = token.head
            while head.dep_ == "conj" and head.head != head:
                head = head.head

            # Check if 'they' is the subject of the verb
            subject = [child for child in head.children if child.dep_ == "nsubjpass" and child.text.lower() == "they"]
            if subject:
                corrected_sentence_tokens.append("are")
                continue

        # FOR WAS -- notice: token.dep_ = auxpass or ROOT and child.dep_ = nsubjpass
        elif token.text.lower() == "was" and token.dep_ == "auxpass" or token.dep_ == "ROOT" :
            # Traverse up the tree to handle coordination and find the main verb
            head = token.head
            while head.dep_ == "conj" and head.head != head:
                head = head.head

            # Check if 'they' is the subject of the verb
            subject = [child for child in head.children if child.dep_ == "nsubjpass" and child.text.lower() == "they"]
            if subject:
                corrected_sentence_tokens.append("were")
                continue
        
        corrected_sentence_tokens.append(token.text)

    # Reconstruct the sentence
    corrected_sentence = ' '.join(corrected_sentence_tokens)
    corrected_sentences.append(corrected_sentence)

corrected_text = ' '.join(corrected_sentences)
print(corrected_text)




