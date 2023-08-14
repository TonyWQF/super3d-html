import socket
from threading import Thread
import time

class MachineStatus:
  def __init__(self):
    self.nozzle_temp = -15
    self.bed_temp = -15
    self.nozzle_target_temp = 0
    self.bed_target_temp = 0
    self.fan_0 = 0
    self.fan_1 = 0
    self.fan_2 = 0
    self.fan_3 = 0
    self.fan_4 = 0
    self.fan_5 = 0
    self.endstop = 0
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0
    self.e = 0.0
    self.print_percent = 0
    self.status = 0
    self.strStatus = ["PRINT_STATE_IDLE", "PRINT_STATE_PRINTING", "PRINT_STATE_PAUSE", "PRINT_STATE_PAUSE_PROCESSING", "PRINT_STATE_FAULT_PAUSE", "PRINT_STATE_FAULT_PAUSE_PROCESSING", "PRINT_STATE_ENDDING", "PRINT_STATE_PAUSE_RESUME", "PRINT_STATE_POWER_LOST_RESUME", "PRINT_STATE_PROCESSING", "PRINT_STATE_FIL_FAULT_PAUSE", "PRINT_STATE_FIL_FAULT_PROCESSING", "PRINT_STATE_MEDIA_FAULT_PAUSE", "PRINT_STATE_MEDIA_FAULT_PROCESSING", "PRINT_STATE_ABL_PROCESSING", "PRINT_STATE_MBL_PROCESSING", "PRINT_STATE_HOMING", "PRINT_STATE_ZOFFSET_PROCESSING", "PRINT_STATE_POWER_LOST"]

  def to_string_array(self):
    str_value = []
    str_value.append(self.strStatus[self.status])
    str_value.append(str(self.nozzle_temp))
    str_value.append(str(self.nozzle_target_temp))
    str_value.append(str(self.bed_temp))
    str_value.append(str(self.bed_target_temp))
    str_value.append(str(self.x))
    str_value.append(str(self.y))
    str_value.append(str(self.z))
    str_value.append(str(self.e))
    str_value.append(str(self.fan_0))
    str_value.append(str(self.fan_1))
    str_value.append(str(self.fan_2))
    str_value.append(str(self.fan_3))
    str_value.append(str(self.fan_4))
    str_value.append(str(self.fan_5))
    str_value.append(str(self.endstop))
    retval = ','.join(str_value)
    return '[' + retval + ']'

class Commands:
  def __init__(self):
    self.__CMD_STATUS              = 0x08
    self.__SCMD_STAT_MACHINE       = 0x00
    self.__SCMD_STAT_FEEDRATE      = 0x01
    self.__SCMD_STAT_POWERLOST_FLAG = 0x02
    self.__SCMD_STAT_FLOWRATE      = 0x03
    self.__SCMD_STAT_REMAIN_TIME   = 0x04

    self.__CMD_CONTROL             = 0x0C
    self.__SCMD_CTRL_FAN           = 0x01
    self.__SCMD_CTRL_HEATER        = 0x02
    self.__SCMD_CTRL_HOME          = 0x03
    self.__SCMD_CTRL_HOME_AXIS     = 0x04
    self.__SCMD_CTRL_MOVE          = 0x05
    self.__SCMD_CTRL_MOTOR_OFF     = 0x06
    self.__SCMD_CTRL_EXTRUDE       = 0x07
    self.__SCMD_CTRL_RETRACT       = 0x08
    self.__SCMD_CTRL_STOP_STEPPER  = 0x09
    self.__SCMD_CTRL_FEEDRATE      = 0x0a
    self.__SCMD_CTRL_FLOWRATE      = 0x0b
    self.__SCMD_CTRL_EMERGENCY_STOP      = 0x0C
    self.__SCMD_CTRL_LASER_PERCENT = 0x0D
    self.__SCMD_CTRL_LASER_ENABLE  = 0x0E
    self.__SCMD_CTRL_LASER_FOCUS   = 0x0F
    self.__SCMD_CTRL_GET_LASER_PERCENT   = 0x10
    
    self.machine_status = MachineStatus()
    self.connect_id = 0

  def analize(self, data):
    self.connect_id = data[3]
    self.machine_status.status = int.from_bytes(data[4:5], byteorder='little', signed=False)
    if(data[0] == self.__CMD_STATUS):
      if(data[1] == self.__SCMD_STAT_MACHINE):
        self.parse_status(data)

    retval = [data[0], data[1], data[2]]

  def parse_status(self, data):
    self.machine_status.nozzle_temp = int.from_bytes(data[6:8], byteorder='little', signed=True)
    self.machine_status.nozzle_target_temp = int.from_bytes(data[8:10], byteorder='little', signed=True)
    self.machine_status.bed_temp = int.from_bytes(data[10:12], byteorder='little', signed=True)
    self.machine_status.bed_target_temp = int.from_bytes(data[12:14], byteorder='little', signed=True)
    self.machine_status.x = int.from_bytes(data[14:18], byteorder='little', signed=True) / 1000.0
    self.machine_status.y = int.from_bytes(data[18:22], byteorder='little', signed=True) / 1000.0
    self.machine_status.z = int.from_bytes(data[22:26], byteorder='little', signed=True) / 1000.0
    self.machine_status.e = int.from_bytes(data[26:30], byteorder='little', signed=True) / 1000.0
    self.machine_status.print_percent = int.from_bytes(data[30:32], byteorder='little', signed=True)
    self.machine_status.fan_0 = int.from_bytes(data[32:33], byteorder='little', signed=False)
    self.machine_status.fan_1 = int.from_bytes(data[33:34], byteorder='little', signed=False)
    self.machine_status.fan_2 = int.from_bytes(data[34:35], byteorder='little', signed=False)
    self.machine_status.fan_3 = int.from_bytes(data[35:36], byteorder='little', signed=False)
    self.machine_status.fan_4 = int.from_bytes(data[36:37], byteorder='little', signed=False)
    self.machine_status.fan_5 = int.from_bytes(data[37:38], byteorder='little', signed=False)
    self.machine_status.endstop = int.from_bytes(data[38:39], byteorder='little', signed=False)

  def req_status(self):
    retval = b''
    retval += int.to_bytes(self.__CMD_STATUS, 1, byteorder='little', signed=True)
    retval += int.to_bytes(self.__SCMD_STAT_MACHINE, 1, byteorder='little', signed=True)
    retval += b'\x00'
    retval += int.to_bytes(self.connect_id, 1, byteorder='little', signed=True)
    return retval
  
  def req_heatup(self, target, temp):
    retval = b''
    retval += int.to_bytes(self.__CMD_CONTROL, 1, byteorder='little', signed=True)
    retval += int.to_bytes(self.__SCMD_CTRL_HEATER, 1, byteorder='little', signed=True)
    retval += b'\x00'
    retval += int.to_bytes(self.connect_id, 1, byteorder='little', signed=True)
    retval += int.to_bytes(target, 1, byteorder='little', signed=True)
    retval += int.to_bytes(temp, 2, byteorder='little', signed=True)
    return retval
