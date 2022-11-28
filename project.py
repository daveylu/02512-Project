import math
from numpy import random
from matplotlib import pyplot as plt

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
    part2 = k*(dw5*math.sqrt(y1*i1) + dw7*math.sqrt(y2*i2) + dw9*math.sqrt(y3*i3))
    return part1 + part2
    
def dD(i3, u, k, dt, dw10):
    return (u*i3*dt) + k*dw10*math.sqrt(u*i3)
    
def main(days):
    # Initialize conditions and parametres.
    N = 1000
    i1 = 0
    i2 = 0
    i3 = 0
    S = N
    E = 1
    D = 0
    R = 0
    # fixed paramter set (for now), maybe allow adjustments later
    a = 0.2
    b1 = 0.5
    b2 = 0.1
    b3 = 0.1
    y1 = 0.133  
    p1 = 0.033
    p2 = 0.042
    y2 = 0.125
    u = 0.050
    y3 = 0.075
    dt = 0.5
    k = 0

    # The parametres can be changed based upon the severity of PHSM (Public Health and Safety Measures)

    vals_S = [S]
    vals_E = [E]
    vals_i1 = [i1]
    vals_i2 = [i2]
    vals_i3 = [i3]
    vals_D = [D]
    vals_R = [R]
    t = [0]
    runs = int(days / dt)
    for i in range(1, runs + 1):
        
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
        change_S= dS(b1, b2, b3, i1, i2, i3, S, k, dt, dw1, dw2, dw3)
        change_E = dE(b1, b2, b3, i1, i2, i3, a, E, S, k, dt, dw1, dw2, dw3)
        change_R = dR(y1, y2, y3, i1, i2, i3, k, dt, dw5, dw7, dw9)
        change_i1 = dI1(a, E, y1, p1, dt, i1, k, dw4, dw5, dw6)
        change_i2 = dI2(p1, y2, p2, dt, i1, i2, k, dw6, dw7, dw8)
        change_i3 = dI3(y2, p2, i2, y3, u, dt, i3, k, dw8, dw9, dw10)
        change_D = dD(i3, u, k, dt, dw10)

        if(S + change_S < 0):
            E += S
            S = 0
        else:
            S += change_S

        if(E + change_E < 0):
            i1 += E
            E = 0
        else:
            E += change_E

        if(i1 + change_i1 < 0):
            i2 += i1 * (p1 / (y1 + p1))
            R += i1 * (y1 / (y1 + p1))
            i1 = 0
        else:
            i1 += change_i1

        if(i2 + change_i2 < 0):
            i3 += i2 * (p2 / (y2 + p2))
            R += i2 * (y2 / (y2 + p2))
            i2 = 0
        else:
            i2 += change_i2

        i3 += change_i3
        if(i3 < 0): i3 = 0
        R += change_R
        if(R < 0): R = 0
        D += change_D
        if(D < 0): D = 0

        vals_S.append(S)
        vals_E.append(E)
        vals_i1.append(i1)
        vals_i2.append(i2)
        vals_i3.append(i3)
        vals_D.append(D)
        vals_R.append(R)
        t.append(i)

    plt.plot(t, vals_S, label = "Susceptible")
    plt.plot(t, vals_E, label = "Exposed")
    plt.plot(t, vals_i1, label = "Mild Infection")
    plt.plot(t, vals_i2, label = "Severe Infection")
    plt.plot(t, vals_i3, label = "Critical Infection")
    plt.plot(t, vals_D, label = "Dead")
    plt.plot(t, vals_R, label = "Recovered")
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title(f"Plot of COVID spread: {N} total population")
    plt.legend()
    plt.show()
    

main(300)
