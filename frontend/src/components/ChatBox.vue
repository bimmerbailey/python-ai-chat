<script setup lang="ts">
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'
import ChatMessages from '@/components/ChatMessages.vue'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()

const sendMessage = () => {
  chatStore.sendMessage().catch((err) => {
    console.log(err)
  })
}

const { chatHistory, newMessage } = storeToRefs(chatStore)

const clearMessages = () => {
  if (chatStore.chatHistory.length > 0) {
    chatStore.chatHistory = []
  }
}
</script>

<template>
  <div>
    <div class="bg-gray-500 rounded p-2">
      <div v-for="message in chatHistory">
        <chat-messages :text="message.content" :author="message.role" />
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
