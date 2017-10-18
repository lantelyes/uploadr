app.controller("MainController", function($scope, $http, Upload, toastr){ 

    $scope.isMenuOpen = false;

    $scope.fileList = [];
    $scope.file = {};

    $scope.upload= function($file) {
         Upload.upload({
            url: API_URL + FILE_UPLOAD_URL,
            data: {file: $file},
        }).then(function (resp) {
            toastr.success("Upload Successful");
            populateFileList();
        }, function (resp) {
            toastr.error("Upload Failed");
        });
    }

    $scope.getDownloadLink = function(file) {

        return API_URL + FILE_DOWNLOAD_URL + file.name;

    }

    getExtentionFromFilename = function(filename){
        
        ext_split = filename.split(".");
        ext = ext_split[ext_split.length-1].toLowerCase();

        return ext;
    }

    $scope.getFileIcon = function(file) {

        ext = getExtentionFromFilename(file.name);
        
        switch(ext){
            case "doc":
            case "docx":
                return "fa-file-word-o"
            case "pdf":
                return "fa-file-pdf-o"
            default:
                return "fa-file"
        }

    }

    $scope.getFileType = function(file) {

        ext = getExtentionFromFilename(file.name);


        switch(ext){
            case "doc":
            case "docx":
                return "Word Document"
            case "pdf":
                return "PDF"
            default:
                return "Unknown"
        }

    }

    $scope.menuToggle = function() {
        $scope.isMenuOpen = !$scope.isMenuOpen;
    }

    $scope.editFileDescription = function(file) {
        console.log("edit");
        file.isEditingDescription = true;

    }

    $scope.saveFileDescription = function(file) {

        $http({
            method: 'POST',
            url: '/file',
            data: file
        }).then(function successCallback(response) {
                toastr.success("Succesfily saved file desciption");
                file.isEditingDescription = false
            }, function errorCallback(response) {
                toastr.error("Error saving file desciption");
        });

    }
    
    

    


    init = function()  {
        populateFileList();
    }



    populateFileList = function() {
        $http({
            method: 'GET',
            url: '/list'
        }).then(function successCallback(response) {
    
                $scope.fileList = response.data;
    
            }, function errorCallback(response) {
                console.log(response);
        });
    }

    init();

});