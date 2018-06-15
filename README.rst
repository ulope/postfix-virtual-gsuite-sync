Postfix `virtual` GSuite Sync
=============================

Syncs aliases from a postfix `virtual` file to GSuite user accounts.


Usage
-----

    gsuite-sync <target_domain_name> <virtual_file>


Example content of a `virtual` file
-----------------------------------

    doe@example.com            jane
    jane.doe@example.com       jane
    doe@example.com            jane

    smith@example.com          agent
    agent.smith@example.com    agent
    smith@example.com          agent

Example usage with above `virtual` file
---------------------------------------

    gsuite-sync example.com virtual
