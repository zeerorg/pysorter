import os

from testfixtures import TempDirectory, tempdir

from helper import initialize_dir

import helper
from pysorter.core import pysorter

import pytest


@tempdir()
def test_replacement_pattern(d):
    os.chdir(d.path)
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{keyword}/{name}.{ext}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'cruel/',
        'cruel/hello.pdf',
        'other/',
        'directories/']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@tempdir()
def test_bad_keyword_replacement_pattern(d):
    os.chdir(d.path)
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{unknown}/{keyword}/{name}.{ext}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    with pytest.raises(ValueError):
        pysorter.main(args)


@tempdir()
def test_bad_numbered_replacement_pattern(d):
    os.chdir(d.path)
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{keyword}/{name}.{ext}/{4}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    with pytest.raises(ValueError):
        pysorter.main(args)


@tempdir()
def test_callable_configuration(d):
    def comparison_function(match, entity):
        return 'foobar/'

    os.chdir(d.path)
    filetypes = {
        '\.pdf$': comparison_function
    }

    to_sort = 'files/'
    dest = 'sorted/'

    to_make = ['hello_cruel.pdf']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '-d', dest]

    pysorter.main(args)
    # --- compare sorted
    expected = [
        'foobar/',
        'foobar/hello_cruel.pdf',
        'other/',
        'directories/']
    pysorter.main(args)
    d.compare(expected=expected, path=dest)


@tempdir()
def test_rule_behaviour_into_directory_for_file(d):
    os.chdir(d.path)
    filetypes = {
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/hello_cruel.pdf',
        'other/',
        'directories/']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@tempdir()
def test_rule_behaviour_to_for_file(d):
    os.chdir(d.path)
    filetypes = {
        '.*\.pdf$': 'pdf'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'pdf',
        'other/',
        'directories/']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@tempdir()
def test_rule_behaviour_into_directory_for_dir(d):
    os.chdir(d.path)
    filetypes = {
        'foo/$': 'pdf/'
    }

    to_sort = 'files/'

    to_make = ['foo/']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/foo/',
        'other/',
        'directories/']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@tempdir()
def test_rule_behaviour_to_for_dir(d):
    os.chdir(d.path)
    filetypes = {
        'foo/$': 'pdf'
    }

    to_sort = 'files/'

    to_make = ['foo/']
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    expected = [
        'pdf/',
        'other/',
        'directories/']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


if __name__ == '__main__':
    # test_noargs()
    pass