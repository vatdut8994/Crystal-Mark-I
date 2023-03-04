# Run the following command to install the required libraries:
# pip install alive_progress bs4 requests pypdf2 colorama termcolor pyfiglet

from alive_progress import alive_bar
from bs4 import BeautifulSoup
from requests import get
from PyPDF2 import PdfReader
import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint 
from pyfiglet import figlet_format

cprint(figlet_format('Extracting Wikipedia'),
       'green', attrs=['bold'])

source = get("https://en.wikipedia.org/wiki/Wikipedia:Contents/A%E2%80%93Z_index").text
soup = BeautifulSoup(source, 'html.parser')
base_url = "https://en.wikipedia.org"

def extract_text(file, first_page=1):
    pdfFileObj = open(file, 'rb')
    pdfReader = PdfReader(pdfFileObj)

    book_write = [str(pdfReader.pages[i].extract_text()) for i in range(first_page-1, len(pdfReader.pages))]
    with open("book.txt", 'a+', encoding="utf-8") as book:
        book.write(book_write)

    pdfFileObj.close()

def filter_file(input, output):
    with open(input, 'r', encoding="utf-8") as reader:
        words = reader.read().split('\n')
    with open(output, 'a', encoding="utf-8") as file2:
        file2.write("\n".join(sorted(set(words), key=words.index)))
    book = open('book.txt', "w")
    book.close()

def mainText(article_link):
    article_soup = BeautifulSoup(get(article_link).text, 'html.parser')
    all_text = article_soup.find('div', class_="mw-parser-output").text
    main_text = [section for section in all_text.split('\n') if len(section.split()) > 15 and section != "" and "|" not in section]
    filtered_text = [section[2:] if section.startswith('^ ') else section for section in main_text]
    return '\n'.join(filtered_text)

wikipedia_dump = open("wikipediaPart2.txt", 'a')
try:
  stop = open("stop.txt", "r")
except:
  stop = open('stop.txt', 'w+')
total_articles = 1

article_start = stop.read()


if article_start == '':
    article_start = 0
else:
    article_start = int(article_start)

stop.close()
print("Starting from index", article_start)

print('Script by Vatsal Dutt.\tEstimated Size: 27GiB\nAll data will be written to "wikipedia.txt"\n\n\n')

with alive_bar(6604261, force_tty=True) as bar:
    for i in soup.find_all('tr'):
        current_article = []
        for link in soup.find_all('a'):
            all_article_links = []
            link = link.get('href')
            if link != None:
                if link.startswith('/wiki/Special:AllPages'):
                    sub_link = base_url+link
                    sub_source = get(sub_link).text
                    sub_soup = BeautifulSoup(sub_source, 'html.parser')
                    for sublink in sub_soup.find_all('a'):
                        sublink = sublink.get('href')
                        if sublink != None:
                            if sublink.startswith('/wiki/'):
                                article_link = base_url+sublink
                                all_article_links.append(article_link)
            all_article_links = all_article_links[:-18]
            for full_link in all_article_links:
                total_articles += 1
                if total_articles > article_start:
                    try:
                        jist_of_article = mainText(full_link)
                        current_article.append(jist_of_article+"\n")
                        wikipedia_dump.write('\n'.join(current_article))
                        with open('stop.txt', 'w') as current:
                            current.write("")
                            current.write(str(total_articles))
                    except:
                        pass
                bar.text('Article: '+full_link.split('/')[-1])
                bar()
print("Download complete!")
wikipedia_dump.close()
