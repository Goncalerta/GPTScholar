class BaseLlm:
    def prompt(self, prompts):
        pass

def _user_message(message):
    return { "role": "user", "content": message }

def _system_message(message):
    return { "role": "system", "content": message }

class LlmSession:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def prompt(self, prompt):
        self.history.append(_user_message(prompt))
        answer = self.llm.prompt(self.history)
        self.history.append(_system_message(answer))
        return answer
