angular.module('app', ['ngRoute'])

.constant('config', {
    auth_base_url: 'http://quantify.me:8080',
})

.service('quantify', Quantify)

.service('state', function() {
    this.account_id = null;
    this.access_token = null;
})

.config(function($routeProvider) {
    $routeProvider
        .when('/login', {templateUrl: 'login.tpl.html'})
        .when('/account', {templateUrl: 'account.tpl.html'})
        .otherwise({redirectTo: '/login'})
})



.controller('appController', function($scope, state) {
    $scope.state = state;
})



.controller('loginController', function($scope, $location, $window,
                                        config, state, quantify) {
    $scope.config = config;
    $scope.credentials = {
        email: '',
        password: '',
    };

    $scope.login = function() {
        quantify.loginAccount(
            $scope.credentials.email, $scope.credentials.password
        ).success(function (data, status, headers, config) {
            alert("Logged in:\n[" + status + "] " + data);
        }).error(function (data, status, headers, config) {
            alert("Failed to create user:\n[" + status + "] " + data);
        });
    };
})


;
