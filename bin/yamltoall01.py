#!/usr/bin/env python3

# Convert a yaml file to LaTeX file
# Usage : 'python3 yamltoall.py toto.yaml'
# Output : create a file toto.tex
# Other format 'python3 yamltoall -f amc toto.yaml' to convert it to 'amc' format


import argparse
import yaml
import sys
import os
import string
import random

#--------------------------------------------------
#--------------------------------------------------
# Arguments 

parser = argparse.ArgumentParser(description='Conversion of mutliple choice questions from yaml to other format (LaTeX by default).')
parser.add_argument('-f', '--format', nargs='?', default='tex', help='output format file')
parser.add_argument('inputfile', help='input yaml filename')
parser.add_argument('outputfile', nargs='?', help='output filename')

options = parser.parse_args()

#print(options.inputfile)
#print(options.outputfile)
#print(options.format)

yaml_file = options.inputfile
output = options.outputfile
output_format = options.format


# OLD Get argument : a yaml file
#yaml_file = sys.argv[1]

 
#--------------------------------------------------
#--------------------------------------------------
# Input file / output file

# Input file name
file_name, file_extension = os.path.splitext(yaml_file) 

# Output file name 
if output:
    output_file = output    # Name given by user
else:
    if output_format == 'tex':
        output_file = file_name+'.tex' # Conversation to .tex extension
    if output_format == 'amc':
        output_file = file_name+'.amc' # Conversation to .amc extension
    if output_format == 'moodle':  # To be done in a near future...
        output_file =  file_name+'.moodle' # Conversation to a xml file with a.moodle extension

# Read all data
stream = open(yaml_file, 'r', encoding='utf-8')
my_data = yaml.load_all(stream)
all_data = list(my_data)



#--------------------------------------------------
#--------------------------------------------------
# Screen output
#for data in all_data:
#    print(data['question'])
#    for answers in data['answers']:
#        print(answers['value'])
#        correct = answers['correct']
#        if correct == True:
#             print("It's true\n")
#        else:    
#             print("It's false\n")  
 
 
#--------------------------------------------------
#--------------------------------------------------
#                   TEX
# Write data to a LaTeX file in our standardized format 
if output_format == 'tex':
  with open(output_file, 'w', encoding='utf-8') as out:
    for data in all_data:
        if 'title' in data.keys():
            out.write('\n\n\\begin{question}['+data['title']+']\n')
        else:
            out.write('\n\n\\begin{question}\n')

        if 'id' in data.keys():
            out.write('\qid{'+str(data['id'])+'}\n')

        if 'author' in data.keys():
            out.write('\qauthor{'+data['author']+'}\n')

        if 'classification' in data.keys():
            out.write('\qclassification{'+data['classification']+'}\n')

        if 'tags' in data.keys():
            out.write('\qtags{'+data['tags']+'}\n')

        if 'type' in data.keys():
            out.write('\qtype{'+data['type']+'}\n')

        if 'keeporder' in data.keys():
            if data['keeporder']:
                out.write('\qkeeporder\n')

        if 'oneline' in data.keys():
            if data['oneline']:
                out.write('\qoneline\n')

        if 'idontknow' in data.keys():
            if data['idontknow']:
                out.write('\qidontknow\n')


        out.write('\n'+data['question']+'\n')

        if 'image' in data.keys():
            dataimage = data['image'][0] 
            print(dataimage)
            if 'options' in dataimage.keys():
                out.write('\\qimage['+dataimage['options']+']{'+dataimage['file']+'}\n\n')
            else:
                out.write('\\qimage{'+dataimage['file']+'}\n\n')     


        out.write('\\begin{answers}\n')    

        for answers in data['answers']:
            value = answers['value']
            value = value.rstrip()  #re.sub('[\s]*$','',text,re.MULTILINE) # Delete potential space at the end
            correct = answers['correct']
            if correct == True:
                out.write('    \\good{'+value+'}\n')
            else:    
                out.write('    \\bad{'+value+'}\n')
     
        out.write('\\end{answers}\n') 

        if 'explanations' in data.keys():
            out.write('\\begin{explanations}\n'+data['explanations']+'\\end{explanations}\n')

        out.write('\\end{question}\n')


#--------------------------------------------------
#--------------------------------------------------
# Random word generator (from stackoverflow)
def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


#--------------------------------------------------
#--------------------------------------------------
#                      AMC
# Write data to a LaTeX file in the format 'amc'
if output_format == 'amc':
  with open(output_file, 'w', encoding='utf-8') as out:
    for data in all_data:
        
        if 'id' in data.keys():
            myid = str(data['id'])
        else:
            myid = id_generator()

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            out.write('\n\n\\begin{question}{'+myid+'}\n\n')
        else:
            out.write('\n\n\\begin{questionmult}{'+myid+'}\n\n')

        if 'author' in data.keys():
            out.write('%Author: '+data['author']+'\n\n')

        if 'classification' in data.keys():
            out.write('%Classification: '+data['classification']+'\n\n')

        if 'tags' in data.keys():
            out.write('%\\tags{'+data['tags']+'.}\n\n')

        if 'title' in data.keys():
            out.write('\\textbf{'+data['title']+'.} ')


        out.write(data['question']+'\n')

        if 'image' in data.keys():
            dataimage = data['image'][0] 
            out.write('\\begin{center}\n')
            if 'options' in dataimage.keys():
                out.write('\\includegraphics['+dataimage['options']+']{'+dataimage['file']+'}')
            else:
                out.write('\\includegraphics{'+dataimage['file']+'}')     
            out.write('\n\\end{center}\n\n')

        if 'oneline' in data.keys() and data['oneline']:
            out.write('\\begin{choiceshoriz}')
        else:
            out.write('\\begin{choices}')

        if 'keeporder' in data.keys() and data['keeporder']:
            out.write('[o]\n')
        else:
            out.write('\n')  

        for answers in data['answers']:
            value = answers['value']
            value = value.rstrip()  #re.sub('[\s]*$','',text,re.MULTILINE) # Delete potential space at the end
            correct = answers['correct']
            if correct == True:
                out.write('    \\correctchoice{'+value+'}\n')
            else:    
                out.write('    \\wrongchoice{'+value+'}\n')

        if 'oneline' in data.keys() and data['oneline']:
            out.write('\\end{choiceshoriz}\n')
        else:
            out.write('\\end{choices}\n')     

        if 'explanations' in data.keys():
            out.write('\explain{'+data['explanations']+'}\n')

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            out.write('\\end{question}\n')
        else:
            out.write('\\end{questionmult}\n')


 
#--------------------------------------------------
#--------------------------------------------------
#                   MOODLE
# Write data to a xml file in a moodle format 

beginmoodle = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
endmoodle = '\n\n</quiz>\n'

if output_format == 'moodle':
  with open(output_file, 'w', encoding='utf-8') as out:

    out.write(beginmoodle)

    for data in all_data:

#        if 'id' in data.keys():
#            myid = str(data['id'])

        if 'type' in data.keys() and ( data['type'] == 'onlyone'  or data['type'] == 'truefalse' ):
            out.write('\n\n<question type="multichoice">\n')
        else:
            out.write('\n\n<question type="multichoice">\n')

        if 'title' in data.keys():
            out.write('<name><text>'+data['title']+'</text></name>\n')
        else: 
            out.write('<name><text> </text></name>\n')

        out.write('<questiontext format="html">\n<text><![CDATA[<p>\n')
        out.write(data['question'])
        out.write('</p>]]></text>\n</questiontext>\n<defaultgrade>1.0</defaultgrade>\n')

        if 'explanations' in data.keys():
            out.write('<generalfeedback format="html"><text><![CDATA[<p>\n')
            out.write(data['explanations'])
            out.write('</p>]]></text></generalfeedback>\n')

        if 'keeporder' in data.keys() and data['keeporder']:
            out.write('<shuffleanswers>0</shuffleanswers>\n')
        else:
            out.write('<shuffleanswers>1</shuffleanswers>\n') 

        out.write('<answernumbering>abc</answernumbering>\n')

#        if 'image' in data.keys():
#            dataimage = data['image'][0] 
#            out.write('\\begin{center}\n')
#            if 'options' in dataimage.keys():
#                out.write('\\includegraphics['+dataimage['options']+']{'+dataimage['file']+'}')
#            else:
#                out.write('\\includegraphics{'+dataimage['file']+'}')     
#            out.write('\n\\end{center}\n\n')

        nbans = 0
        nbgood = 0
        nbbad = 0
        for answers in data['answers']:
            correct = answers['correct']
            nbans += 1
            if correct:
                nbgood += 1
            else:
                nbbad += 1

        goodratio = str("%.5f" % float(100/nbgood))
        badratio = str("%.5f" % float(100/nbbad))


        for answers in data['answers']:
            if answers['correct']:
                out.write('<answer fraction="'+goodratio+'" format="html"><text><![CDATA[<p>\n')
            else:
                out.write('<answer fraction="-'+badratio+'" format="html"><text><![CDATA[<p>\n')
            out.write(answers['value'])
            out.write('</p>]]></text></answer>\n')

#            value = 
#            value = value.rstrip()  #re.sub('[\s]*$','',text,re.MULTILINE) # Delete potential space at the end
#            correct = 
#              correct == True:
#                out.write('    \\correctchoice{'+value+'}\n')
#            else:    
#                out.write('    \\wrongchoice{'+value+'}\n')

        out.write('</question>')

    out.write(endmoodle)
