# libs for beautifully table output
import pandas as pd
import numpy as np


class TreeNode:
    """
    Custom tree class for creating categories tree
    """

    def __init__(self, cur_id, category, count):
        """
        Tree class constructor

        :param cur_id: id of tree node
        :param category: category text for tree node
        :param count: count of offers for this category
        """
        self.cur_id = cur_id
        self.category = category
        self.count = count
        self.children = []  # references to children nodes

    def add_child(self, child_node):
        """
        Add child to tree node
        """
        # creates parent-child relationship
        self.children.append(child_node)

    def __fill_out_df(self):
        """
        Filling __out_df for good output (tree traversal)
        """

        result = pd.DataFrame(data={'category': [], 'offers': []},
                              dtype=np.int8)

        # for each tree node have to push row to global table
        if self.cur_id != 0:
            result.loc[len(result)] = [self.category,
                                       self.count]

        # go to children of tree node
        for child in self.children:
            result = pd.concat([result, child.__fill_out_df()])

        return result

    def __str__(self):
        """
        Overload of output
        """

        # return the result dataframe in string format
        return self.__fill_out_df().to_string()
