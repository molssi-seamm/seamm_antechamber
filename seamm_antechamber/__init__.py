# -*- coding: utf-8 -*-

"""
seamm_antechamber
The Antechamber atom typing tool
"""

# Bring up the classes so that they appear to be directly in
# the seamm_antechamber package.

from seamm_antechamber.seamm_antechamber import Antechamber  # noqa: F401, E501
from seamm_antechamber.seamm_antechamber_step import AntechamberStep  # noqa: F401, E501

# Handle versioneer
from ._version import get_versions
__author__ = """Eliseo Marin"""
__email__ = 'meliseo@vt.edu'
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
