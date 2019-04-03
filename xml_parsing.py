from lxml import etree
import xml.etree.ElementTree as ET

#client = Client('http://www.soapclient.com/xml/soapresponder.wsdl')
#wsdl = 'https://www.nasa.gov/rss/dyn/breaking_news.rss'
wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'

data = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>"""


root = ET.fromstring(data)

#for element in root.iter():
#    print("{} {}: {}".format(element.tag, element.attrib, element.text))

for element in root.findall('country'):
    name = element.get('name')
    result = element.find('year').text
    print(name, " is ", result)
    if result == '2011':
        print("Great year!")
    else:
        print("Not a great year")






#A = 2
#B = 0

#print(root.text[1])
#print(root.findall('.//country'))
#print(root[A][B].tag)
#print(root[A][B].attrib)
#print(root[A][B].text)
