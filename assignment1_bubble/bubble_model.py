import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from random import seed
from random import random
from random import randint
import math
from random import gauss
from random import gammavariate

STOCKSn = 400000
FALLING = False
maxVAL = 0

z = 0
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# Starting amount of stocks owned by careful investors
StocksOwnedByCarefulInvestors = 0.01 * STOCKSn
# Growth rate for the percentage of stocks owned by careful investors
StocksOwnedByCarefulInvestorsGrowthRate = 0.0001
# Arbitary value on how much careful investors believe in market a.k.a buy more stocks
CarefulStockOwnersFaith = 0.5


def model_specs():
    #print("Reading parameters of the model...")
    mp = 0.5  # Market Penetration
    d = 0.7  # Disruptiveness
    liq = 10 ** 9  # forecast for liquidity
    length = 33  # length of the bubble in years
    psycho_impact = 0.01  # Psychological impact
    return mp, d, liq, length, psycho_impact


def fill_list(mp, d, liq, length, pi):
    #print("Starting model calculation...")
    x, y = [0], [1000]
    whenLastCrashEnded = 0
    global FALLING
    # Force first phase to be 4 years
    first_phase_length = 4
    # TODO
    # - Implement a mechanism to allow stock price influence when the bubble starts
    for year in range(length):
        yearsFromLastCrash = year - whenLastCrashEnded
        if yearsFromLastCrash <= first_phase_length:
            print("FirstPhase")
            x, y = calculate_price_first_phase(x, y, yearsFromLastCrash + 1, year + 1, mp, pi)
        else:
            print("SecondPhase")
            x, y, temp = calculate_price_second_phase(x, y, yearsFromLastCrash + 1, year + 1, mp, d, liq, pi, whenLastCrashEnded)
            # Reset the model back to phase one when crash has reached it's lowest
            if temp > whenLastCrashEnded:
                print("Reset cycle")
                FALLING = False
                whenLastCrashEnded = temp
    return x, y


def calculate_price_first_phase(x, y, yearsFromLastCrash, year, mp, pi):
    # TODO
    global STOCKSn, StocksOwnedByCarefulInvestors, StocksOwnedByCarefulInvestorsGrowthRate, CarefulStockOwnersFaith
    save_every_x_days = 10
    for day in range(365):
    
        # Stocks owned by careful investors rise during the first phase
        StocksOwnedByCarefulInvestors = StocksOwnedByCarefulInvestors + (STOCKSn-StocksOwnedByCarefulInvestors) * StocksOwnedByCarefulInvestorsGrowthRate
        # And they slowly gain more faith in the market
        CarefulStockOwnersFaith = min(CarefulStockOwnersFaith + pi, 1)
        
        # During the first phase stocks prices grow slowly
        tmp = (yearsFromLastCrash + 0.0026 * day)/5
        stock = y[-1] + gauss(tmp, 5)
        if day % save_every_x_days == 0:
            x.append(x[-1] + save_every_x_days)
            #print("day:{}| stock:{}| tmp:{}".format(x[-1], stock, tmp))
            
            if stock > 80:
                y.append(stock)
            else:
                stock = stock + gauss(1, 5) * 1.1
                y.append(stock)
    return x, y


def calculate_price_second_phase(x, y, yearsFromLastCrash, year, mp, d, liq, pi, previousCrashEnded):
    # Added a mechanish to start the cycle again
    lastCrashEnded = previousCrashEnded
    crashHasEnded = False
    
    # TODO
    save_every_x_days = 10
    global FALLING, maxVAL, StocksOwnedByCarefulInvestors, STOCKSn, CarefulStockOwnersFaith
    
    for day in range(365):
        tmp = yearsFromLastCrash + 0.00275 * day
        
        delta = gauss(tmp, tmp ** 0.5) * tmp
        stock = y[-1] + delta
        
        # During the phase two careful investors start to lose their faith in the market
        CarefulStockOwnersFaith = max(CarefulStockOwnersFaith - pi, 0.01)
        # This results in them selling their stocks.
        if CarefulStockOwnersFaith < 0.55 and StocksOwnedByCarefulInvestors > 1000:
            stock -= delta * (2 / math.sqrt(CarefulStockOwnersFaith)) * (StocksOwnedByCarefulInvestors / STOCKSn)
            StocksOwnedByCarefulInvestors -= StocksOwnedByCarefulInvestors * (0.1 / math.sqrt(CarefulStockOwnersFaith)) * 0.02
        
        if day % save_every_x_days == 0:
            x.append(x[-1] + save_every_x_days)
            if not FALLING:
                # If total price reaches the liquidity bubble will burst
                if stock * STOCKSn > liq:
                    print("bubble...")
                    FALLING = True
                else:
                    # Keep track of the max Value
                    if maxVAL < y[-1]:
                        maxVAL = y[-1]
                    if stock > 0:
                        y.append(stock)
                    else:
                        # If price goes below 0 pause the simulation
                        input("Too low? {}".format(stock))
                        y.append(stock)
            if FALLING:
                # Market penetration acts as a reality check and sets the limit for how low the price can go
                if y[-1] > maxVAL * mp and not crashHasEnded:
                    variation = gauss(10, 8) * 10
                    stock = y[-1] - variation
                    if y[-1] < 100 * d:
                        stock = -y[-1] / (d * 10)
                    y.append(stock + gauss(50, 10))
                elif not crashHasEnded:
                    # As the stock has reached its low point return the current year to reset simulation back to phase one
                    lastCrashEnded = year
                    crashHasEnded = True
                    stock = y[-1] + abs(gauss(0, 5))
                    y.append(stock + gauss(5, 10))
                else:
                    y.append(y[-1] + abs(gauss(3, 10)))
    return x, y, lastCrashEnded


def plot_graph(x, y, length):
    print("Plotting graph...")
    plt.title("Ellesmera bubble")
    plt.ylabel("price [$]")
    plt.xlabel("time [year]")
    plt.plot(x, y, label="bubble")
    plt.xticks([i*365 for i in range(length+1)], [str(0+i) for i in range(length+1)])
    plt.show()


def main():
    mp, d, liq, length, pi = model_specs()  # read characteristics of 'Ellesmera' (fictional name of a new application)
    x, y = fill_list(mp, d, liq, length, pi)  # fill list with nominal price of 'Ellesmera
    if input("Animate the graph? [y/n]") == "y":
        ani = animation.FuncAnimation(fig, animate, fargs = (x,y), interval=50)
    else:
        plot_graph(x, y, length)  # plot graph
    plt.show()


def animate(i,x,y):
    global z
    x = x[0:z]
    y = y[0:z]
    z += 1
    ax1 = fig.add_subplot(1,1,1)
    ax1.clear()
    ax1.set_ylabel('price [$]')
    ax1.set_xlabel('time [day]')
    ax1.set_title('Bubble')
    ax1.plot(x,y)
    


main()

