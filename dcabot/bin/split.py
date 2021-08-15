#!/usr/bin/python3
#import cbpro
import sys
import argparse
# P_sell = ( 1/(1-F) ) * P_buy

def buy_split(P_buy, amt=1.0, F_rate=0.005, verbose=False):
    if verbose:
        print("Sell at limit to break even:")
    
    p_limit_sell = ((1/(1-F_rate))**2)*float(P_buy)


    return p_limit_sell

def sell_split(P_sell, F_rate=0.005, verbose=False):
    if verbose:
        print("Buy at limit to break even:")
    p_limit_buy = P_sell * ((1-F_rate)**2)

    return p_limit_buy

def do_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
            '--price',
            help="Price which you purchased/sold at",
            type=float
            )

    parser.add_argument(
            '--side',
            help="buy or sell",
            type=str
            )

    parser.add_argument(
            '--fee',
            help="buy or sell",
            type=float
            )

    args = parser.parse_args()
    return args

def main():
    args = do_args()
    if args.side == 'buy':
        print(buy_split(args.price, F_rate=args.fee, verbose=True))
    elif args.side == 'sell':
        print(sell_split(args.price, F_rate=args.fee,  verbose=True))
    else:
        print('u dum?')

if __name__ == '__main__':
    main()
#    P_SELL = float(sys.argv[2])
#    P_BUY = float(sys.argv[2])
#    verbose = False
#    if len(sys.argv) > 3:
#        verbose = sys.argv[3]
#
#    if sys.argv[1] == 'buy':
#        print(buy_split(P_BUY, verbose=verbose))
#    elif sys.argv[1] == 'sell':
#        print(sell_split(P_SELL, verbose=verbose))

