import { ArrowUpRight, Sparkles } from "lucide-react";
import { useState } from "react";
import { sendMessage } from "../services/api";

function ChatBox() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!message.trim() || loading) return;

    await sendUserMessage(message.trim());
  };

  const sendUserMessage = async (text) => {
    if (!text.trim() || loading) return;

    const userMessage = text.trim();

    setMessage("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setLoading(true);

    try {
      const data = await sendMessage(
        userMessage,
        conversationId
      );

      // Save the conversation ID returned
      // by the AI API.
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the AI agent.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">

      {/* Header */}

      <div className="chat-header">
        <div className="chat-header-icon">
          <Sparkles size={16} />
        </div>

        <div>
          <span>AI FINANCIAL ASSISTANT</span>
          <small>
            ASK ABOUT YOUR MONEY
          </small>
        </div>
      </div>


      {/* Messages */}

      <div className="messages">

        {messages.length === 0 && (
          <div className="empty-chat">

            <div className="mini-orb">
              <Sparkles size={20} />
            </div>

            <h3>How can I help?</h3>

            <p>
              Ask me about your expenses,
              spending or add a new expense.
            </p>

          </div>
        )}


        {messages.map((item, index) => (
          <div
            key={index}
            className={`message ${
              item.role === "user"
                ? "user-message"
                : "ai-message"
            }`}
          >

            <span>
              {item.role === "user"
                ? "YOU"
                : "AI AGENT"}
            </span>

            <p>{item.content}</p>

          </div>
        ))}


        {/* Typing indicator */}

        {loading && (
          <div className="message ai-message">

            <span>AI AGENT</span>

            <div className="typing-indicator">
              <i></i>
              <i></i>
              <i></i>
            </div>

          </div>
        )}

      </div>


      {/* Input */}

      <form
        className="chat-box"
        onSubmit={handleSubmit}
      >

        <input
          type="text"
          placeholder='Try "I spent ₹500 on groceries"'
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading || !message.trim()}
        >
          {loading ? (
            "THINKING..."
          ) : (
            <>
              SEND
              <ArrowUpRight size={13} />
            </>
          )}
        </button>

      </form>


      {/* Suggestions */}

      {messages.length === 0 && (
        <div className="suggested-prompts">

          <button
            type="button"
            onClick={() =>
              sendUserMessage(
                "Show my expenses"
              )
            }
          >
            Show my expenses
          </button>

          <button
            type="button"
            onClick={() =>
              sendUserMessage(
                "How much did I spend?"
              )
            }
          >
            How much did I spend?
          </button>

          <button
            type="button"
            onClick={() =>
              sendUserMessage(
                "What is my top category?"
              )
            }
          >
            Top category
          </button>

        </div>
      )}

    </div>
  );
}

export default ChatBox;