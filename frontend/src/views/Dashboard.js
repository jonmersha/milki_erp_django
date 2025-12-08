import React from "react";
import NavBar from "../components/NavBar";

export default function Dashboard() {
  return (
    <div>
      <NavBar />
      <main style={{ padding: "2rem" }}>
        <h1>Milki ERP System</h1>
        <p>Welcome to the static ERP dashboard.</p>
        <ul>
          <li>Sales Orders</li>
          <li>Inventory</li>
          <li>Users</li>
        </ul>
      </main>
    </div>
  );
}
