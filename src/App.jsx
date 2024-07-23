import React from 'react'
import './App.css'
import ResumeUploader from "./components/ResumeUploader.jsx";
// import ResumeForm from "./components/ResumeForm.jsx"
function App() {
  return (
    <div className="App">

      <main>
        <ResumeUploader />
        {/* <ResumeForm /> */}
      </main>

    </div>
  )
}

export default App