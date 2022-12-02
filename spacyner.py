import sys
import logging
from cassis import *
import spacy
import os
from datetime import datetime

# we load a language model from spacy. Here, we use the small german model.
nlp = spacy.load("de_core_news_sm")
path = os.getcwd()+"/"

# the XMI corresponding to the CAS of the prior pipeline component is in the system input stream.
# we read every line from the input and store the XMI in string representation in the variable 'c'
xmi_representation = ""
for line in sys.stdin:
    xmi_representation += line

# We instantiate the CAS from the typesystem and the XMI.
with open('sample_typesystem.xml', 'rb') as f:
    sample_typesystem = load_typesystem(f)

merged_typesystem = merge_typesystems(sample_typesystem, load_dkpro_core_typesystem())
cas = load_cas_from_xmi(xmi_representation, typesystem=merged_typesystem)

# We fetch the type from given typesystem
Token = merged_typesystem.get_type("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity")

# create a spaCy Document instance from applying the Language model nlp to the sofa text
doc = nlp(cas.sofa_string)

# Translate the spacy tokens to the dkpro cassis Token instances. Accumulate tokens into a list
tokens = []
# xmiID=None, value=None, identifier=None, begin=0, end=4, type='bla'
for ent in doc.ents:
    tokens.append (Token(begin=ent.start_char, end=ent.end_char, value=ent.label_))

# Add newly constructed tokens to the Common analysis system
for t in tokens:
    cas.add(t)

# pass the XMI to the next pipeline component via stdout.
print (cas.to_xmi())
