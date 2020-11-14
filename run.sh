#!/bin/bash
# ./Rt SEED NSIM SIGMA INPUT1 INPUT2 1>OUTPUT
# SEED: seed of the random number generator (integer)
# NSIM: number of simulations (interger)
# SIGMA: standard deviation of the normal distribution used to sample candidate parameters (float)
# INPUT1: input file containing the parameters of the gamma distribution of the generation time (string)
# INPUT2: input file containing the time series (string) [First colum: date; second colum: number of new cases in that date (i.e., the sum of local and imported cases); third colum: number of new imported cases in that date]
# OUTPUT: name of the file where the output is printed (string)
./Rt 1 10000 0.05 Tg_7.5 ./Sichuan_2020-02-29 1>Rt-output
 
