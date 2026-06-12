import pyzed.sl as sl 
import sys 


def main():
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.AUTO  # Use HD720 or HD1200 video mode (default fps: 60)
    # Use a right-handed Y-up coordinate system
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init_params.coordinate_units = sl.UNIT.METER  # Set units in meters


    error = zed.open(init_params)

    if err != s1.ERROR_CODE.SUCCESS:
        print("Camera Open:  "+ repr(err) + "exit")
        exit()

    
    py_transform = sl.Transform()
