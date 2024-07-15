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

    def corner_multiply(self, other):
        """Multiply this cubie cube with another cubie cube b, restricted to the corners.
        Does not change b.
        """

        c_perm = [0] * 8
        c_ori = [0] * 8

        for c in Corner:
            c_perm[c] = self.cp[other.cp[c]]
            ori_a = self.co[other.cp[c]]
            ori_b = other.co[c]

            if ori_a < 3:
                if ori_b < 3:
                    ori = (ori_a + ori_b) - 3 if ori_a + ori_b >= 3 else ori_a + ori_b
                else:
                    ori = (ori_a + ori_b) - 3 if ori_a + ori_b >= 6 else ori_a + ori_b
            else:
                if ori_b < 3:
                    ori = (ori_a - ori_b) + 3 if ori_a - ori_b < 3 else ori_a - ori_b
                else:
                    ori = (ori_a - ori_b) + 3 if ori_a - ori_b < 0 else ori_a - ori_b
            c_ori[c] = ori

        for c in Corner:
            self.cp[c] = c_perm[c]
            self.co[c] = c_ori[c]

    def edge_multiply(self, other):
        """ Multiply this cubie cube with another cubiecube b, restricted to the edges. Does not change b."""
        e_perm = [0] * 12
        e_ori = [0] * 12
        for e in Edge:
            e_perm[e] = self.ep[other.ep[e]]
            e_ori[e] = (other.eo[e] + self.eo[other.ep[e]]) % 2
        for e in Edge:
            self.ep[e] = e_perm[e]
            self.eo[e] = e_ori[e]

    def multiply(self, other):
        self.corner_multiply(other)
        self.edge_multiply(other)

    def inv_rough_cube(self, other):
        """Store the inverse of this rough cube in d."""
        for e in Edge:
            other.ep[self.ep[e]] = e
        for e in Edge:
            other.eo[e] = self.eo[other.ep[e]]

        for c in Corner:
            other.cp[self.cp[c]] = c
        for c in Corner:
            ori = self.co[other.cp[c]]
            if ori >= 3:
                other.co[c] = ori
            else:
                other.co[c] = -ori if other.co[c] >= 0 else other.co[c] + 3

    def corner_parity(self):
        """Give the parity of the corner permutation."""
        s = 0
        for i in range(Corner.DRB, Corner.URF, -1):
            for j in range(i - 1, Corner.URF - 1, -1):
                if self.cp[j] > self.cp[i]:
                    s += 1
        return s % 2

    def edge_parity(self):
        """Give the parity of the edge permutation. A solvable cube has the same corner and edge parity."""
        s = 0
        for i in range(Edge.BR, Edge.UR, -1):
            for j in range(i - 1, Edge.UR - 1, -1):
                if self.ep[j] > self.ep[i]:
                    s += 1
        return s % 2

    def symmetries(self):
        """Generate a list of the symmetries and antisymmetries of the cubie cube."""
        from symmetries import symCube, inv_idx  # not nice here but else we have circular imports
        s = []
        d = CubieCube()
        for j in range(N_SYM):
            c = CubieCube(symCube[j].cp, symCube[j].co, symCube[j].ep, symCube[j].eo)
            c.multiply(self)
            c.multiply(symCube[inv_idx[j]])
            if self == c:
                s.append(j)
            c.inv_cubie_cube(d)
            if self == d:  # then we have antisymmetry
                s.append(j + N_SYM)
        return s

    @classmethod
    def from_facecube(cls, facecube:FaceCube):
        """Return a cubie representation of the facelet cube."""
        co = list()
        cp = list()
        eo = list()
        ep = list()

        # find every corner and its orientation
        for corner in cornerFacelet:
            for i in range(3):
                if (facecube.facelets[corner[i]] == Color.U
                        or facecube.facelets[corner[i]] == Color.D):
                    source = [facecube.facelets[corner[i]],
                              facecube.facelets[corner[(i + 1) % 3]],
                              facecube.facelets[corner[(i + 2) % 3]]]
                    co.append(i)
                    cp.append(cornerColor.index(source))
                    break

        for edge in edgeFacelet:
            source = [facecube.facelets[edge[0]],
                      facecube.facelets[edge[1]]]
            if source in edgeColor:
                ep.append(edgeColor.index(source))
                eo.append(0)
            else:
                source.reverse()
                ep.append(edgeColor.index(source))
                eo.append(1)

        return cls(cp, co, ep, eo)
