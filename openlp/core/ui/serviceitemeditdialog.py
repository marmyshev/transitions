# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The UI widgets for the service item edit dialog
"""
from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box, create_button


class Ui_ServiceItemEditDialog(object):
    """
    The UI widgets for the service item edit dialog
    """
    def setupUi(self, serviceItemEditDialog):
        """
        Set up the UI
        """
        serviceItemEditDialog.setObjectName(u'serviceItemEditDialog')
        self.dialog_layout = QtGui.QGridLayout(serviceItemEditDialog)
        self.dialog_layout.setContentsMargins(8, 8, 8, 8)
        self.dialog_layout.setSpacing(8)
        self.dialog_layout.setObjectName(u'dialog_layout')
        self.list_widget = QtGui.QListWidget(serviceItemEditDialog)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setObjectName(u'list_widget')
        self.dialog_layout.addWidget(self.list_widget, 0, 0)
        self.button_layout = QtGui.QVBoxLayout()
        self.button_layout.setObjectName(u'button_layout')
        self.delete_button = create_button(serviceItemEditDialog, u'deleteButton', role=u'delete',
            click=serviceItemEditDialog.on_delete_button_clicked)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addStretch()
        self.up_button = create_button(serviceItemEditDialog, u'upButton', role=u'up',
            click=serviceItemEditDialog.on_up_button_clicked)
        self.down_button = create_button(serviceItemEditDialog, u'downButton', role=u'down',
            click=serviceItemEditDialog.on_down_button_clicked)
        self.button_layout.addWidget(self.up_button)
        self.button_layout.addWidget(self.down_button)
        self.dialog_layout.addLayout(self.button_layout, 0, 1)
        self.button_box = create_button_box(serviceItemEditDialog, u'button_box', [u'cancel', u'save'])
        self.dialog_layout.addWidget(self.button_box, 1, 0, 1, 2)
        self.retranslateUi(serviceItemEditDialog)

    def retranslateUi(self, serviceItemEditDialog):
        """
        Translate the UI on the fly
        """
        serviceItemEditDialog.setWindowTitle(translate('OpenLP.ServiceItemEditForm', 'Reorder Service Item'))
