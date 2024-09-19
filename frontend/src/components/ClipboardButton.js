import React from "react";
import { LuClipboard, LuClipboardCheck } from "react-icons/lu";
import {CopyToClipboard} from 'react-copy-to-clipboard';

export default function ClipboardButton({ text, onCopy, copied = false, className = "" }) {
  const classes = "text-gray-700 text-sm inline hover:text-gray-950 cursor-pointer" + (className ? " " + className : "");

  return (
    <CopyToClipboard text={text}
        onCopy={onCopy}>
        {copied ? <LuClipboardCheck className={classes} /> : <LuClipboard className={classes} />}
    </CopyToClipboard>
  );
}
