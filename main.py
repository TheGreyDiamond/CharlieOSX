#!/usr/bin/env pybricks-micropython

import time
import math
import OSTools as tools
from pybricks import ev3brick as charlie
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

#load data of the robot & filed
import config

# sensor initialisation
gyro = GyroSensor(config.gyroSensorPort)
rLight = ColorSensor(config.rightLightSensorPort) if (config.rightLightSensorPort != 0) else 0
lLight = ColorSensor(config.leftLightSensorPort) if (config.leftLightSensorPort != 0) else 0  
touch = TouchSensor(config.touchSensorPort) if (config.touchSensorPort != 0) else 0

# motor initialisation
if config.robotType == 'NORMAL':
    lMotor = Motor(config.leftMotorPort, Direction.CLOCKWISE if (not config.leftMotorInverted) else Direction.COUNTERCLOCKWISE)
    rMotor = Motor(config.rightMotorPort, Direction.CLOCKWISE if (not config.rightMotorInverted) else Direction.COUNTERCLOCKWISE)

    if config.useGearing:
        gearingPortMotor = Motor(config.gearingSelectMotorPort, Direction.CLOCKWISE if (not config.gearingSelectMotorPortInverted) else Direction.COUNTERCLOCKWISE)
        gearingTurnMotor = Motor(config.gearingTurnMotorPort, Direction.CLOCKWISE if (not config.gearingTurnMotorPortInverted) else Direction.COUNTERCLOCKWISE)

    else:
        aMotor1 = Motor(config.firstActionMotorPort, Direction.CLOCKWISE if (not config.firstActionMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.firstActionMotorPort != 0) else 0
        aMotor2 = Motor(config.secondActionMotorPort, Direction.CLOCKWISE if (not config.secondActionMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.secondActionMotorPort != 0) else 0

else:
    fRMotor = Motor(config.frontRightMotorPort, Direction.CLOCKWISE if (not config.frontRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.frontRightMotorPort != 0) else 0
    bRMotor = Motor(config.backRightMotorPort, Direction.CLOCKWISE if (not config.backRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.backRightMotorPort != 0) else 0
    fLMotor = Motor(config.frontLeftMotorPort, Direction.CLOCKWISE if (not config.frontLeftMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.frontLeftMotorPort != 0) else 0
    bLMotor = Motor(config.backRightMotorPort, Direction.CLOCKWISE if (not config.backRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.backRightMotorPort != 0) else 0



def driveNormal(speed):
    rMotor.speed(speed)
    lMotor.speed(speed)
def driveALL(speed):
    fRMotor.dc(speed)
    bRMotor.dc(speed)
    fLMotor.dc(speed)
    bLMotor.dc(speed)
drive = {'NORMAL': driveNormal(), 'ALLWHEEL': driveALL()}

gyro.reset_angle(0)

# TODO: gearing homing?

def execute(params, *args):
    """Lol das ist der Fahrinterpreter der das ganze fahren lässt..."""
    if (charlie.battery.voltage() <= 7500):
        print('Please Charge the battery', '  only ', charlie.battery.voltage())
        return "Battery too low"

    
    while params != [] and not any(charlie.buttons()):

        mode = params.pop(0)
        arg1 = params.pop(0)
        arg2 = params.pop(0)
        arg3 = params.pop(0)

        #turn
        if mode == 4:
            turn(arg1, arg2, arg3)
    
        #gearing
        elif mode == 5:
            gearing(arg1, arg2, arg3)
    
        #straight
        elif mode == 7:
            straight(arg1, arg2, arg3)
        
        #intervall
        elif mode == 9:
            intervall(arg1, arg2, arg3)
        
        #curve shaped
        elif mode == 11:
            curveShape(arg1, arg2, arg3)
        
        #to color 
        elif mode == 12:
            toColor(arg1, arg2, arg3)
        
        #until back wall
        elif mode == 15:
            toWall(arg1, arg2, arg3)
        
    lMotor.dc(0)
    rMotor.dc(0)
    gearingPortMotor.run_target(300, 0, Stop.HOLD, True)    #reset gearing
    time.sleep(0.3)



# finished
def turn(speed, deg, port, *args):
    """turns deg with speed. port indicates with wich motor(s)"""
    startValue = gyro.angle()

    #turn only with left motor
    if port == 2:
        #right motor off
        rMotor.dc(0)
        #turn the angle
        if deg > 0:
            while gyro.angle() - startValue < deg:
                lMotor.dc(speed)
                #slow down to not overshoot
                if not gyro.angle() - startValue < deg * 0.6:
                    speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                #cancel if button pressed
                if any(charlie.buttons()):
                    return
        else:
            while gyro.angle() - startValue > deg:
                lMotor.dc(-speed)
                #slow down to not overshoot
                if not gyro.angle() - startValue > deg * 0.6:
                    speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                #cancel if button pressed
                if any(charlie.buttons()):
                    return

    #turn only with right motor
    elif port == 3:
        #left motor off
        lMotor.dc(0)
        #turn the angle
        if deg > 0:
            while gyro.angle() - startValue < deg:
                rMotor.dc(-speed)
                #slow down to not overshoot
                if not gyro.angle() - startValue < deg * 0.6:
                    speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                #cancel if button pressed
                if any(charlie.buttons()):
                    return                 
        else:
            while gyro.angle() - startValue > deg:
                rMotor.dc(speed)
                #slow down to not overshoot
                if not gyro.angle() - startValue > deg * 0.6:
                    speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed
                
                #cancel if button pressed
                if any(charlie.buttons()):
                    return

    #turn with both motors
    elif port == 23:
        #turn the angle
        if deg > 0:
            while gyro.angle() - startValue < deg:
                rMotor.dc(-speed / 2)
                lMotor.dc(speed / 2)
                #slow down to not overshoot
                if not gyro.angle() - startValue < deg * 0.6:
                    speed = speed - tools.map(deg, 1, 360, 10, 0.01) if speed > 40 else speed

                #cancel if button pressed
                if any(charlie.buttons()):
                    return    
                
        else:
            while gyro.angle() - startValue > deg:
                rMotor.dc(speed / 2)
                lMotor.dc(-speed / 2)
                #slow down to not overshoot
                if not gyro.angle() - startValue > deg * 0.6:
                    speed = speed - tools.map(deg, 1, 360, 10, 0.01) if speed > 40 else speed
                
                #cancel if button pressed
                if any(charlie.buttons()):
                    return

# TODO: MECANUM Part
def straight(speed, cm, *args):
    """drives forward with speed in a straight line, corrected by the gyro"""
    correctionStrength = 2 # how strongly the robot will correct. 2 = default, 0 = nothing
    startValue = gyro.angle()
    rMotor.reset_angle(0)
    
    revs = cm / (config.wheelDiameter * math.pi) # convert the input (cm) to revs
    revs = revs / 2

    rSpeed = speed
    lSpeed = speed
    #drive
    if config.robotType == 'NORMAL':
        if revs > 0:
            while revs > rMotor.angle() / 360:
                #if not driving staright correct it
                if gyro.angle() - startValue > 0:
                    lSpeed = speed - abs(gyro.angle() - startValue) * correctionStrength
                    rSpeed = speed
                elif gyro.angle() - startValue < 0:
                    rSpeed = speed - abs(gyro.angle() - startValue) * correctionStrength
                    lSpeed = speed
                else:
                    lSpeed = speed
                    rSpeed = speed

                rMotor.dc(rSpeed)
                lMotor.dc(lSpeed)
                
                #cancel if button pressed
                if any(charlie.buttons()):
                        return
        else:
            while revs < rMotor.angle() / 360:
                
                #if not driving staright correct it
                if gyro.angle() - startValue < 0:
                    rSpeed = speed + abs(gyro.angle() - startValue) * correctionStrength
                    lSpeed = speed
                elif gyro.angle() - startValue > 0:
                    lSpeed = speed + abs(gyro.angle() - startValue) * correctionStrength
                    rSpeed = speed
                else:
                    lSpeed = speed
                    rSpeed = speed

                rMotor.dc(-rSpeed)
                lMotor.dc(-lSpeed)

                #cancel if button pressed
                if any(charlie.buttons()):
                        return
    
    elif config.robotType == 'ALLWHEEL':
        if revs > 0:
            while revs > rMotor.angle() / 360:
                #if not driving staright correct it
                if gyro.angle() - startValue > 0:
                    lSpeed = speed - abs(gyro.angle() - startValue) * correctionStrength
                    rSpeed = speed
                elif gyro.angle() - startValue < 0:
                    rSpeed = speed - abs(gyro.angle() - startValue) * correctionStrength
                    lSpeed = speed
                else:
                    lSpeed = speed
                    rSpeed = speed

                fRMotor.dc(rSpeed)
                bRMotor.dc(rSpeed)
                fLMotor.dc(lSpeed)
                bLMotor.dc(lSpeed)
                
                #cancel if button pressed
                if any(charlie.buttons()):
                        return
        else:
            while revs < rMotor.angle() / 360:
                
                #if not driving staright correct it
                if gyro.angle() - startValue < 0:
                    rSpeed = speed + abs(gyro.angle() - startValue) * correctionStrength
                    lSpeed = speed
                elif gyro.angle() - startValue > 0:
                    lSpeed = speed + abs(gyro.angle() - startValue) * correctionStrength
                    rSpeed = speed
                else:
                    lSpeed = speed
                    rSpeed = speed

                fRMotor.dc(rSpeed)
                bRMotor.dc(rSpeed)
                fLMotor.dc(lSpeed)
                bLMotor.dc(lSpeed)

                #cancel if button pressed
                if any(charlie.buttons()):
                        return

    elif config.robotType == 'MECANUM':
        print('mecanum Robot WIP')

# finished
def intervall(speed, revs, count, *args):
    """drives revs forward and backward with speed count times"""
    i = 0
    speed = speed * 1.7 * 6 # speed in deg/s to %
    # move count times for- and backwards
    while i < count:
        if config.robotType == 'NORMAL':
            ang = lMotor.angle()
            # drive backwards
            rMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
            lMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
            # return to cancel if any button is pressed
            while lMotor.angle() > revs * -360:
                if any(charlie.buttons()):
                    return

            #drive forwards
            lMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
            rMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
            # return to cancel if any button is pressed
            while rMotor.angle() <= ang:
                if any(charlie.buttons()):
                    return
        
        elif config.robotType == 'ALLWHEEL' or config.robotType == 'MECANUM':
            ang = lMotor.angle()
            # drive backwards
            fRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
            bRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
            fLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
            bLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
            # return to cancel if any button is pressed
            while lMotor.angle() > revs * -360:
                if any(charlie.buttons()):
                    return

            #drive forwards
            fRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
            bRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
            fLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
            bLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
            # return to cancel if any button is pressed
            while rMotor.angle() <= ang:
                if any(charlie.buttons()):
                    return

        i += 1

# TODO: add cancel
def curveShape(speed, revs1, deg, *args):
    """Drives in a curve deg over revs with speed"""
    speed = speed * 1.7 * 6 #speed to deg/s from %

    #gyro starting point
    startValue = gyro.angle()
    
    #claculate revs for the second wheel
    pathOutside = config.wheelDiameter * 2 * math.pi * revs1
    rad1 = pathOutside / (math.pi * (deg / 180))
    rad2 = rad1 - config.wheelDistance
    pathInside = rad2 * math.pi * (deg/180)
    revs2 = pathInside / (config.wheelDiameter * 2 * math.pi)

    #claculate the speed for the second wheel
    relation = revs1 / revs2
    speedSlow = speed / relation

    if deg > 0:
        #asign higher speed to outer wheel
        lSpeed = speed
        rSpeed = speedSlow
        print(rSpeed, lSpeed, revs1, revs2)
        rMotor.run_angle(rSpeed, revs2 * 360, Stop.COAST, False)
        lMotor.run_angle(lSpeed, revs1 * 360 + 5, Stop.COAST, False)
        #turn
        while gyro.angle() - startValue < deg and not any(charlie.buttons()):
            pass

    else:
        #asign higher speed to outer wheel
        rSpeed = speed
        lSpeed = speedSlow
        
        rMotor.run_angle(rSpeed, revs1 * 360 + 5, Stop.COAST, False)
        lMotor.run_angle(lSpeed, revs2 * 360, Stop.COAST, False)

        #turn
        while gyro.angle() + startValue > deg and not any(charlie.buttons()):
            pass
            print(lMotor.angle() / 360, gyro.angle() - startValue, relation)

# finished
def toColor(speed, color, side, *args):
    #sets color to a value that the colorSensor can work with
    if color == 0:
        color = Color.BLACK
    else:
        color = Color.WHITE

    #only drive till left colorSensor 
    if side == 2:
        #if drive to color black drive until back after white to not recognize colors on the field as lines
        if color == Color.BLACK:
            while lLight.color() != Color.WHITE and not any(charlie.buttons()):
                drive[config.robotType](speed)

        while lLight.color() != color and not any(charlie.buttons()):
            rMotor.dc(speed)
            lMotor.dc(speed)
        
    #only drive till right colorSensor 
    elif side == 3:
        #if drive to color black drive until back after white to not recognize colors on the field as lines
        if color == Color.BLACK:
            while rLight.color() != Color.WHITE and not any(charlie.buttons()):
                rMotor.dc(speed)
                lMotor.dc(speed)
            
        while rLight.color() != color and not any(charlie.buttons()):
            rMotor.dc(speed)
            lMotor.dc(speed)
        
    #drive untill both colorSensors
    elif side == 23:
        rSpeed = speed
        lSpeed = speed
        rWhite = False
        lWhite = False
        
        while (rLight.color() != color or lLight.color() != color) and not any(charlie.buttons()):
            #if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                if rLight.color() == Color.WHITE:
                    rWhite = True
                if lLight.color() == Color.WHITE:
                    lWhite = True

            rMotor.dc(rSpeed)
            lMotor.dc(lSpeed)
            #if right at color stop right Motor
            if rLight.color() == color and rWhite:
                rSpeed = 0
            #if left at color stop left Motor
            if lLight.color() == color and lWhite:
                lSpeed = 0

#finished
def toWall(speed, *args):
    """drives backwards with speed until it reaches a wall"""
    while not touch.pressed():
        rMotor.dc(abs(speed) * -1)
        lMotor.dc(abs(speed)
         * -1)

        if any(charlie.buttons()):
            break
    
    lMotor.dc(0)
    rMotor.dc(0)

# finished
def gearing(speed, revs, port, *args):
    """rotates the port for revs revulutions with a speed of speed"""
    speed = speed * 1.7 * 6 #speed to deg/s from %
    gearingPortMotor.run_target(300, port * 90, Stop.HOLD, True) #select gearing Port
    ang = gearingTurnMotor.angle()
    gearingTurnMotor.run_angle(speed, revs * 360, Stop.BRAKE, False) #start turning the port
    #cancel, if any brick button is pressed
    if revs > 0:
        while gearingTurnMotor.angle() < revs * 360 - ang:
            if any(charlie.buttons()):
                gearingTurnMotor.dc(0)
                return
    else:
        while gearingTurnMotor.angle() > revs * 360 + ang:
            if any(charlie.buttons()):
                gearingTurnMotor.dc(0)
                return

charlie.sound.beep()


#execute([15, 50, 0, 0]) #toWall
#execute([5, 50, 2, 1, 5, 100, -5, 3]) # gearing pos 1 & 3
#execute([9, 75, 1, 2]) #intervall
#execute([12, 50, 0, 23]) #toColor
#execute([4, 100, 90, 23]) #turn 
#execute([7, 75, 10, 0]) #straight
#execute([11, 75, 3, -90]) #curve shaped

#execute([11, 75, 8, -23]) #7, 100, 10, 0, 4, 75, 50, 2, ])
'''execute([4, 55, -20, 3, 7, 100, 155, 0, # to elevator
        4, 50, 30, 2, 4, 50, 50, 23, 7, 50, 5, 0, 4, 50, 10, 2, 7, 40, 5, 0, 4, 20, 10, 2, # do the house
        7, 50, 5, 0, 11, 50, 1, 25, 7, 50, 5, 0, 4, 50, -45, 3, #do the schaukel
        7, 100, -20, 0, 4, 50, -50, 23, 15, 100, 0, 0]) # back home'''


#while True:
#    print(gyro.angle())

