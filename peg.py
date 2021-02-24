from typing import Mapping, List, Optional, Dict, Tuple, Iterable, Set
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
import penman
import networkx as nx
import json


from peg_to_amr import to_amr_triplet, edge_to_amr
from definitions import PEGNodeType, PEGNode, PEGProcessEvent, PEGEntity

PEG_NODE_FROM_NODE_TYPE_MAP = {
    PEGNodeType.ENTITY: PEGEntity,
    PEGNodeType.EVENT: PEGProcessEvent,
}


    
    
class PEG:
    """ 
    Process Execution Graph representing an executable workflow for an experimental procedure. 
    This class wraps a networkx DiGraph to faciliate convenient access to various views
    of the data.
    
    
    Attributes:
        G (networkx.DiGraph): graph representing PEG.
        proto_idx: the WLP protocol index this PEG represents.
        sentences: original sentences comprising the protocol this PEG represents.
    
    Methods:
        to_amr_str(): Convert PEG to AMR string representation (Penman notation).
    """
    def __init__(self):
        self.G = nx.DiGraph()
        
    @property
    def sentences(self) -> List[str]:
        """ 
        Return the original sentences comprising the protocol this PEG represents.
        """
        return self.G.graph["sentences"]
    
    @property
    def proto_idx(self) -> int:
        """ 
        Return the WLP protocol index this PEG represents. 
        """
        return self.G.graph["proto_idx"]
                
    def node_data_by_id(self, node_id: str) -> PEGNode:
        """ 
        Return node data of PEG node `node_id`
        """
        return self.G.nodes()[node_id]["data"]
    
    @classmethod
    def from_json(cls, load_path: Path) -> "PEG":
        """ 
        Load a PEG from a .peg file. 
        """
        loaded_peg_json = json.load(load_path.open())
        return cls.load_graph(loaded_peg_json)
    
    def to_json(self):
        g_data = nx.readwrite.json_graph.node_link_data(self.G)
        for node in g_data["nodes"]:
            node["data"] = node["data"].to_dict()
        return g_data
    
    def save_graph(self, save_file: Path):
        """
        Saves the ProcessExecutionGraph in serializable JSON form
        """
        peg = self.to_json()
        json.dump(peg, save_file.open(mode="w"))
        
    @classmethod
    def load_graph(cls, data) -> "PEG":
        instance = cls()
        g = nx.readwrite.json_graph.node_link_graph(data)
        for n, node_data in g.nodes(data=True):
            node_type = node_data["data"]["node_type"]
            peg_node_cls = PEG_NODE_FROM_NODE_TYPE_MAP.get(node_type)
            node_data["data"] = peg_node_cls.from_dict(node_data["data"])


        instance.G = g
        return instance
        
    def get_amr_root(self) -> str:
        """ 
        Find and return the AMR root node id. The root node is defined to be the last
        operation of the process (in topological order). If there is more than one
        option, we take the last executed operation (using recorded simulator timestep).
        """
    
        # get all events
        evs = [x for x in self.G.nodes() if self.node_data_by_id(x).node_type.value == "event"]
        
        # find last executed event
        max_ev_time = max([self.node_data_by_id(x).step for x in evs])
        
        amr_G = self.G.reverse(copy=True)
        amr_G = amr_G.subgraph(evs)
        
        assert(nx.algorithms.dag.is_directed_acyclic_graph(amr_G))
        nns = [n for n in nx.algorithms.lexicographical_topological_sort(amr_G,
                                         key=lambda x: (max_ev_time - amr_G.nodes()[x]["data"].step))]
        root = nns[0]
        return root
    
    def to_amr(self) -> penman.Graph:
        """ 
        Convert PEG to AMR as `penman.Graph` object. 
        """
        
        # reverse the graph edges, as the root is defined as the last executed node of 
        # the original PEG. This means the arrows will be backwards if you visualize
        # the AMR graph!
        amr_G = self.G.reverse(copy=True)

        # set arbitrary amr variable ids
        for i, (n, ndata) in enumerate(sorted(amr_G.nodes(data=True))):
            ndata["amr_ids"] = {"name": f"n{i}", "var": f"a{i}"}


        # get root
        root = self.get_amr_root()

        root_amr_id = amr_G.nodes()[root]["amr_ids"]["var"]

        # get all instance triplets
        instance_trips = []
        for n in sorted(amr_G.nodes()):
            node = amr_G.nodes()[n]["data"]
            amr_ids = amr_G.nodes()[n]["amr_ids"]
            instance_trips += to_amr_triplet(node, amr_ids["var"], amr_ids["name"])

        # get all edge trips
        edge_trips = []
        for source, target, data in sorted(amr_G.edges(data=True)):
            source_pegn: PEGNode = self.node_data_by_id(source)
            target_pegn: PEGNode = self.node_data_by_id(target)
            edge_trips += edge_to_amr(source_pegn, target_pegn, data, amr_G)

        all_trips = instance_trips + edge_trips

        return penman.Graph(triples=all_trips, top=root_amr_id)
    
    def to_amr_str(self) -> str:
        """
        Convert PEG to AMR string representation (Penman notation).
        """
        pg = self.to_amr()
        return penman.PENMANCodec().encode(pg)
    
        
        
