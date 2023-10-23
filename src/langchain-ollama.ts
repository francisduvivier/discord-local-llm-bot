import {Ollama} from "langchain/llms/ollama";
import {ChatOllama} from "langchain/chat_models/ollama";
import { CallbackManager } from "langchain/callbacks";

// Llama 2 7b wrapped by Ollama
const model = new Ollama({
    baseUrl: "http://localhost:11434",
    model: "mistral",
    callbackManager: CallbackManager.fromHandlers({
        async handleLLMNewToken(token: string) {
          console.log({ token });
        },
        async handleLLMEnd(output) {
          console.log("End of stream.", output);
        }
    })
});

const chatModel = new ChatOllama(model);
export async function getAnswer(question: string) {
    const result = await chatModel.predict(question);
    return result
}