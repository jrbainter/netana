#!/usr/bin/env python3
from tkinter import *
import math,cmath,time
from tkinter.messagebox import showerror
from disreport import DisReport
from matutil import insertmat, evalmat


class MkReport():
	""" class MkReport is a continuation of the NetAna application.
	This part writes the output results for both the AC and DC analysis.
	"""
	def __init_(self,parent):
		self.parent = parent

	def mkreport(self):
		try:
			if not isinstance(self.NetDict['VG'],float):
				raise TypeError
		except TypeError:
			self.showerror('Error','VG must be of type float')

		self.AcDc = 'DC'
		for key in self.NetDict:
			if key[0] in ['L','C']: self.AcDc='AC'


		# Start evaluating equations
		with open(self.ReportFile, 'w', encoding='utf-8') as self.ofile:
			self.matvalues = self.EvalEqu(self.Mat)   # Convert Equation string to values
			print ("# Analysis Created by 'NetAna'.", file=self.ofile)
			when = time.ctime()
			lend = "\n# Date Created: "+when+"\n#\n\n"
			if self.AcDc == 'AC':
				if self.AnalType == 'Node':
					# AC Node Analysis
					print("# AC Node Analysis of file: {:s}".format(self.FileName), file=self.ofile)
					print("# Report file created: {:s} {:s}".format(self.ReportFile, lend), file=self.ofile)
					self.DoACAnalysis('IG')
				else:
					# AC Mash Analysis
					print("# AC Mash Analysis of file: {:s}".format(self.FileName), file=self.ofile)
					print("# Report file created: {:s} {:s}".format(self.ReportFile, lend), file=self.ofile)
					self.DoACAnalysis('VG')
			else:
				if self.AnalType == 'Node':
					# DC Node Analysis
					print("# DC Node Analysis of file: {:s}".format(self.FileName), file=self.ofile)
					print("# Report file created: {:s} {:s}".format(self.ReportFile, lend),file=self.ofile)
					self.DoDCAnalysis('IG')
				else:
					# DC Mash Analysis
					print("# DC Mash Analysis of file: {:s}".format(self.FileName), file=self.ofile)
					print("# Report file created: {:s} {:s}".format(self.ReportFile, lend), file=self.ofile)
					self.DoDCAnalysis('VG')

		self.ofile.close() # done writing to output file
		# Show Report
		DisReport(self.parent, self.ReportFile)

	def DoACAnalysis(self,source='VG'):
		if source == 'VG':
			uLab = 'i'
			dLab = 'Amps'
		else:
			uLab = 'e'
			dLab = 'Volts'

		if 'IGLIST' in self.NetDict :
			m = self.NetDict['IGLIST']
		elif 'VGLIST' in self.NetDict:
			m = self.NetDict['VGLIST']
		else:
			#m = bldmat(1,self.Nodes,0)
			# Build list of of zeros, one per Node
			m = [0]*self.Nodes
			# Input 'VG' or 'IG'
			m[0] = self.NetDict[source]

		print('##### Units = {:s} {:s}'.format(dLab, '####\n'), file=self.ofile)
		try:
			fstart, fstop, finc, flab = self.NetDict['FREQ']
		except:
			self.showerror("Error",'"FREQ" not defined!')
		else:
			# Save the Component values in a separate dictonary XCompDict
			self.SaveCompValues()
			# Print Header
			self.FreqUnits = flab # Save freq. units
			s1 = " "*7; s2= " "*4
			print('# Frequency({:s}){:s}Magnitude(db){:s}Phase Angle(deg)'.format(flab,s1,s2), file=self.ofile)
			Tauj = 2*math.pi*1j
			for freq in self.genfreq(fstart, fstop, finc):
				print("{:10.2f}".format(freq), file=self.ofile, end="")
				tox = Tauj*freq
				for n in range(self.Nodes):   # Do all nodes
					# Convert reactive components to reactances
					for key in self.XCompDict:
						if key[0] in ['L','C']:
							self.NetDict[key] = self.XCompDict[key] * tox
					# Convert Equation string to values
					self.matvalues = self.EvalEqu(self.Mat)
					# Solve for all voltages or currents.
					determ = insertmat(self.matvalues,m,n)
					num = evalmat(determ)
					dem = evalmat(self.matvalues)
					res = num/dem
					res_key = uLab.upper()+str(n+1)
					self.NetDict[res_key] = res


				# Now finished nodes for this frequency
				# Get User Transfer Function and Evaluate it.
				try:
					stf = self.NetDict['TF']
				except:
					self.showerror("Error",'Transfer Function "TF" not defined!')
					break
				else:
					tf = eval(stf,{},self.NetDict)
					# See if tf is near or eq zero
					# if it is set it to small value
					if abs(tf) < 1.0e-6: tf = complex(1.0e-30, 0.0)
					mag = 20.0*math.log10(abs(tf))
					angle = math.degrees(cmath.phase(tf))
					print("{:+20.4f}{:+20.4f}".format(mag, angle ),\
						file=self.ofile)


	def DoDCAnalysis(self,source='VG'):
		if source == 'VG':
			uLab = 'i'
			dLab = 'Amps'
		else:
			uLab = 'e'
			dLab = 'Volts'

		if 'IGLIST' in self.NetDict :
			m = self.NetDict['IGLIST']
		elif 'VGLIST' in self.NetDict:
			m = self.NetDict['VGLIST']
		else:
			#m = bldmat(1,self.Nodes,0)	# Build Matrix
			# Build list of of zeros, one per Node
			m = [0]*self.Nodes
			m[0] = self.NetDict[source]

		dem = evalmat(self.matvalues)
		print('#### Units ={:s} {:s}'.format(dLab,'####\n'), file=self.ofile)
		for n in range(self.Nodes):
			determ = insertmat(self.matvalues,m,n)
			num = evalmat(determ)
			res = num/dem
			reskey = uLab.upper()+str(n+1)
			self.NetDict[reskey] = res
			print('{:s}{:d} = {:g}'.format(uLab,n+1,res), file=self.ofile)

		# Write GOALS to Report File
		if 'GOALS' in self.NetDict:
			print(file=self.ofile)	# Write one \n
			for goalnb in range(self.NetDict['GOALS']):
				goalkey = 'GOAL'+ str(goalnb+1)
				goal_result = eval(self.NetDict[goalkey][0],self.NetDict,self.NetDict)
				# Add goal result to dict for goal chaining
				gres = 'GR' + str(goalnb+1)
				self.NetDict[gres] = goal_result
				gUnit = self.NetDict[goalkey][1]
				print('#{:s} = {:g} {:s}\t{}'.format(goalkey, goal_result,\
				 gUnit, self.NetDict[goalkey] ), file=self.ofile)

		self.ofile.close()

		# Display Report
		DisReport(self.parent, self.ReportFile)

	def EvalEqu(self,equ):
		""" Converts the equation strings to numeric values
		by using the function 'eval' on the strings."""
		res = []
		for r in range(len(equ)):
			temp = []
			for c in range(len(equ)):
				try:
					temp.append(eval(equ[r][c],self.NetDict,self.NetDict))
				except:
					self.showerror("error","Equation Syntax Error row = {:s} col = {:s}".format(r,c))
			res.append(temp)
		return res

	def SaveCompValues(self):
		for key in self.NetDict:
			if key[0] in ['L','C']:
				self.XCompDict[key] = self.NetDict[key]


	def genfreq(self,start,stop,inc):
		""" This method returns the next number in a sequence
		using the Python "yield" statment in order to return one value
		at a time instead of a list all at once.
		call:  genfreq(start, stop, increment)
		"""
		freq = start
		while freq < stop:
			yield freq
			freq += inc

