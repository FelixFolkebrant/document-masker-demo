"use client"
import React, { useState, useEffect, use } from 'react';
import axios from 'axios';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import HighlightText from './HighlightedText';


const UploadForm: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [textPrompt, setTextPrompt] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [editorText, setEditorText] = useState<string>("");
  const [textToPreserve, setTextToPreserve] = useState<string[]>([]);

  useEffect(() => {
    console.log(textToPreserve);
  }, [textToPreserve]);

  const fileSelectedHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    setResponse("");
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const textPromptHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(event.target.value);
  }

  
const fileUploadHandler2 = async (): Promise<void> => {
  setResponse("Processing...");
  const formData = new FormData();
  formData.append('file', selectedFile as Blob);
  formData.append('textToPreserve', textToPreserve.join('|,|'));

  try {
    const response = await axios.post<ArrayBuffer>('http://localhost:8000/remask', formData, {
      responseType: 'arraybuffer',
      headers: {
        'Accept': 'multipart/form-data'
      }
    });

    const contentType = response.headers['content-type'];
    if (!contentType) throw new Error('Content-Type header missing');

    const match = contentType.match(/boundary=(.+)/);
    if (!match) throw new Error('Boundary not found');
    const boundary = '--' + match[1];

    const rawData = new Uint8Array(response.data);

    // Convert ArrayBuffer to string for easier manipulation
    const decoder = new TextDecoder();
    const dataString = decoder.decode(rawData);

    // Split response data into parts
    const parts = dataString.split(boundary).filter(part => part && part !== '--');

    // Extract and log the message
    const messagePart = parts.find(part => part.includes('Content-Disposition: form-data; name="message"'));
    if (messagePart) {
      const messageContentStart = messagePart.indexOf('\r\n\r\n') + 4;
      const messageContent = messagePart.substring(messageContentStart).trim();
      let decodedString = decodeURIComponent(messageContent.replace(/\+/g, ' '));
      let tmpTest = decodedString.split("|text_to_preserve|=").filter(part => part)[1].replace("\\?", "")
      setTextToPreserve([tmpTest])
      decodedString = decodedString.split("|text_to_preserve|=").filter(part => part)[0]
      decodedString = decodedString.split("|file_text|=")[1]
      setEditorText(decodedString);
      console.log(decodedString)
      console.log(tmpTest)
    }

    // Handle the zip file
    const zipPart = parts.find(part => part.includes('Content-Disposition: form-data; name="file"'));
    if (zipPart) {
      const zipDataIndex = zipPart.indexOf('\r\n\r\n') + 4;
      const zipDataEnd = zipPart.lastIndexOf('\r\n--');
      const zipData = rawData.subarray(zipDataIndex, zipDataEnd); // Adjusted to slice ArrayBuffer directly
      const blob = new Blob([zipData], { type: 'application/zip' });
      const zip = await JSZip.loadAsync(blob); // Changed to blob input
      zip.forEach((path, file) => {
        file.async('blob').then(blob => {
          saveAs(blob, path);
          setResponse('Files are ready for download.');
        });
      });
    }

  } catch (error) {
    console.error(error);
    setResponse('An error occurred while processing the files.');
  }
};

const fileUploadHandler = async (): Promise<void> => {
  setResponse("Processing...");
  const formData = new FormData();
  formData.append('file', selectedFile as Blob);
  formData.append('textPrompt', textPrompt);

  try {
    const response = await axios.post<ArrayBuffer>('http://localhost:8000/process_pdf', formData, {
      responseType: 'arraybuffer',
      headers: {
        'Accept': 'multipart/form-data'
      }
    });

    const contentType = response.headers['content-type'];
    if (!contentType) throw new Error('Content-Type header missing');

    const match = contentType.match(/boundary=(.+)/);
    if (!match) throw new Error('Boundary not found');
    const boundary = '--' + match[1];

    const rawData = new Uint8Array(response.data);

    // Convert ArrayBuffer to string for easier manipulation
    const decoder = new TextDecoder();
    const dataString = decoder.decode(rawData);

    // Split response data into parts
    const parts = dataString.split(boundary).filter(part => part && part !== '--');

    // Extract and log the message
    const messagePart = parts.find(part => part.includes('Content-Disposition: form-data; name="message"'));
    if (messagePart) {
      const messageContentStart = messagePart.indexOf('\r\n\r\n') + 4;
      const messageContent = messagePart.substring(messageContentStart).trim();
      let decodedString = decodeURIComponent(messageContent.replace(/\+/g, ' '));
      let tmpTest = decodedString.split("|text_to_preserve|=").filter(part => part)[1].replace("\\?", "")
      setTextToPreserve([tmpTest])
      decodedString = decodedString.split("|text_to_preserve|=").filter(part => part)[0]
      decodedString = decodedString.split("|file_text|=")[1]
      setEditorText(decodedString);
      console.log(decodedString)
      console.log(tmpTest)
    }

    // Handle the zip file
    const zipPart = parts.find(part => part.includes('Content-Disposition: form-data; name="file"'));
    if (zipPart) {
      const zipDataIndex = zipPart.indexOf('\r\n\r\n') + 4;
      const zipDataEnd = zipPart.lastIndexOf('\r\n--');
      const zipData = rawData.subarray(zipDataIndex, zipDataEnd); // Adjusted to slice ArrayBuffer directly
      const blob = new Blob([zipData], { type: 'application/zip' });
      const zip = await JSZip.loadAsync(blob); // Changed to blob input
      zip.forEach((path, file) => {
        file.async('blob').then(blob => {
          saveAs(blob, path);
          setResponse('Files are ready for download.');
        });
      });
    }

  } catch (error) {
    console.error(error);
    setResponse('An error occurred while processing the files.');
  }
};
  return (
    <div className="mx-auto flex flex-col items-center">
      <input
        type="file"
        id="file"
        onChange={fileSelectedHandler}
        className="hidden"
      />
      <label
        htmlFor="file"
        className="px-4 py-2 bg-blue-500 text-white cursor-pointer"
      >
        Select File
      </label>
      {selectedFile && <p className="mt-2">Selected file: {selectedFile.name}</p>}

      <input
        type="text"
        value={textPrompt}
        onChange={textPromptHandler}
        className="mt-4 px-4 py-2 border-2 border-gray-300"
        placeholder="Enter your text prompt"
      />

      <button
        onClick={fileUploadHandler}
        className="mt-4 px-4 py-2 bg-blue-500 text-white"
      >
        Upload
      </button>
      <div>{response}</div>
      {editorText ?
        <div>
          <button
            onClick={fileUploadHandler2}
            className="mt-4 ml-16 px-4 py-2 bg-blue-500 text-white"
          >Reupload</button>
          <HighlightText
            fullText={editorText}
            maskingStrings={textToPreserve}
            setTextToPreserve = {setTextToPreserve}
          />
        </div>
        :
        <></>
      }
    </div>
  );
};

export default UploadForm;
