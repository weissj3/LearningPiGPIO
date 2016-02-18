import RPi.GPIO as GPIO
import time
import math as ma

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PWM_Freq = 800


class MicroStepper:
    # adjust if different
    def __init__(self, SC=10, pin1=17, pin2=18, pin3=22, pin4=23, pwmAC=24, pwmBD=25):
        
        self.StepState = 0; # 8 per full step
        self.Position = 0;  # 400 per revolution
        self.TableSize = SC * 4
        
        self.StepCount = SC
        self.Coils_Table = range(0, self.TableSize)
        self.PWM_Table = range(0, self.TableSize)
        
        self.coil_A_1_pin = pin1
        self.coil_A_2_pin = pin2
        self.coil_B_1_pin = pin3
        self.coil_B_2_pin = pin4
        self.PWM_AC_pin = pwmAC
        self.PWM_BD_pin = pwmBD
        
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        GPIO.setup(self.PWM_AC_pin, GPIO.OUT)
        GPIO.setup(self.PWM_BD_pin, GPIO.OUT)
        self.PWM_AC = GPIO.PWM(self.PWM_AC_pin, PWM_Freq)
        self.PWM_BD = GPIO.PWM(self.PWM_BD_pin, PWM_Freq)
        self.setStep(0,0,0,0) #Zero Coils
        self.PWM_AC.start(0)
        self.PWM_BD.start(0)
        self.buildStepTable()
        
    def buildStepTable(self):
        for i in range(self.TableSize):
            self. Coils_Table = [0,0,0,0]
            self.PWM_Table = [ma.floor(ma.sqrt(ma.fabs(ma.sin( ma.pi * float(i) / (self.TableSize / 2.0))))), ma.floor(ma.sqrt(ma.fabs(ma.cos( ma.pi * float(i) / (self.TableSize / 2.0)))))]
            
        for i in range(self.TableSize / 2):
            self.Coils_Table[i][0] = 1
            self.Coils_Table[i + self.TableSize / 2][1] = 1
        for i in range(self.TableSize / 4):
            self.Coils_Table[i][2] = 1
            self.Coils_Table[i + self.TableSize / 2][2] = 1
            self.Coils_Table[i + 3 * self.TableSize / 4][3] = 1
            self.Coils_Table[i + self.TableSize / 4][3] = 1
        
    def setDuty(self, AC, BD):
        self.PWM_AC.ChangeDutyCycle(AC)
        self.PWM_BD.ChangeDutyCycle(BD)
        
        
    def stopStepper(self):
        self.setStep(0,0,0,0) #Zero Coils
        self.setDuty(0,0)
                
    def setStep(self, w1, w2, w3, w4):    
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)
        
    def setToStepState(self):
            self.setStep(self.Coils_Table[self.StepState][0], self.Coils_Table[self.StepState][1], self.Coils_Table[self.StepState][2], self.Coils_Table[self.StepState][3])
            self.setDuty(self.PWM_Table[self.StepState][0], self.PWM_Table[self.StepState][1])

    def forward(self, delay, steps):
        for i in range(steps):
            self.StepState = self.StepState + 1
            self.Position = self.Position + 1
            if self.StepState == self.StepCount:
                self.StepState = 0
            self.setToStepState()
            time.sleep(delay)

    def backwards(self, delay, steps):
        for i in range(steps):
            self.StepState = self.StepState - 1
            self.Position = self.Position - 1
            if self.StepState < 0:
                self.StepState = self.StepCount - 1
            self.setToStepState()
            time.sleep(delay)
            
    def setPosition(self, pos):
        if pos < self.Position:
            self.backwards(.01, self.Position - pos)
        elif pos > self.Position:
            self.forward(.01, pos - self.Position)
        print "Current Position: ", self.Position


if __name__ == '__main__':
    motor = MicroStepper();
    while True:
        steps = raw_input("How many steps forward? ")
        if not int(steps): break
        motor.setPosition(int(steps));
        
    GPIO.cleanup()
        

