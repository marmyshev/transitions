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

from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.songs.forms.topicsdialog import Ui_TopicsDialog


class TopicsForm(QtGui.QDialog, Ui_TopicsDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(TopicsForm, self).__init__(parent)
        self.setupUi(self)

    def exec_(self, clear=True):
        """
        Execute the dialog.
        """
        if clear:
            self.nameEdit.clear()
        self.nameEdit.setFocus()
        return QtGui.QDialog.exec_(self)

    def accept(self):
        """
        Override the inherited method to check before we close.
        """
        if not self.nameEdit.text():
            critical_error_message_box(message=translate('SongsPlugin.TopicsForm',
                'You need to type in a topic name.'))
            self.nameEdit.setFocus()
            return False
        else:
            return QtGui.QDialog.accept(self)
