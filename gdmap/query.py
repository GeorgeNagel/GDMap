from gdmap.es_index import es
from gdmap.settings import ELASTICSEARCH_INDEX_NAME


def build_terms_query_body(terms):
    body = {
        "query": {
            "match": {
                "title": terms
            }
        }
    }
    return body


def get_query_results(terms=None):
    if terms:
        body = {
            "query": {
                "match": {
                    "title": terms
                }
            }
        }
    else:
        body = {"query": {"match_all": {}}}

    res = es.search(index=ELASTICSEARCH_INDEX_NAME, body=body)
    return res
