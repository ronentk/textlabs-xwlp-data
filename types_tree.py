

from pathlib import Path
import pandas as pd
import networkx as nx
from networkx.algorithms.dag import descendants


types_dir = Path(__file__).parent / "types"


def load_type_tree(types_df):
    G = nx.DiGraph()
    edges = []
    for i, row in types_df.iterrows():
        edges.append((row["parent_type"], row["type"]))
    G.add_edges_from(edges)
    return G
    

class TypesTree:
    def __init__(self, path: str = str(types_dir.absolute())):
        self.types_df = pd.read_csv(f"{path}/types.csv").set_index("type", drop=False)
        self.type_tree = load_type_tree(self.types_df)
        
        self.tl_convert_df = self.types_df.dropna(axis=0,subset=["tl_conversion"]).set_index("tl_conversion")
        
    def descendants(self, type: str):
        """ 
        Return descendants of type `type`
        """
        return list(descendants(self.type_tree, type))
    
    def convert_tl_name(self, tl_name: str) -> str:
        """ 
        Convert old TextLabs name to updated version.
        """
        return self.tl_convert_df.loc[tl_name]["type"]
    
    def parent_type(self, type: str) -> str:
        """ 
        Return parent type of input entity type.
        """
        return self.types_df.loc[type]["parent_type"]
        
    
    def draw_tree(self):
        # hierarchical layout
        from networkx.drawing.nx_agraph import graphviz_layout
        
        pos = graphviz_layout(self.type_tree, prog='dot')
        nx.draw_networkx(self.type_tree, pos=pos)


TYPES = TypesTree()


    
    
        