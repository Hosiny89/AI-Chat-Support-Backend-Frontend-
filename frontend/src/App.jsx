import React, { useState } from "react";
import ReactMarkdown from "react-markdown";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    // أضيف رسالة المستخدم
    setMessages((prev) => [...prev, { role: "user", content: input }]);

    // أضيف placeholder للرد بتاع الـ AI
    const aiIndex = messages.length + 1; // مكان الرسالة بتاعت AI
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    const userMessage = input;
    setInput("");

    try {
      const res = await fetch(
        "https://congenial-fiesta-9vqxqx779rcp6r6-8000.app.github.dev/api/chat/stream",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_message: userMessage }),
        }
      );

      if (!res.ok) {
        throw new Error("Server error");
      }

      // التعامل مع StreamingResponse
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = ""; // <-- هنا هنخزن الرد كاملاً بدون تكرار

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        // كل مرة نحدّث الرسالة الأخيرة بالـ buffer كله
        setMessages((prev) => {
          const updated = [...prev];
          updated[aiIndex].content = buffer;
          return updated;
        });
      }
    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "AI: حدث خطأ في الاتصال بالـ server" },
      ]);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Chat with AI</h1>

      {/* عرض الرسائل */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          height: "300px",
          overflowY: "auto",
          marginBottom: "20px",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              margin: "5px 0",
              textAlign: msg.role === "user" ? "right" : "left",
            }}
          >
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
      </div>

      {/* إدخال الرسالة */}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
          }
        }}
        placeholder="Ask anything"
        style={{ width: "300px", marginRight: "10px" }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;




