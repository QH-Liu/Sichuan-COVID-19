0.  "project.py": python code for projection

1. "long_tg.txt": the file for the generation time distribution. 
Each row includes two columns with the following format:
interval \t probability

2. "posterior_R_Sichuan_2020-02-29_SI7.5_WEEKS1": the estimates of R0 by using the last one week before the declaration of the public health emergency.
Each row is an estiamte of R0.

3. "posterior_R1_Sichuan_2020-02-29_SI7.5_scenario2": the estimates of R_final when assuming a linear decrease from R0 to R_final within one week when the public health emergency is declared
Each row is an estiamte of R_final.

4. "Rt.c": estimating Rt, using run.sh to run

5. "Tg_7.5": each row with two values: shape and rate for the gamma distribution of the generation time. 

6. "Sichuan_2020-02-29": each row includes three columns: date, daily number of symptomatic cases, daily number of imported cases
