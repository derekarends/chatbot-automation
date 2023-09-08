import { ConversationResponse, Message } from "./types";

const endpoint = import.meta.env.VITE_API_URL || ''

async function sendChat(chatMessages: Message[], message: Message): Promise<ConversationResponse> {
  try {
    const data = JSON.stringify({
      history: chatMessages.map((c) => ({
        text: c.text,
        isChatOwner: c.isChatOwner,
      })),
      message: {
        text: message.text,
        isChatOwner: message.isChatOwner,
        collectionName: 'space_turtles'
      },
    });

    const response = await fetch(`${endpoint}/api/conversation`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: data,
    });
    if (!response.ok) {
      return { response: `Uh oh! An error occurred. Please try again` };
    }

    return await response.json();
  } catch (e: unknown) {
    return { response: `Uh oh! An error occurred. Please try again` };
  }
}

export { sendChat }