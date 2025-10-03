// Dashboard.jsx
import React, { useEffect, useState } from 'react'
import {useNavigate} from 'react-router-dom'

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
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="bg-gray-100 p-4 rounded">
        <p><strong>File Name:</strong> {parsedData?.name}</p>
        <p><strong>Type:</strong> {parsedData?.type}</p>
        <p><strong>Size:</strong> {parsedData?.size}</p>
      </div>
    </div>
  );
}

export default Dashboard;
