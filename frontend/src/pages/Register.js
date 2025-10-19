import React, { useState } from "react";
import { Card, Form, InputGroup, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import 'bootstrap-icons/font/bootstrap-icons.css';

function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("register/", form);
      alert("Registration successful!");
      navigate("/login");
    } catch (err) {
      alert("Error registering user.");
    }
  };

  return (
    <div className="col-md-4 mx-auto mt-5">
      <Card className="shadow-sm hover-scale">
        <Card.Body>
          <h3 className="text-center mb-4">Register</h3>
          <Form onSubmit={handleSubmit}>
            <InputGroup className="mb-3">
              <InputGroup.Text><i className="bi bi-person-circle"></i></InputGroup.Text>
              <Form.Control
                name="username"
                placeholder="Username"
                value={form.username}
                onChange={handleChange}
              />
            </InputGroup>

            <InputGroup className="mb-3">
              <InputGroup.Text><i className="bi bi-envelope-fill"></i></InputGroup.Text>
              <Form.Control
                name="email"
                type="email"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
              />
            </InputGroup>

            <InputGroup className="mb-3">
              <InputGroup.Text><i className="bi bi-lock-fill"></i></InputGroup.Text>
              <Form.Control
                name="password"
                type="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
              />
            </InputGroup>

            <Button type="submit" variant="primary" className="w-100">
              <i className="bi bi-person-plus-fill me-2"></i>Register
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Register;