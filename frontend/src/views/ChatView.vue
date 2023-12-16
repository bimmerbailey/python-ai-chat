<script setup lang="ts">
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionMain from '@/components/SectionMain.vue'

import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'

import { mdiTableBorder } from '@mdi/js'
</script>

<template>
  <layout-authenticated>
    <section-main>
      <section-title-line-with-button
        :icon="mdiTableBorder"
        title="Chat"
        main
      ></section-title-line-with-button>
      <div class="grid grid-cols-1 lg:grid-cols-1 gap-6 mb-6">
        This is our chat window
      </div>
    </section-main>
  </layout-authenticated>
</template>

<style scoped></style>
