"use client";
import { useState } from 'react';
import axios from 'axios';

const UploadForm: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [textPrompt, setTextPrompt] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  const fileSelectedHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const textPromptHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTextPrompt(event.target.value);
  };

  const fileUploadHandler = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile as Blob);
    formData.append('textPrompt', textPrompt); // Add the text prompt to the form data
    try {
      const response = await axios.post('http://localhost:8000/process_pdf', formData, {
        responseType: 'blob', // Important: This tells axios to handle the response as a Blob
      });

      // Create a URL for the blob
      const fileURL = window.URL.createObjectURL(new Blob([response.data]));
      
      // Create a temporary anchor tag and trigger the download
      const link = document.createElement('a');
      link.href = fileURL;
      link.setAttribute('download', 'file.pdf'); // Set the file name for the download
      document.body.appendChild(link);
      link.click();

      // Clean up by removing the temporary link
      if (link.parentNode) {
        link.parentNode.removeChild(link);
      }

      // Optional: Update the UI to indicate the file is being downloaded
      setResponse('Downloading file...');
    } catch (error) {
      console.error(error);
      setResponse('An error occurred while processing the file.');
    }
  };

  return (
    <div className="mx-auto flex flex-col items-center">
      <input
        type="file"
        id="file"
        onChange={fileSelectedHandler}
        className="hidden" // hide the actual input
      />
      <label
        htmlFor="file"
        className="px-4 py-2 bg-blue-500 text-white cursor-pointer" // style the label as you like
      >
        Select File
      </label>
      {selectedFile && <p className="mt-2">Selected file: {selectedFile.name}</p>}

      {/* Text Prompt Input */}
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
