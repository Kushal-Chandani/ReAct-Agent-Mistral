# from guidance import models, gen

# # load a model (could be Transformers, LlamaCpp, VertexAI, OpenAI...)
# llama2 = models.LlamaCpp(path) 

# # append text or generations to the model
# llama2 + f'Do you want a joke or a poem? ' + gen(stop='.')

# Import necessary modules from Guidance AI
from guidance import models, gen

# Specify the path to your Mistral model
mistral_model_path = ""

# Load your Mistral model
mistral_model = models.Mistral(path=mistral_model_path)

# Example function to generate a response
def generate_response(prompt):
    lm = mistral_model + prompt
    response = lm + gen(max_tokens=50)
    return response

if __name__ == "__main__":
    prompt = "Describe a beautiful sunset."
    print(generate_response(prompt))
