# # #
# Makefile
#
# History
# -------
# :2012-08-19: initial coding
# :2012-08-21: true make version
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

outdir?=$(dir)makedata#end of the line
inputfile=$(outdir)input.txt#end of the line
globalvar_input=$(outdir)/*/*part*.seq#end of the line
globalvar_output=$(outdir)$(varname)#end of the line
convert2exodus_input=$(globalvar_output)/part*#end of the line
    
all: exodus2seq globalvar convert2exodus
.PHONY: all 

simform-deploy.tar.gz: exopy2.py
	tar czf simform-deploy.tar.gz exopy2.py

preprocess: preprocess.py
	@echo 'Preprocessing...';\
	python preprocess.py $(dir) $(outdir);\
	echo 'Done!'
	
exodus2seq: preprocess mr_exodus2seq_hadoop.py simform-deploy.tar.gz
	@echo 'Converting exodus files to sequence files...';\
	hadoop fs -test -z $(inputfile) || time python mr_exodus2seq_hadoop.py \
	$(inputfile) -r hadoop --python-archive simform-deploy.tar.gz -t $(timesteps) -d $(outdir) --variables $(variables);\
	echo 'Done! All is updated!';\
	hadoop fs -rm $(inputfile)
	
globalvar: mr_globalvar_hadoop.py
	@echo 'Computing the global variance...';\
	hadoop fs -test -e $(globalvar_output) && \
	python check_time.py $(outdir) $(globalvar_output) && \
	hadoop fs -rmr $(globalvar_output);\
	hadoop fs -test -e $(globalvar_output) || \
	time python mr_globalvar_hadoop.py $(globalvar_input) -r hadoop \
	--no-output -o $(globalvar_output) --variable $(variables);\
	echo 'Done! All is updated!'

	
convert2exodus: convert2exodus_download.py simform-deploy.tar.gz
	@echo 'Inserting the global variance to a new exodus file...';\
	time python convert2exodus_download.py $(convert2exodus_input) \
	--template $(template) --output $(output) \
	--tmpdir $(tmpdir)  --varname $(varname) --python-archive simform-deploy.tar.gz;\
	echo 'Done! All is updated'
	
clean:
	@test -e $(tmpdir)tmp && rm -r $(tmpdir)tmp;\
	echo 'Clean Done!'
