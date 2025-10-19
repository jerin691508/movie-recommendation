import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import API from '../api/axios';

function MovieCard({ movie, showActions = true }) {

  const handleWatchlist = async () => {
    try {
      await API.post('user/watchlist/', { movie_id: movie.id });
      alert(`${movie.title} added to watchlist!`);
    } catch (err) { console.error(err); }
  };

  const avgStars = [];
  const fullStars = Math.floor(movie.avg_rating || 0);
  for (let i=0;i<fullStars;i++) avgStars.push(<i key={i} className="bi bi-star-fill text-warning"></i>);

  return (
    <Card className="m-2 shadow-sm" style={{ width: '14rem', cursor: 'pointer' }}>
      <Card.Img variant="top" src={movie.poster_url || 'https://via.placeholder.com/200x300?text=No+Image'} />
      <Card.Body>
        <Card.Title className="text-truncate">{movie.title}</Card.Title>
        <Card.Text>
          <small className="text-muted">{movie.genre || 'Unknown Genre'}</small>
        </Card.Text>
        <div>{avgStars}</div>
        <Link to={`/movie/${movie.id}`} className="btn btn-primary btn-sm mt-2 w-100">Details</Link>
        {showActions && <Button variant="warning" size="sm" className="mt-2 w-100" onClick={handleWatchlist}>+ Watchlist</Button>}
      </Card.Body>
    </Card>
  );
}

export default MovieCard;
