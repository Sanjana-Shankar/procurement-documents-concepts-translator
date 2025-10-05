import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Download, X, MessageCircle, Send } from "lucide-react"; // optional icon
import "./Dashboard.css";


function Dashboard() {
  const location = useLocation();
  const data = location.state?.data || []; // ✅ Safe fallback if undefined
  const [showChat, setShowChat] = useState(false)
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi 👋, I'm your Spend Assistant! Ask me anything about your data or uploaded documents." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [enrichedData, setEnrichedData] = useState([]);
  {/* Only uses the threshold fetch whenever data changes */} 
  useEffect(() => {
    const fetchThresholds = async () => {
      if (!data || data.length === 0) return;
    
      try {
        const res = await fetch("http://127.0.0.1:8000/spend/check-thresholds", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
    
        const enriched = await res.json();
        setEnrichedData(enriched);
      } catch (err) {
        console.error("Error fetching thresholds:", err);
        setEnrichedData(data); // fallback to original data if error
      }
    };
    fetchThresholds();
  }, [data]);

   // 🧾 CSV Export Function
   const handleExportCSV = () => {
    if (!data || data.length === 0) {
      alert("No data to export!");
      return;
    }

    // Extract table headers dynamically
    const headers = Object.keys(enrichedData[0] || {});

    // Build CSV content
    const csvRows = [
      headers.join(","), // header row
      ...enrichedData.map((row) =>
        headers.map((header) => JSON.stringify(row[header] ?? "")).join(",")
      ),
    ];

    const csvContent = csvRows.join("\n");

    // Create a downloadable Blob
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    // Create download link dynamically
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;

    const currentDate = new Date().toISOString().split("T")[0];
    link.download = `normalized_spend_report_${currentDate}.csv`;
    document.body.appendChild(link);
    link.click();

    // Clean up
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Handle chatbot message send
  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chatbot/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });

      const data = await res.json();
      const botMessage = { sender: "bot", text: data.answer || "No answer found." };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "⚠️ Error connecting to chatbot." }]);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="dashboard-container">
      <h2 className="dashboard-text">Dashboard</h2>

      <div className="dashboard-info">
        <h3 className="table-title">📊 Normalized Spend Table</h3>

        {data.length === 0 ? (
          <p className="no-data-text">No data available. Please upload a file first.</p>
        ) : (
          <div className="table-wrapper">
            <table className="data-table fancy-table">
              <thead>
                <tr>
                  <th>Description</th>
                  <th>Amount</th>
                  <th>Category</th>
                  <th>Spend Type</th>
                </tr>
              </thead>
              <tbody>
                {enrichedData.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.description}</td>
                    <td>{item.amount}{item.is_over_budget && <span className="warning-icon"> ⚠️</span>}</td>
                    <td>{item.category}</td>
                    <td>{item.spend_type}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/*Displaying explanations under the table */}
        <div className="threshold-explanations">
          {enrichedData.map(
            (item, idx) =>
              item.is_over_budget && (
                <p key={idx} className="explanation-text">
                  {item.explanation}
                </p>
              )
          )}
        </div>

        <button className="export-button" onClick={handleExportCSV}>
          <Download className="inline-block w-5 h-5 mr-2" />
          ⬇️ Export CSV
        </button>
      </div>

    {/* 💬 Floating Chat Button */}
    <button className="chat-button" onClick={() => setShowChat(!showChat)}>
      {showChat ? <X size={20} /> : <MessageCircle size={24} />}
    </button>

    {/* 🪟 Chat Window */}
    {showChat && (
      <div className="chat-window">
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
          {loading && <div className="chat-message bot">Thinking...</div>}
        </div>

        <div className="chat-input-area">
          <input
            type="text"
            placeholder="Ask about your spend data..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button className="send-btn" onClick={handleSend}>
            <Send size={18} />
          </button>
        </div>
      </div>
    )}
  </div>
    
  );
}


export default Dashboard;