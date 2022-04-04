CREATE TABLE "movimientos"(
    "id" INTEGER,
    "fecha" TEXT NOT NULL,
    "hora" TEXT NOT NULL,
    "moneda_from" TEXT NOT NULL,
    "cantidad_from" REAL NOT NULL,
    "moneda_to" TEXT NOT NULL,
    "cantidad_to" REAL NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
)