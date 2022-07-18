import copy
import logging
from collections import ChainMap
from multiprocessing import Pipe, Process

import ppqm

_logger = logging.getLogger("molcalc:calc")

MAX_TIME = 10  # seconds


def _get_options(existing_options, tmp_path):
    orca_options = {"scr": tmp_path, "n_cores": 1, "memory": 2}
    options_prime = ChainMap(orca_options, existing_options)
    options_prime = dict(options_prime)
    return options_prime


def optimize_coordinates(molobj, orca_options):

    calculation_options = {
        'pm3': None,
        'opt': None
    }

    # Remove GAMESS options that ppqm.orca.OrcaCalculator doesn't expect
    orca_options.pop('gamess_scr', None)
    orca_options.pop('gamess_userscr', None)
    orca_options.pop('method_options', None)
    options_prime = _get_options(orca_options, '/home/cloudlab/scratch/orca/')

    calc_obj = ppqm.orca.OrcaCalculator(**options_prime)
    results = calc_obj.calculate(molobj, calculation_options)
    properties = results[0]

    return properties


def calculate_vibrations(molobj, orca_options):

    # Vibrate molecule
    calculation_options = {
        'pm3': None,
        # 'Opt': None,
        'NumFreq': None
    }

    # Remove GAMESS options that ppqm.orca.OrcaCalculator doesn't expect
    orca_options.pop('gamess_scr', None)
    orca_options.pop('gamess_userscr', None)
    orca_options.pop('method_options', None)
    options_prime = _get_options(orca_options, '/home/cloudlab/scratch/orca/')

    calc_obj = ppqm.orca.OrcaCalculator(**options_prime)
    results = calc_obj.calculate(molobj, calculation_options)
    properties = results[0]

    return properties


def calculate_orbitals(molobj, gamess_options):

    # See https://sites.google.com/site/orcainputlibrary/semiempirical-methods
    # for info on the Grimme's 3-corrected Hartree-Fock method. This is being
    # used here as an effective replacement for the semiempirical "STO" method
    # used for the corresponding calculate_orbitals using GAMESS
    calculation_options = {
        'HF-3c': None
    }

    # Remove GAMESS options that ppqm.orca.OrcaCalculator doesn't expect
    orca_options.pop('gamess_scr', None)
    orca_options.pop('gamess_userscr', None)
    orca_options.pop('method_options', None)
    options_prime = _get_options(orca_options, '/home/cloudlab/scratch/orca/')

    calc_obj = ppqm.orca.OrcaCalculator(**options_prime)
    try:
        results = calc_obj.calculate(molobj, calculation_options)
        properties = results[0]
    except TypeError:
        properties = dict()
        properties["error"] = "Failed orbital calculation"

    return properties