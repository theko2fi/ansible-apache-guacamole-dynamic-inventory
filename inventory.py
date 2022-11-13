#!/usr/bin/env python3

# Copyright: (c) 2022, Kenneth KOFFI <https://www.linkedin.com/in/kenneth-koffi-6b1218178/>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


'''
Example custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import json
import guacamole

from dotenv import load_dotenv


class ExampleInventory(object):

    def __init__(self):
        load_dotenv()
        self.inventory = {}
        self.read_cli_args()
        self.guacamole_url = os.getenv('GUACAMOLE_URL')
        self.guacamole_user = os.getenv('GUACAMOLE_USER')
        self.guacamole_password = os.getenv('GUACAMOLE_PASSWORD')


        # Called with `--list`.
        if self.args.list:
            self.inventory = self.guacamole_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    # Example inventory for testing.
    def example_inventory(self):
        return {
            'group': {
                'hosts': ['192.168.28.71', '192.168.28.72'],
                'vars': {
                    'ansible_user': 'vagrant',
                    'ansible_ssh_private_key_file':
                        '~/.vagrant.d/insecure_private_key',
                    'ansible_python_interpreter':
                        '/usr/bin/python3',
                    'example_variable': 'value'
                }
            },
            '_meta': {
                'hostvars': {
                    '192.168.28.71': {
                        'host_specific_var': 'foo'
                    },
                    '192.168.28.72': {
                        'host_specific_var': 'bar'
                    }
                }
            }
        }

    def guacamole_inventory(self):

        guacamole_token = guacamole.guacamole_get_token(self.guacamole_url, True, self.guacamole_user, self.guacamole_password)
        auth_token=guacamole_token['authToken']
        guacamole_connections = guacamole.guacamole_get_connections(self.guacamole_url, True, guacamole_token['dataSource'], 'ROOT', auth_token)
        #print(guacamole_connections)
        all_hosts = []
        hostvars = {}
        for connection in guacamole_connections:

            connection_detail = guacamole.guacamole_get_connection_details(self.guacamole_url, True, guacamole_token['dataSource'], connection['identifier'], auth_token)
            connection_detail_hostname = connection_detail['hostname']

            hostvars[connection_detail_hostname] = {}
            hostvars[connection_detail_hostname]['ansible_user'] = connection_detail['username']
            hostvars[connection_detail_hostname]['ansible_password'] = connection_detail['password']

            all_hosts.append(connection_detail_hostname)

        ansible_inventory = {}
        ansible_inventory['ungrouped'] = {}
        ansible_inventory['ungrouped']['hosts'] = all_hosts
        ansible_inventory['ungrouped']['vars'] = {'ansible_ssh_extra_args': '-o StrictHostKeyChecking=no'}

        ansible_inventory['_meta'] = {}
        ansible_inventory['_meta']['hostvars'] = hostvars
        return ansible_inventory



    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()


if __name__ == "__main__":
    # Get the inventory.
    ExampleInventory()



