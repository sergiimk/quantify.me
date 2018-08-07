function group_by_sorted(arr, key) {
	var res = [{key: null}];
	for(var i = 0; i != arr.length; i++) {
		k = key(arr[i])
		if(res[res.length - 1].key == k)
			res[res.length - 1].values.push(arr[i]);
		else
			res.push({key: k, values: [arr[i]]});
	}
	res.shift();
	return res;
}


function aggregate_candlestick(events, time_key) {
	return group_by_sorted(events, e => time_key(e.t).getTime())
		.map(function(g) {
			g.date = time_key(g.values[0].t);
			return g;
		})
		.map(function(g) {
			red = g.values.reduce(function(acc, el) {
				acc.delta = acc.delta + el.delta;
				acc.delta_low = acc.delta_low > acc.delta ? acc.delta : acc.delta_low;
				acc.delta_high = acc.delta_high < acc.delta ? acc.delta : acc.delta_high;
				return acc;
			}, {delta: 0, delta_low: 0, delta_high: 0});
			g.delta = red.delta;
			g.delta_low = red.delta_low;
			g.delta_high = red.delta_high;
			return g;
		})
		.reduce(function(acc, g) {
			var prev = 0;
			if(acc.length > 0) {
				prev = acc[acc.length - 1].close;
			}
			g.open = prev;
			g.close = g.open + g.delta;
			g.low = g.open + g.delta_low;
			g.high = g.open + g.delta_high;
			acc.push(g);
			return acc;
		}, [])
		.map(function(g) { g.values = '[...]'; return g});
}
