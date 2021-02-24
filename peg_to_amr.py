from typing import Tuple, List, Dict
import networkx as nx


from definitions import PEGNodeType, PEGNode
from types_tree import TYPES
from utils import ev_re

# translation between simulator and propbank argument type labels
CORE_SLOTS = ['a', 'b', 'c']


def to_amr_instance_name(s) -> str:
    """ 
    Adjust names for conversion to AMR nodes.
    """
    # return generic 'event' instead of 'ev_x' so AMR is invariant to ordering
    matches = ev_re.findall(s)
    if matches:
        return "event"
    else:
        return s.replace("_", "-") # remove underscore
   

def build_amr_arg_map():
    """
    Map core argument types to PropBank format (ARG{n}). 
    """
    ev_types = TYPES.descendants('ev')

    # Core AMR slots (ARG*)
    amr_arg_map = {x: f"ARG{i}" for i,x in enumerate(CORE_SLOTS)}

    # Non core slots- use original name
    amr_arg_map.update({x: to_amr_instance_name(x) for x in ev_types + ['succ', 'site']})

    return amr_arg_map

AMR_ARG_MAP = build_amr_arg_map()


   
def to_amr_triplet(peg_node: PEGNode, amr_var: str, amr_name: str) -> List[Tuple]:
    """
    Convert a PEG node to AMR nodes. Following https://github.com/nschneid/amr-tutorial/raw/master/slides/AMR-TUTORIAL-FULL.pdf
    """
    
    # node representing entity
    type_trip = (amr_var, 'instance', to_amr_instance_name(peg_node.type))

    # node representing entity name
    name_inst_trip = (amr_name, 'instance', "name")

    # linking name node and string constant with string mention (cleaned version) 
    name_link_trip = (amr_name, 'op1', f'"{to_amr_instance_name(peg_node.amr_name)}"')

    # link entity node with name node
    link_trip = (amr_var, 'name', amr_name)

    return [type_trip, name_inst_trip, link_trip, name_link_trip]

def edge_to_amr(source_pegn: PEGNode, target_pegn: PEGNode,
                    edge_data: Dict, amr_graph: nx.DiGraph) -> List[Tuple]:
    """
    Convert edge in PEG to AMR edge triplets.
    Creates one edge per input atom, and additional dependency edge
    if event-event edge, to preserve dependencies between events.
    """

    amr_edge_trips = []

    
    source = source_pegn.name
    target = target_pegn.name
    
    source_var_id = amr_graph.nodes()[source]["amr_ids"]["var"]
    target_var_id = amr_graph.nodes()[target]["amr_ids"]["var"]

    # if ev-ev, add special successor relation
    if ((source_pegn.node_type == PEGNodeType.EVENT) and
        (target_pegn.node_type == PEGNodeType.EVENT)):
        amr_edge_trips.append((source_var_id, AMR_ARG_MAP['succ'], target_var_id))
    
    
    # add edges to all nodes in route
    for source, edge_data in edge_data.items():
        slot_target = amr_graph.nodes()[source]["amr_ids"]["var"]
        amr_edge_trips.append((source_var_id, AMR_ARG_MAP[edge_data["slot"]], slot_target))
        

    return amr_edge_trips
