export interface OpenAIDelta {
  content: string | null
}

export enum MessageRole {
  user = 'user',
  assistant = 'assistant',
}

export interface OpenAIMessage {
  role: MessageRole
  content: string
}

export interface OpenAIChoice {
  finish_reason: string | null
  delta: OpenAIDelta | null
  message: OpenAIMessage
  sources: any | null // TODO: Come back to this
  index: number
}

export interface OpenAICompletion {
  id: string | null
  object: string | null
  created: number | null
  model: string | null
  choices: Array<OpenAIChoice>
}

export interface ChatBody {
  messages: OpenAIMessage[]
  use_context: boolean
  context_filter: null | undefined
  include_sources: boolean
  stream: boolean
}

export interface ChatResponse {
  message: OpenAIMessage
  raw: object | null
  delta: string | null
  additional_kwargs: object
}
