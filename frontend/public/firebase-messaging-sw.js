// public/firebase-messaging-sw.js
importScripts("https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.7.0/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyApfjxHUXQc9WD5iLDUlbGRExCb2OBmwoM",
  authDomain: "sharevents-bac56.firebaseapp.com",
  projectId: "sharevents-bac56",
  storageBucket: "sharevents-bac56.firebasestorage.app",
  messagingSenderId: "168906945433",
  appId: "1:168906945433:web:2873aef8d0a91d27c55908",
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  // self.registration.showNotification("payload.showNotification.title", {
  //   body: "payload.showNotification.body",
  //   icon: "/web-app-manifest-192x192.png",
  // });
  console.log("fsiofjhfisjojfoijsdofjoifjopdfjsofjsjfsfjdosdjfsdoijfosjfoidjso")
});