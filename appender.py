# Import stuff
import argparse
import configparser
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(filename="appender.log", level=logging.DEBUG)
log = logging.getLogger(__name__)

def main(args):
    config = read_config(args)
    xml_tree = initialize_element_tree(config['input']['input_file'])
    appended_tree = add_keywords(xml_tree, config)
    write_output(appended_tree)

def read_config(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    return config

# Adds the namespaces to ET and parses the input file
def initialize_element_tree(file_location):
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    ET.register_namespace('schemaLocation', "http://standards.iso.org/iso/19115/-3/mdb/2.0 https://schemas.isotc211.org/19115/-3/mdb/2.0/mdb.xsd")
    ET.register_namespace('gml' , "http://www.opengis.net/gml/3.2")
    ET.register_namespace('mpc',"http://standards.iso.org/iso/19115/-3/mpc/1.0")
    ET.register_namespace('mri', 'http://standards.iso.org/iso/19115/-3/mri/1.0')
    ET.register_namespace('mrl', "http://standards.iso.org/iso/19115/-3/mrl/2.0")
    ET.register_namespace('mmi', "http://standards.iso.org/iso/19115/-3/mmi/1.0")
    ET.register_namespace('mdb', 'http://standards.iso.org/iso/19115/-3/mdb/2.0')
    ET.register_namespace('mcc', "http://standards.iso.org/iso/19115/-3/mcc/1.0")
    ET.register_namespace('msr', "http://standards.iso.org/iso/19115/-3/msr/2.0")
    ET.register_namespace('mac', "http://standards.iso.org/iso/19115/-3/mac/2.0")
    ET.register_namespace('cit', "http://standards.iso.org/iso/19115/-3/cit/2.0")
    ET.register_namespace('mrs', "http://standards.iso.org/iso/19115/-3/mrs/1.0")
    ET.register_namespace('gco', 'http://standards.iso.org/iso/19115/-3/gco/1.0')
    ET.register_namespace('lan', 'http://standards.iso.org/iso/19115/-3/lan/1.0')
    ET.register_namespace('mco', "http://standards.iso.org/iso/19115/-3/mco/1.0")
    ET.register_namespace('gex', "http://standards.iso.org/iso/19115/-3/gex/1.0")
    ET.register_namespace('mdq', "http://standards.iso.org/iso/19157/-2/mdq/1.0")
    ET.register_namespace('mas', "http://standards.iso.org/iso/19115/-3/mas/1.0")
    ET.register_namespace('mrd', "http://standards.iso.org/iso/19115/-3/mrd/1.0")
    ET.register_namespace('mrc', "http://standards.iso.org/iso/19115/-3/mrc/2.0")
    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
    tree = ET.parse(file_location)
    return tree      

# Adding restricted keywords to the element tree
# Assumption that none already exist
# TODO: See if any issues with running on one that already has restricted
# under mdb:identification > mri:MD_DataIdentification
def add_keywords(tree, config):
    namespaces = {'mri':'http://standards.iso.org/iso/19115/-3/mri/1.0', 'gco':'http://standards.iso.org/iso/19115/-3/gco/1.0',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'lan': 'http://standards.iso.org/iso/19115/-3/lan/1.0', 'mdb': 'http://standards.iso.org/iso/19115/-3/mdb/2.0'}

    # Creates the subelement that will contain all the restricted information
    # TODO: Try to use an existing template and insert? 
    et_subelement_root = ET.Element("mri:descriptiveKeywords")
    et_keywords = ET.SubElement(et_subelement_root, "mri:MD_Keywords")

    # Sets the element text to the keyword
    keywords_en = split_config_list(config['restricted_keywords']['en'])
    for x in keywords_en:
        ET.SubElement(ET.SubElement(et_keywords, "mri:keyword"), "gco:CharacterString").text = x

    keywords_fr = split_config_list(config['restricted_keywords']['fr'])
    for x in keywords_fr:
        et_keyword_fr = ET.SubElement(et_keywords, "mri:keyword")
        et_keyword_fr.set(ET.QName('http://www.w3.org/2001/XMLSchema-instance', 'type'),'lan:PT_FreeText_PropertyType')
        ET.SubElement(ET.SubElement(ET.SubElement(et_keyword_fr, "lan:PT_FreeText"),"lan:textGroup"),"lan:LocalisedCharacterString", locale = '#fr').text = x

    # Adds the class name to the subelement
    et_keyword_class = ET.SubElement(ET.SubElement(et_keywords, "mri:keywordClass"), "mri:MD_KeywordClass")
    et_class_name = ET.SubElement(et_keyword_class, 'mri:className')
    et_class_name.set(ET.QName('http://www.w3.org/2001/XMLSchema-instance', 'type'),'lan:PT_FreeText_PropertyType')
    ET.SubElement(et_class_name, "gco:CharacterString").text = config['restricted_template']['class_name']

    # Sets up citation to add the title and online resource below
    et_citation = ET.SubElement(ET.SubElement(et_keyword_class, "mri:ontology"), "cit:CI_Citation")

    # Adds citation title information
    et_citation_title = ET.SubElement(et_citation, "cit:title")
    ET.SubElement(et_citation_title, "gco:CharacterString").text = config['restricted_template']['citation_title']

    # Adds online resource information
    et_linkage = ET.SubElement(ET.SubElement(ET.SubElement(et_citation, "cit:onlineResource"), "cit:CI_OnlineResource"), "cit:linkage")
    ET.SubElement(et_linkage, "gco:CharacterString").text = config['restricted_template']['online_resource']

    # Inserts the section with the other descriptiveKeyword sections
    # TODO: Unsure if constant or will need to be detected
    # Can do a find for descriptiveKeywords, find index of the last one and place after it
    et_data_identification = tree.find(".//mri:MD_DataIdentification", namespaces)
    et_data_identification.insert(len(et_data_identification) - 2, et_subelement_root)
    ET.indent(et_data_identification, level =2)
    return tree

def write_output(tree):
    with open("output/test_output.xml", 'w') as f:
        tree.write(f, encoding='unicode')

def split_config_list(config_list):
    split_list = [x.strip() for x in config_list.split(",")]
    return split_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        help="Config file to be used",
        default="appender_config.ini",
        action="store",
    )
    args = parser.parse_args()

    main(args)