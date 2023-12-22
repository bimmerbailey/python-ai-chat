import { defineStore } from 'pinia'
import axios from 'axios'

interface ChatStore {
  [index: string]: string | null | Array<string>

  newMessage: string | null
  previousMessages: Array<string>
  author: string
}

export const useChatStore = defineStore('chat', {
  state: (): ChatStore => ({
    newMessage: null,
    previousMessages: [],
    author: "bot",
  }),
  actions: {
    async sendMessage() {
      return "to send at some time."
    }
  },
  getters: {},
})
