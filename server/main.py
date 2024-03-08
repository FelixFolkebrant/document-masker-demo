import os
import tempfile
import zipfile
from time import sleep

from api.openai_chat import get_chat_response
from flask import Flask, request, send_file
from flask_cors import CORS
from utils.modify_document import censor, extract_text_from_pdf, highlight

app = Flask(__name__)
CORS(app)


@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    print("Request received")
    prompt = request.form.get("textPrompt")
    file = request.files["file"]
    if file:
        # Define file paths
        input_pdf_path = os.path.join("server", "input.pdf")
        censored_pdf_path = os.path.join("server", "censored_output.pdf")
        highlighted_pdf_path = os.path.join("server", "highlighted_output.pdf")

        # Temporarily save the uploaded file
        file.save(input_pdf_path)

        # Extract text from PDF and get the chat response
        file_text = extract_text_from_pdf(input_pdf_path)
        print("Getting chat response...")
        text_to_preserve = get_chat_response(file_text, prompt)
        print("Chat response received:", text_to_preserve)

        # Perform censor and highlight operations
        censor(input_pdf_path, censored_pdf_path, text_to_preserve)
        highlight(input_pdf_path, highlighted_pdf_path, text_to_preserve)

        # Create a temporary zip file
        print("Zipping files...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            with zipfile.ZipFile(tmp.name, "w") as myzip:
                myzip.write(
                    censored_pdf_path, arcname=os.path.basename(censored_pdf_path)
                )
                myzip.write(
                    highlighted_pdf_path, arcname=os.path.basename(highlighted_pdf_path)
                )
            # Send the zip file
            print("Sending zip file...")
            response = send_file(
                tmp.name, as_attachment=True, download_name="processed_files.zip"
            )

        # Clean up: delete the temporary files
        print("Deleting temporary files...")

        sleep(5)

        os.remove(input_pdf_path)
        os.remove(censored_pdf_path)
        os.remove(highlighted_pdf_path)
        return response

    return "No file provided", 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server at port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
