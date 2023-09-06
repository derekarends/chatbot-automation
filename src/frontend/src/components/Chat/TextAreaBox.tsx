import { useState } from "react";
import { Message } from "../../types";
import { DebouncedTextArea } from "../DebouncedElements";

type Props = {
  sendMessage: (message: Message) => void;
};

function TextAreaBox({ sendMessage }: Props) {
  const [message, setMessage] = useState("");

  const onSendMessage = () => {
    if (message && message.length > 0) {
      const newMessagePayload: Message = {
        sentAt: new Date(),
        sentBy: "You",
        isChatOwner: true,
        text: message,
      };
      sendMessage(newMessagePayload);
      setMessage("");
    }
  };

  return (
    <div className="px-6 py-3 bg-white w-100 overflow-hidden rounded-bl-xl rounded-br-xla">
      <div className="flex flex-row items-center space-x-5">
        <DebouncedTextArea
          value={message ?? ""}
          debounce={100}
          onChange={(value) => setMessage(String(value))}
        />
        <button
          type="button"
          disabled={!message || message.length === 0}
          className="px-3 py-2 text-xs font-medium text-center text-white bg-blue-500 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 disabled:opacity-50"
          onClick={onSendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default TextAreaBox;
