#!/bin/env python

import sys, getopt
import os.path
import hashlib

def DNA_analysis(input):
    A = input.count('a')
    T = input.count('t')
    G = input.count('g')
    C = input.count('c')
    AT = A+T
    GC = G+C
    size = len(input)

    TGA = input.count('tga')
    TAA = input.count('taa')
    TGA = input.count('tga')

    print("GC content: " + str(GC/(GC+AT)))
    print("AT/GC ratio: " + str(AT/GC))
    print("sequence length: " + str(round(size/1000)) + " kbp")
    print("#codons stops (all frames) TGA=" + str(TGA)
          + ", TAA=" + str(TAA)
          + ", TGA=" + str(TGA)
          + ", total=" + str(TGA+TAA+TGA))
    

def trans(input):
    bit2qit = {'00':'a',
               '01':'t',
               '10':'g',
               '11':'c'}
    output = ''
    
    if type(input) is not type(str.encode('')):
        input = str.encode(input)
    
    for byte in input:
        bits = bin(byte)[2:].rjust(8,'0')
        for qit in range(0,8,2):
            output += bit2qit[bits[qit:qit+2]]
            
    return output

def read_translate_write(inputfile,outputfile):
    
    buffer_out = ''
    buffer_in  = ''
    
    print("reading " + inputfile)
    f = open(inputfile, "rb")
    buffer_in = f.read()
    f.close()
    
    print("translating")
    buffer_out = trans(buffer_in)
    
    print("writing " + outputfile)
    fileout = open(outputfile, 'w')
    fileout.write(buffer_out)
    fileout.close()
    
    return (buffer_in,buffer_out)

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
            
    byte2DNA_processing(inputfile,outputfile)

def byte2DNA_processing(inputfile, outputfile):
    print("="*20 + " ENCODING " + "="*20)
    (fi,fo) = read_translate_write(inputfile,outputfile)

    print()
    print("="*20 + " DNA analysis " + "="*20)
    DNA_analysis(fo)

    print()
    print("="*20 + " HASHING " + "="*20)
    hi = hashlib.sha224(fi).hexdigest()
    print("inputfile sha224 hash = " + hi)
    hi_DNA = trans(hi)
    print("DNA version = " + hi_DNA)
    
    print()
    print("="*20 + " HASHING " + "="*20)
    ho = hashlib.sha224(fo.encode('utf-8')).hexdigest()
    print("DNA sequence sha224 hashing = " + ho)
    ho_DNA = trans(ho)
    print("DNA version = " + ho_DNA)

if __name__ == "__main__":
    byte2DNA_processing('facebook-lipulsar.zip','facebook-lipulsar.DNA.txt')
    #main(sys.argv[1:])



