import React, { useState } from "react";
import "./Modal.css";

export default function Modal({ onSubmit, onCancel }) {
  const [text, setText] = useState("");
  const [isChecked, setIsChecked] = useState(false);

  const handleSubmit = () => {
    onSubmit({ fuzzerTime: text, noTime: isChecked });
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Enter time for fuzzer</h2>
        <div style={{ height: '1rem' }}></div>
        <input
          placeholder="Enter time"
          value={text}
          disabled={isChecked}
          onChange={(e) => setText(e.target.value)}
        />
        <div>
          <input
            type="checkbox"
            id="check"
            checked={isChecked}
            onChange={() => setIsChecked(!isChecked)}
          />
          <label htmlFor="check">Run indefinitely</label>
        </div>
        <div style={{ height: '1rem' }}></div>
        <button onClick={handleSubmit}>Submit</button>
        <button onClick={onCancel}>Cancel</button>
      </div>
    </div>
  );
}
