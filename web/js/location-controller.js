var app = angular.module('App', ['angularExtApp', 'googlechart']);

app.controller('locController', function($scope, $http) {

    function aggregate(data, key_prop, value_prop) {
        var map = {};
        for(var i = 0; i != data.length; ++i) {
            var el = data[i];
            var key = el[key_prop];
            var value = el[value_prop];

            if(!map.hasOwnProperty(key))
                map[key] = value;
            else
                map[key] += value;
        }

        return map;
    }

    function linearize(map) {
        var ret = [];

        for(var key in map) {
            if(!map.hasOwnProperty(key))
                continue;

            var val = map[key] / 3600 / 24;
            val = !val ? 0 : Math.log(val);
            ret.push([key, val]);
        }

        return ret;
    }

    function getCityChartData(data) {
        return linearize(aggregate(data, 'city', 'duration'));
    }

    function getCountryChartData(data) {
        return linearize(aggregate(data, 'country', 'duration'));
    }

    $scope.events = [];

    $scope.cityChart =
    {
        data: [ ['City', 'Stay'] ],
        type: "GeoChart",
        displayed: true,
        options: {
            displayMode: 'markers',
            colorAxis: {colors: ['#bbbbff', '#0000ff']}
        }
    };

    $scope.countryChart =
    {
        data: [ ['Country', 'Stay'] ],
        type: "GeoChart",
        displayed: true,
        options: {
            displayMode: 'regions',
            colorAxis: {colors: ['#bbbbff', '#0000ff']}
        }
    };

    $scope.refresh = function() {
        Quantify.getData($http).success(function(data) {
            $scope.events = data;
        });
    }
    $scope.refresh();

    $scope.$watch('events', function(events) {
        $scope.cityChart.data = [ ['City', 'Stay'] ].concat(getCityChartData(events));
        $scope.countryChart.data = [ ['Country', 'Stay'] ].concat(getCountryChartData(events));
    });
});