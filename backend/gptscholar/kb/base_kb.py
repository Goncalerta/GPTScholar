class Kb:
    PREFIXES = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX dblp: <https://dblp.org/rdf/schema#> 
"""

    def replace_prefixes(self, query):
        processed = ""
        start = False
        for line in query.split("\n"):
            if line.strip() == "":
                continue
            if "prefix" not in line.lower():
                start = True
            if start:
                processed += line + "\n"

        processed = self.PREFIXES + processed
        return processed

    def query(self, query):
        query = query.replace("```sparql", "").replace("```", "")
        result = self.inner_query(query)
        if isinstance(result, KbError):
            query = self.replace_prefixes(query)
            result = self.inner_query(query)
        return result
    
    def inner_query(self, query):
        pass

class KbResponse:
    def raw(self):
        pass

    def vars(self):
        pass

    def bindings(self):
        pass

class KbResults(KbResponse):
    def __init__(self, results, limit=None):
        self.results = results
        self.limit = limit

    def raw(self):
        return self.results
    
    def vars(self):
        return self.results["head"]["vars"]
    
    def bindings(self):
        raw_bindings = self.results["results"]["bindings"]
        title_var = "title"
        author_name_var = "authorName"
        orcid_var = "orcid"
        type_var = "type"
        bindings = []
        for binding in raw_bindings:
            bindings.append({ key: binding[key]["value"] for key in binding.keys() })

        new_bindings = []
        for binding in bindings:
            if not title_var in binding:
                new_bindings.append(binding)
                continue
            title = binding[title_var]
            for existing in new_bindings:
                if title_var in existing and existing[title_var] == title:
                    if author_name_var in binding and binding[author_name_var] not in [x["name"] for x in existing["author"]]:
                        existing["author"].append({
                            "name": binding[author_name_var],
                            "orcid": binding[orcid_var] if orcid_var in binding else None,
                        })
                    if type_var in binding and type_var in existing and binding[type_var] not in existing[type_var]:
                        existing[type_var].append(binding[type_var])
                    break
            else:
                if author_name_var in binding:
                    binding["author"] = [{
                        "name": binding[author_name_var],
                        "orcid": binding[orcid_var] if orcid_var in binding else None,
                    }]
                    del binding[author_name_var]
                    if orcid_var in binding:
                        del binding[orcid_var]
                    if type_var in binding:
                        binding[type_var] = [binding[type_var]]
                new_bindings.append(binding)
        
        if self.limit is not None:
            new_bindings = new_bindings[:self.limit]
        else:
            new_bindings = new_bindings[:10]
        return new_bindings

class KbError(KbResponse):
    def __init__(self, message):
        self.message = message
    
    def raw(self):
        return self.message

    def vars(self):
        return []

    def bindings(self):
        return {"error": self.message}
