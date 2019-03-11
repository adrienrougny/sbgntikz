from os import listdir
from os.path import isfile, join

from pylatex import Document, NoEscape

from sbgnml2tikz import *
sbgnml_path = "examples/sbgnml"
pdf_path = "examples/pdf"
tex_path = "examples/tex"

for f in listdir(sbgnml_path):
    if f.endswith(".sbgn"):
        if isfile(join(sbgnml_path, f)):
            for name in ["", "_tidy"]:
                print(f, name)
                if name == "":
                    s = sbgnml_to_tikzpicture(join(sbgnml_path, f), tidy = False, keep_sizes = True)
                else:
                    s = sbgnml_to_tikzpicture(join(sbgnml_path, f), tidy = True, keep_sizes = True)
                doc = Document(documentclass = "standalone")
                doc.preamble.append(NoEscape("\\usepackage[utf8]{inputenc}"))
                doc.preamble.append(NoEscape("\\usepackage{tikz}"))
                doc.preamble.append(NoEscape("\\usetikzlibrary{sbgn}"))
                doc.append(NoEscape(s))
                doc.generate_tex(join(tex_path, f.split(".")[0] + name))
                doc.generate_pdf(join(pdf_path, f.split(".")[0] + name), clean_tex = True)
