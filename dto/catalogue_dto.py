"""
Data Transfer object (DTO) for catalogue entity
"""

class catalogue:
    """
    Represents a catalogue item.

    :param catalogue_name: Name of the catalogue.
    :type catalogue_name: str
    :param catalogue_description: Description of the catalogue.
    :type catalogue_description: str
    :param effective_from: Start date of the catalogue's validity.
    :type effective_from: str
    :param effective_to: End date of the catalogue's validity.
    :type effective_to: str
    :param status: Status of the catalogue (e.g., active, inactive).
    :type status: str
    """


    def __init__(self,catalogue_name:str, catalogue_description:str, effective_from:str, effective_to:str, status:str) ->None:
        self.catalogue_name =catalogue_name
        self.catalogue_description = catalogue_description
        self.effective_from = effective_from
        self.effective_to= effective_to
        self.status = status




