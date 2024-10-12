/* deletes posts table if it already exists*/

DROP TABLE IF EXISTS posts;

/* create the table */
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL
);