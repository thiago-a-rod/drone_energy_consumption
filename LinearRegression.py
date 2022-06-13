import numpy as np 
import pandas as pd
from scipy.stats import t
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib


def linear_regression(df,x):
	tk_x = df[x]
	tk_y = df['Power_takeoff']

	cr_x = df[x]
	cr_y = df['Power_cruise']

	ld_x = df[x]
	ld_y = df['Power_landing']

	tk_b0, tk_b1, tk_pvalue, tk_Rsq = cal_coefficients(tk_x, tk_y)
	cr_b0, cr_b1, cr_pvalue, cr_Rsq = cal_coefficients(cr_x, cr_y)
	ld_b0, ld_b1, ld_pvalue, ld_Rsq = cal_coefficients(ld_x, ld_y)

	df_coefficients = pd.DataFrame([],columns = ['regime','b1','b0','p_value','R_sq'])
	df_coefficients.loc[0] = ['takeoff', tk_b1,tk_b0,tk_pvalue,tk_Rsq]
	df_coefficients.loc[1] = ['cruise', cr_b1, cr_b0, cr_pvalue, cr_Rsq]
	df_coefficients.loc[2] = ['landing', ld_b1, ld_b0, ld_pvalue, ld_Rsq]

	df_coefficients.set_index('regime', inplace=True)
	return df_coefficients


def cal_coefficients(x,y):
	xbar = x.mean()
	ybar = y.mean()
	n = len(x)
	Sxx = ((x - xbar)**2).sum()
	Sxy = ((x - xbar)*(y-ybar)).sum()


	b1 = Sxy/Sxx
	b0 = ybar - b1*xbar

	SStot = ((y - ybar)**2).sum()
	SSreg = b1**2 * Sxx
	SSerr = SStot - SSreg

	Rsq = SSreg/SStot
	s = np.sqrt(SSerr/(n-2))

	t_b1 = b1/(s/np.sqrt(Sxx))
	degF = n-2
	tcdf = t.cdf(t_b1, degF, loc=0, scale=1)
	#print(t_b1)
	if b1 < 0:
		pvalue = 2*(tcdf)
	else:
		pvalue = 2*(1-tcdf)

	return b0,b1,pvalue,Rsq
