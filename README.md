# Alma Patrons Loader

Alma Patrons Loader includes the python and shell scripts required to pre-process patron records in preparation for loading into Ex Libris Alma. An extract of records from the Student Information System (SIS) and Human Resources system (SAP) is uploaded on a daily basis to the Libraries' ftp server. 

Patrons_v1tov2.py removes illegal xml characters from the input file and converts the input file from version 1 to version 2 of the xsd. (see https://developers.exlibrisgroup.com/alma/apis/xsd/external_sys_user.xsd. ) Two files are created for upload to Alma:
prep_employee_changed.xml
prep_student_changed.xml

At Boston University, the python script is run on a scheduled basis using the bash script: patrons.sh. This removes the file from the previous day (with a suffix .old), zips the two files, and moves the xml files into a subdirectory.

After Alma job runs to load the patron records, the zipped file is renamed with a file extension '.old'. In order to give circulation staff an opportunity to resolve any errors in the load, the file is renamed with a zip extension by a bash script: rename_patrons.sh. The Alma job to load patron records is scheduled to run every 6 hours (4:00, 10:00, 16:00, and 22:00). 
