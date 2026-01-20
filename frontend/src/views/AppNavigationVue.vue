<template>
  <div>
    <v-app-bar color="surface" density="compact">
      <template v-slot:prepend>
        <v-menu v-if="isMobile" width="200">
          <template v-slot:activator="{ props }">
            <v-app-bar-nav-icon v-bind="props"></v-app-bar-nav-icon>
          </template>
          <v-list>
            <v-list-item
              prepend-icon="mdi-view-dashboard-variant"
              color="selected"
              @click="setAccount(null, True)"
              title="Dashboard"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-bank"
              to="/accounts"
              color="selected"
              title="Accounts"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-chart-bar"
              to="/forecast"
              color="selected"
              title="Forecast"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-bell"
              to="/reminders"
              color="selected"
              title="Reminders"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-folder"
              to="/planning"
              color="selected"
              title="Planning"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-tag"
              to="/tags"
              color="selected"
              title="Tags"
            ></v-list-item>
          </v-list>
        </v-menu>
        <v-img :width="132" aspect-ratio="1/1" cover src="logov2.png"></v-img>
      </template>
      <v-app-bar-title>
        <span class="text-caption font-weight-bold">v{{ version }}</span>
      </v-app-bar-title>
      <v-btn
        icon="mdi-theme-light-dark"
        @click="handleToggle"
        :color="isDark ? '#F5F5F5' : '#121212'"
        size="small"
      ></v-btn>
      <v-menu location="start">
        <template v-slot:activator="{ props }">
          <v-btn class="text-none" stacked v-bind="props">
            <v-badge
              :content="messages ? messages.unread_count : 0"
              color="error"
              v-if="messages && messages.unread_count > 0"
            >
              <v-icon icon="mdi-inbox-full"></v-icon>
            </v-badge>
            <v-icon icon="mdi-inbox" v-else></v-icon>
          </v-btn>
        </template>
        <v-card width="500" density="compact">
          <v-card-text>
            <v-list density="compact" nav>
              <v-list-item
                :prepend-icon="
                  message.unread
                    ? 'mdi-message-text'
                    : 'mdi-message-text-outline'
                "
                v-for="message in messages.messages"
                :key="message.id"
              >
                <v-list-item-title>
                  <span :class="message.unread ? 'font-weight-bold' : ''">
                    {{ message.message }}
                  </span>
                </v-list-item-title>
                <v-list-item-subtitle>
                  <span :class="message.unread ? 'font-weight-bold' : ''">
                    {{ getPrettyDate(message.message_date) }}
                  </span>
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="messages.total_count == 0">
                No messages : You're all caught up!
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions v-if="messages.total_count > 0">
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="markRead">Mark All Read</v-btn>
            <v-btn color="primary" @click="deleteAll">Delete All</v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
    </v-app-bar>
    <v-navigation-drawer color="primary" rail permanent v-if="mdAndUp">
      <v-list density="compact" nav>
        <v-tooltip text="Dashboard">
          <template v-slot:activator="{ props }">
            <v-list-item
              prepend-icon="mdi-view-dashboard-variant"
              v-bind="props"
              color="selected"
              @click="setAccount(null, True)"
            ></v-list-item>
          </template>
        </v-tooltip>
        <v-tooltip text="Accounts">
          <template v-slot:activator="{ props }">
            <v-list-item
              base-color="surface"
              :active="nav_toggle"
              prepend-icon="mdi-bank"
              @click="nav_toggle = true"
              v-bind="props"
              color="selected"
            ></v-list-item>
          </template>
        </v-tooltip>
        <v-tooltip text="Forecast">
          <template v-slot:activator="{ props }">
            <v-list-item
              prepend-icon="mdi-chart-bar"
              to="/forecast"
              v-bind="props"
              color="selected"
            ></v-list-item>
          </template>
        </v-tooltip>
        <v-tooltip text="Reminders">
          <template v-slot:activator="{ props }">
            <v-list-item
              prepend-icon="mdi-bell"
              to="/reminders"
              v-bind="props"
              color="selected"
            ></v-list-item>
          </template>
        </v-tooltip>
        <v-tooltip text="Planning">
          <template v-slot:activator="{ props }">
            <v-list-item
              base-color="surface"
              :active="!nav_toggle"
              prepend-icon="mdi-folder"
              @click="nav_toggle = false"
              v-bind="props"
              color="selected"
            ></v-list-item>
          </template>
        </v-tooltip>
        <v-tooltip text="Tags">
          <template v-slot:activator="{ props }">
            <v-list-item
              prepend-icon="mdi-tag"
              to="/tags"
              v-bind="props"
              color="selected"
            ></v-list-item>
          </template>
        </v-tooltip>
        <v-tooltip text="Settings">
          <template v-slot:activator="{ props }">
            <v-list-item
              prepend-icon="mdi-cog"
              as="a"
              href="/admin"
              v-bind="props"
              color="selected"
            ></v-list-item>
          </template>
        </v-tooltip>
      </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer permanent width="250" color="surface" v-if="mdAndUp">
      <AccountsMenu v-if="nav_toggle" />
      <PlanningMenu v-if="!nav_toggle" />
    </v-navigation-drawer>
  </div>
</template>
<script setup>
import { ref, watch, computed } from "vue";
import { useDisplay, useTheme } from "vuetify";
import { useThemeStore } from "@/stores/themeStore";

const theme = useTheme();
const themeStore = useThemeStore();

theme.change(themeStore.currentTheme);

const isDark = computed({
  get: () => themeStore.currentTheme === "myCustomDarkTheme",
  set: value => {
    themeStore.setTheme(value ? "myCustomDarkTheme" : "myCustomLightTheme");
  },
});

const version = import.meta.env.VITE_APP_VERSION;

const { mdAndUp, smAndDown } = useDisplay();
const isMobile = smAndDown;
const nav_toggle = ref(true);

const getPrettyDate = uglyDate => {
  const newDate = new Date(uglyDate);
  const formattedDate = newDate.toLocaleString("en-US");
  return formattedDate;
};

watch(
  () => themeStore.currentTheme,
  newTheme => {
    theme.change(newTheme);
  },
);

function handleToggle() {
  themeStore.toggleTheme();
}
</script>
