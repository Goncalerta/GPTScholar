import sys
import itertools
from .base_llm import BaseLlm

class MockLlm(BaseLlm):
    """
    MockLlm is a mock implementation of the LLM interface for testing purposes.
    It asks the standard input of the server to input the response to the prompt.
    """
    def prompt(self, prompts):
        print(f"Please enter the answer to the following prompt:\n----------\n{prompts[-1]['content']}\n----------\nWhen you are done, type '&send' and press enter.\n")
        return "".join(itertools.takewhile(lambda x: x != '&send\n', sys.stdin))
