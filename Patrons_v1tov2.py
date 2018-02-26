###
### Convert Patrons file incoming from IS&T in a version 1 schema to a version 2 schema
### written by J Ammerman
### October 9, 2015
###

# coding: utf-8
# requires python 3.x

## load required modules
import codecs
import os
import xml.etree.ElementTree as ET
import glob
from zipfile import ZipFile
from xml.dom import minidom
import csv

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_user_details(u,user):
    u_dict = {}
    u_dict['recordType'] = 'record_type'
    u_dict['userName'] = 'primary_id'
    u_dict['firstName'] = 'first_name'
    u_dict['middleName'] = 'middle_name'
    u_dict['lastName'] = 'last_name'
    u_dict['userGroup'] = 'user_group'
    u_dict['campusCode'] = 'campus_code'
    u_dict['expiryDate'] = 'expiry_date'
    u_dict['purgeDate'] = 'purge_date'
    u_dict['userType'] = 'account_type'
    u_dict['userTitle'] = 'user_title'
    u_dict['defaultLanguage'] = 'preferred_language'
    full_name = ET.SubElement(user,'full_name')
    for i in u.findall('userDetails'):
        for d in i:
            if d.tag == 'firstName':
                fname = d.text
            if d.tag == 'middleName':
                if d.text == None:
                    mname = ' '
                else:
                    mname = ' ' + d.text + ' '
            if d.tag == 'lastName':
                lname = d.text
            if d.tag in u_dict:
                d.tag = u_dict[d.tag]
            if d.tag == 'record_type':
                d.text = 'PUBLIC'
                d.set('disc','Public') 
            if d.tag == 'status':
                d.text = d.text.upper()
                d.set('disc',d.text.title())
            if d.tag == 'expiry_date' or d.tag == 'purge_date':
                date = d.text
                d.text = date[:4] + '-'+ date[4:6] + '-' + date[-2:] + 'Z'
            e = ET.SubElement(user,d.tag)
            e.text = d.text
            if e.tag == 'user_group':
                e.set('desc',user_groups[e.text])
        name = fname + mname + lname
        full_name.text = name
        #print(name)

          
def add_notes(u,user):
    for i in u.findall('userNoteList'):
        for d in i:
            e = ET.SubElement(user,d.tag)
            e.text = d.text

def add_identifiers(u,user):
    for i in u.findall('userIdentifiers'):
        UIs = ET.SubElement(user,'user_identifiers')
        for d in i:
            e = ET.SubElement(UIs,'user_identifier')
            for child in d:
                f = ET.SubElement(e,child.tag.replace('type','id_type'))
                f.text = child.text

def add_contacts(u,user):
    u_dict = {}
    u_dict['stateProvince'] = 'state_province'
    u_dict['addressNote'] = 'address_note'
    u_dict['postalCode'] = 'postal_code'
    u_dict['startDate'] = 'start_date'
    u_dict['endDate'] = 'end_date'
    u_dict['phone'] = 'phone_number'
    u_dict['email'] = 'email_address'
  
    for i in u.findall('userAddressList'):
        contact_info = ET.SubElement(user,'contact_info')
        addresses = ET.SubElement(contact_info,'addresses')
        emails = ET.SubElement(contact_info,'emails')
        phones = ET.SubElement(contact_info,'phones')

        for d in i:
            if d.tag == 'userAddress':
                address = ET.SubElement(addresses,'address')
                address.set('segment_type','External')
                address.set('preferred','true')
                for child in d:
                    if child.tag == 'segmentAction':
                        pass
                    elif child.tag == 'types':
                        address_types = ET.SubElement(address,'address_types') 
                        for x in child.findall('userAddressTypes'):
                            address_type = ET.SubElement(address_types,'address_type')
                            address_type.text = x.text
                            if x.text == 'work':
                                address_type.set('desc', 'Work')
                            if x.text == 'home':
                                address_type.set('desc', 'Home')
                            if x.text == 'school':
                                address_type.set('desc', 'School')                            
                    else:
                        if child.tag in u_dict:
                            child.tag = u_dict[child.tag]
                        f = ET.SubElement(address,child.tag)
                        f.text = child.text
                        if f.tag == 'line1' and f.text == None:
                            addresses.remove(address)
                            break
            if d.tag == 'userPhone':
                phone = ET.SubElement(phones,'phone')
                phone.set('segment_type','External')
                phone.set('preferred','true')
                #phone.set('preferredSMS', 'false')
                for child in d:
                    if child.tag == 'segmentAction':
                        pass
                    elif child.tag == 'types':
                        phone_types = ET.SubElement(phone,'phone_types') 
                        for x in child.findall('userPhoneTypes'):
                            phone_type = ET.SubElement(phone_types,'phone_type')
                            phone_type.text = x.text
                            if x.text == 'office':
                                phone_type.set('desc', 'Office')
                            if x.text == 'work':
                                phone_type.set('desc', 'Work')
                            if x.text == 'home':
                                phone_type.set('desc', 'Home')
                            if x.text == 'school':
                                phone_type.set('desc', 'School')                            
                    else:
                        if child.tag in u_dict:
                            child.tag = u_dict[child.tag]
                        f = ET.SubElement(phone,child.tag)
                        f.text = child.text
                        if f.text == None:
                            phones.remove(phone)
                            #print('No Phone')
            if d.tag == 'userEmail':
                pass
                email = ET.SubElement(emails,'email')
                email.set('segment_type','External')
                email.set('preferred','true')
                for child in d:
                    if child.tag == 'segmentAction':
                        pass
                    elif child.tag == 'types':
                        email_types = ET.SubElement(email,'email_types') 
                        for x in child.findall('userEmailTypes'):
                            email_type = ET.SubElement(email_types,'email_type')
                            email_type.text = x.text
                            if x.text == 'office':
                                email_type.set('desc', 'Office')
                            if x.text == 'work':
                                email_type.set('desc', 'Work')
                            if x.text == 'home':
                                email_type.set('desc', 'Home')
                            if x.text == 'school':
                                email_type.set('desc', 'School')                            
                    else:
                        if child.tag in u_dict:
                            child.tag = u_dict[child.tag]
                        f = ET.SubElement(email,child.tag)
                        f.text = child.text  
                        if f.text == None:
                            p_id = user.find('primary_id')
                            f.text = p_id.text+'@bu.edu'
                            #print(p_id.text+'@bu.edu')
                        


#os.chdir('/Volumes/jwa_drive1/git/patrons')
file_list = glob.glob('patrons*.xml')
##
## Here we get the list of user group codes and descriptions to read into a dictionary
## to enhance the records with the description
reader = csv.DictReader(open('user_groups.csv'))
user_groups = {}
for row in reader:
    key = row.pop('Code')
    if key in user_groups:
        # implement your duplicate row handling here
        pass
    user_groups[key] = row['Description']

for f in file_list:
    out_file = codecs.open('prep_'+ f[8:],'w','utf-8')
    users = ET.Element('users')
    xml_str = codecs.open(f,'rb', 'Windows-1252').read()
    xml_str = xml_str.replace('\u0007','').replace('\u001a','').replace('\u0016','')
    xml_str = xml_str.replace('use:','').replace('xmlns:use="http://com/exlibris/digitool/repository/extsystem/xmlbeans" xsi:schemaLocation="http://com/exlibris/digitool/repository/extsystem/xmlbeans user_012513.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"','')
    root = ET.fromstring(xml_str)
    for child in root:
        user = ET.SubElement(users, 'user')
        add_user_details(child,user)
        #add_notes(child,user)
        add_identifiers(child,user)
        add_contacts(child,user)

    out_file.write(prettify(users))
    out_file.close()
        
file_list = glob.glob('prep*.xml')
for f in file_list:
    with ZipFile('patrons.zip','a') as myzip:
        myzip.write(f)
myzip.close()


