import React from "react";
import { Navbar, Container, Nav, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import SearchBar from "./SearchBar";
import 'bootstrap-icons/font/bootstrap-icons.css';

function NavbarComponent() {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="mb-4 shadow-sm hover-scale">
      <Container>
        <Navbar.Brand as={Link} to="/">🎬 Movie Recommender</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="me-auto">
            {isLoggedIn && (
              <>
                <Nav.Link as={Link} to="/dashboard">Dashboard</Nav.Link>
                <Nav.Link as={Link} to="/recommendations">Recommendations</Nav.Link>
                <Nav.Link as={Link} to="/watchlist">Watchlist</Nav.Link>
                <Nav.Link as={Link} to="/history">History</Nav.Link>
                <Nav.Link as={Link} to="/feedback">Feedback</Nav.Link>
                <Nav.Link as={Link} to="/profile">Profile</Nav.Link>
              </>
            )}
          </Nav>

          <div className="d-flex align-items-center">
            <SearchBar />
            {isLoggedIn ? (
              <Button variant="outline-light" className="ms-3" size="sm" onClick={handleLogout}>
                <i className="bi bi-box-arrow-right me-2"></i>Logout
              </Button>
            ) : (
              <>
                <Nav.Link as={Link} to="/login" className="ms-3">Login</Nav.Link>
                <Nav.Link as={Link} to="/register">Register</Nav.Link>
              </>
            )}
          </div>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavbarComponent;