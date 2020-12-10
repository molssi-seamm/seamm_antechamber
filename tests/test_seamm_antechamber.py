#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `seamm_antechamber` package."""

import pytest  # noqa: F401
import seamm_antechamber  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = seamm_antechamber.Antechamber()
    assert str(type(result)) == (
        "<class 'seamm_antechamber.seamm_antech.Antechamber'>"  # noqa: E501
    )
