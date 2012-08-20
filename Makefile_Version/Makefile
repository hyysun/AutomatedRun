# # #
# Makefile
#
# History
# -------
# :2012-08-19: initial coding
#
# Example:
#
# make all  dir=hdfs://icme-hadoop1.localdomain/user/yangyang/simform/ \
# 	variables=TEMP varname=Global_Variance \
# 	template=thermal_maze0001.e output=tempglobalvar.e 
#
# Author = 'Yangyang Hou <hyy.sun@gmail.com>'
#
# # # # # # # # #

timesteps=10
tmpdir=./
output=
template=
varname=
variables=

inputfile=$(dir)input.txt#end of the line
outdir=$(dir)/makedata#end of the line
globalvar_input=$(outdir)/*/*part*.seq#end of the line
globalvar_output=$(dir)$(varname)#end of the line
convert2exodus_input=$(globalvar_output)/part*#end of the line
    
all: preprocess exodus2seq globalvar convert2exodus
.PHONY: all 

preprocess: preprocess.py
	@echo 'Preprocessing...';\
	python preprocess.py $(dir);\
	echo 'Done!'

exodus2seq: mr_exodus2seq_hadoop.py exopy2.py
	@echo 'Converting exodus files to sequece files...';\
	time python mr_exodus2seq_hadoop.py $(inputfile) -r hadoop -t $(timesteps) \
	-d $(outdir) --variables $(variables);\
	echo 'Done!';\
	hadoop fs -rm $(inputfile)
	
globalvar: mr_globalvar_hadoop.py
	@echo 'Computing the global variance...';\
	time python mr_globalvar_hadoop.py $(globalvar_input) -r hadoop \
	--no-output -o $(globalvar_output) --variable $(variables);\
	echo 'Done!'
	
convert2exodus: convert2exodus_download.py exopy2.py
	@echo 'Inserting the global variance to a new exodus file...';\
	time python convert2exodus_download.py $(convert2exodus_input) \
	--template $(template) --output $(output) \
	--tmpdir $(tmpdir)  --varname $(varname);\
	echo 'Done!'
	
clean:
	-rm -r $(tmpdir)tmp