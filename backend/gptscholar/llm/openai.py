from .base_llm import BaseLlm
import openai

class OpenAiLlm(BaseLlm):
    """
    OpenAiLlm is an implementation of the LLM interface that uses the OpenAI API.
    """
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def prompt(self, prompts):
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = prompts,
        )

        answer = completion.choices[0].message.content
        return answer
