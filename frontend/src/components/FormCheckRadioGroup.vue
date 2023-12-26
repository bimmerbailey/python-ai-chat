<script setup lang="ts">
import { computed, type PropType } from 'vue'
import FormCheckRadio from '@/components/FormCheckRadio.vue'
import type { ItemType } from '@/interfaces/Components'

const props = defineProps({
  options: {
    type: Array as PropType<ItemType[]>,
  },
  name: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: 'checkbox',
    validator: (value: string) =>
      ['checkbox', 'radio', 'switch'].includes(value),
  },
  componentClass: {
    type: String,
    default: null,
  },
  isColumn: Boolean,
  modelValue: {
    type: [Array, String, Number, Boolean],
    default: null,
  },
})

const emit = defineEmits(['update:modelValue'])

const computedValue = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
  },
})
</script>

<template>
  <div
    class="flex justify-start flex-wrap -mb-3"
    :class="{ 'flex-col': isColumn }"
  >
    <FormCheckRadio
      v-for="option in options"
      :key="option.text"
      v-model="computedValue"
      :type="type"
      :name="name"
      :input-value="option.value"
      :label="option.text"
      :class="componentClass"
      class="mr-6 mb-3 last:mr-0"
    />
  </div>
</template>
