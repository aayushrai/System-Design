import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";

import Products from "./admin/Products";
import Main from "./main/Main";
import ProductCreate from "./admin/ProductCreate";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/admin/products" element={<Products />} />
          <Route path="/admin/products/create" element={<ProductCreate />} />
          <Route path="/" element={<Main />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
