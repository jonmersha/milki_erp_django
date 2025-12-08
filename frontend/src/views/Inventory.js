import React from "react";
import NavBar from "../components/NavBar";

export default function Inventory() {
  const dummyProducts = [
    { id: 1, name: "Product A", stock: 50 },
    { id: 2, name: "Product B", stock: 20 },
    { id: 3, name: "Product C", stock: 75 }
  ];

  return (
    <div>
      <NavBar />
      <main style={{ padding: "2rem" }}>
        <h1>Inventory Products</h1>
        <ul>
          {dummyProducts.map(p => (
            <li key={p.id}>
              {p.name} - Stock: {p.stock}
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}
