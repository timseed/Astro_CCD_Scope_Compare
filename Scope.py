from dataclasses import dataclass


@dataclass
class _scope:
    def __init__(self, name: str, focal_length_in_mm: int):
        """
        name:str  the Name of the scope. Please use UPPERCASE and No Spaces. SV555 REDCAT51 are fine etc.
        focal_length_in_mm:int The focal length of the scope in mm. Please note we do NOT care about the F-Stop (speed) of the lense.
        """
        self.name = name
        self.focal_length = focal_length_in_mm


class AstroScope:
    def __init__(self):
        self._scope = []
        self._scope.append(_scope("SV555", 243))
        self._scope.append(_scope("ASKAR71F", 490))
        self._scope.append(_scope("REDCAT51", 250))

    def dump(self):
        print("#### Current Defined Astro Scopes #####")
        for astroscope in self._scope:
            print(f"Name {astroscope.name} Focal Length:{astroscope.focal_length}")

    def find(self, wanted: str) -> Optional(_scope):
        """
        wanted: str. The name of the scope. Expected to be UPPERCASE - and with no leading or trailing spaces.

        returns: _scope object if found  - else None
        """
        for astroscope in self._scope:
            if astroscope.name == wanted:
                return astroscope
        return None


if __name__ == "__main__":
    print("Test _scope")
    test = AstroScope()
    test.dump()
    s = test.find("SV555")
    if s:
        print("✔ Found Valid Scope worked")
        if s.focal_length == 243:
            print("✔ Scope Focal length correct")
        else:
            print("✖ Scope Focal length failed")

    else:
        print("✖ Found Valid Scope failed ")
    if test.find("fake101"):
        print("✖ Found InValid Scope THIS IS WRONG")
    else:
        print("✔ Found InValid Scope failed. ")
