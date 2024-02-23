import os
from api.openai_chat import get_chat_response
from flask import Flask, request, send_file
from flask_cors import CORS

from utils.modify_document import censor, highlight, extract_text_from_pdf

app = Flask(__name__)
CORS(app)

# Your existing functions (censor and highlight) go here without modification


@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    print("request received")
    operation = request.form.get("operation")  # 'censor', 'highlight', or 'both'
    operation = "highlight"
    prompt = request.form.get("textPrompt")  # List of texts to preserve or highlight
    file = request.files["file"]
    if file:
        input_pdf_path = "input.pdf"
        output_pdf_path = "output.pdf"
        file.save(input_pdf_path)  # Temporarily save the uploaded file

        file_text = extract_text_from_pdf(input_pdf_path)
        print("Getting chat response...")
        text_to_preserve = get_chat_response(file_text, prompt)
        # Depending on the operation, call the respective function(s)
        if operation == "censor":
            censor(input_pdf_path, "./server/"+output_pdf_path, text_to_preserve)
        elif operation == "highlight":
            highlight(input_pdf_path, "./server/"+output_pdf_path, text_to_preserve)
        elif operation == "both":
            # For both, you might need to handle intermediate steps or combine functions
            censor(input_pdf_path, "temp.pdf", text_to_preserve)
            highlight("temp.pdf", output_pdf_path, text_to_preserve)
            os.remove("temp.pdf")  # Remove the intermediate file

        return send_file(output_pdf_path, as_attachment=True)

    return "No file provided", 400


if __name__ == "__main__":
    port = "8000"
    print("Starting server at port {port}".format(port=port))
    app.run(host="0.0.0.0", port=port, debug=True)
