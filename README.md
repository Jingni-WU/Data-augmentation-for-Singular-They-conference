# Data-augmentation-for-Singular-They-conference

## Part 1: Dataset Creation - Augmentation of GAP Dataset

From the original GAP dataset, we created a GAP-2 dataset, wherein ⅓ of the data has unaltered feminine target pronouns, ⅓ has unaltered masculine target pronouns, and ⅓ has singular ‘they’ target pronouns, achieved through augmentation of the remaining GAP data. 

**Benefits of building from GAP:** 
- Co referring name-pronoun pairs are human labeled.
- High complexity is retained, with two possible antecedents in each data point.
- Augmented ‘they’ will always refer back to a singular named entity (i.e., don’t need to disambiguate generic and personal ‘they’).
- Already gender-balanced 2 ways: masc. and fem, singular target pronouns


**Data Augmentation Process:**
1. Changed all target pronouns to a form of ‘they.' Using POS tags (via SpaCy tokenization and Stanza for POS tagging), transformed the target pronoun to a form of ‘they.'
2. To maintain internal logic in the text, we used AllenNLP’s NeuralCoref to get coreference clusters of all pronouns for the correct antecedent (marked as label ‘TRUE’) Then, we used the same procedure as before, using POS tags and word form to update all corfering pronouns to the appropriate form of ‘they’.
3. Using SpaCy tokenization and POS tagging, we implemented a rule based system to inflect verbs following ‘they,’ to maintain proper agreement.
4. Update offset values (to identify targets and antecedents in the text)
5. Finally, we re-integrated the unaltered masculine and feminine portions of the GAP dataset, to create a final dataset that had ⅓ masculine, ⅓ feminine, and ⅓ gender neutral ‘they’ target pronouns. We randomly divided the dataset into an 80-20 train-test split, marked in ‘ID’ column, maintaining equal proportions of masc-fem-neutral target pronouns. 

**GAP-2** 
- 1484 rows of data from original GAP, with fem target pronoun
- 1484 rows of data from original GAP, with masc. target pronoun
- 1484 rows of data from augmented GAP, with singular 'they' target pronoun
- all rows have two possible named-entity antecedents (human-labeled for coreference)

## Part 2: Comparatively assess gender bias in coreference resolution systems

**Evaluation Method**
Looking only at the target pronoun, A-coref, and B-coref:
- True positive = both the true antecedent and target pronoun appear in a coref cluster
- False negative = either/both the true antecedent and target pronoun are absent in a coref cluster 
- False positive = both the false antecedent and target pronoun appear in a coref cluster

Evaluation code for FCoref, AllenNLP Coref, and Stanza Coref on the GAP-2 dataset is provided in the *eval_coref_models* dir


### GAP Citation

@article{webster-etal-2018-mind,
    title = "Mind the {GAP}: A Balanced Corpus of Gendered Ambiguous Pronouns",
    author = "Webster, Kellie  and
      Recasens, Marta  and
      Axelrod, Vera  and
      Baldridge, Jason",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "6",
    year = "2018",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/Q18-1042",
    doi = "10.1162/tacl_a_00240",
    pages = "605--617",
}





