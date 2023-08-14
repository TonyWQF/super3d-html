import socket
from threading import Thread
import time
from V30Commands import Commands, MachineStatus

class MachineControler:
  def __init__(self):
    self.__recv_buffer = b''
    self.__protocal = ProtocalV30()
    self.__transmiter = TcpTransmiter()
    self.__commands = Commands()

    self.__heart_thread_handle = Thread(target=self.__auto_request_status, daemon=True)
    self.__heart_thread_handle.start()
  
    self.__data_thread_handle = Thread(target=self.__data_process, daemon=True)
    self.__data_thread_handle.start()
    self.__wait_queue = []
    
    self.status = MachineStatus()
    
    print('machine inited')
  
  def __data_process(self):
    while(True):
      new_data = self.__transmiter.fetch_data()
      self.__recv_buffer = self.__recv_buffer + new_data
      parse_data = self.__protocal.parse(self.__recv_buffer)
      if(parse_data is not None):
        self.__recv_buffer = parse_data[0]
        result = self.__commands.analize(parse_data[1])
      self.status = self.__commands.machine_status
      time.sleep(0.01)

  def __auto_request_status(self):
    while(True):
      src_datas = self.__commands.req_status()
      datas_to_send = self.__protocal.setup_pack(src_datas)
      self.__transmiter.send_pack(datas_to_send)
      time.sleep(1)

  def get_status(self):
    return self.status

  def heatup(self,Target, Temp):
    src_datas = self.__commands.req_heatup(int(Target), int(Temp))
    datas_to_send = self.__protocal.setup_pack(src_datas)
    self.__transmiter.send_pack(datas_to_send)

  def move_axis(self,Axis, Distance):
    pass

  def home_axis(self,Axis):
    pass

  def start_print(self,FileName):
    pass

  def stop_print(self):
    pass

  def pause_print(self):
    pass

  def resume_print(self):
    pass

class ProtocalV30:
  def __init__(self):
    self.name="V40"
    self.version = '40'
  
  def setup_pack(self, source):
    packed_data = b'\xa5\x5a\x40'
    packed_data += int.to_bytes(len(source), 4, byteorder='little', signed=False)
    len_check = packed_data[3] ^ packed_data[4] ^ packed_data[5] ^ packed_data[6]
    packed_data += int.to_bytes(len_check, 1, byteorder='little',signed=False)
    checksum = 0
    for i in source:
      checksum = checksum + i
    checksum = checksum & 0xffff
    packed_data += int.to_bytes(checksum, 2, byteorder='little', signed=False)
    packed_data += source
    return packed_data

  def parse(self, source):
    while(len(source) >= 12):
      if(source[0] != 0xa5): 
        source = source[1:]
        continue
      if(source[1] != 0x5a): 
        source = source[2:]
        continue

      # Version

      #Pack len check
      if(source[3] ^ source[4] ^ source[5] ^ source[6] != source[7]):
        source = source[2:]
        print('Len Verify fail')
        continue

      pack_len = (source[3]) | (source[4] << 8) | (source[5] << 16) | (source[6] << 24)

      if(pack_len + 10) > len(source): 
        return None

      # Verify datas
      src_checksum = source[8] | (source[9] << 8)
      pack_data = source[10:10 + pack_len]
      cal_check = 0
      for i in pack_data:
        cal_check = cal_check + i
      cal_check = cal_check & 0xffff

      if(src_checksum != cal_check):
        source = source[2:]
        print('Check fail:' + str(src_checksum) + str(cal_check))
        continue

      source = source[pack_len + 10:]
      return [source, pack_data]
    return None


class TcpTransmiter:
  def __init__(self):
    self.pack_queue = []
    self.__recv_buffer = b''
    self.__recv_thread_handle = Thread(target=self.__receive_thread, daemon=True)
    self.__recv_thread_handle.start()
    self.__connect_retry = False

  def fetch_data(self):
    retval = b''
    if(len(self.__recv_buffer) > 0):
      retval = self.__recv_buffer
      self.__recv_buffer = b''
    return retval

  def peek_length(self):
    return len(self.__recv_buffer)

  def __receive_thread(self):
    while(True):
      try:
        datas = self.tcp_client.recv(10240)
        self.__recv_buffer = self.__recv_buffer + datas
        if(len(self.__recv_buffer) > 40960):
          self.__recv_buffer = b''
      except:
        time.sleep(1)

  def connect_check(self):
    print("Connect after 1s")
    time.sleep(1)
    while(True):
      try:
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect(("192.168.1.7", 7777))
        if(len(self.pack_queue) > 0):
          self.tcp_client.send(self.pack_queue[0])
          self.pack_queue = self.pack_queue[1:]
        print('connect ok')
        break
      except:
        print('connect fail')
        time.sleep(1)
        continue
      self.__connect_retry = False

  def send_pack(self, data):
    try:
      self.tcp_client.send(data)
      return True
    except:
      if(self.__connect_retry == False):
        self.__connect_retry = True
        self.pack_queue.append(data)
        self.connection_thread = Thread(target=self.connect_check, daemon=True)
        self.connection_thread.start()
      return False
