#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vagrant


def vm_deploy(vagrant_file='.',machine_name=[]):
    v = vagrant.Vagrant(vagrant_file)
    if machine_name:
        for i in machine_name:
            v.up(vm_name=i)
    else:
        v.up()
    vm_machine_list(vagrant_file)

def vm_destroy(vagrant_file='.',machine_name=''):
    v = vagrant.Vagrant(vagrant_file)
    v.destroy()

def vm_status(vagrant_file='.',machine_name=''):
    v = vagrant.Vagrant(vagrant_file)
    status = v.status()
    return status

def vm_machine_list(vagrant_file='.'):
    status_data = vm_status(vagrant_file)
    machine_name = []
    for i in status_data:
        machine_name.append(i.name)
    return machine_name

def vm_box_list(vagrant_file='.'):
    box_list = vagrant.Vagrant(vagrant_file).box_list()
    box_list_name = []
    for i in box_list:
        box_list_name.append(i.name)
    return box_list_name
