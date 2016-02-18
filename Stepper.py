import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Stepper:
    # adjust if different
    def __init__(self, pin1=17, pin2=18, pin3=22, pin4=23):
        
        self.StepState = 0; # 8 per full step
        self.Position = 0;  # 400 per revolution
        
        
        self.StepCount = 8
        self.Seq = range(0, self.StepCount)
        self.Seq[0] = [0,1,0,0]
        self.Seq[1] = [0,1,0,1]
        self.Seq[2] = [0,0,0,1]
        self.Seq[3] = [1,0,0,1]
        self.Seq[4] = [1,0,0,0]
        self.Seq[5] = [1,0,1,0]
        self.Seq[6] = [0,0,1,0]
        self.Seq[7] = [0,1,1,0]
        
        self.coil_A_1_pin = pin1
        self.coil_A_2_pin = pin2
        self.coil_B_1_pin = pin3
        self.coil_B_2_pin = pin4
        
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        #self.setStep(self.Seq[self.StepState][0], self.Seq[self.StepState][1], self.Seq[self.StepState][2], self.Seq[self.StepState][3])
                
    def setStep(self, w1, w2, w3, w4):    
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def forward(self, delay, steps):
        for i in range(steps):
            self.StepState = self.StepState + 1
            self.Position = self.Position + 1
            if self.StepState == self.StepCount:
                self.StepState = 0
            self.setStep(self.Seq[self.StepState][0], self.Seq[self.StepState][1], self.Seq[self.StepState][2], self.Seq[self.StepState][3])
            time.sleep(delay)

    def backwards(self, delay, steps):
        for i in range(steps):
            self.StepState = self.StepState - 1
            self.Position = self.Position - 1
            if self.StepState < 0:
                self.StepState = self.StepCount - 1
            self.setStep(self.Seq[self.StepState][0], self.Seq[self.StepState][1], self.Seq[self.StepState][2], self.Seq[self.StepState][3])
            time.sleep(delay)
            
    def setPosition(self, pos):
        if pos < self.Position:
            self.backwards(.002, self.Position - pos)
        elif pos > self.Position:
            self.forward(.002, pos - self.Position)
        print "Current Position: ", self.Position


if __name__ == '__main__':
    motor = Stepper();
    while True:
        steps = raw_input("How many steps forward? ")
        motor.setPosition(int(steps));

