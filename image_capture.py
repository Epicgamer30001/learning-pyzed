import pyzed.sl as sl

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
    

    image = sl.Mat()  #image buffer
    runtime_parameters = sl.RuntimeParameters()  #camera setting to capture

    for i in range(50):
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:   #runtime params must be given to grab()
            zed.retrieve_image(image, sl.VIEW.LEFT)  #retrieve left, right, depth, or SIDEBY SIDE
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  #current time
            print(f"image res: {image.get_width()} x {image.get_height()} || timestamp {timestamp.get_milliseconds()}!!!!")

    
    zed.close()


if __name__ == "__main__":
    main()
