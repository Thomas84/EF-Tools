from Autodesk.Revit.DB import (FilteredElementCollector,
                               BuiltInCategory,
                               BuiltInParameter,
                               ViewSheet)
from pyrevit.forms import SelectFromList
from pyrevit import forms

from Snippets.variables import ALL_VIEW_TYPES
import sys

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GET ELEMENTS

def get_selected_elements():
    """Property that retrieves selected views or promt user to select some from the dialog box."""
    selected_elements = []

    #>>>>>>>>>> VIEWS SELECTED IN UI
    for element_id in uidoc.Selection.GetElementIds():
        element = doc.GetElement(element_id)
        selected_elements.append(element)

    if not selected_elements:
        forms.alert("No elements  were selected.\nPlease, try again.", exitscript=True)
    return selected_elements







#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GET VIEWS

def get_selected_views(exit_if_none = False):
    """Function to get selected views.
    :return: list of selected views."""
    #>>>>>>>>>> GET SELECTED ELEMENTS
    UI_selected = uidoc.Selection.GetElementIds()

    #>>>>>>>>>> FILTER SELECTION
    selected_views = [doc.GetElement(view_id) for view_id in UI_selected if type(doc.GetElement(view_id)) in ALL_VIEW_TYPES]

    #>>>>>>>>>> EXIT IF NONE SELECTED
    if not selected_views and exit_if_none:
        forms.alert("No views were selected. Please try again.", exitscript=True)

    return selected_views

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GET SHEETS
def get_selected_sheets(exit_if_none = False):
    """Function to get selected views.
    return list of selected views."""
    #>>>>>>>>>> GET SELECTED ELEMENTS
    UI_selected = uidoc.Selection.GetElementIds()

    #>>>>>>>>>> FILTER SELECTION
    selected_sheets = [doc.GetElement(sheet_id) for sheet_id in UI_selected if type(doc.GetElement(sheet_id)) == ViewSheet ]

    #>>>>>>>>>> EXIT IF NONE SELECTED
    if not selected_sheets and exit_if_none:
        forms.alert("No sheets were selected. Please try again.", exitscript=True)

    return selected_sheets






#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SELECT TITLEBLOCK


def select_title_block():
    """Function to let user select a title block."""

    #>>>>>>>>>> SELECT TITLE BLOCK
    all_title_blocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().ToElements()
    unique_title_blocks = {}
    for tb in all_title_blocks:
        family_name = tb.FamilyName
        type_name = tb.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        unique_title_blocks["{} - {}".format(family_name, type_name)] = tb.Id

    #>>>>>>>>>> MAKE SURE IT'S SELECTED
    selected_option = SelectFromList.show(list(unique_title_blocks), title="Select Title Block")
    if not selected_option:
        forms.alers("Nothing was selected. Please try again", exitscript=True)

    selected_title_block = unique_title_blocks[selected_option]
    return selected_title_block


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PICK WALL

#>>>>>>>>> LIMIT SELECTION
class CustomISelectionFilter(ISelectionFilter):
    """Filter user selection to certain element."""
    def __init__(self, nom_categorie):
        self.nom_categorie = nom_categorie

    def AllowElement(self, e):
        if str(e.Category.Id) == str(self.nom_categorie):
        #if e.Category.Name == "Walls"
            return True
        else:
            return False
    def AllowReference(self, ref, point):
        return true

#>>>>>>>>>> PICK WALL
def pick_wall():
    """Function to promt user to select a wall element."""
    wall_id = uidoc.Selection.PickObject(ObjectType.Element, CustomISelectionFilter("-2000011"), "Select a Wall")    # -2000011 <- Id of OST_Walls
    wall = doc.GetElement(wall_id)
    return wall


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>