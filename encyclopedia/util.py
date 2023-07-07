import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import markdown2
import html2text
import random

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
def get_html(title):
    try:
        data = get_entry(str(title))
        html = markdown2.markdown(data)
        return html
    except Exception as e:
        return None

def get_orginal(html):
    html_to_md = html2text.HTML2Text()
    markdown = html_to_md.handle(html)
    print(markdown)
    return markdown

    
def get_list_Similler(title):
    try:
        l_entries = list_entries()
        empty_list = []
        for item in l_entries:
            if(str(title).lower() in str(item).lower()):
                empty_list.append(item)
        if not empty_list:
            return None     
        return empty_list
    except Exception as e:
        print("Error processing item list ")
        return None
def random_entrie():
    List=list_entries()
    length = len(List)
    return List[random.randint(0,length-1)]

