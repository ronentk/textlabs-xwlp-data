"""
"pseudo python" implementation of TextLabs WLP operations

Some operations use more basic functions which are described here (not fully implemented):
`locate_at(a,site)`: creates new `located_at(a,site)` proposition, removes any other
`located_at(a,*)` for `* != site`
`seal(b,a)`: creates new `seal_of(b,a)` proposition, removes any other
`seal_of(b,*)` for `* != a`
 `co_ref(b,a)`: creates new relation co_ref_of(b,a)
 `destroy(a)`: removes(a) from simulator
"""

from typing import Optional

def transfer_op(a, site, Optional[b], Optional[c]):
    locate_at(a,site) # creates new `located_at` proposition, removes
    if b:
        locate_at(b,site)
    if c:
        locate_at(c,site)

def destroy_op(a):
    destroy(a)


def create_op(a, Optional[b], Optional[site]):
    if b:
        co_ref(b,a)
    if site:
        locate_at(a,site)


def convert_op(a, b, Optional[site]):
    destroy(a)
    if site:
        locate_at(b,site)


def cover_op(a, b, Optional[site]):
    seal(b,a)
    if site:
        locate_at(a,site)

def centrifuge_op(a, Optional[b], Optional[c], Optional[site]):
    if b:
        locate_at(b,a)
    if c:
        locate_at(c,a)
    if site:
        locate_at(a,site)


############### default ops (ops with default execution semantics)

def temp_treat_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)

def measure_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)

def wash_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)

def default_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)

def time_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)

def mix_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)

def remove_op(a, Optional[b], Optional[c], Optional[site]):
    if site:
        locate_at(a,site)
        if b:
            locate_at(b,site)
        if c:
            locate_at(c,site)
