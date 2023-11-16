from devices.ThorlabsBST import ThorlabsBST

class SeekPixel:
    # Constants
    MOTOR_LIMITS = {'left': 0, 'right': 130}
    
    # Class-level variables
    BST_SERIAL = None
    BENCHTOP_MOTOR = None
    SEEK_OPERATION = None

    @staticmethod
    def connect():
        if SeekPixel.BST_SERIAL is None:
            raise ValueError("No BST serial set")
        
        SeekPixel.BENCHTOP_MOTOR = ThorlabsBST(SeekPixel.BST_SERIAL)

    @staticmethod
    def seek(pixel: int):
        if not SeekPixel.BENCHTOP_MOTOR or not SeekPixel.BENCHTOP_MOTOR.is_connected:
            print("Thorlab Rotation Stage (BST) not connected")
            return
        
        motor_deg = SeekPixel.get_motor_pos(pixel)

        if not SeekPixel.within_limits(motor_deg):
            print(f"Requested degree ({motor_deg}) is out of motor limits")
            return
        
        try:
            SeekPixel.BENCHTOP_MOTOR.move_to(motor_deg)
        except Exception as e:
            print(f"Exception caught while attempting to move benchtop motor: {e}")

    @staticmethod
    def within_limits(degree):
        '''
        Ensure the motor does not over-rotate, which may cause damage to the testbed.
        '''
        lim = SeekPixel.MOTOR_LIMITS
        if isinstance(degree, float):
            return lim['left'] < degree < lim['right']
        else:
            print("Degree is not a float")

    @staticmethod
    def get_motor_pos(pixel: int) -> int:
        if SeekPixel.SEEK_OPERATION:
            return SeekPixel.SEEK_OPERATION(pixel)
        else:
            return lambda x: x / -1

    @staticmethod
    def set_seek_operation(operation):
        SeekPixel.SEEK_OPERATION = operation

def main():
    SeekPixel.set_seek_operation(operation=lambda x: (float(x) - 154.3) / -1.64)
    SeekPixel.connect()
    SeekPixel.seek(1)

if __name__ == "__main__":
    main()
