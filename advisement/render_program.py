def render(checksheet, program_title):
    html = f"<div class=program><h1 class=title>{program_title}</h1>"
    id_gen = id_generator()
    for title, data in checksheet.items():
        html += f"<div class=req><h1>{title}</h1><h2>{data['description']}</h2><table>"
        html += "<tr><th>Course</th><th>CR</th><th>Grade</th></tr>"
        if data["type"] == "reqlist":
            html += reqlist(data, id_gen)
        elif data["type"] == "creditdemand":
            html += creditdemand(data, id_gen)
        html += "</table></div>"

    #collapse parentheses
    html = html.replace("(", "<span class=tooltip title=\"")
    html = html.replace(")", "\">*</span>")
    html += "</div>"
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
