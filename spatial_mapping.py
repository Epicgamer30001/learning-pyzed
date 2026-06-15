import pyzed.sl as sl 
import sys 


def main():
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.set_from_camera_id(1)
    init_params.camera_resolution = sl.RESOLUTION.AUTO  # Use HD720 or HD1200 video mode (default fps: 60)
    # Use a right-handed Y-up coordinate system
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init_params.coordinate_units = sl.UNIT.METER  # Set units in meters


    err = zed.open(init_params)

    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open:  "+ repr(err) + "exit")
        exit()

    
    py_transform = sl.Transform()   #initial position boilerplate
    tracking_parameters = sl.PositionalTrackingParameters(_init_pos = py_transform)
    err = zed.enable_positional_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Enable positional tracking : "+repr(err)+". Exit program.")
        zed.close()
        exit()

    mapping_params = sl.SpatialMappingParameters(map_type = sl.SPATIAL_MAP_TYPE.MESH)  #initialize spatial mapping 
    err = zed.enable_spatial_mapping(mapping_params)
    if err != sl.ERROR_CODE.SUCCESS:    #error checking
        print("Enable spatial mapping : "+repr(err)+". Exit program.")
        zed.close()
        exit(1)

    mesh = sl.Mesh()  #mesh object
    runtime_parameters = sl.RuntimeParameters()
    n= 10000
    for i in range(n):

        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:

            mapping_state = zed.get_spatial_mapping_state()
            sys.stdout.write(f"Images captured:  {i}/{n} || {mapping_state} \n")
            sys.stdout.flush()
    print("\n")

    print("Extracting mesh \n")
    err = zed.extract_whole_spatial_map(mesh)
    print(repr(err))
    print("Filtering mesh \n")

    mesh.filter(sl.MeshFilterParameters())  #remove unneccesary vertices and faces
    print("Saving mesh \n")
    mesh.save("mesh.obj")

    zed.disable_spatial_mapping()
    zed.disable_positional_tracking()
    zed.close()

if __name__ == "__main__":
    main()