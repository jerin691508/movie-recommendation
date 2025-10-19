import React, { useEffect, useState } from "react";
import { Card, Row, Col } from "react-bootstrap";
import API from "../api/axios";
import Loader from "../components/Loader";

function Watchlist() {
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWatchlist = async () => {
      try {
        const res = await API.get("user/watchlist/");
        const formatted = res.data.map(item => item.movie || item);
        setWatchlist(formatted);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchWatchlist();
  }, []);

  return (
    <div className="container mt-4">
      <h3>📌 My Watchlist</h3>
      {loading && <Loader />}
      {!loading && watchlist.length > 0 ? (
        <Row className="mt-3">
          {watchlist.map(movie => (
            <Col md={4} key={movie.id} className="mb-4">
              <Card>
                <Card.Img
                  variant="top"
                  src={movie.poster_url || "https://via.placeholder.com/300x450?text=No+Image"}
                  alt={movie.title}
                />
                <Card.Body>
                  <Card.Title>{movie.title}</Card.Title>
                  <Card.Text>
                    <strong>Genre:</strong> {movie.genre || "Unknown"}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      ) : (
        <p>Your watchlist is empty.</p>
      )}
    </div>
  );
}

export default Watchlist;