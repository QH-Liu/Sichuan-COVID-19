import numpy as np
import matplotlib.pyplot as plt

#read case data up to the DAY
def readCaseData_new(rfile,DAY):
	f=open(rfile,'r')
	caseSeq=[]
	day=0
	for line in f:
		lines = line[:-1].split(' ')
		date=lines[0]
		case=int(lines[1])
		#input_case=int(lines[2])
		if day<DAY:
			caseSeq.append(case)
		day=day+1
	f.close()

	simCaseSeq={}
	for i in range(1000):		#repeat for 1000 times
		simCaseSeq[i]=caseSeq
	return simCaseSeq

#read the distribution of the generation time
def readTgFile(rfile):
	tgDis={}
	f=open(rfile,"r")
	for line in f:
		lines=line[:-1].split("\t")
		tg=int(lines[0])
		p=float(lines[1])
		tgDis[tg]=p
	f.close()
	return tgDis

#project the number of cases at the next day
def projectCase(caseSeq,tgDis,Rt):
	p_It=0
	for tau in range(14):
		p_It += Rt * caseSeq[len(caseSeq) - 1 - tau] * tgDis[tau]

	p_It=int(p_It)

	return p_It

#project all
def projectAllCase(caseSeq,tgDis,R0,R1,num_delay_weeks):
	t_caseSeq=[]
	for i in range(len(caseSeq)):
		t_caseSeq.append(caseSeq[i])

	if num_delay_weeks==0:			#no delay
		for t in range(1,150):		#jan 25 to Mar 6
			case=projectCase(t_caseSeq,tgDis,R1)
			t_caseSeq.append(case)

	elif num_delay_weeks>0:
		for t in range(1,7*num_delay_weeks+1):		#jan 25 to Mar 6
			case=projectCase(t_caseSeq,tgDis,R0)
			t_caseSeq.append(case)

		step=1
		for t in range(7*num_delay_weeks+1,7*num_delay_weeks+8):		#jan 25 to Mar 6
			case=projectCase(t_caseSeq,tgDis,R0-(R0-R1)/7*step)
			step=step+1
			t_caseSeq.append(case)

		for t in range(7*num_delay_weeks+8,150):		#jan 25 to Mar 6
			case=projectCase(t_caseSeq,tgDis,R1)
			t_caseSeq.append(case)
	else:
		print("error")
	return t_caseSeq

def readLastOneWeekRt(rfile):
	f=open(rfile,"r")
	seq=[]
	for line in f:
		r=float(line[:-1])
		seq.append(r)
	f.close()

	return seq #seq[index_low:index_up]


def projection(num_delay_weeks,R0_Data_file,Rfinal_Data_file):
	sim_case_confirm=readCaseData_new("./../data/Sichuan_2020-02-29",24)	#read the first 24 data points
	sim_all_realData=readCaseData_new("./../data/Sichuan_2020-02-29",66)	#read all data points

	tgDis=readTgFile("long_tg.txt")

	sim_all_cumCase={}
	for sim in sim_all_realData.keys():
		if not sim in sim_all_cumCase.keys():
			sim_all_cumCase[sim]=[]
			sim_all_cumCase[sim].append(sim_all_realData[sim][0])
		for i in range(1,len(sim_all_realData[sim])):
			cum_case=sim_all_cumCase[sim][i-1]+sim_all_realData[sim][i]
			sim_all_cumCase[sim].append(cum_case)

	R0_seq=readLastOneWeekRt(R0_Data_file)
	R1_seq=readLastOneWeekRt(Rfinal_Data_file)

	sim_estimateCumCase={}

	for sim in range(len(sim_case_confirm.keys())):		#for each seq
		case_confirm=sim_case_confirm[sim]
		if not sim in sim_estimateCumCase.keys():
			sim_estimateCumCase[sim]=np.zeros(173)

		num_sub_sims=1
		for sub_sim in range(num_sub_sims):		#run for 1000 times
			indexSeq = np.random.randint(len(R0_seq), size=1)
			R0=R0_seq[indexSeq[0]]
			indexSeq = np.random.randint(len(R1_seq), size=1)
			R1 = R1_seq[indexSeq[0]]
			estimatedCase=projectAllCase(case_confirm,tgDis,R0,R1,num_delay_weeks)
			cum_estimateCase=[]
			cum_estimateCase.append(estimatedCase[0])
			for i in range(1,len(estimatedCase)):
				cum_estimateCase.append(cum_estimateCase[i-1]+estimatedCase[i])

			sim_estimateCumCase[sim]=sim_estimateCumCase[sim]+np.array(cum_estimateCase)*1.0/num_sub_sims

	day_cumSeq={}

	#output
	w=open("projectedCase_"+str(num_delay_weeks)+".txt",'w')
	w1=open("projectedTotalCase_"+str(num_delay_weeks)+".txt","w")
	for sim in sim_estimateCumCase.keys():
		seq=sim_estimateCumCase[sim]
		for day in range(len(seq)):
			w.write(str(sim)+'\t'+str(day)+'\t'+str(int(seq[day]))+'\n')
		day=len(seq)-1
		w1.write(str(sim)+'\t'+str(int(sim_estimateCumCase[sim][day]))+'\n')
	w.close()
	w1.close()

R0_Data_file="posterior_R_Sichuan_2020-02-29_SI7.5_WEEKS1"
Rfinal_Data_file="posterior_R1_Sichuan_2020-02-29_SI7.5_scenario2"

for num_delay_week in range(1,5):
	projection(num_delay_week,R0_Data_file,Rfinal_Data_file)
	print(num_delay_week)





