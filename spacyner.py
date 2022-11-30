import sys
import logging
from cassis import *
import spacy
import os
from datetime import datetime

nlp = spacy.load("de_core_news_sm")
path = os.getcwd()+"/"

c = ""
for line in sys.stdin:
    c = c + line

# Default Typesystem
typesystem=load_dkpro_core_typesystem()
# make cas out of stdin
cas = load_cas_from_xmi(c, typesystem=load_dkpro_core_typesystem())

# Get Token type
Token = typesystem.get_type("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity")
# Create Spacy doc
doc = nlp(cas.sofa_string)

# Add NE
tokens = []
# xmiID=None, value=None, identifier=None, begin=0, end=4, type='bla'
for ent in doc.ents:
    tokens.append (Token(begin=ent.start_char, end=ent.end_char, value=ent.label_))

for t in tokens:
    cas.add(t)
    
print (cas.to_xmi())
