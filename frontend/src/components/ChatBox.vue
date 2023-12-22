<script setup lang="ts">
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'
import ChatMessages from '@/components/ChatMessages.vue'
import { ref } from 'vue'

const sendMessage = () => {
  console.log('Message', newMessage.value)
  if (newMessage.value != null) {
    chatMessages.value?.push(newMessage.value)
  }
  console.log('All messages', chatMessages.value)
}

const clearMessages = () => {
  if (chatMessages.value.length > 0) {
    chatMessages.value = []
  }
}

const chatMessages = ref<Array<string>>([])
const newMessage = ref<string>()
</script>

<template>
  <div>
    <div class="bg-gray-500 rounded p-2">
      <div v-for="message in chatMessages">
        <chat-messages :text="message" author="me" />
      </div>
    </div>
    <div>
      <form-field class="mt-4">
        <div class="grid grid-cols-12 grid-rows-2 gap-4">
          <form-control
            v-model="newMessage"
            class="col-span-10"
            placeholder="Type a message"
          />
          <base-button
            @click="sendMessage"
            type="submit"
            color="info"
            label="Submit"
            class="col-span-2"
          />
          <base-button @click="clearMessages" label="Clear" />
        </div>
      </form-field>
    </div>
  </div>
</template>

<style scoped></style>
