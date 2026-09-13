import ChatBox from "./ChatBox";

function AgentSection() {
  return (
    <section id="agent" className="agent-section">

      <div className="section-tag">
        02 — YOUR PERSONAL EXPENSE AGENT
      </div>

      <h2>
        TALK TO
        <br />
        <span>YOUR MONEY.</span>
      </h2>

      <div className="agent-window">

        <div className="agent-top">

          <div className="agent-status">
            <span className="status-dot"></span>
            EXPENSE AI — ONLINE
          </div>

          <span className="agent-model">
            GROQ / AI AGENT
          </span>

        </div>

        <ChatBox />

      </div>

    </section>
  );
}

export default AgentSection;