import React from "react";
import NavBar from "../components/NavBar";

export default function Users() {
  const dummyUsers = [
    { id: 1, username: "admin", email: "admin@example.com" },
    { id: 2, username: "johndoe", email: "john@example.com" },
    { id: 3, username: "alice", email: "alice@example.com" }
  ];

  return (
    <div>
      <NavBar />
      <main style={{ padding: "2rem" }}>
        <h1>Users</h1>
        <ul>
          {dummyUsers.map(u => (
            <li key={u.id}>
              {u.username} - {u.email}
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}
