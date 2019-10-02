#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import re
import sys
import operator

#THE LIST OF ALL DEPARTMENTS.
all_departments=['MANAGEMENT', 'ASIAN+STUDIES', 'ASIAN+STUDIES+WITH+THESIS', 'ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY',
                 'AUTOMOTIVE+ENGINEERING', 'MOLECULAR+BIOLOGY+%26+GENETICS', 'BUSINESS+INFORMATION+SYSTEMS',
                 'BIOMEDICAL+ENGINEERING', 'CRITICAL+AND+CULTURAL+STUDIES', 'CIVIL+ENGINEERING', 'CONSTRUCTION+ENGINEERING+AND+MANAGEMENT',
                 'COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY', 'EDUCATIONAL+TECHNOLOGY', 'CHEMICAL+ENGINEERING', 'CHEMISTRY',
                 'COMPUTER+ENGINEERING', 'COGNITIVE+SCIENCE', 'COMPUTATIONAL+SCIENCE+%26+ENGINEERING', 'ECONOMICS', 'EDUCATIONAL+SCIENCES',
                 'ELECTRICAL+%26+ELECTRONICS+ENGINEERING', 'ECONOMICS+AND+FINANCE', 'ENVIRONMENTAL+SCIENCES', 'ENVIRONMENTAL+TECHNOLOGY',
                 'EARTHQUAKE+ENGINEERING', 'ENGINEERING+AND+TECHNOLOGY+MANAGEMENT', 'FINANCIAL+ENGINEERING', 'FOREIGN+LANGUAGE+EDUCATION',
                 'GEODESY', 'GEOPHYSICS', 'GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING', 'HISTORY', 'HUMANITIES+COURSES+COORDINATOR', 'INDUSTRIAL+ENGINEERING',
                 'INTERNATIONAL+COMPETITION+AND+TRADE', 'CONFERENCE+INTERPRETING', 'INTERNATIONAL+TRADE', 'INTERNATIONAL+TRADE+MANAGEMENT',
                 'LINGUISTICS', 'WESTERN+LANGUAGES+%26+LITERATURES', 'LEARNING+SCIENCES', 'MATHEMATICS', 'MECHANICAL+ENGINEERING',
                 'MECHATRONICS+ENGINEERING', 'INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST',
                 'INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS', 'MANAGEMENT+INFORMATION+SYSTEMS', 'FINE+ARTS',
                 'PHYSICAL+EDUCATION', 'PHILOSOPHY', 'PHYSICS', 'POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS', 'PRIMARY+EDUCATION', 'PSYCHOLOGY',
                 'MATHEMATICS+AND+SCIENCE+EDUCATION', 'SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION', 'SYSTEMS+%26+CONTROL+ENGINEERING', 'SOCIOLOGY',
                 'SOCIAL+POLICY+WITH+THESIS', 'SOFTWARE+ENGINEERING', 'SOFTWARE+ENGINEERING+WITH+THESIS', 'TURKISH+COURSES+COORDINATOR', 'TURKISH+LANGUAGE+%26+LITERATURE',
                 'TRANSLATION+AND+INTERPRETING+STUDIES', 'SUSTAINABLE+TOURISM+MANAGEMENT', 'TOURISM+ADMINISTRATION', 'TRANSLATION', 'EXECUTIVE+MBA', 'SCHOOL+OF+FOREIGN+LANGUAGES']


long_all_departments={"MANAGEMENT":"AD","ASIAN+STUDIES":"ASIA","ASIAN+STUDIES+WITH+THESIS":"ASIA","ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY":"ATA",
                      "AUTOMOTIVE+ENGINEERING":"AUTO","BIOMEDICAL+ENGINEERING":"BM","BUSINESS+INFORMATION+SYSTEMS":"BIS","CHEMICAL+ENGINEERING":"CHE",
                      "CHEMISTRY":"CHEM","CIVIL+ENGINEERING":"CE","COGNITIVE+SCIENCE":"COGS","COMPUTATIONAL+SCIENCE+%26+ENGINEERING":"CSE",
                      "COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY":"CET","COMPUTER+ENGINEERING":"CMPE","CONFERENCE+INTERPRETING":"INT",
                      "CONSTRUCTION+ENGINEERING+AND+MANAGEMENT":"CEM","CRITICAL+AND+CULTURAL+STUDIES":"CCS","EARTHQUAKE+ENGINEERING":"EQE","ECONOMICS":"EC"
    ,"ECONOMICS+AND+FINANCE":"EF","EDUCATIONAL+SCIENCES":"ED","EDUCATIONAL+TECHNOLOGY":"CET","ELECTRICAL+%26+ELECTRONICS+ENGINEERING":"EE",
                      "ENGINEERING+AND+TECHNOLOGY+MANAGEMENT":"ETM","ENVIRONMENTAL+SCIENCES":"ENV","ENVIRONMENTAL+TECHNOLOGY":"ENVT",
                      "EXECUTIVE+MBA":"XMBA","FINANCIAL+ENGINEERING":"FE","FINE+ARTS":"PA","FOREIGN+LANGUAGE+EDUCATION":"FLED","GEODESY":"GED","GEOPHYSICS":"GPH","GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING":"GUID",
                      "HISTORY":"HIST","HUMANITIES+COURSES+COORDINATOR":"HUM","INDUSTRIAL+ENGINEERING":"IE","INTERNATIONAL+COMPETITION+AND+TRADE":"INCT","INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST":"MIR",
                      "INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS":"MIR","INTERNATIONAL+TRADE":"INTT","INTERNATIONAL+TRADE+MANAGEMENT":"INTT",
                      "LEARNING+SCIENCES":"LS","LINGUISTICS":"LING","MANAGEMENT+INFORMATION+SYSTEMS":"MIS","MATHEMATICS":"MATH","MATHEMATICS+AND+SCIENCE+EDUCATION":"SCED","MECHANICAL+ENGINEERING":"ME",
                      "MECHATRONICS+ENGINEERING":"MECA","MOLECULAR+BIOLOGY+%26+GENETICS":"BIO","PHILOSOPHY":"PHIL","PHYSICAL+EDUCATION":"PE","PHYSICS":"PHYS","POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS":"POLS",
                      "PRIMARY+EDUCATION":"PRED","PSYCHOLOGY":"PSY","SCHOOL+OF+FOREIGN+LANGUAGES":"YADYOK","SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION":"SCED","SOCIAL+POLICY+WITH+THESIS":"SPL",
                      "SOCIOLOGY":"SOC","SOFTWARE+ENGINEERING":"SWE","SOFTWARE+ENGINEERING+WITH+THESIS":"SWE","SUSTAINABLE+TOURISM+MANAGEMENT":"TRM","SYSTEMS+%26+CONTROL+ENGINEERING":"SCO","TOURISM+ADMINISTRATION":"TRM","TRANSLATION":"WTR",
                      "TRANSLATION+AND+INTERPRETING+STUDIES":"TR","TURKISH+COURSES+COORDINATOR":"TK","TURKISH+LANGUAGE+%26+LITERATURE":"TKL","WESTERN+LANGUAGES+%26+LITERATURES":"LL"}

#determines the number of grad and undergad lessons in the given lessons set.
def find_undergrad_grad(lessons):

    grad = set()
    undergrad = set()
    #print lessons.keys()
    for i in lessons.keys():

        if len(i)<2:
            continue

        if not re.search("\d",i):
            undergrad.add(i)

        elif int(i[re.search("\d",i).start()])>4:
            grad.add(i)
        else:
            undergrad.add(i)

    result = [undergrad,grad]
    return result

#Find headers is a method the determine the index of the
#headers in the course schedule website.
#For example, it determines the indexes of, Code.Sec, Desc., Cr. and so on.
def find_headers(headers):
    header_list = []
    #0 abbr ,1 name, 2 instr

    tmp_index = 0
    for i in headers:
        if(i=="Code.Sec"):
            header_list.append(tmp_index)
        elif(i=="Name"):
            header_list.append(tmp_index)
        elif(i=="Instr."):
            header_list.append(tmp_index)

        tmp_index = tmp_index+1
    return header_list

#The course website consists of grey and white rows. This method merges this white and grey
#rows and return all the information in a list.
#the firs parameter is the source code of the website, and the second argument is the
#index list of the headers determined by the find_header method previously.
def pull_data(source,index_list):
    gray = (source.find_all("tr",attrs={"class":"schtd2"}))
    white= (source.find_all("tr",attrs={"class":"schtd"}))
    big_list=[]

    i_1 = 0
    i_2 = 0
    turn = 0

    while i_1 < len(gray) or i_2 < len(white):
        if(turn==0):
            if(i_1>=len(gray)):
                turn=1
                continue
            parsed = gray[i_1].text
            parsed = re.split("\n",parsed)
            if not parsed[index_list[0]]:
                i_1 = i_1 + 1
            else:
                turn = 1
                big_list.append(gray[i_1])
                i_1 = i_1+1
        else:
            if(i_2>=len(white)):
                turn=0
                continue
            parsed = white[i_2].text
            parsed = re.split("\n",parsed)
            if not parsed[index_list[0]]:
                i_2 = i_2 + 1
            else:
                turn = 0
                big_list.append(white[i_2])
                i_2 = i_2 + 1


    return big_list

#construct table is a method to create the table in the range of given years and semesters.
#For each department, it traverses the website of departments for each year separately, and store
#the information.
def construct_table(year_1,semester_1,year_2,semester_2):

    fieldnames = ["Dept./Prog.(name)", "Course Code", "Course Name"]
    for department in all_departments:

        #the list storing the instructors of each semester separately.
        semester_instr = []
        #the list storing the lessons of each semester separately.
        semester_lesson = []

        #the set storing all the lessons for the department
        #for all years, in the pair of code-name
        total_lessons= {}

        #the set storing all the lessons for the department
        #for all years, in the pair of of Course.cod - set of semesters.
        #it is used to determine in which semesters does the lesson be given.
        lesson_semesters = {}

        #the set storing all the lessons for the department
        #for all years, in the pair of of Course.cod - set of instructors.
        #it is used to determine how many different lecturer teaches a given lesson.
        lesson_instructors={}
        for year in range(year_1,year_2+1):
            # print (year)
            for i in range(1,4):
                #ilk ve son yil kontrolu
                if(year == year_1):
                    if i < semester_1:
                        continue

                if(year == year_2):
                    if i > semester_2:
                        break

                #The first tree temp are used to get the website url.
                temp=str(year)
                temp2=str(year+1)
                temp3=str(i)
                temp4=""
                decode_semester=""
                if i==1:
                    decode_semester="-Fall"
                    temp4=temp
                elif i==2:
                    decode_semester="-Spring"
                    temp4=temp2
                else:
                    decode_semester="-Summer"
                    temp4=temp2
                #temp4 and decode_semester is used to get the pair such as 2019-Spring
                #in the csv table format.
                if not temp4+decode_semester in fieldnames:
                    fieldnames.append(temp4+decode_semester)

                r= requests.get("https://registration.boun.edu.tr/scripts/sch.asp?donem="+temp+"/"+temp2+"-"+temp3+"&kisaadi="
                                +long_all_departments[department]+"&bolum="+department,timeout=20)


                source = BeautifulSoup(r.content, "html")
                if not source.find("tr",attrs={"class":"schtitle"}):
                    semester_lesson.append({"C.OZTURAN"})
                    semester_instr.append({"C.OZTURAN"})
                    continue
                if source.find("tr",attrs={"class":"schtitle"}):

                    headers = (source.find("tr",attrs={"class":"schtitle"}).text).splitlines()
                    #determining index of headers
                    index_list = find_headers(headers)
                    #merging grey & white rows
                    big_list = pull_data(source,index_list)

                    #print big_list[0].text
                    #print big_list[1].text
                    #print big_list[2].text

                    #parsing rows and storing the data
                    inst_of_semester = set()
                    lesson_of_semester = set()
                    i=0
                    while i<len(big_list):

                        parse_string =  big_list[i].text
                        parse_string = re.split("\n",parse_string)
                        #UptoDown
                        #the temporary set for storing the instructors
                        course_code=re.search("[a-zA-Z0-9]*\s*[0-9]*\w?",parse_string[index_list[0]])
                        split_code=re.split("\s+",course_code.group(0))
                        if len(split_code)==1:
                            course_code=course_code.group(0)
                        else:
                            course_code=split_code[0]+split_code[1]


                        if "STAFF" not in parse_string[index_list[2]]:
                            inst_of_semester.add(parse_string[index_list[2]])

                        lesson_of_semester.add(course_code)
                        total_lessons[course_code] = re.sub("\xa0","",parse_string[index_list[1]]).strip()

                        # ders - yil
                        # bu dersi hangi dönemlerde aldigimi tutuyorum
                        if course_code in lesson_semesters:
                            temp_list1 = lesson_semesters[ course_code ]
                            temp_list1.add( temp4+decode_semester )
                            lesson_semesters[ course_code ] = temp_list1
                        else:
                            temp_list1 = set()
                            temp_list1.add( temp4+decode_semester)
                            lesson_semesters[ course_code ] = temp_list1

                        #bu dersi veren hocaları tutuyorum
                        if "STAFF" not in parse_string[index_list[2]]:
                            if course_code in lesson_instructors:
                                temp_list2 = lesson_instructors[ course_code ]
                                temp_list2.add( parse_string[index_list[2]].strip() )
                                lesson_instructors[ course_code ] = temp_list2
                            else:
                                temp_list2 = set()
                                temp_list2.add( parse_string[index_list[2]].strip() )
                                lesson_instructors[ course_code ] = temp_list2

                        i=i+1

                    semester_lesson.append(lesson_of_semester)
                    semester_instr.append(inst_of_semester)


        #Determining the number of undergrad and grad courses.
        undergrad_grad = find_undergrad_grad(total_lessons)

        #WHAT'S GOING ON HERE.
        if not "Total Offerings" in fieldnames:
            fieldnames.append("Total Offerings")
            str_fieldnames=re.sub(", ",",",str(fieldnames))
            str_fieldnames=str_fieldnames[1:len(str_fieldnames)-1]
            print (str_fieldnames)

        name= re.sub("%26\+","",department)
        name= re.sub("\+|%3a|%2c"," ",name)
        column_dict = ({"Dept./Prog.(name)" : long_all_departments[department]+"("+name+")", "Course Code" : str("U" +
                                                                                                                 str(len(undergrad_grad[0])) + " " + "G" + str(len(undergrad_grad[1]))).strip()})

        total_grad = 0
        total_undergrad = 0
        total_instr = set()
        tuple1=0
        tuple2=0
        tuple3=set()

        for i in range(0,len(fieldnames)-4):
            if semester_lesson[i]!={"C.OZTURAN"}and len(undergrad_grad[0])>0:
                tuple1 = len(undergrad_grad[0].intersection(semester_lesson[i]))
            if semester_lesson[i]!={"C.OZTURAN"}and len(undergrad_grad[1])>0:
                tuple2 = len(undergrad_grad[1].intersection(semester_lesson[i]))
            tuple3 = semester_instr[i]
            column_dict[fieldnames[i+3]] = str("U"+ str(tuple1)+ " "+"G" + str(tuple2) + " " + "I" + str(len(tuple3))).strip()

            total_undergrad = total_undergrad + tuple1
            total_grad = total_grad + tuple2
            total_instr = total_instr.union(tuple3)
        #print (total_instr)


        column_dict["Total Offerings"] = str("U" + str(total_undergrad) + " " + "G" + str(total_grad) + " " \
                                             + "I" + str(len(total_instr))).strip()

        str_columns=[]
        for eachcolumn in fieldnames:
            if not eachcolumn in column_dict.keys():
                str_columns.append("")
            elif eachcolumn=="Total Offerings":
                str_columns.append(column_dict["Total Offerings"])
            else:
                str_columns.append(str(column_dict[eachcolumn]))
        str_columns=re.sub(", ",",",str(str_columns))
        str_columns=str_columns[1:len(str_columns)-1]
        print (str_columns)

        for i in sorted(total_lessons.keys()):
            str_courses=[]
            if len(i)<2:
                continue
            temp_dict = {"Course Code": i, "Course Name": total_lessons[i]}
            for j in lesson_semesters[i]:
                temp_dict[j] = "x"

            sayac1 = 0
            for j in temp_dict.keys():
                if temp_dict[j]=="x":
                    sayac1 = sayac1 + 1
            sayac2 = 0
            if i  in lesson_instructors:
                sayac2 = len(lesson_instructors[i])

            temp_dict["Total Offerings"] = str(sayac1) + "/" + str(sayac2)

            for eachcolumn in fieldnames:
                if not eachcolumn in temp_dict.keys():
                    str_courses.append("")
                elif eachcolumn=="Total Offerings":
                    str_courses.append(temp_dict["Total Offerings"])
                else:
                    str_courses.append(str(temp_dict[eachcolumn]))

            str_courses=re.sub(", ",",",str(str_courses))
            str_courses=str_courses[1:len(str_courses)-1]
            print (str_courses)


#gives inputs to the function
#sys.argv[1] ve sys.argv[2]
input_1=sys.argv[1]
input_2=sys.argv[2]
index_1=re.search("-",input_1).start()
year_1=int(input_1[:index_1])
semester_1=input_1[index_1+1:]
if semester_1=="Fall":
    semester_1=1
elif semester_1=="Spring":
    semester_1=2
    year_1=year_1-1
else:
    semester_1=3
    year_1=year_1-1

index_2=re.search("-",input_2).start()
year_2=int(input_2[:index_2])
semester_2=input_2[index_2+1:]
if semester_2=="Fall":
    semester_2=1
elif semester_2=="Spring":
    semester_2=2
    year_2=year_2-1
else:
    semester_2=3
    year_2=year_2-1





construct_table(int(year_1),semester_1,int(year_2),semester_2)



