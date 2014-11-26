angular.module('app', [
    'ngRoute',
    'ui.bootstrap',
    'hljs',
    'angularFileUpload',
    'googlechart',
])

///////////////////////////////////////////////////////////
// Config
///////////////////////////////////////////////////////////

.constant('config', {
    auth_base_url: 'http://boot2docker:8080',
    client_secret: 'web',
    data_base_url: 'http://boot2docker:8081',
})

.service('quantify', Quantify)

.service('state', function() {
    this.account_id = null;
    this.access_token = null;
})

.config(function($routeProvider) {
    $routeProvider
        .when('/login', {templateUrl: 'login.tpl.html'})
        .when('/register', {templateUrl: 'register.tpl.html'})
        .when('/new_user', {templateUrl: 'new_user.tpl.html'})
        .when('/dashboard', {templateUrl: 'dashboard.tpl.html'})
        .when('/import-export', {templateUrl: 'import-export.tpl.html'})
        .otherwise({redirectTo: '/login'})
})

///////////////////////////////////////////////////////////
// App
///////////////////////////////////////////////////////////

.controller('appController', function($scope, state) {
    $scope.state = state;
})

///////////////////////////////////////////////////////////
// Navigation
///////////////////////////////////////////////////////////

.controller('navController', function($scope, $location, state, quantify) {
    if(state.access_token == null) {
        $location.path('/login');
    }

    $scope.logout = function() {
        state.account_id = null;
        state.access_token = null;
        $location.path('/login');
    }
})

///////////////////////////////////////////////////////////
// Login
///////////////////////////////////////////////////////////

.controller('loginController', function($scope, $location, state, quantify) {
    if(state.access_token != null) {
        $location.path('/dashboard');
    }

    $scope.credentials = {
        email: '',
        password: '',
    };

    $scope.login = function() {
        $scope.inProgress = true;

        quantify.loginAccount(
            $scope.credentials.email,
            $scope.credentials.password
        ).success(function (data, status, headers, config) {
            state.account_id = data.account_id;
            state.access_token = data.access_token;
            $location.path('/dashboard');
        }).error(function (data, status, headers, config) {
            $scope.inProgress = false;

            console.error("Failed to login:\n[" + status + "] " + data);
            $scope.fault = true;
        });
    };
})

///////////////////////////////////////////////////////////
// Register
///////////////////////////////////////////////////////////

.controller('registerController', function($scope, $location, state, quantify) {
    $scope.account = {
        email: '',
        password: '',
        password2: '',
    };

    $scope.register = function() {
        if($scope.account.password != $scope.account.password2) {
            alert("Passwords do not match");
            return;
        }

        quantify.createAccount(
            $scope.account.email,
            $scope.account.password
        ).success(function (data, status, headers, config) {
            $location.path('/new_user');
        }).error(function (data, status, headers, config) {
            console.error("Failed to create user:\n[" + status + "] " + data);
            $scope.fault = true;
        });
    };
})

///////////////////////////////////////////////////////////
// Account
///////////////////////////////////////////////////////////

.controller('accountController', function($scope, $location, state, quantify, FileUploader) {
    $scope.exportDataUrl = quantify.getExportDataURL(state.account_id, state.access_token);

    $scope.uploader = new FileUploader({
        url: quantify.getImportDataURL(state.account_id, state.access_token),
    });

    $scope.uploader.onSuccessItem = function(item, response, status, headers) {
        alert('Uploaded successfully.');
    };

    $scope.uploader.onErrorItem = function(item, response, status, headers) {
        alert("Upload failed:\n[" + status + "] " + response);
    };

    $scope.deleteData = function() {
        quantify.deleteData(
            state.account_id,
            state.access_token
        ).success(function (data, status, headers, config) {
            alert('Data deleted successfully.')
        }).error(function (data, status, headers, config) {
            alert("Failed to delete data:\n[" + status + "] " + data);
        });
    }
})

///////////////////////////////////////////////////////////
// Dashboard
///////////////////////////////////////////////////////////

.controller('dashboardController', function($scope, $location, state, quantify) {
    $scope.data = null;
    $scope.data_str = null;

    $scope.getData = function() {
        console.info("Loading sensor data");

        quantify.getData(
            state.account_id,
            state.access_token
        ).success(function (data, status, headers, config) {
            $scope.data = data;
            $scope.data_str = JSON.stringify($scope.data, null, 2);
        }).error(function (data, status, headers, config) {
            alert("Failed to load sensor data:\n[" + status + "] " + data);
        });
    };
})

///////////////////////////////////////////////////////////
// Location
///////////////////////////////////////////////////////////

.controller('locationController', function($scope, $location, state, quantify) {
    // TODO: remove
    $scope.firstOpen = true;

    $scope.stayPerCity = null;
    $scope.stayPerCountry = null;

    $scope.cityChart =
    {
        type: "GeoChart",
        displayed: true,
        options: {
            width: 800,
            displayMode: 'markers',
            colorAxis: {colors: ['#bbbbff', '#0000ff']}
        },
        data: [ ['City', 'Stay'] ]
    };

    $scope.countryChart =
    {
        type: "GeoChart",
        displayed: true,
        options: {
            width: 800,
            displayMode: 'regions',
            colorAxis: {colors: ['#bbbbff', '#0000ff']}
        },
        data: [ ['Country', 'Stay'] ]
    };

    function calculateDuration(events) {
        var ret = [];
        for(var i = 0; i != events.length; ++i) {
            ret[i] = {duration: 0}
            for(var x in events[i])
                ret[i][x] = events[i][x]
        }

        for(var i = 1; i != events.length; ++i)
            ret[i - 1].duration =
                parseInt(events[i].ts) - parseInt(events[i - 1].ts);

        ret[ret.length - 1].duration =
            Math.floor(Date.now() / 1000) - parseInt(ret[i - 1].ts);

        return ret;
    };

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

    function logarithmicScale(map) {
        var ret = {};

        for(var key in map) {
            if(!map.hasOwnProperty(key))
                continue;

            var val = map[key] / 3600 / 24;
            ret[key] = !val ? 0 : Math.log(val);
        }

        return ret;
    }

    function getCityChartData(events) {
        var data = []
        if(events != null) {
            data = logarithmicScale(
                aggregate(
                    calculateDuration(events),
                    'city',
                    'duration'
                )
            );
        }

        var ret = []
        for(var key in data)
            ret.push([key, data[key]]);
        return ret;
    };

    function getCountryChartData(events) {
        var data = []
        if(events != null)
            data = logarithmicScale(
                aggregate(
                    calculateDuration(events),
                    'country',
                    'duration'
                )
            );

        var ret = []
        for(var key in data)
            ret.push([key, data[key]]);
        return ret;
    };

    // data -> stayPerCity, stayPerCountry
    $scope.$watch('data', function(events) {
        $scope.stayPerCity = events == null
            ? null
            : aggregate(
                calculateDuration(events),
                'city', 'duration');

        $scope.stayPerCountry = events == null
            ? null
            : aggregate(
                calculateDuration(events),
                'country', 'duration');
    });

    // stayPerCity -> cityChart.data
    $scope.$watch('stayPerCity', function(stayPerCity) {
        var logscale = logarithmicScale(stayPerCity);
        var val = [ ['City', 'Stay'] ];

        for(var key in logscale)
            val.push([key, logscale[key]]);

        $scope.cityChart.data = val;
    });

    // stayPerCity -> countryChart
    $scope.$watch('stayPerCountry', function(stayPerCountry) {
        var logscale = logarithmicScale(stayPerCountry);
        var val = [ ['Country', 'Stay'] ];

        for(var key in logscale)
            val.push([key, logscale[key]]);

        $scope.countryChart.data = val;
    });
})

///////////////////////////////////////////////////////////
// Location Add
///////////////////////////////////////////////////////////

.controller('locationAddController', function($scope, $location, state, quantify) {
    $scope.data = {
        date: new Date()
    };

    $scope.event = null;
    $scope.event_str = null;

    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.opened = true;
    };

    $scope.addLocation = function() {
        $scope.inProgress = true;
        console.info("Adding event:\n" + $scope.event_str);

        quantify.addData(
            state.account_id,
            state.access_token,
            [$scope.event]
        ).success(function (data, status, headers, config) {
            $scope.inProgress = false;
        }).error(function (data, status, headers, config) {
            $scope.inProgress = false;
            alert("Failed to load sensor data:\n[" + status + "] " + data);
        });
    };

    // event -> event_str
    $scope.$watch('data', function(data) {
        data.date.setUTCMilliseconds(0);
        data.date.setUTCSeconds(0);
        data.date.setUTCMinutes(0);
        data.date.setUTCHours(0);

        $scope.event = {
            type: 'location',
            t: data.date.toISOString(),
            country: data.country,
            city: data.city,
            transport: data.transport,
        };

        $scope.event_str = JSON.stringify($scope.event, null, 2);
    }, true);
})


;
