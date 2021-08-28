/// <reference types="cypress" /> 

import scores from "../fixtures/postScores.json";
import scoresSetTwo from "../fixtures/postScoresSetTwo.json";
var faker = require("faker");

let session_Id;
let set_one_quizId;
let set_two_quizId;
//let Zip_Code;
let user1;
let user2;
let user3;
let user4;
let user5;
let user6;
let user7;
const successMessage = "Successfully created user";
const badReqMessage1 = "Email and password must be included in the request body";
const alreadyRegisteredMessage = "Email already registered";
const badReqMessage2 = "Email and password must be included in the request body.";
const missingName = "Name is missing.";
//const missingQuizId = "Quiz UUID must be included to register.";
//const missingQuizId = "QUIZ_UUID is required.";
const invalidQuizId = "Quiz ID is not a valid UUID4 format.";
const rateLimitPerSecond = "ratelimit exceeded 5 per 1 second";
const rateLimitPerMinute = "ratelimit exceeded 10 per 1 minute";
const rateLimitPerHour = "ratelimit exceeded 50 per 1 hour";
const rateLimitPerDay = "ratelimit exceeded 100 per 1 day";


describe("'/register' endpoint", () => {
    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                set_one_quizId = response.body.quizId;
            });
            cy.scoresEndpoint(scoresSetTwo, session_Id).should((response) => {
                set_two_quizId = response.body.quizId;
            });
        })
    });

    it("should register a user", () => {
        user1 = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };
        
        cy.registerEndpoint(user1).should((response) => {
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.headers["access-control-allow-origin"]).to.equal(
                "http://0.0.0.0:3000"
            );
            expect(response.body).to.be.a("object");

            if (response.status == 201) {

                expect(response.status).to.equal(201);
                expect(response.body).to.have.property("message");
                expect(response.body.message).to.satisfy(function (s) {
                    return s === successMessage;
                });

            } else {
                expect(response.status).to.equal(429);
                expect(response.body).to.have.property("error");
                let errorMessage = response.body;
                if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === rateLimitPerSecond;
                    });
                } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === rateLimitPerMinute;
                    });
                } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === rateLimitPerHour;
                    });
                }
                expect(response.body.error).to.satisfy(function (s) {
                    return s === rateLimitPerDay;
                });
            }

        });

    });

    it("should register another user", () => {
        user2 = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user2).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.headers["access-control-allow-origin"]).to.equal(
                "http://0.0.0.0:3000"
            );
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("message");
            expect(response.body.message).to.satisfy(function (s) {
                return s === successMessage;
            });
        });
    });

    it("should handle if the user already exists", () => {
        user2 = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_two_quizId
        };

        cy.registerEndpoint(user2).then(() => {
            cy.registerEndpoint(user2).should((response) => {
                expect(response.status).to.equal(401);
                expect(response.headers["content-type"]).to.equal("application/json");
                expect(response.body).to.be.a("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === alreadyRegisteredMessage;
                });
            });
        });
    });

    it("should handle a missing email", () => {
        user3 = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };

        cy.registerEndpoint(user3).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === badReqMessage1;
            });
        });
        
    });

    it("should handle a missing password", () => {
        user4 = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            quizId: set_one_quizId
        };
        
        cy.registerEndpoint(user4).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.satisfy(function (s) {
                return s === badReqMessage2;
            });
        });
    });

    it("should handle a missing body", () => {
        cy.registerEndpoint().should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === badReqMessage2;
            });
        });
    });

    it("should handle a missing firstName", () => {
        user5 = {
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };
            
        cy.registerEndpoint(user5).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error, { timeout: 3000 }).to.satisfy(function (s) {
                return s === missingName;
            });
        });
    });

    it("should handle a missing lastName", () => {
        user6 = {
            firstName: faker.name.firstName(),
            email: faker.internet.email(),
            password: faker.internet.password(),
            quizId: set_one_quizId
        };
        
        cy.registerEndpoint(user6).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === missingName;
            });
        });
    });

    it("should handle a missing quizId", () => {
        user7 = {
            firstName: faker.name.firstName(),
            lastName: faker.name.lastName(),
            email: faker.internet.email(),
            password: faker.internet.password()
        };
        
        cy.registerEndpoint(user7).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === invalidQuizId;
            });
        });
    });
});
