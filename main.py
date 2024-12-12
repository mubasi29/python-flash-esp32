from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
import threading
import esptool
import sys

if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    from serial.tools import list_ports

class DemoApp(App):
    def __init__(self, *args, **kwargs):
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.read_thread = None
        self.port_thread_lock = threading.Lock()
        self.on_scan_device()
        super(DemoApp, self).__init__(*args, **kwargs)

    def build(self):
        layout = BoxLayout(orientation='vertical')
        ports = self.device_name_list
        print(ports)
        for btn_str in ports:
            button = Button(
                text=f"{btn_str}",
                size_hint=(None, None),
                size=("280dp", "50dp"),
                on_release=self.on_button_click
            )
            layout.add_widget(button)
        return layout

    def on_scan_device(self):
        if platform == 'android':
            usb_device_list = usb.get_usb_device_list()
            self.device_name_list = [
                device.getDeviceName() for device in usb_device_list
            ]
        else:
            usb_device_list = list_ports.comports()
            self.device_name_list = [port.device for port in usb_device_list]

    def on_stop(self):
        if self.serial_port:
            with self.port_thread_lock:
                self.serial_port.close()

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

if __name__ == '__main__':
    DemoApp().run()