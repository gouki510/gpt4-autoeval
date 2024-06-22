from openai import OpenAI, AzureOpenAI
    

with open("./assets/prompt_eval.txt") as f:
    template_prompt = f.read()

with open("./secrets/OPENAI_API_KEY") as f:
    OPENAI_API_KEY = f.read()

client = OpenAI(api_key=OPENAI_API_KEY)

api_version = "2023-12-01-preview"
endpoint = "https://pj-absol-openai-australia-east.openai.azure.com/"

azure_client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=api_version,
    azure_endpoint=endpoint,
)
