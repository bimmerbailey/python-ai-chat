import type { IngestResponse } from '@/interfaces/Ingest'
import type { AxiosError, AxiosResponse } from 'axios'

import api from './base'

export const IngestApi = {
  async getDocuments(): Promise<IngestResponse> {
    return await api
      .get('/v1/ingest/list')
      .then((res: AxiosResponse<IngestResponse>) => {
        return res.data
      })
      .catch((err: AxiosError) => {
        throw err
      })
  },
}
