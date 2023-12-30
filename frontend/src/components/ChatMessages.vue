<script setup lang="ts">
const props = defineProps({
  text: { type: String, required: false },
  author: { type: String, required: true, default: 'assistant' },
})
</script>

<template>
  <div
    :class="{ 'text-right': author === 'assistant' }"
    class="p-2 bg-blue-500 rounded my-1.5"
  >
    <h5 class="text-xl">{{ props.author }}</h5>
    <p>{{ props.text }}</p>
  </div>
</template>

<style scoped></style>
