import socket
import struct
import cv2
import numpy as np

MAX_DGRAM = 2**16
def dump_buffer(s):
  while True:
    seg, addr = s.recvfrom(MAX_DGRAM)
    print(seg[0])
    # 49 = ASCII '1'
    # Räknar ner till sissta segmentet (1)
    seg_n = struct.unpack('B', seg[0:1])[0]
    if seg_n == 1 or seg_n == 49:
      print('finish emptying buffer')
      break

def main(): 
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 1337))
    dat = b''
    dump_buffer(s)
    
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print('recv')
        if struct.unpack('B', seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            cv2.imshow("frame", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b'' # cap.release()

    cv2.destroyAllWindows()
    s.close()


main()
