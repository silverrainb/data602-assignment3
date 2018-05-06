#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import trade
from ledger import Ledger
import gdax_websocket as gw
import time
import pl_display as pldisp

def menu():
    print("1. Trade")
    print("2. Show Blotter")
    print("3. Show P/L")
    print("4. Show P/L Records")
    print("5. Show P/L Chart")
    print("6. Quit")


def main(argv):
    horizontal_line = "-------------------------"
    print(horizontal_line * 2)
    print("DAT602-assignment3 crypto-trading demo.")
    gdax = gw.gdax_websocket()
    gdax.start()
    time.sleep(1)
    ledger = Ledger(100000000)
    print("$" + str(ledger.get_current_cash()) + " available to start trading.")
    print(horizontal_line * 2)

    fini = False

    while not fini:
        menu()
        choice = input(">>>>> Please select the menu: \n>")
        if choice == "6":  # Quit
            fini = True
            gdax.stop()

        elif choice == "5":  # Show P/L Chart
            print(horizontal_line * 3)
            print("<<P/L Line Chart>>")
            print(horizontal_line * 3)
            try:
                pl_data = ledger.get_pl_cache()
                pldisp.pl_display(pl_data)
                print("Should the graph fails to load in the browser,")
                print("Please click: https://plot.ly/~silverrainb/10/vwap-executedprice-total-pl-cash/")
                print(horizontal_line * 3)
            except TypeError:
                print("Unable to load the chart. Please try again.")
                print(horizontal_line * 3)

        elif choice == "4":  # Show P/L Records
            print(horizontal_line * 3)
            print("<<P/L Records>>")
            print(horizontal_line * 3)
            pl_data = ledger.get_pl_cache()
            print(pl_data)

        elif choice == "3":  # Show P/L
            print(horizontal_line * 3)
            print("<<P/L>>")
            print("Please hold while calculating forecast...")
            print(horizontal_line * 3)
            ledger.update_positions(gdax)
            print(horizontal_line * 3)

        elif choice == "2":  # Show Blotter
            print(horizontal_line * 3)
            print("<<Blotter>>")
            print(horizontal_line * 3)
            blotter = ledger.get_blotter()
            print(blotter)
            print(horizontal_line * 3)

        elif choice == "1":  # Trade
            trade.trade(ledger, gdax)

    print(">>>>> Goodbye!")


if __name__ == "__main__":
    main(sys.argv)
