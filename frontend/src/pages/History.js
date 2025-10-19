import React, { useEffect, useState } from "react";
import { Table, Spinner } from "react-bootstrap";
import API from "../api/axios";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const formatDate = (dateStr) => {
    if (!dateStr) return "-";
    const d = new Date(dateStr);
    return isNaN(d) ? "-" : d.toLocaleDateString();
  };

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await API.get("user/history/");
        const formatted = res.data.map(item => ({
          ...item.movie,
          rating: item.rating,
          rated_at: item.rated_at,
        }));
        setHistory(formatted);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="container mt-4">
      <h3>📜 Rating History</h3>
      {loading ? (
        <div className="text-center mt-4">
          <Spinner animation="border" />
        </div>
      ) : history.length > 0 ? (
        <Table striped hover responsive className="mt-3">
          <thead>
            <tr>
              <th>Movie</th>
              <th>Genre</th>
              <th>Rated</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {history.map(item => (
              <tr key={item.id}>
                <td>{item.title}</td>
                <td>{item.genre || "Unknown"}</td>
                <td>{formatDate(item.rated_at)}</td>
                <td>{item.rating}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      ) : (
        <p>No history found.</p>
      )}
    </div>
  );
}

export default History;