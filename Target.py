from dataclasses import dataclass


@dataclass
class _target:
    """
    DataClass to how info about a CCD Camera
    """

    def __init__(self, name: str, dso_list: list):
        self.name = name
        self.dso = dso_list


class AstroTarget:
    """
    Using the _target camera object. Create a collection, and allow this collection to be a list and searchable.
    """

    def __init__(self):
        self._targets = []
        self._targets.append(
            _target(
                "Top20",
                [
                    "M31 - Andromeda Galaxy",
                    "M42 - Orion Nebula",
                    "M45 - Pleiades",
                    "M13 - Hercules Globular Cluster",
                    "M51 - Whirlpool Galaxy",
                    "M81 - Bode's Galaxy",
                    "M82 - Cigar Galaxy",
                    "M33 - Triangulum Galaxy",
                    "M101 - Pinwheel Galaxy",
                    "M57 - Ring Nebula",
                    "M27 - Dumbbell Nebula",
                    "NGC 7000 - North America Nebula",
                    "NGC 0253 - Sculptor Galaxy",
                    "NGC 0869 - Double Cluster",
                    "M104 - Sombrero Galaxy",
                    "M20 - Trifid Nebula",
                    "M8 - Lagoon Nebula",
                    "M17 - Swan (Omega) Nebula",
                    "M4 - Globular Cluster in Scorpius",
                    "M87 - Virgo A Galaxy",
                ],
            )
        )
        self._targets.append(
            _target(
                "Winter",
                [
                    "M31 - Andromeda Galaxy",
                    "M42 - Orion Nebula",
                    "M45 - Pleiades",
                    "M51 - Whirlpool Galaxy",
                    "M81 - Bode's Galaxy",
                ],
            )
        )
        self._targets.append(
            _target(
                "Quick",
                [
                    "M31 - Andromeda Galaxy",
                    "M42 - Orion Nebula",
                    "M45 - Pleiades",
                ],
            )
        )

    def dump(self):
        """
        Just output the names and details of the objects.
        """
        print("#### Current Defined Astro Cameras  #####")
        for target in self._targets:
            print(f"Name {target.name} {target.dso}")

    def find(self, wanted: str) -> Optional(_target):
        """
        wanted: str. The name of the DSO target collection. No leading or trailing spaces.

        returns: _target object if found  - else None
        """
        for target in self._targets:
            if target.name == wanted:
                return target
        return None


if __name__ == "__main__":
    print("Test _Target")
    test = AstroTarget()
    test.dump()
    if test.find("Top20"):
        print("✔ Found Valid Target worked")
    else:
        print("✖ Found Valid Target failed ")
    if test.find("fake101"):
        print("✖ Found InValid Target THIS IS WRONG")
    else:
        print("✔ Found InValid Target failed. ")
