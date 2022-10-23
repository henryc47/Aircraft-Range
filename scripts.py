#contains scripts which are useful to the aircraft-range project
#all units are SI except where otherwise noted
import math as m

#calculates the atmospheric density by altitude
#https://en.wikipedia.org/wiki/Barometric_formula
def get_atmospheric_density(altitude):
    hs = [0,11000,20000,32000,47000,51000,71000] #starting altitude for each band
    next_hs = [11000,20000,32000,47000,51000,71000,m.inf]
    ps = [1.225,0.36391,0.08803,0.01322,0.00143,0.00086,0.000064] #starting density for each band
    ts = [288.15,216.65,216.65,228.65,270.65,270.65,214.65] #starting temperature for each band
    Ls = [-0.0065,0,0.001,0.0028,0,-0.0028,-0.002] #temperature lapse rate each band
    band = 0
    for max_height in next_hs: #extract the max altitude in each band
        if altitude<max_height:
            #extract info from the relevant band
            h = hs[band]
            pb = ps[band]
            t = ts[band]
            L = Ls[band]
            if L==0:
                p = get_atmospheric_density_no_temp_lapse(pb,t,altitude-h)
            else:
                p = get_atmospheric_density_temp_lapse(pb,t,L,altitude-h)
            return p #we have calculated the density

        else:
            band = band + 1

    print("WARNING: Max Atmosphere Height ",next_hs[-1]," Exceeded, zero density returned")
    return 0






#Implemention of equation 1, temperature lapse rate not zero
#pb = density at base, t = temperature at base, L = temperature lapse rate h = height relative to base, R = gas constant, g= gravity acceleration, M = molar mass air 
def get_atmospheric_density_temp_lapse(pb,t,L,h,R=8.314,g=9.81,M=0.02896):
    p = pb*(t/(t+h*L))**(1+((g*M)/(R*L)))
    return p

#Implemention of equation 2, temperature lapse rate equal to zero
def get_atmospheric_density_no_temp_lapse(pb,t,h,R=8.314,g=9.81,M=0.02896):
    p = pb*m.exp((-g*M*h)/(R*t))
    return p

#Implemention of equation 2, temperature lapse rate not zero