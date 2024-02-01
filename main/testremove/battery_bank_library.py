import time
from operator import truediv

from labjack_library import LabJack


#changed liblabjack.Labjack to just LabJack in line below
class BattLabJack(LabJack):
    def __init__(self, senseControlPins, chargeControlPins, relayWait=0.1):
        super().__init__()
        self.senseControlPins = senseControlPins
        self.chargeControlPins = chargeControlPins
        self.protectedGroups = (self.senseControlPins, self.chargeControlPins)
        for group in self.protectedGroups:
            for pin in group:
                self.pinMode(pin, True)
                self.digitalWrite(pin, False)
        self.relayWait = relayWait

    def safeDigitalWrite(self, pin, state=False, delay=None):
        if delay == None:
            delay = self.relayWait
        for set in self.protectedGroups:
            if pin in set:
                for pin in set:
                    self.digitalWrite(pin, False)
                break
        time.sleep(delay)
        self.digitalWrite(pin, state)

    def waitForRelays(self):
        time.sleep(self.relayWait)


class BatteryBank:
    def __init__(self, battlabjack: BattLabJack, bankID: int, cellCount=4):
        self.lj = battlabjack
        self.bankID = bankID
        self.cellCount = cellCount
        self.lastMeasurement = None
        self.cellVolts = []
        self.cellTemps = []
        for i in range(self.cellCount):
            self.cellVolts.append(0)
            self.cellTemps.append(0)
        self.setMySensePin(True) #line added

    def __del__(self):
        self.setMySensePin(False)

    def setMySensePin(self, val=False):
        self.lj.safeDigitalWrite(self.lj.senseControlPins[self.bankID], val)

    def setMyChargePin(self, val=False):
        self.lj.safeDigitalWrite(self.lj.chargeControlPins[self.bankID], val)

    def measure(self, avgCount=4, delay=0.05):
        #self.setMySensePin(True)
        for cellNum in range(self.cellCount):
            av = 0
            at = 0
            for avi in range(avgCount):
                time.sleep(delay)
                av += self.lj.analogRead(cellNum * 2, settling=1, diff=True)
                atv = self.lj.analogRead(cellNum + 8)
                at += atv
            self.cellVolts[cellNum] = av / avgCount
            self.cellTemps[cellNum] = at / avgCount
            #set my sense pin to False
