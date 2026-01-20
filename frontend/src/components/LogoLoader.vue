<template>
  <div class="loader-container">
    <div
      class="logo-wrapper"
      :style="{
        width: size + 'px',
        height: size + 'px',
      }"
    >
      <v-img :src="logo" :width="size" :height="size" />
      <div
        class="shine"
        :style="{
          animationDuration: duration + 's',
          animationDirection: direction,
          background: `linear-gradient(
              120deg,
              rgba(255, 255, 255, 0) 0%,
              rgba(255, 255, 255, ${opacity}) 50%,
              rgba(255, 255, 255, 0) 100%
            )`,
        }"
      />
    </div>
    <div v-if="currentMessage" class="loading-message">
      {{ currentMessage }}
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
  logo: {
    type: String,
    required: true,
  },
  size: {
    type: Number,
    default: 120,
  },
  duration: {
    type: Number,
    default: 2,
  },
  direction: {
    type: String,
    default: "alternate",
    validator: val => ["normal", "alternate"].includes(val),
  },
  opacity: {
    type: Number,
    default: 0.4,
    validator: val => val >= 0 && val <= 1,
  },
  messages: {
    type: Array,
    default: () => [],
  },
});

const currentMessage = ref("");
let intervalId = null;

function pickRandomMessage(exclude = "") {
  if (props.messages.length === 0) return "";
  let message;
  do {
    message = props.messages[Math.floor(Math.random() * props.messages.length)];
  } while (message === exclude && props.messages.length > 1);
  return message;
}

onMounted(() => {
  currentMessage.value = pickRandomMessage();

  if (props.messages.length > 1) {
    intervalId = setInterval(() => {
      currentMessage.value = pickRandomMessage(currentMessage.value);
    }, props.duration * 1000);
  }
});

onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.loader-container {
  position: fixed;
  inset: 0;
  background-color: white;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
  padding: 1rem;
}

.logo-wrapper {
  position: relative;
  display: inline-block;
  overflow: hidden;
}

.shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  animation-name: shine;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  pointer-events: none;
}

.loading-message {
  font-size: 1.25rem;
  color: #555;
  transition: opacity 0.4s ease;
}

@keyframes shine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}
</style>
