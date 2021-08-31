/// <reference types="cypress" />

const susccessfulLogoutMessage = "User logged out";
describe("/logout", () => {
    it("User can log out", () => {
        cy.request("POST", "http://localhost:5000/logout").should((response) => {
            expect(response.status).to.equal(200);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal(
                "http://0.0.0.0:3000"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("message");
            expect(response.body.message).to.be.a("string");
            expect(response.body.message).to.satisfy(function (s) {
                return s === susccessfulLogoutMessage;
            });
        });
    });
});
