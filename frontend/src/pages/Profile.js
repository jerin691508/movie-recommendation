import React, { useEffect, useState } from "react";
import { Card, Badge } from "react-bootstrap";
import API from "../api/axios";

function Profile() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await API.get("user/profile/");
        setProfile(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchProfile();
  }, []);

  if (!profile) return <p className="mt-3">Loading profile...</p>;

  return (
    <div className="container mt-4">
      <h3>👤 My Profile</h3>
      <Card className="mt-3">
        <Card.Body>
          <Card.Title>{profile.username}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted">{profile.email}</Card.Subtitle>
          <Card.Text>
            <strong>Date Joined:</strong>{" "}
            <Badge bg="secondary">{new Date(profile.date_joined).toLocaleDateString()}</Badge>
          </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Profile;