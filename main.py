from kivy.app import App
import serial.tools.list_ports
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import esptool
import sys

class DemoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        ports = serial.tools.list_ports.comports()
        for btn_str in ports:
            button = Button(
                text=f"{btn_str.device}",
                size_hint=(None, None),
                size=("280dp", "50dp"),
                on_release=self.on_button_click
            )
            layout.add_widget(button)
        return layout

    def on_button_click(self, instance):
        port = instance.text
        flash_address = "0x10000"
        firmware_path = r".\firmware-custom.bin"
        baud_rate = 115200

        try:
            sys.argv = [
                "esptool.py",
                "--port",
                port,
                "--baud",
                str(baud_rate),
                "write_flash",
                "-z",
                flash_address,
                firmware_path,
            ]

            esptool.main()
            print("\nFlashing completed successfully!")

        except Exception as e:
            print(f"\nError flashing ESP32: {e}")

demoApp = DemoApp()
demoApp.run()