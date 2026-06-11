import pyzed.sl as sl 
import math 
import numpy as np
import sys


def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Use NEURAL depth mode
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use meter units (for depth measurements)
    init_params.camera_fps = 30


    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS: #Ensure the camera has opened succesfully
        print("Camera Open : "+repr(status)+". Exit program.")
        exit()

    runtime_parameters = sl.RuntimeParameters()

    image = sl.Mat()
    depth = sl.Mat()  #data buffers 
    point_cloud = sl.Mat()

    mirror_ref = sl.Transform()   #creates translation and rotation matrix
    mirror_ref.set_translation(sl.Translation(2.75,4.0,0))   #(x,y,z) = (0,0,0)
    

    for i in range(50):

        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:

            zed.retrieve_image(image, sl.VIEW.LEFT)

            zed.retrieve_measure(depth,sl.MEASURE.DEPTH)  #depth map in bufffer

            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)  #point cloud in buffer


            #calculate middle pixel of the camera 
            x = round(image.get_width()/2)
            y = round(image.get_height()/2)
            err,point_cloud_value = point_cloud.get_value(x,y)  #get depth at middle pixel

            #euclidian distance (?)
            if math.isfinite(point_cloud_value[2]):
                distance = math.sqrt(point_cloud_value[0]*point_cloud_value[0] + point_cloud_value[1]*point_cloud_value[1] + point_cloud_value[2]*point_cloud_value[2])
                print(f"Distance to Camera at pixel {{{x};{y}}}: {distance}")
            else:
                print("Distance cannot be computed.")

    zed.close()

if __name__ == "__main__":
    main()



