class TemplateBuilder:
    def __init__(self, type, template):
        self.type = type
        self.template = template
    
    def get_filepath(self):
        return f"gptscholar/templates/{self.type}/{self.template}.txt"

    def build(self, **kwargs):
        with open(self.get_filepath(), 'r') as f:
            return f.read().format(**kwargs)
