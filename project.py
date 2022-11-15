import math
import sys
from numpy import random

def dS(b1, b2, b3, i1, i2, i3, S, k, dt, dw1, dw2, dw3):
    
    part1 = -(b1*i1 + b2*i2 + b3*i3)*S*dt
    part2 = -k*(dw1*math.sqrt(b1*i1*S) + dw2*math.sqrt(b2*i2*S) + dw3*math.sqrt(b3*i3*S))
    return part1 + part2

def dE(b1, b2, b3, i1, i2, i3, a, E, S, k, dt, dw1, dw2, dw3):
    part1 = (b1*i1 + b2*i2 + b3*i3)*S*dt -a*E*dt
    part2 = k*(dw1*math.sqrt(b1*i1*S) + dw2*math.sqrt(b2*i2*S) + dw3*math.sqrt(b3*i3*S))
    return part1 + part2
    
def dI1(a, E, y1, p1, dt, i1, k, dw4, dw5, dw6):
    part1 = a*E*dt - (y1+p1)*i1*dt
    part2 = k*(dw4*math.sqrt(a*E) - dw5*math.sqrt(y1*i1) - dw6*math.sqrt(p1*i1))
    return part1 + part2

def dI2(p1, y2, p2, dt, i1, i2, k, dw6, dw7, dw8):
    part1 = p1*i1 - (y2+p2)*i2*dt
    part2 = k*(dw6*math.sqrt(p1*i1) - dw7*math.sqrt(y2*i2) - dw8*math.sqrt(p2*i2))
    return part1 + part2

def dI3(y2, p2, i2, y3, u, dt, i3, k, dw8, dw9, dw10):
    part1 = p2*i2*dt - (y3+u)*i3*dt
    part2 = k*(dw8*math.sqrt(p2*i2) - dw9*math.sqrt(y3*i3) - dw10*math.sqrt(u*i3))
    return part1 + part2

def dR(y1, y2, y3, i1, i2, i3, k, dt, dw5, dw7, dw9):
    part1 = (y1*i1 + y2*i2 + y3*i3)*dt
    part2 = k(dw5*math.sqrt(y1*i1) + dw7*math.sqrt(y2*i2) + dw9*math.sqrt(y3*i3))
    return part1 + part2
    
def dD(i3, u, k, dt, dw10):
    return (u*i3*dt) + k*dw10*math.sqrt(u*i3)
    
def main(paramList):
    # Initialize the parametres for our model and starting conditions
    # The parametres can be changed based upon the severity of PHSM (Public Health and Safety Measures)
    # NOTE: The loop condition is just temporary; will update later.
    while(True):
        dw1 = random.normal(0, 1)
        dw2 = random.normal(0, 1)
        dw3 = random.normal(0, 1)
        dw4 = random.normal(0, 1)
        dw5 = random.normal(0, 1)
        dw6 = random.normal(0, 1)
        dw7 = random.normal(0, 1)
        dw8 = random.normal(0, 1)
        dw9 = random.normal(0, 1)
        dw10 = random.normal(0, 1)

        # Run our model on each country. The countries are U.S., China, and E.U.
        # Call each differential function (e.g. dS) on the paramList given for the country. For instance, we pass in the parametres for U.S. into main(), and from there, we just call dS, dE, etc. on the respective parametres (e.g. get dS(b1, b2, b3, i1, i2, i3, S, k, dt, dw1, dw2, dw3) as the dS for U.S., China, E.U.).


if __name__ == '__main__':
    _,paramList = sys.argv
    main(paramList)
