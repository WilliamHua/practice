import math

#FDM pricing methods for vanilla and binary options

def basket(Vol_H, Vol_L, r, bStrike, lowStrike, highStrike, Expiration, NAS, weight1, weight2):
    ds = 2 * highStrike / NAS   
    dt = 0.9 / Vol_H ** 2 / NAS ** 2
    NTS = int(Expiration/dt) + 1
    dt = Expiration/NTS
    assetPrices = [0]*NAS
    payoff = [0]*NAS
    vold = [0]*NAS
    vnew = [0]*NAS
    value = [0]*NAS
    heaviside = lambda x, y: 1 if x > y else 0 

    for i in range(NAS):
        assetPrices[i] = i * ds
        payoff[i] = (heaviside(assetPrices[i], bStrike) + weight1 * max(assetPrices[i] - lowStrike, 0) + weight2 * max(assetPrices[i] - highStrike, 0)) * 1000
        vold[i] = payoff[i]

    for i in range(NTS):
        for j in range(NAS - 1):
            Delta = (vold[j + 1] - vold[j - 1]) / (2 * ds)
            Gamma = (vold[j + 1] - 2 * vold[j] + vold[j - 1]) / (ds ** 2)

            if(Gamma >= 0):
                Vol = Vol_L
            else: 
                Vol = Vol_H

            Theta = r * vold[j] - 0.5 * (Vol * assetPrices[j]) ** 2 * Gamma - r * assetPrices[j] * Delta
            vnew[j] = vold[j] - Theta * dt

        vnew[0] = vold[0] * (1 - r * dt)
        vnew[NAS - 1] = 2 * vnew[NAS - 2] - vnew[NAS - 3]
        for j in range(NAS):
            vold[j] = vnew[j]

    for i in range(NAS):
        value[i] = vold[i]
        value[i] = value[i] / 1000.0
        payoff[i] = payoff[i] / 1000.0

    return [assetPrices, payoff, value]

def option(Vol_H, Vol_L, r, Option_Type, Strike, Expiration, NAS, position):
    ds = 2 * Strike / NAS               #inf
    dt = 0.9 / Vol_H ** 2 / NAS ** 2    #stability
    NTS = int(Expiration/dt) + 1
    dt = Expiration/NTS
    assetPrices = [0]*NAS
    payoff = [0]*NAS
    vold = [0]*NAS
    vnew = [0]*NAS
    value = [0]*NAS
    heaviside = lambda x, y: 1 if x > y else 0 #if y < x else 0.5

    for i in range(NAS):
        assetPrices[i] = i * ds
        if Option_Type == "vanilla":
            payoff[i] = max(assetPrices[i] - Strike, 0) * 1000
        elif Option_Type == "binary":
            payoff[i] = heaviside(assetPrices[i], Strike) * 1000
        else:
            print "Option_Type unrecognized"
        vold[i] = payoff[i]

    for i in range(NTS):
        for j in range(NAS - 1):
            Delta = (vold[j + 1] - vold[j - 1]) / (2 * ds)
            Gamma = (vold[j + 1] - 2 * vold[j] + vold[j - 1]) / (ds ** 2)

            if position * Gamma >= 0:
                Vol = Vol_L
            else: 
                Vol = Vol_H

            Theta = r * vold[j] - 0.5 * (Vol * assetPrices[j]) ** 2 * Gamma - r * assetPrices[j] * Delta
            vnew[j] = vold[j] - Theta * dt

        vnew[0] = vold[0] * (1 - r * dt)
        vnew[NAS - 1] = 2 * vnew[NAS - 2] - vnew[NAS - 3]
        for j in range(NAS):
            vold[j] = vnew[j]

    for i in range(NAS):
        value[i] = vold[i]
        value[i] = value[i] / 1000.0
        payoff[i] = payoff[i] / 1000.0

    return [assetPrices, payoff, value]

def BlackScholes(currentPrice, strikePrice, time, interestRate, impliedVol):

        #Convert all numbers to float
        (strikePrice, time, interestRate, impliedVol) = (float(strikePrice), float(time), float(interestRate), float(impliedVol))
        #Find d1 and d2(currentPrice, strikePrice, time, interestRate, impliedVol)
        d1 = (math.log(currentPrice / strikePrice) + (interestRate + impliedVol**2 / 2)*time) / (math.sqrt(time)*impliedVol)
        d2 = (math.log(currentPrice / strikePrice) + (interestRate - impliedVol**2 / 2)*time) / (math.sqrt(time)*impliedVol)
        
        return cdf(d1)*currentPrice - cdf(d2)*strikePrice*math.exp(-interestRate*time)


def cdf(x): 
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def findValue(arrays, value):
    for i in range(len(arrays[0])):
        if arrays[0][i] == value:
            return arrays[2][i]

lowerOption = BlackScholes(100, 90, .5, .05, .25)
higherOption = BlackScholes(100, 110, .5, .05, .25)

realLower = 14.81
realHigher = 4.94


#baskets = basket(.3, .2, .05, 100, 90, 110, .5, 100, -.05, .05)
#print str(findValue(baskets, 100))
binary = option(.3, .2, .05, "binary", 100, .5, 100, -1)

minimum = [100, 100, 100]
for i in range(-10, 0):
    for j in range(1, 10):
        baskets = basket(.3, .2, .05, 100, 90, 110, .5, 100, i/100.0, j/100.0) 
        value = findValue(baskets, 100) - i/100.0 * lowerOption - j/100.0 * higherOption
        if(abs(minimum[2]) > abs(findValue(baskets, 100))): #and findValue(baskets, 80) < .001):
            print "i: " + str(i) + " j: " + str(j) + "baskets: " + str(findValue(baskets, 100))
            minimum[0] = i
            minimum[1] = j
            minimum[2] = findValue(baskets, 100)

print "MIN: Lambda1 = " + str(minimum[0]) + " Lambda2: " + str(minimum[1]) + " Value: " + str(minimum[2]) 
print "Backed binary: " + str(minimum[2] - minimum[0]/100.0*lowerOption - minimum[1]/100.0*higherOption)
