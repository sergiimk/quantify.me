function chartAssets() {
	function my(selection) {
		var data = selection.datum()
			.map((g, i) => ({
				type: 'scatter',
				mode: 'none',
				fill: i == 0 ? 'tozeroy' : 'tonexty',
				name: g.name,
				x: g.events.map(e => e.t),
				y: g.events.reduce(
					(acc, e) => {
						acc.push(acc.length > 0
							? acc[acc.length - 1] + e.delta
							: e.delta);
						return acc;
					},
					[]
				),
			}));

		var layout = {
			margin: { t: 0 }
		};

		Plotly.plot(
			document.getElementById(selection.attr('id')),
			data,
			layout,
		);
	};

	return my;
}