"""
field.py

Class instance used for modifying field via Display window.
"""

# Load the needed packages
from functools import partial

from ..core import Variable, Component, QtGui, QtCore


class FieldButtonWindow(Component):
    '''Class to display a Window with Field name radio buttons.'''

    Vradar = None  #: see :ref:`shared_variable`
    Vfield = None  #: see :ref:`shared_variable`

    def __init__(self, Vradar, Vfield, name="FieldButtons", parent=None):
        '''
        Initialize the class to create the interface.

        Parameters
        ----------
        Vradar : :py:class:`~artview.core.core.Variable` instance
            Radar signal variable.
        Vfield : :py:class:`~artview.core.core.Variable` instance
            Field signal variable.
        [Optional]
        name : string
            Field Radiobutton window name.
        parent : PyQt instance
            Parent instance to associate to FieldButtonWindow.
            If None, then Qt owns, otherwise associated with parent PyQt
            instance.

        Notes
        -----
        This class records the selected button and passes the
        change value back to variable.
        '''
        super(FieldButtonWindow, self).__init__(name=name, parent=parent)

        # Set up signal, so that DISPLAY can react to external
        # (or internal) changes in field (Core.Variable instances expected)
        # The change is sent through Vfield
        self.Vradar = Vradar
        self.Vfield = Vfield
        self.sharedVariables = {"Vradar": self.NewRadar,
                                "Vfield": self.NewField}
        self.connectAllVariables()

        self.CreateFieldWidget()
        self.SetFieldRadioButtons()
        self.show()

    ########################
    # Button methods #
    ########################

    def FieldSelectCmd(self, field):
        '''Captures a selection and updates field variable.'''
        self.Vfield.change(field)

    def CreateFieldWidget(self):
        '''Create a widget to store radio buttons to control field adjust.'''
        self.radioBox = QtGui.QGroupBox("Field Selection", parent=self)
        self.rBox_layout = QtGui.QVBoxLayout(self.radioBox)
        self.radioBox.setLayout(self.rBox_layout)
        self.setCentralWidget(self.radioBox)

    def SetFieldRadioButtons(self):
        '''Set a field selection using radio buttons.'''
        # Instantiate the buttons into a list for future use
        self.fieldbutton = {}

        if self.Vradar.value is None:
            return

        # Loop through and create each field button and
        # connect a value when selected
        for field in self.Vradar.value.fields.keys():
            button = QtGui.QRadioButton(field, self.radioBox)
            self.fieldbutton[field] = button
            QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"),
                                   partial(self.FieldSelectCmd, field))

            self.rBox_layout.addWidget(button)

        # set Checked the current field
        self.NewField(self.Vfield, self.Vfield.value, True)

    def NewField(self, variable, value, strong):
        '''Slot for 'ValueChanged' signal of
        :py:class:`Vfield <artview.core.core.Variable>`.

        This will:

        * Update radio check
        '''
        if (self.Vradar.value is not None and
                value in self.Vradar.value.fields):
            self.fieldbutton[value].setChecked(True)

    def NewRadar(self, variable, value, strong):
        '''Slot for 'ValueChanged' signal of
        :py:class:`Vradar <artview.core.core.Variable>`.

        This will:

        * Recreate radio items
        '''
        self.CreateFieldWidget()
        self.SetFieldRadioButtons()
