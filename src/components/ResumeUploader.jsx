// import React, { useState } from 'react';
// import axios from 'axios';
// import { MdCloudUpload, MdDelete } from 'react-icons/md';
// import { AiFillFileImage } from 'react-icons/ai';
// import { Worker, Viewer } from '@react-pdf-viewer/core';
// import { toolbarPlugin } from '@react-pdf-viewer/toolbar';
// import { zoomPlugin } from '@react-pdf-viewer/zoom';
// import '@react-pdf-viewer/core/lib/styles/index.css';
// import '@react-pdf-viewer/toolbar/lib/styles/index.css';
// import '@react-pdf-viewer/zoom/lib/styles/index.css';
// import './uploader.css';

// function ResumeUploader() {
//   const [file, setFile] = useState(null);
//   const [fileName, setFileName] = useState("No selected file");
//   const [isLoading, setIsLoading] = useState(false);

//   const toolbarPluginInstance = toolbarPlugin();
//   const { renderDefaultToolbar } = toolbarPluginInstance;
//   const zoomPluginInstance = zoomPlugin();

//   const handleFileChange = (event) => {
//     const selectedFile = event.target.files[0];
//     setFile(selectedFile);
//     if (selectedFile) {
//       setFileName(selectedFile.name);
//     }
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       alert('Please select a file first!');
//       return;
//     }

//     const formData = new FormData();
//     formData.append('resume', file);

//     setIsLoading(true);

//     try {
//       const response = await axios.post('http://127.0.0.1:5000/api/upload-resume', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });

//       console.log(response.data);
//       // Handle the response data as needed
//     } catch (error) {
//       console.error('Error uploading file:', error.response ? error.response.data : error.message);
//       alert('An error occurred while uploading the file.');
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <main>
//       <form onClick={() => document.querySelector(".input-field").click()}>
//         <input 
//           type="file" 
//           accept=".pdf" 
//           className='input-field' 
//           hidden 
//           onChange={handleFileChange} 
//         />
//         {file ? (
//           <AiFillFileImage color='#1475cf' size={60} />
//         ) : (
//           <>
//             <MdCloudUpload color='#1475cf' size={60} />
//             <p>Browse Files to upload</p>
//           </>
//         )}
//       </form>

//       <section className='uploaded-row'>
//         <AiFillFileImage color='#1475cf' />
//         <span className='upload-content'>
//           {fileName} - 
//           <MdDelete
//             onClick={() => {
//               setFile(null);
//               setFileName("No selected File");
//             }}
//           />
//         </span>
//       </section>

//       {file && (
//         <div className="pdf-preview">
//           <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
//             <Viewer 
//               fileUrl={URL.createObjectURL(file)} 
//               plugins={[toolbarPluginInstance, zoomPluginInstance]}
//             />
//           </Worker>
//           {renderDefaultToolbar()}
//         </div>
//       )}

//       <button onClick={handleUpload} disabled={isLoading}>
//         {isLoading ? 'Extracting...' : 'Upload and Extract'}
//       </button>
//     </main>
//   );
// }

// export default ResumeUploader;

















import React, { useState } from 'react';
import axios from 'axios';
import { MdCloudUpload, MdDelete } from 'react-icons/md';
import { AiFillFileImage } from 'react-icons/ai';
import { Worker, Viewer } from '@react-pdf-viewer/core';
import { toolbarPlugin } from '@react-pdf-viewer/toolbar';
import { zoomPlugin } from '@react-pdf-viewer/zoom';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/toolbar/lib/styles/index.css';
import '@react-pdf-viewer/zoom/lib/styles/index.css';
import './uploader.css';

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("No selected file");
  const [isLoading, setIsLoading] = useState(false);

  const toolbarPluginInstance = toolbarPlugin();
  const { renderDefaultToolbar } = toolbarPluginInstance;
  const zoomPluginInstance = zoomPlugin();

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      setFileName(selectedFile.name);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/upload-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log(response.data);
      // Handle the response data as needed
    } catch (error) {
      console.error('Error uploading file:', error.response ? error.response.data : error.message);
      alert('An error occurred while uploading the file.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main>
      {!file && (
        <form onClick={() => document.querySelector(".input-field").click()}>
          <input 
            type="file" 
            accept=".pdf" 
            className='input-field' 
            hidden 
            onChange={handleFileChange} 
          />
          <MdCloudUpload color='#1475cf' size={60} />
          <p>Browse Files to upload</p>
        </form>
      )}

      {isLoading && (
        <div className="loading-animation">
          <p>Uploading...</p>
        </div>
      )}

      {!isLoading && file && (
        <>
          <section className='uploaded-row'>
            <AiFillFileImage color='#1475cf' />
            <span className='upload-content'>
              {fileName} - 
              <MdDelete
                onClick={() => {
                  setFile(null);
                  setFileName("No selected File");
                }}
              />
            </span>
          </section>

          <div className="pdf-preview">
            <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
              <Viewer 
                fileUrl={URL.createObjectURL(file)} 
                plugins={[toolbarPluginInstance, zoomPluginInstance]}
              />
            </Worker>
            {renderDefaultToolbar()}
          </div>

          <button onClick={handleUpload} disabled={isLoading}>
            {isLoading ? 'Extracting...' : 'Upload and Extract'}
          </button>
        </>
      )}
    </main>
  );
}

export default ResumeUploader;
