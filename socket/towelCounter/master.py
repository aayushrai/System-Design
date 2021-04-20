

import requests
import sys
import cv2
import numpy as np
from ctypes import *
from time import time
from loguru import logger

from imports.CameraParams_const import *
from imports.CameraParams_header import *
from imports.MvCameraControl_class import *
from imports.MvCameraControl_header import *
from imports.MvErrorDefine_const import *
from imports.PixelType_const import *
from imports.PixelType_header import *

from detector import detect
from logic import count_towels


import io
import socket
import struct
import pickle
import zlib



def is_dir(path):
    """Helper function which creates directory if it does not exist

    Args:
        path ([str]): Path of the directory to be created if does not exist
    """
    if not os.path.isdir(path):
        logger.debug(f'Creating {path}...')
        os.mkdir(path)


def error_message(message):
    """Helper function which logs error message and exits

    Args:
        message ([str]): Message to be displayed
    """
    logger.error(message)
    sys.exit()


def warning_message(message):
    """Helper function which logs warning message

    Args:
        message ([str]): Message to be displayed
    """
    logger.warning(message)


def setup_host():
    """Returns list of devices connected

    Returns:
        [list]: List of connected devices
    """
    SDKVersion = MvCamera.MV_CC_GetSDKVersion()
    logger.debug(f'SDKVersion: {SDKVersion}')

    device_type = MV_GIGE_DEVICE
    device_list = MV_CC_DEVICE_INFO_LIST()

    ret = MvCamera.MV_CC_EnumDevices(device_type, device_list)
    if ret != 0:
        error_message(f'Enum of Devices Failed! ret[0x{ret}]')

    if device_list.nDeviceNum == 0:
        error_message('No Device Found!')

    logger.debug(f'{device_list.nDeviceNum} Devices Found!')

    return device_list


def show_devices_ip(device_list):
    """Prints IP of connected devices

    Args:
        device_list ([list]): List of connected devices
    """
    for itr in range(0, device_list.nDeviceNum):
        mvcc_dev_info = cast(device_list.pDeviceInfo[itr], POINTER(
            MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            logger.debug(f'GIGE Device: {itr}')

            model_name = ""
            for word in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                model_name = model_name + chr(word)

            logger.debug(f'Device Model Name: {model_name}')

            nip1 = (
                (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = (
                (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = (
                (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            logger.debug(f'Current IP: {nip1}.{nip2}.{nip3}.{nip4}')


def get_camera_object(device_list):
    """Returns a camera object for the selected device from device_list

    Args:
        device_list ([list]): List of connected devices

    Returns:
        [MvCamera]: MvCamera object
    """
    # This value holds index of the connected devices
    # During scaling, this value should be changed if more than 1 devices are connected to the host
    # It can also be taken as an input via terminal
    connection_number = 0

    if int(connection_number) >= device_list.nDeviceNum:
        error_message(f'Invalid Input. {device_list.nDeviceNum} Devices Found')

    cap = MvCamera()

    selected_device = cast(device_list.pDeviceInfo[int(
        connection_number)], POINTER(MV_CC_DEVICE_INFO)).contents

    ret = cap.MV_CC_CreateHandle(selected_device)
    if ret != 0:
        error_message(f'Handle Creation Failed! ret[0x{ret}]')

    ret = cap.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        error_message(f'Opening Device Failed! ret[0x{ret}]')

    return cap


def get_payload_size(cap):
    """Returns optimum payload size

    Args:
        cap ([MvCamera]): MvCamera object for selected device

    Returns:
        [Any]: Optimum payload size
    """
    # Detecting Optimal Packet Size for the Network (works only for GIGE Camera)
    packet_size = cap.MV_CC_GetOptimalPacketSize()
    if packet_size > 0:
        ret = cap.MV_CC_SetIntValue('GevSCPSPacketSize', packet_size)
        if ret != 0:
            warning_message(f'Failed when Setting Packet Size! ret[0x{ret}]')
    else:
        warning_message(
            f'Failed when Getting Packet Size! ret[0x{packet_size}]')

    ret = cap.MV_CC_SetEnumValue('TriggerMode', MV_TRIGGER_MODE_OFF)
    if ret != 0:
        error_message(f'Failed when Setting Trigger Mode! ret[0x{ret}]')

    # Get Payload Size
    st_param = MVCC_INTVALUE()

    memset(byref(st_param), 0, sizeof(MVCC_INTVALUE))

    ret = cap.MV_CC_GetIntValue('PayloadSize', st_param)
    if ret != 0:
        error_message(f'Failed when Getting Payload Size! ret[0x{ret}]')

    payload_size = st_param.nCurValue

    ret = cap.MV_CC_StartGrabbing()
    if ret != 0:
        error_message(f'Failed when Starting Grabbing of Frames! ret[0x{ret}]')

    return payload_size


def get_numpy_array(frame_info, data_pointer):
    """Returns frame as an ndarray

    Args:
        frame_info ([Any]): Information of the frame
        data_pointer ([Any]): Pointer to the memory location that holds the frame

    Returns:
        [ndarray]: Image as an ndarray
    """
    if data_pointer is None:
        return None

    st_param = MV_SAVE_IMAGE_PARAM_EX()
    st_param.nWidth = frame_info.nWidth
    st_param.nHeight = frame_info.nHeight
    st_param.nDataLen = frame_info.nFrameLen
    st_param.pData = cast(data_pointer, POINTER(c_ubyte))

    frame_buffer = (c_ubyte * st_param.nDataLen)()
    try:
        memmove(byref(frame_buffer), st_param.pData, st_param.nDataLen)
        frame = np.array(frame_buffer[:], dtype=np.uint8)
        frame = np.reshape(frame, (st_param.nHeight, st_param.nWidth, -1))
        frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_RG2RGB)
    except Exception as e:
        error_message(e)
    if frame_buffer is not None:
        del frame_buffer

    return frame


def create_request_to_ai_engine(engine,frame,frame_no,group):
    try:
        result, frame = cv2.imencode('.jpg', frame, encode_param)
    #    data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps([frame,frame_no,group], 0)
        size = len(data)
        engine.sendall(struct.pack(">L", size) + data)
    except Exception as e:
        print("Error while sending frame to ai engine")
  
engines  = []      
engineCounter = 0
group = "a"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 6000))
connection = client_socket.makefile('wb')
engines.append(client_socket)

client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1.connect(('127.0.0.1', 6001))
connection1 = client_socket1.makefile('wb')
engines.append(client_socket1)

client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect(('127.0.0.1', 6002))
connection2 = client_socket2.makefile('wb')
engines.append(client_socket2)

client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket3.connect(('127.0.0.1', 6003))
connection3 = client_socket3.makefile('wb')
engines.append(client_socket3)
      
def fetch_frames(cap=0, data_pointer=0, payload_size=0):
    """Fetches frames from camera module and converts to numpy array

    Args:
        cap (int, MvCamera): MvCamera object. Defaults to 0.
        data_pointer (int, Any): Pointer to the memory location that holds the frame. Defaults to 0.
        payload_size (int, Any): Optimum payload size. Defaults to 0.
    """
    global engineCounter,engines
    frame_info = MV_FRAME_OUT_INFO_EX()
    memset(byref(frame_info), 0, sizeof(frame_info))
    while True:
        ret = cap.MV_CC_GetOneFrameTimeout(
            data_pointer, payload_size, frame_info, 73)
        if ret == 0:
            logger.debug(
                f'Fetched: Width[{frame_info.nWidth}], Height[{frame_info.nHeight}], PixelType[0x{frame_info.enPixelType}], FrameNumber[{frame_info.nFrameNum}]')

            frame = get_numpy_array(frame_info, data_pointer)
            
            if engineCounter >= 4:
                engineCounter = 0
                group = ord(group) + 1
                group = chr(group)
            
            if group > "z":
                group = "a"
                
            create_request_to_ai_engine(engines[engineCounter],frame,frameNumber,group)
            engineCounter += 1
            
            
            if frame is None:
                ret = cap.MV_CC_StopGrabbing()
                if ret != 0:
                    error_message(
                        f'Failed when Stopping Grabbing of Frames! ret[0x{ret}]')

                ret = cap.MV_CC_CloseDevice()
                if ret != 0:
                    error_message(f'Closing Device Failed! ret[0x{ret}]')

                ret = cap.MV_CC_DestroyHandle()
                if ret != 0:
                    error_message(f'Destrying Handle Failed! ret[0x{ret}]')
                error_message('Frame is None!')
        else:
            ret = cap.MV_CC_StopGrabbing()
            if ret != 0:
                error_message(
                    f'Failed when Stopping Grabbing of Frames! ret[0x{ret}]')

            ret = cap.MV_CC_CloseDevice()
            if ret != 0:
                error_message(f'Closing Device Failed! ret[0x{ret}]')

            ret = cap.MV_CC_DestroyHandle()
            if ret != 0:
                error_message(f'Destrying Handle Failed! ret[0x{ret}]')
            error_message(f'No Data [0x{ret}]')


def main(print_devices_ip=False):
    """Main function which handles the calling

    Args:
        print_devices_ip (bool): Flag for printing IP of connected devices. Defaults to False.
        run_detector (bool): Flag for choosing between auto_annotator and detector. Defaults to True.
    """
    device_list = setup_host()

    if print_devices_ip:
        show_devices_ip(device_list)

    cap = get_camera_object(device_list)

    payload_size = get_payload_size(cap)

    data_buffer = (c_ubyte * payload_size)()
    
    fetch_frames(cap,
                 byref(data_buffer), payload_size)


if __name__ == '__main__':
    main()

