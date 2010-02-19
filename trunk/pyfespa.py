#! /usr/bin/env python
# -*- coding: utf-8 -*-

# pyfespa - python library for Fespa
# Copyright (C) 2010  F.E. Karaoulanis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# authors: ...

# Each MTEXT entity has 10 arguments.
# i[1]  = subclass marker (Mtext)
# i[2]  = Layer name
# i[3]  = insertion point X
# i[4]  = insertion point Y
# i[5]  = text height
# i[6]  = Reference rectangle width
# i[7]  = Attachment point
# i[8]  = Drawing direction
# i[9]  = Text string
# i[10] = Rotation Angle

from __future__ import print_function
import re
import os

def get_MTEXT(c5,c8,c10,c20,c40,c41,c71,c72,c1,c7,c50,newlines):
    """
    create MTEXT string
    """
    s=r'0\nMTEXT\n5\n%s\n100\nAcDbEntity\n8\n%s\n100\nAcDbMText\n10\n%s\n20\n%s\n40\n%s\n41\n%s\n71\n%s\n72\n%s\n1\n%s\n7\n%s\n50\n%s\n'%(c5,c8,c10,c20,c40,c41,c71,c72,c1,c7,c50)
    if newlines:
        s=s.replace(r'\n','\n').strip()+'\n'
    return s
    
def get_MTEXT_regex(layer):
    """
    Δημιουργεί ένα regex το οποίο ταιριάζει με MTEXT's που ανήκουν
    σε ένα δεδομένο layer.
    """
    c=r'(.*)'
    s=get_MTEXT(c,c,c,c,c,c,c,c,r'\{\\f\|b0\|i0\;(.*)\}',layer,c,False)
    return s
def fix_slabs(f, prefix_layer, element_layer):
    """
    replace slab text: Π+8 -> Π8
    """
    s1=get_MTEXT_regex(element_layer)
    s2=get_MTEXT_regex(prefix_layer)
    pat=re.compile('('+s1+s2+')')
    matches=pat.findall(f)
    for i in matches:
        handle   = i[11]
        x0       = i[13]
        y0       = i[14]
        h        = i[15]
        w        = 1.5
        text     = i[19]+i[9]   
        layer    = element_layer
        angle    = i[10]
        old=i[0]
        new=get_MTEXT(handle,layer,x0,y0,h,w,1,1,text,layer,angle,True)
        f=f.replace(old,new)
        #print ("replacing : ",text)
    return f

def fix_slabs2(f,element_layer):
    """
    replace slab text: h= + 15 -> h=15
    """
    s1=get_MTEXT_regex(element_layer)
    s2=get_MTEXT_regex(element_layer)
    pat=re.compile('('+s1+s2+')')
    matches=pat.findall(f)
    for i in matches:
        handle   = i[1]
        x0       = i[3]
        y0       = i[4]
        h        = i[5]
        w        = 1.5
        text     = i[9]+i[19]
        layer    = element_layer
        angle    = i[10]
        old=i[0]
        new=get_MTEXT(handle,layer,x0,y0,h,w,1,1,text,layer,angle,True)
        f=f.replace(old,new)
        #print ("replacing : ",text)
    return f
def fix_beams(f, prefix_layer, element_layer):
    """
    replace beam text: Δ+9+30/60 -> Δ9 30/60
    """
    s1=get_MTEXT_regex(prefix_layer)
    s2=get_MTEXT_regex(element_layer)
    s3=get_MTEXT_regex(element_layer)
    pat=re.compile('('+s1+s2+s3+')')
    matches=pat.findall(f)
    for i in matches:
        handle   = i[1]
        x0       = i[3]
        y0       = i[4]
        h        = i[5]
        w        = 2.5
        text     = i[9]+i[19]+' '+i[29].strip()
        layer    = element_layer
        angle    = i[10]
        old=i[0]
        new=get_MTEXT(handle,layer,x0,y0,h,w,1,1,text,layer,angle,True)
        f=f.replace(old,new)
        #print ("replacing : ",text)
    return f

def fix_columns(f, prefix_layer, element_layer):
    """
    replace column text: K+8 -> K8
    """
    s1=get_MTEXT_regex(prefix_layer)
    s2=get_MTEXT_regex(element_layer)
    pat=re.compile('('+s1+s2+')')
    matches=pat.findall(f)
    for i in matches:
        handle   = i[1]
        x0       = i[3]
        y0       = i[4]
        h        = i[5]
        w        = 1.5
        text     = i[9]+i[19]
        layer    = element_layer
        angle    = i[10]
        old=i[0]
        new=get_MTEXT(handle,layer,x0,y0,h,w,1,1,text,layer,angle,True)
        f=f.replace(old,new)
        #print ("replacing : ",text)      
    return f

def fixing(f):
    u"""
    Η συνάρτηση αυτή καλεί τις υπόλοιπες συναρτήσεις που διορθώνουν τα αρχεία dxf
    """
    # merging the layers
    f=fix_beams(f, 'beam_prefix_name_beton', 'beam_name_beton_upperstruct')
    f=fix_beams(f, 'beam_prefix_name_beton', 'beam_name_beton_found_shear_wal')
    f=fix_beams(f, 'beam_prefix_name_beton', 'beam_name_beton_foundation')
    f=fix_columns(f, 'column_prefix_name_beton', 'column_name_beton')
    f=fix_slabs(f, 'slab_prefix_name', 'slab_name')
    f=fix_slabs2(f, 'slab_name')	
    
    # replace the letter Φ with the diameter sign
    f=f.replace('Φ'.decode('utf-8').encode('windows-1253'),'%%C')
    
    return f

if __name__ == "__main__":
    s = u"""
----------------------------------------------------------------------------
|Το πρόγραμμα αυτό επεξεργάζεται τα αρχεία dxf που παράγονται από το FESPΑ.|
|                                                                          |
|Στην εισαγωγή του αρχείου εισόδου ΔΕΝ πρέπει να γράφεται η επέκταση       |
|(extension) του αρχείου. Π.χ. "filename" και όχι "filename.tek".          |
|                                                                          |
|Το όνομα του αρχείου εξόδου είναι ίδιο με αυτό του αρχείου εισόδου, με την|
|προσθήκη του "_FIXED" στο τέλος του ονόματος.                             |
|                                                                          |
|Έτσι τα αρχεία που παράχθηκαν από το "filename.tek", δηλαδή τα :          |
|"filename_Or##.dxf" θα γίνουν "filename_Or##_FIXED.dxf"                   |
----------------------------------------------------------------------------
    """
    print(s)            # Printing welcoming string
    
    # Getting the path of the current directory
    path = os.path.abspath('')

    #Getting a list with all the files in the directory
    directory_files = os.listdir(path)

    #Getting the input file base name
    base_name=raw_input("Give the name of the *.tek file : ")

    for file in directory_files:
        if file.startswith(base_name) and file.endswith(".dxf"):
            #Opening reading and closing input file
            try:
                ifile=open(file,'r')
            except:
                raise 'cannot open file'
            f=ifile.read()
            ifile.close()

            # fix dxf file
            f=fixing(f)

            #setting the output file name
            ofilename=file.replace(".dxf","_FIXED.dxf")

            # opening, writing and closing output file
            try:
                ofile=open(ofilename,'w')
            except:
                raise 'cannot open file'
            ofile.write(f)
            ofile.close()

            print("The new file is : ",ofilename)
        else:
            print("The file is not a dxf, or it doesn't start with the specified name.")          
    raw_input('press <enter> to exit...')
