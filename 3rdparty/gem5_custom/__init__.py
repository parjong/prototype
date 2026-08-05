"""
Customized GEM5 Python package.
Exposes GEM5 Python modules and Custom SystemC device integration.
"""

import sys
import os

# Include gem5 python source path in sys.path if needed
_gem5_python_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "gem5", "src", "python"))
if os.path.exists(_gem5_python_dir) and _gem5_python_dir not in sys.path:
    sys.path.insert(0, _gem5_python_dir)
