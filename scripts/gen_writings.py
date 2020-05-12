#
# Script to generate html entries from blog-src/ txt files.
# To be called ONLY by build.sh
#

import os
import datetime
from bs4 import BeautifulSoup

SRC_PATH = "blog-src/"
OUT_PATH = "writings/"
BLOG_OUT_PATH = "writings.html"
TEMPLATE_PATH = "templates/"


def format_time(ts):
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st


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
            content = file.read()

        # Insert tuple
        files.append((path, ctime, title, content))

    # Sort by creation date (ctime). Reversed to order newest file first.
    files.sort(key=lambda tup: tup[1], reverse=True)
    return files


def gen_post_html(file):
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
    time = format_time(file[1])
    date.string = f"{time}"

    # Convert lines to <p> components and add to html
    body = soup.find(id="content")
    for line in file[3].splitlines():
        p = soup.new_tag("p")
        p.string = line
        body.append(p)
    
    print(soup.prettify(formatter=None))
    return soup.prettify(formatter=None)


def gen_blog_html(files):
    # Open writings template
    with open(TEMPLATE_PATH + "writings-template.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # Generate table of contents of all posts
    posts = soup.find(id="posts")
    ul = soup.new_tag("ul")
    i = len(files)
    for file in files:
        li = soup.new_tag("li")
        a = soup.new_tag("a", href=f"{OUT_PATH}{i}.html")
        date = format_time(file[1])
        a.string = file[2]
        li.append(a)
        li.append(f" | Date modifed: {date}")
        ul.append(li)
        i = i - 1

    posts.append(ul)
    return soup.prettify()


# Scan src directory for .txt blog entries
files = scan_src_dir(SRC_PATH)

# Loop through files and generate html for each
i = len(files)
for file in files:
    html = gen_post_html(file)
    with open(f"{OUT_PATH}{i}.html", 'w') as out_file:
        out_file.write(html)

    i = i - 1

# Generate writings.html
html = gen_blog_html(files)
with open(BLOG_OUT_PATH, "w") as out_file:
    out_file.write(html)
