import React, { useEffect, useState } from "react";
import API from "../api/axios";
import MovieCard from "../components/MovieCard";

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const res = await API.get("recommendations/");
        setRecommendations(res.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchRecommendations();
  }, []);

  return (
    <div className="container mt-4">
      <h3 className="mb-3">🎯 Recommended for You</h3>
      {loading ? (
        <p>Loading recommendations...</p>
      ) : recommendations.length > 0 ? (
        <div className="d-flex flex-wrap">
          {recommendations.map((m) => (
            <MovieCard key={m.id} movie={m} />
          ))}
        </div>
      ) : (
        <p>No recommendations yet — try rating some movies!</p>
      )}
    </div>
  );
}

export default Recommendations;
