import toml
from datetime import datetime
import glob
import re
import bs4

template_index_filename = "template/index.html"
template_post_filename = "template/post.html"

with open("config.toml", "r") as config:
    parsed_config = toml.loads(config.read())

# generate new post based on template
print("Filename:")
new_filename = input()
new_filename = new_filename.strip().lower()
if len(new_filename) > 0:
    if ".html" not in new_filename:
        new_filename = new_filename + ".html"

    # ask for headline
    print("Headline:")
    new_headline = input()

    # build date string
    timestamp = datetime.now()
    today = timestamp.strftime("%d.%m.%Y")

    with open(template_post_filename, "r") as template:
        with open(f"{parsed_config['public_folder']}{parsed_config['post_folder']}/{new_filename}", "w") as new_file:
            template_content = template.read()
            template_content = template_content.replace("[#HEADLINE#]", new_headline)
            template_content = template_content.replace("[#DATE#]", today)
            new_file.write(template_content)

element_list: list[str] = []
element_list.append("<ul>")

rss_output: list[str] = []
rss_output.append('<?xml version="1.0" encoding="utf-8"?>')
rss_output.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
rss_output.append('<channel>')

# read config and read blog posts

    
rss_output.append(f'<title>{parsed_config["title"]}</title>')
rss_output.append(f'<link>{parsed_config["link"]}</link>')
rss_output.append(f'<description>{parsed_config["description"]}</description>')

blog_list: list[str] = []

for filename in glob.glob(f"{parsed_config['public_folder']}{parsed_config['post_folder']}/*.html", recursive=True):
    with open(filename) as f:
        # default values
        headline = ""
        timestamp = datetime.now()
        description = ""

        # parse html content
        content = f.read()
        soup = bs4.BeautifulSoup(content, "html.parser")

        # read and format date
        date_tag_content = soup.find(id="date")
        if date_tag_content:
            date_string = re.search(r"\d\d\.\d\d\.\d\d\d\d", date_tag_content.text)
            if date_string:
                timestamp = datetime.strptime(date_string.group(), "%d.%m.%Y")
        pubdate = timestamp.strftime("%a, %d %b %Y %H:%M:%S +0100")

        # find headline
        headline_tag = soup.find("h1")
        if headline_tag:
            headline = headline_tag.text
        print(headline)

        # find description
        description_tag = soup.find("p")
        if description_tag:
            description = description_tag.text
        
        # build link
        relative_filename = filename.replace(parsed_config['public_folder'], "")
        link = relative_filename
        guid = relative_filename

        rss_output.append(f'<atom:link href="{parsed_config["link"]}{parsed_config["post_folder"]}/feed.rss" rel="self" type="application/rss+xml" />')

        # build items for rss feed
        rss_output.append("<item>")
        rss_output.append(f"<title>{headline}</title>")
        rss_output.append(f"<description>{description}</description>")
        rss_output.append(f'<link>{parsed_config["link"]}{link}</link>')
        rss_output.append(f'<guid>{parsed_config["link"]}{guid}</guid>')
        rss_output.append(f'<pubDate>{pubdate}</pubDate>')
        rss_output.append("</item>")

        # build html elements for index
        element_list.append('<li>')
        element_list.append(f'<a href="{link}">{headline}</a>')
        element_list.append(f'<p>{description}</p>')
        element_list.append('</li>')

rss_output.append('</channel>\n</rss>')
element_list.append("</ul>")

# write rss file
with open(f"{parsed_config['public_folder']}{parsed_config['post_folder']}/feed.rss", "w") as f:
    print("Write feed.rss...")
    f.write("\n".join(rss_output))

# build index based on template
with open(template_index_filename, "r") as f:
    # read file content
    content = f.read()
    # replace placeholder with index elements
    new_content = content.replace("[#BLOG_INDEX#]", "\n".join(element_list))

# write to file
with open(f"{parsed_config['public_folder']}/index.html", "w") as f:
    print("Write index.html...")
    f.write(new_content)
