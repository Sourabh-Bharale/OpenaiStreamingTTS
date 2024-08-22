import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_CLIENT = openai.OpenAI()
