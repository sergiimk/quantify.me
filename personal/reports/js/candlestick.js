function chartCandlestick() {
	function my(selection) {
		var margin = {top: 20, right: 20, bottom: 30, left: 50};
		var width = 960 - margin.left - margin.right;
		var height = 500 - margin.top - margin.bottom;

		var xScale = techan.scale.financetime()
			.range([0, width]);
		var yScale = d3.scaleLinear()
			.range([height, 0]);

		var plot = techan.plot.candlestick()
			.xScale(xScale)
			.yScale(yScale);

		plot.accessor()
			.date(d => d.date)
			.open(d => d.open)
			.high(d => d.high)
			.low(d => d.low)
			.close(d => d.close);

		var xAxis = d3.axisBottom()
			.scale(xScale);

		var yAxis = d3.axisLeft()
			.scale(yScale);

		var svg = selection
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		svg.append("clipPath")
			.attr("id", "clip")
			.append("rect")
			.attr("x", 0)
			.attr("y", yScale(1))
			.attr("width", width)
			.attr("height", yScale(0) - yScale(1));

		svg.append("g")
			.attr("class", "candlestick")
			.attr("clip-path", "url(#clip)");

		svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")");

		svg.append("g")
			.attr("class", "y axis");

		xScale.domain(selection.datum().map(plot.accessor().d));
		yScale.domain(techan.scale.plot.ohlc(selection.datum(), plot.accessor()).domain());

		svg.select("g.candlestick").call(plot);
		svg.selectAll("g.x.axis").call(xAxis);
		svg.selectAll("g.y.axis").call(yAxis);
	};

	return my;
}
