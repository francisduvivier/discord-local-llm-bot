import { Ollama } from "langchain/llms/ollama";
import { ChatOllama } from "langchain/chat_models/ollama";
import { CallbackManager } from "langchain/callbacks";
type TokenCallback = undefined | ((token: string) => unknown);
let tokenCallback: TokenCallback = undefined
// Llama 2 7b wrapped by Ollama
const model = new Ollama({
    baseUrl: "http://localhost:11434",
    model: "mistral",
    callbackManager: CallbackManager.fromHandlers({
        async handleLLMNewToken(token: string) {
            console.log({ token });
            tokenCallback?.(token);
        },
        async handleLLMEnd(output) {
            console.log("End of stream.", output);
        }
    })
});

const chatModel = new ChatOllama(model);
let busy = false;
export async function getAnswer(question: string, tokenCallback: TokenCallback) {
    try {
        if (busy) {
            throw new Error('Sorry, I am unable to answer because I\'m busy with another request.')
        }
        busy = true;
        setTokenCallback(tokenCallback);
        const result = await chatModel.predict(question);
        return result;
    } finally {
        setTokenCallback(undefined);
        busy = false;
    }
}
export function setTokenCallback(callback: TokenCallback) {
    tokenCallback = callback;
}