export type User = {
  username: string;
}

export type Message = {
  text: string;
  sentBy: string;
  sentAt: Date;
  isChatOwner: boolean;
  tool?: string;
}

export type ConversationResponse = {
  response: string;
  tool?: string;
}