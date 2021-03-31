"""
This file contains utilities to transform a JSON description of a university program into an HTML form respresenting
the described checksheet.
"""

from .models import ChecksheetTemplate
import json


"""accept an object describing a checksheet (parsed from json) and the title the checksheet should have. Returns a 
string containing and HTML form. """
def render(checksheet, program_title, id_gen=None):
    html = f"<div class=program><h1 class=title>{program_title}</h1>"

    #in order to serialize and unserialize the form state, the inputs and textareas must have a name. Ideally, these
    #names would be shared across checksheets for equivalent programs, allowing for the migration of data between
    #different uni programs. Right now, we just give every input an incrementing id.
    # allowing the id generator to be passed in enables numerous programs to share the same id namespace
    if id_gen == None:
        id_gen = id_generator()

    #checksheets are made up of blocks of related requirements
    html += render_elements(checksheet, id_gen)

    # do some hacky string manipulation to replace elements in parentheses with <span>s. This is used to make a tooltip
    html = html.replace("(", "<span class=tooltip title=\"")
    html = html.replace(")", "\">*</span>")

    html += "</div>"
    return html

def render_elements(checksheet, id_gen):
    html = ""
    for title, data in checksheet.items():
        if data["type"] == "include":
            html += include(title, data, id_gen)
        elif data["type"] == "section":
            html += section(title, data, id_gen)
        else:
            html += reqblock(title, data, id_gen)
    return html


def include(title, data, id_gen):
    program = ChecksheetTemplate.objects.get(name=data["name"])
    obj = json.loads(program.data)
    return render_elements(obj, id_gen)

def section(title, data, id_gen):
    html = "<div class=section><h1>" + title + "<span class=toggle-vis>👁️</span></h1>"
    html += "<p>" + data["description"] + "</p>"
    html += "<div class=contents>" + render_elements(data["data"], id_gen) + "</div>"
    html += "</div>"
    return html

"""Fill in the border, title, and table headers for a requirement block. 

Accepts a string specifying the title, an object defining a requirement, and an id generator. """
def reqblock(title, data, id_gen):
    html = ""
    # each block has a border, title, and table headers
    html += f"<div class=req><h1>{title}</h1><h2>{data['description']}</h2><table>"
    html += "<tr><th>Course</th><th>CR</th><th>Grade</th></tr>"

    # then,
    if data["type"] == "reqlist":
        html += reqlist(data, id_gen)
    elif data["type"] == "creditdemand":
        html += creditdemand(data, id_gen)
    html += "</table></div>"
    return html


def reqlist(data, id_gen):
    html = ""
    for course in data["courses"]:
        html += f"<tr><td>{course[0]}</td><td>{format_credit(course[1], id_gen)}</td><td>{grade_selector(id_gen)}</td></tr>"
    return html


def creditdemand(data, id_gen):
    html = ""
    for slot in range(data["slots"]): #FIXME
        html += f"<tr><td>{course_selector(id_gen)}</td><td>{format_credit(data['credit prefill'], id_gen)}" \
                f"</td><td>{grade_selector(id_gen)}</td></tr>"
    html += f"<tr><td colspan=3>Total Credits: {data['credits'][0]} - {data['credits'][1]}</td></tr>"
    return html


def format_credit(cr, id_gen):
    if cr > 0:
        return str(cr)
    else:
        return f"<input name={next(id_gen)} type='number'/>"

def grade_selector(id_gen):
    return f"""
        <select name={next(id_gen)}>
            <option value="" selected></option>
            <option value=E>E</option>
            <option value=A>A</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B">B</option>
            <option value="B-">B-</option>
            <option value="C+">C+</option>
            <option value="C">C</option>
            <option value="D">D</option>
            <option value=F>F</option>
            <option value=P>P</option>
            <option value=I>I</option>
            <option value=NC>NC</option>
        </select>
    """

def course_selector(id_gen):
    return f"<input name={next(id_gen)} type=text placeholder='course number'/>" + \
           f"<input name={next(id_gen)} type=text placeholder='course name'/>"


def id_generator():
    i = 0
    while True:
        i += 1
        yield i

def test_wrapper(body_html):
    return f"""
    <!doctype html>
    <html>
    <head>
    <title>Checksheet</title>
    <link href="style.css" rel="stylesheet">
    </head>
    <body>
    <div id=wrapper>{body_html}</div>
    <div id=notes><textarea>Record advisement notes here</textarea></div></body>
    </html> """
