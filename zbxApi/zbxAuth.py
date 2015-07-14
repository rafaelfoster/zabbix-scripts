#!/usr/bin/python

from zbxApi import ZabbixAPI

zbx_user     = "zabbix_api_user"
zbx_password = "secure_password"
zbx_server   = "https://zabbix.server"

zapi = ZabbixAPI(zbx_server)
zapi.login(zbx_user, zbx_password)
print "Connected to Zabbix API Version %s" % zapi.api_version()
