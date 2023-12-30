interface DocumentMetadata {
  page_label: string
  file_name: string
}

export interface IngestedDocument {
  object: string
  doc_id: string
  doc_metadata: DocumentMetadata | null
}

export interface IngestResponse {
  object: string
  model: string
  data: IngestedDocument[]
}
