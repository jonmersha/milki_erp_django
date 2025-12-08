import React from "react";
import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav style={{ padding: "1rem", backgroundColor: "#eee" }}>
      <Link to="/">Dashboard</Link> |{" "}
      <Link to="/so">Sales Orders</Link> |{" "}
      <Link to="/inventorylist">Inventory</Link> |{" "}
      <Link to="/userslist">Users</Link>
    </nav>
  );
}
