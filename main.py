from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import time
import random

# PubNub Configuration
pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-1bcad5c9-063b-4ef2-af21-63beef749a96"
pnconfig.subscribe_key = "sub-c-152b2f8c-6bde-462a-b24b-acbcf550a503"
pnconfig.uuid = "iot-home-security"
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

# States
magnetic_sensor_enabled = True
motion_sensor_enabled = True
buzzer_enabled = True
rgb_led_enabled = True
notifications_enabled = True

# Simulate sensor data
def simulate_sensors():
    data = {
        "type": "sensor_data",  # Indicate this is sensor data
        "window_status": "open" if magnetic_sensor_enabled else "disabled",
        "motion_detected": random.choice([True, False]) if motion_sensor_enabled else "disabled",
        "rgb_led": "red" if rgb_led_enabled else "disabled",
        "buzzer": "on" if buzzer_enabled else "disabled",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": pnconfig.uuid,
    }
    return data

# Callback for handling publish results
def publish_callback(result, status):
    if status.is_error():
        print(f"Failed to publish data: {status.error_data.information if status.error_data else 'Unknown error'}")
    else:
        print(f"Message published successfully! Timetoken: {result.timetoken}")

# Handle commands
class CommandCallback(SubscribeCallback):
    def message(self, pubnub, event):
        global magnetic_sensor_enabled, motion_sensor_enabled, buzzer_enabled, rgb_led_enabled, notifications_enabled
        command = event.message

        # Handle commands only
        if command.get("type") == "command" and command.get("room") == "Kitchen":
            sensor = command.get("sensor")
            status = command.get("status") == "on"
            if sensor == "magnetic_sensor":
                magnetic_sensor_enabled = status
            elif sensor == "motion_sensor":
                motion_sensor_enabled = status
            elif sensor == "buzzer":
                buzzer_enabled = status
            elif sensor == "led":
                rgb_led_enabled = status
            elif sensor == "notifications":
                notifications_enabled = status
            print(f"Updated {sensor} to {'enabled' if status else 'disabled'}")

# Publish mock data
def publish_mock_data():
    while True:
        data = simulate_sensors()
        pubnub.publish().channel("iot-home-security").message(data).pn_async(publish_callback)
        print(f"Published: {data}")
        time.sleep(5)

if __name__ == "__main__":
    pubnub.add_listener(CommandCallback())
    pubnub.subscribe().channels("iot-home-security").execute()
    publish_mock_data()