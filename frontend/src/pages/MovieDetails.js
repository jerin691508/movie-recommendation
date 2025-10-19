import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';
import API from "../api/axios";
import Loader from "../components/Loader";
import RateMovie from "../components/RateMovie";
import MovieGrid from "../components/MovieGrid";

function MovieDetails() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const res = await API.get(`movie/${id}/`);
        setMovie(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    const fetchSimilar = async () => {
      try {
        const res = await API.get(`recommendations/`);
        const filtered = res.data.filter(m => m.id !== parseInt(id)).slice(0, 5);
        setSimilar(filtered);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMovie();
    fetchSimilar();
  }, [id]);

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("feedback/", { movie_id: id, feedback });
      setSubmitted(true);
      setFeedback("");
    } catch (err) {
      console.error(err);
      alert("Failed to submit feedback");
    }
  };

  if (loading) return <Loader />;
  if (!movie) return <p>Movie not found.</p>;

  return (
    <Container className="mt-4">
      <Row>
        <Col md={4}>
          <img
            src={movie.poster_url || "https://via.placeholder.com/300x450?text=No+Image"}
            className="img-fluid rounded"
            alt={movie.title}
          />
        </Col>
        <Col md={8}>
          <h2>{movie.title}</h2>
          <p><strong>Genre:</strong> {movie.genre || "Unknown"}</p>
          <p><strong>Description:</strong> {movie.description || "No description available."}</p>
          <RateMovie movieId={movie.id} />
        </Col>
      </Row>

      <hr />

      <h4>💬 Feedback</h4>
      <Card className="mb-4">
        <Card.Body>
          {submitted && <div className="alert alert-success">Thank you for your feedback!</div>}
          <Form onSubmit={handleFeedbackSubmit}>
            <Form.Group className="mb-2">
              <Form.Control
                as="textarea"
                rows={3}
                placeholder="Write your feedback about this movie..."
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                required
              />
            </Form.Group>
            <Card.Footer className="text-end">
              <Button type="submit" variant="primary">Submit Feedback</Button>
            </Card.Footer>
          </Form>
        </Card.Body>
      </Card>

      <hr />

      <h4>🎞️ Similar / Recommended Movies</h4>
      {similar.length > 0 ? <MovieGrid movies={similar} /> : <p>No recommendations available.</p>}
    </Container>
  );
}

export default MovieDetails;