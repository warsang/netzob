#-*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011-2016 Georges Bossert and Frédéric Guihéry              |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| File contributors :                                                       |
#|       - Georges Bossert <georges.bossert (a) supelec.fr>                  |
#|       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+
from netzob.Common.Utils.Decorators import typeCheck, NetzobLogger
from netzob.Model.Vocabulary.Domain.Variables.Leafs.AbstractVariableLeaf import AbstractVariableLeaf
from netzob.Model.Vocabulary.AbstractField import AbstractField
from netzob.Model.Vocabulary.Domain.Variables.SVAS import SVAS
from netzob.Model.Vocabulary.Domain.Specializer.SpecializingPath import SpecializingPath

@NetzobLogger
class AbstractRelationVariableLeaf(AbstractVariableLeaf):
    """Represents a relation relation between variables, one being updated with the others.

    """

    def __init__(self, varType, fieldDependencies=None, name=None,svas = SVAS.VOLATILE ):
        super(AbstractRelationVariableLeaf, self).__init__(varType, name, svas=svas)
        if fieldDependencies is None:
            fieldDependencies = []
        self.fieldDependencies = fieldDependencies

    @property
    def fieldDependencies(self):
        """A list of fields that are required before computing the value of this relation

        :type: a list of :class:`netzob.Model.Vocabulary.AbstractField.AbstractField`
        """
        return self.__fieldDependencies

    @fieldDependencies.setter
    @typeCheck(list)
    def fieldDependencies(self, fields):
        if fields is None:
            fields = []
        for field in fields:
            if not isinstance(field, AbstractField):
                raise TypeError("At least one specified field is not a Field.")
        self.__fieldDependencies = []
        for f in fields:
            self.__fieldDependencies.extend(f._getLeafFields())

    @typeCheck(SpecializingPath)
    def regenerateAndMemorize(self, variableSpecializerPath, acceptCallBack=True):
        """This method participates in the specialization process.
        It memorizes the value present in the path of the variable
        """

        self._logger.debug("RegenerateAndMemorize Variable {0}".format(self))

        if variableSpecializerPath is None:
            raise Exception("VariableSpecializerPath cannot be None")

        if variableSpecializerPath.memory.hasValue(self):
            old_value = variableSpecializerPath.memory.getValue(self)
            newValue = self.generate(oldValue = old_value)
        else:
            newValue = self.generate()
        variableSpecializerPath.memory.memorize(self, newValue)

        variableSpecializerPath.addResult(self, newValue)

        return [variableSpecializerPath]
