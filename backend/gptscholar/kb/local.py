from logger import Logger
import os
import requests

from .base_kb import Kb, KbError, KbResults

from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST


class LocalKb(Kb):
    """
    LocalKb is an implementation of the KB interface that uses a local SPARQL endpoint.
    """

    MAXIMUM_LIMIT = 100

    def __init__(self, fuseki_domain, fuseki_dataset, fuseki_kg, admin_username, admin_password):
        self.fuseki_kg = fuseki_kg
        self.admin_username = admin_username
        self.admin_password = admin_password

        self.sparql_query_endpoint = f"http://{fuseki_domain}/{fuseki_dataset}/sparql"


    def inner_query(self, query):
        final_part_query = query.split("}")[-1].lower()
        limit_str = final_part_query.split("limit")
        if len(limit_str) == 1:
            limit_str = ""
        else:
            limit_str = limit_str[-1].strip().split(" ")[0]
        
        if limit_str == "":
            limit = None
            query = query + f" LIMIT {self.MAXIMUM_LIMIT}"
        else:
            limit_statement_str = "LIMIT" + final_part_query.split("limit")[-1].split(limit_str)[0] + limit_str
            query = query.replace(limit_statement_str, f"LIMIT {self.MAXIMUM_LIMIT}")
            limit = int(limit_str)
        
        Logger().debug(f"KB query:\n----------\n{query}\n----------\n")

        sparql_wrapper = SPARQLWrapper(self.sparql_query_endpoint)
        sparql_wrapper.setHTTPAuth(DIGEST)
        sparql_wrapper.setMethod(POST)
        sparql_wrapper.setCredentials(self.admin_username, self.admin_password)
        sparql_wrapper.setReturnFormat(JSON)

        result = None

        try:
            sparql_wrapper.setQuery(query)
            result = sparql_wrapper.query().convert()
        except Exception as e:
            Logger().error(f"KB query failed: {e}")
            return KbError("KB returned an exception.")

        if "exception" in result:
            if 'metadata' in result and 'line' in result['metadata'] and 'positionInLine' in result['metadata'] and 'exception' in result:
                Logger().error(f"KB query failed at {result['metadata']['line']}:{result['metadata']['positionInLine']}: {result['exception']}")
            elif 'exception' in result:
                Logger().error(f"KB query failed: {result['exception']}")
            else:
                Logger().error(f"KB query failed: {result}")
            return KbError("KB returned an exception.")

        return KbResults(result, limit=limit)
