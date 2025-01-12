document.addEventListener("DOMContentLoaded", function () {
  // Log to confirm script is loaded
  console.log("PubNub script loaded successfully");

  // Initialize PubNub
  const pubnub = new PubNub({
    publishKey: "pub-c-1bcad5c9-063b-4ef2-af21-63beef749a96",
    subscribeKey: "sub-c-152b2f8c-6bde-462a-b24b-acbcf550a503",
    uuid: "website-client",
    ssl: true,
    cipher: "1OGZnDanEaRiuMYXZpHU7G448cnJ1onrFL_pitQgaI8=", // Using cipher key
  });

  // Subscribe to the "iot-home-security" channel
  pubnub.subscribe({
    channels: ["iot-home-security"], // Commands and data are sent here
  });

  // Listen for incoming messages
  pubnub.addListener({
    message: function (event) {
      console.log("Message Received:", event.message);

      // Update the webpage dynamically with received data
      if (event.message.type === "sensor_data") {
        updatePage(event.message);
      }
    },
    status: function (statusEvent) {
      if (statusEvent.category === "PNConnectedCategory") {
        console.log("Connected to PubNub channel: iot-home-security");
      }
    },
  });

  // Function to send settings to hardware
  function sendSettingsToHardware(settings) {
    const commandMessage = {
      type: "command", // Distinguish between commands and sensor data
      ...settings,
      sender: "website-client",
      timestamp: new Date().toISOString(),
    };

    // Encrypt the commandMessage using the CIPHER_KEY
    const encryptedMessage = encryptMessage(commandMessage);

    // Publish encrypted message to the same channel
    pubnub.publish(
      {
        channel: "iot-home-security",
        message: { data: encryptedMessage }, // Send encrypted data
      },
      function (status, response) {
        if (status.error) {
          console.error("Failed to send settings:", status);
        } else {
          console.log("Settings sent successfully:", response);
        }
      }
    );
  }

  // Function to encrypt message using the provided CIPHER_KEY
  function encryptMessage(message) {
    const messageString = JSON.stringify(message); // Convert message to string
    const encryptedMessage = CryptoJS.AES.encrypt(
      messageString,
      "1OGZnDanEaRiuMYXZpHU7G448cnJ1onrFL_pitQgaI8="
    ).toString();
    console.log("Encrypted message:", encryptedMessage);
    return encryptedMessage;
  }

  // Attach event listeners to toggles
  document.querySelectorAll(".sensor-toggle").forEach((toggle) => {
    toggle.addEventListener("change", (event) => {
      const sensor = toggle.dataset.sensor; // e.g., "motion_sensor"
      const status = toggle.checked ? "on" : "off"; // "on" or "off"
      const room = toggle.closest(".room-card").dataset.room; // Room name
      const settings = {
        room: room,
        sensor: sensor,
        status: status,
      };
      console.log("Sending settings to hardware:", settings);
      sendSettingsToHardware(settings);
    });
  });

  // Function to dynamically update the page
  function updatePage(data) {
    const logContainer = document.getElementById("log-container");
    if (logContainer) {
      const newLog = document.createElement("div");
      newLog.style.marginBottom = "10px";
      newLog.style.border = "1px solid #ddd";
      newLog.style.padding = "5px";
      newLog.style.borderRadius = "5px";
      newLog.style.backgroundColor = "#f9f9f9";

      newLog.innerHTML = `
          <strong>Timestamp:</strong> ${data.timestamp} <br>
          <strong>Device:</strong> ${data.device} <br>
          <strong>Window Status:</strong> ${data.window_status} <br>
          <strong>Motion Detected:</strong> ${data.motion_detected} <br>
          <strong>RGB LED:</strong> ${data.rgb_led} <br>
          <strong>Buzzer:</strong> ${data.buzzer}
        `;

      logContainer.prepend(newLog);
    }
  }
});
