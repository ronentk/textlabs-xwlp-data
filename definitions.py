from typing import Mapping, List, Optional, Dict, Tuple, Iterable, Set
from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from utils import clean_names

class PEGNodeType(str, Enum):
    EVENT = 'event'
    ENTITY = 'entity'
    
    
@dataclass_json
@dataclass
class PEGNode:
    """
    Represents a generic node in a PEG.
    
    Attributes:
        name: Internal node identifier.
        type: Node type.
        parent_type: Higher level class the node belongs to.
        display_name: Mention of the node as referred to in the text ("e.g., 'test tubes').
        amr_name: Pre-processed version of `display_name` used in the AMR graph, as special chars can cause problems with AMR readers.
        node_type: Top-level class the node belongs to (either event or argument).
        word_spans: List of word indices in the form of tuples- (sentence_idx, word_idx).
        spans: Char-level span in the format [start, end]
    """
    name: str
    type: str
    parent_type: str
    display_name: str
    amr_name: str
    node_type: PEGNodeType
    word_spans: Optional[List[str]] = field(default_factory=list)
    spans: Optional[List] = field(default_factory=list)
    

    @property
    def unique_display_name(self):
        """ 
        Return unqiue name including span position in text, for disambiguation.
        """
        if self.word_spans:
            s, w = self.word_spans[-1]
            return f"s{s}_w{w}_{self.display_name}" 
        else:
            return self.display_name
        

@dataclass_json
@dataclass
class PEGEntity(PEGNode):
    """
    Represents an argument (entity) node in a PEG.
    
    Attributes:
        events: The sequence of events this entity participated in.  
    """
    node_type: PEGNodeType = PEGNodeType.ENTITY
    events: Optional[List[str]] = field(default_factory=list)


    
    
@dataclass_json
@dataclass
class PEGProcessEvent(PEGNode):
    """
    Represents an event in a PEG. 

    Attributes:
        inputs: Map of input arguments keyed by type (argument type).
        outputs: List of output entities.
        step: Integer step number marking when event took place in simulator session.
    """
    name: str
    inputs: Dict[str, str] = field(default_factory=dict)
    outputs: List[str] = field(default_factory=list)
    step: float = field(default=float("inf"))
    node_type: PEGNodeType = PEGNodeType.EVENT
    
    
    
    
    
    