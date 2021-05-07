CREATE TABLE IF NOT EXISTS zabytki (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  inspire_id TEXT NOT NULL,
  forma_ochrony TEXT NOT NULL,
  dokladnosc_polozenia TEXT NOT NULL,
  nazwa TEXT NOT NULL,
  chronologia TEXT NOT NULL,
  funkcja TEXT NOT NULL,
  wykaz_dokumentow TEXT NOT NULL,
  data_wpisu TEXT NOT NULL,
  wojewodztwo TEXT NOT NULL,
  powiat TEXT NOT NULL,
  gmina TEXT NOT NULL,
  miejscowosc TEXT NOT NULL,
  ulica TEXT NOT NULL,
  nr_adresowy TEXT NOT NULL
);
