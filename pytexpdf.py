"""
Module to generate cropped PDFs of LaTeX typeset strings. Example:
>>> import pytexpdf
>>> texPdfEnv = pytexpdf.PyTexPdf()
>>> texPdfEnv.UsePackage("amsmath")
>>> texPdfEnv.MakeTexPdf(r"howdy \int \, \mathrm{d}x")
>>> texPdfEnv.MakeTexPdf("howdy $\\int \\, \\mathrm{d}x$", fileName="blurb", isEqn=False)
"""

import os.path # because it's special
from os import system, remove
from sys import platform
from warnings import warn

class PyTexPdf:
	"""Generate cropped PDFs of LaTeX typeset equations."""
	def __init__(self):
		"""Initializes object, holds package list"""
		self.packages = ""

	def UsePackage(self, package: str):
		"""Tell LaTeX to use a package."""
		self.packages = self.packages + "\\usepackage{" + package + "}\n"

	def MakeTexPdf(self, texString: str, fileName="pytexpdf", isEqn=True) -> str:
		"""
		Takes a TeX string, generates a .pdf from it, and returns the name of the .pdf file. If filename not given, it will generate its own. Assumes the TeX string is supposed to be an equation.
		"""
		tex = ".tex"
		pdf = ".pdf"

		self._CheckTex()

		if fileName == "pytexpdf":
			# Make new file names up until pytexpdf9 otherwise it will clog the user's directory
			count = 0
			badName = True
			while badName:
				fileName = "pytexpdf" + str(count)
				if os.path.exists(fileName + tex) or os.path.exists(fileName + pdf):
					badName = True
					count += 1
				else:
					badName = False

				if count > 9:
					raise Exception("Path has too many .tex and .pdf files starting with 'pytexpdf' :-(")

		file = open(fileName + tex, "w")
		file.write("\\documentclass[border=1pt]{standalone}\n")
		file.write(self.packages + "\n")
		file.write("\\begin{document}\n")
		if isEqn:
			file.write("$\\displaystyle\n")
		file.write(texString + "\n")
		if isEqn:
			file.write("$\n")
		file.write("\\end{document}\n")
		file.close()
		system("pdflatex -interaction=nonstopmode \"" + fileName + ".tex\"")
		remove(fileName + tex)
		remove(fileName + ".aux")
		remove(fileName + ".log")

		if os.path.exists(fileName + pdf):
			return fileName + pdf
		else:
			raise Exception("Could not generate TeX .pdf :-(")

	@staticmethod
	def _CheckTex() -> bool:
		"""Checks if user has pdflatex at predicted location"""
		pdflatex = True
		if "darwin" in platform:
			if not os.path.exists("/Library/TeX/texbin/pdflatex"):
				warn("Missing pdflatex at /Library/TeX/texbin/pdflatex :-(")
				pdflatex = False
		elif "linux" in platform:
			if not os.path.exists("/usr/bin/pdflatex"):
				warn("Missing pdflatex at /usr/bin/pdflatex :-(")
				pdflatex = False
		else:
			warn("Your platform is not supported :-(")
			pdflatex = False
		return pdflatex
