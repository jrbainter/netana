#!/bin/env python3

from tkinter import *
from tkinter import ttk

import tkinter.filedialog as tfd
import webbrowser,os,sys,shutil
from importlib_resources import files

from analize import AnalizeSpec
from equations import Equations
from mkreport import MkReport
from plotutil import matplot


class NetAna(Equations, AnalizeSpec, MkReport):
	def __init__(self, master):
		self.opt = options = {}
		options['defaultextension']='.txt'
		options['filetypes']=[('text files', '.txt')]
		options['parent']=master
		options['title']='Get File Name'
		options['initialdir'] = os.path.expanduser('~')+'/netana-examples'
		self.bld_menu(master)
		self.bld_widgets(master)
		self.parent=master
		self.freg = []
		self.lmag = []
		self.lpa = []
		self.plotdata = []

	def bld_menu(self, master):
		mBar = Menu(master, relief='groove', borderwidth=5)
		filemenu = Menu(mBar, tearoff=0)
		filemenu.add_command(label='SpecFile', underline=0,
			command = self.getspecfn)
		filemenu.add_separator()
		filemenu.add_command(label='Exit',
			underline=0, command=master.destroy)
		mBar.add_cascade(label='File', menu=filemenu)
		helpmenu = Menu(mBar, tearoff=0)
		helpmenu.add_command(label='Doc', underline=0, command=self.helpdoc)
		helpmenu.add_command(label='About', underline=0, command=self.about)
		mBar.add_cascade(label='Help', menu=helpmenu)
		master.config(menu=mBar)

	def bld_widgets(self, master):
		title = ttk.Style()
		title.configure("RED.TLabel", font ='times 18 normal italic', foreground='red' )
		fm = ttk.Frame(master)
		ttk.Label(fm, text="Network Analizer", style="RED.TLabel").grid(sticky=N, pady=10)
		fm.pack()
		fm1 = Frame(master)
		self.fnbtn=ttk.Button(fm1,text='Enter Spec. File Name', command=self.getspecfn)
		self.fnbtn.grid(row=0,column=0, sticky=E+W,padx=5,pady=5)
		self.equbtn=ttk.Button(fm1,text='Enter Network Equations', command=self.getequations)
		self.equbtn.grid(row=0, column=1, sticky=E+W,padx=5,pady=5)

		self.analbtn=ttk.Button(fm1,text='Analize Network',command=self.mkreport)
		self.analbtn.grid(row=1,column=0, sticky=E+W,padx=5,pady=5)
		self.plotbtn=ttk.Button(fm1,text='Plot Network Results',command=self.plot)
		self.plotbtn.grid(row=1, column=1, sticky=E+W,padx=5,pady=5)

		self.Quit=ttk.Button(fm1, text='Quit', command=fm1.quit)
		self.Quit.grid(row=2,column=0, sticky=W,padx=5,pady=5)
		fm1.pack(anchor=W)
		master.bind_all('<F1>',self.helpdoc)
		# Set default button state
		self.btnctrl(['!disabled','disabled','disabled','disabled'])


	def getspecfn(self):
		file=tfd.askopenfilename(**self.opt)
		self.FileName=file
		self.ProjectName=os.path.basename(file)
		self.BaseFileName=file[:-4]
		self.EquFileName = self.BaseFileName + '.equ'
		self.ReportFile= self.BaseFileName + '.report'
		self.NetFileName = self.BaseFileName + '.net'
		self.Nodes=0
		self.AcDc=''
		self.AnalType=''
		self.FreqUnits=''
		self.Mat=[]
		self.NetDict={}
		self.XCompDict={}
		self.btnctrl(['disabled','!disabled','disabled','disabled'])

	def getequations(self):
		AnalizeSpec.analize(self)
		Equations.getequ(self)
		self.btnctrl(['disabled','disabled','!disabled','disabled'])

	def mkreport(self):
		MkReport.mkreport(self)
		self.btnctrl(['disabled','disabled','disabled','!disabled'])

	def plot(self):
		if  self.AcDc == "AC" :   # Plot AC Response
			ylabel = ''
			self.plotdata = [self.ProjectName,self.lfreq, self.lmag, self.lpa]
			matplot(self.FreqUnits,ylabel,self.plotdata)
		else:  # Plot DC Response
			if self.AnalType == 'Node':
				ylabel = 'Volts'
			else:
				ylabel = 'Amps'
			self.plotdata = [self.ProjectName,self.lmag]
			units = ""
			matplot(units,ylabel,self.plotdata)
		self.btnctrl(['!disabled','disabled','disabled','!disabled'])

	def helpdoc(self,event=None):
		fp = str(files("netana").joinpath("doc/NetAnaDoc.html"))
		firefox_browser = webbrowser.get('firefox')
		webbrowser.open(fp)

	def about(self,event=None):
		fp = str(files("netana").joinpath("doc/about.html"))
		firefox_browser = webbrowser.get('firefox')
		webbrowser.open(fp)

	def btnctrl(self,blist):
		assert len(blist) == 4
		self.fnbtn.state([blist[0]])
		self.equbtn.state([blist[1]])
		self.analbtn.state([blist[2]])
		self.plotbtn.state([blist[3]])

	def main():
		root = Tk()
		root.title('NetAna')
		# Center window on screen
		width = root.winfo_screenwidth()
		height = root.winfo_screenheight()
		root.geometry(f'+{width//2}+{height//3}')
		root.resizable(False,False)
		app = NetAna(root)
		root.mainloop()


	def cpdir():
		""" Define the source directoy and the destination directory
		    (userr's home directory). Copy 'netana-examples' to users
			home directory if it does not already exist.
		"""
		source_dir = 'netana-examples'
		dest_dir = os.path.expanduser('~') + '/' + source_dir
		# Coyy the directory if it does not exist in users home directory
		if not os.path.exists(dest_dir):
			shutil.copytree(source_dir, dest_dir)


if __name__ == "__main__":
	from netana import NetAna
	p1 = NetAna()
	# copy netana-examples dir to Home dir
	p1.cpdir()
	# start gui
	p1.main()

