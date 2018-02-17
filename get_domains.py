import urllib2
import urllib
from bs4 import BeautifulSoup
import  json
import  time
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

data = None
domain_dict=[]
with open("dawn_com.json") as dawn:
    data=json.load(dawn)
    print "Total files "+ str(len(data))
count=0
count_total = 0
processed_count=0
file_count=0
output_file = "/home/uzairh/fypcode/data/paragraph_classification_data_"+str(file_count)+".json"
for item in data:
    count_total +=1
    if count_total < 0:
        continue
    print str(count_total) + " Processed"
    if processed_count==500:
        with open(output_file, 'w') as outfile:
            json.dump(domain_dict, outfile, indent=4)
            file_count+=1
            output_file = "/home/uzairh/fypcode/data/paragraph_classification_data_" + str(file_count) + ".json"
            del(domain_dict[:])
            processed_count=0
    url = item['expanded_url']
    print url
    # content = item['text']
    # splitted_content = content.split(' ')
    # filtered_content = ""
    # domain = ""
    # for words in splitted_content:
    #     words = words.encode('utf-8')
    #     words = words.replace('\'','')
    #     if words =='|':
    #         break
    #     else:
    #         if "http" not in words and "https" not in words:
    #             filtered_content+=words+" "
    if "urdu.dawn.com" not in url:
        try:
            url_open_output = urllib.urlopen(url)
            page = url_open_output.read()
            soup = BeautifulSoup(page, "html.parser")
            span_domain = soup.find('li', class_="active")
            div_content = soup.findAll('div', class_="story__content pt-1 mt-1")
            table = soup.findAll('div' , attrs={"class": "story__content pt-1 mt-1"})
            contentt = None
            final_string = ''
            if span_domain is not None and div_content is not None:
                # print "Entered"
                for x in table:
                    contentt = x.contents
                    for element in contentt:
                        if element.name is not None:
                            if element.name.encode('utf-8') == "p":
                                for details in element.contents:
                                    # print type(details)
                                    if details is not None and details.name is not None and details.name.encode(
                                            'utf-8') != 'div':
                                        # print details
                                        final_string += details.text + " "
                                    elif details.name is None:
                                        # print 'Detail was None'
                                        # print details
                                        final_string += details + " "

                                            # print 'printing final string'
                if final_string != "":
                    final_string = final_string.replace('\n',' ')
                    domain = span_domain.a.string
                    domain = domain.lower()
                    print domain + "   " + final_string
                    identifier = item['id_str']
                    t = {
                        "text": final_string ,
                        "class": domain ,
                        "id_str": identifier
                    }
                    count += 1
                    processed_count += 1
                    print str(count) + " Valid"
                    domain_dict.append(t)
                    time.sleep(3)
                else:
                    print "String was empty"



            else:
                continue
        except:
            print "unable to open "+url
            continue

print "total tweets "+ str(len(domain_dict))
