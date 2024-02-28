"use client"
import React, { useState } from 'react';
import axios from 'axios';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';


const UploadForm: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [textPrompt, setTextPrompt] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  const fileSelectedHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    setResponse("");
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const textPromptHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(event.target.value);
  };

  const fileUploadHandler = async () => {
    setResponse("Processing...")
    const formData = new FormData();
    formData.append('file', selectedFile as Blob);
    formData.append('textPrompt', textPrompt);
    try {
      const response = await axios.post('http://localhost:8000/process_pdf', formData, {
        responseType: 'blob',
      });

      // Use JSZip to handle the zip file
      JSZip.loadAsync(response.data).then((zip) => {
        Object.keys(zip.files).forEach((filename) => {
          zip.files[filename].async('blob').then((blob) => {
            // Use file-saver to save the extracted file
            saveAs(blob, filename);
          });
        });
        setResponse('Files are ready for download.');
      });
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
    </div>
  );
};

export default UploadForm;
