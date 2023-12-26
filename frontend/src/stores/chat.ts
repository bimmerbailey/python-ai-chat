import type {
  ChatBody,
  OpenAICompletion,
  OpenAIMessage,
} from '@/interfaces/Chat'
import { MessageRole } from '@/interfaces/Chat'
import type { AxiosError } from 'axios'

import { defineStore } from 'pinia'
import { ChatApi } from '@/api/chat'

interface ChatStore {
  loading: boolean
  newMessage: string | undefined
  chatHistory: OpenAIMessage[]
  useContext: boolean
  contextFilter: null | undefined
  stream: boolean
}

// NOTE: This might be able to be part of the view
export const useChatStore = defineStore('chat', {
  state: (): ChatStore => ({
    newMessage: undefined,
    chatHistory: [],
    loading: false,
    useContext: false,
    stream: false,
    contextFilter: null,
  }),
  actions: {
    async sendMessage(): Promise<void> {
      this.loading = true

      if (this.newMessage != undefined) {
        const formattedNewMessage: OpenAIMessage = {
          content: this.newMessage,
          role: MessageRole.user,
        }
        this.chatHistory.push(formattedNewMessage)
      }
      const body: ChatBody = {
        messages: this.chatHistory,
        use_context: this.useContext,
        stream: this.stream,
        include_sources: this.useContext,
        context_filter: this.contextFilter,
      }
      console.log("Body", body)
      return await ChatApi.chatQuery(body)
        .then((res: OpenAICompletion): void => {
          res.choices.forEach((choice) => {
            this.chatHistory.push(choice.message)
          })
        })
        .catch((err: AxiosError): void => {
          throw err
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
})
