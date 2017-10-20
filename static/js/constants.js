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
            URL: "/file?name=",
            METHOD: "GET"
        },
        LIST: {
            URL: "/list?",
            METHOD: "GET"
        }
    }

    DEFAULT_SEARCH_OPTIONS = {
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