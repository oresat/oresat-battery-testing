import u6

class LabJack:
    def __init__(self):
        self.d = u6.U6()

    def analogRead(self, pin, resolution=1, gain=0, settling=0, diff=False):
        if not (0 <= pin <= 11):
            raise ValueError("Invalid Pin number!")
        if not (1 <= resolution <= 8):
            raise ValueError("Invalid Pin number!")
        if not (0 <= gain <= 3 or gain == 15):
            raise ValueError("Invalid Pin number!")
        if not (0 <= settling <= 9):
            raise ValueError("Invalid settling!")
        return self.d.getAIN(pin, resolution, gain, settling, diff)

    def pinMode(self, pin, dir=None):
        if not (0 <= pin <= 19):
            raise ValueError("Invalid Pin number!")
        if dir == 0 or dir == 1:
            return self.d.getFeedback(u6.BitDirWrite(pin, dir))
        elif dir == None:
            return self.d.getFeedback(u6.BitDirRead())
        else:
            raise ValueError("Invalid dir!")
        
    def digitalWrite(self, pin, state):
        if not (0 <= pin <= 19):
            raise ValueError("Invalid Pin number!")
        if not (0 <= state <= 1 or state == True or state == False):
            raise ValueError("Invalid state!")
        return self.d.getFeedback(u6.BitStateWrite(pin, state))

    def digitalRead(self, pin):
        if not (0 <= pin <= 19):
            raise ValueError("Invalid Pin number!")
        return self.d.getFeedback(u6.BitStateRead(pin))