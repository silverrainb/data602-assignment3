#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import trade
from ledger import Ledger
import gdax_websocket as gw
import time
from pl_display import pl_display


def menu():
    print("1. Trade")
    print("2. Show Blotter")
    print("3. Show P/L")
    print("4. Show P/L History")
    print("5. Quit")


def main(argv):
    horizontal_line = "-------------------------"
    print(horizontal_line * 2)
    print("DAT602-assignment3 crypto-trading demo.\n$100MM available to start trading.")
    print(horizontal_line * 2)
    gdax = gw.gdax_websocket()
    gdax.start()
    time.sleep(1)
    ledger = Ledger(100000000)

    fini = False

    while not fini:
        menu()
        choice = input(">>>>> Please select the menu: \n>")
        if choice == "5":  # Quit
            fini = True
            gdax.stop()

        elif choice == "4":  # Show P/L History
            print(horizontal_line * 3)
            print("<<P/L History & Line Chart>>")
            print(horizontal_line * 3)
            pl_data = ledger.print_pl_cache()
            print(pl_data)
            try:
                pl_display(pl_data)
            except ValueError as e:
                print("No transactions have been performed to display the history" + str(e))
            print(horizontal_line * 3)
            print("Should the graph fails to load in the browser,")
            print("please click: https://plot.ly/~silverrainb/10/vwap-executedprice-total-pl-cash/")
            print(horizontal_line * 3)

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

            ledger.print_blotter()
            print(horizontal_line * 3)

        elif choice == "1":  # Trade
            trade.trade(ledger, gdax)

    print(">>>>> Goodbye!")


if __name__ == "__main__":
    main(sys.argv)
