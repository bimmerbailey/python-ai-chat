<script setup lang="ts">
import { IngestApi } from '@/api/ingest'
import { onMounted, type Ref, ref } from 'vue'

const documents: Ref<string[]> = ref([])

onMounted(() => {
  IngestApi.getDocuments().then((res) => {
    res.data.forEach((document) => {
      if (document.doc_metadata?.file_name) {
        // TODO: Set maybe?
        if (!documents.value.includes(document.doc_metadata.file_name)) {
          documents.value.push(document.doc_metadata.file_name)
        }
      }
    })
  })
})
</script>

<template>
  <div>
    <ul v-for="document in documents">
      {{ document }}
    </ul>
  </div>
</template>

<style scoped></style>
