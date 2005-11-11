#
#  Copyright Red Hat, Inc. 2005
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 2, or (at your option) any
#  later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; see the file COPYING.  If not, write to the
#  Free Software Foundation, Inc.,  675 Mass Ave, Cambridge, 
#  MA 02139, USA.

# Author: Stanko Kupcevic <kupcevic@redhat.com>
#


import gtk
import gtk.glade

import err
import fence_base


def get_fence_name():
    return 'APC MasterSwitch'


class FenceApcSharedInfo(fence_base.FenceBaseSharedInfo):
    def __init__(self):
        fence_base.FenceBaseSharedInfo.__init__(self)
        
        self.hostname_entry = self.glade_xml.get_widget('fence_apc_hostname')
        self.username_entry = self.glade_xml.get_widget('fence_apc_username')
        self.password_entry = self.glade_xml.get_widget('fence_apc_password')
        
        container = self.glade_xml.get_widget('fence_apc_shared')
        container.unparent()
        self.add(container)
        
        pass
    
    
    def validate(self):
        hostname, username, password = self.__get_info()
        if hostname == '':
            raise err.Err('missing fence device hostname')
        if username == '':
            raise err.Err('missing fence device username')
        if password == '':
            raise err.Err('missing fence device password')
    
    def get_fencedevice_tag(self):
        template = '<fencedevice agent=\"fence_apc\" name=\"fence-apc\" ipaddr=\"%s\" login=\"%s\" passwd=\"%s\"/>'
        hostname, username, password = self.__get_info()
        return template % (hostname, username, password)
    
    def __get_info(self):
        hostname = self.hostname_entry.get_text().strip()
        username = self.username_entry.get_text().strip()
        password = self.password_entry.get_text().strip()
        return hostname, username, password
    
    


class FenceApc(fence_base.FenceBase, gtk.HBox):

    def __init__(self, node, shared_info):
        fence_base.FenceBase.__init__(self, node, shared_info)
        gtk.HBox.__init__(self)
        
        self.port_entry = self.glade_xml.get_widget('fence_apc_port')
        
        container = self.glade_xml.get_widget('fence_apc_node_specific')
        container.unparent()
        self.pack_start(container)
        
    
    def get_widget(self):
        return self
    
    def validate(self):
        port = self.__get_info()
        if port == '':
            raise err.Err('node ' + self.node + ' missing fence device\'s port')
    
    def get_nodes_fence_tag(self):
        template = '<device name=\"fence-apc\" port=\"%s\" switch=\"0\"/>'
        return template % self.__get_info()
    
    def get_fencedevice_tag(self):
        return self.shared_info.get_fencedevice_tag()
    
    def __get_info(self):
        port = self.port_entry.get_text().strip()
        return port
