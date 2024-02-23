import os
import re
import ast
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
BASE_PROMPT = """
Du är en tjänst utformad för att analysera komplexa textdokument, såsom medicinska tidskrifter, och extrahera delar som är relevanta för en specifik uppmaning, med fokus främst på breda ämnen men kan fördjupa sig i specifika detaljer vid förfrågan. Kolla igenom hela dokumentet om det behövs någon ytterligare kontext såsom datum eller plats och ta med det också om det inte specifikt efterfrågas att inte göra det. Den returnerar svar i en Python-lista med strängar för tydliga matchningar. Till exempel, om den blir tillfrågad om knäskador, kommer den att censurera orelaterad information, som detaljer om en förkylning, om den inte specifikt ombeds att inkludera den. Förutom de specifika matchningarna ska den också inkludera relevant kontextinformation såsom kategori av överkänslighet och diagnoserande personal, när sådan information är tillgänglig och relevant för förfrågan. Doc Analyst kan också hantera uteslutningsuppmaningar, som att hämta all information utom specificerade ämnen från ett givet år, och säkerställa att den ursprungliga texten bevaras exakt som den är i svaret.
"""
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(organization="org-sXMg36FtwtvWOC71TH6ida3r", api_key=API_KEY)

def get_chat_response(file_text: str, prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": BASE_PROMPT+"\nfråga: "+prompt},
            {"role": "user", "content": file_text+"\nfråga: "+prompt},
        ],
    )
    response = completion.choices[0].message.content
    return find_python_lists(response)

def find_python_lists(text):
    pattern = r'\[(?:[^\[\]]*|"(?:\\.|[^"\\])*")*\]'
    match = re.search(pattern, text)
    if match:
        return ast.literal_eval(match.group(0))  # Returns the matched list as a string
    return None

