import React, { useState } from "react";
import { Card, Form, InputGroup, Button, Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import 'bootstrap-icons/font/bootstrap-icons.css';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("login/", { username, password });
      localStorage.setItem("token", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      navigate("/dashboard");
    } catch {
      setError(true);
    }
  };

  return (
    <div className="col-md-4 mx-auto mt-5">
      <Card className="shadow-sm hover-scale">
        <Card.Body>
          <h3 className="text-center mb-4">Login</h3>
          {error && <Alert variant="danger">Invalid credentials</Alert>}
          <Form onSubmit={handleLogin}>
            <InputGroup className="mb-3">
              <InputGroup.Text><i className="bi bi-person-circle"></i></InputGroup.Text>
              <Form.Control
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </InputGroup>

            <InputGroup className="mb-3">
              <InputGroup.Text><i className="bi bi-lock-fill"></i></InputGroup.Text>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </InputGroup>

            <Button type="submit" variant="primary" className="w-100">
              <i className="bi bi-box-arrow-in-right me-2"></i>Login
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Login;