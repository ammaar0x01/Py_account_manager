CREATE TABLE IF NOT EXISTS User_info(
    username BLOB       PRIMARY KEY UNIQUE NOT NULL,
    password BLOB       NOT NULL
); 

CREATE TABLE IF NOT EXISTS Service_accounts(
    account_num INTEGER         PRIMARY KEY, 
    account_username BLOB       NOT NULL, 
    account_password BLOB       NOT NULL, 
    Service TEXT(30)            NOT NULL, 
    username BLOB               NOT NULL REFERENCES User_info(username) 
    -- username TEXT(30)           NOT NULL REFERENCES User_info(username) 
);

CREATE TABLE IF NOT EXISTS Bookmarks(
    bookmark_num INTEGER    PRIMARY KEY, 
    website_name TEXT(30)   NOT NULL, 
    link TEXT(100), 
    comment TEXT(100), 
    username BLOB           NOT NULL REFERENCES User_info(username) 
    -- username TEXT(30)       NOT NULL REFERENCES User_info(username) 
);