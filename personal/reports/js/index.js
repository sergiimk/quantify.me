var chart = new CandlestickChart(d3.select("#chart"))
	.initPlot();

d3.json("data/all_in_one.json", function(error, data) {
	if (error) throw error;

	chq = data['Scotiabank - Chequing'];

	chq.map(function(e) {
		e.t = d3.isoParse(e.t);
		return e;
	});

	data = aggregate_candlestick(
		chq,
		(t) => new Date(Date.UTC(t.getFullYear(), t.getMonth(), 1))
	);

	data_view_populate(data);
	chart.datum(data);
	chart.draw();
});

function data_view_populate(data) {
	d3.select('#data')
		.selectAll('div')
		.data(data)
		.enter()
		.append('div')
		.text(function(d) {
			return JSON.stringify(d);
		});
}


var map = mapTravel();

d3.json("https://d3js.org/world-50m.v1.json", function(error, world) {
	if (error) throw error;

	d3.select('#map')
		.datum(world)
		.call(map);
});
