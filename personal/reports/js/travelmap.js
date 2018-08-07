function mapTravel() {
	function my(selection) {
		var svg = selection;
		var world = svg.datum();

		var width = +svg.attr("width");
		var height = +svg.attr("height");

		var projection = d3.geoPatterson()
			.scale(153)
			.translate([width / 2, height / 2])
			.precision(0.1);

		var path = d3.geoPath()
			.projection(projection);

		svg.append("path")
			.datum(d3.geoGraticule10())
			.attr("class", "graticule")
			.attr("d", path);

		svg.insert("path", ".graticule")
			.datum(topojson.feature(world, world.objects.land))
			.attr("class", "land")
			.attr("d", path);

		svg.insert("path", ".graticule")
			.datum(topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }))
			.attr("class", "boundary")
			.attr("d", path);
	};

	return my;
}
