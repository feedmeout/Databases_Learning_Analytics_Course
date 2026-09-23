db
show dbs
use world
show collections
db.country.insertOne({ name: "Greece", euSince: 1981, population: 10400000 })
show dbs
db.country.insertOne({ _id: 2, name: "Cyprus", population: 980000 })
db.country.insertMany([
  { name: "France", euSince: 1958, population: 68600000,
    capital: { name: "Paris", timezone: "Europe/Paris" } },
  { name: "Germany", euSince: 1958, population: 83600000,
    capital: { name: "Berlin", timezone: "Europe/Berlin" } }
])
db.country.findOne()
db.country.find({ name: "Greece" })
db.country.find({ "capital.name": "Paris" })
db.country.countDocuments()
db.country.countDocuments({ euSince: 1958 })
db.country.insertOne({ name: "Italy", "capital.name": "Rome" })
db.country.findOne({ name: "Italy" })
db.country.find({ "capital.name": "Rome" })
db.country.deleteOne({ name: "Italy" })
db.country.deleteOne({ name: "Cyprus" })
db.country.find({ capital: "Paris" })
db.country.countDocuments()
