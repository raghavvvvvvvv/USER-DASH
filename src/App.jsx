import React from 'react'
import './App.css'
import ResumeUploader from "./components/ResumeUploader.jsx";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Resume Text Extractor</h1>
      </header>
      <main>
        <ResumeUploader />
      </main>
      <footer>
        <p>© 2024 Resume Text Extractor</p>
      </footer>
    </div>
  )
}

export default App