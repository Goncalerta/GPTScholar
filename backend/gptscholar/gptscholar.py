import os
from logger import Logger
from .llm.base_llm import LlmSession
from .template_builder import TemplateBuilder

def _init_llm():
    llm_source = os.environ.get('LLM_SOURCE', None)
    if llm_source == "mock":
        from .llm.mock import MockLlm
        return MockLlm()
    elif llm_source == "openai":
        from .llm.openai import OpenAiLlm
        api_key = os.environ.get('OPENAI_API_KEY', None)
        if api_key is None:
            raise Exception("OPENAI_API_KEY environment variable not found. Please set it to the API key of your OpenAI account.")
        return OpenAiLlm(api_key)
    else:
        raise Exception(f"Unknown LLM source {llm_source}. Please set the LLM_SOURCE environment variable to either 'mock' or 'openai'.")

def _init_kb():
    kb_source = os.environ.get('KB_SOURCE', None)
    if kb_source == 'dblp':
        from .kb.dblp import DblpKb
        return DblpKb()
    elif kb_source == 'local':
        from .kb.local import LocalKb
        fuseki_domain = os.environ.get('FUSEKI_DOMAIN', None)
        fuseki_dataset = os.environ.get('FUSEKI_DATASET', None)
        fuseki_kg = os.environ.get('FUSEKI_KG', None)
        admin_username = os.environ.get('ADMIN_USERNAME', None)
        admin_password = os.environ.get('ADMIN_PASSWORD', None)

        return LocalKb(fuseki_domain, fuseki_dataset, fuseki_kg, admin_username, admin_password)
    else:
        raise Exception(f"Unknown KB source {kb_source}. Please set the KB_SOURCE environment variable to either 'dblp' or 'local'.")

def _log_step(step, result):
    return f"{step}:\n----------\n{result}\n----------\n"

class GptScholar:
    llm = None
    kb = None

    def __init__(self, llm=None, kb=None):
        if llm is None:
            self.llm = _init_llm()
        else:
            self.llm = llm
        if kb is None:
            self.kb = _init_kb()
        else:
            self.kb = kb    
    
    def run(self, prompt, initial_template_id="1", sparql_template_id="1", final_template_id="1"):
        Logger().info(_log_step("Original user promp", prompt))

        llm_session = LlmSession(self.llm)

        llm_prompt = TemplateBuilder("initial", initial_template_id).build(
            user_prompt=prompt,
        )
        Logger().debug(_log_step("LLM prompt for SPARQL", llm_prompt))

        llm_response = llm_session.prompt(llm_prompt)
        Logger().info(_log_step("LLM response for SPARQL", llm_response))

        sparql_query = TemplateBuilder("sparql", sparql_template_id).build(
            llm_response=llm_response,
        )

        kb_results = self.kb.query(sparql_query)
        Logger().info(_log_step("KB reponse", kb_results.raw()))
        Logger().info(_log_step("KB results", kb_results.bindings()))

        final_llm_prompt = TemplateBuilder("final", final_template_id).build(
            kb_bindings=kb_results.bindings(),
            user_prompt=prompt,
        )
        Logger().debug(_log_step("LLM final prompt", final_llm_prompt))

        final_response = llm_session.prompt(final_llm_prompt)
        Logger().info(_log_step("Final response", final_response))

        return {
            "initial_prompt": llm_prompt,
            "sparql_query": sparql_query,
            "kb_results": kb_results.raw(),
            "final_prompt": final_llm_prompt,
            "final_response": final_response
        }
