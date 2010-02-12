#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re

def get_MTEXT(c5,c8,c10,c20,c40,c41,c71,c72,c1,c7,c50,newlines):
	"""
	create MTEXT string
	"""
	s=r'0\nMTEXT\n5\n%s\n100\nAcDbEntity\n8\n%s\n100\nAcDbMText\n10\n%s\n20\n%s\n40\n%s\n41\n%s\n71\n%s\n72\n%s\n1\n%s\n7\n%s\n50\n%s\n'%(c5,c8,c10,c20,c40,c41,c71,c72,c1,c7,c50)
	if newlines:
		s=s.replace(r'\n','\n').strip()+'\n'
	return s

def fix_beams(f):
	"""
	replace beam text: Δ+9+30/60 -> Δ9 30/60
	"""
	c=r'(.*)'
	s1=get_MTEXT(c,c,c,c,c,c,c,c,r'\{\\f\|b0\|i0\;(.*)\}','beam_prefix_name_beton',     c,False)
	s2=get_MTEXT(c,c,c,c,c,c,c,c,r'\{\\f\|b0\|i0\;(.*)\}','beam_name_beton_upperstruct',c,False)
	s3=get_MTEXT(c,c,c,c,c,c,c,c,r'\{\\f\|b0\|i0\;(.*)\}','beam_name_beton_upperstruct',c,False)
	pat=re.compile('('+s1+s2+s3+')')
	matches=pat.findall(f)
	for i in matches:
		handle   = i[1]
		x0       = i[3]
		y0       = i[4]
		h        = i[5]
		w        = 1.5
		text     = i[9]+i[19]+' '+i[29].strip()
		layer    = 'beam_name_beton_upperstruct'
		angle    = i[10]
		old=i[0]
		new=get_MTEXT(handle,layer,x0,y0,h,w,1,1,text,layer,angle,True)
		f=f.replace(old,new)
		print "replacing : "+text
	return f

def fix_columns(f):
	"""
	replace column text: K+8 -> K8
	"""
	c=r'(.*)'
	s1=get_MTEXT(c,c,c,c,c,c,c,c,r'\{\\f\|b0\|i0\;(.*)\}','column_prefix_name_beton',c,False)
	s2=get_MTEXT(c,c,c,c,c,c,c,c,r'\{\\f\|b0\|i0\;(.*)\}','column_name_beton',       c,False)
	pat=re.compile('('+s1+s2+')')
	matches=pat.findall(f)
	for i in matches:
		handle   = i[1]
		x0       = i[3]
		y0       = i[4]
		h        = i[5]
		w        = 1.5
		text     = i[9]+i[19]
		layer    = 'column_name_beton'
		angle    = i[10]
		old=i[0]
		new=get_MTEXT(handle,layer,x0,y0,h,w,1,1,text,layer,angle,True)
		f=f.replace(old,new)
		print "replacing : "+text
	return f

if __name__ == "__main__":
	# input
	ifilename=raw_input('input  : ')
	try:
		ifile=open(ifilename,'r')
	except:
		raise 'cannot open file'
	f=ifile.read()
	ifile.close()
	
	# fixes
	f=fix_beams(f)
	f=fix_columns(f)
	
	# output
	try:
		ofilename=raw_input('output : ')
	except:
		raise 'cannot open file'	
	ofile=open(ofilename,'w')
	ofile.write(f)
	ofile.close()
	raw_input('press <enter> to exit...')