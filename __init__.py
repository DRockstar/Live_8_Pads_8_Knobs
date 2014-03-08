# Code modded by Donovan Bartish, aka DRockstar
from MiniLab_PLUS import MiniLab_PLUS
'''
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8247], model_name='Axiom A.I.R. Mini32'),
     PORTS_KEY: [inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT])]}
'''

def create_instance(c_instance):
    return MiniLab_PLUS(c_instance)