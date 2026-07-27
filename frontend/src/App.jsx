import { useState } from "react";
import {
  Upload,
  FileText,
  Loader2,
  MessageCircle,
  AlertTriangle,
  CheckCircle,
  Activity,
  Stethoscope,
} from "lucide-react";

import "./App.css";

function App() {
  const API_URL = import.meta.env.VITE_API_URL;

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [asking, setAsking] = useState(false);

  // --------------------------------
  // Select File
  // --------------------------------

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) return;

    setFile(selectedFile);
    setResult(null);
    setAnswer("");
    setError("");
  };

  // --------------------------------
  // Analyze Medical Report
  // --------------------------------

  const analyzeReport = async () => {
    if (!file) {
      setError("Please select a medical report first.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    const formData = new FormData();

    formData.append("file", file);

    try {
      console.log("Uploading file:", file.name);

      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log("Backend response:", data);

      if (!response.ok) {
        throw new Error(data.detail || "Failed to analyze report");
      }

      setResult(data);
    } catch (error) {
      console.error(error);

      setError(error.message || "Unable to connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------
  // Ask My Report
  // --------------------------------

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    if (!result) {
      return;
    }

    setAsking(true);
    setAnswer("");
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/ask`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: question,
          report_context: result.extracted_text,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get answer");
      }

      setAnswer(data.answer);
    } catch (error) {
      console.error(error);

      setError(error.message || "Unable to get answer.");
    } finally {
      setAsking(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}

      <header className="header">
        <div className="brand">
          <div className="brand-icon">
            <Activity size={28} />
          </div>

          <div>
            <h1>MedExplain AI</h1>

            <p>Understand your medical reports in simple language</p>
          </div>
        </div>
      </header>

      <main className="container">
        {/* Upload Card */}

        <section className="upload-card">
          <div className="upload-circle">
            <Upload size={32} />
          </div>

          <h2>Upload Your Medical Report</h2>

          <p className="subtitle">
            Upload a blood test or medical report in PDF or image format.
          </p>

          <label className="file-picker">
            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={handleFileChange}
            />

            <FileText size={22} />

            <span>{file ? file.name : "Choose Medical Report"}</span>
          </label>

          {file && (
            <div className="selected-file">
              <FileText size={18} />

              <span>Selected: {file.name}</span>
            </div>
          )}

          <button
            className="analyze-button"
            onClick={analyzeReport}
            disabled={loading || !file}
          >
            {loading ? (
              <>
                <Loader2 size={20} className="spin" />
                Analyzing Report...
              </>
            ) : (
              <>
                <Activity size={20} />
                Analyze Report
              </>
            )}
          </button>

          {error && (
            <div className="error-message">
              <AlertTriangle size={20} />

              <span>{error}</span>
            </div>
          )}
        </section>

        {/* Results */}

        {result && (
          <section className="results-section">
            {/* Summary */}

            <div className="summary-card">
              <div className="section-title">
                <Stethoscope size={24} />

                <h2>AI Report Summary</h2>
              </div>

              <p>{result.analysis.summary}</p>
            </div>

            {/* Test Results */}

            <h2 className="section-heading">Medical Test Results</h2>

            <div className="results-grid">
              {result.analysis.results.map((item, index) => (
                <div className="result-card" key={index}>
                  <div className="result-header">
                    <h3>{item.test_name}</h3>

                    <span className={`status ${item.status.toLowerCase()}`}>
                      {item.status === "Normal" ? (
                        <CheckCircle size={16} />
                      ) : (
                        <AlertTriangle size={16} />
                      )}

                      {item.status}
                    </span>
                  </div>

                  <div className="test-value">
                    {item.value}

                    <span> {item.unit}</span>
                  </div>

                  <div className="reference">
                    <strong>Reference Range</strong>

                    <p>{item.reference_range}</p>
                  </div>

                  <div className="explanation">
                    <strong>Simple Explanation</strong>

                    <p>{item.explanation}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Doctor Questions */}

            <div className="questions-card">
              <div className="section-title">
                <Stethoscope size={24} />

                <h2>Questions to Ask Your Doctor</h2>
              </div>

              <ul>
                {result.analysis.questions_for_doctor.map((question, index) => (
                  <li key={index}>{question}</li>
                ))}
              </ul>
            </div>

            {/* Ask My Report */}

            <div className="ask-card">
              <div className="section-title">
                <MessageCircle size={24} />

                <h2>Ask My Report</h2>
              </div>

              <p className="subtitle">
                Ask a question about the information in your report.
              </p>

              <div className="question-box">
                <input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      askQuestion();
                    }
                  }}
                  placeholder="What does my hemoglobin value mean?"
                />

                <button onClick={askQuestion} disabled={asking}>
                  {asking ? "Thinking..." : "Ask"}
                </button>
              </div>

              {answer && (
                <div className="answer-box">
                  <strong>AI Explanation</strong>

                  <p>{answer}</p>
                </div>
              )}
            </div>

            {/* Disclaimer */}

            <div className="disclaimer">
              <AlertTriangle size={22} />

              <div>
                <strong>Important Medical Disclaimer</strong>

                <p>
                  This application is for educational purposes only. It does not
                  provide medical diagnosis or treatment. Always consult a
                  qualified healthcare professional for medical advice.
                </p>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
