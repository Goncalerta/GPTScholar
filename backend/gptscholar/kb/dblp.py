from .base_kb import Kb, KbResults, KbError
from logger import Logger
import requests

class DblpKb(Kb):
    """
    DblpKb is an implementation of the KB interface that uses the DBLP SPARQL endpoint.
    """
    ENDPOINT = "https://sparql.dblp.org/sparql"
    MAXIMUM_LIMIT = 100

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

        try:
            r = requests.post(
                self.ENDPOINT, 
                data = { 
                    "query": query,
                },
                headers = {
                    "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                }
            )
        except requests.exceptions.RequestException as e:
            Logger().error(f"KB query failed: {e}")
            return KbError("KB returned an exception.")
        
        result = r.json()

        if "exception" in result:
            if 'metadata' in result and 'line' in result['metadata'] and 'positionInLine' in result['metadata'] and 'exception' in result:
                Logger().error(f"KB query failed at {result['metadata']['line']}:{result['metadata']['positionInLine']}: {result['exception']}")
            elif 'exception' in result:
                Logger().error(f"KB query failed: {result['exception']}")
            else:
                Logger().error(f"KB query failed: {result}")
            return KbError("KB returned an exception.")

        return KbResults(result, limit=limit)
