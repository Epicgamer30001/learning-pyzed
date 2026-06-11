import pyzed.sl as sl

devices = sl.Camera.get_device_list()
for dev in devices:
    print(f"ID: {dev.id}  |  Model: {dev.camera_model}  |  Serial: {dev.serial_number}")
