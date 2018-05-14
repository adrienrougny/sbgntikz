import libsbgnpy.libsbgn as libsbgn

sbgnml_to_tikz = {
    "MACROMOLECULE": "macromolecule",
    "PROCESS": "generic process",
    "STATE_VARIABLE": "sv",
    "UNIT_OF_INFORMATION": "ui",
    "CONSUMPTION": "consumption",
    "PRODUCTION": "production",
    "CATALYSIS": "catalysis"
}

def float_to_distance(x, unit = "pt"):
    return str(x) + unit

def node_string(label, name = None, position = None, keys = None):
    s = "\\node"
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

def sbgn_node_to_string(node):
    l = []
    keys = {}
    keys[sbgnml_to_tikz[node.get_class().name]] = None
    if node.get_clone():
        keys["clone"] = None
    label = node.get_label()
    if label:
        label_text = label.get_text()
    else:
        label_text = None
    state = node.get_state()
    if state:
        label_text = ""
        if state.value:
            label_text += state.value
        if state.variable:
            label_text += "@{}".format(state.variable)
    name = node.get_id()
    bbox = node.get_bbox()
    keys["minimum width"] = float_to_distance(bbox.w)
    keys["minimum height"] = float_to_distance(bbox.h)
    keys["anchor"] = "south west"
    position = (float_to_distance(bbox.x), float_to_distance(bbox.y))
    for subnode in node.get_glyph():
        l += sbgn_node_to_string(subnode)
    # if node.get_class().name == "PROCESS":
    #     l = node.get_port()
    #     for port in l:
    #         print(port.x)
    l.append(node_string(label_text, name, position, keys))
    return l

def sbgn_arc_to_string(arc):
    keys = {}
    keys[sbgnml_to_tikz[arc.get_class().name]] = None
    positions = []
    start = arc.get_start()
    positions.append((float_to_distance(start.x),float_to_distance(start.y)))
    end = arc.get_end()
    positions.append((float_to_distance(end.x),float_to_distance(end.y)))
    return arc_string(positions, keys)
