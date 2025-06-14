import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import axios from "axios";

function Home() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a resume file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const response = await axios.post("http://localhost:8000/parse-resume", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Check console.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await axios.get("http://localhost:8000/download-pdf", {
        responseType: "blob",
      });

      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "parsed_resume.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("PDF download failed:", error);
    }
  };

  return (
    <div style={styles.mainContent}>
      <h1 style={styles.header}>AI Resume Parser</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading} style={styles.button}>
        {loading ? "Uploading..." : "Upload Resume"}
      </button>

      {result && (
        <div style={styles.result}>
          <h3>Results</h3>
          <p><strong>Name:</strong> {result.resume_data?.name}</p>
          <p><strong>Email:</strong> {result.resume_data?.email}</p>
          <p><strong>Phone:</strong> {result.resume_data?.phone}</p>
          <p><strong>Skills:</strong> {result.resume_data?.skills.join(", ")}</p>
          <p><strong>Match Score:</strong> {result.match_score}</p>
          <button onClick={handleDownloadPDF} style={styles.button}>Download PDF</button>
        </div>
      )}
    </div>
  );
}

function About() {
  return (
    <div style={styles.mainContent}>
      <h2>About</h2>
      <p>This is an AI-based Resume Parser web application.This shows a match_score based on Some predefined parameters.This is intended to help HR processes and assessment of CVs automatically</p>
    </div>
  );
}

function Contact() {
  return (
    <div style={styles.mainContent}>
      <h2>Contact</h2>
      <p>Email us at: resumeParsersupport@example.com</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div style={styles.appContainer}>
        <nav style={styles.sidebar}>
          <h2 style={styles.logo}>Resume Parser</h2>
          <Link to="/" style={styles.navLink}>Home</Link>
          <Link to="/about" style={styles.navLink}>About</Link>
          <Link to="/contact" style={styles.navLink}>Contact</Link>
        </nav>
        <div style={styles.contentArea}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

const styles = {
  appContainer: {
    display: "flex",
    minHeight: "100vh",
    fontFamily: "Arial, sans-serif",
  },
  sidebar: {
    width: "200px",
    backgroundColor: "#2c3e50",
    color: "#fff",
    display: "flex",
    flexDirection: "column",
    padding: "1rem",
  },
  logo: {
    marginBottom: "2rem",
    fontSize: "1.5rem",
    borderBottom: "1px solid #7f8c8d",
    paddingBottom: "1rem",
  },
  navLink: {
    color: "#ecf0f1",
    textDecoration: "none",
    marginBottom: "1rem",
    fontSize: "1rem",
  },
  contentArea: {
    flex: 1,
    padding: "2rem",
    backgroundColor: "#f4f4f4",
  },
  mainContent: {
    maxWidth: "700px",
    margin: "0 auto",
  },
  header: {
    fontSize: "2rem",
    marginBottom: "1rem",
  },
  button: {
    marginTop: "1rem",
    padding: "0.5rem 1rem",
    fontSize: "1rem",
    cursor: "pointer",
  },
  result: {
    marginTop: "2rem",
    backgroundColor: "#fff",
    padding: "1rem",
    border: "1px solid #ccc",
    borderRadius: "8px",
  },
};

export default App;
