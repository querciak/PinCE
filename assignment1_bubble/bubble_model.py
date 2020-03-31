import numpy as np
from matplotlib import pyplot as plt
from random import seed
from random import random
from random import randint
import math
from random import gauss
from random import gammavariate

STOCKSn = 200000
FALLING = False
maxVAL = 0


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
        stock = gauss(2.7 ** tmp, 10 * (mp + pi))
        ref = y[-1] / 3
        if stock < ref:
            stock = gauss(ref, ref * mp + pi)
        if day % save_every_x_days == 0:
            x.append(x[-1] + save_every_x_days)
            print("day:{}| stock:{}| tmp:{}".format(x[-1], stock, tmp))
            y.append(stock + gammavariate(0.5, 5))
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
                    y.append(stock)
            if FALLING:
                if y[-1] > maxVAL/3:
                    variation = abs(gauss(maxVAL/300, 100 / d))
                    print("stock below zero: ", stock, " y[-2]: ", y[-2], " variation: ", variation)
                    stock = y[-1] - variation
                    if y[-1] < 100 * d:
                        stock = -y[-1] / (d * 10)

                else:
                    stock = y[-1] + abs(gauss(50, 100))
                    print("else")
                y.append(stock)

    return x, y


def plot_graph(x, y):
    print("Plotting graph...")
    plt.title("Ellesmera bubble")
    plt.ylabel("price [$]")
    plt.xlabel("time [day]")
    plt.plot(x, y, label="bubble")
    # plt.bar(x, y, width=0.1)
    plt.show()


def main():
    mp, d, liq, length, pi = model_specs()  # read characteristics of 'Ellesmera' (fictional name of a new application)
    x, y = fill_list(mp, d, liq, length, pi)  # fill list with nominal price of 'Ellesmera
    plot_graph(x, y)  # plot graph


main()


def test_graph():
    # add a title
    plt.title("info")
    # add axes' name
    plt.ylabel("Y axis")
    plt.xlabel("X axis")

    # data w/ linspace
    z = np.linspace(0, 10, 100)
    # plot z
    plt.plot(z, z, label="linear")
    # add the legend
    plt.legend()

    # plot x and y as symple lists
    plt.plot([1, 2, 3], [4, 5, 1])

    # third line again with simple lists as x & y
    x = [5, 8, 10]
    y = [12, 16, 6]
    plt.plot(x, y)

    # Result
    plt.show()
