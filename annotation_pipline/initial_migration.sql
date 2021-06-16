CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY,
    claim TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (url)
        REFERENCES fulltext (url)
);

CREATE TABLE IF NOT EXISTS fulltext (
    url TEXT NOT NULL,
    plaintext TEXT NOT NULL,
    saved_to_wayback_machine TEXT
);

CREATE TABLE IF NOT EXISTS "references" (
    id INTEGER NOT NULL,
    reference TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES claims (id)
);
