#!/usr/bin/env python3

import sys, netana

def main(args=None) :
	if args == None :
		args = sys.argv[1:]
		netana.main()
   
if __name__ == "__main__" :
	print("Starting Netana")
	main()
	print("Exiting Netana")
