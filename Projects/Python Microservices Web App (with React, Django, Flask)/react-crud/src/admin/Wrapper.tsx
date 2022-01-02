import React, { PropsWithChildren } from "react";
import Nav from "../components/Nav";
import Menu from "../components/Menu";

export default function Wrapper(props: PropsWithChildren<any>) {
  return (
    <div>
      <Nav />

      <div className="container-fluid">
        <div className="row">
          <Menu />

          <main role="main" className="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
            {props.children}
          </main>
        </div>
      </div>
    </div>
  );
}
