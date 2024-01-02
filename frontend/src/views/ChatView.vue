<script setup lang="ts">
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionMain from '@/components/SectionMain.vue'

import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import ChatBox from '@/components/ChatBox.vue'
import DocumentList from '@/components/DocumentList.vue'

import { mdiRobotOutline } from '@mdi/js'
</script>

<template>
  <layout-authenticated>
    <section-main>
      <section-title-line-with-button
        :icon="mdiRobotOutline"
        title="Chat with AI"
        main
      />
      <div class="grid sm:grid-cols-3 md:grid-cols-12 gap-4 min-h-screen">
        <document-list class="md:col-span-3 sm:col-span-3" />
        <chat-box class="md:col-span-9 sm:col-span-3" />
      </div>
    </section-main>
  </layout-authenticated>
</template>

<style scoped></style>
