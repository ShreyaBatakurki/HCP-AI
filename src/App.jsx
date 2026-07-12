import React, { useState, useEffect } from "react";

function App() {
  const [doctorName, setDoctorName] = useState("");
  const [hospital, setHospital] = useState("");
  const [topics, setTopics] = useState("");
  const [aiText, setAiText] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [history,setHistory]= useState([]);

  const saveInteraction = async () => {

    try {
      const response = await fetch("http://127.0.0.1:8000/log-interaction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
    doctor_name: doctorName,
    hospital: hospital,
    topics: topics,
    ai_response: aiResponse,

        }),
      });

      const data = await response.json();
      alert(data.message);
      await getHistory();

      setDoctorName("");
      setHospital("");
      setTopics("");
    } catch (error) {
      alert("Failed to save interaction");
    }
  };
  const getHistory = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/interactions");
        const data = await response.json();
        setHistory(data);
    } catch (error) {
        console.log(error);
    }
};
useEffect(() => {
    getHistory();
}, []);

  const askAI = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/ask-ai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: aiText,
        }),
      });

      const data = await response.json();
      setAiResponse(data.response);
    } catch (error) {
      alert("AI request failed");
    }
  };

  return (
    <div
      style={{
        fontFamily: "Arial",
        background: "#f4f6f9",
        minHeight: "100vh",
        padding: "20px",
      }}
    >
      <h1 style={{ textAlign: "center" }}>Log HCP Interaction</h1>

      <div style={{ display: "flex", gap: "20px", marginTop: "30px" }}>
        <div
          style={{
            flex: 2,
            background: "white",
            padding: "20px",
            borderRadius: "10px",
          }}
        >
          <h2>Interaction Details</h2>

          <input
            type="text"
            placeholder="Doctor Name"
            value={doctorName}
            onChange={(e) => setDoctorName(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
          />

          <input
            type="text"
            placeholder="Hospital"
            value={hospital}
            onChange={(e) => setHospital(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
          />

          <textarea
            rows="5"
            placeholder="Topics Discussed"
            value={topics}
            onChange={(e) => setTopics(e.target.value)}
            style={{ width: "100%", padding: "10px" }}
          />

          <br />
          <br />

          <button
            onClick={saveInteraction}
            style={{
              padding: "10px 20px",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Save Interaction
          </button>
        </div>

        <div
          style={{
            flex: 1,
            background: "white",
            padding: "20px",
            borderRadius: "10px",
          }}
        >
          <h2>AI Assistant</h2>

          <textarea
            rows="8"
            placeholder="Describe interaction..."
            value={aiText}
            onChange={(e) => setAiText(e.target.value)}
            style={{ width: "100%", padding: "10px" }}
          />

          <br />
          <br />

          <button
            onClick={askAI}
            style={{
              width: "100%",
              padding: "10px",
              background: "#16a34a",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Ask AI
          </button>

          <br />
          <br />

          <textarea
            rows="8"
            value={aiResponse}
            readOnly
            placeholder="AI Response"
            style={{
              width: "100%",
              padding: "10px",
              background: "#f9f9f9",
            }}
          />
        </div>
      </div>
      <h2>Interaction History</h2>

<table border="1" cellPadding="8">
  <thead>
    <tr>
      <th>ID</th>
      <th>Doctor</th>
      <th>Hospital</th>
      <th>Topics</th>
      <th>AI Response</th>
      <th>Date</th>
    </tr>
  </thead>

  <tbody>
    {history.map((item) => (
  <tr key={item.id}>
    <td>{item.id}</td>
    <td>{item.doctor_name}</td>
    <td>{item.hospital}</td>
    <td>{item.topics}</td>

    <td
  style={{
    width: "350px",
    minWidth: "350px",
    maxWidth: "350px",
    padding: "10px",
    verticalAlign: "top",
  }}
>
  <div
    style={{
      height: "120px",
      overflowY: "auto",
      overflowX: "hidden",
      whiteSpace: "pre-wrap",
      wordBreak: "break-word",
    }}
  >
    {item.ai_response}
  </div>
</td>

    <td>{item.created_at}</td>
  </tr>
))}
  </tbody>
</table>
    </div>
  );
}

export default App;