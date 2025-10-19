import React from "react";
import { useNavigate } from "react-router-dom";

function SearchBar() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/search");
  };

  return (
    <button className="btn btn-outline-light" onClick={handleClick}>
      <i className="bi bi-search me-2"></i>Search
    </button>
  );
}

export default SearchBar;