var chart = chartCandlestick();
var g_chartAssetsStacked = chartAssets();


d3.json("data/all_in_one.json").then(function(data) {
	data.forEach(g => {
		g.events.forEach(e => { e.t = d3.isoParse(e.t); });
	});


	d3.select("#candlestick")
		.datum(
			aggregate_candlestick(
				data.find(g => g.name == 'Scotiabank - Chequing').events,
				(t) => new Date(Date.UTC(t.getFullYear(), t.getMonth(), 1))))
		.call(chart);

	d3.select('#assets-stacked')
		.datum(data.filter(g => g.name != 'Location'))
		.call(g_chartAssetsStacked);
});





var map = mapTravel();

d3.json("https://d3js.org/world-50m.v1.json").then(function(world) {
	d3.select('#map')
		.datum(world)
		.call(map);
});
