// LandingPage.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import UploadModal from "./Components/UploadModal";
import "./LandingPage.css";

function LandingPage({ setUploadedFile }) {
  const navigate = useNavigate();
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [documentData, setDocumentData] = useState(null)

  const handleFileSelect = (data) => {
    console.log("✅ Extracted data received in LandingPage:", data);
    if (data) {
      // Save JSON response to state
      setDocumentData(data);
  
      // Optional: if you also want to keep original file
      setUploadedFile(data.originalFile || null);
  
      // Close the modal
      setShowUploadModal(false);

      // Navigate to dashboard
      navigate("/dashboard", { state: { data } });
  
      // Optional: navigate to dashboard
      // navigate("/dashboard");
    }
  };

  return (
    <>
      <div className="landing-container">
        <div className="intro-message">
            <h1 className="landing-title">
                Welcome to <span className="app-gradient">BudgetIQ!</span>
            </h1>
            <p className="landing-subtitle">This is a Procurement Spend Normalizer that extracts invoices, PDFs, spreadsheets, and etc and categorizes it in a smart way for easy readability and convenience.</p>
            <p className="landing-subtitle">
                Our app automatically extracts and standardizes spend data from PDFs, scans, and spreadsheets, then makes it instantly searchable with a natural language chatbot.
            </p>
            <p className="landing-subtitle">
            Start adding your files to get results instantly
            </p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="upload-btn"
        >
          Upload File
        </button>
      </div>

      <UploadModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onFileSelect={handleFileSelect}
      />
      {/*}
      {documentData && (
        <pre>{JSON.stringify(documentData, null, 2)}</pre>
      )}
      */}
    </>
  );
}

export default LandingPage;
