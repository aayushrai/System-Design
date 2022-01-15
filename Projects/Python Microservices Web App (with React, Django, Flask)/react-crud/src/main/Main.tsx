import { useEffect, useState } from "react";
import { Product } from "../interface/Product";

export default function Main() {
  const [Products, setProducts] = useState([]);
  const baseUrl = "http://localhost:8001";
  useEffect(() => {
    (async () => {
      const response = fetch(baseUrl + "/api/products");
      const products = await (await response).json();
      setProducts(products);
    })();
  }, []);
  return (
    <div>
      <main role="main">
        <div className="album py-5 bg-light">
          <div className="container">
            <div className="row">
              {Products.map((product: Product) => (
                <div className="col-md-4" key={product.id}>
                  <div className="card mb-4 box-shadow">
                    <img
                      className="card-img-top"
                      src={product.image}
                      alt="Card image cap"
                    />
                    <div className="card-body">
                      <p className="card-text">{product.title}</p>
                      <div className="d-flex justify-content-between align-items-center">
                        <div className="btn-group">
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-secondary"
                          >
                            Like
                          </button>
                        </div>
                        <small className="text-muted">9 mins</small>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
