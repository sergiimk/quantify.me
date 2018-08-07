
class CandlestickChart {

	constructor(svg) {
		this.svg = svg;

		this.margin = {top: 20, right: 20, bottom: 30, left: 50};
		this.width = 960 - this.margin.left - this.margin.right;
		this.height = 500 - this.margin.top - this.margin.bottom;

		this.xScale = techan.scale.financetime()
			.range([0, this.width]);
		this.yScale = d3.scaleLinear()
			.range([this.height, 0]);

		this.plot = techan.plot.candlestick()
			.xScale(this.xScale)
			.yScale(this.yScale);

		this.plot.accessor()
			.date(d => d.date)
			.open(d => d.open)
			.high(d => d.high)
			.low(d => d.low)
			.close(d => d.close);

		this.xAxis = d3.axisBottom()
			.scale(this.xScale);

		this.yAxis = d3.axisLeft()
			.scale(this.yScale);
	}

	initPlot() {
		this.svg = this.svg
			.attr("width", this.width + this.margin.left + this.margin.right)
			.attr("height", this.height + this.margin.top + this.margin.bottom)
			.append("g")
			.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

		this.svg.append("clipPath")
			.attr("id", "clip")
			.append("rect")
			.attr("x", 0)
			.attr("y", this.yScale(1))
			.attr("width", this.width)
			.attr("height", this.yScale(0) - this.yScale(1));

		this.svg.append("g")
			.attr("class", "candlestick")
			.attr("clip-path", "url(#clip)");

		this.svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + this.height + ")");

		this.svg.append("g")
			.attr("class", "y axis");

		var self = this;
		this.zoom = d3.zoom()
			.on("zoom", function() { self.on_zoom(); });

		this.svg.append("rect")
			.attr("class", "pane")
			.attr("width", this.width)
			.attr("height", this.height)
			.call(this.zoom);

		return this;
	}

	datum(data) {
		this.xScale.domain(data.map(this.plot.accessor().d));
		this.yScale.domain(techan.scale.plot.ohlc(data, this.plot.accessor()).domain());
		this.svg.selectAll("g.candlestick").datum(data);

		// Associate the zoom with the scale after a domain has been applied
		// Stash initial settings to store as baseline for zooming
		this.zoomableInit = this.xScale.zoomable().clamp(false).copy();

		return this;
	}

	draw() {
		this.svg.select("g.candlestick").call(this.plot);
		// using refresh method is more efficient as it does not perform any data joins
		// Use this if underlying data is not changing
		// this.svg.select("g.candlestick").call(candlestick.refresh);
		this.svg.selectAll("g.x.axis").call(this.xAxis);
		this.svg.selectAll("g.y.axis").call(this.yAxis);

		return this;
	}

	on_zoom() {
		var rescaledY = d3.event.transform.rescaleY(this.yScale);
		this.yAxis.scale(rescaledY);
		this.plot.yScale(rescaledY);

		// Emulates D3 behaviour, required for financetime due to secondary zoomable scale
		this.xScale.zoomable().domain(
			d3.event.transform.rescaleX(this.zoomableInit).domain());

		this.draw();
	}
}
