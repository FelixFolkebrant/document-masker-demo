import os
import zipfile
from time import sleep
from flask import Flask, request, Response
from io import BytesIO
from api.openai_chat import get_chat_response
from flask_cors import CORS
from utils.modify_document import censor, extract_text_from_pdf, highlight
import urllib.parse

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
        if not text_to_preserve:
            return "No text to censor", 400
        print("Chat response received:", text_to_preserve)

        # Perform censor and highlight operations
        censor(input_pdf_path, censored_pdf_path, text_to_preserve)
        highlight(input_pdf_path, highlighted_pdf_path, text_to_preserve)

        print("Zipping files...")
        zip_stream = BytesIO()
        with zipfile.ZipFile(zip_stream, "w") as myzip:
            myzip.write(censored_pdf_path, arcname=os.path.basename(censored_pdf_path))
            myzip.write(
                highlighted_pdf_path, arcname=os.path.basename(highlighted_pdf_path)
            )
        zip_stream.seek(0)

        # Create multipart response
        boundary = "boundary123"

        def generate(encoded_message: str):
            yield f"--{boundary}\r\n"
            yield "Content-Type: application/zip\r\n"
            yield 'Content-Disposition: form-data; name="file"; filename="processed_files.zip"\r\n\r\n'
            yield zip_stream.read()
            yield f"\r\n--{boundary}\r\n"
            yield "Content-Type: text/plain\r\n"
            yield 'Content-Disposition: form-data; name="message"\r\n\r\n'
            yield f"{encoded_message}\r\n"
            yield f"--{boundary}--\r\n"

        # Send the multi-part response
        params = {
            "|file_text|": file_text,
            "|text_to_preserve|": "\?" + "|,|".join(text_to_preserve),
        }
        encoded_message = urllib.parse.urlencode(params)
        print(encoded_message)
        response = Response(
            generate(encoded_message), mimetype=f"multipart/mixed; boundary={boundary}"
        )
        response.headers["Content-Disposition"] = 'attachment; filename="response.zip"'

        # Clean up: delete the temporary files
        print("Deleting temporary files...")

        sleep(2)

        os.remove(input_pdf_path)
        os.remove(censored_pdf_path)
        os.remove(highlighted_pdf_path)
        return response

    return "No file provided", 400


@app.route("/remask", methods=["POST"])
def remask():
    print("Request received")
    text_to_preserve = request.form.get("textToPreserve")
    text_to_preserve = text_to_preserve.split("|,|")
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
        print(text_to_preserve)
        # Perform censor and highlight operations
        censor(input_pdf_path, censored_pdf_path, text_to_preserve)
        highlight(input_pdf_path, highlighted_pdf_path, text_to_preserve)

        print("Zipping files...")
        zip_stream = BytesIO()
        with zipfile.ZipFile(zip_stream, "w") as myzip:
            myzip.write(censored_pdf_path, arcname=os.path.basename(censored_pdf_path))
            myzip.write(
                highlighted_pdf_path, arcname=os.path.basename(highlighted_pdf_path)
            )
        zip_stream.seek(0)

        # Create multipart response
        boundary = "boundary123"

        def generate(encoded_message: str):
            yield f"--{boundary}\r\n"
            yield "Content-Type: application/zip\r\n"
            yield 'Content-Disposition: form-data; name="file"; filename="processed_files.zip"\r\n\r\n'
            yield zip_stream.read()
            yield f"\r\n--{boundary}\r\n"
            yield "Content-Type: text/plain\r\n"
            yield 'Content-Disposition: form-data; name="message"\r\n\r\n'
            yield f"{encoded_message}\r\n"
            yield f"--{boundary}--\r\n"

        # Send the multi-part response
        params = {
            "|file_text|": file_text,
            "|text_to_preserve|": "\?" + "|,|".join(text_to_preserve),
        }
        encoded_message = urllib.parse.urlencode(params)
        response = Response(
            generate(encoded_message), mimetype=f"multipart/mixed; boundary={boundary}"
        )
        response.headers["Content-Disposition"] = 'attachment; filename="response.zip"'

        # Clean up: delete the temporary files
        print("Deleting temporary files...")

        sleep(2)

        os.remove(input_pdf_path)
        os.remove(censored_pdf_path)
        os.remove(highlighted_pdf_path)
        return response

    return "No file provided", 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server at port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
