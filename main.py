from kivymd.app import MDApp
from kivy.lang import Builder
import serial.tools.list_ports
from kivymd.uix.button import MDRectangleFlatButton
import esptool
import sys

KV = '''
BoxLayout:
    orientation: "vertical"
    MDLabel:
        text: "Click a Button to Send String"
        halign: "center"
        theme_text_color: "Secondary"
    ScrollView:
        MDList:
            id: button_list
'''

class DemoApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        ports = serial.tools.list_ports.comports()
        for btn_str in ports:
            button = MDRectangleFlatButton(
                text=f"{btn_str.device}",
                size_hint=(None, None),
                size=("280dp", "50dp"),
                on_release=self.on_button_click
            )
            self.root.ids.button_list.add_widget(button)

    def on_button_click(self, instance):
        port = instance.text
        flash_address = "0x10000"
        firmware_path = r".\firmware-custom.bin"
        baud_rate = 115200

        try:
            # Initialize the esptool arguments
            sys.argv = [
                "esptool.py",
                "--port",
                port,
                "--baud",
                str(baud_rate),
                "write_flash",
                "-z",
                "0x1000",
                firmware_path,
            ]

            # Execute the flashing process
            esptool.main()
            print("\nFlashing completed successfully!")

        except Exception as e:
            print(f"\nError flashing ESP32: {e}")

demoApp = DemoApp()
demoApp.run()