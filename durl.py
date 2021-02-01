import requests
import sys
import os

from bs4 import BeautifulSoup

def main():
    url = sys.argv[1]
    destination = sys.argv[2]

    uhead, utail = os.path.split(url)

    # make dir to put downloaded files into
    try:
        os.mkdir(destination)
    except OSError as error:
        print(error)
    finally:
        print("{} directory created".format(destination))

    # get links from soup
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')

    filecount = 0
    # check each link for pdfs and download
    for link in links:
        if link.has_attr('href') and ('.pdf' in link.get('href', [])):
            filecount += 1
            print("Downloading file {} from {} ".format(filecount, link['href']))

            # Get response object for link
            # if doesn't work, try relative link
            try:
                link_href = link.get('href')
                response = requests.get(link_href)
            except requests.exceptions.MissingSchema as error:
                trypath = os.path.join(uhead, link_href)
                response = requests.get(trypath)
                print("Got response from relative path {}".format(trypath))
            finally:
                print("Got response from file path {}".format(link_href))

            # create whole path for pdf
            pdfname = os.path.basename(link_href)
            pdfpath = os.path.join(destination, pdfname)
            
            # Write content in pdf file
            pdf = open(pdfpath, 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File ", filecount, " downloaded to {}\n".format(pdfpath))

    print("All PDF files downloaded from {}".format(url))


if __name__ == '__main__': main()

