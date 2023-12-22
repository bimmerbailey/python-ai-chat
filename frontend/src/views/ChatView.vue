<script setup lang="ts">
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionMain from '@/components/SectionMain.vue'

import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import ChatBox from '@/components/ChatBox.vue'

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
      <div class="grid grid-cols-1 lg:grid-cols-1 gap-6 mb-6">
        <chat-box />
      </div>
    </section-main>
  </layout-authenticated>
</template>

<style scoped></style>
