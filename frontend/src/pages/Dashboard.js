import React, { useEffect, useState } from "react";
import API from "../api/axios";
import MovieCard from "../components/MovieCard";

function Dashboard() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const res = await API.get("movies/");
        setMovies(res.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchMovies();
  }, []);

  return (
    <div className="container mt-4">
      <h3 className="mb-3">🎬 All Movies</h3>
      {loading ? (
        <p>Loading movies...</p>
      ) : (
        <div className="d-flex flex-wrap">
          {movies.map((m) => (
            <MovieCard key={m.id} movie={m} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
