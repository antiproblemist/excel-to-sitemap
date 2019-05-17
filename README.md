# Excel to Sitemap (xl2sitemap)

[![PyPI version](https://badge.fury.io/py/xl2sitemap.svg)](https://badge.fury.io/py/xl2sitemap)

**Xl2sitemap** is a command line tool to generate sitemaps using data in an excel sheet. Xl2sitemap reads data from an excel sheet and converts the data into **SEO friendly** sitemaps that can be submitted to search engines directly after uploading.

  - Generates a .xml file
  - Generates a .xml.gz file (compressed)
  - Gives you flexibility with the number of urls in a single file

# New Features!

  - Ability to create multiple sitemaps based on classifiers. Classifiers are nothing but different groups for which it is ideal to create different sitemaps. This makes it easier for **indexation problem debugging** as mentioned on the blog [XML Sitemaps] by Moz
  
You can also:
  - Add attributes such as priority, changefreq, lastmod to your urlsets
 
### Requirements

Dillinger uses a number of open source projects to work properly:

* [Python 3] - Python 3 and above
* A well structured excel file with appropriate column names as mentioned below

#### Structuring your excel sheet
![Excel sheet format](https://i.imgur.com/JocoeEb.png)
* The column **_url_** is a **compulsory column** in your excel sheet. This contains the urls of your website
* The **_classifier_** column is an optional column. This contains the classifier based on which the sitemap file will be split into multiple files. If you are including this column in your excel sheet, make sure you use the ```-c``` flag
* The **_lastmod_** column is an optional column. This contains the last modified date of the corresponding url in DD/MM/YYYY format. If you are including this column in your excel sheet, make sure you use the ```-l``` flag
* The **_changefreq_** column is an optional column. This contains the last change frequency of the corresponding url. If you are including this column in your excel sheet, make sure you use the ```-f``` flag
* The **_priority_** column is an optional column. This contains the priority of the corresponding url. If you are including this column in your excel sheet, make sure you use the ```-p``` flag


### Installation

Installation of xl2sitemap requires running the following command form your command line utility

```
pip install xl2sitemap
```

### Running from command line

Running xl2sitemap with the basic default configuration requires running the following command

```
xl2sitemap example-input.xlsx
```
The ```example-input.xlsx``` can be any excel sheet with the appropriate columns in it

Other options that can be enabled are

| Flag | Usage |
| ------ | ------ |
| ```-f``` | Will add ```<changefreq>``` tag in your sitemap |
| ```-p``` | Will add ```<priority>``` tag in your sitemap |
| ```-l``` | Will add ```<lastmod>``` tag in your sitemap |
| ```-c``` | Will split sitemap into multiple files based on the classifier column |
| ```-m 50000``` | Will add a maximum of 500,00 urls only in a single sitemap. If urls are greater than 500,00 then multiple files will be generated|

Example
```
xl2sitemap exmaple-input.xlsx -m 40000 -p -f -l
```
This will generate sitemaps with 400,00 urls in each file with ```<changefreq>```, ```<priority>```, ```<lastmod>``` attributes for each ```<urlset>```.

### Development

Want to contribute? Great!
Open your favorite Terminal and run these commands.
```
git clone https://github.com/antiproblemist/excel-to-sitemap.git
```


License
----

BSD 3-Clause

Author
----
Follow the author on [Linkedin]

**Free Software, Hell Yeah!**


   [XML Sitemaps]: <https://moz.com/blog/xml-sitemaps>
   [Python 3]: <https://www.python.org/downloads/>
   [Linkedin]: <https://www.linkedin.com/in/shahzebq>
