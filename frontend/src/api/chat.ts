import type { ChatBody, OpenAICompletion } from '@/interfaces/Chat'
import type { AxiosError, AxiosResponse } from 'axios'

import api from './base'

export const ChatApi = {
  async chatQuery(messages: ChatBody): Promise<OpenAICompletion> {
    return await api
      .post('/v1/chat/completions', messages)
      .then((res: AxiosResponse<OpenAICompletion>) => {
        return res.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  },
}
