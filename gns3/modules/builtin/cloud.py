# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gns3.node import Node

import logging
log = logging.getLogger(__name__)


class Cloud(Node):

    """
    Cloud node

    :param module: parent module for this node
    :param server: GNS3 server instance
    :param project: Project instance
    """

    URL_PREFIX = "cloud"

    def __init__(self, module, server, project):

        super().__init__(module, server, project)
        self.setStatus(Node.started)
        self._always_on = True
        self._interfaces = {}
        self._cloud_settings = {"ports_mapping": []}
        self.settings().update(self._cloud_settings)

    def interfaces(self):

        return self._interfaces

    def _createCallback(self, result, error=False, **kwargs):
        """
        Callback for create.

        :param result: server response
        """
        if "ports_mapping" in result:
            self._settings["ports_mapping"] = result["ports_mapping"].copy()

        if "interfaces" in result:
            self._interfaces = result["interfaces"].copy()

    def update(self, new_settings, force=False):
        """
        Updates the settings for this cloud.

        :param new_settings: settings dictionary
        :param force: force this node to update
        """

        params = {}
        for name, value in new_settings.items():
            if name in self._settings and self._settings[name] != value:
                params[name] = value
        if params or force:
            self._update(params)

    def _updateCallback(self, result):
        """
        Callback for update.

        :param result: server response
        """

        if "ports_mapping" in result:
            self._settings["ports_mapping"] = result["ports_mapping"].copy()

        if "interfaces" in result:
            self._interfaces = result["interfaces"].copy()

    def info(self):
        """
        Returns information about this cloud.

        :returns: formatted string
        """

        info = """Cloud device {name} is always-on
This is a node for external connections
Device run on {host}
""".format(name=self.name(),
           host=self.compute().name())

        port_info = ""
        for port in self._ports:
            if port.isFree():
                port_info += "   Port {} is empty\n".format(port.name())
            else:
                port_info += "   Port {name} {description}\n".format(name=port.name(),
                                                                     description=port.description())

        return info + port_info

    def configPage(self):
        """
        Returns the configuration page widget to be used by the node properties dialog.

        :returns: QWidget object
        """

        from .pages.cloud_configuration_page import CloudConfigurationPage
        return CloudConfigurationPage

    @staticmethod
    def defaultSymbol():
        """
        Returns the default symbol path for this cloud.

        :returns: symbol path (or resource).
        """

        return ":/symbols/cloud.svg"

    @staticmethod
    def symbolName():

        return "Cloud"

    @staticmethod
    def categories():
        """
        Returns the node categories the node is part of (used by the device panel).

        :returns: list of node categories
        """

        return [Node.end_devices]

    def __str__(self):

        return "Cloud"
