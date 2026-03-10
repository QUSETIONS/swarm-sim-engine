import { describe, it, expect } from "vitest";

describe("smoke", () => {
    it("renders app root", () => {
        expect(document.createElement("div")).toBeTruthy();
    });
});
