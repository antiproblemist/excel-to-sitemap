import pandas as pd, numpy as np, gzip, re, argparse
from lxml import etree
from tqdm import tqdm
from datetime import datetime
from math import ceil

parser = argparse.ArgumentParser(description='Command line arguments for sitemap generation')

parser.add_argument("file", help="The path/file name of the Excel file that contains data \
to be converted to a sitemap. The excel file should atleast have a column name 'url' with\
the URLs for which sitemap is to be generated.", action="store")

parser.add_argument("-f", "--changefreq", help="an option to specify whether a changefreq column \
with the column name 'changefreq' has been provided in the excel sheet. If provided, all \
generated sitemaps will have a <changefreq> atrribute.", default=False, action="store_true")

parser.add_argument("-p", "--priority", help="an option to specify whether a priority column \
with the column name 'priority' has been provided in the excel sheet. If provided, all \
generated sitemaps will have a <priority> atrribute", default=False, action="store_true")

parser.add_argument("-l", "--lastmod", help="an option to specify whether a last modified date \
column with the column name 'lastmod' has been provided in the excel sheet. If provided, all \
generated sitemaps will have a <lastmod> atrribute", default=False, action="store_true")

parser.add_argument("-m", "--maxurls", type=int, default=35000, help="an integer to specify the maximum number of URLs that \
should be contained in a single sitemap file and the sitemap will be split into multiple files.")

parser.add_argument("-c", "--classifier", help="an option to specify whether a classifier column \
with the column name 'classifier' has been provided in the excel sheet. If provided the sitemaps \
will be split into multiple files based on the unique values of the classifiers",\
default=False, action="store_true")

args = parser.parse_args()

URL_COLUMN = "url"
PRIORITY_COLUMN = "priority"
CHANGEFREQ_COL = "changefreq"
LASTMODIFIED_COL = "lastmod"
CLASSIFIER_COL = "classifier"
PER_FILE_LIMIT = args.maxurls

def clean_string(text):
	"""This function runs a regex function to strip all special characters and make it appropriate for a file name
	Parameters:
	text (str): The string that needs to be converted to an appropriate file name

	Returns:
	str: Return the clean value appropriate for a file name
	"""
	text = re.sub('[^a-z0-9-]+', '', text.lower().strip().replace(" ", "-"))
	return text


def generate_sitemap(df, frequency, priority, lastmodified, maxurls, classifier_value=None):
	"""This function iterates over the DataFrame, reading the 'url' column in it. \
	If the total length of the number of urls exceeds the default or specified value of \
	maxurls then the file is split into multiple files.

	Parameters:
		df (DataFrame): The pandas DataFrame containing the urls and other optional columns
		frequency (bool): A boolean value indicating whether to include the <changefreq> attributes in the sitemap or not
		priority (bool): A boolean value indicating whether to include the <priority> attributes in the sitemap or not	
		lastmodified (bool): A boolean value indicating whether to include the <lastmod> attributes in the sitemap or not
		maxurls (int): An int value specifying the maximum number of urls inside a single sitemap file
		classifier_value (str, optional): The name of the classifer for which the sitemap is to be generated. This will be included int he sitemap file name.
	"""

	count_lower_limit = 0
	count_higher_limit = PER_FILE_LIMIT

	file_count = int(ceil(float(len(df.index)) / float(PER_FILE_LIMIT)))

	for file_number in range(1, file_count + 1):
		root = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
		for index, row in tqdm(df[count_lower_limit:count_higher_limit].iterrows(), total=len(df[count_lower_limit:count_higher_limit].index)):
			try:
				url = etree.Element("url")

				loc = etree.Element("loc")
				loc.text = str(row[URL_COLUMN])
				url.append(loc)

				if lastmodified:
					lastmod_attribute = etree.Element("lastmod")
					lastmod_datetime = datetime.strftime(row[LASTMODIFIED_COL], '%Y-%m-%d')
					lastmod_attribute.text = str(lastmod_datetime)
					url.append(lastmod_attribute)

				if priority:
					priority_attribute = etree.Element("priority")
					priority_attribute.text = str(row[PRIORITY_COLUMN])
					url.append(priority_attribute)

				if frequency:
					changefreq_attribute = etree.Element("changefreq")
					changefreq_attribute.text = str(row[CHANGEFREQ_COL])
					url.append(changefreq_attribute)

				root.append(url)
			except Exception as e:
				print(str(e))
				continue

		if classifier_value:
			file_name = "sitemap-%s-%s.xml" % (clean_string(classifier_value), file_number)
		else:
			file_name = "sitemap-%s.xml" % file_number

		file = open(file_name, 'wb')
		file.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8'))
		file.close()
		
		file = open(file_name, 'rb')
		gfile = gzip.open("%s.gz" % file_name, "wb")
		gfile.writelines(file)
		gfile.close()
		file.close()

		count_lower_limit += PER_FILE_LIMIT
		count_higher_limit += PER_FILE_LIMIT

def main():
	"""This function reads the excel file and generates a sitemap according to the command line arguments provided"""
	try:
		df = pd.read_excel(args.file, 'Sheet1', index_col=None)
	except Exception as e:
		print("%s. File error" % e)
		exit()

	if args.classifier:
		unique_clasifiers_list = np.array(list(set(df[CLASSIFIER_COL].tolist())))
		for classifier_item in tqdm(unique_clasifiers_list, total=len(unique_clasifiers_list)):
			classifier_df = df.loc[(df[CLASSIFIER_COL]==classifier_item)]
			generate_sitemap(classifier_df, args.changefreq, args.priority, args.lastmod, PER_FILE_LIMIT, classifier_item)
	else:
		generate_sitemap(df, args.changefreq, args.priority, args.lastmod, PER_FILE_LIMIT)