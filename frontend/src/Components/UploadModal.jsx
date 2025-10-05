
// UploadModal.jsx
import React, {useState, useRef} from "react";
import { useNavigate } from "react-router-dom"; 
import "./UploadModal.css"

function UploadModal({ isOpen, onClose, onFileSelect }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  if (!isOpen) return null; // don’t render unless open

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/document/extract", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to extract document");
      }

      const data = await response.json();
      console.log("✅ Extracted JSON from API:", data);

      // Step 2: Send extracted data to normalization endpoint
      const normalizeResponse = await fetch("http://127.0.0.1:8000/document/normalize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ line_items: data.line_items || data || [] }),
      });

      if (!normalizeResponse.ok) throw new Error("Failed to normalize document");

      const normalizedData = await normalizeResponse.json();
      console.log("✅ Normalized Data:", normalizedData);


      // Navigate to Dashboard with extracted JSON
      //navigate("/dashboard", { state: { extractedData: data } });
      // Pass extracted JSON to parent (LandingPage)
      onFileSelect(normalizedData);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to extract document. See console for details.");
    } finally {
      setIsLoading(false);
    }
  };

  // const handleDrop = (event) => {
  //   event.preventDefault();
  //   setIsDragging(false);
  //   const file = event.dataTransfer.files[0];
  //   if (file) onFileSelect(file);
  // };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div 
        className="modal-container" 
        onClick={(e) => e.stopPropagation()}
      >
        {isLoading? (
          <div className="loader"></div>
        ) :(
          <>
            <h2 className="upload-title">Upload a File</h2>
            <div className="drag-area">
              <p>Drag and Drop file here</p>
              <p>Or</p>
              <button className="browse-button" onClick={triggerFileInput}>
                Browse File
              </button>
            </div>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf, image/*, .xlsx, .xls"
                    className="uploadFile-hidden-input"
                    onChange={handleFileChange}
                />
            <button className="cancel-button" onClick={onClose}>Cancel</button>
          </>
        )}
        
      </div>
    </div>
  );
}

export default UploadModal;
