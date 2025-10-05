import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {BrowserRouter as Router, Routes, Route, useNavigate} from 'react-router-dom'
import LandingPage from "./LandingPage"
import Dashboard from "./Dashboard"

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);

  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage setUploadedFile={setUploadedFile}/>}/>
        <Route path="/dashboard" element={<Dashboard uploadedFile={uploadedFile} />} />
      </Routes>
    </>
  )
}

export default App
