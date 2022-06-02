import rcu
import math
#-Robot1 port:
m1= 3
m2= 4 
m3= 2
at= 7

rcu.SetBluetoothData(1) #Initialize bluetooth
rcu.SetSysTime() #set sys time to 0
rcu.SetMotorCode(3) # reset encoder M3 - left motor
rcu.SetMotorCode(4) # reset encoder M4 - right motor
rcu.SetMotorCode(2) # reset encoder M2 - back motor
rcu.SetAHRS(7,2) # reset attitude sensor
rcu.SetAHRS(7,1) # attitude sensor is correcting
rcu.SetAICamData(4,0) # set Ai camera mode detect ball 
#define gobal variables
counter = 0
a= 3150
check_intensity = []
intensity_50 = []
ball_position= []
temp= []
degree = []
intensity= 0
distance = 0
direction = 0
posiball = 0
heading = 0

minUltraRange = 50
maxUltraRange = 80
goalRange = 30

#camera component
cameraMidPointX = 125 #will be modified
cameraMidPointY = 150 #will be modified

farRangeX = 50
farRangeY = 20

farRangeSpeed = 120
nearRangeSpeed = 100

xPoint = 0
yPoint = 0

xMove = 0
yMove = 0

outRange = False


    

#-------------------------------------------------------
#funtion
def angle_get():
    angle= rcu.GetAHRS(7,3,0)- heading
    rcu.SetDisplayVar(1,angle,0xFFE0,0x0000)
def move(vx, vy, Omega):
    V1= (vy + Omega*0.2)
    V2= -vy * math.cos(math.pi/3) + vx*math.sin(math.pi/3) + Omega*0.2
    V3= -vy * math.cos(-math.pi/3) + vx*math.sin(-math.pi/3) + Omega*0.2
    if (V3 <= -100):
        V3 = -100
    elif (V3 >= 100):
        V3 = 100
    if (V2 <= -100):
        V2 = -100
    elif (V2 >= 100):
        V2 = 100
    if (V1 <= -100):
        V1 = -100
    elif (V1 >= 100):
        V1 = 100
    #rcu.SetMotorPower(V3,0,V2,V1)
    rcu.SetMotor(3,V3/1.5)
    rcu.SetMotor(4,-V2/1.5)
    rcu.SetMotor(2,-V1)  
def stopMotor():
    rcu.SetMotor(3,0)
    rcu.SetMotor(4,0)
    rcu.SetMotor(2,0)
#--------------------------------------------
stopMotor()

rcu.SetSysTime()
blData = 1
currentTime = rcu.GetSysTime()
lastTime = rcu.GetSysTime()
while True:
    angle= rcu.GetAHRS(7,3,0)- heading
    rcu.SetDisplayVar(1,heading,0xFFE0,0x0000)
    rcu.SetDisplayVar(2,angle,0xFFE0,0x0000)
    rcu.SetDisplayVar(4,rcu.GetLightSensor(4),0xFFE0,0x0000)
    xPoint = rcu.GetAICamData(1)
    yPoint = rcu.GetAICamData(2)
    if (xPoint < cameraMidPointX - 30 and  xPoint > 0):
        yMove = -1
    elif (xPoint > cameraMidPointX + 30 and xPoint > 0):
        yMove = 1
    else:
        yMove = 0
    xMove = 1
    outRange = False
    if (xPoint <= 0) or (yPoint <= 0) :
        outRange = True
        xMove = -1
        yMove = 0
    if (outRange) and ((rcu.GetLightSensor(4) > 200) or (rcu.GetLightSensor(1) > 200) ):
        xMove *= -120
    else:
        if (yPoint > cameraMidPointY):
            xMove *= farRangeSpeed
        elif (rcu.GetLightSensor(4) > 200) or (rcu.GetLightSensor(1) > 200):
            xMove *= -farRangeSpeed
        else:
            xMove *= nearRangeSpeed

        if (xPoint > cameraMidPointX + farRangeX):
            yMove *= farRangeSpeed
        elif (xPoint <= cameraMidPointX - farRangeX):
            yMove *= nearRangeSpeed



    if (rcu.GetLightSensor(4) > 100):
        rcu.SetDisplayString(3,"Attacing",0xFFE0,0x0000)
        rcu.SetBluetoothData(0)
    else:
        rcu.SetDisplayString(3,"Finding Ball",0xFFE0,0x0000)
        rcu.SetBluetoothData(1)

    
    if (currentTime - lastTime > 3000):
        blData = rcu.GetBluetoothData()
        lastTime = currentTime

    currentTime = rcu.GetSysTime()
    if (blData == 0):
        rcu.SetDisplayString(3,"Denfense Ball",0xFFE0,0x0000)
        if (rcu.GetUltrasound(6) < minUltraRange):
            yMove = 120
        elif (rcu.GetUltrasound(6) > maxUltraRange):
            yMove = -120
        else:
            yMove = 0

        if (rcu.GetUltrasound(5) <= 30):
            xMove = 0
        else:
            xMove = -120

    rcu.SetDisplayString(5,"Light 4",0xFFE0,0x0000)
    rcu.SetDisplayVar(5, rcu.GetLightSensor(4),0xFFE0,0x0000)
    rcu.SetDisplayString(6,"Light 1",0xFFE0,0x0000)
    rcu.SetDisplayVar(6, rcu.GetLightSensor(1),0xFFE0,0x0000)
    move(xMove, yMove, angle)


while True:
    rcu.SetDisplayString(1,"lighting",0xFFE0,0x0000)
    rcu.SetDisplayString(2,str(rcu.GetLightSensor(4)),0xFFE0,0x0000)
    if (rcu.GetBluetoothData() == 0):
        rcu.SetDisplayString(3,"Defending",0xFFE0,0x0000)
        continue
    
    if (rcu.GetLightSensor(4) > 1000):
        rcu.SetDisplayString(3,"Attacing",0xFFE0,0x0000)
        rcu.SetBluetoothData(0)
    else:
        rcu.SetDisplayString(3,"Finding Ball",0xFFE0,0x0000)
        rcu.SetBluetoothData(1)
