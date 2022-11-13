# ansible-apache-guacamole-dynamic-inventory

A script to, query Apache Guacamole API, retrieve all connections informations and pass them to ansible as inventory

## Installation
- Clone the repo:
```
git clone git@github.com:theko2fi/ansible-apache-guacamole-dynamic-inventory.git
```
- Create a `.env` file in the project directory with the fllowing content:
```
GUACAMOLE_URL="http://example.com/guacamole"
GUACAMOLE_USER=""
GUACAMOLE_PASSWORD=""
```
> Where:
> * `GUACAMOLE_URL` is the url of your Apache Guacamole instance
> * `GUACAMOLE_USER` is your username
> * `GUACAMOLE_PASSWORD` is your password
>

## Usage

```
ansible-playbook -i inventory.py main.yml
```