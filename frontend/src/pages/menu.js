import React from "react";

export default function Menu() {
  const items = [
    { name: "Admin Panel", url: "/admin/", emoji: "🛠" },

    // CORE
    { name: "Companies", url: "/core/companies/", emoji: "🏭" },
    { name: "Factories", url: "/core/factories/", emoji: "🏢" },
    { name: "Admin Regions", url: "/core/admin-regions/", emoji: "🌍" },
    { name: "Cities", url: "/core/cities/", emoji: "🏘️" },

    // SALES
    { name: "Sales Orders", url: "/sales/orders/", emoji: "🧾" },
    { name: "Order Items", url: "/sales/order-items/", emoji: "📦" },

    // INVENTORY
    { name: "Warehouses", url: "/inventory/warehouses/", emoji: "🏚️" },
    { name: "Products", url: "/inventory/products/", emoji: "🛒" },
    { name: "Stocks", url: "/inventory/stocks/", emoji: "📊" },

    // USERS
    { name: "Users", url: "/users/users/", emoji: "👤" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 p-8 flex justify-center">
      <div className="w-full max-w-5xl">
        <h1 className="text-4xl font-extrabold text-center text-gray-800 mb-10 drop-shadow-sm">
          ✨ Milki ERP Menu
        </h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {items.map((item, index) => (
            <a
              key={index}
              href={item.url}
              className="
                bg-white/80 backdrop-blur-lg 
                border border-gray-200 
                rounded-2xl p-8 
                shadow-md 
                hover:shadow-xl 
                hover:-translate-y-1 
                transition 
                text-center 
                flex flex-col items-center 
              "
            >
              <span className="text-5xl mb-4">{item.emoji}</span>
              <h2 className="text-xl font-semibold text-gray-800">{item.name}</h2>
            </a>
          ))}
        </div>

        <p className="text-center text-sm text-gray-600 mt-12">
          Milki ERP — Powered by Django + React
        </p>
      </div>
    </div>
  );
}
