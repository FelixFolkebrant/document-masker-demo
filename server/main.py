from api.openai_chat import get_chat_response
from flask import Flask, request
from flask_cors import CORS

# if __name__ == "__main__":
#     prompt = "Hello!"
#     instructions = "You are a helpful bot"
#     test_response = get_chat_response(prompt, instructions)
#     print(test_response)

app = Flask(__name__)
CORS(app)
# Jag vill endast ha all information som behövs för att avgöra patientens reaktion till apelsiner. 
BASE_PROMPT = """
Uppgift: Text Masker är ett verktyg för att dölja viss information i textdokument. Verktyget fokuserar på att arbeta med vetenskapliga artiklar och medicinska journaler. Din uppgift är att dölja delar av texten som inte är relevanta enligt specifika instruktioner, men att behålla resten av texten oförändrad.

Hur det fungerar: När du identifierar ett stycke text som ska döljas, ta bort det stycket eller ordet från texten. Verktyget ändrar inte den övriga texten utan tar endast bort ord eller stycken som inte är relevanta

Vad du behöver veta:

    Du måste vara noggrann och respektera komplexiteten i dokumenten du arbetar med.
    Det är viktigt att hantera medicinsk information försiktigt.

Instruktioner från användaren: Användaren kommer att ge dig specifika instruktioner om vilken information som är relevant och ska behållas synlig. Din uppgift är att följa dessa instruktioner och dölja all annan information.

Om det är oklart: Om det inte är tydligt vilken information som ska döljas, bör du följa användarens instruktioner. Om det fortfarande är oklart kan du förutsätta att inte dölja. 

Exempel:

    Originaltext: Test Testsson har en historia av hjärtsjukdomar och diabetes. Han har också en historia av depression och ångest. Han har tagit medicinen Xanax i 5 år.
    Fråga: Har Test Testsson haft diabetes?
    Modifierad text: Test Testsson har en historia av och diabetes. <mask>Han har också en historia av depression och ångest. Han har tagit medicinen Xanax i 5 år.</mask>

Vad du ska göra: Använd användarens instruktioner för att avgöra vilken information som ska förbli synlig och vilken som ska döljas. Den information som ska vara synlig returneras i en python lista av strings
"""
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    text_prompt = request.form.get('textPrompt')
    if file:
        text = file.read().decode('utf-8')
        instructions = BASE_PROMPT+text_prompt
        processed_text = get_chat_response(prompt=text, instructions=instructions)
        print(processed_text)
    return processed_text

if __name__ == '__main__':
    port = "8000"
    print("Starting server at port {port}".format(port=port))
    app.run(host='0.0.0.0', port=port, debug=True)