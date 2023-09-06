import { useState } from "react";
import Header from "./Header";
import Content from "./Content";
import { ConversationResponse, Message } from "../../types";
import InputBox from "./InputBox";

const aiName = "ChatAI";

type Props = {
  username: string;
};

function Chat({ username }: Props) {
  const [loading, setLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState<Message[]>(() => [
    {
      text: `Hey, ${username} what can I do for you today?`,
      sentBy: aiName,
      sentAt: new Date(),
      isChatOwner: false,
    },
  ]);

  const sendANewMessage = async (message: Message) => {
    setChatMessages((prevMessages) => [...prevMessages, message]);

    setLoading(true);
    let answer: ConversationResponse;
    try {
      const data = JSON.stringify({
        history: chatMessages.map((c) => ({
          text: c.text,
          isChatOwner: c.isChatOwner,
        })),
        question: message,
      });

      const response = await fetch("/api/conversation", {
        method: "POST",
        body: data,
      });
      answer = await response.json();
    } catch (e: unknown) {
      answer = { response: `Uh oh! An error occurred. Please try again` };
    } finally {
      setChatMessages((prevMessages) => [
        ...prevMessages,
        {
          text: answer.response,
          sources: answer.sources,
          tool: answer.tool,
          sentBy: aiName,
          sentAt: new Date(),
          isChatOwner: false,
        },
      ]);
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mt-8 ">
      <div className="bg-white border border-gray-200 rounded-lg shadow relative">
        <Header name={username} numberOfMessages={chatMessages.length} />
        <Content loading={loading} messages={chatMessages} />
        <InputBox sendMessage={sendANewMessage} />
      </div>
    </div>
  );
}

export default Chat;
