#!/usr/bin/python

import os, sys, subprocess
import argparse

parser = argparse.ArgumentParser(description="Extracts the abstract from PAPER.tex and builds it into a PDF without hyphenation. Allows for easy copy-pasting when a plain text abstract is needed (e.g., HotCRP).")

parser.add_argument('paper', metavar="PAPER.tex", nargs=1,
                    help='LaTeX file for the paper')
#parser.add_argument("-o", "--output-dir", dest="outputDir", default="abstract", \
#                  help="The extracted abstract will be rendered into a PDF in this directory.")

args = parser.parse_args()

stringsToIgnore = [
    "\usepackage[english]{babel}", # TODO: this should be a regex instead
    "\usepackage[autostyle,english=american]{csquotes}", # TODO: this should be a regex instead
    "\MakeOuterQuote{\"}",
    "\usepackage{flushend}",
    "\input"]

addedNohypenPackage = False
out_lines = []
for l in open(args.paper[0], 'r'):
    if not addedNohypenPackage and l.count(r'\usepackage') > 0:
        # this package disables hyphenation
        out_lines.append(r'\usepackage[none]{hyphenat}')
        # l gets added to out_lines below
        addedNohypenPackage = True
        pass
    ignoreLine = any([s for s in stringsToIgnore if l.count(s) > 0])
    if ignoreLine:
        continue
    if l.count(r'\end{abstract}') > 0:
        out_lines.append(l)
        break
    
    out_lines.append(l)
    pass

out_lines.append( r'\maketitle' )
out_lines.append( r'\end{document}' )

# NB: using an output directory doesn't work because we need to copy the .cls
# file over, and potentially lots of other files as well...

# # create output directory (if needed)

# if not os.path.isdir(args.outputDir):
#     os.makedirs(args.outputDir)

# os.chdir(args.outputDir)
    
# write out abstract to a file

abstractFile = "extracted-abstract.tex"
abstractTex = open(abstractFile, "w")
abstractTex.writelines(out_lines)
abstractTex.close()

# compile abstract to pdf
subprocess.check_call("latexmk -pdf "+abstractFile, shell=True)

print
print "Abstract can be copy-pasted from", abstractFile.replace('.tex','.pdf')

