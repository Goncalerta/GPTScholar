import React, { useState } from "react";
import api from "./api";
import Message from "./components/Message";
import PromptArea from "./components/PromptArea";
import Logo from "./components/Logo";

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [controller, setController] = useState(null);
  const [prompts, setPrompts] = useState([]);
  const [responses, setResponses] = useState([]);
  const [clipboard, setClipboard] = useState(null);

  const submitPrompt = async function () {
    const controller = new AbortController();
    startLoading(controller);
    const request = api.prompt(prompt, controller);
    pushPrompt(prompt);
    setPrompt('');
    const result = await request;
    
    pushResponse(result);
    
    stopLoading();
    console.log(result);
  };

  const handlePromptChange = event => {
    setPrompt(event.target.value);
  };

  const startLoading = (controller) => {
    setController(controller);
    setLoading(true);
  };

  const stopLoading = () => {
    setController(null);
    setLoading(false);
  };

  const abortPrompt = () => {
    controller.abort();
  };

  const copyToClipboard = (id) => {
    setClipboard(id);
    setTimeout(() => {
      setClipboard(null);
    }, 1000);
  };

  const pushPrompt = (item) => {
    setPrompts([...prompts, item]);
  };

  const pushResponse = (item) => {
    setResponses([...responses, item]);
  };

  return (
    <div className="flex flex-col">
      <header className="mt-10 mb-10 sticky top-0 z-50 bg-white">
        <h1 className="mt-10 text-center"><Logo /></h1>
      </header>
      <div className="flex flex-col items-center px-2">
        <div className="w-full max-w-xl mb-4 ps-4 pe-10">
          {
            prompts.map((prompt, index) => (
              <div key={index}>
                <Message
                  author="You"
                  message={prompt}
                  onCopy={() => copyToClipboard(`prompt.${index}`)}
                  copied={clipboard === `prompt.${index}`}
                />
                {responses.length > index ? (
                  <Message
                    author="GPTscholar"
                    error={responses[index].error}
                    message={responses[index].error? responses[index].error.message : responses[index].final_response}
                    onCopy={() => copyToClipboard(`final_response.${index}`)}
                    copied={clipboard === `final_response.${index}`}
                    markdown={true}
                  />
                ) : (
                  <Message
                    author="GPTscholar"
                      message="Waiting for response"
                      grayed={true}
                  />
                )}
              </div>
            ))
          }
        </div>
        <PromptArea
          prompt={prompt}
          handlePromptChange={handlePromptChange}
          abortPrompt={abortPrompt}
          submitPrompt={submitPrompt}
          loading={loading}
          placeholder="Write your prompt..."
          className="mb-10"
        />
      </div>
    </div>
  );
}
