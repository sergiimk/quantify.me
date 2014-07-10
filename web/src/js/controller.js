angular.module('app', ['ngRoute'])

///////////////////////////////////////////////////////////
// Config
///////////////////////////////////////////////////////////

.constant('config', {
    auth_base_url: 'http://localhost:8080',
    client_secret: 'web',
    data_base_url: 'http://localhost:8081',
})

.service('quantify', Quantify)

.service('state', function() {
    this.account_id = 1;
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
// Login
///////////////////////////////////////////////////////////

.controller('loginController', function($scope, $location, state, quantify) {
    $scope.credentials = {
        email: '',
        password: '',
    };

    $scope.login = function() {
        quantify.loginAccount(
            $scope.credentials.email,
            $scope.credentials.password
        ).success(function (data, status, headers, config) {
            $location.path('/dashboard');
        }).error(function (data, status, headers, config) {
            alert("Failed to login:\n[" + status + "] " + data);
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
    };

    $scope.register = function() {
        quantify.createAccount(
            $scope.account.email,
            $scope.account.password
        ).success(function (data, status, headers, config) {
            $location.path('/new_user');
        }).error(function (data, status, headers, config) {
            alert("Failed to create user:\n[" + status + "] " + data);
        });
    };
})

///////////////////////////////////////////////////////////
// Account
///////////////////////////////////////////////////////////

.controller('accountController', function($scope, $location, state, quantify) {
    $scope.exportDataUrl = quantify.getExportDataURL(state.account_id, state.access_token);
    $scope.importDataFile = null;

    $scope.importData = function() {
        quantify.importData(
            state.account_id,
            state.access_token,
            $scope.importDataFile
        ).success(function (data, status, headers, config) {
            alert('Data uploaded successfully.')
        }).error(function (data, status, headers, config) {
            alert("Failed to upload data:\n[" + status + "] " + data);
        });
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


;
