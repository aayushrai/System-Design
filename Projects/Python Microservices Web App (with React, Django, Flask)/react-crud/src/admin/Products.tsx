import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Product } from "../interface/Product";
import Wrapper from "./Wrapper";

export default function Products() {
  const [Products, setProducts] = useState([]);
  const baseUrl = "http://localhost:8000";
  useEffect(() => {
    (async () => {
      const response = fetch(baseUrl + "/api/products");
      const products = await (await response).json();
      console.log(products);
      setProducts(products);
    })();
  }, []);

  const deleteProduct = async (id: number) => {
    if (
      window.confirm(`Are sure you want to delete product with id: ${id} ?`)
    ) {
      await fetch(baseUrl + `/api/products/${id}`, { method: "DELETE" });
      setProducts(Products.filter((product: Product) => product.id !== id));
    }
  };
  return (
    <Wrapper>
        <div className="pt-3 pb-2 mb-3 border-bottom">
            <div className="btn-toolbar mb-2 mb-md-0">
                <Link to={"/admin/products/create"} className="btn btn-sm btn-outline-secondary">Add</Link>
            </div>
        </div>
      <div className="table-responsive">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th>Id</th>
              <th>Image</th>
              <th>Title</th>
              <th>Likes</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {Products.map((product: Product) => {
              return (
                <tr>
                  <td>{product.id}</td>
                  <td>{product.image}</td>
                  <td>{product.title}</td>
                  <td>{product.likes}</td>
                  <td>
                    <div className="btn-group mr-2">
                      <a
                        href="#"
                        className="btn btn-sm btn-outline-secondary"
                        onClick={() => deleteProduct(product.id)}
                      >
                        Delete
                      </a>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Wrapper>
  );
}
