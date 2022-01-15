import { PropsWithoutRef, SyntheticEvent, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Wrapper from "./Wrapper";

export default function ProductEdit(props: PropsWithoutRef<any>) {
  const [title, settitle] = useState("");
  const [image, setimage] = useState("");
  const [redirect, setredirect] = useState(false);
  const { id } = useParams();
  const baseUrl = "http://localhost:8000";

  useEffect(() => {
    (async () => {
      const response = fetch(baseUrl + `/api/products/${id}`);
      const product = await (await response).json();
      settitle(product.title);
      setimage(product.image);
    })();
  }, []);

  const submit = async (event: SyntheticEvent) => {
    event.preventDefault();
    await fetch(baseUrl + `/api/products/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, image }),
    });
    setredirect(true);
  };

  if (redirect) {
    window.location.href = "http://localhost:3000/admin/products";
  }
  return (
    <div>
      <Wrapper>
        <form onSubmit={(event) => submit(event)}>
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              className="form-control"
              defaultValue={title}
              onChange={(e) => settitle(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Image</label>
            <input
              type="text"
              className="form-control"
              defaultValue={image}
              onChange={(e) => setimage(e.target.value)}
            />
          </div>

          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
      </Wrapper>
    </div>
  );
}
