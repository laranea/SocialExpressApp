from reportlab.graphics.charts.linecharts import HorizontalLineChart

class HorizontalChartNew(HorizontalLineChart):

    def calcPositions_xy(self):
        """Works out where they go.
        Sets an attribute _positions which is a list of
        lists of (x, y) matching the data.
        """
        vA, cA = self.valueAxis, self.categoryAxis
        vA.setPosition(self.x, self.y, self.height)
        if vA: vA.joinAxis = cA
        if cA: cA.joinAxis = vA
        vA.configure(self.data)
        # If zero is in chart, put x axis there, otherwise
        # use bottom.
        xAxisCrossesAt = vA.scale(0)
        if ((xAxisCrossesAt > self.y + self.height) or (xAxisCrossesAt < self.y)):
            y = self.y
        else:
            y = xAxisCrossesAt
        cA.setPosition(self.x, y, self.width)
        cA.configure(self.data)

        self._seriesCount = len(self.data)
        self._rowLength = max(map(len,self.data))
        if self.useAbsolute:
            # Dimensions are absolute.
            normFactor = 1.0
        else:
            # Dimensions are normalized to fit.
            normWidth = self.groupSpacing
            availWidth = self.categoryAxis.scale(0)[1]
            normFactor = availWidth / normWidth

        self._positions = []
        for rowNo in range(len(self.data)):
            lineRow = []
            for colNo in range(len(self.data[rowNo])):          
                datum = self.data[rowNo][colNo]
                if datum is not None:
                    (groupX, groupWidth) = self.categoryAxis.scale(colNo)
                    x = groupX + (0.5 * self.groupSpacing * normFactor)
                    y = self.valueAxis.scale(0)
                    height = self.valueAxis.scale(datum) - y
                    lineRow.append((x, y+height))
            self._positions.append(lineRow)
        return self._positions
    
    def map_optima(self, optima):
        """Works out where they go.
        Sets an attribute _positions which is a list of
        lists of (x, y) matching the data.
        """
        vA, cA = self.valueAxis, self.categoryAxis
        vA.setPosition(self.x, self.y, self.height)
        if vA: vA.joinAxis = cA
        if cA: cA.joinAxis = vA
        vA.configure(self.data)
        # If zero is in chart, put x axis there, otherwise
        # use bottom.
        xAxisCrossesAt = vA.scale(0)
        if ((xAxisCrossesAt > self.y + self.height) or (xAxisCrossesAt < self.y)):
            y = self.y
        else:
            y = xAxisCrossesAt
        cA.setPosition(self.x, y, self.width)
        cA.configure(self.data)

        self._seriesCount = len(self.data)
        self._rowLength = max(map(len,self.data))
        if self.useAbsolute:
            # Dimensions are absolute.
            normFactor = 1.0
        else:
            # Dimensions are normalized to fit.
            normWidth = self.groupSpacing
            availWidth = self.categoryAxis.scale(0)[1]
            normFactor = availWidth / normWidth

        self._positions = []
        for rowNo in range(len(self.data)):
            lineRow = []
            #for colNo in range(len(self.data[rowNo])):
            if optima is not None:
                for colNo in optima:
                    datum = self.data[rowNo][colNo]
                    if datum is not None:
                        print rowNo, colNo
                        print datum
                        (groupX, groupWidth) = self.categoryAxis.scale(colNo)
                        x = groupX + (0.5 * self.groupSpacing * normFactor)
                        y = self.valueAxis.scale(0)
                        height = self.valueAxis.scale(datum) - y
                        lineRow.append((x, y+height))
                    
            self._positions.append(lineRow)
        return self._positions
