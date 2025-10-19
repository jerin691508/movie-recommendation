import React, { useState } from "react";
import API from "../api/axios";

function RateMovie({ movieId }) {
  const [rating, setRating] = useState(0);

  const handleRate = async () => {
    if (!rating) {
      alert("Please select a rating!");
      return;
    }
    try {
      await API.post(`movie/${movieId}/rate/`, { rating });
      alert("Thanks for your rating!");
    } catch (error) {
      console.error(error);
      alert("Error submitting rating");
    }
  };

  return (
    <div className="mt-3">
      <select
        className="form-select w-auto d-inline"
        value={rating}
        onChange={(e) => setRating(e.target.value)}
      >
        <option value="0">Rate this movie</option>
        {[1, 2, 3, 4, 5].map((num) => (
          <option key={num} value={num}>{num} ⭐</option>
        ))}
      </select>
      <button className="btn btn-sm btn-primary ms-2" onClick={handleRate}>
        Submit
      </button>
    </div>
  );
}

export default RateMovie;
