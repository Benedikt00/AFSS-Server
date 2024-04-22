


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