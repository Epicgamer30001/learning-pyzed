import pyzed.sl as sl 
import time 

def main():
    #create camera object 
    zed = sl.Camera()

    #create Init parametsrs object and set parameters 
    init_params = sl.InitParameters()
    init_params.sdk_verbose = 0 
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30

    #open camera with parameters specified
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : " + repr(err)+"Exit Program.")
        exit(1)
    
    #get camera info 
    zed_serial = zed.get_camera_information().serial_number
    for i in range(10000):
        print(f"Yooooooo serial number ->  {zed_serial}")


    time.sleep(3)

    #close the camera 
    zed.close()

if __name__ == "__main__":
    main()

