import {Ollama} from "langchain/llms/ollama";
import {ChatOllama} from "langchain/chat_models/ollama";

// Llama 2 7b wrapped by Ollama
const model = new Ollama({
    baseUrl: "http://localhost:11434",
    model: "mistral",
});

const chatModel = new ChatOllama(model);
export async function getAnswer(question: string) {
    const result = await chatModel.predict(question);
    return result
}