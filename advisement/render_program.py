def render(checksheet, program_title):
    html = f"<div class=program><h1 class=title>{program_title}</h1>"
    for title, data in checksheet.items():
        html += f"<div class=req><h1>{title}</h1><h2>{data['description']}</h2><table>"
        html += "<tr><th>Course</th><th>CR</th><th>Grade</th></tr>"
        if data["type"] == "reqlist":
            html += reqlist(data)
        elif data["type"] == "creditdemand":
            html += creditdemand(data)
        html += "</table></div>"

    #collapse parentheses
    html = html.replace("(", "<span class=tooltip title=\"")
    html = html.replace(")", "\">*</span>")
    html += "</div>"
    return html


def reqlist(data):
    html = ""
    for course in data["courses"]:
        html += f"<tr><td>{course[0]}</td><td>{format_credit(course[1])}</td><td>{grade_selector()}</td></tr>"
    return html


def creditdemand(data):
    html = ""
    for slot in range(data["slots"]): #FIXME
        html += f"<tr><td>{course_selector()}</td><td>{format_credit(data['credit prefill'])}" \
                f"</td><td>{grade_selector()}</td></tr>"
    html += f"<tr><td colspan=3>Total Credits: {data['credits'][0]} - {data['credits'][1]}</td></tr>"
    return html


def format_credit(cr):
    if cr > 0:
        return str(cr)
    else:
        return "<input type='number'/>"

def grade_selector2():
    return """
        <select>
            <option value="" selected></option>
            <option value=A>A</option>
            <option value=B>B</option>
            <option value=C>C</option>
            <option value=D>D</option>
            <option value=F>F</option>
            <option value=P>P</option>
            <option value=PC>PC</option>
            <option value=NC>NC</option>
        </select>
        <select>
            <option value="+">+</option>
            <option value="" selected> </option>
            <option value="-">-</option>
        </select>
    """

def grade_selector():
    return """
        <select>
            <option value="" selected></option>
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
def course_selector():
    return """<input type=text placeholder='course number'/><input type=text placeholder='course name'/>"""


def id_generator():
    for i in range(9999999):
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