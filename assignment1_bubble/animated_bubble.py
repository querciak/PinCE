import numpy as np
#from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import pandas as pd

from random import seed
from random import random
from random import randint
import math
from random import gauss
from random import gammavariate

STOCKSn = 200000
FALLING = False
maxVAL = 0
z=0
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def model_specs():
    print("Reading parameters of the model...")
    # TODO
    mp = 0.02  # Market Penetration
    d = 0.7  # Disruptiveness
    liq = 10 ** 9  # forecast for liquidity
    length = 11  # length of the bubble in years
    psycho_impact = 0.7  # Psychological impact
    return mp, d, liq, length, psycho_impact


def fill_list(mp, d, liq, length, pi):
    print("Starting model calculation...")
    x, y = [0], [0]
    first_phase = length / 3
    for year in range(length):
        if year <= first_phase:
            x, y = calculate_price_first_phase(x, y, year + 1, mp, pi)
        else:
            x, y = calculate_price_second_phase(x, y, year + 1, d, liq, pi)

    return x, y


def calculate_price_first_phase(x, y, year, mp, pi):
    # TODO
    save_every_x_days = 10
    for day in range(365):
        tmp = year + 0.0026 * day
        # stock = gauss(2.7 ** tmp, 10 * (mp + pi))
        stock = gauss(2.7 ** tmp, 10 * ((mp + 0.5)**2 + pi))
        ref = y[-1] / 3
        if stock < ref:
            stock = gauss(ref, ref * mp + pi)
        if day % save_every_x_days == 0:
            x.append(x[-1] + save_every_x_days)
            print("day:{}| stock:{}| tmp:{}".format(x[-1], stock, tmp))
            price = stock + gauss(30, 30)
            if price > 0:
                y.append(stock + abs(gauss(stock, 30)))
            else:
                stock = gauss(4, 1)
                y.append(stock)
        print(stock)
    return x, y


def calculate_price_second_phase(x, y, year, d, liq, pi):
    # TODO
    save_every_x_days = 10
    global FALLING, maxVAL
    for day in range(365):
        tmp = year + 0.00275 * pi * day
        ref = y[-1] / 3
        stock = abs(gauss(2.7 ** tmp, tmp ** 1.5))
        if stock < ref:
            stock = gauss(ref * 2, ref * d + pi)
        if day % save_every_x_days == 0:
            x.append(x[-1] + save_every_x_days)
            if not FALLING:
                if stock * STOCKSn > liq:
                    print("bubble...")
                    FALLING = True
                else:
                    print("day:{}|stock:{}|tmp:{}".format(x[-1], stock, tmp))
                    if maxVAL < y[-1]:
                        maxVAL = y[-1]
                    stock = stock + gauss(50, 100)
                    if stock > 0:
                        y.append(stock)
                    else:
                        y.append(-stock)
            if FALLING:
                if y[-1] > maxVAL/3:
                    variation = abs(gauss(maxVAL/300, 100 / d))
                    print("stock below zero: ", stock, " y[-2]: ", y[-2], " variation: ", variation)
                    stock = y[-1] - variation
                    if y[-1] < 100 * d:
                        stock = -y[-1] / (d * 10)

                else:
                    stock = y[-1] + abs(gauss(50, 50))
                    print("else")
                y.append(stock + gauss(50, 100))
    return x, y


def plot_graph(x, y, length):
    print("Plotting graph...")
    plt.title("Ellesmera bubble")
    plt.ylabel("price [$]")
    plt.xlabel("time [year]")
    plt.plot(x, y, label="bubble")
    plt.xticks([i*365 for i in range(length+1)], [str(2020+i) for i in range(length+1)])
    plt.show()

def animate(i,x,y):
    global z
    x = x[0:z]
    y = y[0:z]
    z = z + 1
    ax1 = fig.add_subplot(1,1,1)
    ax1.clear()
    ax1.set_ylabel('price [$]')
    ax1.set_xlabel('time [year]')
    ax1.set_title('Bubble')
    ax1.plot(x,y)
    
def main():
    
    #fig = plt.figure()
    
    mp, d, liq, length, pi = model_specs()  # read characteristics of 'Ellesmera' (fictional name of a new application)
    x, y = fill_list(mp, d, liq, length, pi)  # fill list with nominal price of 'Ellesmera
    #plot_graph(x, y, length)  # plot graph
    ani = animation.FuncAnimation(fig, animate, fargs = (x,y), interval=50)
    plt.show()


main()
