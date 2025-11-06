from archivesspace import archivesspace
import argparse
import logging
import csv
import pprint
import json

def record_agent_list(agents):
    agent_list = []
    for agent in agents:
        if agent['role'] != 'subject':
            agent_record = aspace.get(agent['ref'])
            agent_name = agent_record['title']
            if agent_record['agent_type'] == 'agent_person':
                agent_type = 'person'
            elif agent_record['agent_type'] == 'agent_corporate_entity':
                agent_type = 'corporate_body'
            else:
                agent_type = 'family'
            try:
                agent_relator = agent['relator']
            except:
                agent_relator = 'asn'
            agent_list.append("relators:" + agent_relator + ":" + agent_type + ":" + agent_name + "|")
#    print(agent_list)
    return agent_list

def record_subject_agent_list(agents):
    subject_agent_list = []
    for agent in agents:
        if agent['role'] == 'subject':
            agent_record = aspace.get(agent['ref'])
            agent_name = agent_record['title']
            if agent_record['agent_type'] == 'agent_person':
                agent_type = 'person'
            elif agent_record['agent_type'] == 'agent_corporate_entity':
                agent_type = 'corporate_body'
            else:
                agent_type = 'family'
            try:
                agent_relator = agent['relator']
            except:
                agent_relator = 'asn'
            subject_agent_list.append("relators:" + agent_relator + ":" + agent_type + ":" + agent_name + "|")
    print(subject_agent_list)
    return subject_agent_list

def parent_agent_list(parent_agents):
    parent_agent_list = []
    for agent in parent_agents:
        if agent['role'] != 'subject':
            agent_record = aspace.get(agent['ref'])
            agent_name = agent_record['title']
            if agent_record['agent_type'] == 'agent_person':
                agent_type = 'person'
            elif agent_record['agent_type'] == 'agent_corporate_entity':
                agent_type = 'corporate_body'
            else:
                agent_type = 'family'
            try:
                agent_relator = agent['relator']
            except:
                agent_relator = 'cre'
            parent_agent_list.append("relators:" + agent_relator + ":" + agent_type + ":" + agent_name + "|")
#    print(parent_agent_list)
    return parent_agent_list

def collection_agent_list(collection_agents):
    collection_agent_list = []
    for agent in collection_agents:
        if agent['role'] != 'subject':
            agent_record = aspace.get(agent['ref'])
            agent_name = agent_record['title']
            if agent_record['agent_type'] == 'agent_person':
                agent_type = 'person'
            elif agent_record['agent_type'] == 'agent_corporate_entity':
                agent_type = 'corporate_body'
            else:
                agent_type = 'family'
            try:
                agent_relator = agent['relator']
            except:
                agent_relator = 'cre'
            collection_agent_list.append("relators:" + agent_relator + ":" + agent_type + ":" + agent_name + "|")
#    print("Collection Agent List:")
#    print(collection_agent_list)
    return collection_agent_list

def date_begin_func(dates):
        #print(dates)
        value = dates.get(begin)
        print(value)
        for date in dates:
            if date['label'] == 'creation':
                try:
                    date_begin = date['begin']
                except:
                    continue
        return date_begin



def date_end_func(dates):
    for date in dates:
        if date['label'] == 'creation' and date['date_type'] == 'inclusive':
            try:
                date_end = date['end']
                print("Inclusive date. Date end is " + date_end)
            except:
                Exception
        else:
            date_end = 'null'
    return date_end

def subject_func(subjects):
    print(" Getting any topical subjects.")
    subject_list_topic = []
    for subject in subjects:
        subject_record = aspace.get(subject['ref'])
        if subject_record['terms'][0]['term_type'] == 'topical':
            subject_list_topic.append(subject_record['title'] + "|")
        # else:
        #     print("Not a topical subject.")
    return subject_list_topic

def geographic_subject_func(subjects):
    print(" Getting any geographic subjects.")
    subject_list_geographic = []
    for subject in subjects:
        subject_record = aspace.get(subject['ref'])
        if subject_record['terms'][0]['term_type'] == 'geographic':
            subject_list_geographic.append(subject_record['title'] + "|")
        # else:
        #     print("Not a geographic subject.")
    return subject_list_geographic

def genre_func(subjects):
    genre_list = []
    print(" Getting any genre subjects.")
    for subject in subjects:
        subject_record = aspace.get(subject['ref'])
        if subject_record['terms'][0]['term_type'] == 'genre_form':
            genre_list.append(subject_record['title'] + "|")
        # else:
        #     print("Not a genre subject.")
    return genre_list

def language_func(langauge_dict):
    language_list = []
    print(" Getting languages.")
    #Needed logic is to first establish whether any sub-array within the language_dict has a non-empty notes field. If so, get the language from the notes field. If NOT, start a for loop and get the language from language and script.
    if any(dictionary.get('notes') != [] for dictionary in language_dict):
        print(" At least one language note value is not empty. Getting language from note.")
        if language_dict[0]['notes'] != []:
            try:
                content_language = language_dict[0]['notes'][0]['content']
                language_list = content_language
                print(content_language)
            except:
                print("that didn't work #1")
                Exception
        elif language_dict[1]['notes'] != []:
            try:
                content_language = language_dict[1]['notes'][0]['content']
                #content_language = language_dict
                language_list = content_language
                print(content_language)
            except:
                print("that didn't work #2")
                Exception
    else:
        print(" All language note values are empty. Getting language code(s).")
        for l in language_dict:
            lang_sub_note = l['language_and_script']
            content_language = lang_sub_note['language']
            language_list.append(content_language)
    return language_list


#authentication stuff
if __name__ == "__main__":

    CONFIGFILE = "archivesspace.cfg"

    argparser = argparse.ArgumentParser()
    argparser.add_argument("SERVERCFG", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'recording'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
    argparser.add_argument("CSVFILE", default="DEFAULT", help="Path to CSV file for parsing.")
    argparser.add_argument("CSVOUT", default="DEFAULT", help="CSV output name.")
    cliArguments = argparser.parse_args()

    aspace = archivesspace.ArchivesSpace()
    aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
    aspace.connect()

#opening the csv file, getting data from the archival object, its parent, and its resource
    with open(cliArguments.CSVFILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(cliArguments.CSVOUT, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(["title", "identifier", "field_resource_type", "field_model", "field_member_of", "parent_id", "field_weight", "field_extent", "field_genre","field_subjects_name","begin_date", "end_date","field_edtf_date_created","subjects","field_subject","field_geographic_subject","field_linked_agent","field_language","field_description_long","field_rights","field_use_and_reproduction","field_finding_aid_link","field_item_desc_link","field_campus","field_repository","field_campus_unit_repository","field_unit","field_preferred_citation","field_display_hints","full_record","bioghist"])
            for row in reader:
                #print (row.keys())
                print("\nStarting to build record for " + row['ao_uri'])
#            with open(cliArguments.CSVOUT, 'w') as output:
                record = aspace.get(row['ao_uri'])
                id = row['id']
                field_member_of = row['field_member_of']
                parent_id = row['parent_id']
                field_extent = row['field_extent']
                field_resource_type = row['field_resource_type']
                field_weight = row['field_weight']
                try:
                    parent = aspace.get(record['parent']['ref'])
                except:
                    parent = 'No Parent'
                collection = aspace.get(record['resource']['ref'])
                #print("AO: ",record['title'])
                #print("Parent: ",parent)
                #print("Collection: ",collection['title'])
                writer = csv.writer(output)

                scope_note = ""
                access_note = ""
                use_note = ""
                bioghist = ""
                
                if parent != 'No Parent':
                    try:
                        parent_title = parent['display_string']
                    except:
                        parent_title = 'null'
                try:
                    coll_title = collection['title']
                except:
                    coll_title = 'null'
                try:
                    coll_agents = collection['linked_agents']
                except:
                    coll_agents = 'null'

                print(" building notes")
                if record['notes'] != []:
                    record_notes = record['notes']
                    print(" Record has notes, checking for multi-part notes.")
                    for note in record_notes:
                        print(note)
                        if note['jsonmodel_type'] == 'note_multipart':
                            print(" Record has multi-part notes.")
                            if note['type'] == 'scopecontent':
                                print("It's a scope note.")
                                scope_note = note['subnotes'][0]['content']
                            elif note['type'] == 'accessrestrict':
                                print("It's an access note.")
                                access_note = note['subnotes'][0]['content']
                            elif note['type'] == 'userestrict':
                                print("It's a use note.")
                                use_note = note['subnotes'][0]['content']

                        else:
                            #continue means to stop the current iteration of the loop and move to the next
                            print('Not a multipart note.')
                            general_note = note['content']
                if scope_note == '':
                    print("The record has no scope note. Building one from the parent record.")
                    if parent != 'No Parent':
                        scope_note = "This material can be found in the " + coll_title + ", " + parent_title + "."
                    else:
                        scope_note =  "This material can be found in the " + coll_title + "."
                if use_note == '':
                    print("The record has no use note. Getting it from collection record.")
                    coll_notes = collection['notes']
                    for note in coll_notes:
                        if note['jsonmodel_type'] == 'note_multipart':
                            if note['type'] == 'userestrict':
                                use_note = note['subnotes'][0]['content']
                if access_note == '':
                    print("The record has no access note. Creating generic.")
                    access_note = "This material is available for research use."

#attempting to get parent agents if no AO agents
                print(" Checking for agents")
                if record['linked_agents'] == []:
                    field_subjects_name = []
                    print("  No agents on record. Checking parent record.")
                    if parent != 'No Parent':
                        if parent['linked_agents'] == []:
                            print("  The parent also has no agents. Getting agents from collection record.")
                            if collection['linked_agents'] != []:
                                collection_agents = collection['linked_agents']
    #                            print(collection_agents)
                                collection_agents = collection['linked_agents']
                                agent_list = collection_agent_list(collection_agents)
                            else:
                                agent_list = 'null'
                        elif parent['linked_agents'] != []:
    #                        print(parent['linked_agents'])
                            parent_agents = parent['linked_agents']
                            agent_list = parent_agent_list(parent_agents)
                    elif parent == 'No Parent':
                        print("  Getting agents from collection record since there are no parents.")
                        if collection['linked_agents'] != []:
                            collection_agents = collection['linked_agents']
                            agent_list = collection_agent_list(collection_agents)
                        else:
                            agent_list = 'null'
                else:
                    print("  Getting agents from record .")
                    agents = record['linked_agents']
                    agent_list = record_agent_list(agents)
                    if agent_list == []:
                        if parent != 'No Parent':
                            if parent['linked_agents'] == []:
                                print("  The parent also has no agents. Getting agents from collection record.")
                                if collection['linked_agents'] != []:
                                    collection_agents = collection['linked_agents']
    #                               print(collection_agents)
                                    collection_agents = collection['linked_agents']
                                    agent_list = collection_agent_list(collection_agents)
                                else:
                                    agent_list = 'null'
                            elif parent['linked_agents'] != []:
    #                           print(parent['linked_agents'])
                                parent_agents = parent['linked_agents']
                                agent_list = parent_agent_list(parent_agents)
                        elif parent == 'No Parent':
                            print("  Getting agents from collection record since there are no parents.")
                            if collection['linked_agents'] != []:
                                collection_agents = collection['linked_agents']
                                agent_list = collection_agent_list(collection_agents)
                            else:
                                agent_list = 'null'

                    field_subjects_name = record_subject_agent_list(agents)

#date stuff ported over
                # try:
                #     begin_date = record['dates'][0]['begin']
                # except:
                #     begin_date = 'null'
                # try:
                #     end_date = record['dates'][0]['end']
                # except:
                #     end_date = 'null'




#attempting to get parent date specifically if it's creation date
                if record['dates'] != []:
                    print(" Trying to get dates from the record")
                    #print(record['dates'])
                    try:
                        begin_date = record['dates'][0]['begin']
                    except:
                        begin_date = 'null'
                    try:
                        end_date = record['dates'][0]['end']
                    except:
                        end_date = 'null'
                    if begin_date == 'null' and end_date == 'null':
                        if parent != 'No Parent':
                            print("Checking the parent for dates ")
                            if parent['dates'] != []:
                                try:
                                    begin_date = parent['dates'][0]['begin']
                                except:
                                    begin_date = 'null'
                                try:
                                    end_date = parent['dates'][0]['end']
                                except:
                                    end_date = 'null'
                                if begin_date == 'null' and end_date == 'null':
                                    try:
                                        begin_date = collection['dates'][0]['begin']
                                    except:
                                        begin_date = 'null'
                                    try:
                                        end_date = collection['dates'][0]['end']
                                    except:
                                        end_date = 'null'
                elif parent != 'No Parent':
                    print(" Record didn't have a date. Checking the parent for dates ")
                    if parent['dates'] != []:
                        try:
                            begin_date = "~" + parent['dates'][0]['begin']
                        except:
                            begin_date = 'null'
                        try:
                            end_date = "~" + parent['dates'][0]['end']
                        except:
                            end_date = 'null'
                        if begin_date == 'null' and end_date == 'null':
                            try:
                                begin_date = collection['dates'][0]['begin']
                            except:
                                begin_date = 'null'
                            try:
                                end_date = collection['dates'][0]['end']
                            except:
                                end_date = 'null'


                if begin_date == 'null' and end_date == 'null':
                    edtf_date = 'XXXX'
                elif begin_date == 'null' and end_date != 'null':
                    edtf_date = "../" + end_date
                elif begin_date != 'null' and end_date == 'null':
                    edtf_date = begin_date
                else:
                    edtf_date = begin_date + "/" + end_date

                if edtf_date == 'XXXX':
                    print(" Undated material!! Check the collection record dates: "+ collection['dates'][0]['begin'])

#                     dates = record['dates']
#                     date_begin = date_begin_func(dates)
#                     date_end = date_end_func(dates)
#                     print('Getting date from archival object ' + record['uri'])
#                     print(" Printing the record dates: ",dates)
#                     print(" Printing the date_begin: ",date_begin)
#                     print(" Printing the date_end: ",date_end)
#                 elif parent != 'No Parent':
#                     if parent['dates'] != []:
#                         dates = parent['dates']
#                         print('Getting date from the parent')
#                         date_begin = date_begin_func(dates)
#                 else:
#                     dates = collection['dates']
#                     print(" Printing the collection dates: " + dates)
#                     date_begin = date_begin_func(dates)
#                     print('Getting date from the collection')
#                 try:
#                     begin_date = str(date_begin)
#                 #    begin_date = record['dates'][0]['begin']
#                 except:
#                     begin_date = 'null'
#                 try:
#                     end_date = date_end
#                 except:
#                     end_date = 'null'
#
#                 if end_date == []:
#                     end_date = 'null'
#
#
#
# #make edtf date from existing dates
#                 if date_begin == 'null' and date_end == 'null':
#                     edtf_date = 'XXXX'
#                 elif date_begin == 'null' and date_end != 'null':
#                     edtf_date = "../" + date_end
#                 elif date_begin != 'null' and date_end == 'null':
#                     edtf_date = date_begin
#                 else:
#                     print("Date begin is :",date_begin)
#                     edtf_date = date_begin + "/" + date_end

#get subjects from AO, if none in AO, get from parent
                if record['subjects'] != []:
                    subjects = record['subjects']
                    subject_list_topic = subject_func(subjects)
                    subject_list_geographic = geographic_subject_func(subjects)
                    genre_list = genre_func(subjects)
                elif parent != 'No Parent':
                    if parent['subjects'] != []:
                        try:
                            subjects = parent['subjects']
                        except:
                            subjects = 'null'
                            subject_list_topic = 'null'
                            subject_list_geographic = 'null'
                            genre_list = 'null'
                    else:
                        subjects = 'null'
                        subject_list_topic = 'null'
                        subject_list_geographic = 'null'
                        genre_list = 'null'
                # elif collection['subjects'] != []:
                #     try:
                #         subjects = collection['subjects']
                #     except:
                #         subjects = 'null'
                else:
                    subjects = 'null'
                    subject_list_topic = 'null'
                    subject_list_geographic = 'null'
                    genre_list = 'null'
                try:
                    agents = record['linked_agents']
                    agent_list = agent_list(agents)
                    #print(agent_list)
                except:
                    agents = 'null'
#getting the language
                if record['lang_materials'] != []:
                    print(" Language note from record ")
                    #print(record['lang_materials'])
                    language_dict = record['lang_materials']
                    language_list = language_func(language_dict)
                    print(language_list)
                # elif parent != 'No Parent':
                #     if parent['lang_materials'] != []:
                #         print(" Language note from parent ")
                #         #print(parent['lang_materials'])
                #         language_dict = parent['lang_materials']
                #         language_list = language_func(language_dict)
                #         print(" Language list from parent: ",language_list)
                #     else:
                #         print(" Language note from collection ")
                #         language_dict = collection['lang_materials']
                #         language_list = language_func(language_dict)
                #         print(" Language list from collection: ",language_list)
                # else:
                #     print(" Language note from collection since there's no parent ")
                #     language_dict = collection['lang_materials']
                #     language_list = language_func(language_dict)
                #     print(" Language list from collection: ",language_list)
                else:
                #defaulting to English since no language at recording
                    print(" No language associated with record, defaulting to English.")
                    language_list = 'English'




#dealing with notes again:



#Commenting out as this seems to be the source of the issue where a variable from a previous line is asigned to a later line.                            
                    # if 'use_note' in locals():
                    #     print('Already a use note.')
                    # else:
                    #     print(" No use note on record. Getting use note from collection level.")
                    #     notes = collection['notes']
                    #     for note in notes:
                    #         if note['jsonmodel_type'] == 'note_multipart':
                    #             if note['type'] == 'userestrict':
                    #                 use_note = note['subnotes'][0]['content']
                    # if 'access_note' in locals():
                    #     print('Already an access note.')
                    # else:
                    #     access_note = 'This material is available for research use.'
                    # if 'bioghist' in locals():
                    #     print('Already a bioghist note.')
                    # else:
                    #     bioghist = ''








# #getting the use note:
#                 if record['notes'] != []:
#                     print(" Record has notes, checking for use note.")
#                     record_notes = record['notes']
#                     for note in record_notes:
#                         print(note)
#                         if note['jsonmodel_type'] == 'note_multipart':
#                             if note['type'] == 'userestrict':
#                                 use_note = note['subnotes'][0]['content']
#                                 break
#                             else:
#                                 print(" not a use note")
#                         # if 'access_note' in locals():
#                         #     print('Already a use note.')
#                         # else:
#                         #     notes = collection['notes']
#                         #     for note in notes:
#                         #         if note['jsonmodel_type'] == 'note_multipart':
#                         #             if note['type'] == 'userestrict':
#                         #                 use_note = note['subnotes'][0]['content']
#                         #             else:
#                         #                 continue

#                 elif record['notes'] == []:
#                     print(" No notes on record. Getting use note from collection level.")
#                     notes = collection['notes']
#                     for note in notes:
#                         if note['jsonmodel_type'] == 'note_multipart':
#                             if note['type'] == 'userestrict':
#                                 use_note = note['subnotes'][0]['content']
#                             # else:
#                             #     continue

# #getting the access note:
#                 if record['notes'] != []:
#                     print(" Record has notes, checking for access note.")
#                     record_notes = record['notes']
#                     for note in record_notes:
#                         print(note)
#                         if note['jsonmodel_type'] == 'note_multipart':
#                             if note['type'] == 'accessrestrict':
#                                 if 'label' in note:
#                                     print("this has a note label")
#                                     if note['label'] == 'Conditions Governing Web Access':
#                                         print("Web access not regular access.")
#                                     else:
#                                         continue
#                                 else:
#                                     access_note = note['subnotes'][0]['content']
#                                     break
#                             else:
#                                 print(" not an access note")
#  #                               continue
#                 elif record['notes'] == []:
#                     print(" No notes on record. Building access note.")
#                     access_note = "This material is available for research use."

 

# #getting the bioghist note:
#                 print(" building bioghist note")
#                 if record['notes'] != []:
#                     print(" Record has notes, checking for bioghist note.")
#                     record_notes = record['notes']
#                     for note in record_notes:
#                         print(note)
#                         if note['jsonmodel_type'] == 'note_multipart':
#                             if note['type'] == 'bioghist':
#                                 bioghist = note['subnotes'][0]['content']
#                                 break
#                             else:
#                                 print(" not a bioghist note")
#                 else:
#                     print(" Record has no notes. Putting N/A for bioghist note.")
#                     bioghist = "n/a"


#getting the repository info
                if record['repository']['ref'] == '/repositories/2':
                    repo_text = "Sophia Smith Collection of Women's History"
                elif record['repository']['ref'] == '/repositories/4':
                    repo_text = "Smith College Archives"
                elif record['repository']['ref'] == '/repositories/3':
                    repo_text = "Mortimer Rare Book Collection"


                print(" building the campus and repository info")
                field_campus = "Smith College"
                field_repository = "Smith College Special Collections"
                field_campus_unit_repository = repo_text
                field_unit = repo_text
                if row['field_resource_type'] == 'Text':
                    display_hints = 'PDFjs'
                    field_model = 'Digital Document'
                elif row['field_resource_type'] == 'Collection':
                    display_hints = 'Mirador'
                    field_model = 'Paged Content'
                elif row['field_resource_type'] == 'Still Image':
                    display_hints = 'Mirador'
                    field_model = 'Image'
                print(" building the citation")
#building the citation
                repo_id = collection['id_0'] + '-' + collection['id_1'] + '-' + collection['id_2']
                citation = "[identification of item], " + coll_title + ' (' + repo_id + ')' + ', ' + repo_text + ", Smith College Special Collections, Northampton, Massachusetts. [url]"
                print(" building the finding aid links")
                field_finding_aid_link = "https://findingaids.smith.edu" + collection['uri']
                field_item_desc_link = "https://findingaids.smith.edu" + record['uri']
                print(" writing the data")
                writer.writerow([record['display_string'],id,field_resource_type,field_model,field_member_of,parent_id,field_weight,field_extent,genre_list,field_subjects_name,begin_date,end_date,edtf_date,subjects,subject_list_topic,subject_list_geographic,agent_list,language_list,scope_note,access_note,use_note,field_finding_aid_link,field_item_desc_link,field_campus,field_repository,field_campus_unit_repository,field_unit,citation,display_hints,record,bioghist])
                print(" Record finished building.")
                            
            #writer.writerow(["Name", "Age", "Country"])
