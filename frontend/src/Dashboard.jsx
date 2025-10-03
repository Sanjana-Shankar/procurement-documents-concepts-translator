// Dashboard.jsx
import React, { useEffect, useState } from 'react'
import {useNavigate} from 'react-router-dom'
import "./Dashboard.css"

// Dashboard.jsx

function Dashboard({ uploadedFile }) {
  const [parsedData, setParsedData] = useState(null);

  useEffect(() => {
    if (uploadedFile) {
      // Example parsing: just show metadata
      setParsedData({
        name: uploadedFile.name,
        type: uploadedFile.type,
        size: `${(uploadedFile.size / 1024).toFixed(2)} KB`,
      });

      // TODO: Add PDF/image/Excel parsing logic here
    }
  }, [uploadedFile]);

//   if (!uploadedFile) return <p>No file uploaded.</p>;

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-text">Dashboard</h2>
      <div className="dashboard-info">
        <p>Data</p>
        <div className="data-layout"></div>
        <button className="export-button">Export Data</button>
        
      </div>
    </div>
  );
}

export default Dashboard;
