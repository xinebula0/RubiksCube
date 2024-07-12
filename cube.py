from cubedefs import Color, Corner, Edge, cornerFacelet, cornerColor, edgeFacelet, edgeColor


class FaceCube:
    """Represent a cube on the facelet level with 54 colored facelets."""
    colors = [Color.U, Color.R, Color.F, Color.D, Color.L, Color.B]

    def __init__(self):
        self.facelets = [color for color in self.colors for _ in range(9)]

    def __str__(self):
        return self.to_string()

    def from_string(self, facelets):
        """Construct a facelet cube from a string.
           See class Facelet(IntEnum) in enums.py for string format.
        """
        if len(facelets) < 54:
            return f'Error: Cube definition string {facelets} contains less than 54 facelets.'
        elif len(facelets) > 54:
            return f'Error: Cube definition string {facelets} contains more than 54 facelets.'
        cnt = [0 for _ in range(6)]

        for index, character in enumerate(facelets):
            for color in Color:
                if character == color.name:
                    self.facelets[index] = color
                    cnt[color.value] += 1
                    break

        if all(x == 9 for x in cnt):
            return True
        else:
            return 'Error: Cube definition string ' + facelets + ' does not contain exactly 9 facelets of each color.'

    def from_colors(self, colors):
        valid_colors = ["Y", "R", "B", "W", "O", "G"]
        facelets = ''
        for color in colors:
            if color not in valid_colors:
                return f'Error: Invalid color {color} in facelet colors.'
            for member in Color:
                if valid_colors.index(color) == member.value:
                    facelets += member.name
                    break
        self.from_string(facelets)

    def to_string(self):
        """Give a string representation of the facelet cube."""
        facelets = ''
        for i in range(54):
            for member in Color:
                if self.facelets[i] == member:
                    facelets += member.name
                    break

        return facelets

    def to_2dstring(self):
        """Give a 2dstring representation of a facelet cube."""
        s = self.to_string()
        r = '   ' + s[0:3] + '\n   ' + s[3:6] + '\n   ' + s[6:9] + '\n'
        r += s[36:39] + s[18:21] + s[9:12] + s[45:48] + '\n' + s[39:42] + s[21:24] + s[12:15] + s[48:51] \
            + '\n' + s[42:45] + s[24:27] + s[15:18] + s[51:54] + '\n'
        r += '   ' + s[27:30] + '\n   ' + s[30:33] + '\n   ' + s[33:36] + '\n'
        return r

    @classmethod
    def from_roughcube(cls, roughcube):
        """Return a facelet representation of the cube."""
        fc = cls()
        for i in Color:
            j = roughcube.cp[i]  # corner j is at corner position i
            ori = roughcube.co[i]  # orientation of C j at position i
            for k in range(3):
                fc.facelets[cornerFacelet[i][(k + ori) % 3]] = cornerColor[j][k]
        for i in Edge:
            j = roughcube.ep[i]  # similar for Es
            ori = roughcube.eo[i]
            for k in range(2):
                fc.facelets[edgeFacelet[i][(k + ori) % 2]] = edgeColor[j][k]
        return fc


class RoughCube:
    """Represent a cube on level 1 with 8 corner cubies, 12 edge cubies and the cubie orientations.

    Is also used to represent:
    1. the 18 cube moves
    2. the 48 symmetries of the cube.
    """
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        """
        Initializes corners and edges.
        :param cp: corner permutation
        :param co: corner orientation
        :param ep: edge permutation
        :param eo: edge orientation
        """
        self.cp = cp.copy() if cp else [member for member in Corner]
        self.co = co.copy() if co else [0] * 8
        self.ep = ep.copy() if ep else [member for member in Edge]
        self.eo = eo.copy() if eo else [0] * 12

    def __str__(self):
        """Print string for a rough cube."""
        s = ''
        for member in Color:
            s += '(' + str(self.cp[member]) + ',' + str(self.co[member]) + ')'
        s += '\n'
        for member in Edge:
            s += '(' + str(self.ep[member]) + ',' + str(self.eo[member]) + ')'
        return s

    def __eq__(self, other):
        """Define equality of two rough cubes."""
        if self.cp == other.cp and self.co == other.co and self.ep == other.ep and self.eo == other.eo:
            return True
        else:
            return False

    @classmethod
    def to_facecube(cls, facecube:FaceCube):
        """Return a cubie representation of the facelet cube."""
        for member in Corner:
            fac = cornerFacelet[member]  # find every corner and its orientation
            for i in range(3):
                if (facecube.facelets[fac[i]] == Color.U
                        or facecube.facelets[fac[i]] == Color.D):
                    break

        cc = cls()
        cc.cp = [-1] * 8  # invalidate corner and edge permutation
        cc.ep = [-1] * 12
        for i in Corner:
            fac = cornerFacelet[i]  # facelets of corner  at position i
            ori = 0
            for ori in range(3):
                if self.f[fac[ori]] == Color.U or self.f[fac[ori]] == Color.D:
                    break
            col1 = self.f[fac[(ori + 1) % 3]]  # colors which identify the corner at position i
            col2 = self.f[fac[(ori + 2) % 3]]
            for j in Corner:
                col = cornerColor[j]  # colors of corner j
                if col1 == col[1] and col2 == col[2]:
                    cc.cp[i] = j  # we have corner j in corner position i
                    cc.co[i] = ori
                    break

        for i in Edge:
            for j in Edge:
                if self.f[edgeFacelet[i][0]] == edgeColor[j][0] and \
                        self.f[edgeFacelet[i][1]] == edgeColor[j][1]:
                    cc.ep[i] = j
                    cc.eo[i] = 0
                    break
                if self.f[edgeFacelet[i][0]] == edgeColor[j][1] and \
                        self.f[edgeFacelet[i][1]] == edgeColor[j][0]:
                    cc.ep[i] = j
                    cc.eo[i] = 1
                    break
        return cc