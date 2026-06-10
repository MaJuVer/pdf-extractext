var dbName = process.env.MONGO_DB || 'pdf-extractext';
var appUser = process.env.MONGO_USER || 'pdfextractext26';
var appPass = process.env.MONGO_PASS || 'pdfextractext26';

var appDb = db.getSiblingDB(dbName);

appDb.createUser({
  user: appUser,
  pwd: appPass,
  roles: [
    {
      role: 'readWrite',
      db: dbName   
    }
  ]
});

appDb.createCollection('registros');
appDb.registros.createIndex({ "hash_contenido": 1 }, { unique: true });

print('====================================================================');
print('¡Base de datos "' + dbName + '" y usuario "' + appUser + '" creados con éxito!');
print('====================================================================');