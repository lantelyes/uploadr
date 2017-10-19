    UPLOAD_DIRECTORY = "data/",
    API = {
        UPLOAD: {
            URL: "/upload",
            METHOD: "NONE"
        },
        DELETE: {
            URL: "/file?oid=",
            METHOD: "DELETE"
        },
        UPDATE: {
            URL: "/file",
            METHOD: "POST"
        },
        DOWNLOAD: {
            URL: "/file?oid=",
            METHOD: "get"
        }
    }