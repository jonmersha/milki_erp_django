import React from "react";
import NavBar from "../components/NavBar";

export default function SalesOrders() {
  const dummyOrders = [
    { id: 1, customer: "John Doe", amount: 500 },
    { id: 2, customer: "Jane Smith", amount: 300 },
    { id: 3, customer: "Alice Brown", amount: 250 }
  ];

  return (
    <div>
      <NavBar />
      <main style={{ padding: "2rem" }}>
        <h1>Sales Orders</h1>
        <ul>
          {dummyOrders.map(order => (
            <li key={order.id}>
              Order #{order.id} - {order.customer} - ${order.amount}
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}
