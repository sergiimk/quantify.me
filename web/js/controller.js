var app = angular.module('App', ['angularExtApp']);

app.controller('qmController', function($scope) {
    $scope.events = Quantify.getData();
});