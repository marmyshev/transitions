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
The language selection dialog.
"""
from PyQt4 import QtGui

from openlp.core.lib.ui import create_action
from openlp.core.utils import LanguageManager
from firsttimelanguagedialog import Ui_FirstTimeLanguageDialog


class FirstTimeLanguageForm(QtGui.QDialog, Ui_FirstTimeLanguageDialog):
    """
    The language selection dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qmList = LanguageManager.get_qm_list()
        self.languageComboBox.addItem(u'Autodetect')
        for key in sorted(self.qmList.keys()):
            self.languageComboBox.addItem(key)

    def exec_(self):
        """
        Run the Dialog with correct heading.
        """
        return QtGui.QDialog.exec_(self)

    def accept(self):
        """
        Run when the dialog is OKed.
        """
        # It's the first row so must be Automatic
        if self.languageComboBox.currentIndex() == 0:
            LanguageManager.auto_language = True
            LanguageManager.set_language(False, False)
        else:
            LanguageManager.auto_language = False
            action = create_action(None, self.languageComboBox.currentText())
            LanguageManager.set_language(action, False)
        return QtGui.QDialog.accept(self)

    def reject(self):
        """
        Run when the dialog is canceled.
        """
        LanguageManager.auto_language = True
        LanguageManager.set_language(False, False)
        return QtGui.QDialog.reject(self)
