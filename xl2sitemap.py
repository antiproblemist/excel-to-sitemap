import pandas as pd, numpy as np, gzip, re, argparse
from lxml import etree
from tqdm import tqdm
from datetime import datetime
from math import ceil

parser = argparse.ArgumentParser(description='Command line arguments for sitemap generation')

parser.add_argument("file", help="The path/file name of the Excel file that contains data \
to be converted to a sitemap. The excel file should atleast have a column name 'url' with\
the URLs for which sitemap is to be generated.", action="store")

parser.add_argument("-f", "--frequency", help="an option to specify whether a frequency column \
with the column name 'frequency' has been provided in the excel sheet. If provided, all \
generated sitemaps will have a <changefreq> atrribute.", default=False, action="store_true")

parser.add_argument("-p", "--priority", help="an option to specify whether a priority column \
with the column name 'priority' has been provided in the excel sheet. If provided, all \
generated sitemaps will have a <priority> atrribute", default=False, action="store_true")

parser.add_argument("-l", "--lastmodified", help="an option to specify whether a last modified \
column with the column name 'lastmodified' has been provided in the excel sheet. If provided, all \
generated sitemaps will have a <lastmod> atrribute", default=False, action="store_true")

parser.add_argument("-m", "--maxurls", type=int, default=35000, help="an integer to specify the maximum number of URLs that \
should be contained in a single sitemap file and the sitemap will be split into multiple files.",\
action="store_const")

parser.add_argument("-c", "--classifier", help="an option to specify whether a classifier column \
with the column name 'classifier' has been provided in the excel sheet. If provided the sitemaps \
will be split into multiple files based on the unique values of the classifiers",\
default=False, action="store_true")

args = parser.parse_args()

input_workbook_path = args.file

url_col = "url"
priority_col = "priority"
changefreq_col = "frequency"
lastmodified_col = "lastmodified"
classifier_col = "classifier"

try:
	df = pd.read_excel(args.file, 'Sheet1', index_col=None)
except Exception as e:
	print("%s. File error" % e)
	
def clean(text):
	text = re.sub('[^a-z0-9-]+', '', text.lower().strip().replace(" ", "-"))
	return text

unique_clasifiers_list = np.array(list(set(df[classifier_col].tolist())))

per_file_limit = 35000

file_df = pd.DataFrame(columns=['file_name', 'gzip_file_name', 'type'])
file_list = []
for classifier_item in tqdm(unique_clasifiers_list, total=len(unique_clasifiers_list)):

	count_lower_limit = 0
	count_higher_limit = per_file_limit

	city_df = df.loc[(df[classifier_col]==classifier_item)]
	file_count = int(ceil(float(len(city_df.index)) / float(per_file_limit)))

	for file_number in range(1, file_count + 1):
		root = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
		for index, row in tqdm(city_df[count_lower_limit:count_higher_limit].iterrows(), total=len(city_df[count_lower_limit:count_higher_limit].index)):
			try:
				url = etree.Element("url")

				loc = etree.Element("loc")
				loc.text = str(row[link_col])
				url.append(loc)

				lastmod = etree.Element("lastmod")
				lastmod_datetime = datetime.strftime(row[lastmodified_col], '%Y-%m-%d')
				lastmod.text = str(lastmod_datetime)
				url.append(lastmod)

				priority = etree.Element("priority")
				priority.text = str(row[priority_col])
				url.append(priority)

				changefreq = etree.Element("changefreq")
				changefreq.text = str(row[changefreq_col])
				url.append(changefreq)

				root.append(url)
			except Exception:
				continue

		file_name = "sitemap-%s-listing-%s.xml" % (clean(city_item), file_number)
		file = open(file_name, 'w')
		file.write(etree.tostring(root, pretty_print=True, xml_declaration = True, encoding='UTF-8'))
		file.close()
		
		file = open(file_name, 'r')
		gfile = gzip.open("%s.gz" % file_name, "wb")
		gfile.writelines(file)
		gfile.close()
		file.close()
		
		file_dict = {
			'file_name': file_name,
			'gzip_file_name': "%s.gz" % file_name,
			'type': 'listing'
		}
		file_list.append(file_dict)

		count_lower_limit += per_file_limit
		count_higher_limit += per_file_limit
		
temp_df = pd.DataFrame.from_dict(file_list)
file_df = file_df.append(temp_df, ignore_index=True)
file_df.to_excel("List-of-sitemaps-generated.xlsx", sheet_name='Sheet1', index=None)