import autoclass
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
import threading
import esptool
import sys
import os

if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    from serial.tools import list_ports

def request_permission():
    if platform == 'android':
       from android.permissions import request_permissions, Permission
       request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

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
        
        if len(ports) == 0:
            layout.add_widget(Label(text = 'empty '))

        # if platform == "android":
        #     # Android-specific UI
        #     button = Button(text="Select File (Android)")
        #     button.bind(on_press=self.select_android_file)
        #     layout.add_widget(button)
            
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


    def select_android_file(self, instance):
        self.open_file_picker()


    def open_file_picker(self):
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Intent = autoclass("android.content.Intent")

        intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.setType("*/*")  # Select all file types, filter later if needed
        intent.addCategory(Intent.CATEGORY_OPENABLE)

        activity = PythonActivity.mActivity
        activity.startActivityForResult(intent, 1)

    def on_button_click(self, instance):
        port = instance.text
        flash_address = "0x10000"
        # firmware_path = "/storage/emulated/0/Download/StatusSaverApp/firmware-custom-1.bin"
        firmware_path = "res/file/firmware-custom.bin"
        baud_rate = 115200
        
        if not os.path.exists(firmware_path):
        	print(firmware_path)
        	print("\nfile not exits")
        	return
        

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
    request_permission()
    DemoApp().run()
