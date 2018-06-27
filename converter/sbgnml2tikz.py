#!/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
import argparse

from math import degrees
from numpy import arctan2

try:
    import libsbgnpy.libsbgn as libsbgn
except:
    raise(ImportError("Please install package libsbgnpy first\n\t pip install libsbgnpy"))

glyph_dic = {
    "UNSPECIFIED_ENTITY": {"sbgntikz": "unspecified entity", "super": "EPN"},
    "SIMPLE_CHEMICAL": {"sbgntikz": "simple chemical", "super": "EPN"},
    "MACROMOLECULE": {"sbgntikz": "macromolecule", "super": "EPN"},
    "NUCLEIC_ACID_FEATURE": {"sbgntikz": "nucleic acid feature", "super": "EPN"},
    "SIMPLE_CHEMICAL_MULTIMER": {"sbgntikz": "simple chemical multimer", "super": "EPN"},
    "MACROMOLECULE_MULTIMER": {"sbgntikz": "macromolecule multimer", "super": "EPN"},
    "NUCLEIC_ACID_FEATURE_MULTIMER": {"sbgntikz": "nucleic acid feature multimer", "super": "EPN"},
    "COMPLEX": {"sbgntikz": "complex", "super": "EPN"},
    "COMPLEX_MULTIMER": {"sbgntikz": "complex multimer", "super": "EPN"},
    "SOURCE_AND_SINK": {"sbgntikz": "empty set", "super": "EPN"},
    "PERTURBING_AGENT": {"sbgntikz": "perturbation", "super": "EPN"},
    "PERTURATION": {"sbgntikz": "perturbation", "super": "ACTIVITY"},
    "SUB_UNSPECIFIED_ENTITY": {"sbgntikz": "unspecified entity subunit", "super": "SUBUNIT"},
    "SUB_SIMPLE_CHEMICAL": {"sbgntikz": "simple chemical subunit", "super": "SUBUNIT"},
    "SUB_MACROMOLECULE": {"sbgntikz": "macromolecule subunit", "super": "SUBUNIT"},
    "SUB_NUCLEIC_ACID_FEATURE": {"sbgntikz": "nucleic acid feature subunit", "super": "SUBUNIT"},
    "SUB_SIMPLE_CHEMICAL_MULTIMER": {"sbgntikz": "simple chemical multimer subunit", "super": "SUBUNIT"},
    "SUB_MACROMOLECULE_MULTIMER": {"sbgntikz": "macromolecule multimer subunit", "super": "SUBUNIT"},
    "SUB_NUCLEIC_ACID_FEATURE_MULTIMER": {"sbgntikz": "nucleic acid feature multimer subunit", "super": "SUBUNIT"},
    "SUB_COMPLEX": {"sbgntikz": "complex subunit", "super": "SUBUNIT"},
    "SUB_COMPLEX_MULTIMER": {"sbgntikz": "complex multimer subunit", "super": "SUBUNIT"},
    "PROCESS": {"sbgntikz": "generic process", "super": "PROCESS"},
    "OMITTED_PROCESS": {"sbgntikz": "omitted process", "super": "PROCESS"},
    "UNCERTAIN_PROCESS": {"sbgntikz": "uncertain process", "super": "PROCESS"},
    "ASSOCIATION": {"sbgntikz": "association", "super": "PROCESS"},
    "DISSOCIATION": {"sbgntikz": "dissociation", "super": "PROCESS"},
    "PHENOTYPE": {"sbgntikz": "phenotype", "super": "PROCESS"},
    "OR": {"sbgntikz": "or", "super": "LOGICAL_OPERATOR"},
    "AND": {"sbgntikz": "and", "super": "LOGICAL_OPERATOR"},
    "NOT": {"sbgntikz": "not", "super": "LOGICAL_OPERATOR"},
    "DELAY": {"sbgntikz": "delay", "super": "LOGICAL_OPERATOR"},
    "CATALYSIS": {"sbgntikz": "catalysis", "super": "MODULATION"},
    "MODULATION": {"sbgntikz": "modulation", "super": "MODULATION"},
    "STIMULATION": {"sbgntikz": "stimulation", "super": "MODULATION"},
    "INHIBITION": {"sbgntikz": "inhibition", "super": "MODULATION"},
    "UNKNOWN_INFLUENCE": {"sbgntikz": "modulation", "super": "MODULATION"},
    "POSITIVE_INFLUENCE": {"sbgntikz": "stimulation", "super": "MODULATION"},
    "NEGATIVE_INFLUENCE": {"sbgntikz": "inhibition", "super": "MODULATION"},
    "NECESSARY_STIMULATION": {"sbgntikz": "necessary stimulation", "super": "MODULATION"},
    "ABSOLUTE_STIMULATION": {"sbgntikz": "absolute stimulation", "super": "MODULATION"},
    "ABSOLUTE_INHIBITION": {"sbgntikz": "absolute inhibition", "super": "MODULATION"},
    "CONSUMPTION": {"sbgntikz": "consumption", "super": "FLUX_ARC"},
    "PRODUCTION": {"sbgntikz": "production", "super": "FLUX_ARC"},
    "EQUIVALENCE_ARC": {"sbgntikz": "equivalence arc", "super": None},
    "LOGIC_ARC": {"sbgntikz": "logic arc", "super": None},
    "STATE_VARIABLE": {"sbgntikz": "sv", "super": None},
    "UNIT_OF_INFORMATION": {"sbgntikz": "ui", "super": None},
    "CARDINALITY": {"sbgntikz": "ui", "super": "UNIT_OF_INFORMATION"},
    "COMPARTMENT": {"sbgntikz": "compartment", "super": None},
    "BIOLOGICAL_ACTIVITY": {"sbgntikz": "biological activity", "super": "ACTIVITY"},
    "ENTITY": {"sbgntikz": "entity", "super": None},
    "EXISTENCE": {"sbgntikz": "sv existence", "super": "STATE_VARIABLE"},
    "LOCATION": {"sbgntikz": "sv location", "super": "STATE_VARIABLE"},
    "INTERACTION_NODE": {"sbgntikz": "nary", "super": None},
    "INTERACTION_ARC": {"sbgntikz": "interaction", "super": None},
    "ASSIGNMENT": {"sbgntikz": "assignment", "super": None},
    "VARIABLE_VALUE": {"sbgntikz": "sv", "super": None},
    "OUTCOME": {"sbgntikz": "outcome", "super": None},
    "SUBMAP": {"sbgntikz": "submap", "super": None},
    "TERMINAL": {"sbgntikz": "tag", "super": "TAG"},
    "TAG": {"sbgntikz": "tag", "super": None},
    "IMPLICIT_XOR": {"sbgntikz": "implicit xor", "super": None}
}

def float_to_distance(x, unit = "pt"):
    return str(x) + unit

"""Returns the center of a bbox as a position"""
def center_as_position(bbox, unit = "pt"):
    return (float_to_distance(bbox.x + bbox.w /2, unit), float_to_distance(bbox.y + bbox.h / 2, unit))

"""Computes the angle between the horizontal of the center of bbox1 and the center of p2 if p2 is a bbox, or p2 if it is a point"""
def compute_angle(bbox1, bbox2, point = "center"):
    center1 = (bbox1.x + bbox1.w/2, bbox1.y + bbox1.h/2)
    if hasattr(bbox2, "w"):
        if point == "center":
            center2 = (bbox2.x + bbox2.w/2, bbox2.y + bbox2.h/2)
        elif point == "west":
            center2 = (bbox2.x, bbox2.y + bbox2.h/2)
        elif point == "east":
            center2 = (bbox2.x + bbox2.w, bbox2.y + bbox2.h/2)
        elif point == "north":
            center2 = (bbox2.x + bbox2.w/2, bbox2.y)
        elif point == "south":
            center2 = (bbox2.x + bbox2.w/2, bbox2.y + bbox2.h)
    else:
        center2 = (bbox2.x, bbox2.y)
    # return round(degrees(atan2(center2[1] - center1[1], center2[0] - center1[0])))
    return round(degrees(arctan2(center2[1] - center1[1], center2[0] - center1[0])))

"""Returns True if the line defined by point1 and point2 points to the center of the bbox, with a vertical error of error"""
def points_to_center(point1, point2, bbox, error = 3):
    dx = point2.x - point1.x
    x = bbox.x + bbox.w / 2
    if dx == 0:
        if x > point1.x - error and x < point1.x + error:
            return True
    else:
        a = (point2.y - point1.y) / dx
        b = point1.y - a * point1.x
        y = bbox.y + bbox.h / 2
        yy = a * x + b
        if y > yy - error and y < yy + error:
            return True
    return False

def normalize_name(name):
    return name.replace(".", "_")

def normalize_label(label):
    label = label.replace("\n","\\\\")
    label = label.replace("_","\\_")
    label = label.replace("β","$\\beta$")
    label = label.replace("α","$\\alpha$")
    label = label.replace("γ","$\\gamma$")
    return label

def node_string(label, name = None, position = None, keys = None):
    s = "\\node"
    if label and "\\" in label:
        keys["align"] = "center"
    if keys:
        s += "[{}] ".format(", ".join(["{}={}".format(key, keys[key]) if keys[key] else "{}".format(key) for key in keys]))
    else:
        s += " "
    if name:
        s += "({}) ".format(name)
    if position:
        s += "at ({}) ".format(",".join(position))
    s += "{{{}}};".format(label) if label else "{};"
    return s

def arc_string(positions, keys = None):
    s = "\\draw"
    if keys:
        s += "[{}] ".format(", ".join(["{}={}".format(key, keys[key]) if keys[key] else "{}".format(key) for key in keys]))
    else:
        s += " "
    if positions:
        s += " -- ".join(["({})".format(",".join(position)) for position in positions])
    s += ";"
    return s

def sbgn_node_to_string(node, nodes_dic, ports_dic, tidy = False, keep_sizes = True, unit = "pt"):
    nodes_dic[node.get_id()] = node
    class_name = node.get_class().name
    if class_name == "INTERACTION":
        class_name = "INTERACTION_NODE"
    l = []
    keys = OrderedDict()
    keys[glyph_dic[class_name]["sbgntikz"]] = None
    if node.get_class().name == "COMPARTMENT":
        keys["shape"] = "rectangle"
        keys["rounded corners"] = "20pt"
    if node.get_clone():
        keys["clone"] = None
    label = node.get_label()
    if label:
        label_text = normalize_label(label.get_text())
    else:
        label_text = None
    state = node.get_state()
    if state:
        label_text = ""
        if state.value:
            label_text += state.value
        if state.variable:
            label_text += "@{}".format(state.variable)
    name = normalize_name(node.get_id())
    bbox = node.get_bbox()
    # if keep_sizes:
    keys["minimum width"] = float_to_distance(bbox.w, unit)
    keys["minimum height"] = float_to_distance(bbox.h, unit)
    # keys["anchor"] = "north west"
    position = center_as_position(bbox)
    for subnode in node.get_glyph():
        l += sbgn_subnode_to_string(subnode, node, nodes_dic, tidy, keep_sizes, unit)
    if glyph_dic[class_name]["super"] == "PROCESS" or glyph_dic[class_name]["super"] == "LOGICAL_OPERATOR":
        ports = node.get_port()
        for port in ports:
            if port.x < bbox.x:
                keys["connectors"] = "horizontal"
                keys["left connector length"] = float_to_distance(bbox.x - port.x, unit)
                if tidy:
                    ports_dic[port.get_id()] = ("{}.west".format(name),)
            elif port.x > bbox.x + bbox.w:
                keys["right connector length"] = float_to_distance(port.x - (bbox.x + bbox.w), unit)
                if tidy:
                    ports_dic[port.get_id()] = ("{}.east".format(name),)
            elif port.y < bbox.y:
                keys["connectors"] = "vertical"
                keys["left connector length"] = float_to_distance(bbox.y - port.y, unit)
                if tidy:
                    ports_dic[port.get_id()] = ("{}.north".format(name),)
            elif port.y > bbox.y + bbox.h:
                keys["right connector length"] = float_to_distance(port.y - (bbox.y + bbox.h), unit)
                if tidy:
                    ports_dic[port.get_id()] = ("{}.south".format(name),)
    l.append(node_string(label_text, name, position, keys))
    l = reversed(l)
    return l

def sbgn_subnode_to_string(subnode, node, nodes_dic, tidy = False, keep_sizes = True, unit = "pt"):
    nodes_dic[subnode.get_id()] = subnode
    class_name = subnode.get_class().name
    l = []
    keys = OrderedDict()
    entity = subnode.get_entity()
    if entity: # if AF ui
        keys["ui {}".format(entity.get_name())] = None
    else:
        keys[glyph_dic[class_name]["sbgntikz"]] = None
        if class_name == "STATE_VARIABLE":
            keys["shape"] = "ellipse"
    label = subnode.get_label()
    if label:
        label_text = normalize_label(label.get_text())
    else:
        label_text = None
    state = subnode.get_state()
    if state: # if state variable
        label_text = ""
        if state.value:
            label_text += state.value
        if state.variable:
            label_text += "@{}".format(state.variable)
    name = normalize_name(subnode.get_id())
    bbox = subnode.get_bbox()
    if class_name == "TERMINAL":
        orientation = subnode.orientation
        keys["orientation"] = orientation
    if tidy:
        if glyph_dic[class_name]["super"] == "STATE_VARIABLE" or glyph_dic[class_name]["super"] == "UNIT_OF_INFORMATION" or class_name == "TERMINAL":
            if class_name == "TERMINAL":
                if orientation == "right":
                    point = "west"
                elif orientation == "left":
                    point = "east"
                elif orientation == "up":
                    point = "north"
                elif orientation == "down":
                    point = "south"
            else:
                point = "center"
            angle = compute_angle(node.get_bbox(), bbox, point)
            position = ("{}.{}".format(normalize_name(node.get_id()), -angle),)
            keys["anchor"] = point
        else:
            position = center_as_position(bbox)
    else:
        if class_name == "TERMINAL": # special case because center in sbgntikz is not the center of the bbox
            if orientation == "down" or orientation == "right":
                keys["anchor"] = "north west"
                position = (float_to_distance(bbox.x), float_to_distance(bbox.y))
            else:
                keys["anchor"] = "south east"
                position = (float_to_distance(bbox.x + bbox.w), float_to_distance(bbox.y + bbox.h))
        else:
            position = center_as_position(bbox)
    keys["minimum width"] = float_to_distance(bbox.w)
    if class_name == "EXISTENCE" or class_name == "LOCATION": # those are circles, we take just the width (to avoid SBGN-ED's bug)
        keys["minimum height"] = "0pt"
    else:
        keys["minimum height"] = float_to_distance(bbox.h)
    for subsubnode in subnode.get_glyph():
        l += sbgn_subnode_to_string(subsubnode, subnode, nodes_dic, tidy, keep_sizes, unit = "pt")
    l.append(node_string(label_text, name, position, keys))
    # l = reversed(l)
    return l

def sbgn_arc_to_string(arc, nodes_dic, ports_dic, tidy = False, keep_sizes = True, unit = "pt"):
    l = []
    keys = OrderedDict()
    class_name = arc.get_class().name
    if class_name == "INTERACTION":
            class_name = "INTERACTION_ARC"
    keys[glyph_dic[class_name]["sbgntikz"]] = None
    if class_name == "INTERACTION_ARC" or class_name == "ASSIGNMENT":
        target = arc.get_target()
        if target in nodes_dic:
            node = nodes_dic[target]
            if node.get_class().name == "INTERACTION":
                keys["{}-"] = None
            if node.get_class().name == "IMPLICIT_XOR":
                keys["-{}"] = None
    positions = []
    if tidy:
        source = arc.get_source()
        if source in ports_dic:
            positions.append(ports_dic[source])
        else:
            source_node = nodes_dic[source]
            start = arc.get_start()
            nexts = arc.get_next()
            if nexts:
                n = nexts[0]
            else:
                n = arc.get_end()
            if points_to_center(start, n, source_node.get_bbox()):
                positions.append((normalize_name(source),))
            else:
                angle = compute_angle(source_node.get_bbox(), start)
                positions.append(("{}.{}".format(normalize_name(source), -angle),))
    else:
        start = arc.get_start()
        positions.append((float_to_distance(start.x, unit),float_to_distance(start.y, unit)))
    nexts = arc.get_next()
    for n in nexts:
        positions.append((float_to_distance(n.x, unit),float_to_distance(n.y, unit)))
    if tidy:
        target = arc.get_target()
        if target in ports_dic:
            positions.append(ports_dic[target])
        else:
            target_node = nodes_dic[target]
            end = arc.get_end()
            if nexts:
                n = nexts[-1]
            else:
                start = arc.get_start()
                n = start
            if points_to_center(n, end, target_node.get_bbox()):
                positions.append((normalize_name(target),))
            else:
                angle = compute_angle(target_node.get_bbox(), end)
                positions.append(("{}.{}".format(normalize_name(target), -angle),))
    else:
        end = arc.get_end()
        positions.append((float_to_distance(end.x, unit),float_to_distance(end.y, unit)))
    l.append(arc_string(positions, keys))
    return l

def sbgn_arc_nodes_and_ports_to_string(arc, nodes_dic, ports_dic, tidy = False, keep_sizes = True, unit = "pt"):
    l = []
    if tidy:
        ports = arc.get_port()
        if ports:
            for port in ports:
                l.append(node_string(None, normalize_name(port.get_id()), (float_to_distance(port.x, unit),float_to_distance(port.y, unit)), {"anchor point": None}))
                ports_dic[port.get_id()] = (normalize_name(port.get_id()),)
    for node in arc.get_glyph():
        l += sbgn_node_to_string(node, nodes_dic, ports_dic, tidy, keep_sizes, unit)
        nodes_dic[node.get_id()] = node
    return l

def sbgn_arcgroup_nodes_and_ports_to_string(arc, nodes_dic, ports_dic, tidy = False, keep_sizes = True, unit = "pt"):
    l = []
    for node in arcgroup.get_glyph():
        l += sbgn_node_to_string(node, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    for arc in arcgroup.get_arc():
        l += sbgn_arc_nodes_and_ports_to_string(arc, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    return l

def sbgnml_to_tikzpicture(filename, tidy = False, keep_sizes = True, unit = "pt"):
    ports_dic = {}
    nodes_dic = {}
    if not keep_sizes:
        tidy = True
    sbgn = libsbgn.parse(filename, silence=True)
    sbgnmap = sbgn.get_map()
    l = []
    for node in sbgnmap.get_glyph():
        l += sbgn_node_to_string(node, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    for arcgroup in sbgnmap.get_arcgroup():
        l += sbgn_arc_nodes_and_ports_to_string(arcgroup, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    for arc in sbgnmap.get_arc():
        l += sbgn_arc_nodes_and_ports_to_string(arc, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    for argroup in sbgnmap.get_arcgroup():
        for arc in arcgroup.get_arc():
            l += sbgn_arc_to_string(arcgroup, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    for arc in sbgnmap.get_arc():
        l += sbgn_arc_to_string(arc, nodes_dic, ports_dic, tidy, keep_sizes, unit)
    s = "\\begin{tikzpicture}[sbgn, yscale=-1]\n"
    s += "\n".join(l)
    s += "\n\\end{tikzpicture}"
    return s

def tikzpicture_to_pdf(s, output):
    try:
        from pylatex import Document, NoEscape
    except:
        raise(ImportError("Please install package pylatex first\n\t pip install pylatex"))
    if output.endswith(".pdf"):
        output = output[:-4]
    doc = Document(documentclass = "standalone")
    doc.preamble.append(NoEscape("\\usepackage[utf8]{inputenc}"))
    doc.preamble.append(NoEscape("\\usepackage{tikz}"))
    doc.preamble.append(NoEscape("\\usetikzlibrary{sbgn}"))
    doc.append(NoEscape(s))
    doc.generate_pdf(output, clean = True, clean_tex = True)

def tikzpicture_to_tex(s, output):
    f = open(output, "w")
    f.write(s)
    f.close()

def tikzpicture_to_string(s): #someday we might add some fancy stuff
    return s

if __name__ == '__main__':
    usage = "%(prog)s SBGN-ML FILE"
    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument("--no-tidy", dest = "tidy", action = "store_false", default = True, help = "draw the map only using coordinates")
    parser.add_argument("--tex", dest = "tex", default = None, help="output to a tex file")
    parser.add_argument("--pdf", dest = "pdf", default = None, help="output to a pdf file")
    parser.add_argument("--unit", dest = "unit", default = "pt", help="the length unit to be used (pt, cm, in, px)")
    parser.add_argument("input", help="SBGN-ML FILE")

    args = parser.parse_args()

    s = sbgnml_to_tikzpicture(args.input, args.tidy, True, args.unit)
    if args.pdf:
        tikzpicture_to_pdf(s, args.pdf)
    if args.tex:
        tikzpicture_to_tex(s, args.tex)
    if not args.pdf and not args.tex:
        print(tikzpicture_to_string(s))
