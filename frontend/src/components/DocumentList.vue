<script setup lang="ts">
import { onMounted, type Ref, ref } from 'vue'

import { IngestApi } from '@/api/ingest'
import CardBox from '@/components/CardBox.vue'

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
  <card-box>
    <h1 class="text-2xl font-bold pb-2">Uploaded Documents</h1>
    <ul v-for="document in documents">
      {{ document }}
    </ul>
  </card-box>
</template>

<style scoped></style>
