# importing requests for get xml by the url and lib for xml
import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from copy import copy as obj_copy

# custom tree class
from TreeNode import TreeNode


def xml_parser(url):
    """
    Function for building tree of categories by XML from specific URL

    :param url: url path for get specific xml for parsing
    :return: tree of categories by xml string
    """

    def calculate_count(xml_root):
        """
        Calculate count of specific category in list of offers in xml tree

        :param xml_root: root of xml tree
        :param cur_id: id specific category for calculate
        :return: count of specific category in list of orders
        """
        # counter for category
        count_dict = defaultdict(lambda: 0)

        # searching for specific category in the list of orders
        for offer in xml_root.findall('shop/offers/offer'):
            # if found - add to the dict
            count_dict[offer.findall('categoryId')[0].text] += 1

        return count_dict

    def find_all_rootes(xml_root, count_dict):
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
                             count_dict[category.attrib["id"]]
                             )
                )

                # remove the root from general list of categories from xml tree
                # to speed up the search for the next steps
                xml_root.findall('shop/categories')[0].remove(category)

        # return final highest root
        return basic_root

    def build_tree_safe(xml_root, tree_node, count_dict):
        """
        Build tree of categories recursive way by xml tree
        (input parameters will not change)

        :param xml_root: root of xml tree
        :param tree_node: node from which we build further tree
        """
        def build_tree(xml_root, tree_node, count_dict):
            """
            Build tree of categories recursive way by xml tree
            (input parameters will change)

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
                                 count_dict[category.attrib["id"]]
                                 )
                    )

                    # remove the category from general list of categories from xml tree
                    # to speed up the search for the next steps
                    xml_root.findall('shop/categories')[0].remove(category)

            # go to deep (always first left child)
            for child in tree_node.children:
                build_tree(xml_root, child, count_dict)

        # call without the input data change
        xml_root_copy = obj_copy(xml_root)
        build_tree(xml_root_copy, tree_node, count_dict)

    # get root element from xml tree by url
    root = ET.fromstring(requests.get(url).content)

    # get dict of counts
    dict_values = calculate_count(root)

    # find all rootes
    root_category = find_all_rootes(root, dict_values)

    # build tree of categories
    for subroot in root_category.children:
        build_tree_safe(root, subroot, dict_values)

    # return finished tree of categories
    return root_category


if __name__ == "__main__":
    # example 1
    print(xml_parser("https://saratov.tbmmarket.ru/tbmmarket/service/yandex-market.xml"))

    # example 2
    print(xml_parser("https://nnetwork.ru/yandex-market.xml"))
