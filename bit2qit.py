#!/bin/env python

import sys, getopt
import os.path

def read_translate_write(inputfile,outputfile):
    bit2qit = {'00':'a',
               '01':'t',
               '10':'g',
               '11':'c'}
    
    buffer_out = ''
    buffer_in  = ''
    
    print("reading " + inputfile)
    f = open(inputfile, "rb")
    buffer_in = f.read()
    f.close()
    
    print("translating")
    for byte in buffer_in:
        bits = bin(byte)[2:].rjust(8,'0')
        for qit in range(0,8,2):
            buffer_out += bit2qit[bits[qit:qit+2]]

    print(" size: " + str(len(buffer_out)) + "bp")
    
    print("writing " + outputfile)
    fileout = open(outputfile, 'w')
    fileout.write(buffer_out)
    fileout.close()

def main(argv):
    help_message = 'usage: bit2qit -i <inputfile> -o <outputfile>'
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["i=","o="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
 
    if inputfile == '':
        print("no input file\n" + help_message)
        sys.exit(2)           
    if outputfile == '':
        print("no output file\n" + help_message)
        sys.exit(2)
    if not os.path.isfile(inputfile):
        print(inputfile + ": no such file\n" + help_message)
        sys.exit(2)
    while os.path.isfile(outputfile):
        print(outputfile + ": file exists")
        (file,extension) = outputfile.split('.')
        outputfile = file + '_.' + extension
        print("writing to: " + outputfile) 
            
    read_translate_write(inputfile,outputfile)
    
if __name__ == "__main__":
    main(sys.argv[1:])



