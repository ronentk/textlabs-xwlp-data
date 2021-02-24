
from typing import Optional, Dict, List
from pathlib import Path
from dataclasses import dataclass
from collections import Counter
import numpy as np
from matplotlib import cm
import networkx as nx
from networkx import DiGraph
from networkx.readwrite import json_graph, node_link_graph
from networkx.drawing.nx_agraph import graphviz_layout

import pyvis
from enum import Enum
from pyvis.network import Network

from types_tree import TYPES
from definitions import PEGNodeType, PEGNode
from peg import PEG



@dataclass
class PyVisNodeData:
    """
    Relevant node parameters for pyvis.
    """
    title: str
    color: Dict
    x: int = None
    y: int = None
    borderWidth: int = 1
    border_color: str = "black"
    shape: str = "dot"
    
    def __post_init__(self):
        r, g, b = self.color
        self.color = {"background": "rgb({},{},{})".format(r, g, b),
                      "border": self.border_color }

@dataclass
class PyVisEdgeData:
    """
    Relevant edge parameters for pyvis.
    """
    label: str
    color: str
    title: str = None
    
    
    def __post_init__(self):
        r, g, b = self.color
        self.color = "rgb({},{},{})".format(r, g, b)
        

class ProcessEventGraphVisualizer:
    def __init__(self) -> None:
        self.G = DiGraph()
        self.network = Network(height=1000,
                               width=1000,
                               directed=True)


        node_types = list(TYPES.types_df.type)
        
        # mix up order of types to get uniform dist. over colors
        rand_state = np.random.RandomState(1245688)
        random_sorted = rand_state.permutation(node_types).tolist()
        
        node_cmap = cm.get_cmap('gist_ncar', len(node_types))
        
        # convert to js color scale [0, 255]
        colors = np.round(255 * node_cmap(range(len(node_types)))[:, :3])
        self.node_color_map = {type: colors.tolist()[i] for i,type in
                               enumerate(random_sorted) }
        
        
    def reset(self, manual_vis: bool = False):
        self.G = DiGraph()
        self.network = Network(height=1000,
                               width=1000,
                               directed=True
                               )
        if manual_vis:
            self.network.show_buttons()
        else:
            self.set_fixed_nodes_option()
        
    
    def edge_vis_data(self, edge_type: str, title: str=None) -> PyVisEdgeData:
        return PyVisEdgeData(label=edge_type, color=(0,0,0), 
                             title=title)
        """
        Translate PEG edge data into pyvis params.
        """
        
    def node_vis_data(self, e_type: str, 
                      node_data: PEGNode,
                      x: Optional[int] = None,
                      y: Optional[int] = None) -> PyVisNodeData:
        """
        Translate PEG node data into pyvis params.
        """

        if node_data.node_type == PEGNodeType.EVENT:
            shape = "square"
        else: # entity
            shape = "dot"
        
        return PyVisNodeData(title=TYPES.types_df.loc[node_data.type]['name'], 
                             color=self.node_color_map[e_type], x=x, y=y, shape=shape)
    
    
    def set_fixed_nodes_option(self):
        """ 
        Set pyvis options for interactive display.
        """
        self.network.set_options("""    
var options = {
  "nodes": {
    "physics": false
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "layout": {
    "hierarchical": {
      "enabled": true,
      "nodeSpacing": 130,
      "blockShifting": false,
      "direction": "LR"
    }
  },
  "physics": {
    "hierarchicalRepulsion": {
      "centralGravity": 0
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  }
}
                """)
            
        
    

    def from_process_event_graph(self, peg: PEG, manual_vis: bool = False):
        """
        Initialize visualizer from PEG.
        """
        self.reset(manual_vis=manual_vis)
        
        peg_G = peg.G
        
        # counter to disambiguate between different entities with identical display names.
        names_disambig = Counter([peg.node_data_by_id(n).display_name for n in peg.G.nodes()])
        
        def disambig_name(node, names_disambig):
            """ 
            For entities with non-unique display names, add unique span location to display name
            """
            if names_disambig[node.display_name] > 1:
                return node.unique_display_name
            else:
                return node.display_name

        # add nodes
        nodes = []
        for node, data in peg_G.nodes(data=True):
            peg_node_data =  data["data"]
            node_name = disambig_name(peg_node_data, names_disambig)
            node_data = {'name': node_name}
            node_vis = self.node_vis_data(peg_node_data.type, peg_node_data)
            node_data.update({'pyvis_options': node_vis.__dict__})
            nodes.append((node_name, node_data))
        self.G.add_nodes_from(nodes)
        
        # add edges
        edges = []
        
        for edge in peg_G.edges(data=True):
            source, target, data = edge
            source_name = disambig_name(peg_G.nodes()[source]["data"], names_disambig)
            target_name = disambig_name(peg_G.nodes()[target]["data"], names_disambig)
            routes = { d["slot"]: disambig_name(peg_G.nodes()[k]["data"], names_disambig) for k, d in data.items() }
            slots = str(list(routes.keys()))
            full_info = str(routes)

            edge_data = self.edge_vis_data(edge_type=slots, title=full_info)
            edges.append((source_name, target_name, {'pyvis_options': edge_data.__dict__ }))
            self.G.add_edges_from(edges)
        
        
        self.network.from_nx_all(self.G)
        
        return self.to_dict()
        
    
    def to_dict(self) -> Dict:
        return {'nodes': self.network.nodes, 
                'edges': self.network.edges} 
    

        
    def export_html(self, path="mygraph.html"):
        self.network.show(path)


def save_peg_html(peg, save_path: str, manual_vis: bool = False):
    """ 
    Save interactive PEG visualization to static html page. Set manual_vis = True 
    to enable manual control of visualization options.
    """
    pegv = ProcessEventGraphVisualizer()
    pegv.from_process_event_graph(peg, manual_vis=manual_vis)
    pegv.export_html(save_path)