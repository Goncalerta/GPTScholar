import React from "react";
import ReactTextareaAutosize from "react-textarea-autosize";
import { FaRegStopCircle } from "react-icons/fa";
import { FiCornerDownRight } from "react-icons/fi";

export default function PromptArea({ prompt, handlePromptChange, abortPrompt, submitPrompt, loading, placeholder, className='' }) {
  return (
    <div className={"w-full max-w-xl relative" + (className ? " " + className : "")}>
      <ReactTextareaAutosize
          className="w-full border-2 rounded-xl resize-none py-3 ps-3 pe-16"
          placeholder={placeholder}
          value={prompt}
          onChange={handlePromptChange}
      />
      {loading ? (
        <button className="text-black absolute bottom-4 right-2 w-9 h-9 p-1" onClick={abortPrompt}><FaRegStopCircle size={30} /></button>
      ) : (prompt === '' ? (
        <button className="rounded-md bg-gray-200 text-white p-2 absolute bottom-4 right-2"><FiCornerDownRight /></button>
      ) : (
        <button className="rounded-md bg-black text-white p-2 absolute bottom-4 right-2" onClick={submitPrompt}><FiCornerDownRight /></button>
      ))} 
    </div>
  );
}
