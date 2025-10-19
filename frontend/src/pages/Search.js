import React, { useState } from "react";
import { Form, InputGroup, Button, Spinner } from "react-bootstrap";
import API from "../api/axios";
import MovieGrid from "../components/MovieGrid";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    try {
      const res = await API.get(`search/?query=${query}`);
      setResults(res.data);
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h3>🔍 Search Movies</h3>
      <Form onSubmit={handleSearch} className="mb-3">
        <InputGroup>
          <Form.Control
            type="text"
            placeholder="Search by title or genre..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Button variant="primary" type="submit">
            Search
          </Button>
        </InputGroup>
      </Form>

      {loading && (
        <div className="text-center my-4">
          <Spinner animation="border" variant="primary" />
        </div>
      )}

      {!loading && results.length > 0 && <MovieGrid movies={results} />}
      {!loading && results.length === 0 && query && (
        <p>No results found for "{query}".</p>
      )}
    </div>
  );
}

export default Search;