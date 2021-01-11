# -*- coding: utf-8 -*-

"""Non-graphical part of the Antechamber step in a SEAMM flowchart
"""

import logging
import pprint  # noqa: F401
import os
import seamm_antechamber
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: 'job' and 'printer'. 'job' send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# 'printer' sends output to the file 'step.out' in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('Antechamber')

ANTECHAMBER = "/Users/meliseo/Scratch/antechamber/amber20_src/bin/antechamber"


class Antechamber:
    """
    The non-graphical part of a Antechamber step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : AntechamberParameters
        The control parameters for Antechamber.

    See Also
    --------
    TkAntechamber,
    Antechamber, AntechamberParameters
    """

    def __init__(
        self,
        parameter_set=None,
        logger=logger,
        **_ignore
    ):
        """A step for Antechamber in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug('Creating Antechamber {}'.format(self))
        self.directory = os.getcwd()

    def atom_type(self, system=None):
        pass


    @property
    def version(self):
        """The semantic version of this module.
        """
        return seamm_antechamber.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return seamm_antechamber.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        text = (
            'Please replace this with a short summary of the '
            'Antechamber step, including key parameters.'
        )

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    @property
    def supported_forcefields(self):
        return ["GAFF"]

    def assign_parameters(self, system=None):

        input_files = {}
        input_files['pdbfile.pdb'] = system.to_pdb_text()

        filename = os.path.join(self.directory, "pdbfile.pdb")
        with open(filename, "w") as f:
            f.write(input_files["pdbfile.pdb"])

        cmd = [ANTECHAMBER,
            "-i", 
            "pdbfile.pdb", 
            "-fi",
            "pdb",
            "-o",
            "molfile.mol2",
            "-fo",
            "mol2"
        ] 
        return_files = ["molfile.mol2"]
        local = seamm.ExecLocal()
        result = local.run(cmd=cmd, files=input_files, return_files=return_files)

        if result is None:
            self.logger.error("There was an error running Antechamber")
            return None

        f = os.path.join(self.directory, "stdout.txt")
        with open(f, mode="w") as fd:
            fd.write(result["stdout"])

        for filename in result['files']:
            f = os.path.join(self.directory, filename)
            mode = "wb" if type(result[filename]['data']) is bytes else "w"
            with open(f, mode=mode) as fd:
                if result[filename]['data'] is not None:
                    fd.write(result[filename]['data'])
                else:
                    fd.write(result[filename]['exception'])

            atom_types = self.extract_atom_types(f, system)

        return atom_types

    def extract_atom_types(self, data, system):

        atom_types = ["?"] * system.n_atoms() 

        with open(data, "r") as f:
            try:
                section = None
                for line in f:
                    if line.startswith('#'): 
                        continue
                    if not line.strip() and section is None: 
                        continue
                    if line.startswith('@<TRIPOS>'):
                        section = line[9:].strip()
                        continue
                    if section is None:
                        raise TypeError('Error reading Mol2 file')
                    if section == 'ATOM':
                        line_split= line.split()
                        atom_id = int(line_split[0])
                        atom_name = line_split[1]
                        atom_type = line_split[5]
                        atom_types[atom_id - 1] = atom_type
            except:
                pass
        return atom_types
