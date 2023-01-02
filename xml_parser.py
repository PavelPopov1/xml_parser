# importing requests for get xml by the url and lib for xml
import requests
import xml.etree.ElementTree as ET

# custom tree class
from tree_class import TreeNode


def xml_parser(url):
    """
    Function for building tree of categories by XML from specific URL

    :param url: url path for get specific xml for parsing
    :return: tree of categories by xml string
    """

    def calculate_count(xml_root, cur_id):
        """
        Calculate count of specific category in list of offers in xml tree

        :param xml_root: root of xml tree
        :param cur_id: id specific category for calculate
        :return: count of specific category in list of orders
        """
        # counter for category
        count_counter = 0

        # searching for specific category in the list of orders
        for offer in xml_root.findall('shop/offers/offer'):
            # if found
            if int(cur_id) == int(offer.findall('categoryId')[0].text):
                count_counter += 1
                # remove the order from general list of orders from xml tree
                # to speed up the search for the next steps
                xml_root.findall('shop/offers')[0].remove(offer)

        return count_counter

    def find_all_rootes(xml_root):
        """
        Finding all category rootes in xml tree

        :param xml_root: root of xml tree
        :return: highest root which relates all roots of categories
        """
        # create basic root
        basic_root = TreeNode(0, "Root of all rootes", 0)

        # looking for all category roots and relate its with basic root
        for category in xml_root.findall('shop/categories/category'):
            if category.get("parentId") is None:

                # create, add root and calculate count of offers for this root
                basic_root.add_child(
                    TreeNode(category.attrib["id"], category.text,
                             calculate_count(xml_root, category.attrib["id"])
                             )
                )

                # remove the root from general list of categories from xml tree
                # to speed up the search for the next steps
                xml_root.findall('shop/categories')[0].remove(category)

        # return final highest root
        return basic_root

    def build_tree(xml_root, tree_node):
        """
        Build tree of categories recursive way by xml tree

        :param xml_root: root of xml tree
        :param tree_node: node from which we build further tree
        """
        # looking for children for tree_node
        for category in xml_root.findall('shop/categories/category'):
            if int(category.attrib["parentId"]) == int(tree_node.cur_id):

                # calculating offers count for each match child
                # and creating node object and relating with tree_node
                tree_node.add_child(
                    TreeNode(category.attrib["id"],
                             f"{tree_node.category} / {category.text}",
                             calculate_count(xml_root, category.attrib["id"])
                             )
                )

                # remove the category from general list of categories from xml tree
                # to speed up the search for the next steps
                xml_root.findall('shop/categories')[0].remove(category)

        # go to deep (always first left child)
        for child in tree_node.children:
            build_tree(xml_root, child)

    # get root element from xml tree by url
    root = ET.fromstring(requests.get(url).content)

    # find all rootes
    root_category = find_all_rootes(root)

    # build tree of categories
    for subroot in root_category.children:
        build_tree(root, subroot)

    # return finished tree of categories
    return root_category


if __name__ == "__main__":
    # example 1
    print(xml_parser("https://saratov.tbmmarket.ru/tbmmarket/service/yandex-market.xml"))

    # example 2
    print(xml_parser("https://nnetwork.ru/yandex-market.xml"))
