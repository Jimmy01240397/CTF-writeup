db.createCollection('users');
db.getCollection('users').insertMany([
    { username: 'admin', password: 'A153{this is FAKE flag but I will still see it in submission records}' }
]);
