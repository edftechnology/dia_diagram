import ast
import xml.etree.ElementTree as ET
import gzip
import shutil
import os

def parse_python_file(filename):
    """Read a Python file and extract functions, decisions, and loops"""
    with open(filename, "r") as file:
        tree = ast.parse(file.read())

    elements = []
    y = 2
    elements.append(("Flowchart - Ellipse", "Início", (2, y)))
    y += 3

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            elements.append(("Flowchart - Box", f"Função: {node.name}", (2, y)))
            y += 3
        elif isinstance(node, ast.If):
            elements.append(("Flowchart - Preparation", "Decisão (if)", (2, y)))
            y += 3
        elif isinstance(node, (ast.For, ast.While)):
            elements.append(("Flowchart - Box", "Loop", (2, y)))
            y += 3

    elements.append(("Flowchart - Ellipse", "Fim", (2, y)))
    return elements

def generate_dia_xml(elements):
    """Generate Dia-compatible XML from element list"""
    root = ET.Element("dia:diagram", attrib={"xmlns:dia": "http://www.lysator.liu.se/~alla/dia/"})
    diagram_data = ET.SubElement(root, "dia:diagramdata")
    background = ET.SubElement(diagram_data, "dia:attribute", name="background")
    ET.SubElement(background, "dia:color", val="#ffffffff")

    layer = ET.SubElement(root, "dia:layer", name="Fluxograma", visible="true", connectable="true")

    for idx, (shape_type, text, position) in enumerate(elements):
        obj = ET.SubElement(layer, "dia:object", type=shape_type, version="0", id=f"O{idx}")

        pos_attr = ET.SubElement(obj, "dia:attribute", name="obj_pos")
        ET.SubElement(pos_attr, "dia:point", val=f"{position[0]},{position[1]}")

        bb_attr = ET.SubElement(obj, "dia:attribute", name="obj_bb")
        ET.SubElement(bb_attr, "dia:rectangle", val=f"{position[0]-0.1},{position[1]-0.1};{position[0]+2},{position[1]+1.5}")

        text_attr = ET.SubElement(obj, "dia:attribute", name="text")
        ET.SubElement(text_attr, "dia:string", val=text)

    return ET.tostring(root, encoding="unicode")

def save_xml_and_dia(xml_content, output_path_base):
    """Save XML and compress to .dia"""
    xml_filename = output_path_base + ".xml"
    dia_filename = output_path_base + ".dia"

    with open(xml_filename, 'w', encoding='utf-8') as file:
        file.write(xml_content)

    with open(xml_filename, 'rb') as f_in, gzip.open(dia_filename, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    print(f"Arquivo XML salvo em: {xml_filename}")
    print(f"Arquivo DIA salvo em: {dia_filename}")

def generate_flowchart_from_py(input_py):
    """Generate flowchart from Python file with matching name"""
    output_base = os.path.splitext(input_py)[0]
    elements = parse_python_file(input_py)
    xml_content = generate_dia_xml(elements)
    save_xml_and_dia(xml_content, output_base)

# Exemplo de uso:
if __name__ == "__main__":
    generate_flowchart_from_py("docs/analysis_predefined_design.py")
