import rcu
import math
#-Robot1 port:
#m1= 1
#m2= 3
#m3= 4
#at= 1
#-Robot2 port:
m1= 3
m2= 4 
m3= 2
at= 7

rcu.SetSysTime() #set sys time to 0
rcu.SetMotorCode(3) # reset encoder M3 - left motor
rcu.SetMotorCode(4) # reset encoder M4 - right motor
rcu.SetMotorCode(2) # reset encoder M2 - back motor
rcu.SetAHRS(7,2) # reset attitude sensor
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
#-------------------------------------------------------
#funtion
def angle_get():
    angle= rcu.GetAHRS(7,3,0)- heading
    rcu.SetDisplayVar(1,angle,0xFFE0,0x0000)
    ##print('angle: ', angle)
def Cam_get():
    xBall = rcu.GetAICamData(1)
    yBall =rcu.GetAICamData(2)
def move(vx, vy, Omega):
    V1= (vy+ Omega*1)/2.7
    V2= -vy * math.cos(math.pi/3)+vx*math.sin(math.pi/3) + Omega*1
    V3= -vy * math.cos(-math.pi/3)+vx*math.sin(-math.pi/3)+Omega*1
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
    rcu.SetMotor(3,-V3)
    rcu.SetMotor(4,V2)
    rcu.SetMotor(2,V1)  
def stopMotor():
    rcu.SetMotor(3,0)
    rcu.SetMotor(4,0)
    rcu.SetMotor(2,0)
#--------------------------------------------
stopMotor()
rcu.SetAHRS(7,1)    
while True:
    #Cam_get()
    #print('direction', direction)
    angle= rcu.GetAHRS(7,3,0)+0
    rcu.SetDisplayVar(1,rcu.GetAHRS(7,3,0),0xFFE0,0x0000)
    rcu.SetDisplayVar(2,angle,0xFFE0,0x0000)
    move(0, -150, angle)



# import rcu

# def task1():
#   rcu.SetMotorCode(1)
#   rcu.SetAHRS(1,1)
#   while True:
#     rcu.SetDisplayString(1,"đọc encoder",0xFFE0,0x0000)
#     rcu.SetDisplayVar(1,rcu.GetMotorCode(1),0xFFE0,0x0000)
#     rcu.SetMotorPower(100,100,100,100)
#     rcu.SetDisplayString(1,"đọc gyro",0xFFE0,0x0000)
#     rcu.SetDisplayVar(1,rcu.GetAHRS(1,3,0),0xFFE0,0x0000)
#     rcu.SetDisplayString(1,"đọc tọa độ banh",0xFFE0,0x0000)
#     rcu.SetDisplayVar(1,"".join((rcu.GetAICamData(1),rcu.GetAICamData(2))),0xFFE0,0x0000)
#     rcu.SetDisplayString(1,"đọc color",0xFFE0,0x0000)
#     rcu.SetDisplayVar(1,rcu.GetColorSensor(1,4),0xFFE0,0x0000)

# task1()