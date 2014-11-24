angular.module('app', ['ngRoute', 'ui.bootstrap', 'angularFileUpload'])

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
        quantify.loginAccount(
            $scope.credentials.email,
            $scope.credentials.password
        ).success(function (data, status, headers, config) {
            state.account_id = data.account_id;
            state.access_token = data.access_token;
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
            alert("Failed to create user:\n[" + status + "] " + data);
        });
    };
})

///////////////////////////////////////////////////////////
// Dashboard
///////////////////////////////////////////////////////////

.controller('dashboardController', function($scope, $location, state, quantify) {
    $scope.data = null;

    $scope.getData = function() {
        quantify.getData(
            state.account_id,
            state.access_token
        ).success(function (data, status, headers, config) {
            $scope.data = data;
        }).error(function (data, status, headers, config) {
            alert("Failed to load sensor data:\n[" + status + "] " + data);
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

    $scope.uploader.onCompleteItem = function(item, response, status, headers) {
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


;
