import {
  type ChatBody,
  MessageRole,
  type OpenAICompletion,
  type OpenAIMessage,
} from '@/interfaces/Chat'
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
          this.newMessage = ''
        })
    },
    async streamMessage(): Promise<void> {
      this.loading = true

      if (this.newMessage != undefined) {
        const formattedNewMessage: OpenAIMessage = {
          content: this.newMessage,
          role: MessageRole.user,
        }
        this.chatHistory.push(formattedNewMessage)
        this.chatHistory.push({
          content: '',
          role: MessageRole.assistant,
        })
      }
      const response = await fetch(
        'http://127.0.0.1:8000/api/v1/chat/completions',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            messages: this.chatHistory,
            use_context: this.useContext,
            stream: true,
            include_sources: this.useContext,
            context_filter: this.contextFilter,
          }),
        }
      )
      const reader = response.body
        ?.pipeThrough(new TextDecoderStream())
        .getReader()
      if (!reader) return
      // eslint-disable-next-line no-constant-condition
      while (true) {
        // eslint-disable-next-line no-await-in-loop
        const { value, done } = await reader.read()
        if (done) break
        let dataDone = false
        const arr = value.split('\n')
        arr.forEach((data) => {
          if (data.length === 0) return // ignore empty message
          if (data.startsWith(':')) return // ignore sse comment message
          if (data === 'data: [DONE]') {
            dataDone = true
            return
          }
          const json: OpenAICompletion = JSON.parse(data.substring(6))
          if (json.choices[0].finish_reason === null) {
            this.chatHistory[this.chatHistory.length - 1].content +=
              json.choices[0].delta?.content
          }
        })
        if (dataDone) break
      }
    },
  },
})
