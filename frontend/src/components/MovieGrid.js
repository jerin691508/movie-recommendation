import React from "react";
import MovieCard from "./MovieCard";

function MovieGrid({ movies }) {
  if (!movies || movies.length === 0) {
    return <p>No movies found.</p>;
  }

  return (
    <div className="row">
      {movies.map((movie) => (
        <div className="col-md-3 mb-3" key={movie.id}>
          <MovieCard movie={movie} />
        </div>
      ))}
    </div>
  );
}

export default MovieGrid;
