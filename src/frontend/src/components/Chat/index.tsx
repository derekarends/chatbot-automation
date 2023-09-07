import { useState } from "react";
import Header from "./Header";
import Content from "./Content";
import { Message } from "../../types";
import InputBox from "./InputBox";
import { sendChat } from "../../api";

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
    setLoading(true);

    const answer = await sendChat(chatMessages, message);
    setChatMessages((prevMessages) => [
      ...prevMessages,
      message,
      {
        text: answer.response,
        tool: answer.tool,
        sentBy: aiName,
        sentAt: new Date(),
        isChatOwner: false,
      },
    ]);

    setLoading(false);
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
