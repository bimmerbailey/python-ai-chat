<script setup lang="ts">
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'
import ChatMessages from '@/components/ChatMessages.vue'
import FormCheckRadioGroup from '@/components/FormCheckRadioGroup.vue'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'
import CardBox from '@/components/CardBox.vue'

const chatStore = useChatStore()

const sendMessage = () => {
  chatStore.sendMessage().catch((err) => {
    console.log(err)
  })
}

const { chatHistory, newMessage, useContext } = storeToRefs(chatStore)

const clearMessages = () => {
  if (chatStore.chatHistory.length > 0) {
    chatStore.chatHistory = []
  }
}
</script>

<template>
  <card-box>
    <form-check-radio-group
      name="chat-type"
      :options="[
        { text: 'LLM Chat', value: false },
        { text: 'Chat with docs', value: true },
      ]"
      v-model="useContext"
      type="radio"
    />
    <div class="bg-gray-500 rounded p-2 size-40">
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
  </card-box>
</template>

<style scoped></style>
