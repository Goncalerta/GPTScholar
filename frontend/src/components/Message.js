import React from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import ClipboardButton from "./ClipboardButton";

export default function Message({ author, message, onCopy = null, copied = false, markdown = false, error = false, grayed = false }) {
  return (
    <div className="w-full mb-6">
      <div className="w-full"><span className="font-bold text-xl">{author}</span> {!error && onCopy && (<ClipboardButton className="mb-1 ms-1" text={message} onCopy={onCopy} copied={copied} />)}</div>
      <div className={'w-full font-light text-base' + (markdown ? ' markdown-response' : '') + (error ? ' text-red-500' : (grayed ? ' text-gray-400' : ''))}>{markdown ? (<Markdown remarkPlugins={[remarkGfm]}>{message}</Markdown>) : (<pre className={grayed ? 'loading inline' : ''}>{message}</pre>)}</div>
    </div>
  );
}
