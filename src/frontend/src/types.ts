export type Message = {
  text: string;
  sources?: Source[];
  tool?: string;
  sentBy: string;
  sentAt: Date;
  isChatOwner?: boolean;
}

export type User = {
  username: string;
}

export type Domain = {
  user?: User;
  status: Status;
  isLoading: boolean;
  isRejected: boolean;
  isIdle: boolean;
};

export type Option = {
  id: number;
  label: string;
};

export enum Status {
  idle,
  loading,
  success,
  redirect,
  rejected,
}

export type ConversationResponse = {
  response: string;
  sources?: [Source];
  tool?: string;
}

export type Source = {
  source: string;
  pageNumber: string;
}