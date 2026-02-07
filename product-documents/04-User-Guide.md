# User Guide

## MedAssist AI - How to Use

---

### 1. Getting Started

MedAssist AI is a healthcare information chatbot that answers your health questions using trusted medical sources. It supports both text and voice interaction.

**Access the application at:** `http://localhost:5173`

---

### 2. Interface Overview

```
+----------------------------------------------------------+
|  [M] MedAssist AI                    📚 40 chunks  🟢 OK |
|      Healthcare Information Assistant                     |
+----------------------------------------------------------+
|                                                          |
|  👋 Hello! I'm MedAssist AI, your healthcare             |
|  information assistant...                                |
|                                                          |
|                          What are symptoms of diabetes?  |
|                                                          |
|  According to the Diabetes Overview guide, common        |
|  symptoms include increased thirst, frequent             |
|  urination, unexplained weight loss...                   |
|  📚 Sources: Diabetes-Overview.pdf (p.1)          🔊    |
|                                                          |
+----------------------------------------------------------+
|  [🎤] [  Ask a health question...            ] [▶ Send] |
|  MedAssist AI provides information only — not medical    |
|  advice. Always consult a healthcare professional.       |
+----------------------------------------------------------+
```

**Header Elements:**
- **Status indicator** (green/yellow/red dot) - shows backend connection status
- **Chunks indexed** - number of document chunks in the knowledge base

**Chat Area:**
- Messages appear in conversation bubbles
- Your messages appear on the right (blue)
- Assistant responses appear on the left (white)

**Input Area:**
- Text input field for typing questions
- Microphone button for voice input
- Send button to submit your question

---

### 3. Asking Questions via Text

1. Click the text input field at the bottom of the screen
2. Type your health question (e.g., "What are the symptoms of high blood pressure?")
3. Press **Enter** or click the **Send** button
4. Wait for the assistant's response (typing indicator will appear)

**Tips for better answers:**
- Be specific: "What are the risk factors for Type 2 diabetes?" works better than "diabetes"
- Ask one question at a time for clearer responses
- Follow up on previous answers for deeper information

---

### 4. Asking Questions via Voice

1. Click the **🎤 microphone button** (left of the text input)
2. The button turns red with a pulse animation when recording
3. Speak your question clearly
4. Click the microphone button again to stop recording, or it will stop automatically
5. Your spoken text appears in the input field and is auto-submitted

**Requirements:**
- Works in Chrome and Edge browsers
- Microphone permission must be granted when prompted
- Quiet environment recommended for better accuracy

---

### 5. Listening to Responses

Each assistant response has a **🔊 speaker button** in the bottom-right corner:

1. Click **🔊** to have the response read aloud
2. Click **🔇** to stop playback
3. Only one response can be read at a time

---

### 6. Understanding Response Types

MedAssist AI uses three types of responses, indicated by colored badges:

#### Standard Answer (No Badge)
The assistant found relevant information and provides a cited answer.
- Includes source citations (document name and page number)
- Ends with a medical advice disclaimer

#### Clarification (❓ Badge)
Your question was too vague or ambiguous. The assistant asks for more details.
- Example: Asking "diabetes" might prompt "Are you asking about Type 1 or Type 2?"
- Provide the requested details to get a specific answer

#### Emergency Escalation (🚨 Badge)
The assistant detected potential emergency symptoms in your question.
- Displays emergency contact numbers (911/999/112)
- Advises seeking immediate medical attention
- Takes priority over all other response types

---

### 7. Source Citations

When the assistant answers from the knowledge base, sources are displayed below the response:

```
📚 Sources:
  Diabetes-Overview.pdf (p.1)    Diabetes-Overview.pdf (p.2)
```

Each source shows:
- **Document name** - which medical guide the information came from
- **Page number** - specific page in the document

---

### 8. Conversation History

- The chat maintains your conversation history during the current session
- The assistant uses your last 6 messages for context
- Follow-up questions are understood in context
- Refreshing the page clears the conversation

---

### 9. Connection Status

The status indicator in the top-right shows the backend connection:

| Indicator | Meaning | Action |
|-----------|---------|--------|
| 🟢 Connected | Backend is running normally | None needed |
| 🟡 Connecting | Attempting to reach backend | Wait a moment |
| 🔴 Disconnected | Backend is not running | Start the backend server |

If disconnected, a yellow warning bar appears with the command to start the server.

---

### 10. Important Disclaimers

- MedAssist AI provides **information only**, not medical advice
- Always consult a qualified healthcare professional for personal medical decisions
- Information is sourced from public health guidelines (WHO, NHS, CDC)
- The system will never diagnose conditions or prescribe medication
- In a medical emergency, always call emergency services directly

---

### 11. Frequently Asked Questions

**Q: What topics can MedAssist AI answer questions about?**
A: Any topic covered by the medical documents in its knowledge base. The default setup includes guides on diabetes, hypertension, cold & flu, mental health, and first aid.

**Q: Can I upload my own medical documents?**
A: Yes, administrators can upload PDF files via the `/upload` API endpoint. Only public, non-confidential medical documents should be used.

**Q: Why did the assistant say "I don't have information on this"?**
A: The question falls outside the topics covered by the knowledge base documents. The assistant only answers from its indexed sources.

**Q: Is my conversation data saved?**
A: No. Conversation history exists only in your browser session and is cleared when you refresh the page. No data is stored on the server.

**Q: Why isn't the microphone button showing?**
A: Voice input requires a browser that supports the Web Speech API (Chrome or Edge). It is not available in Firefox or Safari.
