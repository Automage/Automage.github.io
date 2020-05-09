import os
from bs4 import BeautifulSoup

SRC_PATH = "../blog-src/"
OUT_PATH = "../writings/"
TEMPLATE_PATH = "../templates/"


def scan_src_dir(dirpath):
    # Get files in directory and retrieve (path, ctime, title, content)
    files = []
    for filename in os.listdir(dirpath):
        path = os.path.join(dirpath, filename)
        ctime = os.path.getctime(path)
        content = ""
        title = ""

        # Read in content
        with open(path, "r") as file:
            title = file.readline()
            content = title + file.read()

        # Insert tuple
        files.append((path, ctime, title, content))

    # Sort by creation date (ctime). Reversed to order newest file first.
    files.sort(key=lambda tup: tup[1], reverse=True)
    print(files)
    return files


def gen_html(file):
    # Open post template
    with open(TEMPLATE_PATH + "post-template.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # Set head title
    soup.title.string = file[2]

    # Set H1 title tag
    h1_title = soup.find(id="title")
    h1_title.string = file[2]

    # Set date
    date = soup.find(id="date")
    date.string = f"{file[1]}"

    # Convert lines to <p> components and add to html
    body = soup.find(id="content")
    for line in file[3].splitlines():
        p = soup.new_tag("p")
        p.string = line
        body.append(p)

    return soup.prettify()


# Open writings template
with open(TEMPLATE_PATH + "writings-template.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Scan src directory for .txt blog entries
files = scan_src_dir(SRC_PATH)

# Loop through files and generate html for each
i = len(files)
for file in files:
    html = gen_html(file)
    with open(f"{OUT_PATH}{i}.html", 'w') as out_file:
        out_file.write(html)

    i = i - 1
