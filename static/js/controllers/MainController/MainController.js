app.controller("MainController", function($scope, $http, Upload, toastr){ 


    $scope.searchOptions = {
        query: "",
        extentions: {
            word: false,
            pdf: false
        },
        types: {
            name: false,
            contents: false,
        },
        caseSensitive: false
    };
    $scope.fileList = [];
    $scope.isMenuOpen = false;

    //Uplaod the selected file to the server
    $scope.upload= function($file) {
         Upload.upload({
            url: '/upload',
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
    
    //Get a normalized to lowercase extention from a filename
    getExtentionFromFilename = function(filename){
        
        ext_split = filename.split(".");
        ext = ext_split[ext_split.length-1].toLowerCase();

        return ext;
    }
    
    //Given a file object, return the appropriate icon class for use in the DOM
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

    //Given a file object, return its type based on its extention
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

    //Open the descripion editor
    $scope.editFileDescription = function(file) {
        file.isEditingDescription = true;
    }

    //Updatethe file descripion on the server
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

    //Build a query string to pass to the API for file searching
    buildQueryString = function(searchOptions) {
        queryString =  "query="+searchOptions.query + "&";

        if(searchOptions.extentions.word)
        {
            queryString += "ext=doc&ext=docx&"
        }
        if(searchOptions.extentions.pdf)
        {
            queryString += "ext=pdf&"
        }
        if(searchOptions.types.name)
        {
            queryString += "type=name"
        }
        if(searchOptions.types.contents)
        {
            queryString += "type=contents"
        }

        return queryString;
    }
    
    
    $scope.searchFiles = function()
    {

        queryString = buildQueryString($scope.searchOptions);
        $http({
            method: 'GET',
            url: '/list?' + queryString,
        }).then(function successCallback(response) {
                $scope.fileList = response.data;
            }, function errorCallback(response) {
                toastr.error("Error searching for files");
        });
    }
    


    init = function()  {
        populateFileList();
    }



    populateFileList = function() {
        $http({
            method: 'GET',
            url: '/list?query=&ext=pdf&ext=doc&ext=docx'
        }).then(function successCallback(response) {
    
                $scope.fileList = response.data;
    
            }, function errorCallback(response) {
                console.log(response);
        });
    }

    init();

});