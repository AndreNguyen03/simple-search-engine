import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App";

// Mock các component để đơn giản hóa test
jest.mock("../pages/Index", () => () => <div>Mock Index Page</div>);
jest.mock("../pages/SearchResults", () => () => <div>Mock Search Results Page</div>);
jest.mock("../pages/NotFound", () => () => <div>Mock Not Found Page</div>);

describe("App routing", () => {
  it("renders Index page on / route", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("Mock Index Page")).toBeInTheDocument();
  });

  it("renders SearchResults page on /search route", () => {
    render(
      <MemoryRouter initialEntries={["/search"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("Mock Search Results Page")).toBeInTheDocument();
  });

  it("renders NotFound page on unknown route", () => {
    render(
      <MemoryRouter initialEntries={["/unknown"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("Mock Not Found Page")).toBeInTheDocument();
  });
});
