import type { AxiosError, AxiosResponse } from 'axios'

import api from './base'

interface ChatBody {
  messages: Array<string>
  use_context: boolean
  context_filter: null
  include_sources: boolean
  stream: boolean
}

export const ChatApi = {
  async ChatQuery(messages: ChatBody) {
    await api
      .post('/api/v1/chat/completions', messages)
      .then((res: AxiosResponse) => {
        return res.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  },
}
