import pandas as pd
import openpyxl

excel_path = 
for x in 10:
    f = open('pinpoll'+ x +'.txt','w')
    f.write('
            <annotation>
	<folder>od_dogs</folder>
	<filename>aaron-bookout-3NJ_LjXXqsM-unsplash.jpg</filename>
	<path>C:\Users\nakata\Python\myfolder\od_test\od_dogs\aaron-bookout-3NJ_LjXXqsM-unsplash.jpg</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>640</width>
		<height>427</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>dog</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>223</xmin>
			<ymin>38</ymin>
			<xmax>491</xmax>
			<ymax>409</ymax>
		</bndbox>
	</object>
</annotation>
')