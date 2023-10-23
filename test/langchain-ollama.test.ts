import {describe, expect, it} from "bun:test";
import {getAnswer} from "../src/langchain-ollama.ts";

describe('langchange ollama test suite', function () {
    it('should return a string when calling getAnswer', async () => {
        const answer = await getAnswer('Who are you?');
        expect(answer).toBeTypeOf('string');
        expect(answer).toContain('Mistral');
    });
})