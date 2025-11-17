from dataclasses import dataclass


@dataclass
class _ccd:
    """
    DataClass to how info about a CCD Camera
    """

    def __init__(self, name: str, height_in_mm: float, width_in_mm: float):
        self.name = name
        self.height = height_in_mm
        self.width = width_in_mm


class AstroCamera:
    """
    Using the _ccd camera object. Create a collection, and allow this collection to be a list and searchable.
    """

    def __init__(self):
        self._ccds = []
        self._ccds.append(_ccd("imx585", 10.2, 12.2))
        self._ccds.append(_ccd("imx533", 11.2, 11.2))
        self._ccds.append(_ccd("asi1200", 23.2, 12.2))

    def dump(self):
        """
        Just output the names and details of the objects.
        """
        print("#### Current Defined Astro Cameras  #####")
        for astrocam in self._ccds:
            print(
                f"Name {astrocam.name} Width:{astrocam.width} Height:{astrocam.height}"
            )

    def find(self, wanted: str) -> Optional(_ccd):
        """
        wanted: str. The name of the CCD camera. Expected to be lowercase - and with no leading or trailing spaces.

        returns: _ccd object if found  - else None
        """
        for astrocam in self._ccds:
            if astrocam.name == wanted:
                return astrocam
        return None


if __name__ == "__main__":
    print("Test _ccd")
    test = AstroCamera()
    test.dump()
    if test.find("imx585"):
        print("✔ Found Valid camera worked")
    else:
        print("✖ Found Valid camera failed ")
    if test.find("fake101"):
        print("✖ Found InValid camera THIS IS WRONG")
    else:
        print("✔ Found InValid camera failed. ")
