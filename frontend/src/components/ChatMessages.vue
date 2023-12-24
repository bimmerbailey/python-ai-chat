<script setup lang="ts">
const props = defineProps({
  text: { type: String, required: false },
  author: String,
})
</script>

<template>
  <div class="px-2 bg-blue-500 rounded my-1.5">
    <h5>{{ props.author }}</h5>
    {{ props.text }}
  </div>
</template>

<style scoped>
</style>
