from cubedefs import Color, Edge, cornerFacelet, cornerColor, edgeFacelet, edgeColor


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
    def from_stage1cube(cls, stage1cube):
        """Return a facelet representation of the cube."""
        fc = cls()
        for i in Color:
            j = stage1cube.cp[i]  # corner j is at corner position i
            ori = stage1cube.co[i]  # orientation of C j at position i
            for k in range(3):
                fc.facelets[cornerFacelet[i][(k + ori) % 3]] = cornerColor[j][k]
        for i in Edge:
            j = stage1cube.ep[i]  # similar for Es
            ori = stage1cube.eo[i]
            for k in range(2):
                fc.facelets[edgeFacelet[i][(k + ori) % 2]] = edgeColor[j][k]
        return fc

