export interface OpenAIDelta {
  content: string | null
}

export interface OpenAIMessage {
  role: string // TODO: Come back to this "Literal", Enum?
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
