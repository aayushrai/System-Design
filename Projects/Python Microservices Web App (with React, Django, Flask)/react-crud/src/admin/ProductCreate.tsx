import { useState } from "react";
import Wrapper from "./Wrapper";

export default function ProductCreate() {
  const [title, settitle] = useState("");
  const [image, setimage] = useState("");
  const [redirect, setredirect] = useState(false);

  const baseUrl = "http://localhost:8000";
  const submit = async (event: any) => {
    event.preventDefault();
    await fetch(baseUrl + "/api/products", {
      method: "POST",
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
              value={title}
              onChange={(e) => settitle(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Image</label>
            <input
              type="text"
              className="form-control"
              value={image}
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
