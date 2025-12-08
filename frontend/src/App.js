import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Menu from "./pages/menu";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Menu />} />
      </Routes>
    </Router>
  );
}

export default App;
