// UploadModal.jsx
import React, {useState, useRef} from "react";
import "./UploadModal.css"

function UploadModal({ isOpen, onClose, onFileSelect }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  if (!isOpen) return null; // don’t render unless open

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // show loading spinner
      setIsLoading(true);
      // simulate parse
      setTimeout(() => {
        onFileSelect(file);
        setIsLoading(false);
      }, 2000)
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
