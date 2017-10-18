app.controller("MainController", function($scope, $http){ 

    $scope.isMenuOpen = false;

    $scope.fileList = [];


    $scope.menuToggle = function() {
        $scope.isMenuOpen = !$scope.isMenuOpen;
    }

    init = function()  {

// Simple GET request example:
    $http({
        method: 'GET',
        url: '/list'
    }).then(function successCallback(response) {

            $scope.fileList = response.data;

        }, function errorCallback(response) {

        });

    }


    init();

});