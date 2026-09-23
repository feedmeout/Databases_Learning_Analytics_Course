// NoSQL, Βραδιά 1, Μέρος 3: οι εντολές της επίδειξης, με τη σειρά των διαφανειών.
// Για αντιγραφή και επικόλληση στο mongosh, μία εντολή τη φορά (όχι με load(): τα show και use είναι εντολές του κελύφους).
// Τα ObjectId θα διαφέρουν από εκείνα των διαφανειών: περιέχουν τη στιγμή δημιουργίας.
// Επανάληψη από την αρχή: use world και μετά db.dropDatabase()

// Διαφάνεια 15: πλοήγηση
db
show dbs
use world
show collections

// Διαφάνεια 17: insertOne (και μετά ξανά show dbs)
db.country.insertOne({ name: "Greece", euSince: 1981, population: 10400000 })
show dbs

// Διαφάνεια 18: δικό μας _id
db.country.insertOne({ _id: 2, name: "Cyprus", population: 980000 })

// Διαφάνεια 19: insertMany
db.country.insertMany([
  { name: "France", euSince: 1958, population: 68600000,
    capital: { name: "Paris", timezone: "Europe/Paris" } },
  { name: "Germany", euSince: 1958, population: 83600000,
    capital: { name: "Berlin", timezone: "Europe/Berlin" } }
])

// Διαφάνεια 21: η τελεία στο όνομα πεδίου (και καθαρισμός)
db.country.insertOne({ name: "Italy", "capital.name": "Rome" })
db.country.findOne({ name: "Italy" })
db.country.find({ "capital.name": "Rome" })
db.country.deleteOne({ name: "Italy" })

// Διαφάνειες 22-24: ανάγνωση
db.country.findOne()
db.country.find({ name: "Greece" })
db.country.find({ "capital.name": "Paris" })

// Διαφάνεια 25: πλήθος
db.country.countDocuments()
db.country.countDocuments({ euSince: 1958 })

// Διαφάνεια 26: διαγραφή
db.country.deleteOne({ name: "Cyprus" })

// Διαφάνεια 28 (μετά τη δημοσκόπηση της 27)
db.country.find({ capital: "Paris" })
db.country.find({ "capital.name": "Paris" })
