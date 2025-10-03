// LandingPage.jsx
import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import UploadModal from './Components/UploadModal';

function LandingPage({setUploadedFile}) {
    const navigate = useNavigate();
    const [showUploadModal, setShowUploadModal] = useState(false);

    const handleFileSelect = (file) => {
        if (file) {
            setUploadedFile(file);
            setShowUploadModal(false);
            // navigate("/dashboard");
        }
    }

    return (
        <>
            <div>
                <h1>
                Welcome to App Name!
                </h1>
                <p>Start adding files</p>
                <button 
                onClick={() => setShowUploadModal(true)}
                >
                    Upload File
                </button>
                
            </div>
            <UploadModal
                isOpen={showUploadModal}
                onClose={() => setShowUploadModal(false)}
                onFileSelect={handleFileSelect}
            />

        </>

    )
}

export default LandingPage;