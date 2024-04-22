from flask import Blueprint, jsonify, render_template
from models import *
from extensions import db
import os
from config import Config

import math
from math import sqrt, log

# Create a Blueprint instance
search = Blueprint('search', __name__)

import json

import re

def remove_special_characters(text):
    # Define the regex pattern to keep German special characters ü, ö, and ä
    pattern = r'[^a-zA-Z0-9\süöäÜÖÄ]'
    return re.sub(pattern, '', text)


def term_frequency(term, document):
    """how often does this term appear relative to other therms in this document"""
    normalize_document = document.lower().split()
    return normalize_document.count(term.lower()) / float(len(normalize_document))


def inverse_document_frequency(term, all_documents):
    """how important is this therm"""
    num_documents_with_this_term = 0
    for doc in all_documents:
        if term.lower() in doc.lower().split():
            num_documents_with_this_term = num_documents_with_this_term + 1

    if num_documents_with_this_term > 0:
        return 1.0 + log(float(len(all_documents)) / num_documents_with_this_term)
    else:
        return 1.0


def cos_similarity(query_p, document_p):

    if not len(query_p) == len(document_p):
        raise ValueError("Lengths differ")

    dp = 0
    abs_doc_ = 0
    abs_query_ = 0
    for x in range(len(query_p)):
        dp += query_p[x] * document_p[x]
        abs_doc_ += document_p[x]**2
        abs_query_ += query_p[x] ** 2

    abs_doc = sqrt(abs_doc_)
    abs_query = sqrt(abs_query_)
    if abs_doc * abs_query == 0:
        return 0
    return dp / (abs_doc * abs_query)

# credit: https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/

@search.route('/s/<search_term>')
def method_name(search_term):


    print(search_term)

    search_vector = []

    for term in search_term.split():
        tf_for_term = term_frequency(term, search_term)
        
        idf_for_term = InverseDocumentTableSearch.query.get(term)

        if idf_for_term:
            idf_for_term = idf_for_term.value
        else:
            idf_for_term = 0
        search_vector.append(idf_for_term * tf_for_term)
    
    print(search_vector)

    document_vectors = []
    doc_ids = []

    term_freq_list = TermFrequencyList.query.all()
    for doc in term_freq_list:
        doc_terms = doc.terms
        doc_vec = []
        print(doc_terms)
        for term in search_term.split():
            if InverseDocumentTableSearch.query.get(term):
                inverse_document_frequency_for_term = InverseDocumentTableSearch.query.get(term).value
            else:
                inverse_document_frequency_for_term = 0
            if inverse_document_frequency_for_term:
                if term in doc_terms.keys():
                    term_frequency_for_document = doc_terms[term]
                else:
                    term_frequency_for_document = 0
                tf_idf = inverse_document_frequency_for_term * term_frequency_for_document
                doc_vec.append(tf_idf)
            else:
                doc_vec.append(0)
        document_vectors.append(doc_vec)
        doc_ids.append(doc.id)
    sims = []

    for document_vec in document_vectors:
        diff = cos_similarity(search_vector, document_vec)
        sims.append(diff)
    
    print(sims)
    print(doc_ids)
    return "200"

@search.route("/search_test", methods=["GET", "POST"])
def search_test():

    
        # Output the content
    print(content)
    
    return jsonify("200")

@search.route('/set_search_db')
def set_search_db():
    db.session.query(InverseDocumentTableSearch).delete()
    db.session.query(TermFrequencyList).delete()
    db.session.commit()

    db_data = {}
    articles = Article.query.all()
    for article in articles:
        # Convert picture column to text, remove special characters
        picture_content = remove_special_characters(article.picture) if article.picture else ""

        # Convert category and groupes columns to text
        category_text = ' '.join(article.category) if article.category else ""
        groupes_text = ' '.join(article.groupes) if article.groupes else ""

        category_text = remove_special_characters(groupes_text).replace("  ", " ")

        # Combine all text fields into a single string
        content = remove_special_characters(f"{article.article_name} {article.article_description} {category_text} {groupes_text}")

        db_data[article.id] = content

    term_frequency_list = []

    all_terms = []


    for doc in db_data:
        ls = {}
        el = db_data[doc]
        for term in el.lower().split():
            freq = term_frequency(term, el)
            ls[term] = freq

            if term not in all_terms:
                all_terms.append(term)

        new_tfl = TermFrequencyList(
            id = doc,
            terms = ls
        )
        db.session.add(new_tfl)
    

    print(term_frequency_list)

    idf = {}

    print(all_terms)

    for term_ in all_terms:
        print(term_)
        new_el = InverseDocumentTableSearch(
            term = term_,
            value = inverse_document_frequency(term_, list(db_data.values()))
        )
        db.session.add(new_el)
    print("list_end")
    db.session.commit()

    return "200"

# make a dict, with the weighted importance of every therm




# the term Frequeny for every therm in all of the documents


""" 

#make the document vektors
document_vectors = []

for doc in term_frequency_list:

    doc_vec = []

    for term in query_terms:

        if term in idf.keys():
            invers_document_frequency_for_term = idf[term]
            if term in doc.keys():
                term_frequency_for_document = doc[term]
            else:
                term_frequency_for_document = 0
            tf_idf = invers_document_frequency_for_term * term_frequency_for_document

            doc_vec.append(tf_idf)
        else:
            doc_vec.append(0)
    document_vectors.append(doc_vec)

sims = []

for document_vec in document_vectors:
    diff = cos_similarity(search_vector, document_vec)
    sims.append(diff)

print(sims)

number_of_elements_to_desplay = 5

top_indeces = get_top_indices(sims, 5)


for x in top_indeces:
    print(" ", documents[x]) """