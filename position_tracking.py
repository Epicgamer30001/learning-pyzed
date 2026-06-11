import pyzed.sl as sl
import time 
import math

def quaternion_to_rpy(x, y, z, w):
    # roll (rotation around X)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = round(math.atan2(sinr_cosp, cosr_cosp),3)

    # pitch (rotation around Y)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = round(math.copysign(math.pi / 2, sinp),3)   # clamp at ±90° (gimbal lock)
    else:
        pitch = round(math.asin(sinp),3)

    # yaw (rotation around Z)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = round(math.atan2(siny_cosp, cosy_cosp),3)

    d_roll = round(math.degrees(roll),3)
    d_yaw = round(math.degrees(yaw),3)
    d_pitch = round(math.degrees(pitch),3)


    return roll, pitch, yaw, d_roll, d_pitch ,d_yaw 





def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 or HD1200 video mode (default fps: 60)
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP # Use a right-handed Y-up coordinate system
    init_params.coordinate_units = sl.UNIT.METER  # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()

    py_transform = sl.Transform() #py_transform is the position at that moment
    tracking_parameters = sl.PositionalTrackingParameters(_init_pos=py_transform)  #treat initial as origin

    err = zed.enable_positional_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Enable positional tracking : " + repr(err) + "Exit Program.")
        zed.close()
        exit()

    zed_pose = sl.Pose()  #container that holds the cameras position and orientation 

    zed_sensors = sl.SensorsData()   #holds sensordata

    runtime_params = sl.RuntimeParameters()

    can_compute_imu = zed.get_camera_information().camera_model != sl.MODEL.ZED

    for i in range(1000):
        time.sleep(0.5)
        if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:

            zed.get_position(zed_pose, sl.REFERENCE_FRAME.WORLD)  #puts position in zed_pose object

            

            #x,y,z translation(where camera is)
            py_translation = sl.Translation()
            tx = round(zed_pose.get_translation(py_translation).get()[0], 3)
            ty = round(zed_pose.get_translation(py_translation).get()[1], 3)
            tz = round(zed_pose.get_translation(py_translation).get()[2], 3)
            print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(tx, ty, tz, zed_pose.timestamp.get_milliseconds()))


            #xyz orientation in quaternions: x,y,z is axis, w is how much its rotated by
            py_orientation = sl.Orientation()
            ox = round(zed_pose.get_orientation(py_orientation).get()[0], 3)
            oy = round(zed_pose.get_orientation(py_orientation).get()[1], 3)
            oz = round(zed_pose.get_orientation(py_orientation).get()[2], 3)
            ow = round(zed_pose.get_orientation(py_orientation).get()[3], 3)
            print("Orientation: Ox: {0}, Oy: {1}, Oz {2}, Ow: {3}\n".format(ox, oy, oz, ow))


            roll, pitch, yaw, d_roll, d_pitch ,d_yaw = quaternion_to_rpy(ox, oy, oz, ow)

            print(f"Radians -> roll={roll}  pitch={pitch}  yaw={yaw}")
            print(f"Degrees -> roll={d_roll}  pitch={d_pitch}  yaw={d_yaw}")

            if can_compute_imu:
                zed.get_sensors_data(zed_sensors, sl.TIME_REFERENCE.IMAGE)
                zed_imu = zed_sensors.get_imu_data()
                #Display the IMU acceleratoin
                acceleration = [0,0,0]
                zed_imu.get_linear_acceleration(acceleration)
                ax = round(acceleration[0], 3)
                ay = round(acceleration[1], 3)
                az = round(acceleration[2], 3)
                print("IMU Acceleration: Ax: {0}, Ay: {1}, Az {2}\n".format(ax, ay, az))
                
                #Display the IMU angular velocity
                a_velocity = [0,0,0]
                zed_imu.get_angular_velocity(a_velocity)
                vx = round(a_velocity[0], 3)
                vy = round(a_velocity[1], 3)
                vz = round(a_velocity[2], 3)
                print("IMU Angular Velocity: Vx: {0}, Vy: {1}, Vz {2}\n".format(vx, vy, vz))

                # Display the IMU orientation quaternion
                zed_imu_pose = sl.Transform()
                ox = round(zed_imu.get_pose(zed_imu_pose).get_orientation().get()[0], 3)
                oy = round(zed_imu.get_pose(zed_imu_pose).get_orientation().get()[1], 3)
                oz = round(zed_imu.get_pose(zed_imu_pose).get_orientation().get()[2], 3)
                ow = round(zed_imu.get_pose(zed_imu_pose).get_orientation().get()[3], 3)
                print("IMU Orientation: Ox: {0}, Oy: {1}, Oz {2}, Ow: {3}\n".format(ox, oy, oz, ow))
                


    zed.close()

if __name__ == "__main__":
    main()

