use library
printjson(db.books.findOne({ title: "XSLT Quickly" }, { title: 1, publishedDate: 1 }))
db.books.findOne({ title: "XSLT Quickly" }, { title: 1, publishedDate: 1 })
print(EJSON.stringify(db.books.findOne({ title: "XSLT Quickly" }, { title: 1, publishedDate: 1 }), null, 2))
print(JSON.stringify(db.books.findOne({ title: "XSLT Quickly" }, { title: 1, publishedDate: 1 }), null, 2))
db.books.find({ categories: "Python" }, { title: 1, _id: 0 }).pretty()
db.books.find({ categories: "Python" }, { title: 1, pageCount: 1, _id: 0 }).forEach(printjson)
var filter = { categories: "Python" }
var fields = { title: 1, pageCount: 1, _id: 0 }
db.books.find(filter, fields)
var filter = { categories: "Perl" }
db.books.countDocuments(filter)
const f2 = { status: "MEAP" }
const f2 = { status: "PUBLISH" }
let n = db.books.countDocuments({ status: "MEAP" })
n
var b = db.books.findOne({ title: "MongoDB in Action, Second Edition" })
b.authors
b.authors.length
var top = db.books.find({}, { title: 1, pageCount: 1, _id: 0 }).sort({ pageCount: -1 }).limit(3).toArray()
top.length
top[0].title
db.books.find({ pageCount: { $gt: 1000 } }, { title: 1 })
db.books.find({}, { title: 1, _id: 0 }).sort({ pageCount: 1 }).limit(3)
db.books.find({ pageCount: { $gt: 0 } }, { title: 1, pageCount: 1, _id: 0 }).sort({ pageCount: 1 }).limit(3)
db.books.find({ categories: "Java" })
it
