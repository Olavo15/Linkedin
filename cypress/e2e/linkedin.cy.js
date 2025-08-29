import { validUser } from "../fixtures/login";

describe("LinkedIn Login Page", () => {
  beforeEach(() => {
    cy.session("login", () => {
      cy.visit("https://www.linkedin.com/login");
      cy.get("#username").type(validUser.username);
      cy.get("#password").type(validUser.password);
      cy.get('button[type="submit"]').click();
      cy.url().should("include", "/feed");
    });
  });

  it("should open Jobs after login", () => {
    cy.visit("https://www.linkedin.com/jobs/");
    cy.url().should("include", "/jobs");
  });
  it("should open My Network after login", () => {
    cy.get("#jobs-search-box-keyword-id-ember1204").type(
      "Desenvolvedor{enter}"
    );
    cy.url().should("include", "/jobs/search");
  });
});
