import React, { useState } from "react";
import API from "../api/axios";

function Feedback() {
  const [text, setText] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("feedback/", { feedback: text });
      setSubmitted(true);
      setText("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container mt-4">
      <h3>📝 Feedback</h3>
      {submitted && <div className="alert alert-success">Thank you for your feedback!</div>}
      <form onSubmit={handleSubmit}>
        <textarea
          className="form-control mb-2"
          rows="4"
          placeholder="Enter your feedback..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        />
        <button className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
}

export default Feedback;
