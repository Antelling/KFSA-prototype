import json, os
try:
    import render_program
except ImportError:
    from . import render_program

program_files = os.listdir(os.path.join(os.getcwd(), "programs"))
programs = []
for file in program_files:
    cs = open(os.path.join(os.getcwd(), "programs", file), "r").read()
    html = render_program.render(json.loads(cs), str(file.split(".")[0]).replace("_", " "))
    programs.append(html)
html = render_program.test_wrapper(",".join(programs))

f = open("output.html", "w")
f.write(html)
f.close()
