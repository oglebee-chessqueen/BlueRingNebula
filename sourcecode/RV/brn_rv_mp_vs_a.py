'''
		Determine companion mass for TYC 2597-735-1 using known RV shift
		and variable radii from CS

		RV Equation:
									 M_star    (v_star sin(i))
						M_p =  ------ x ------------------
									 sin(i)   sqrt(G M_star / a)

		K. Hoadley - 12 March 2020
'''

import numpy
import matplotlib.pyplot as plt
from matplotlib import rc
params = {'legend.fontsize': 20,
          'figure.figsize': (6,8), 	#(15, 5),
         'axes.labelsize': 30,
         'axes.titlesize': 30,
         'xtick.labelsize':24,
         'ytick.labelsize':24}
plt.rcParams.update(params)
plt.rcParams["font.family"] = "Times New Roman"
rc('font', weight='bold')
rc('axes', linewidth=2)



# Define variables and constants here
G = 6.674e-8				# Grav constant; cm^3 g^-1 s^-2
R_sun = 6.96e+10		# Solar radius; cm
M_sun = 1.99e+33		# Solar mass; g
c = 2.99792458e+10	# speed of light; cm/s
au2cm = 1.496e+13		# Astronomical unit; cm
m2cm = 1.0e2				# conversion: meters -> cm
km2cm = 1.0e5				# conversion: km -> cm
M_Jup = 1.898e+30		# Jupiter masses; g
M_BD_min = 13*M_Jup		# Brown dwarf, min mass
M_BD_max = 80*M_Jup		# Brown dwarf, max mass
v_brn = 400.*km2cm		# Ejecta velocity, mim
M_brn = 0.01*M_sun		# Mass ejected in BRN from TYC 2597-735-1 from merger
E_brn_min = M_brn*v_brn*v_brn*0.5		# minimum energy required to eject BRN
print E_brn_min

# Find Delta(Energy) released by having a companion spiral in from infinity to a = 0.1AU
# Expression: dE = (1.0E45 erg)*(Mp/10 MJ)*(a/0.1AU)
# -> Mp = E_brn_min * (0.1 AU/a) * 10 MJ / (1.0E45) ~ 10*E_brn_min / 1.0E45
Mp_brn_min = 10.*E_brn_min / (1.0E45)
print Mp_brn_min

vsini = 199.*m2cm		# RV of star; m/s -> cm/s, measured by Keck/HIRES + HET/HPF
i = 15.0						# Assumed inclination angle we are vieing TYC; degrees
M_star = 2.*M_sun		# Mass of TYC; solar masses -> g
R_star = 10.*R_sun	# Radius of TYC; solar radii -> cm

# Semi-major axis of companion, assuming RV period (13.7 days)
a_p = 0.1	#numpy.logspace(amin, amax, num=10, endpoint=True, base=10.0)

# Ranges of semi-major axes for plot
amin = 0.005		# 1 Rsun
amax = 500.			# AU
a = numpy.logspace(amin, amax, num=500, endpoint=True, base=10.0)


# Find possible Mp values: no sini dependence, this is smallest mass expected
Mp = M_star * ( vsini / ( numpy.sqrt( (G * M_star)/( a_p*au2cm) ) ))

Mpsini = Mp / numpy.sin(i * 3.14/180)		# with inclination taken into account

#~ # Plot
#~ print Mp/M_Jup		# g
#~ print
#~ print Mpsini/M_Jup	# solar mass

#Plot
fig = plt.figure(figsize=(9,9))
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel(r'a (AU)',weight='bold')
ax1.set_ylabel(r'M$_{c}$ (M$_{J}$)',weight='bold')
ax1.set_xlim([0.005,10])	#amax])
ax1.set_ylim([0.5,500])
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.xaxis.set_tick_params(width=3, length=8, direction='in', which='both')
ax1.yaxis.set_tick_params(width=3, length=8, direction='in', which='both')

#~ plt.plot(numpy.log10(a_p), Mp/M_Jup, linestyle='dashed', lw=5, color='blue',
				 #~ label=r'$sin i$ = 90$^{\circ}$')
#~ plt.plot(numpy.log10(a_p), Mpsini/M_Jup, linestyle='solid', lw=5, color='blue',
				 #~ label=r'$sin i$ = 15$^{\circ}$')
#~ ax1.fill_between(numpy.log10(a_p), Mp/M_Jup, Mpsini/M_Jup, color='blue',
								 #~ alpha=0.25)#, label=r'Possible mass range')
#~ plt.text(0.075, 20, r"Companion Mass Range", rotation=34., fontsize="xx-large",
				 #~ weight='bold', color='darkblue')

plt.plot([a_p,a_p], [Mp/M_Jup, Mpsini/M_Jup], lw=10, color='blue')#,
				 #label=r'Companion Mass Range with P=13.7d')
plt.text(0.125, 6, r"M$_c$ Range", rotation=0., fontsize=22,
				 weight='bold', color='blue')

ax1.errorbar([a_p,a_p], [Mp_brn_min,Mp_brn_min], yerr=[100,100], lw=5, capsize=8, capthick=2, color='purple',
							lolims='True')#,label=r'Min M$_c$ required to eject BRN')
plt.text(0.125, 250, r"Min M$_c$ to eject BRN", rotation=0., fontsize=22,
				 weight='bold', color='purple')

plt.legend()

# Outer radius of TYC
plt.axvline(R_star/au2cm, color='forestgreen', lw=2)
plt.axvspan(0.005, R_star/au2cm, facecolor='lightgreen', alpha=0.4, hatch='//', edgecolor='forestgreen')
#~ plt.text(0.03, 0.3, r"R$_{\star}$", rotation=90., fontsize="xx-large",
				 #~ weight='bold', color='forestgreen')
plt.text(0.0125, 300, r"R$_{\star}$", rotation=0., fontsize=24,
				 weight='bold', color='forestgreen')

plt.axhline(M_Jup/M_Jup, lw=5, color='darkorange')		# Jupiter mass
plt.text(3, 1.15, r"1 M$_{J}$", rotation=0., fontsize=24,
				 weight='bold', color='darkorange')
#~ plt.text(25, 1.1, r"M$_{Jupiter}$", rotation=0., fontsize="xx-large",
				 #~ weight='bold', color='darkorange')
# Brown dwarf mass limits
plt.axhspan(M_BD_min/M_Jup, M_BD_max/M_Jup, color='gold', alpha=0.25)
plt.text(3, 60, r"M$_{BD}$", rotation=0., fontsize=24,
				 weight='bold', color='darkgoldenrod')

plt.axhline(0.1*M_sun/M_Jup, lw=5, color='crimson')		# 0.1M_sun star
plt.text(3, 115, r"0.1M$_{\odot}$", rotation=0., fontsize=24,
				 weight='bold', color='crimson')
#~ plt.text(25, 110, r"0.1 M$_{\odot}$", rotation=0., fontsize="xx-large",
				 #~ weight='bold', color='crimson')

plt.show()
