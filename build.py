import os, json, shutil, re, yaml
from datetime import date, datetime
today = date.today()

def interpret(out, md):
    f, full, fullfc = False, "", 0
    p, fullp, fullpc = False, "", 0
    for linet in md:
        line = linet
        if re.search("^# [a-zA-Z0-9]", line) is not None:
            try:
                q = line[line.index(" ")+1:].replace("\n","")
                out.write("<h2>"+q+"</h2> \n")
            except:
                print(line)
        elif re.search("^## [a-zA-Z0-9]", line) is not None:
            try:
                q = line[line.index(" ")+1:].replace("\n","")
                out.write("<h3>"+q+"</h3> \n")
            except:
                print(line)

        elif re.search("^### [a-zA-Z0-9]", line) is not None:
            try:
                q = line[line.index(" ")+1:].replace("\n","")
                out.write("<h4>"+q+"</h4> \n")
            except:
                print(line)
        elif re.search("^$", line) is not None:
            out.write("<br> \n")
        else:
            if re.search("^- ", line) is not None or re.search("^ - ", line) is not None:
                if prev_is_li:
                    line = "<li>"+line[2:].replace("\n","")+"</li> \n"
                else:
                    line = "<li>"+line[2:].replace("\n","")+"</li> \n"

                prev_is_li = True
            else : prev_is_li = False


                # out.write("<li>"+line[2:].replace("\n","")+"</li> \n")

            ## replacing links with a tags
            links = re.findall(r"\[[^\[\]\(\)]+\]\([^\[\]\(\)]+\)", line)
            for match in links:
                text = match[match.index("[")+1:match.index("]")]
                l = match[match.index("(")+1:match.index(")")]
                link = None
                if "http" in l:
                    link = '<a href="'+l+'" target="_blank">'+text+'</a>'
                else:
                    link = '<a href='+l+'>'+text+'</a>'
                line = line.replace(str(match), str(link), 1)

            # replacing italics
            italics = re.findall(r"[^\*]\*[^\*]+\*[^\*]|^\*[^\*]+\*[^\*]|[^\*]\*[^\*]+\*$|^\*[^\*]+\*$", line)
            for match in italics:
                text = match[match.index("*")+1:match[match.index("*")+1:].index("*")+1+match.index("*")]
                tblock = '<i>'+text+'</i>'
                if match[0] == " " : tblock = " " + tblock
                if match[-1] == " " : tblock+= " "
                match = match[match.index("*"):match[match.index("*")+1:].index("*")+2+match.index("*")]
                line = line.replace(match, str(tblock), 1)

            # replacing bolds
            bolds = re.findall(r"[^\*]\*\*[^\*]+\*\*[^\*]|^\*\*[^\*]+\*\*[^\*]|[^\*]\*\*[^\*]+\*\*$|^\*\*[^\*]+\*\*$", line)
            for match in bolds:
                text = match[match.index("**")+2:match[match.index("**")+1:].index("**")+1+match.index("**")]
                tblock = '<b>'+text+'</b>'
                if match[0] == " " : tblock = " " + tblock
                if match[-1] == " " : tblock+= " "
                match = match[match.index("**"):match[match.index("**")+1:].index("**")+3+match.index("**")]
                line = line.replace(str(match), str(tblock), 1)

            if not prev_is_li : out.write(line + "<br> \n")
            else : out.write(line + " \n")

try:
    os.remove("static/index.html")
    os.remove("static/about.html")
    os.remove("static/now.html")
    os.remove("static/thoughts.html")
except:
    pass
    print("no files")

try:
    dirs = ["static/thoughts"]
    for dirv in dirs:
        for f in os.listdir(os.path.join(dirv)):
    	       os.remove(os.path.join(dirv, f))
except:
    print("no dirs needed clearing")

# create index
with open("templates/index.html") as temp, open ("build/index.md") as about:
    out = open("static/index.html", "a")
    for line in temp:
        lt = line
        if "{{content}}" in lt:
            interpret(out, about)
        else : out.write(lt)

with open("templates/about.html") as temp, open ("build/about.md") as about:
    out = open("static/about.html", "a")
    for line in temp:
        lt = line
        if "{{content}}" in lt:
            interpret(out, about)
        else : out.write(lt)

with open("templates/now.html") as temp, open ("build/now.md") as about:
    out = open("static/now.html", "a")
    for line in temp:
        lt = line
        if "{{content}}" in lt:
            interpret(out, about)
        else : out.write(lt)

with open("templates/thoughts.html") as temp, open ("build/thoughts.md") as about:
    out = open("static/thoughts.html", "a")
    for line in temp:
        lt = line
        if "{{content}}" in lt:
            interpret(out, about)
        elif "{{posts}}" in lt:
            items = os.listdir("build/thoughts")
            posts_content = ""
            for d in items:
                tt = d.replace(".md","").replace("-"," ")
                rr = d.replace(".md",".html")
                posts_content += '<li> <a href="thoughts/'+rr+'">'+tt+'</a> </li>\n'

            out.write(posts_content)
        else : out.write(lt)

for d in os.listdir("build/thoughts"):
    with open("templates/thought.html") as temp, open ("build/thoughts/"+d) as about:
        title = d.replace(".md","").replace("-"," ")
        out = open("static/thoughts/"+d.replace(".md",".html"), "a")
        for line in temp:
            lt = line
            if "{{content}}" in lt:
                interpret(out, about)
            elif "{{title}}" in lt:
                out.write(lt.replace("{{title}}", title))
            else : out.write(lt)

