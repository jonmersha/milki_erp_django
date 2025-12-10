export default function App() {
  const menuItems = [
    { name: "Dashboard", icon: "📊" },
    { name: "Reports", icon: "📄" },
    { name: "Users", icon: "👥" },
    { name: "Settings", icon: "⚙️" },
    { name: "Notifications", icon: "🔔" },
    { name: "Files", icon: "📁" },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* NAVBAR */}
      <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">MyApp</h1>

        <ul className="flex gap-6 text-gray-700 font-medium">
          <li className="hover:text-blue-600 cursor-pointer">Home</li>
          <li className="hover:text-blue-600 cursor-pointer">About</li>
          <li className="hover:text-blue-600 cursor-pointer">Contact</li>
        </ul>
      </nav>

      {/* GRID MENU */}
      <div className="p-8 max-w-6xl mx-auto">
        <h2 className="text-xl font-semibold text-gray-800 mb-6">
          Quick Menu
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {menuItems.map((item) => (
            <div
              key={item.name}
              className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg cursor-pointer transition flex flex-col items-center justify-center"
            >
              <span className="text-5xl mb-3">{item.icon}</span>
              <h3 className="text-lg font-semibold text-gray-700">{item.name}</h3>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
