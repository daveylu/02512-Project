import math
from numpy import random
from matplotlib import pyplot as plt

def dS(b1, b2, b3, i1, i2, i3, S, k, dt, dw1, dw2, dw3,N):
    
    part1 = -(b1*i1 + b2*i2 + b3*i3)*S*dt/(N)
    part2 = -k*(dw1*math.sqrt(b1*i1*S) + dw2*math.sqrt(b2*i2*S) + dw3*math.sqrt(b3*i3*S))
    return part1 + part2

def dE(b1, b2, b3, i1, i2, i3, a, E, S, k, dt, dw1, dw2, dw3, dw4, S_floored,N):
    if(S_floored == True): S_part = S
    else:
        S_part = (b1*i1 + b2*i2 + b3*i3)*S*dt/N + k*(dw1*math.sqrt(b1*i1*S) + dw2*math.sqrt(b2*i2*S) + dw3*math.sqrt(b3*i3*S))
    E_part = -a*E*dt - (dw4*math.sqrt(a*E))
    return S_part + E_part

def dI1(a, E, y1, p1, dt, i1, k, dw4, dw5, dw6, E_floored):
    if(E_floored == True):
        E_part = E
    else:
        E_part = a*E*dt + k*dw4*math.sqrt(a*E)
    i1_part = -(y1+p1)*i1*dt - k*(dw5*math.sqrt(y1*i1) + dw6*math.sqrt(p1*i1))
    return E_part + i1_part

def dI2(p1, y1, y2, p2, dt, i1, i2, k, dw6, dw7, dw8, i1_floored):
    if(i1_floored == True):
        i1_part = i1 * (p1 / (y1 + p1))
    else:
        i1_part = p1*i1 + k*dw6*math.sqrt(p1*i1)
    i2_part = -(y2+p2)*i2*dt - k*(-dw7*math.sqrt(y2*i2) - dw8*math.sqrt(p2*i2))
    return i1_part + i2_part

def dI3(y2, p2, i2, y3, u, dt, i3, k, dw8, dw9, dw10, i2_floored):
    if(i2_floored == True):
        i2_part = i2 * (p2 / (y2 + p2))
    else:
        i2_part = p2*i2*dt + k*dw8*math.sqrt(p2*i2)
    i3_part = -(y3+u)*i3*dt + k*(-dw9*math.sqrt(y3*i3) - dw10*math.sqrt(u*i3))
    return i2_part + i3_part

def dR(y1, y2, y3, p1, p2, u, i1, i2, i3, k, dt, dw5, dw7, dw9, i1_floored, i2_floored, i3_floored):
    if(i1_floored == True): i1_part = i1 * (y1 / (y1 + p1))
    else: i1_part = y1*i1*dt + k*dw5*math.sqrt(y1*i1)

    if(i2_floored == True): i2_part = i2 * (y2 / (y2 + p2))
    else: i2_part = y2*i2*dt + k*dw7*math.sqrt(y2*i2)

    if(i3_floored == True): i3_part = i3 * (y3 / (y3 + u))
    else: i3_part = y3*i3*dt + k*dw9*math.sqrt(y3*i3)
    return i1_part + i2_part + i3_part
    
def dD(i3, y3, u, k, dt, dw10, i3_floored):
    if(i3_floored == True):
        return i3 * (u / (y3 + u))
    return (u*i3*dt) + k*dw10*math.sqrt(u*i3)
    
def model(days, modifiers):
    # Initialize conditions and parametres.
    N = 1000000
    i1 = 0
    i2 = 0
    i3 = 0
    S = N-1
    E = 1
    D = 0
    R = 0
    masking_enabled = modifiers[0]
    lockdown_enabled = modifiers[1]
    stochasticity_enabled = modifiers[2]

    if(stochasticity_enabled == True):
        k = 0.1
    else:
        k = 0
    # fixed parameter set (for now), maybe allow adjustments later

    a = 0.2
    b1 = 0.5
    b2 = 0.1
    b3 = 0.1
    p1 = 0.033
    p2 = 0.042
    y1 = 0.133  
    y2 = 0.125
    y3 = 0.075
    u = 0.050
    dt = 1

    
    if(lockdown_enabled == True):
        lockdown_initiated = False

    # The parametres can be changed based upon the severity of PHSM (Public Health and Safety Measures)

    vals_S = [S]
    vals_E = [E]
    vals_i1 = [i1]
    vals_i2 = [i2]
    vals_i3 = [i3]
    vals_D = [D]
    vals_R = [R]
    # vals_total = [N]
    t = [0]
    runs = int(days / dt)
    for i in range(1, runs + 1):
        
        #used to create noise/stochasticity
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

        #needed to keep track of whether that bucket drops to zero in a step
        S_floored = False
        E_floored = False
        i1_floored = False
        i2_floored = False
        i3_floored = False

        #holds copies of initial/original values for calculations
        #all calculations should be done with these vars so everything occurs "at once"
        init_S = S
        init_E = E
        init_i1 = i1
        init_i2 = i2
        init_i3 = i3
        
        change_S= dS(b1, b2, b3, init_i1, init_i2, init_i3, init_S, k, dt, dw1, dw2, dw3, N)
        if(S + change_S < 0):
            S = 0
            S_floored = True
        elif(change_S < 0):
            S += change_S

        change_E = dE(b1, b2, b3, init_i1, init_i2, init_i3, a, init_E, init_S, k, dt, dw1, dw2, dw3, dw4, S_floored, N)
        if(init_E + change_E < 0): #amount of E at start of step drops to zero
            i1 += init_E #move it all to i1 since that's how the model works
            E -= init_E #remove initial amount from current E.
            E_floored = True
        else:
            E += change_E
        assert(E >= 0)

        change_i1 = dI1(a, init_E, y1, p1, dt, init_i1, k, dw4, dw5, dw6, E_floored)
        if(init_i1 + change_i1 < 0):
            i2 += init_i1 * (p1 / (y1 + p1))
            R += init_i1 * (y1 / (y1 + p1))
            i1 -= init_i1
            i1_floored = True
        else:
            i1 += change_i1
        assert(i1 >= 0)

        change_i2 = dI2(p1, y1, y2, p2, dt, init_i1, init_i2, k, dw6, dw7, dw8, i1_floored)
        if(init_i2 + change_i2 < 0):
            i3 += init_i2 * (p2 / (y2 + p2))
            R += init_i2 * (y2 / (y2 + p2))
            i2 -= init_i2
            i2_floored = True
        else:
            i2 += change_i2
        assert(i2 >= 0)

        change_i3 = dI3(y2, p2, init_i2, y3, u, dt, init_i3, k, dw8, dw9, dw10, i2_floored)
        if(init_i3 + change_i3 < 0):
            R += init_i3 * (y3 / (y3 + u))
            D += init_i3 * (u / (y3 + u))
            i3 -= init_i3
            i3_floored = True
        else:
            i3 += change_i3
        assert(i3 >= 0)

        change_R = dR(y1, y2, y3, p1, p2, u, i1, i2, i3, k, dt, dw5, dw7, dw9, i1_floored, i2_floored, i3_floored)
        R += change_R

        change_D = dD(i3, y3, u, k, dt, dw10, i3_floored)
        if change_D >= 0:
            D += change_D
        else:
            i3 -= change_D

        if(masking_enabled == True):
            if((i1 + i2 + i3) / N > 0.01):
                b1 = 0.25

        if(lockdown_enabled == True):
            if((i1 + i2 + i3) / N > 0.01):
                b1 = 0.375
                lockdown_initiated = True
                lockdown_start = i
            
            if(lockdown_initiated == True):
                if(i - lockdown_start >= 60 / dt):
                    b1 = 0.5

        vals_S.append(S)
        vals_E.append(E)
        vals_i1.append(i1)
        vals_i2.append(i2)
        vals_i3.append(i3)
        vals_D.append(D)
        vals_R.append(R)
        # vals_total.append(S + E + i1 + i2 + i3 + D + R)
        t.append(i)

    return [t, vals_S, vals_E, vals_i1, vals_i2, vals_i3, vals_D, vals_R]

    print(vals_D[-1]/N * 100)
    plt.plot(t, vals_S, label = "Susceptible")
    plt.plot(t, vals_E, label = "Exposed")
    plt.plot(t, vals_i1, label = "Mild Infection")
    plt.plot(t, vals_i2, label = "Severe Infection")
    plt.plot(t, vals_i3, label = "Critical Infection")
    plt.plot(t, vals_D, label = "Dead")
    plt.plot(t, vals_R, label = "Recovered")
    # plt.plot(t, vals_total, label = "total")
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title(f"Plot of COVID Spread")
    plt.legend()
    plt.show()
    return
    

def main():
    deterministic_vals = model(500, [True, False, False])
    stochastic_vals = model(500, [True, False, True])
    
    deter_t = deterministic_vals[0]
    deter_S = deterministic_vals[1]
    deter_E = deterministic_vals[2]
    deter_i1 = deterministic_vals[3]
    deter_i2 = deterministic_vals[4]
    deter_i3 = deterministic_vals[5]
    deter_D = deterministic_vals[6]
    deter_R = deterministic_vals[7]

    stoch_t = stochastic_vals[0]
    stoch_S = stochastic_vals[1]
    stoch_E = stochastic_vals[2]
    stoch_i1 = stochastic_vals[3]
    stoch_i2 = stochastic_vals[4]
    stoch_i3 = stochastic_vals[5]
    stoch_D = stochastic_vals[6]
    stoch_R = stochastic_vals[7]

    print(f"Percent of Deaths (Deterministic): {deter_D[-1]/1000000 * 100}%")
    print(f"Percent of Deaths (Stochastic): {stoch_D[-1]/1000000 * 100}%")
    plt.plot(deter_t, deter_S, label = "Susceptible (Deterministic)")
    plt.plot(deter_t, deter_E, label = "Exposed (Deterministic)")
    plt.plot(deter_t, deter_i1, label = "Mild Infection (Deterministic)")
    plt.plot(deter_t, deter_i2, label = "Severe Infection (Deterministic)")
    plt.plot(deter_t, deter_i3, label = "Critical Infection (Deterministic)")
    plt.plot(deter_t, deter_D, label = "Dead (Deterministic)")
    plt.plot(deter_t, deter_R, label = "Recovered (Deterministic)")
    plt.plot(stoch_t, stoch_S, label = "Susceptible (Stochastic)")
    plt.plot(stoch_t, stoch_E, label = "Exposed (Stochastic)")
    plt.plot(stoch_t, stoch_i1, label = "Mild Infection (Stochastic)")
    plt.plot(stoch_t, stoch_i2, label = "Severe Infection (Stochastic)")
    plt.plot(stoch_t, stoch_i3, label = "Critical Infection (Stochastic)")
    plt.plot(stoch_t, stoch_D, label = "Dead (Stochastic)")
    plt.plot(stoch_t, stoch_R, label = "Recovered (Stochastic)")
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title(f"Plot of COVID Spread")
    plt.legend()
    plt.show()

    return

main()

