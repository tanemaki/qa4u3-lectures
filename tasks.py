"""
This file is the entry point for the command line.
It imports all the tasks defined in the modules under the scripts directory and adds them to the top level collection.
"""

import invoke

import scripts.lecture01

# Create top level collection, which is the entry point for the command line
namespace = invoke.Collection(__name__)

# Add tasks defined in each module to the top level collection
namespace.add_collection(scripts.lecture01)
