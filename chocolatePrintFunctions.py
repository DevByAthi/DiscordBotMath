

def printSingleCut(barHeight, barLength, cutIndex, cutDirection):
    """Given chocolate bar dimensions, a location to cut, and an orientation, print a graphical display of the cut.
    
    barLength and barHeight are positive integers referring to the size of the bar before splitting. cutIndex is a positive integer 
    referring to the where on the bar the cut is located. cutDirection is an integer used to describe whether the cut is horizontal or vertical.
    
    The indexing scheme is such that (0,0) refers to the upper left point on the bar.
    A cutDirection of 0 refers to a horizontal cut, and a cutDirection of 1 refers to a vertical cut."""

    # Input checking
    assert cutDirection == 0 or cutDirection == 1
    assert barHeight > 1
    assert barLength > 1
    if cutDirection == 1:
        assert 0 < cutIndex < barLength
    elif cutDirection == 0:
        assert 0 < cutIndex < barHeight

    imageToReturn = str()
    i = 0
    while i < barHeight+1:
        # This must be a while loop in order to allow us to modify the loop counter variable
        # from within, for the horizontal cut case where that is necessary for proper printing.
        currentLine = str()
        if i == 0:
            verticalChar = "."
        else:
            verticalChar = "|"

        for j in range(0,barLength):
            if cutDirection == 1 and cutIndex == j:
                # The cut is vertical. Thus it may occur at any of the horizontal indices.
                currentLine += verticalChar + " x " + verticalChar + "__"
            elif cutDirection == 0 and cutIndex == i:
                # This entire line is a cut
                currentLine += "\u0332".join("xxx") + "\u0332"
            else:
                # A normal segment
                currentLine += verticalChar + "__"

        # At the end of the line, add the final vertical character.
        if cutDirection == 0 and cutIndex == i:
            currentLine += "x" + "\u0332"
        else:
            currentLine += verticalChar

        # If the cut is horizontal, we'll need to print another row to avoid losing squares.
        if cutDirection == 0 and cutIndex == i:
            cutIndex = -1
            i -= 1

        imageToReturn += currentLine
        if i != barHeight:
            imageToReturn += "\n"
            
        i += 1

    return imageToReturn


# Testing ground
print(printSingleCut(3,6,4,1))
print(printSingleCut(3,4,2,0))
